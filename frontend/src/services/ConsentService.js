import api from './api';

export const ConsentService = {
    /**
     * List user's own consent records.
     */
    getMyConsents() {
        return api.get('/consent/');
    },

    /**
     * Grant a new data processing permission.
     * @param {Object} data { requester_id, scope, purpose_code, expires_in_days }
     */
    grantConsent(data) {
        return api.post('/consent/grant/', data);
    },

    /**
     * Revoke an existing consent record.
     * @param {Number|String} id 
     */
    revokeConsent(id) {
        return api.post(`/consent/${id}/revoke/`);
    },

    /**
     * Check if active consent exists for a specific scope.
     * @param {String} scope 
     * @param {String} requester_code 
     */
    checkConsent(scope, requester_code) {
        return api.get('/consent/check/', {
            params: { scope, requester_code }
        });
    }
};

export default ConsentService;
