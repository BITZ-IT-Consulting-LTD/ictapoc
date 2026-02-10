<template>
  <div>
    <router-link to="/dashboard" class="text-indigo-600 hover:text-indigo-900 mb-4 inline-block">&larr; Back to Dashboard</router-link>
    <div v-if="request" class="bg-white p-8 rounded-lg shadow">
      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-3xl font-bold">{{ request.service_config.service_name }}</h1>
          <p class="text-gray-500">Request ID: {{ request.request_id }}</p>
        </div>
        <span class="px-3 py-1.5 text-sm font-semibold rounded-full" :class="statusClass(request.status)">
          {{ request.status }}
        </span>
      </div>

      <div class="mt-6 border-t pt-6">
        <h2 class="text-xl font-semibold mb-4">Submitted Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-50 p-4 rounded-md">
          <div v-for="(value, key) in request.payload" :key="key">
            <label class="block text-sm font-medium text-gray-700 capitalize">{{ key.replace(/_/g, ' ') }}</label>
            <div v-if="value && typeof value === 'object' && value.content">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  FILE: {{ value.name }} ({{ (value.size / 1024).toFixed(1) }} KB)
                </span>
                <button 
                  @click="viewFile(value)" 
                  class="ml-2 text-xs text-indigo-600 hover:text-indigo-900 underline focus:outline-none"
                >
                  View / Download
                </button>
            </div>
            <p v-else class="text-gray-600">{{ value }}</p>
          </div>
        </div>
      </div>

      <div class="mt-6 border-t pt-6">
        <h2 class="text-xl font-semibold mb-4">Current Status</h2>
        <div class="flex items-center">
            <div class="flex-1">
                <p class="text-sm text-gray-500">Current Step</p>
                <p class="text-lg font-medium">{{ request.current_step ? request.current_step.step_name : 'Completed' }}</p>
                <div v-if="request.current_step" class="mt-2 flex items-center gap-4">
                  <p class="text-xs text-gray-400">Target Role: <span class="font-bold text-gray-600">{{ request.current_step.role }}</span></p>
                  <p v-if="request.assigned_to" class="text-xs text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100 flex items-center gap-1">
                    <span class="w-1.5 h-1.5 bg-indigo-600 rounded-full animate-pulse"></span>
                    Claimed by: <span class="font-bold">{{ request.assigned_to_details?.username }}</span>
                  </p>
                  <p v-else class="text-xs text-gray-500 bg-gray-50 px-2 py-0.5 rounded border border-gray-100 italic">
                    Unassigned Pool
                  </p>
                </div>
            </div>
        </div>
      </div>

      <!-- Claim Task Banner -->
      <div v-if="canClaim" class="mt-8 border-t pt-6 bg-slate-50 p-6 rounded-lg border border-slate-200 flex flex-col items-center text-center">
        <h3 class="text-xl font-bold text-slate-900 mb-2">This task is available in your pool.</h3>
        <p class="text-slate-600 mb-4 max-w-md">You need to claim this document before you can process the current workflow step.</p>
        <button @click="claimTask" class="px-8 py-3 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-700 shadow-lg transition-all transform hover:scale-105">
          Claim & Start Processing
        </button>
      </div>

      <!-- Actions -->
      <div v-if="canTakeAction" class="mt-8 border-t pt-6 bg-blue-50 p-4 rounded-md">
        <h3 class="text-lg font-medium mb-4">Take Action</h3>
        <form @submit.prevent="handleAction" class="space-y-4">
            <div>
                <label class="block text-sm font-medium">Action</label>
                <select v-model="actionForm.action" class="mt-1 block w-full border rounded-md p-2">
                    <option value="">Select Action...</option>
                    <option value="approve">Approve / Proceed</option>
                    <option value="reject">Reject</option>
                    <option value="request_changes">Request Changes</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium">Comments / Notes</label>
                <textarea v-model="actionForm.details" rows="3" class="mt-1 block w-full border rounded-md p-2"></textarea>
            </div>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Submit Decision</button>
        </form>
      </div>

       <!-- Audit Logs -->
      <div class="mt-8 border-t pt-6">
        <h3 class="text-lg font-medium mb-4">History</h3>
        <ul class="space-y-4">
          <li v-for="log in sortedLogs" :key="log.id" class="flex items-start">
            <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center mr-4">
               <span class="text-gray-600 text-xs">{{ log.actor?.username ? log.actor.username.substring(0, 2) : 'Sys' }}</span>
            </div>
            <div>
              <p class="font-semibold">{{ capitalize(log.action.replace(/_/g, ' ')) }}</p>
              <p class="text-sm text-gray-600">{{ log.details }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ formatDate(log.timestamp) }}</p>

              <!-- Mock Document Viewer trigger -->
              <button v-if="log.action === 'EDRMS_ARCHIVED'" @click="viewArchivedRecord" class="mt-2 text-indigo-600 hover:text-indigo-800 text-sm font-medium flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
                View Archived Record (Mock PDF)
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <p>Loading request details...</p>
    </div>
    <!-- Document Preview Modal (Teleported to Body) -->
    <Teleport to="body">
      <div v-if="showDocModal" class="fixed inset-0 z-[9999] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showDocModal = false"></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                  <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                    Document Preview
                  </h3>
                  <div class="mt-4 h-[600px] bg-gray-100 border rounded">
                    <iframe v-if="currentDocUrl" :src="currentDocUrl" class="w-full h-full" frameborder="0"></iframe>
                    <p v-else class="text-center pt-20 text-gray-400">No document source</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button 
                v-if="canTakeAction"
                @click="quickVerifyFromModal()"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm"
              >
                Verify & Close
              </button>
              <button 
                type="button" 
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                @click="showDocModal = false"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useCitizenStore } from '../store/citizen';
import { useAuditLogStore } from '../store/auditLog';
import { useAuthStore } from '../store/auth';
import { useStaffStore } from '../store/staff';
import api from '../services/api';

