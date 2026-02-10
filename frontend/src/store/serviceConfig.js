import { defineStore } from 'pinia';
import api from '../services/api';

export const useServiceConfigStore = defineStore('serviceConfig', {
  state: () => ({
    services: [],
  }),
  actions: {
    async fetchServices() {
      try {
        const response = await api.get('/service-configs/');
        this.services = response.data;
      } catch (error) {
        console.error('Failed to fetch Service Configurations:', error);
      }
    },
    async createService(serviceData) {
      try {
        const response = await api.post('/service-configs/', serviceData);
        this.services.push(response.data);
      } catch (error) {
        console.error('Failed to create Service Configuration:', error);
      }
    },
    async updateService(serviceData) {
      try {
        const response = await api.put(`/service-configs/${serviceData.id}/`, serviceData);
        const index = this.services.findIndex(s => s.id === serviceData.id);
        if (index !== -1) {
          this.services[index] = response.data;
        }
      } catch (error) {
        console.error('Failed to update Service Configuration:', error);
      }
    },
    async deleteService(serviceId) {
      try {
        await api.delete(`/service-configs/${serviceId}/`);
        this.services = this.services.filter(s => s.id !== serviceId);
      } catch (error) {
        console.error('Failed to delete Service Configuration:', error);
      }
    },
  },
});
