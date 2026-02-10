<template>
  <div class="bg-white p-6 rounded-lg shadow mt-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold">Role Management (RBAC)</h2>
      <button @click="openCreateModal" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
        + Create New Role
      </button>
    </div>
    
    <div class="mb-4 max-w-sm">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search roles..." 
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500"
      >
    </div>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Users</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="role in filteredRoles" :key="role.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ role.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ role.description || 'N/A' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ role.users ? role.users.length : 0 }} users</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="openEditModal(role)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
              <button @click="deleteRoleDirect(role.id)" class="ml-4 text-red-600 hover:text-red-900">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Role Editor Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div class="relative mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
        <h2 class="text-xl font-semibold mb-4 text-center">{{ form.id ? 'Edit Role' : 'Create Role' }}</h2>
        
        <form @submit.prevent="saveRole" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Role Name</label>
              <input v-model="form.name" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Description</label>
              <input v-model="form.description" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Permissions</label>
            <input 
              type="text" 
              v-model="permSearch" 
              placeholder="Search permissions..." 
              class="mb-2 w-full px-3 py-1 text-xs border border-gray-200 rounded"
            >
            <div class="grid grid-cols-2 md:grid-cols-3 gap-2 border p-4 rounded max-h-60 overflow-y-auto bg-gray-50">
              <label v-for="perm in filteredPermissions" :key="perm" class="inline-flex items-center">
                <input type="checkbox" :value="perm" v-model="form.permissions" class="form-checkbox h-4 w-4 text-indigo-600">
                <span class="ml-2 text-sm text-gray-700">{{ perm }}</span>
              </label>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
              {{ form.id ? 'Update Role' : 'Create Role' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';

const roles = ref([]);
const showModal = ref(false);
const searchQuery = ref('');
const permSearch = ref('');

const filteredRoles = computed(() => {
    if (!searchQuery.value) return roles.value;
    const q = searchQuery.value.toLowerCase();
    return roles.value.filter(r => r.name.toLowerCase().includes(q));
});

const filteredPermissions = computed(() => {
    if (!permSearch.value) return systemPermissions;
    const q = permSearch.value.toLowerCase();
    return systemPermissions.filter(p => p.toLowerCase().includes(q));
});

const systemPermissions = [
    'view_request', 'create_request', 'view_own_request',
    'verify_document', 'approve_request', 'reject_request',
    'issue_certificate', 'view_reports', 'manage_users', 
    'manage_roles', 'view_audit_logs', 'archive_record',
    'all'
];

const form = ref({
    id: null,
    name: '',
    description: '',
    permissions: []
});

const fetchRoles = async () => {
    try {
        const response = await api.get('/roles/');
        roles.value = response.data;
    } catch (e) {
        console.error("Failed to fetch roles", e);
    }
};

const openCreateModal = () => {
    form.value = {
        name: '',
        description: '',
        permissions: []
    };
    showModal.value = true;
};

const openEditModal = (role) => {
    form.value = { ...role };
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
};

const saveRole = async () => {
    try {
        if (form.value.id) {
            await api.put(`/roles/${form.value.id}/`, form.value);
        } else {
            await api.post('/roles/', form.value);
        }
        await fetchRoles();
        closeModal();
        alert("Role saved successfully.");
    } catch (e) {
        console.error(e);
        alert("Failed to save role.");
    }
};

const deleteRoleDirect = async (id) => {
    if (!confirm("Delete this role? Users assigned to it may lose access.")) return;
    try {
        await api.delete(`/roles/${id}/`);
        await fetchRoles();
    } catch (e) {
        alert("Failed to delete role.");
    }
};

onMounted(() => {
    fetchRoles();
});
</script>
