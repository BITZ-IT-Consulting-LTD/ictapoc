import { defineStore } from 'pinia';
import api from '../services/api';

export const useWorkflowStepStore = defineStore('workflowStep', {
  state: () => ({
    steps: [],
  }),
  actions: {
    async fetchSteps(serviceConfigId) {
      try {
        const response = await api.get(`/workflow-steps/?service_config=${serviceConfigId}`);
        this.steps = response.data;
      } catch (error) {
        console.error('Failed to fetch Workflow Steps:', error);
        this.steps = []; // Reset on error
      }
    },
    async createStep(stepData) {
      try {
        const response = await api.post('/workflow-steps/', stepData);
        this.steps.push(response.data);
        return true;
      } catch (error) {
        console.error('Failed to create Workflow Step:', error);
        throw error;
      }
    },
    async updateStep(stepData) {
      try {
        const response = await api.put(`/workflow-steps/${stepData.id}/`, stepData);
        const index = this.steps.findIndex(s => s.id === stepData.id);
        if (index !== -1) {
          this.steps[index] = response.data;
        }
        return true;
      } catch (error) {
        console.error('Failed to update Workflow Step:', error);
        throw error;
      }
    },
    async deleteStep(stepId) {
      try {
        await api.delete(`/workflow-steps/${stepId}/`);
        this.steps = this.steps.filter(s => s.id !== stepId);
      } catch (error) {
        console.error('Failed to delete Workflow Step:', error);
      }
    },
  },
});
