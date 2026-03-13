import api from '../../../services/api';

export default {
    getArtifacts(params) {
        return api.get('/v1/public/artifacts/', { params });
    },
    getArtifact(id) {
        return api.get(`/v1/public/artifacts/${id}/`);
    },
    getDocuments(params) {
        return api.get('/v1/public/documents/', { params });
    },
    downloadDocument(uuid) {
        return api.get(`/v1/public/documents/${uuid}/download/`, { responseType: 'blob' });
    },
    previewDocument(uuid) {
        return api.get(`/v1/public/documents/${uuid}/preview/`, { responseType: 'blob' });
    },
    getProjectPhases() {
        return api.get('/v1/public/phases/');
    },
    getArtifactTypes() {
        return api.get('/v1/public/types/');
    },
    getNodes() {
        return api.get('/v1/public/nodes/');
    },
    getRegistries() {
        return api.get('/v1/public/registries/');
    }
};
