import { defineStore } from 'pinia';
import api from '../services/api';

export const useMdaStore = defineStore('mda', {
  state: () => ({
    mdas: [],
    mdaPagination: {
      count: 0,
      next: null,
      previous: null
    }
  }),
  actions: {
    async fetchMdas(params = { page: 1, search: '' }) {
      try {
        const response = await api.get('/mdas/', { params });
        if (response.data.results) {
          this.mdas = response.data.results;
          this.mdaPagination = {
            count: response.data.count,
            next: response.data.next,
            previous: response.data.previous
          };
        } else {
          this.mdas = response.data;
        }
      } catch (error) {
        console.error('Failed to fetch MDAs:', error);
      }
    },
    async createMda(mdaData) {
      try {
        const response = await api.post('/mdas/', mdaData);
        this.mdas.push(response.data);
      } catch (error) {
        console.error('Failed to create MDA:', error);
      }
    },
    async updateMda(mdaData) {
      try {
        const response = await api.put(`/mdas/${mdaData.id}/`, mdaData);
        const index = this.mdas.findIndex(m => m.id === mdaData.id);
        if (index !== -1) {
          this.mdas[index] = response.data;
        }
      } catch (error) {
        console.error('Failed to update MDA:', error);
      }
    },
    async deleteMda(mdaId) {
      try {
        await api.delete(`/mdas/${mdaId}/`);
        this.mdas = this.mdas.filter(m => m.id !== mdaId);
      } catch (error) {
        console.error('Failed to delete MDA:', error);
      }
    },
  },
});
