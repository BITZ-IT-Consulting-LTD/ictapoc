import { defineStore } from 'pinia';
import repositoryApi from '../services/repositoryApi';

export const useArtifactStore = defineStore('artifact', {
    state: () => ({
        artifacts: [],
        selectedArtifact: null,
        documents: [],
        phases: [],
        artifactTypes: [],
        nodes: [],
        registries: [],
        loading: false,
        error: null,
        meta: {
            count: 0,
        }
    }),
    actions: {
        async fetchArtifacts(params = {}) {
            this.loading = true;
            try {
                const response = await repositoryApi.getArtifacts(params);
                this.artifacts = response.data.results || response.data;
                this.meta.count = response.data.count || 0;
            } catch (err) {
                this.error = err.response?.data?.message || 'Failed to fetch artifacts';
            } finally {
                this.loading = false;
            }
        },
        async fetchArtifactDetails(id) {
            this.loading = true;
            try {
                const [artifactRes, docsRes] = await Promise.all([
                    repositoryApi.getArtifact(id),
                    repositoryApi.getDocuments({ artifact_id: id })
                ]);
                this.selectedArtifact = artifactRes.data;
                this.documents = docsRes.data.results || docsRes.data;
            } catch (err) {
                this.error = 'Failed to fetch artifact details';
                throw err;
            } finally {
                this.loading = false;
            }
        },
        async uploadDocument(formData) {
            try {
                const res = await repositoryApi.uploadDocument(formData);
                // add the new document to state
                if (this.documents && Array.isArray(this.documents)) {
                    this.documents.unshift(res.data);
                }
                return res.data;
            } catch (err) {
                throw err;
            }
        },
        async registerArtifact(payload) {
            this.loading = true;
            try {
                const res = await repositoryApi.createArtifact(payload);
                this.artifacts.unshift(res.data);
                return res.data;
            } catch (err) {
                this.error = 'Failed to create artifact';
                throw err;
            } finally {
                this.loading = false;
            }
        },
        async deleteArtifact(id) {
            try {
                await repositoryApi.deleteArtifact(id);
                this.artifacts = this.artifacts.filter(a => a.id !== id);
            } catch (err) {
                console.error("Failed to delete artifact", err);
                throw err;
            }
        },
        async updateArtifact(id, payload) {
            try {
                const res = await repositoryApi.updateArtifact(id, payload);
                const index = this.artifacts.findIndex(a => a.id === id);
                if (index !== -1) {
                    this.artifacts[index] = res.data;
                }
                return res.data;
            } catch (err) {
                console.error("Failed to update artifact", err);
                throw err;
            }
        },
        async fetchPhases() {
            try {
                const res = await repositoryApi.getProjectPhases();
                this.phases = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load project phases", err);
            }
        },
        async fetchArtifactTypes() {
            try {
                const res = await repositoryApi.getArtifactTypes();
                this.artifactTypes = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load artifact types", err);
            }
        },
        async fetchNodes() {
            try {
                const res = await repositoryApi.getNodes();
                this.nodes = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load nodes", err);
            }
        },
        async fetchRegistries() {
            try {
                const res = await repositoryApi.getRegistries();
                this.registries = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load registries", err);
            }
        }
    }
});
