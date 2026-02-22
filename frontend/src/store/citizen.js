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
    },
    async queryRegistryEndpoint(adapterId, endpointId, params) {
      try {
        // Updated endpoint to support direct registry proxying
        // Constructing URL based on available patterns. 
        // The backend views.RegistryQueryView handles ?registry_code=... or path params.
        // But we have adapter ID and endpoint ID.
        // We might need a new general proxy endpoint or use the existing one with richer payload.
        // Let's assume we post to /registry/query/ but pass explicit IDs.
        const response = await api.post('/registry/query/', {
          adapter_id: adapterId,
          endpoint_id: endpointId,
          params: params
        });
        return response.data;
      } catch (error) {
        console.error('Registry Endpoint query failed:', error);
        throw error;
      }
    }
  },
});
