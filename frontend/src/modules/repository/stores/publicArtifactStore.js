import { defineStore } from 'pinia';
import publicRepositoryApi from '../services/publicRepositoryApi';

export const usePublicArtifactStore = defineStore('publicArtifact', {
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
                const response = await publicRepositoryApi.getArtifacts(params);
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
                    publicRepositoryApi.getArtifact(id),
                    publicRepositoryApi.getDocuments({ artifact_id: id })
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
        async fetchPhases() {
            try {
                const res = await publicRepositoryApi.getProjectPhases();
                this.phases = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load project phases", err);
            }
        },
        async fetchArtifactTypes() {
            try {
                const res = await publicRepositoryApi.getArtifactTypes();
                this.artifactTypes = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load artifact types", err);
            }
        },
        async fetchNodes() {
            try {
                const res = await publicRepositoryApi.getNodes();
                this.nodes = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load nodes", err);
            }
        },
        async fetchRegistries() {
            try {
                const res = await publicRepositoryApi.getRegistries();
                this.registries = res.data.results || res.data;
            } catch (err) {
                console.error("Failed to load registries", err);
            }
        }
    }
});
