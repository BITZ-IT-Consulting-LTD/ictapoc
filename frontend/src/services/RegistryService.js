import api from './api';

export const RegistryService = {
    /**
     * Fetch authoritative data from a national registry.
     * @param {String} code Registry code (e.g., IPRS, KRA, CRS)
     * @param {String} identifier Unique ID (e.g., ID Number, PIN)
     * @param {String} field Optional field name override
     */
    fetchFromRegistry(code, identifier, field = null) {
        const registryPath = code.toLowerCase();
        const params = field ? { field } : {};

        return api.get(`/registries/${registryPath}/${identifier}/`, { params });
    },

    /**
     * Query multiple registries (Legacy approach via direct query endpoint).
     * @param {Object} data { registry, identifier, field }
     */
    queryRegistry(data) {
        return api.post('/registry/query/', data);
    },

    /**
     * Admin dump of all registry configurations.
     */
    getRegistryDump() {
        return api.get('/registry/query/');
    }
};

export default RegistryService;
