<template>
    <div class="payment-widget glass p-6 rounded-2xl shadow-xl max-w-md mx-auto">
        <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-800 dark:text-white">Secure Checkout</h3>
            <div class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold">
                KES {{ amount.toLocaleString() }}
            </div>
        </div>

        <!-- State: Initial / Form -->
        <div v-if="state === 'form'" class="space-y-4">
            <div class="space-y-2">
                <label class="text-xs uppercase font-bold text-gray-500 tracking-wider">M-Pesa Phone Number</label>
                <div class="relative">
                    <span class="absolute left-4 top-3.5 text-gray-400 font-medium">+254</span>
                    <input v-model="phoneNumber" type="tel" placeholder="712345678"
                        class="w-full pl-16 pr-4 py-3 rounded-xl border border-gray-100 dark:border-gray-800 bg-white/50 dark:bg-gray-900/50 focus:ring-2 focus:ring-green-500 transition-all outline-none"
                        :disabled="loading" />
                </div>
            </div>

            <button @click="startPayment" :disabled="!isValidPhone || loading"
                class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-green-200 dark:shadow-none transition-all flex items-center justify-center transform active:scale-95 disabled:opacity-50 disabled:active:scale-100">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/M-PESA_LOGO-01.svg" alt="M-Pesa"
                    class="h-6 mr-3 bg-white p-0.5 rounded" />
                Pay with M-Pesa
            </button>

            <p class="text-[10px] text-center text-gray-400">
                By clicking, you will receive an STK Push prompt on your mobile phone to enter your M-Pesa PIN.
            </p>
        </div>

        <!-- State: Processing / Polling -->
        <div v-else-if="state === 'processing'" class="text-center py-8 space-y-6">
            <div class="relative mx-auto w-24 h-24">
                <div class="absolute inset-0 border-4 border-green-100 rounded-full"></div>
                <div class="absolute inset-0 border-4 border-green-600 rounded-full border-t-transparent animate-spin">
                </div>
                <div class="absolute inset-0 flex items-center justify-center text-green-600">
                    <i class="fas fa-mobile-alt text-3xl animate-bounce"></i>
                </div>
            </div>

            <div>
                <h4 class="text-lg font-bold text-gray-800 dark:text-white">Waiting for Payment...</h4>
                <p class="text-sm text-gray-500 mt-2">Check your phone ({{ fullPhone }}) and enter your M-Pesa PIN.</p>
            </div>

            <button @click="reset" class="text-xs text-blue-600 hover:underline">Change phone number</button>
        </div>

        <!-- State: Success -->
        <div v-else-if="state === 'success'" class="text-center py-8 space-y-4 animate-in fade-in zoom-in duration-300">
            <div
                class="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto text-4xl shadow-inner">
                <i class="fas fa-check"></i>
            </div>

            <div>
                <h4 class="text-lg font-bold text-gray-800 dark:text-white">Payment Received!</h4>
                <p class="text-sm text-gray-500">Transaction verified. Your request is being processed.</p>
            </div>
        </div>

        <!-- State: Error -->
        <div v-else-if="state === 'error'" class="text-center py-8 space-y-4">
            <div
                class="w-20 h-20 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto text-4xl shadow-inner">
                <i class="fas fa-times"></i>
            </div>

            <div>
                <h4 class="text-lg font-bold text-gray-800 dark:text-white">Payment Failed</h4>
                <p class="text-sm text-gray-500">{{ errorMessage }}</p>
            </div>

            <button @click="reset" class="btn-primary-sm w-full">Try Again</button>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onBeforeUnmount } from 'vue';
    import PaymentService from '@/services/PaymentService';

    const props = defineProps({
        amount: {
            type: Number,
            required: true
        },
        serviceRequestId: {
            type: String,
            required: true
        }
    });

    const emit = defineEmits(['payment-complete', 'payment-failed']);

    const state = ref('form'); // form, processing, success, error
    const phoneNumber = ref('');
    const loading = ref(false);
    const txnId = ref(null);
    const errorMessage = ref('');
    let pollInterval = null;

    const fullPhone = computed(() => `254${phoneNumber.value.replace(/^0/, '')}`);
    const isValidPhone = computed(() => {
        const clean = phoneNumber.value.replace(/^0/, '');
        return clean.length === 9 && /^[0-9]+$/.test(clean);
    });

    const startPayment = async () => {
        loading.value = true;
        state.value = 'processing';

        try {
            const response = await PaymentService.initiatePayment({
                request_id: props.serviceRequestId,
                phone_number: fullPhone.value,
                amount: props.amount,
                provider: 'MPESA'
            });

            if (response.data.status === 'SUCCESS') {
                txnId.value = response.data.transaction_id;
                startPolling();
            } else {
                throw new Error(response.data.message || 'Initiation failed');
            }
        } catch (err) {
            state.value = 'error';
            errorMessage.value = err.message || 'Platform could not connect to Payment Gateway.';
            emit('payment-failed', err.message);
        } finally {
            loading.value = false;
        }
    };

    const startPolling = () => {
        if (pollInterval) clearInterval(pollInterval);

        pollInterval = setInterval(async () => {
            try {
                const response = await PaymentService.checkStatus(txnId.value);
                const status = response.data.status;

                if (status === 'SUCCESS') {
                    clearInterval(pollInterval);
                    state.value = 'success';
                    emit('payment-complete', response.data);
                } else if (status === 'FAILED') {
                    clearInterval(pollInterval);
                    state.value = 'error';
                    errorMessage.value = 'Payment was cancelled or timed out.';
                }
                // If PENDING, continue polling
            } catch (err) {
                console.error('Polling error:', err);
            }
        }, 5000);
    };

    const reset = () => {
        if (pollInterval) clearInterval(pollInterval);
        state.value = 'form';
        errorMessage.value = '';
    };

    onBeforeUnmount(() => {
        if (pollInterval) clearInterval(pollInterval);
    });
</script>

<style scoped>
    .glass {
        @apply bg-white/70 backdrop-blur-xl border border-white/20 dark:bg-slate-900/60 dark:border-slate-800;
    }

    .btn-primary-sm {
        @apply bg-blue-600 text-white py-2 px-4 rounded-lg font-bold hover:bg-blue-700 transition-all;
    }
</style>
