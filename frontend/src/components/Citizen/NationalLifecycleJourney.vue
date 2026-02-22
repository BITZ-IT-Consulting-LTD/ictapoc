<template>
    <div class="lifecycle-journey u-mb-10">
        <div class="u-flex u-items-center u-justify-between u-mb-6">
            <div class="page__title-group">
                <h3 class="u-text-xl u-font-black u-text-main u-uppercase u-tracking-tighter">National Lifecycle <span
                        class="u-text-primary">Journey</span></h3>
                <p class="u-text-xs u-text-muted">Track your institutional milestones from cradle to death</p>
            </div>
            <div class="u-flex u-gap-2">
                <span class="badge badge--success badge--small">Verified Identity</span>
            </div>
        </div>

        <!-- Timeline Container -->
        <div class="lifecycle-track-wrapper u-relative u-py-8 u-px-4 u-overflow-x-auto">
            <div class="lifecycle-track u-flex u-gap-8 u-relative u-min-w-max">
                <!-- Connecting Line -->
                <div class="u-absolute u-top-12 u-left-10 u-right-10 u-h-1 u-bg-border-color/30 u-z-0">
                    <div class="u-h-full u-bg-gradient-to-r u-from-primary u-to-success transition-all duration-1000"
                        :style="{ width: progressPercentage + '%' }"></div>
                </div>

                <!-- Lifecycle Nodes -->
                <div v-for="(node, index) in lifecycleNodes" :key="node.code"
                    class="lifecycle-node u-relative u-z-10 u-w-64">

                    <!-- Node Marker -->
                    <div class="u-flex u-flex-col u-items-center u-mb-6">
                        <div class="u-w-12 u-h-12 u-rounded-full u-flex u-items-center u-justify-center u-transition-all u-duration-500 u-shadow-lg u-border-4"
                            :class="getNodeStatusClass(node)">
                            <i :class="[node.icon, isNodeActive(node) ? 'u-animate-pulse' : '']" class="u-text-lg"></i>
                        </div>
                    </div>

                    <!-- Node Card -->
                    <div class="card u-p-4 u-transition-all u-duration-300 hover:u-shadow-xl" :class="[
                        node.status === 'completed' ? 'u-border-success/30 u-bg-success-soft/5' : '',
                        node.status === 'in_progress' ? 'u-border-primary/30 u-bg-primary-soft/5' : '',
                        node.status === 'locked' ? 'u-opacity-60' : ''
                    ]">
                        <div class="u-flex u-items-center u-justify-between u-mb-2">
                            <span class="u-text-[9px] u-font-black u-uppercase u-tracking-[0.2em]"
                                :class="node.status === 'completed' ? 'u-text-success' : (node.status === 'in_progress' ? 'u-text-primary' : 'u-text-muted')">
                                {{ node.status.replace('_', ' ') }}
                            </span>
                            <i v-if="node.status === 'completed'"
                                class="bi bi-patch-check-fill u-text-success u-text-xs"></i>
                        </div>
                        <h4 class="u-text-sm u-font-black u-text-main u-mb-1">{{ node.name }}</h4>
                        <p class="u-text-[10px] u-text-muted u-mb-4 u-leading-tight">{{ node.description }}</p>

                        <div v-if="node.status === 'next'" class="u-mt-auto">
                            <router-link :to="`/apply/${node.code}`"
                                class="button button--primary button--small u-w-full">
                                Begin Stage
                            </router-link>
                        </div>
                        <div v-else-if="node.status === 'in_progress'" class="u-mt-auto">
                            <router-link :to="`/service-request/${node.requestId}`"
                                class="button button--secondary button--small u-w-full">
                                Track Progress
                            </router-link>
                        </div>
                        <div v-else-if="node.status === 'completed'" class="u-mt-auto u-flex u-items-center u-gap-2">
                            <span class="u-text-[10px] u-font-bold u-text-success u-uppercase">Credential Issued</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue';
    import { useCitizenStore } from '../../store/citizen';

    const citizenStore = useCitizenStore();

    const LIFECYCLE_SEQUENCE = [
        { code: 'MOH-NOTIF-001', name: 'Birth Notification', icon: 'bi-hospital', description: 'Institutional capture of birth at medical facility.' },
        { code: 'CRS-CERT-001', name: 'Birth Certificate', icon: 'bi-patch-check', description: 'Official issuance of Birth Certificate and UPI.' },
        { code: 'SHA-UHC-001', name: 'Health Activation', icon: 'bi-heart-pulse', description: 'Activation of Universal Health Coverage (Linda Mama).' },
        { code: 'MOE-NEMIS-001', name: 'Education Entry', icon: 'bi-book', description: 'National school enrollment via NEMIS system.' },
        { code: 'NRB-ID-001', name: 'National ID (Age 18)', icon: 'bi-person-badge', description: 'Biometric upgrade to adult National Identity.' },
        { code: 'KRA-TAX-001', name: 'Tax Compliance', icon: 'bi-cash-coin', description: 'Automated KRA PIN generation and ledger audit.' },
        { code: 'IMM-PASS-001', name: 'Passport Issuance', icon: 'bi-passport', description: 'International travel credentialing via Maisha Namba.' },
        { code: 'BRS-INC-001', name: 'Entrepreneurship', icon: 'bi-briefcase', description: 'Business incorporation and entity registration.' },
        { code: 'AG-MAR-001', name: 'Marriage Registry', icon: 'bi-unity', description: 'Official registration of spousal union.' },
        { code: 'LND-TRF-001', name: 'Property Ownership', icon: 'bi-house-check', description: 'Institutional land transfer and title tokenization.' },
        { code: 'JUD-SUCC-001', name: 'Estate Succession', icon: 'bi-gavel', description: 'Legal distribution of assets and final records.' },
    ];

    const lifecycleNodes = computed(() => {
        const requests = citizenStore.myRequests;
        let firstIncompleteFound = false;

        return LIFECYCLE_SEQUENCE.map((node) => {
            const request = requests.find(r => r.service_config.service_code === node.code);

            let status = 'locked';
            let requestId = null;

            if (request) {
                if (request.status === 'approved' || request.status === 'completed') {
                    status = 'completed';
                } else if (request.status === 'rejected') {
                    status = 'next'; // Allow retry
                    firstIncompleteFound = true;
                } else {
                    status = 'in_progress';
                    requestId = request.id;
                    firstIncompleteFound = true;
                }
            } else if (!firstIncompleteFound) {
                status = 'next';
                firstIncompleteFound = true;
            }

            return { ...node, status, requestId };
        });
    });

    const progressPercentage = computed(() => {
        const completedCount = lifecycleNodes.value.filter(n => n.status === 'completed').length;
        if (completedCount === 0) return 0;
        return (completedCount / (lifecycleNodes.value.length - 1)) * 100;
    });

    const isNodeActive = (node) => node.status === 'in_progress' || node.status === 'next';

    const getNodeStatusClass = (node) => {
        if (node.status === 'completed') return 'u-bg-success u-text-white u-border-success/20';
        if (node.status === 'in_progress') return 'u-bg-primary u-text-white u-border-primary-soft';
        if (node.status === 'next') return 'u-bg-white u-text-primary u-border-primary/40';
        return 'u-bg-slate-100 u-text-muted u-border-slate-200';
    };
</script>

<style scoped>
    .lifecycle-track-wrapper::-webkit-scrollbar {
        height: 6px;
    }

    .lifecycle-track-wrapper::-webkit-scrollbar-track {
        background: var(--color-background-alt);
    }

    .lifecycle-track-wrapper::-webkit-scrollbar-thumb {
        background: var(--color-border);
        border-radius: 10px;
    }

    .perspective {
        perspective: 1000px;
    }
</style>
