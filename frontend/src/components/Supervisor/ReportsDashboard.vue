<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <div>
        <h3 class="text-xl font-extrabold text-slate-900">Operational Analytics</h3>
        <p class="text-sm text-slate-500">Real-time insight into service delivery performance.</p>
      </div>
      <div>
         <button @click="refreshData" class="text-indigo-600 hover:text-indigo-800 text-sm font-bold flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
            Refresh
         </button>
      </div>
    </div>

    <div v-if="summaryData" class="grid grid-cols-1 md:grid-cols-4 gap-6">
      
      <!-- Key Metric 1: Total Volume -->
      <div class="bg-indigo-600 p-6 rounded-2xl text-white shadow-lg shadow-indigo-200">
        <p class="text-xs font-bold text-indigo-200 uppercase tracking-wider mb-1">Total Requests</p>
        <p class="text-4xl font-extrabold mb-1">{{ summaryData.total_requests }}</p>
        <div class="flex items-center gap-2 mt-4 text-xs font-medium bg-indigo-500/30 p-2 rounded-lg inline-flex">
           <span>{{ summaryData.pending_requests }} Pending</span>
           <span class="w-px h-3 bg-indigo-400"></span>
           <span>{{ summaryData.completed_requests }} Closed</span>
        </div>
      </div>

      <!-- Key Metric 2: SLA Compliance -->
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4"></div>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1 relative z-10">SLA Compliance (24h)</p>
        <p class="text-4xl font-extrabold relative z-10" 
           :class="summaryData.performance?.sla_compliance_rate >= 80 ? 'text-emerald-600' : 'text-amber-500'">
            {{ summaryData.performance?.sla_compliance_rate }}%
        </p>
        <p class="text-xs text-slate-400 mt-2 relative z-10 font-medium">Target: > 90%</p>
      </div>

      <!-- Key Metric 3: Avg Processing Time -->
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Avg. Processing Time</p>
        <p class="text-4xl font-extrabold text-slate-900">
            {{ summaryData.performance?.avg_processing_time_hours }} <span class="text-lg text-slate-400 font-normal">hrs</span>
        </p>
        <p class="text-xs text-slate-400 mt-2 font-medium">Time to decision</p>
      </div>

      <!-- Key Metric 4: Approval Rate -->
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Approval Rate</p>
        <p class="text-4xl font-extrabold text-slate-900">
            {{ calculateApprovalRate() }}%
        </p>
         <p class="text-xs text-slate-400 mt-2 font-medium">Of completed requests</p>
      </div>

    </div>

    <div v-if="summaryData" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Breakdown: Status -->
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <h4 class="font-bold text-slate-800 mb-6 flex items-center gap-2">
                <span class="w-2 h-6 bg-indigo-500 rounded-sm"></span>
                Request Status Breakdown
            </h4>
            <div class="space-y-4">
                <div v-for="(count, status) in summaryData.requests_by_status" :key="status" class="flex items-center gap-4">
                    <div class="w-32 text-xs font-bold text-slate-500 uppercase text-right">{{ status.replace('_',' ') }}</div>
                    <div class="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden relative">
                        <div class="h-full rounded-full transition-all duration-1000"
                             :class="getStatusColor(status)"
                             :style="{ width: `${(count / summaryData.total_requests) * 100}%` }"></div>
                    </div>
                    <div class="w-8 text-sm font-bold text-slate-700 text-right">{{ count }}</div>
                </div>
            </div>
        </div>

        <!-- Breakdown: Services -->
         <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <h4 class="font-bold text-slate-800 mb-6 flex items-center gap-2">
                <span class="w-2 h-6 bg-emerald-500 rounded-sm"></span>
                Efficiency by Service
            </h4>
            <div class="space-y-4">
                <div v-for="(count, service) in summaryData.requests_per_service" :key="service" class="pb-3 border-b border-slate-50 last:border-0">
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-sm font-bold text-slate-700">{{ service }}</span>
                        <span class="text-xs font-mono bg-slate-100 px-2 py-1 rounded text-slate-600">{{ count }} reqs</span>
                    </div>
                    <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                         <div class="h-full bg-slate-800 rounded-full" 
                              :style="{ width: `${(count / summaryData.total_requests) * 100}%` }"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div v-else class="py-20 text-center text-slate-400">
      <div class="animate-pulse flex flex-col items-center">
          <div class="w-12 h-12 bg-slate-200 rounded-full mb-4"></div>
          <p>Compiling Government Data Analytics...</p>
      </div>
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
        'approved': 'bg-emerald-500',
        'rejected': 'bg-rose-500',
        'in_progress': 'bg-amber-400',
        'received': 'bg-blue-400',
        'closed': 'bg-slate-500',
        'escalated': 'bg-orange-500',
        'validation_failed': 'bg-red-600'
    };
    return map[status] || 'bg-slate-300';
};
</script>
