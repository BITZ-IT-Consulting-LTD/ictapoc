import api from '../../../services/api';

export default {
    // Artifacts
    getArtifacts(params) {
        return api.get('/v1/artifacts/', { params });
    },
    getArtifact(id) {
        return api.get(`/v1/artifacts/${id}/`);
    },
    updateArtifactStatus(id, status) {
        return api.patch(`/v1/artifacts/${id}/status/`, { status });
    },
    createArtifact(payload) {
        return api.post('/v1/artifacts/', payload);
    },

    // Documents
    getDocuments(params) {
        return api.get('/v1/documents/', { params });
    },
    uploadDocument(formData) {
        return api.post('/v1/documents/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },
    downloadDocument(uuid) {
        return api.get(`/v1/documents/${uuid}/download/`, { responseType: 'blob' });
    },
    previewDocument(uuid) {
        return api.get(`/v1/documents/${uuid}/preview/`, { responseType: 'blob' });
    },

    // Projects & Phases
    getProjectPhases() {
        return api.get('/v1/projects/phases/');
    },
    getArtifactTypes() {
        return api.get('/v1/types/');
    },
    explorePath(path) {
        // Remove leading slash if present as the endpoint handles it
        const cleanPath = path.startsWith('/') ? path.substring(1) : path;
        return api.get(`/v1/repos/explore/${cleanPath}/`);
    },
    explorePathWithParams(path, params) {
        const cleanPath = path.startsWith('/') ? path.substring(1) : path;
        return api.get(`/v1/repos/explore/${cleanPath}/`, { params });
    },
    getNodes() {
        return api.get('/v1/nodes/');
    },
    getRegistries() {
        return api.get('/v1/registries/');
    }
};
