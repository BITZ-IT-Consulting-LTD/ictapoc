<template>
  <section class="page service-request-page">
    <div v-if="request" class="animate-fade-in">
      <!-- Header -->
      <header class="card card--glass mb-8 border-l-4 border-l-primary">
        <div class="card__body flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div class="flex items-center gap-4">
            <router-link to="/dashboard" class="button button--ghost button--icon hover:bg-white/50">
              <i class="bi bi-arrow-left text-xl"></i>
            </router-link>

            <div class="avatar avatar--lg avatar--primary shadow-md hidden md:flex">
              <i class="bi bi-file-earmark-richtext"></i>
            </div>

            <div>
              <div class="flex items-center gap-3 mb-1">
                <h1 class="page__title text-2xl mb-0">{{ request.service_config.service_name }}</h1>
                <span class="badge" :class="statusClass(request.status)">
                  {{ request.status.replace(/_/g, ' ') }}
                </span>
              </div>
              <p class="page__subtitle font-mono text-xs opacity-80 flex items-center gap-2">
                <i class="bi bi-hash"></i> {{ request.request_id }}
                <span class="w-1 h-1 rounded-full bg-slate-400"></span>
                <i class="bi bi-calendar3"></i> {{ formatDate(request.created_at) }}
              </p>
            </div>
          </div>

          <div class="flex gap-2">
            <button class="button button--secondary button--small">
              <i class="bi bi-printer me-2"></i> Print
            </button>
            <button class="button button--secondary button--small">
              <i class="bi bi-share me-2"></i> Share
            </button>
          </div>
        </div>
      </header>

      <div class="grid grid--sidebar">
        <!-- Main Content Column -->
        <div class="flex flex-col gap-6">

          <!-- Information Card -->
          <div class="card">
            <header class="card__header">
              <div class="flex items-center gap-2">
                <i class="bi bi-info-circle text-primary"></i>
                <h2 class="card__title">Submitted Information</h2>
              </div>
            </header>
            <div class="card__body">
              <div class="grid grid--2">
                <div v-for="(value, key) in request.payload" :key="key" class="form__group">
                  <label class="form__label">{{ key.replace(/_/g, ' ') }}</label>

                  <div v-if="value && typeof value === 'object' && value.content"
                    class="flex items-center gap-3 p-3 border border-slate-200 rounded-lg bg-slate-50 hover:bg-white hover:border-primary transition-colors group cursor-pointer"
                    @click="viewFile(value)">
                    <div
                      class="w-10 h-10 rounded bg-white border flex items-center justify-center text-primary text-xl shadow-sm">
                      <i class="bi bi-paperclip"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-bold text-main truncate group-hover:text-primary transition-colors">
                        {{ value.name }}
                      </p>
                      <p class="text-[10px] uppercase font-bold text-muted">
                        {{ (value.size / 1024).toFixed(1) }} KB
                      </p>
                    </div>
                    <i class="bi bi-eye text-muted group-hover:text-primary"></i>
                  </div>

                  <p v-else
                    class="text-lg font-bold text-main border-b border-transparent hover:border-slate-200 inline-block">
                    {{ value }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Audit Trail -->
          <div class="card">
            <header class="card__header justify-between">
              <div class="flex items-center gap-2">
                <i class="bi bi-clock-history text-primary"></i>
                <h2 class="card__title">Transaction Audit Trail</h2>
              </div>
              <span class="badge badge--info">{{ sortedLogs.length }} Events</span>
            </header>
            <div class="list">
              <div v-for="log in sortedLogs" :key="log.id" class="list__item">
                <div class="flex gap-4 w-full">
                  <div class="avatar avatar--sm avatar--secondary flex-shrink-0">
                    {{ log.actor?.username ? log.actor.username.charAt(0).toUpperCase() : 'S' }}
                  </div>
                  <div class="flex-1">
                    <div class="flex justify-between items-start mb-1">
                      <p class="font-bold text-sm text-main">{{ capitalize(log.action.replace(/_/g, ' ')) }}</p>
                      <span class="text-[10px] font-mono font-bold text-muted uppercase tracking-wider">
                        {{ formatDate(log.timestamp) }}
                      </span>
                    </div>
                    <p class="text-sm text-muted bg-slate-50 p-2 rounded border border-slate-100 italic">
                      {{ log.details }}
                    </p>

                    <button v-if="log.action === 'EDRMS_ARCHIVED'" @click="viewArchivedRecord"
                      class="button button--ghost button--small text-primary mt-2 pl-0 hover:bg-transparent hover:underline">
                      <i class="bi bi-file-earmark-lock me-1"></i> View EDRMS Record
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Column -->
        <div class="flex flex-col gap-6">

          <!-- Routing Status -->
          <div class="card">
            <header class="card__header">
              <h2 class="card__title text-sm uppercase tracking-widest">Routing Status</h2>
            </header>
            <div class="card__body flex flex-col gap-6">

              <!-- Workflow Visualization with Telemetry -->
              <div v-if="request.service_config && request.service_config.workflow_steps" class="workflow-visualizer">
                <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-3 flex justify-between">
                  <span>Step-by-Step Telemetry</span>
                  <span class="text-primary font-mono">Real-time Check</span>
                </div>
                <div class="u-flex u-flex-col u-gap-0">
                  <div v-for="(step, index) in sortedWorkflowSteps" :key="step.id" class="u-flex u-gap-3 u-relative">
                    <!-- Connector Line -->
                    <div v-if="index < sortedWorkflowSteps.length - 1" 
                         class="u-absolute u-left-[11px] u-top-[24px] u-bottom-[-16px] u-w-[2px] u-z-0"
                         :class="isStepCompleted(step) ? 'u-bg-success' : 'u-bg-slate-200'"></div>
                    
                    <!-- Step Indicator -->
                    <div class="u-w-6 u-h-6 u-rounded-full u-flex u-items-center u-justify-center u-z-10 u-flex-shrink-0 u-text-[10px] u-font-bold u-border-2 transition-all shadow-sm"
                         :class="getStepIndicatorClass(step)">
                      <i v-if="isStepCompleted(step)" class="bi bi-check-lg"></i>
                      <i v-else-if="isStepActive(step) && step.step_type === 'api_call'" class="bi bi-cpu animate-spin text-[12px]"></i>
                      <span v-else>{{ index + 1 }}</span>
                    </div>

                    <!-- Step Content -->
                    <div class="u-pb-6 u-flex-1">
                      <div class="u-flex u-items-center u-justify-between">
                        <span class="u-text-xs u-font-bold" :class="isStepActive(step) ? 'u-text-primary' : (isStepCompleted(step) ? 'u-text-main' : 'u-text-muted')">
                          {{ step.step_name }}
                        </span>
                        <div class="flex items-center gap-1">
                          <span v-if="isStepActive(step) && step.step_type === 'api_call'" 
                                class="badge badge--primary badge--pill u-py-0 u-px-1 u-text-[8px] animate-pulse">SCHEDULED</span>
                          <span v-if="isStepActive(step) && step.step_type === 'manual'" 
                                class="badge badge--warning badge--pill u-py-0 u-px-1 u-text-[8px] animate-pulse tracking-tighter">PENDING</span>
                        </div>
                      </div>
                      
                      <!-- Telemetry Breakdown -->
                      <div v-if="getExecution(step)" class="mt-1 transition-all">
                        <div class="flex flex-col gap-0.5">
                           <div class="flex items-center gap-1.5 text-[9px] font-mono font-bold">
                              <span class="text-emerald-600 uppercase">Start:</span>
                              <span class="text-slate-500">{{ formatDateCompact(getExecution(step).started_at) }}</span>
                           </div>
                           <div v-if="getExecution(step).completed_at" class="flex items-center gap-1.5 text-[9px] font-mono font-bold">
                              <span class="text-rose-600 uppercase">End:</span>
                              <span class="text-slate-500">{{ formatDateCompact(getExecution(step).completed_at) }}</span>
                           </div>
                           <div v-if="getExecution(step).duration_seconds" class="flex items-center gap-2 mt-1">
                              <div class="flex items-center gap-1 text-[9px] px-1.5 py-0.5 bg-slate-100 rounded text-slate-500 font-black">
                                <i class="bi bi-clock"></i>
                                {{ formatDuration(getExecution(step).duration_seconds) }}
                              </div>
                              <span v-if="getExecution(step).actor_details" class="text-[9px] text-muted italic">
                                — {{ getExecution(step).actor_details.username }}
                              </span>
                           </div>
                        </div>
                      </div>

                      <div v-else class="u-text-[10px] u-text-muted u-mt-0.5 u-uppercase u-tracking-wider opacity-60">
                         Queue: {{ step.role || 'System' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="form__group">
                <label class="form__label">Current Orchestration Node</label>
                <div class="flex items-center gap-3">
                  <div class="w-3 h-3 rounded-full bg-primary animate-pulse"></div>
                  <span class="font-black text-lg text-main">
                    {{ request.current_step ? request.current_step.step_name : 'Pipeline Finished' }}
                  </span>
                </div>
                <div v-if="request.current_step">
                  <span class="badge badge--warning mt-2">
                    <i class="bi bi-person-badge me-1"></i> {{ request.current_step.role }}
                  </span>
                </div>
              </div>

              <div class="form__group">
                <label class="form__label">Active Assignee</label>
                <div v-if="request.assigned_to"
                  class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="avatar avatar--sm bg-secondary text-white">
                    {{ request.assigned_to_details?.username?.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <span class="font-bold block text-sm">{{ request.assigned_to_details?.username }}</span>
                    <span class="text-[10px] uppercase text-muted font-bold">Officer ID: {{ request.assigned_to
                      }}</span>
                  </div>
                </div>
                <div v-else class="alert alert--warning m-0 text-xs">
                  <i class="bi bi-exclamation-triangle-fill"></i>
                  <span>Unassigned - In Agency Pool</span>
                </div>
              </div>
            </div>

            <!-- Claim Action Footer -->
            <div v-if="canClaim" class="card__footer bg-primary-soft">
              <button @click="claimTask" class="button button--primary w-full justify-center">
                <i class="bi bi-hand-index-thumb me-2"></i> Claim Responsibility
              </button>
            </div>
          </div>

          <!-- System Heartbeat Card -->
          <div class="card card--secondary shadow-sm">
            <header class="card__header py-3 bg-slate-50 border-b">
               <div class="flex items-center gap-2">
                 <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                 <h2 class="card__title text-[10px] uppercase font-black text-slate-500">System Dispatch Signal</h2>
               </div>
            </header>
            <div class="card__body py-3">
               <div v-if="request.status === 'in_progress'" class="flex flex-col gap-2">
                  <div class="flex items-center justify-between">
                     <span class="text-[9px] font-bold text-muted uppercase">Scheduling Mode</span>
                     <span class="text-[9px] font-bold text-emerald-600">IMMEDIATE_CHECK</span>
                  </div>
                  <div class="p-2 border border-emerald-100 bg-emerald-50/30 rounded font-mono text-[9px] text-emerald-800 leading-tight">
                     [SIGNAL] System process heartbeat active for Node ID #{{ request.current_step?.id || 'REF-0' }}...
                     <br/>
                     [QUEUE] Listening for Huduma Bridge response...
                  </div>
               </div>
               <div v-else class="text-[10px] text-muted italic text-center py-2">
                  No active scheduled process at this time.
               </div>
            </div>
          </div>

          <!-- Decision Widget -->
          <div v-if="canTakeAction" class="card border-2 border-primary shadow-lg overflow-hidden">
            <header class="card__header bg-primary text-white border-0">
              <div class="flex items-center gap-2">
                <i class="bi bi-gavel"></i>
                <h2 class="card__title text-white">Decision Action</h2>
              </div>
            </header>
            <div class="card__body bg-white">
              <form @submit.prevent="handleAction" class="form flex flex-col gap-4">
                <div class="form__group">
                  <label class="form__label">Disposition</label>
                  <div class="relative">
                    <select v-model="actionForm.action" class="form__select w-full" required>
                      <option value="">Select Outcome...</option>
                      <option value="approve">Approve & Advance</option>
                      <option value="reject">Reject & Terminate</option>
                      <option value="request_changes">Return for Correction</option>
                    </select>
                  </div>
                </div>
                <div class="form__group">
                  <label class="form__label">Official Remarks</label>
                  <textarea v-model="actionForm.details" class="form__textarea w-full" rows="4"
                    placeholder="Enter official decision notes or requirements..."></textarea>
                </div>
                <button type="submit"
                  class="button button--primary w-full justify-center shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
                  <i class="bi bi-check-circle-fill me-2"></i> Commit Decision
                </button>
              </form>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="page--centered flex-col gap-4">
      <div class="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <p class="font-bold text-muted uppercase tracking-widest text-sm">Retrieving Registry Record...</p>
    </div>

    <!-- Document Preview Modal -->
    <BaseModal v-model:show="showDocModal" title="Digital Evidence Preview"
      subtitle="Forensic view of submitted authoritative documents" icon="bi-file-earmark-check" size="lg">
      <div
        class="bg-slate-900 rounded-lg overflow-hidden h-[70vh] flex items-center justify-center relative shadow-inner">
        <iframe v-if="currentDocUrl" :src="currentDocUrl" class="w-full h-full bg-white" frameborder="0"></iframe>
        <div v-else class="text-white/50 flex flex-col items-center gap-4">
          <i class="bi bi-file-earmark-x text-6xl"></i>
          <p>No renderable content stream available</p>
        </div>
      </div>

      <template #footer>
        <button @click="showDocModal = false" class="button button--secondary">
          Close Viewer
        </button>
        <button v-if="canTakeAction" @click="quickVerifyFromModal()" class="button button--primary">
          <i class="bi bi-patch-check me-2"></i> Fast-Track Verify
        </button>
      </template>
    </BaseModal>
  </section>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router';
  import { useAuditLogStore } from '../store/auditLog';
  import { useAuthStore } from '../store/auth';
  import { useStaffStore } from '../store/staff';
  import { useServiceConfigStore } from '../store/serviceConfig';
  import api from '../services/api';
  import BaseModal from '../components/Common/BaseModal.vue';

  const route = useRoute();
  const authStore = useAuthStore();
  const staffStore = useStaffStore();
  const serviceConfigStore = useServiceConfigStore();

  const requestId = route.params.id;
  const request = ref(null);
  const showDocModal = ref(false);
  const currentDocUrl = ref(null);
  
  const sortedWorkflowSteps = computed(() => {
    if (!request.value || !request.value.service_config || !request.value.service_config.workflow_steps) return [];
    return [...request.value.service_config.workflow_steps].sort((a, b) => a.sequence - b.sequence);
  });

  const isStepCompleted = (step) => {
    if (!request.value.current_step) return true; // All steps completed if no current step and status is closed? simplified logic
    if (request.value.status === 'closed' || request.value.status === 'approved' || request.value.status === 'rejected') {
        // If terminal status, check if this step sequence is less than total steps?
        // Simple logic: if request is closed, all are done? Or maybe we need audit logs to be sure.
        // For now: 
        return step.sequence < request.value.current_step.sequence; 
    }
    return step.sequence < request.value.current_step.sequence;
  };

  const isStepActive = (step) => {
     return request.value.current_step && step.id === request.value.current_step.id;
  };

  const getStepIndicatorClass = (step) => {
      if (isStepCompleted(step)) return 'u-bg-success u-text-white u-border-success';
      if (isStepActive(step)) return 'u-bg-white u-text-primary u-border-primary ring-4 ring-primary/10';
      return 'u-bg-white u-text-muted u-border-slate-200';
  };

  const viewFile = (fileObj) => {
    if (fileObj && fileObj.content) {
      currentDocUrl.value = fileObj.content;
      showDocModal.value = true;
    } else {
      alert("Error: Document content is missing or invalid.");
    }
  };

  const quickVerifyFromModal = async () => {
    if (confirm('Verify document and proceed?')) {
      showDocModal.value = false;
      await performVerification();
    }
  };

  const performVerification = async () => {
    actionForm.value.action = 'approve';
    actionForm.value.details = 'Document verified via Evidence Preview.';
    await handleAction();
  };

  onMounted(async () => {
    try {
      const response = await api.get(`/service-requests/${requestId}/`);
      request.value = response.data;
    } catch (error) {
      console.error('Failed to fetch request:', error);
    }
  });

  const actionForm = ref({
    action: '',
    details: ''
  });

  const canTakeAction = computed(() => {
    if (!request.value || !authStore.user) return false;
    if (authStore.user.role === 'citizen') return false;
    if (request.value.status === 'closed') return false;

    // Role must match
    const currentRole = request.value.current_step?.role;
    if (authStore.user.role !== currentRole) return false;

    // Person must be assigned
    return request.value.assigned_to === authStore.user.id;
  });

  const canClaim = computed(() => {
    if (!request.value || !authStore.user) return false;
    if (request.value.status === 'closed') return false;
    if (request.value.assigned_to) return false;

    const currentRole = request.value.current_step?.role;
    return authStore.user.role === currentRole;
  });

  const fetchRequest = async () => {
    try {
      const response = await api.get(`/service-requests/${requestId}/`);
      request.value = response.data;
    } catch (error) {
      console.error('Failed to fetch request:', error);
    }
  };

  const claimTask = async () => {
    try {
      await staffStore.claimTask(requestId);
      await fetchRequest();
    } catch (error) {
      alert('Failed to claim task: ' + (error.response?.data?.detail || error.message));
    }
  };

  const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  const handleAction = async () => {
    if (!actionForm.value.action) return;

    try {
      const response = await api.post(`/service-requests/${requestId}/complete_step/`, actionForm.value);
      request.value = response.data; // Update view
      actionForm.value = { action: '', details: '' }; // Reset form
      alert('Action completed successfully.');
    } catch (error) {
      console.error('Failed to complete action:', error);
      alert('Failed to complete action.');
    }
  };

  const viewArchivedRecord = () => {
    const log = request.value?.audit_logs?.find(l => l.action === 'EDRMS_ARCHIVED');
    alert("Opening EDRMS Viewer for Record: " + (log?.details || 'Unknown'));
  };

  const sortedLogs = computed(() => {
    return [...(request.value?.audit_logs || [])].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  });

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(timestamp).toLocaleString();
  };

  const statusClass = (status) => {
    const classes = {
      received: 'badge--info',
      in_progress: 'badge--warning',
      escalated: 'badge--danger',
      approved: 'badge--success',
      rejected: 'badge--danger',
      closed: 'badge--secondary',
      validation_failed: 'badge--danger',
    };
    return classes[status] || 'badge--secondary';
  };

  const getExecution = (step) => {
    if (!request.value || !request.value.step_executions) return null;
    return request.value.step_executions.find(e => e.step === step.id);
  };

  const formatDateCompact = (timestamp) => {
    if (!timestamp) return '...';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  const formatDuration = (seconds) => {
     if (!seconds) return '0s';
     if (seconds < 60) return `${seconds}s`;
     const mins = Math.floor(seconds / 60);
     const secs = seconds % 60;
     return `${mins}m ${secs}s`;
  };
</script>

<style scoped>

  /* Component-specific Styles */
  .avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;
  }

  .avatar--lg {
    width: 3.5rem;
    height: 3.5rem;
    font-size: 1.5rem;
  }

  .avatar--sm {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 0.9rem;
  }

  .avatar--primary {
    background: var(--primary-soft);
    color: var(--primary);
  }

  .avatar--secondary {
    background: var(--bg-page);
    color: var(--text-muted);
    font-weight: 800;
    border: 1px solid var(--border-color);
  }

  .card--glass {
    background: white;
    border-bottom: 1px solid var(--border-color);
  }

  .animate-fade-in {
    animation: fadeIn 0.5s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
