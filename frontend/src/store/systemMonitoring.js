import { defineStore } from 'pinia';
import api from '../services/api';

export const useSystemMonitoringStore = defineStore('systemMonitoring', {
    state: () => ({
        activeTrace: null,
        lastLogId: null,
        isLive: true,
    }),
    actions: {
        broadcastTrace(layerInfo) {
            this.activeTrace = {
                timestamp: new Date().toLocaleTimeString(),
                ...layerInfo,
                id: Math.random().toString(36).substr(2, 9)
            };
        },
        async pollForEvents() {
            try {
                const response = await api.get('/audit-logs/');
                const logs = response.data;
                if (logs.length > 0) {
                    const latestLog = logs[0]; // Assuming ordered by -timestamp
                    if (this.lastLogId === null) {
                        this.lastLogId = latestLog.id;
                        return;
                    }
                    if (latestLog.id !== this.lastLogId) {
                        this.lastLogId = latestLog.id;
                        this.processLogEvent(latestLog);
                    }
                }
            } catch (error) {
                console.error("Polling error:", error);
            }
        },
        processLogEvent(log) {
            // Map AuditLog actions to Architectural Trace events
            let eventType = null;
            if (log.action === 'REQUEST_SUBMITTED') eventType = 'SERVICE_SUBMISSION';
            else if (log.action.includes('OFFICER_ACTION')) eventType = 'WORKFLOW_STEP_COMPLETION';
            else if (log.action === 'KESEL_EXCHANGE_SUCCESS') eventType = 'BRIDGE_EXCHANGE';
            else if (log.action === 'EDRMS_ARCHIVED') eventType = 'DATA_ARCHIVAL';
            else if (log.action === 'DIGITAL_SIGNATURE_VERIFIED') eventType = 'DIGITAL_SIGNATURE_VERIFIED';

            if (eventType) {
                this.broadcastTrace({
                    type: eventType,
                    requestId: log.service_request?.request_id,
                    details: log.details,
                    action: log.action
                });
            }
        }
    }
});
