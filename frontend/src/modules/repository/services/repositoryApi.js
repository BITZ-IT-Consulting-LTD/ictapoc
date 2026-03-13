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
    updateArtifactVisibility(id, is_public) {
        return api.patch(`/v1/artifacts/${id}/`, { is_public });
    },
    updateArtifact(id, payload) {
        return api.patch(`/v1/artifacts/${id}/`, payload);
    },
    createArtifact(payload) {
        return api.post('/v1/artifacts/', payload);
    },
    deleteArtifact(id) {
        return api.delete(`/v1/artifacts/${id}/`);
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
    getProjects() {
        return api.get('/v1/projects/');
    },
    createProject(payload) {
        return api.post('/v1/projects/', payload);
    },
    deleteProject(id) {
        return api.delete(`/v1/projects/${id}/`);
    },
    getProjectPhases() {
        return api.get('/v1/phases/');
    },
    createProjectPhase(payload) {
        return api.post('/v1/phases/', payload);
    },
    deleteProjectPhase(id) {
        return api.delete(`/v1/phases/${id}/`);
    },
    
    // Artifact Types
    getArtifactTypes() {
        return api.get('/v1/types/');
    },
    createArtifactType(payload) {
        return api.post('/v1/types/', payload);
    },
    deleteArtifactType(id) {
        return api.delete(`/v1/types/${id}/`);
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

    // Nodes
    getNodes() {
        return api.get('/v1/nodes/');
    },
    createNode(payload) {
        return api.post('/v1/nodes/', payload);
    },
    deleteNode(id) {
        return api.delete(`/v1/nodes/${id}/`);
    },

    // Node Types
    getNodeTypes() {
        return api.get('/v1/node-types/');
    },
    createNodeType(payload) {
        return api.post('/v1/node-types/', payload);
    },
    deleteNodeType(id) {
        return api.delete(`/v1/node-types/${id}/`);
    },

    // Registries
    getRegistries() {
        return api.get('/v1/registries/');
    },
    createRegistry(payload) {
        return api.post('/v1/registries/', payload);
    },
    deleteRegistry(id) {
        return api.delete(`/v1/registries/${id}/`);
    }
};
