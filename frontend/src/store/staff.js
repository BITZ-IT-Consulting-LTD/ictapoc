import { defineStore } from 'pinia';
import api from '../services/api';
import { useSystemMonitoringStore } from './systemMonitoring';

export const useStaffStore = defineStore('staff', {
  state: () => ({
    assignedRequests: [],
    assignedMeta: { count: 0, next: null, previous: null },
    unassignedRequests: [],
    unassignedMeta: { count: 0, next: null, previous: null },
    mdaIncompleteRequests: [],
    mdaMeta: { count: 0, next: null, previous: null },
    teamRequests: [],
    teamMeta: { count: 0, next: null, previous: null },
    escalatedRequests: [],
    escalatedMeta: { count: 0, next: null, previous: null },
    loading: false,
    error: null,
  }),
  actions: {
    async fetchIncompleteMdaRequests(params = {}) {
      try {
        const response = await api.get('/service-requests/', { params: { ...params } });
        this.mdaIncompleteRequests = response.data.results || response.data;
        this.mdaMeta = response.data.results ? { count: response.data.count, next: response.data.next, previous: response.data.previous } : { count: this.mdaIncompleteRequests.length };
      } catch (error) {
        console.error('Failed to fetch MDA incomplete requests:', error);
      }
    },
    async fetchAssignedRequests(params = {}) {
      this.loading = true;
      try {
        const response = await api.get('/service-requests/', { params: { ...params, assigned_to_me: true } });
        this.assignedRequests = response.data.results || response.data;
        this.assignedMeta = response.data.results ? { count: response.data.count, next: response.data.next, previous: response.data.previous } : { count: this.assignedRequests.length };
      } catch (error) {
        this.error = 'Failed to fetch assigned requests';
      } finally {
        this.loading = false;
      }
    },
    async fetchUnassignedRequests(params = {}) {
      this.loading = true;
      try {
        const response = await api.get('/service-requests/', { params: { ...params, unassigned: true } });
        this.unassignedRequests = response.data.results || response.data;
        this.unassignedMeta = response.data.results ? { count: response.data.count, next: response.data.next, previous: response.data.previous } : { count: this.unassignedRequests.length };
      } catch (error) {
        this.error = 'Failed to fetch unassigned requests';
      } finally {
        this.loading = false;
      }
    },
    async fetchTeamRequests(params = {}) {
      try {
        const response = await api.get('/service-requests/', { params: { ...params } });
        this.teamRequests = response.data.results || response.data;
        this.teamMeta = response.data.results ? { count: response.data.count, next: response.data.next, previous: response.data.previous } : { count: this.teamRequests.length };
      } catch (error) {
        console.error('Failed to fetch team requests:', error);
      }
    },
    async fetchEscalatedRequests(params = {}) {
      try {
        const response = await api.get('/service-requests/', { params: { ...params, is_escalated: true } });
        this.escalatedRequests = response.data.results || response.data;
        this.escalatedMeta = response.data.results ? { count: response.data.count, next: response.data.next, previous: response.data.previous } : { count: this.escalatedRequests.length };
      } catch (error) {
        console.error('Failed to fetch escalated requests:', error);
      }
    },
    async completeWorkflowStep(requestId, action, details) {
      const monitoring = useSystemMonitoringStore();
      try {
        monitoring.broadcastTrace({ type: 'WORKFLOW_STEP_COMPLETION', requestId, action });
        const response = await api.post(`/service-requests/${requestId}/complete_step/`, {
          action,
          details,
        });
        // Update the request in the store
        const index = this.assignedRequests.findIndex(req => req.id === requestId);
        if (index !== -1) {
          this.assignedRequests[index] = response.data;
        }
        return response.data;
      } catch (error) {
        console.error('Failed to complete workflow step:', error);
        throw error;
      }
    },
    async escalateRequest(requestId) {
      try {
        const response = await api.post(`/service-requests/${requestId}/escalate/`);
        const index = this.assignedRequests.findIndex(req => req.id === requestId);
        if (index !== -1) {
          this.assignedRequests[index] = response.data;
        }
        return response.data;
      } catch (error) {
        console.error('Failed to escalate request:', error);
        throw error;
      }
    },
    async acknowledgeEscalation(requestId) {
      try {
        await api.post(`/service-requests/${requestId}/acknowledge_escalation/`);
        this.escalatedRequests = this.escalatedRequests.filter(req => req.id !== requestId);
      } catch (error) {
        console.error('Failed to acknowledge escalation:', error);
        throw error;
      }
    },
    async claimTask(requestId) {
      try {
        await api.post(`/service-requests/${requestId}/claim/`);
        // Refresh both pools
        await this.fetchAssignedRequests();
        await this.fetchUnassignedRequests();
      } catch (error) {
        console.error('Failed to claim task:', error);
        throw error;
      }
    },
    async releaseTask(requestId) {
      try {
        await api.post(`/service-requests/${requestId}/release/`);
        // Refresh both pools
        await this.fetchAssignedRequests();
        await this.fetchUnassignedRequests();
      } catch (error) {
        console.error('Failed to release task:', error);
        throw error;
      }
    },
  },
});
