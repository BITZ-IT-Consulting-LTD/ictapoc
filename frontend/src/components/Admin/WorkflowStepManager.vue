<template>
  <div class="workflow-step-manager">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
      <div>
        <h4 class="text-lg font-bold text-main">Workflow Pipeline Designer</h4>
        <p class="text-sm text-muted">Configure the sequence of manual and automated processing stages</p>
      </div>
      <button type="button" @click.stop="openCreateModal"
        class="button button--secondary button--small shadow-sm hover:shadow transition-shadow">
        <i class="bi bi-plus-lg me-1"></i> Append Stage
      </button>
    </div>

    <div class="toolbar mb-6">
      <div class="relative w-full">
        <i class="bi bi-search absolute left-4 top-1/2 -translate-y-1/2 text-muted"></i>
        <input type="text" v-model="searchQuery" placeholder="Filter pipeline stages..."
          class="form__input pl-12 w-full" />
      </div>
    </div>

    <!-- Step List -->
    <div class="list space-y-3">
      <div v-for="step in filteredSteps" :key="step.id"
        class="list__item bg-white border border-border-color rounded-lg p-4 hover:shadow-md transition-all cursor-default group">
        <div class="flex items-center gap-4 w-full">
          <div
            class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-slate-100 rounded-lg font-mono font-black text-slate-500 text-lg border border-slate-200 shadow-inner">
            {{ step.sequence }}
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-3 mb-1">
              <span class="font-bold text-main truncate">{{ step.step_name }}</span>
              <span class="badge badge--small font-mono uppercase tracking-wider text-[10px]"
                :class="step.step_type === 'manual' ? 'badge--info' : 'badge--warning'">
                {{ step.step_type === 'manual' ? 'Manual Intervention' : 'Automated Logic' }}
              </span>
            </div>

            <div class="text-xs text-muted flex items-center gap-4 truncate">
              <span v-if="step.step_type === 'manual'" class="flex items-center gap-1">
                <i class="bi bi-person-badge"></i>
                <span class="font-bold">{{ step.role }}</span>
                <i class="bi bi-arrow-right text-slate-300 mx-1"></i>
                <span>{{ step.action }}</span>
              </span>
              <span v-if="step.step_type === 'api_call'" class="flex items-center gap-1 font-mono text-[10px]">
                <i class="bi bi-hdd-network"></i> {{ step.api_config?.url || 'N/A' }}
              </span>
            </div>
          </div>

          <div class="flex gap-2 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
            <button type="button" @click.stop="editStep(step)"
              class="button button--secondary button--small button--icon text-primary hover:bg-indigo-50"
              title="Edit Stage">
              <i class="bi bi-pencil-square"></i>
            </button>
            <button type="button" @click.stop="deleteStep(step.id)"
              class="button button--secondary button--small button--icon text-danger hover:bg-red-50"
              title="Remove Stage">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <div v-if="filteredSteps.length === 0" class="alert alert--info flex items-center gap-3 p-4">
        <i class="bi bi-info-circle-fill text-xl"></i>
        <span>No active pipeline stages found. Begin by appending a new stage to this service.</span>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <BaseModal v-model:show="showModal" :title="stepForm.id ? 'Modify Pipeline Stage' : 'Design New Pipeline Stage'"
      subtitle="Define technical parameters for this orchestration node" icon="bi-diagram-3-fill" size="md">
      <form @submit.prevent="handleStepSubmit" class="form flex flex-col gap-6">
        <div class="grid grid--2 gap-6">
          <div class="form__group">
            <label class="form__label">Execution Sequence</label>
            <input type="number" v-model.number="stepForm.sequence" class="form__input font-mono font-bold" required>
          </div>

          <div class="form__group">
            <label class="form__label">Processing Logic</label>
            <div class="relative">
              <select v-model="stepForm.step_type" class="form__select w-full">
                <option value="manual">Manual Action (Institutional Staff)</option>
                <option value="api_call">Automated Logic (External API Bridge)</option>
              </select>
            </div>
          </div>

          <div class="form__group md:col-span-2">
            <label class="form__label">Stage Designation</label>
            <input type="text" v-model="stepForm.step_name" class="form__input font-bold" required
              placeholder="e.g. Identity Verification">
          </div>
        </div>

        <!-- Manual Step Fields -->
        <div v-if="stepForm.step_type === 'manual'" class="card bg-slate-50 border border-slate-200 shadow-none">
          <div class="card__body p-6">
            <div class="grid grid--2 gap-4">
              <div class="form__group">
                <label class="form__label">Assigned Institutional Role</label>
                <div class="relative">
                  <i class="bi bi-person-badge absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
                  <input type="text" v-model="stepForm.role" class="form__input pl-10" placeholder="e.g. officer">
                </div>
              </div>
              <div class="form__group">
                <label class="form__label">Functional Action Code</label>
                <div class="relative">
                  <i class="bi bi-lightning-charge absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
                  <input type="text" v-model="stepForm.action" class="form__input pl-10" placeholder="e.g. approve">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- API Call Step Fields -->
        <div v-if="stepForm.step_type === 'api_call'" class="card bg-indigo-50 border border-indigo-100 shadow-none">
          <div class="card__body p-6">
            <div class="alert alert--info mb-4 text-xs font-medium">
              <i class="bi bi-info-circle-fill me-2"></i>
              Secure handshake parameters must follow GOK Interoperability Standards.
            </div>
            <div class="form__group">
              <label class="form__label">Payload Configuration (JSON)</label>
              <textarea v-model="apiConfigAsString" rows="6" class="form__textarea font-mono text-xs w-full bg-white"
                placeholder='{"url": "https://api.gov.ke/...", "method": "POST"}'></textarea>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t border-border-color">
          <button type="button" @click="closeModal" class="button button--secondary">Cancel</button>
          <button type="submit"
            class="button button--primary shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <i class="bi bi-cloud-upload me-2"></i> {{ stepForm.id ? 'Save Stage' : 'Deploy Stage' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
  import { ref, computed, watch } from 'vue';
  import { useWorkflowStepStore } from '../../store/workflowStep';
  import BaseModal from '../Common/BaseModal.vue';

  const props = defineProps({
    serviceConfigId: {
      type: Number,
      required: true,
    },
  });

  const stepStore = useWorkflowStepStore();
  const showModal = ref(false);
  const searchQuery = ref('');

  const stepForm = ref({
    id: null,
    service_config: props.serviceConfigId,
    sequence: 1,
    step_name: '',
    step_type: 'manual',
    role: '',
    action: '',
    api_config: null,
  });

  // Computed property to handle JSON conversion for the textarea
  const apiConfigAsString = computed({
    get: () => stepForm.value.api_config ? JSON.stringify(stepForm.value.api_config, null, 2) : '',
    set: (value) => {
      try {
        stepForm.value.api_config = value ? JSON.parse(value) : null;
      } catch (e) {
        console.error('Invalid JSON for API config:', e);
        // Optionally handle invalid JSON input, e.g., by setting an error state
      }
    },
  });

  watch(() => props.serviceConfigId, (newId) => {
    if (newId) {
      stepStore.fetchSteps(newId);
      stepForm.value.service_config = newId;
    }
  }, { immediate: true });

  const sortedSteps = computed(() => stepStore.steps.slice().sort((a, b) => a.sequence - b.sequence));

  const filteredSteps = computed(() => {
    console.log("Re-calculating filteredSteps. Current store steps:", stepStore.steps);
    if (!searchQuery.value) return sortedSteps.value;
    const q = searchQuery.value.toLowerCase();
    return sortedSteps.value.filter(s =>
      s.step_name.toLowerCase().includes(q) ||
      (s.role && s.role.toLowerCase().includes(q))
    );
  });

  const handleStepSubmit = async () => {
    const payload = { ...stepForm.value };

    if (!payload.service_config) {
      alert("System Error: Service Configuration ID is missing.");
      return;
    }

    if (payload.step_type === 'manual') {
      payload.api_config = null;
    } else {
      payload.role = null;
      payload.action = null;
    }

    try {
      console.log("Submitting step with payload:", payload);
      let success = false;
      if (payload.id) {
        success = await stepStore.updateStep(payload);
      } else {
        success = await stepStore.createStep(payload);
      }

      if (success) {
        alert("Workflow step saved successfully.");
        closeModal();
      } else {
        alert("Failed to save workflow step. Please check console.");
      }
    } catch (error) {
      console.error("WorkflowStep Submit Error:", error);
      const msg = error.response?.data ? JSON.stringify(error.response.data) : error.message;
      alert("Critical Error: " + msg);
    }
  };

  const openCreateModal = () => {
    resetStepForm();
    showModal.value = true;
  };

  const editStep = (step) => {
    stepForm.value = { ...step };
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
    resetStepForm();
  };

  const deleteStep = async (id) => {
    if (confirm('Are you sure you want to delete this workflow step?')) {
      await stepStore.deleteStep(id);
    }
  };

  const resetStepForm = () => {
    let nextSequence = 1;
    if (sortedSteps.value && sortedSteps.value.length > 0) {
      const maxSeq = Math.max(...sortedSteps.value.map(s => parseInt(s.sequence || 0)));
      nextSequence = isNaN(maxSeq) ? sortedSteps.value.length + 1 : maxSeq + 1;
    }

    console.log("Resetting form with serviceConfigId:", props.serviceConfigId, "Next sequence:", nextSequence);

    stepForm.value = {
      id: null,
      service_config: props.serviceConfigId,
      sequence: nextSequence,
      step_name: '',
      step_type: 'manual',
      role: '',
      action: '',
      api_config: null,
    };
  };
</script>

<style scoped>
  .text-muted {
    color: var(--text-muted);
  }

  .text-main {
    color: var(--text-main);
  }

  .text-primary {
    color: var(--primary);
  }

  .text-danger {
    color: var(--danger);
  }

  .border-border-color {
    border-color: var(--border-color);
  }
</style>
