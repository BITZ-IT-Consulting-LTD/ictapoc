import { defineStore } from 'pinia';
import api from '@/services/api';

export const useRegistryStore = defineStore('registry', {
    state: () => ({
        adapters: [],
        endpoints: [],
        loading: false,
        error: null,
    }),

    actions: {
        async fetchAdapters() {
            this.loading = true;
            try {
                const response = await api.get('/registries/');
                this.adapters = response.data;
                this.error = null;
            } catch (err) {
                this.error = 'Failed to fetch registry adapters.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        async fetchEndpoints(adapterId = null) {
            this.loading = true;
            try {
                let url = '/registry-endpoints/';
                if (adapterId) {
                    url += `?adapter_id=${adapterId}`;
                }
                const response = await api.get(url);
                this.endpoints = response.data;
                this.error = null;
            } catch (err) {
                this.error = 'Failed to fetch registry endpoints.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        }
    },

    getters: {
        getAdapterById: (state) => (id) => {
            return state.adapters.find(a => a.id === id);
        },
        getEndpointsByAdapter: (state) => (adapterId) => {
            return state.endpoints.filter(ep => ep.adapter === adapterId);
        }
    }
});