const route = useRoute();
const authStore = useAuthStore();
const staffStore = useStaffStore();

const requestId = route.params.id;
const request = ref(null);
const showDocModal = ref(false);
const currentDocUrl = ref(null);

const viewFile = (fileObj) => {
  console.log("View File Clicked", fileObj);
  
  if (fileObj && fileObj.content) {
    console.log("Opening Modal with URL length:", fileObj.content.length);
    currentDocUrl.value = fileObj.content;
    showDocModal.value = true;
  } else {
    console.error("File object missing content property");
    alert("Error: Document content is missing or invalid.");
  }
};

const quickVerify = async () => {
    if (confirm('Are you sure you want to verify this document and proceed?')) {
      await performVerification();
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
    actionForm.value.details = 'Document verified via Quick Action.';
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

// Check for EDRMS Archive Log
const edrmsRecord = computed(() => {
  if (!request.value?.audit_logs) return null;
  const log = request.value.audit_logs.find(l => l.action === 'EDRMS_ARCHIVED');
  if (log) {
      // Mock parsing details: "Archived to EDRMS. Doc ID: MEMO-2026-X"
      return {
          details: log.details
      };
  }
  return null;
});

const viewArchivedRecord = () => {
    alert("Opening EDRMS Viewer for Record: " + edrmsRecord.value.details);
};

const sortedLogs = computed(() => {
  // This computed property is no longer directly used if auditLogStore is removed,
  // but keeping it for now if request.value.audit_logs is expected to exist.
  // If audit_logs are fetched directly into request.value, this would still work.
  return [...(request.value?.audit_logs || [])].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
});

const formatDate = (timestamp) => {
  if (!timestamp) return 'N/A';
  return new Date(timestamp).toLocaleString();
};

const statusClass = (status) => {
  const classes = {
    received: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    escalated: 'bg-orange-100 text-orange-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    closed: 'bg-gray-100 text-gray-800',
    validation_failed: 'bg-red-100 text-red-800',
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};
</script>
