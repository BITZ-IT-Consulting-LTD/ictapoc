import { defineStore } from 'pinia';
import api from '../services/api';

export const useServiceConfigStore = defineStore('serviceConfig', {
  state: () => ({
    services: [],
    families: [],
    catalogueSummary: null,
    loadingSummary: false,
  }),
  actions: {
    async fetchCatalogueSummary() {
      this.loadingSummary = true;
      try {
        const response = await api.get('/catalog/services/process_matrix/');

        let totalServices = 0;
        let withWf = 0;
        let mdaSet = new Set();
        let domainCount = response.data.length;
        let totalMaturity = 0;
        let citizenFacing = 0;

        response.data.forEach(domain => {
          domain.processes.forEach(proc => {
            proc.services.forEach(svc => {
              totalServices++;
              mdaSet.add(svc.mda);
              if (svc.workflow_configured) withWf++;
              totalMaturity += (svc.maturity || 1);
              if (svc.service_type?.includes('C2G')) citizenFacing++;
            });
          });
        });

        this.catalogueSummary = {
          totalServices,
          totalMDAs: mdaSet.size,
          totalDomains: domainCount,
          withWorkflow: withWf,
          missingWorkflow: totalServices - withWf,
          avgMaturity: totalServices > 0 ? (totalMaturity / totalServices).toFixed(1) : 0,
          citizenFacing
        };
      } catch (error) {
        console.error('Failed to fetch Catalogue Summary:', error);
      } finally {
        this.loadingSummary = false;
      }
    },
    async fetchServices() {
      try {
        const response = await api.get('/service-configs/');
        this.services = response.data;
      } catch (error) {
        console.error('Failed to fetch Service Configurations:', error);
      }
    },
    async fetchFamilies() {
      try {
        const response = await api.get('/service-families/');
        this.families = response.data;
      } catch (error) {
        console.error('Failed to fetch Service Families:', error);
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
