<template>
    <div class="consent-dashboard p-6 min-h-screen">
        <!-- Header Section -->
        <header class="mb-8 flex justify-between items-start">
            <div>
                <h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-2">Data Privacy & Consents</h1>
                <p class="text-gray-600 dark:text-gray-400">
                    Manage your data permissions in compliance with the Data Protection Act (2019).
                </p>
            </div>
            <router-link to="/profile"
                class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-sm font-bold transition-all flex items-center">
                <i class="fas fa-arrow-left mr-2"></i> Back to Profile
            </router-link>
        </header>

        <!-- Stats Row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="stats-card glass">
                <div class="flex items-center">
                    <div class="icon-box bg-blue-100 text-blue-600 mr-4">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500 uppercase font-semibold">Active Consents</p>
                        <p class="text-2xl font-bold">{{ activeCount }}</p>
                    </div>
                </div>
            </div>
            <div class="stats-card glass">
                <div class="flex items-center">
                    <div class="icon-box bg-green-100 text-green-600 mr-4">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500 uppercase font-semibold">Total Granted</p>
                        <p class="text-2xl font-bold">{{ consents.length }}</p>
                    </div>
                </div>
            </div>
            <div class="stats-card glass">
                <div class="flex items-center">
                    <div class="icon-box bg-red-100 text-red-600 mr-4">
                        <i class="fas fa-user-lock"></i>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500 uppercase font-semibold">Revoked / Expired</p>
                        <p class="text-2xl font-bold">{{ inactiveCount }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Inventory Table -->
        <div class="glass overflow-hidden rounded-2xl shadow-xl">
            <div class="p-6 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center">
                <h2 class="text-xl font-semibold">Consent Inventory</h2>
                <button @click="fetchConsents" class="btn-icon">
                    <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
                </button>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-50 dark:bg-gray-900/50 text-gray-500 text-xs uppercase tracking-wider">
                            <th class="px-6 py-4">Requester (MDA)</th>
                            <th class="px-6 py-4">Data Scope</th>
                            <th class="px-6 py-4">Purpose</th>
                            <th class="px-6 py-4">Granted At</th>
                            <th class="px-6 py-4">Expiry</th>
                            <th class="px-6 py-4">Status</th>
                            <th class="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                        <tr v-for="c in consents" :key="c.id"
                            class="hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors">
                            <td class="px-6 py-4 font-medium">
                                {{ c.requester_details?.name || 'Unknown MDA' }}
                                <span class="block text-xs text-gray-400 font-normal mt-1">{{ c.requester_details?.code
                                }}</span>
                            </td>
                            <td class="px-6 py-4">
                                <span class="scope-tag">{{ c.data_scope }}</span>
                            </td>
                            <td class="px-6 py-4 text-sm max-w-xs truncate">
                                {{ c.purpose_details?.description || c.purpose }}
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-500">
                                {{ formatDate(c.granted_at) }}
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-500">
                                {{ formatExpiry(c.expires_at) }}
                            </td>
                            <td class="px-6 py-4">
                                <span :class="statusClass(c.status)">
                                    {{ c.status }}
                                </span>
                            </td>
                            <td class="px-6 py-4 text-right">
                                <button v-if="c.status === 'ACTIVE'" @click="revoke(c.id)" class="btn-revoke"
                                    :disabled="revokingId === c.id">
                                    <i class="fas fa-ban mr-1"></i>
                                    {{ revokingId === c.id ? 'Revoking...' : 'Revoke' }}
                                </button>
                                <span v-else class="text-gray-400 text-xs">—</span>
                            </td>
                        </tr>
                        <tr v-if="consents.length === 0 && !loading">
                            <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                                <i class="fas fa-folder-open text-4xl mb-4 block opacity-20"></i>
                                No consent records found.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue';
    import ConsentService from '@/services/ConsentService';

    const consents = ref([]);
    const loading = ref(false);
    const revokingId = ref(null);

    const activeCount = computed(() => consents.value.filter(c => c.status === 'ACTIVE').length);
    const inactiveCount = computed(() => consents.value.length - activeCount.value);

    const fetchConsents = async () => {
        loading.value = true;
        try {
            const response = await ConsentService.getMyConsents();
            consents.value = response.data;
        } catch (error) {
            console.error('Error fetching consents:', error);
        } finally {
            loading.value = false;
        }
    };

    const revoke = async (id) => {
        if (!confirm('Are you sure you want to revoke this consent immediately? This may affect pending service requests.')) return;

        revokingId.value = id;
        try {
            await ConsentService.revokeConsent(id);
            await fetchConsents();
        } catch (error) {
            alert('Failed to revoke consent. Please try again.');
        } finally {
            revokingId.value = null;
        }
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return 'N/A';
        return new Date(dateStr).toLocaleDateString('en-KE', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    const formatExpiry = (dateStr) => {
        if (!dateStr) return 'Never';
        const date = new Date(dateStr);
        const now = new Date();
        const diffDays = Math.ceil((date - now) / (1000 * 60 * 60 * 24));

        if (diffDays < 0) return 'Expired';
        if (diffDays === 0) return 'Expires Today';
        return `${formatDate(dateStr)} (${diffDays}d left)`;
    };

    const statusClass = (status) => {
        const base = 'px-3 py-1 rounded-full text-xs font-bold ';
        if (status === 'ACTIVE') return base + 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
        if (status === 'REVOKED') return base + 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
        return base + 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400';
    };

    onMounted(fetchConsents);
</script>

<style scoped>
    .glass {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .dark .glass {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stats-card {
        @apply p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center;
    }

    .icon-box {
        @apply w-12 h-12 rounded-xl flex items-center justify-center text-xl shadow-inner;
    }

    .btn-icon {
        @apply w-10 h-10 flex items-center justify-center rounded-xl bg-gray-100 text-gray-600 hover:bg-gray-200 transition-all dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700;
    }

    .scope-tag {
        @apply py-1 px-2 rounded-md bg-blue-50 text-blue-600 text-xs font-mono dark:bg-blue-900/20 dark:text-blue-400;
    }

    .btn-revoke {
        @apply text-red-500 text-xs font-bold border border-red-200 px-3 py-1.5 rounded-lg hover:bg-red-500 hover:text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed;
    }

    .dark .btn-revoke {
        @apply border-red-900/50 hover:bg-red-900;
    }

    table thead th {
        @apply font-semibold;
    }
</style>
