import { defineStore } from 'pinia';
import api from '../services/api';

export const useServiceConfigStore = defineStore('serviceConfig', {
  state: () => ({
    services: [],
    families: [],
    groups: [],
    catalogueSummary: null,
    matrixData: [],
    loadingSummary: false,
    servicesPagination: {
      count: 0,
      next: null,
      previous: null
    }
  }),
  actions: {
    async fetchGroups() {
      try {
        const response = await api.get('/service-groups/');
        this.groups = response.data;
      } catch (error) {
        console.error('Failed to fetch Service Groups:', error);
      }
    },
    async fetchCatalogueSummary(force = false) {
      if (this.matrixData.length > 0 && !force) return;

      this.loadingSummary = true;
      try {
        const response = await api.get('/catalog/services/process_matrix/');
        this.matrixData = response.data;

        let totalServices = 0;
        let withWf = 0;
        let mdaSet = new Set();
        let domainCount = this.matrixData.length;
        let totalMaturity = 0;
        let citizenFacing = 0;

        this.matrixData.forEach(domain => {
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
    async fetchServices(params = { page: 1, search: '' }) {
      try {
        const response = await api.get('/service-configs/', { params });
        if (response.data.results) {
          this.services = response.data.results;
          this.servicesPagination = {
            count: response.data.count,
            next: response.data.next,
            previous: response.data.previous
          };
        } else {
          this.services = response.data;
        }
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
