<template>
    <div v-if="stats" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
        <div v-for="item in statCards" :key="item.label"
            class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm transition-all hover:shadow-md group">
            <div class="flex items-center gap-3">
                <div :class="`p-2 rounded-lg ${item.bgClass} ${item.iconClass}`">
                    <component :is="item.icon" class="w-5 h-5" />
                </div>
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest leading-none">{{ item.label
                    }}</span>
            </div>
            <div class="mt-2 flex items-baseline gap-1">
                <p class="text-2xl font-black text-gray-900">{{ item.value }}</p>
                <span v-if="item.suffix" class="text-xs text-gray-400 font-bold">{{ item.suffix }}</span>
            </div>
            <div class="mt-1 text-[10px] text-gray-400 group-hover:text-indigo-500 transition-colors">
                {{ item.sublabel }}
            </div>
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

    const statCards = computed(() => [
        {
            label: 'Services',
            value: props.stats.totalServices || 0,
            sublabel: 'Total WOG Catalogue',
            icon: 'LibraryIcon',
            bgClass: 'bg-indigo-50',
            iconClass: 'text-indigo-600',
            icon: {
                template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>'
            }
        },
        {
            label: 'Agencies',
            value: props.stats.totalMDAs || 0,
            sublabel: 'Active MDAs Mapped',
            bgClass: 'bg-orange-50',
            iconClass: 'text-orange-600',
            icon: {
                template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>'
            }
        },
        {
            label: 'Ministries',
            value: props.stats.totalDomains || 0,
            sublabel: 'Service Domains',
            bgClass: 'bg-purple-50',
            iconClass: 'text-purple-600',
            icon: {
                template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path></svg>'
            }
        },
        {
            label: 'Citizen Apps',
            value: props.stats.citizenFacing || 0,
            sublabel: 'Public Facing (C2G)',
            bgClass: 'bg-blue-50',
            iconClass: 'text-blue-600',
            icon: {
                template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>'
            }
        },
        {
            label: 'Automation',
            value: props.stats.totalServices > 0 ? Math.round((props.stats.withWorkflow / props.stats.totalServices) * 100) : 0,
            suffix: '%',
            sublabel: 'Orchestration Coverage',
            bgClass: 'bg-green-50',
            iconClass: 'text-green-600',
            icon: {
                template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>'
            }
        },
        {
            label: 'Maturity',
            value: props.stats.avgMaturity || 0,
            suffix: '/ 5',
            sublabel: 'Avg Digitization',
            bgClass: 'bg-emerald-50',
            iconClass: 'text-emerald-600',
            icon: {
                template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>'
            }
        }
    ]);
</script>
