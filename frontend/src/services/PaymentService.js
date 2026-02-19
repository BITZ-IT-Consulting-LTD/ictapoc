import api from './api';

export const PaymentService = {
    /**
     * Initiate a payment request (e.g., M-Pesa STK Push).
     * @param {Object} data { request_id, phone_number, amount, provider }
     */
    initiatePayment(data) {
        return api.post('/payments/initiate/', data);
    },

    /**
     * Check the status of a specific payment transaction.
     * @param {Number|String} txnId 
     */
    checkStatus(txnId) {
        return api.get(`/payments/${txnId}/status/`);
    },

    /**
     * List payment history related to service requests.
     */
    getPaymentHistory() {
        return api.get('/payments/');
    }
};

export default PaymentService;
