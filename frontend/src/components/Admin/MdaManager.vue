<template>
  <div class="bg-white p-6 rounded-lg shadow mt-8">
    <h3 class="text-xl font-semibold mb-4">Manage MDAs</h3>

    <!-- Actions -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
      <div class="relative">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Filter MDAs..." 
          class="block w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
      </div>
      <button 
        @click="openCreateModal" 
        class="flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <span class="mr-2">+</span> Create New MDA
      </button>
    </div>

    <!-- MDA List -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">MDA Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Head of MDA</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="mda in filteredMdas" :key="mda.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ mda.code || 'N/A' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ mda.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ mda.head_of_mda || 'N/A' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="openEditModal(mda)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
              <button @click="deleteMda(mda.id)" class="ml-4 text-red-600 hover:text-red-900">Delete</button>
            </td>
          </tr>
          <tr v-if="mdas.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-gray-500">No MDAs found. Create one to get started.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div class="relative mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
        <h3 class="text-lg leading-6 font-medium text-gray-900 text-center mb-4">{{ form.id ? 'Edit MDA' : 'Create New MDA' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="mda-name" class="block text-sm font-medium text-gray-700">MDA Name</label>
              <input type="text" v-model="form.name" id="mda-name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required placeholder="e.g. Ministry of Health">
            </div>
            <div>
              <label for="mda-code" class="block text-sm font-medium text-gray-700">Official Code</label>
              <input type="text" v-model="form.code" id="mda-code" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="e.g. MOH">
            </div>
            <div class="md:col-span-2">
              <label for="mda-description" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea v-model="form.description" id="mda-description" rows="2" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Brief description of responsibilities"></textarea>
            </div>
            <div>
              <label for="mda-head" class="block text-sm font-medium text-gray-700">Head of MDA</label>
              <input type="text" v-model="form.head_of_mda" id="mda-head" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="e.g. CS Health">
            </div>
            <div>
              <label for="mda-email" class="block text-sm font-medium text-gray-700">Contact Email</label>
              <input type="email" v-model="form.contact_email" id="mda-email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="email@domain.go.ke">
            </div>
            <div>
              <label for="mda-phone" class="block text-sm font-medium text-gray-700">Contact Phone</label>
              <input type="text" v-model="form.contact_phone" id="mda-phone" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="+254...">
            </div>
            <div>
              <label for="mda-website" class="block text-sm font-medium text-gray-700">Website URL</label>
              <input type="url" v-model="form.website" id="mda-website" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="https://...">
            </div>
            <div class="md:col-span-2">
              <label for="mda-address" class="block text-sm font-medium text-gray-700">Physical Address</label>
              <textarea v-model="form.address" id="mda-address" rows="1" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Building, Street, City"></textarea>
            </div>
          </div>
          <div class="flex justify-end mt-6 space-x-3">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">{{ form.id ? 'Update' : 'Create' }}</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useMdaStore } from '../../store/mda';

const mdaStore = useMdaStore();
const mdas = computed(() => mdaStore.mdas);
const searchQuery = ref('');

const filteredMdas = computed(() => {
  if (!searchQuery.value) return mdas.value;
  const q = searchQuery.value.toLowerCase();
  return mdas.value.filter(m => 
    m.name.toLowerCase().includes(q) || 
    (m.code && m.code.toLowerCase().includes(q)) ||
    (m.description && m.description.toLowerCase().includes(q))
  );
});

const showModal = ref(false);
const form = ref({
  id: null,
  name: '',
  code: '',
  description: '',
  head_of_mda: '',
  contact_email: '',
  contact_phone: '',
  website: '',
  address: '',
});

onMounted(() => {
  mdaStore.fetchMdas();
});

const openCreateModal = () => {
  form.value = {
    id: null,
    name: '',
    code: '',
    description: '',
    head_of_mda: '',
    contact_email: '',
    contact_phone: '',
    website: '',
    address: '',
  };
  showModal.value = true;
};

const openEditModal = (mda) => {
  form.value = { ...mda };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleSubmit = async () => {
  if (form.value.id) {
    await mdaStore.updateMda(form.value);
  } else {
    await mdaStore.createMda(form.value);
  }
  closeModal();
};

const deleteMda = async (id) => {
  if (confirm('Are you sure you want to delete this MDA? This action cannot be undone.')) {
    await mdaStore.deleteMda(id);
  }
};
</script>
