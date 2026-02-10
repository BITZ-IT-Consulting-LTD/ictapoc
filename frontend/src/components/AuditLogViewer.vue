<template>
  <div class="bg-white p-6 rounded-lg shadow mt-8">
    <h3 class="text-xl font-semibold mb-4">Audit Log</h3>
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Request ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actor</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="log in sortedAuditLogs" :key="log.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(log.timestamp) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ log.service_request.request_id.substring(0, 8) }}...</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ log.actor?.username || 'System' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ log.action }}</td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ log.details }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuditLogStore } from '@store/auditLog';

const auditLogStore = useAuditLogStore();

onMounted(() => {
  auditLogStore.fetchAuditLogs();
});

const sortedAuditLogs = computed(() => {
  return [...auditLogStore.auditLogs].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
});

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};
</script>
