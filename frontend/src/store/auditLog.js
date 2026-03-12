import { defineStore } from 'pinia';
import api from '../services/api';

export const useAuditLogStore = defineStore('auditLog', {
  state: () => ({
    auditLogs: [],
    auditMeta: { count: 0, next: null, previous: null },
    requestLogs: [],
  }),
  actions: {
    async fetchAuditLogs(params = {}) {
      try {
        const response = await api.get('/audit-logs/', { params });
        this.auditLogs = response.data.results || response.data;
        this.auditMeta = response.data.results ? { count: response.data.count, next: response.data.next, previous: response.data.previous } : { count: this.auditLogs.length };
      } catch (error) {
        console.error('Failed to fetch audit logs:', error);
      }
    },
    async fetchLogsForRequest(requestId) {
      try {
        const response = await api.get('/audit-logs/', { params: { service_request: requestId } });
        this.requestLogs = response.data.results || response.data;
      } catch (error) {
        console.error(`Failed to fetch audit logs for request ${requestId}:`, error);
        this.requestLogs = [];
      }
    },
  },
});
