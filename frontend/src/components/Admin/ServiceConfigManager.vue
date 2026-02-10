<template>
  <div class="bg-white p-6 rounded-lg shadow mt-8">
    <h3 class="text-xl font-semibold mb-4">Manage Service Configurations</h3>

    <!-- Actions -->
    <div class="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex flex-1 gap-4">
        <div class="relative max-w-sm flex-1">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Filter by name/code..." 
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
        </div>
        <select v-model="mdaFilter" class="block w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          <option value="">All MDAs</option>
          <option v-for="mda in mdas" :key="mda.id" :value="mda.id">{{ mda.name }}</option>
        </select>
      </div>
      <button 
        @click="openCreateModal" 
        class="flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <span class="mr-2">+</span> Create New Service
      </button>
    </div>

    <!-- Service Config List -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left">Service Code</th>
            <th class="px-6 py-3 text-left">Service Name</th>
            <th class="px-6 py-3 text-left">MDA</th>
            <th class="px-6 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="service in filteredServices" :key="service.id">
            <td class="px-6 py-4">{{ service.service_code }}</td>
            <td class="px-6 py-4">{{ service.service_name }}</td>
            <td class="px-6 py-4">{{ getMdaName(service.mda) }}</td>
            <td class="px-6 py-4 text-right">
              <button @click="openEditModal(service)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
              <button @click="deleteService(service.id)" class="ml-4 text-red-600 hover:text-red-900">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Service Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
      <div class="relative mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg leading-6 font-medium text-gray-900 text-center">{{ editForm.id ? 'Edit Service' : 'Create New Service' }}</h3>
          <form @submit.prevent="handleUpdate" class="mt-2 text-left max-h-[80vh] overflow-y-auto">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-4">
              <div>
                <label class="block text-sm">Service Name</label>
                <input type="text" v-model="editForm.service_name" class="mt-1 block w-full" required>
              </div>
              <div>
                <label class="block text-sm">Service Code</label>
                <input type="text" v-model="editForm.service_code" class="mt-1 block w-full" required>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm">MDA</label>
                <div class="mt-1 space-y-1">
                  <input 
                    type="text" 
                    v-model="mdaDropdownSearch" 
                    placeholder="Search Agencies..." 
                    class="block w-full px-2 py-1 text-xs border border-gray-200 rounded focus:ring-indigo-500 focus:border-indigo-500"
                  >
                  <select v-model="editForm.mda" class="block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" required>
                    <option v-for="mda in filteredMdasForDropdown" :key="mda.id" :value="mda.id">{{ mda.name }}</option>
                  </select>
                </div>
              </div>
            </div>
            
            <FormSchemaBuilder v-model="editForm.config" />
            <WorkflowStepManager v-if="editForm.id" :service-config-id="editForm.id" />
            <div v-else class="mt-8 p-4 bg-yellow-50 text-yellow-800 rounded-md border border-yellow-200">
              <p class="text-sm font-medium">Please save the service details first before configuring workflow steps.</p>
            </div>

            <div class="items-center px-4 py-3 sticky bottom-0 bg-white border-t">
              <button type="button" @click="closeModal" class="mr-2 px-4 py-2 bg-gray-200 rounded-md">Close</button>
              <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useServiceConfigStore } from '../../store/serviceConfig';
import { useMdaStore } from '../../store/mda';
import WorkflowStepManager from './WorkflowStepManager.vue';
import FormSchemaBuilder from './FormSchemaBuilder.vue';

const serviceConfigStore = useServiceConfigStore();
const mdaStore = useMdaStore();

const services = computed(() => serviceConfigStore.services);
const mdas = computed(() => mdaStore.mdas);
const searchQuery = ref('');
const mdaFilter = ref('');

const filteredServices = computed(() => {
  let result = services.value;

  if (mdaFilter.value) {
    result = result.filter(s => s.mda === Number(mdaFilter.value));
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(s => 
      s.service_name.toLowerCase().includes(q) || 
      s.service_code.toLowerCase().includes(q)
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
const editForm = ref({
  id: null,
  service_code: '',
  service_name: '',
  mda: null,
  config: { rules: { schema: { properties: {}, required: [] } } },
});

onMounted(() => {
  serviceConfigStore.fetchServices();
  mdaStore.fetchMdas();
});

const getMdaName = (mdaId) => {
  const mda = mdas.value.find(m => m.id === mdaId);
  if (!mda) return 'N/A';
  return mda.code ? `${mda.name} (${mda.code})` : mda.name;
};

const handleUpdate = async () => {
  if (editForm.value.id) {
    await serviceConfigStore.updateService(editForm.value);
  } else {
    try {
      await serviceConfigStore.createService(editForm.value);
    } catch (e) {
      alert('Failed to create service. Ensure Service Code is unique.');
      return; 
    }
  }
  closeModal();
};

const openCreateModal = () => {
  editForm.value = {
    id: null,
    service_code: '',
    service_name: '',
    mda: mdas.value.length > 0 ? mdas.value[0].id : null,
    config: { rules: { schema: { properties: {}, required: [] } } },
  };
  showModal.value = true;
};

const openEditModal = (service) => {
  // Deep copy to avoid reactive mutations outside of the store
  editForm.value = JSON.parse(JSON.stringify(service));
  if (!editForm.value.config) {
    editForm.value.config = { rules: { schema: { properties: {}, required: [] } } };
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const deleteService = async (id) => {
  if (confirm('Are you sure you want to delete this Service Configuration? It will also delete all associated workflow steps.')) {
    await serviceConfigStore.deleteService(id);
  }
};
</script>
