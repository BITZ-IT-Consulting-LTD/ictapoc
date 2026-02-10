import { defineStore } from 'pinia';
import api from '../services/api';
import { useSystemMonitoringStore } from './systemMonitoring';

export const useCitizenStore = defineStore('citizen', {
  state: () => ({
    availableServices: [],
    myRequests: [],
  }),
  actions: {
    async fetchAvailableServices() {
      try {
        // Anyone can see available services
        const response = await api.get('/service-configs/');
        this.availableServices = response.data;
      } catch (error) {
        console.error('Failed to fetch available services:', error);
      }
    },
    async fetchMyRequests() {
      try {
        // This endpoint is protected and will return only the user's requests
        const response = await api.get('/service-requests/');
        this.myRequests = response.data;
      } catch (error) {
        console.error('Failed to fetch my requests:', error);
      }
    },
    async submitRequest(serviceCode, payload) {
      const monitoring = useSystemMonitoringStore();
      try {
        monitoring.broadcastTrace({ type: 'SERVICE_SUBMISSION', service: serviceCode });
        const response = await api.post('/service-requests/', {
          service_code: serviceCode,
          payload: payload,
        });
        this.myRequests.push(response.data);
        return response.data;
      } catch (error) {
        console.error('Failed to submit service request:', error);
        throw error;
      }
    },
    async queryRegistry(registry, params) {
      try {
        const response = await api.post('/registry/query/', {
          registry: registry,
          params: params
        });
        return response.data;
      } catch (error) {
        console.error('Registry query failed:', error);
        throw error;
      }
    }
  },
});
