<template>
    <div class="dashboard-analytics u-flex u-flex-col u-gap-8 animate-fade-in">
        <!-- Operational Header -->
        <header class="card card--dark u-mb-4 shadow-xl">
            <div class="card__body u-flex u-justify-between u-items-center u-p-8 u-bg-gradient-dark">
                <div class="page__title-group">
                    <h2 class="u-text-2xl u-font-black u-text-white u-mb-1">Operational Command Suite</h2>
                    <p class="u-text-xs u-font-black u-uppercase u-tracking-[0.2em] u-text-primary u-opacity-70">
                        Real-time Service Delivery Intelligence
                    </p>
                </div>
                <button @click="refreshData" class="button button--primary button--pill button--small shadow-lg">
                    <i class="bi bi-arrow-clockwise"></i> Sync Analytics
                </button>
            </div>
        </header>

        <!-- Metric Grid -->
        <div v-if="summaryData" class="stats-grid">
            <!-- Key Metric 1: Total Volume -->
            <article class="stats-card stats-card--primary">
                <div class="stats-card__overlay"></div>
                <div class="stats-card__content">
                    <div class="stats-card__icon-wrapper">
                        <div class="stats-card__icon-container">
                            <div class="stats-card__icon-glow"></div>
                            <div class="stats-card__icon">
                                <i class="bi bi-activity"></i>
                            </div>
                        </div>
                    </div>
                    <div class="stats-card__text-content">
                        <p class="stats-card__label">National Volume</p>
                        <div class="stats-card__value-wrapper">
                            <span class="stats-card__value">{{ summaryData.total_requests }}</span>
                        </div>
                        <p class="stats-card__sublabel">Lifecycle Requests</p>
                    </div>
                </div>
                <div class="u-px-6 u-pb-6 u-relative u-z-base">
                    <div class="u-flex u-gap-2">
                        <span class="badge badge--small u-bg-white/10 u-text-white u-border-0">{{ summaryData.pending_requests }} PENDING</span>
                        <span class="badge badge--small u-bg-white/10 u-text-white u-border-0">{{ summaryData.completed_requests }} CLOSED</span>
                    </div>
                </div>
                <div class="stats-card__accent-line"></div>
            </article>

            <!-- Key Metric 2: SLA Compliance -->
            <article class="stats-card stats-card--success">
                <div class="stats-card__overlay"></div>
                <div class="stats-card__content">
                    <div class="stats-card__icon-wrapper">
                        <div class="stats-card__icon-container">
                            <div class="stats-card__icon-glow"></div>
                            <div class="stats-card__icon">
                                <i class="bi bi-shield-check"></i>
                            </div>
                        </div>
                    </div>
                    <div class="stats-card__text-content">
                        <p class="stats-card__label">Governance Level</p>
                        <div class="stats-card__value-wrapper">
                            <span class="stats-card__value" :class="summaryData.performance?.sla_compliance_rate >= 80 ? '' : 'u-text-warning'">
                                {{ summaryData.performance?.sla_compliance_rate }}
                            </span>
                            <span class="stats-card__unit">%</span>
                        </div>
                        <p class="stats-card__sublabel">SLA Compliance Rate</p>
                    </div>
                </div>
                <div class="u-px-6 u-pb-6 u-relative u-z-base">
                    <div class="progress-bar progress-bar--sm u-bg-white/10">
                        <div class="progress-bar__fill u-bg-white" :style="{ width: `${summaryData.performance?.sla_compliance_rate}%` }"></div>
                    </div>
                </div>
                <div class="stats-card__accent-line"></div>
            </article>

            <!-- Key Metric 3: Processing Velocity -->
            <article class="stats-card stats-card--info">
                <div class="stats-card__overlay"></div>
                <div class="stats-card__content">
                    <div class="stats-card__icon-wrapper">
                        <div class="stats-card__icon-container">
                            <div class="stats-card__icon-glow"></div>
                            <div class="stats-card__icon">
                                <i class="bi bi-lightning-charge"></i>
                            </div>
                        </div>
                    </div>
                    <div class="stats-card__text-content">
                        <p class="stats-card__label">Registry Velocity</p>
                        <div class="stats-card__value-wrapper">
                            <span class="stats-card__value">{{ summaryData.performance?.avg_processing_time_hours }}</span>
                            <span class="stats-card__unit">HRS</span>
                        </div>
                        <p class="stats-card__sublabel">Avg. Processing Latency</p>
                    </div>
                </div>
                <div class="u-px-6 u-pb-6 u-relative u-z-base">
                    <p class="u-text-[10px] u-font-black u-text-muted u-uppercase tracking-widest group-hover:u-text-white transition-colors">Target: &lt; 24h</p>
                </div>
                <div class="stats-card__accent-line"></div>
            </article>

            <!-- Key Metric 4: Success Ratio -->
            <article class="stats-card stats-card--warning">
                <div class="stats-card__overlay"></div>
                <div class="stats-card__content">
                    <div class="stats-card__icon-wrapper">
                        <div class="stats-card__icon-container">
                            <div class="stats-card__icon-glow"></div>
                            <div class="stats-card__icon">
                                <i class="bi bi-gem"></i>
                            </div>
                        </div>
                    </div>
                    <div class="stats-card__text-content">
                        <p class="stats-card__label">Trust Ratio</p>
                        <div class="stats-card__value-wrapper">
                            <span class="stats-card__value">{{ calculateApprovalRate() }}</span>
                            <span class="stats-card__unit">%</span>
                        </div>
                        <p class="stats-card__sublabel">Approval Rate</p>
                    </div>
                </div>
                <div class="u-px-6 u-pb-6 u-relative u-z-base">
                    <p class="u-text-[10px] u-font-black u-text-muted u-uppercase tracking-widest group-hover:u-text-white transition-colors">On Completed Set</p>
                </div>
                <div class="stats-card__accent-line"></div>
            </article>
        </div>

        <!-- Detailed Analytics Section -->
        <div v-if="summaryData" class="u-grid u-grid-cols-1 lg:u-grid-cols-2 u-gap-8">
            <!-- Detailed Status Matrix -->
            <article class="card shadow-xl overflow-hidden">
                <header class="card__header card--dark u-py-4">
                    <h4 class="card__title u-text-lg font-black">Request Lifecycle Matrix</h4>
                </header>
                <div class="card__body u-p-10">
                    <div class="u-flex u-flex-col u-gap-8">
                        <div v-for="(count, status) in summaryData.requests_by_status" :key="status" class="group">
                            <div class="u-flex u-justify-between u-items-center u-mb-3">
                                <span class="u-text-[11px] u-font-black u-text-muted u-uppercase u-tracking-[0.15em] group-hover:u-text-primary transition-colors">
                                    {{ status.replace('_', ' ') }}
                                </span>
                                <span class="badge badge--secondary u-font-black">{{ count }}</span>
                            </div>
                            <div class="progress-bar progress-bar--lg shadow-inner">
                                <div class="progress-bar__fill shadow-sm"
                                    :class="getStatusColor(status)"
                                    :style="{ width: `${(count / summaryData.total_requests) * 100}%` }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </article>

            <!-- Service Efficiency Index -->
            <article class="card shadow-xl overflow-hidden">
                <header class="card__header u-bg-indigo-900 u-text-white u-py-4" style="background-color: #312e81">
                    <h4 class="card__title u-text-white u-text-lg font-black">Service Efficiency Index</h4>
                </header>
                <div class="card__body u-p-10">
                    <div class="u-flex u-flex-col u-gap-6">
                        <div v-for="(count, service) in summaryData.requests_per_service" :key="service"
                            class="u-pb-5 u-border-b u-border-border-color last:u-border-0 last:u-pb-0 group">
                            <div class="u-flex u-justify-between u-items-center u-mb-3">
                                <span class="u-text-sm u-font-black u-text-main group-hover:u-text-primary transition-colors">{{ service }}</span>
                                <span class="badge badge--info badge--small">{{ count }} APPLICATIONS</span>
                            </div>
                            <div class="progress-bar progress-bar--sm">
                                <div class="progress-bar__fill u-bg-main group-hover:u-bg-primary transition-colors"
                                    :style="{ width: `${(count / summaryData.total_requests) * 100}%` }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </article>
        </div>

        <!-- Loading State -->
        <div v-else class="card u-py-32 u-flex u-flex-col u-items-center u-justify-center shadow-lg">
            <div class="u-w-12 u-h-12 u-border-4 u-border-primary-soft u-border-t-primary u-rounded-full animate-spin u-mb-6"></div>
            <p class="u-text-[10px] u-font-black u-uppercase u-tracking-[0.3em] u-text-primary animate-pulse">Compiling National Command Data...</p>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import api from '../../services/api';

    const summaryData = ref(null);

    const fetchData = async () => {
        summaryData.value = null; // Trigger loading state
        try {
            // Quick artificial delay to show off the loading skeleton if we had one, or just feel 'computational'
            // await new Promise(r => setTimeout(r, 600)); 
            const response = await api.get('/reports/summary/');
            summaryData.value = response.data;
        } catch (error) {
            console.error('Failed to fetch report summary:', error);
        }
    };

    const refreshData = () => {
        fetchData();
    };

    onMounted(() => {
        fetchData();
    });

    const calculateApprovalRate = () => {
        if (!summaryData.value || !summaryData.value.completed_requests) return 0;
        const approved = summaryData.value.requests_by_status['approved'] || 0;
        return Math.round((approved / summaryData.value.completed_requests) * 100);
    };

    const getStatusColor = (status) => {
        const map = {
            'approved': 'u-bg-success',
            'rejected': 'u-bg-danger',
            'in_progress': 'u-bg-warning',
            'received': 'u-bg-info',
            'closed': 'u-bg-muted',
            'escalated': 'u-bg-warning',
            'validation_failed': 'u-bg-danger'
        };
        return map[status] || 'u-bg-muted';
    };
</script>
