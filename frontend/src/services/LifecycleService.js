import api from './api';

export const LifecycleService = {
    /**
     * Get the citizen's lifecycle status across all major registries.
     */
    getJourneySummary() {
        return api.get('/lifecycle/journey_summary/');
    },

    /**
     * Attempt to pre-fill an application form using data from other registries.
     * @param {String} serviceCode The code of the service being applied for.
     * @param {Object} inputs Form inputs provided so far (e.g. Birth Cert No).
     */
    prefillApplication(serviceCode, inputs) {
        return api.post('/lifecycle/prefill/', {
            service_code: serviceCode,
            inputs: inputs
        });
    }
};

export default LifecycleService;
