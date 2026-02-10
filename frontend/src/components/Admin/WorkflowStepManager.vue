<template>
  <div class="mt-6 border-t pt-6">
    <div class="flex justify-between items-center mb-6">
      <h4 class="text-lg font-semibold">Workflow Steps</h4>
      <button type="button" @click.stop="openCreateModal" class="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
        + Add New Step
      </button>
    </div>
    
    <!-- Step List Actions -->
    <div class="mb-4">
      <div class="relative max-w-sm">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Filter steps..." 
          class="block w-full px-3 py-1 text-sm border border-gray-300 rounded-md focus:border-indigo-500 shadow-sm" 
        />
      </div>
    </div>

    <!-- Step List -->
    <ul class="space-y-2 mt-4">
      <li v-for="step in filteredSteps" :key="step.id" class="flex justify-between items-center p-3 bg-white border rounded-md hover:border-indigo-300 transition-colors shadow-sm">
        <div>
          <span class="font-bold text-gray-700">{{ step.sequence }}. {{ step.step_name }}</span>
          <span class="text-xs px-2 py-0.5 ml-2 rounded-full uppercase font-medium bg-blue-50 text-blue-600 border border-blue-100">{{ step.step_type }}</span>
          <span v-if="step.step_type === 'manual'" class="text-sm text-gray-500 ml-4">
            <span class="font-medium text-gray-600">Role:</span> {{ step.role }} | <span class="font-medium text-gray-600">Action:</span> {{ step.action }}
          </span>
          <span v-if="step.step_type === 'api_call'" class="text-sm text-gray-500 ml-4">
            <span class="font-medium text-gray-600">URL:</span> {{ step.api_config?.url || 'N/A' }}
          </span>
        </div>
        <div>
          <button type="button" @click.stop="editStep(step)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Edit</button>
          <button type="button" @click.stop="deleteStep(step.id)" class="ml-4 text-red-600 hover:text-red-900 text-sm font-medium">Delete</button>
        </div>
      </li>
    </ul>
    <p v-if="filteredSteps.length === 0" class="text-center py-8 text-gray-400 italic text-sm border-2 border-dashed border-gray-100 rounded-lg">
      No workflow steps found matching your filter.
    </p>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-[60]">
      <div class="relative mx-auto p-6 border w-full max-w-2xl shadow-xl rounded-lg bg-white">
        <h5 class="text-lg font-bold mb-6 text-center text-gray-800">
          {{ stepForm.id ? '🛠️ Edit Workflow Step' : '➕ Add New Workflow Step' }}
        </h5>
        
        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700">Sequence</label>
              <input type="number" v-model.number="stepForm.sequence" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700">Step Name</label>
              <input type="text" v-model="stepForm.step_name" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required placeholder="e.g. Document Verification">
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700">Step Type</label>
            <select v-model="stepForm.step_type" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option value="manual">Manual Verification / Action</option>
              <option value="api_call">Automated API Call</option>
            </select>
          </div>

          <!-- Manual Step Fields -->
          <div v-if="stepForm.step_type === 'manual'" class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-gray-50 p-4 rounded-md">
            <div>
              <label class="block text-sm font-semibold text-gray-700">Responsible Role</label>
              <input type="text" v-model="stepForm.role" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="e.g. officer">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700">Action Key</label>
              <input type="text" v-model="stepForm.action" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="e.g. approve">
            </div>
          </div>

          <!-- API Call Step Fields -->
          <div v-if="stepForm.step_type === 'api_call'" class="bg-gray-50 p-4 rounded-md">
            <div class="mb-3 p-3 bg-indigo-50 border border-indigo-100 rounded text-xs text-indigo-700 flex items-start">
              <span class="mr-2">💡</span>
              <p>
                <strong>Need help with values?</strong> Refer to the 
                <span class="font-bold underline cursor-help" title="Check the 'API Docs' tab in the Admin Dashboard for authoritative system URLs and JSON structures.">Authoritative API Registry</span> 
                for standard KESEL Bridge endpoints and payload samples.
              </p>
            </div>
            <label class="block text-sm font-semibold text-gray-700">API Configuration (JSON)</label>
            <textarea v-model="apiConfigAsString" rows="6" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 font-mono text-sm" placeholder='e.g. {"url": "https://...", "method": "POST"}'></textarea>
            <p class="mt-2 text-xs text-gray-500 italic">Configure the endpoint details that the system should trigger automatically.</p>
          </div>

          <div class="flex justify-end space-x-3 pt-4 border-t">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md shadow-sm hover:bg-gray-50 font-medium">
              Cancel
            </button>
            <button type="button" @click="handleStepSubmit" class="px-5 py-2 bg-indigo-600 text-white rounded-md shadow-sm hover:bg-indigo-700 font-medium">
              {{ stepForm.id ? 'Save Changes' : 'Create Step' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useWorkflowStepStore } from '../../store/workflowStep';

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
