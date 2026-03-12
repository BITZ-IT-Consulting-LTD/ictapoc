<template>
    <div v-if="stats" class="stats-grid u-mb-8">
        <div v-for="item in statCards" :key="item.label" class="stats-card" :class="getCardModifier(item.iconClass)">

            <!-- Gradient Background Overlay -->
            <div class="stats-card__overlay"></div>

            <!-- Content -->
            <div class="stats-card__content">
                <!-- Icon Container - Left Side -->
                <div class="stats-card__icon-wrapper">
                    <div class="stats-card__icon-container">
                        <!-- Glow effect -->
                        <div class="stats-card__icon-glow"></div>

                        <!-- Icon -->
                        <div class="stats-card__icon" v-html="item.iconRaw">
                        </div>
                    </div>
                </div>

                <!-- Content - Right Side -->
                <div class="stats-card__text-content">
                    <!-- Label -->
                    <h3 class="stats-card__label">
                        {{ item.label }}
                    </h3>

                    <!-- Value -->
                    <div class="stats-card__value-wrapper">
                        <p class="stats-card__value">
                            {{ item.value }}
                        </p>
                        <span v-if="item.suffix" class="stats-card__unit">
                            {{ item.suffix }}
                        </span>
                    </div>

                    <!-- Sublabel -->
                    <p class="stats-card__sublabel">
                        {{ item.sublabel }}
                    </p>
                </div>

                <!-- Trend Indicator (optional) -->
                <div v-if="item.trend"
                    class="flex-shrink-0 flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-lg"
                    :class="item.trend > 0 ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'">
                    <i :class="item.trend > 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
                    <span>{{ Math.abs(item.trend) }}%</span>
                </div>
            </div>

            <!-- Bottom Accent Line -->
            <div class="stats-card__accent-line"></div>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue';

    const props = defineProps({
        stats: {
            type: Object,
            required: true
        }
    });

    const getCardModifier = (iconClass) => {
        if (iconClass.includes('indigo')) return 'stats-card--info';
        if (iconClass.includes('orange')) return 'stats-card--warning';
        if (iconClass.includes('purple')) return 'stats-card--primary';
        if (iconClass.includes('blue')) return 'stats-card--info';
        if (iconClass.includes('green') || iconClass.includes('emerald')) return 'stats-card--success';
        return 'stats-card--info';
    };

    const statCards = computed(() => [
        {
            label: 'Services',
            value: props.stats.totalServices || 0,
            sublabel: 'Total WOG Catalogue',
            iconClass: 'text-primary',
            iconRaw: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-8 h-8"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>'
        },
        {
            label: 'Agencies',
            value: props.stats.totalMDAs || 0,
            sublabel: 'Active MDAs Mapped',
            iconClass: 'text-warning',
            iconRaw: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-8 h-8"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>'
        },
        {
            label: 'Ministries',
            value: props.stats.totalDomains || 0,
            sublabel: 'Service Domains',
            iconClass: 'text-info',
            iconRaw: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-8 h-8"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path></svg>'
        },
        {
            label: 'Citizen Apps',
            value: props.stats.citizenFacing || 0,
            sublabel: 'Public Facing (C2G',
            iconClass: 'text-success',
            iconRaw: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-8 h-8"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>'
        },
        {
            label: 'Automation',
            value: props.stats.totalServices > 0 ? Math.round((props.stats.withWorkflow / props.stats.totalServices) * 100) : 0,
            suffix: '%',
            sublabel: 'Orchestration Coverage',
            iconClass: 'text-success',
            iconRaw: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-8 h-8"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>'
        },
        {
            label: 'Maturity',
            value: props.stats.avgMaturity || 0,
            suffix: '/ 5',
            sublabel: 'Avg Digitization',
            iconClass: 'text-indigo',
            iconRaw: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-8 h-8"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>'
        }
    ]);
</script>

<style scoped>
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }

    .stats-card {
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        animation: slideUp 0.6s ease-out forwards;
        opacity: 0;
    }

    .stats-card:nth-child(1) {
        animation-delay: 0.1s;
    }

    .stats-card:nth-child(2) {
        animation-delay: 0.15s;
    }

    .stats-card:nth-child(3) {
        animation-delay: 0.2s;
    }

    .stats-card:nth-child(4) {
        animation-delay: 0.25s;
    }

    .stats-card:nth-child(5) {
        animation-delay: 0.3s;
    }

    .stats-card:nth-child(6) {
        animation-delay: 0.35s;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .stats-card__icon-glow {
        filter: blur(12px);
        opacity: 0.3;
    }

    .stats-card:hover .stats-card__icon-glow {
        opacity: 0.6;
        transform: scale(1.2);
    }

    .stats-card__value {
        letter-spacing: -0.05em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
</style>
