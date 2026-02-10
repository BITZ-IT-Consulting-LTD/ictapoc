import { defineStore } from 'pinia';
import api from '../services/api';

export const useMdaStore = defineStore('mda', {
  state: () => ({
    mdas: [],
  }),
  actions: {
    async fetchMdas() {
      try {
        const response = await api.get('/mdas/');
        this.mdas = response.data;
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
