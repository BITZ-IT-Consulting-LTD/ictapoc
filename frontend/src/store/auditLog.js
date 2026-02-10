import { defineStore } from 'pinia';
import api from '../services/api';

export const useAuditLogStore = defineStore('auditLog', {
  state: () => ({
    auditLogs: [],
    requestLogs: [],
  }),
  actions: {
    async fetchAuditLogs() {
      try {
        const response = await api.get('/audit-logs/');
        this.auditLogs = response.data;
      } catch (error) {
        console.error('Failed to fetch audit logs:', error);
      }
    },
    async fetchLogsForRequest(requestId) {
      try {
        const response = await api.get(`/audit-logs/?service_request=${requestId}`);
        this.requestLogs = response.data;
      } catch (error) {
        console.error(`Failed to fetch audit logs for request ${requestId}:`, error);
        this.requestLogs = [];
      }
    },
  },
});
