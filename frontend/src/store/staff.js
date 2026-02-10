import { defineStore } from 'pinia';
import api from '../services/api';
import { useSystemMonitoringStore } from './systemMonitoring';

export const useStaffStore = defineStore('staff', {
  state: () => ({
    assignedRequests: [], // Specifically assigned to the logged-in user
    unassignedRequests: [], // Total unassigned pool for current role/department
    mdaIncompleteRequests: [], // Full departmental visibility
    teamRequests: [],
    escalatedRequests: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchIncompleteMdaRequests() {
      try {
        const response = await api.get('/service-requests/?all_mda=true');
        this.mdaIncompleteRequests = response.data;
      } catch (error) {
        console.error('Failed to fetch MDA incomplete requests:', error);
      }
    },
    async fetchAssignedRequests() {
      this.loading = true;
      try {
        const response = await api.get('/service-requests/?assigned_to_me=true');
        this.assignedRequests = response.data;
      } catch (error) {
        this.error = 'Failed to fetch assigned requests';
      } finally {
        this.loading = false;
      }
    },
    async fetchUnassignedRequests() {
      this.loading = true;
      try {
        const response = await api.get('/service-requests/?unassigned=true');
        this.unassignedRequests = response.data;
      } catch (error) {
        this.error = 'Failed to fetch unassigned requests';
      } finally {
        this.loading = false;
      }
    },
    async fetchTeamRequests() {
      try {
        const response = await api.get('/service-requests/?team_requests=true');
        this.teamRequests = response.data;
      } catch (error) {
        console.error('Failed to fetch team requests:', error);
      }
    },
    async fetchEscalatedRequests() {
      try {
        const response = await api.get('/service-requests/?is_escalated=true');
        this.escalatedRequests = response.data;
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
