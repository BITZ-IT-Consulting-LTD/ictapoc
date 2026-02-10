<template>
  <div class="bg-white p-6 rounded-lg shadow mt-8">
    <h3 class="text-xl font-semibold mb-4">User & Staff Management</h3>

    <div class="mb-6 flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="flex flex-1 gap-4 w-full md:w-auto">
        <div class="relative max-w-sm flex-1">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search users..." 
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
        </div>
        <div class="flex gap-2">
          <select v-model="roleFilter" class="block w-36 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="">All Roles</option>
            <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
          </select>
          <select v-model="mdaFilter" class="block w-40 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="">All MDAs</option>
            <option :value="null">Global / Citizen</option>
            <option v-for="mda in mdas" :key="mda.id" :value="mda.id">{{ mda.name }}</option>
          </select>
        </div>
      </div>
      <button @click="openCreateModal" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 shadow-sm font-medium transition-colors">
        + Add New User
      </button>
    </div>

    <!-- User Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">MDA Assignment</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="u in filteredUsers" :key="u.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ u.username }}</div>
              <div class="text-sm text-gray-500">{{ u.email }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                {{ u.user_role_details?.name || u.role }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ getMdaName(u.mda) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="openEditModal(u)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
              <button @click="deleteUser(u.id)" class="ml-4 text-red-600 hover:text-red-900">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit User Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div class="relative mx-auto p-6 border w-full max-w-lg shadow-xl rounded-lg bg-white">
        <h3 class="text-xl font-bold text-gray-900 text-center mb-6">{{ form.id ? 'Edit User' : 'Create New User' }}</h3>
        
        <form @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div v-if="!form.id" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Username</label>
                <input v-model="form.username" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Email Address</label>
                <input v-model="form.email" type="email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700">Password</label>
                <input v-model="form.password" type="password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required placeholder="Secure password">
              </div>
            </div>
            <p v-else class="text-sm text-gray-500 mb-6 text-center">Modifying assignments for <strong>{{ form.username }}</strong></p>

            <div>
              <label class="block text-sm font-medium text-gray-700">Role</label>
              <select v-model="form.user_role_id" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
              </select>
            </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700">MDA Assignment</label>
                <div class="mt-1 space-y-2">
                  <input 
                    type="text" 
                    v-model="mdaDropdownSearch" 
                    placeholder="Search MDAs..." 
                    class="block w-full px-2 py-1 text-xs border border-gray-200 rounded focus:ring-indigo-500 focus:border-indigo-500"
                  >
                  <select v-model="form.mda" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    <option :value="null">No MDA (Independent)</option>
                    <option v-for="mda in filteredMdasForDropdown" :key="mda.id" :value="mda.id">{{ mda.name }} ({{ mda.code }})</option>
                  </select>
                </div>
                <p class="mt-1 text-xs text-gray-500">Staff will only see workflows associated with this MDA.</p>
              </div>
          </div>
          <div class="flex justify-end mt-6 space-x-3">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../../services/api';
import { useMdaStore } from '../../store/mda';

const mdaStore = useMdaStore();
const mdas = computed(() => mdaStore.mdas);

const users = ref([]);
const roles = ref([]);
const searchQuery = ref('');
const roleFilter = ref('');
const mdaFilter = ref('');

const filteredUsers = computed(() => {
  let result = users.value;

  if (roleFilter.value) {
    result = result.filter(u => u.user_role === Number(roleFilter.value));
  }

  if (mdaFilter.value !== '') {
    // If user selected "All MDAs", mdaFilter is empty string
    // If user selected "Global / Citizen", mdaFilter is null (from the option value)
    // Otherwise it's the MDA ID
    const filterValue = mdaFilter.value === null ? null : (mdaFilter.value === '' ? undefined : Number(mdaFilter.value));
    
    if (filterValue !== undefined) {
      result = result.filter(u => u.mda === filterValue);
    }
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(u => 
      u.username.toLowerCase().includes(q) || 
      u.email.toLowerCase().includes(q)
    );
  }
  
  return result;
});

const mdaDropdownSearch = ref('');
const filteredMdasForDropdown = computed(() => {
  if (!mdaDropdownSearch.value) return mdas.value;
  const q = mdaDropdownSearch.value.toLowerCase();
  return mdas.value.filter(m => m.name.toLowerCase().includes(q) || (m.code && m.code.toLowerCase().includes(q)));
});
const showModal = ref(false);
const form = ref({
  id: null,
  username: '',
  email: '',
  password: '',
  user_role_id: null,
  mda: null,
});

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/');
    users.value = response.data;
  } catch (e) {
    console.error("Failed to fetch users", e);
  }
};

const fetchRoles = async () => {
  try {
    const response = await api.get('/roles/');
    roles.value = response.data;
  } catch (e) {
    console.error("Failed to fetch roles", e);
  }
};

const getMdaName = (mdaId) => {
  if (!mdaId) return 'Global / Citizen';
  const mda = mdas.value.find(m => m.id === mdaId);
  return mda ? `${mda.name} (${mda.code})` : 'Unknown MDA';
};

onMounted(() => {
  fetchUsers();
  fetchRoles();
  mdaStore.fetchMdas();
});

const openCreateModal = () => {
  form.value = {
    id: null,
    username: '',
    email: '',
    password: '',
    user_role_id: roles.value.length > 0 ? roles.value[0].id : null,
    mda: null,
  };
  showModal.value = true;
};

const openEditModal = (u) => {
  form.value = {
    id: u.id,
    username: u.username,
    email: u.email,
    user_role_id: u.user_role || null,
    mda: u.mda || null,
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleSubmit = async () => {
  try {
    if (form.value.id) {
      await api.patch(`/users/${form.value.id}/`, {
        user_role: form.value.user_role_id,
        mda: form.value.mda
      });
    } else {
      await api.post(`/users/register/`, {
        username: form.value.username,
        email: form.value.email,
        password: form.value.password,
        user_role: form.value.user_role_id,
        mda: form.value.mda,
        role: 'staff' // Default to staff role for admin creation
      });
    }
    await fetchUsers();
    closeModal();
    alert(form.value.id ? "User updated successfully." : "User created successfully.");
  } catch (e) {
    console.error(e);
    alert("Failed to save user: " + (e.response?.data?.message || e.message));
  }
};

const deleteUser = async (id) => {
  if (confirm('Are you sure you want to delete this user? This cannot be undone.')) {
    try {
      await api.delete(`/users/${id}/`);
      await fetchUsers();
    } catch (e) {
      alert("Failed to delete user.");
    }
  }
};
</script>
