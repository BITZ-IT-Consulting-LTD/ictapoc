<template>
  <div class="bg-white p-6 rounded-lg shadow mt-4">
    <div class="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
      <h3 class="text-xl font-bold text-gray-900 border-l-4 border-slate-800 pl-4">System Activity & Audit Logs</h3>
      <div class="flex gap-2">
         <button @click="fetchLogs" class="px-3 py-1 bg-slate-100 border text-slate-600 rounded-md hover:bg-slate-200 text-sm">
           Refresh Logs
         </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 bg-slate-50 p-4 rounded-xl border border-slate-100">
      <div>
        <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Search Action / Details</label>
        <input type="text" v-model="searchQuery" placeholder="Search..." class="w-full px-3 py-2 border rounded-md text-sm" />
      </div>
      <div>
        <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Filter by User</label>
        <input type="text" v-model="userFilter" placeholder="Username..." class="w-full px-3 py-2 border rounded-md text-sm" />
      </div>
      <div>
        <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Action Type</label>
        <select v-model="actionFilter" class="w-full px-3 py-2 border rounded-md text-sm bg-white">
          <option value="">All Actions</option>
          <option value="REQUEST_ESCALATED">Request Escalated</option>
          <option value="ESCALATION_ACKNOWLEDGED">Escalation Acknowledged</option>
          <option value="WORKFLOW_STEP_COMPLETED">Step Completed</option>
          <option value="USER_REGISTERED">User Registered</option>
        </select>
      </div>
    </div>

    <!-- Audit Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-slate-200">
        <thead class="bg-slate-800 text-white">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider">Timestamp</th>
            <th class="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider">Actor</th>
            <th class="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider">Action</th>
            <th class="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider">Request ID</th>
            <th class="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider">Details</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-slate-100">
          <tr v-for="log in filteredLogs" :key="log.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500 font-mono">
              {{ formatTimestamp(log.timestamp) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 font-bold text-xs uppercase mr-2">
                  {{ log.actor?.username?.substring(0, 2) || 'S' }}
                </div>
                <div>
                  <div class="text-sm font-bold text-slate-900">{{ log.actor?.username || 'System' }}</div>
                  <div class="text-xs text-slate-500 uppercase tracking-tighter">{{ log.actor?.role || 'N/A' }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="actionBadgeClass(log.action)" class="px-2 py-1 text-[10px] font-bold rounded uppercase border">
                {{ log.action }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-indigo-600">
              {{ log.service_request?.request_id || 'N/A' }}
            </td>
            <td class="px-6 py-4 text-sm text-slate-600 max-w-xs truncate" :title="log.details">
              {{ log.details }}
            </td>
          </tr>
          <tr v-if="filteredLogs.length === 0">
             <td colspan="5" class="px-6 py-20 text-center text-slate-400 italic">
               No audit logs found matching the criteria.
             </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4 text-right">
      <p class="text-xs text-slate-400">Total logs tracked: {{ logs.length }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../../services/api';

const logs = ref([]);
const searchQuery = ref('');
const userFilter = ref('');
const actionFilter = ref('');

const fetchLogs = async () => {
  try {
    const response = await api.get('/audit-logs/');
    logs.value = response.data;
  } catch (e) {
    console.error("Failed to fetch audit logs", e);
  }
};

const formatTimestamp = (ts) => {
  if (!ts) return 'N/A';
  const date = new Date(ts);
  return date.toLocaleString();
};

const actionBadgeClass = (action) => {
  if (action?.includes('ESCALATED')) return 'bg-orange-50 text-orange-600 border-orange-100';
  if (action?.includes('COMPLETED')) return 'bg-green-50 text-green-600 border-green-100';
  if (action?.includes('ACKNOWLEDGED')) return 'bg-blue-50 text-blue-600 border-blue-100';
  if (action?.includes('REGISTERED')) return 'bg-cyan-50 text-cyan-600 border-cyan-100';
  return 'bg-slate-50 text-slate-600 border-slate-100';
};

const filteredLogs = computed(() => {
  let result = logs.value;

  if (userFilter.value) {
    const u = userFilter.value.toLowerCase();
    result = result.filter(l => l.actor?.username?.toLowerCase().includes(u));
  }

  if (actionFilter.value) {
    result = result.filter(l => l.action === actionFilter.value);
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(l => 
      l.details?.toLowerCase().includes(q) || 
      l.service_request?.request_id?.toLowerCase().includes(q) ||
      l.action?.toLowerCase().includes(q)
    );
  }

  return result;
});

onMounted(() => {
  fetchLogs();
});
</script>
