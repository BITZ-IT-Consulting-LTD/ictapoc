<template>
  <div class="page__wrapper">
    <header class="page__header u-mb-8">
      <div class="page__title-group">
        <h1 class="page__title text-premium flex items-center gap-3">
          <i class="bi bi-bank2 u-text-primary"></i>
          Artifact Registry
        </h1>
        <p class="page__subtitle u-mt-2">Authoritative Central Repository for Government Deliverables and Records</p>
      </div>
      
      <div class="page__actions">
        <div class="u-flex u-items-center u-gap-3">
        <router-link v-if="['admin', 'system_admin'].includes(userRole)" to="/repository/configuration" class="button button--secondary button--tiny button--pill u-px-4">
           <i class="bi bi-gear-fill u-mr-2"></i> DRMS Config
        </router-link>
        <router-link to="/repository/explore/project-registry" class="button button--secondary button--tiny button--pill u-px-4">
           <i class="bi bi-diagram-3 u-mr-2"></i> Hierarchical Explorer
        </router-link>
        <button v-if="userRole !== 'citizen'" @click="showNewModal = true" class="button button--primary button--tiny button--pill u-px-4">
          <i class="bi bi-plus-lg u-mr-2"></i> Register Artifact
        </button>
      </div>
      </div>
    </header>

    <!-- Global Toolbar / Filters -->
    <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-p-4 u-bg-white u-mb-8">
      <div class="u-flex u-flex-wrap u-gap-4 u-items-center">
        <!-- Search -->
        <div class="toolbar__filter-group u-bg-slate-50 u-flex-1 u-min-w-[250px]">
          <i class="bi bi-search toolbar__filter-icon"></i>
          <input type="text" v-model="filters.search" placeholder="Search authoritative records..." class="toolbar__filter-input border-0" @input="debouncedFetch">
        </div>
        
        <!-- Type Filter -->
        <div class="toolbar__filter-group u-bg-slate-50 u-w-48">
           <i class="bi bi-tag toolbar__filter-icon"></i>
           <select v-model="filters.artifact_type" class="toolbar__filter-input u-w-full border-0 bg-transparent" @change="handleTypeChange">
             <option value="">All Types</option>
             <option v-for="t in artifactStore.artifactTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
           </select>
        </div>

        <!-- Registry Filter -->
        <div class="toolbar__filter-group u-bg-slate-50 u-w-48">
           <i class="bi bi-hdd-rack toolbar__filter-icon"></i>
           <select v-model="filters.registry" class="toolbar__filter-input u-w-full border-0 bg-transparent" @change="fetchArtifacts">
             <option value="">All Registries</option>
             <option v-for="reg in artifactStore.registries" :key="reg.id" :value="reg.id">{{ reg.name }}</option>
           </select>
        </div>

        <!-- Node/Branch Filter -->
        <div class="toolbar__filter-group u-bg-slate-50 u-w-48">
           <i class="bi bi-diagram-3 toolbar__filter-icon"></i>
           <select v-model="filters.node" class="toolbar__filter-input u-w-full border-0 bg-transparent" @change="fetchArtifacts">
             <option value="">All Branches</option>
             <option v-for="node in filteredNodes" :key="node.id" :value="node.id">{{ node.full_path }}</option>
           </select>
        </div>

        <!-- Status Filter -->
         <div class="toolbar__filter-group u-bg-slate-50 u-w-48">
           <i class="bi bi-flag toolbar__filter-icon"></i>
           <select v-model="filters.status" class="toolbar__filter-input u-w-full border-0 bg-transparent" @change="fetchArtifacts">
             <option value="">All Statuses</option>
             <option value="draft">Draft</option>
             <option value="reviewed">Reviewed</option>
             <option value="validated">Validated</option>
             <option value="final">Final Official</option>
             <option value="archived">Archived</option>
           </select>
        </div>
      </div>
    </div>

    <!-- Active Loader -->
    <div v-if="artifactStore.loading && artifactStore.artifacts.length === 0" class="u-p-20 u-flex u-flex-col u-items-center">
      <div class="animate-spin u-h-12 u-w-12 u-border-4 u-border-primary u-border-t-transparent u-rounded-full mb-4"></div>
      <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">Querying Registry...</p>
    </div>

    <!-- Registry Table Component -->
    <ArtifactTable v-else :artifacts="artifactStore.artifacts" @delete="deleteArtifact" @edit="openEditModal" />
    
    <!-- Meta Summary -->
    <div class="u-mt-6 u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest" v-if="artifactStore.meta.count > 0">
      Displaying records from a total of {{ artifactStore.meta.count }} registry items.
    </div>

    <!-- Add/Edit Artifact Form -->
    <BaseModal v-model:show="showNewModal" :title="isEditing ? 'Edit Artifact' : 'Register New Artifact'" @close="closeModal">
      <div class="u-p-6">
        <form @submit.prevent="handleRegister" class="u-flex u-flex-col u-gap-4">
          <div class="form-group">
            <label class="form-label u-text-xs u-font-black u-uppercase text-muted">Title / Deliverable Name</label>
            <input type="text" v-model="newArtifact.title" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. Master Digitization Framework">
          </div>
          <div class="form-group">
            <label class="form-label u-text-xs u-font-black u-uppercase text-muted">Artifact Classification (Type)</label>
            <select v-model="newArtifact.artifact_type" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1 bg-white" required>
              <option value="" disabled>Select System Classification...</option>
              <option v-for="t in artifactStore.artifactTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label u-text-xs u-font-black u-uppercase text-muted">Project Phase (Optional)</label>
            <select v-model="newArtifact.phase" class="form-input w-full p-3 rounded-xl border border-slate-100 mt-1 bg-white">
              <option value="">No Phase / General</option>
              <option v-for="phase in artifactStore.phases" :key="phase.id" :value="phase.id">{{ phase.name }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label u-text-xs u-font-black u-uppercase text-muted">Submission Deadline</label>
            <input type="date" v-model="newArtifact.submission_deadline" class="form-input w-full p-3 rounded-xl border border-slate-100 mt-1 bg-white">
          </div>

          <div class="form-group">
            <label class="form-label u-text-xs u-font-black u-uppercase text-muted">Hierarchical Location (Node)</label>
            <select v-model="newArtifact.node" class="form-input w-full p-3 rounded-xl border border-slate-100 mt-1 bg-white" required>
              <option value="" disabled>Select Registry Path...</option>
              <option v-for="node in artifactStore.nodes" :key="node.id" :value="node.id">{{ node.full_path }} ({{ node.node_type_name }})</option>
            </select>
            <p class="u-text-[9px] u-text-primary u-font-bold u-mt-1 uppercase tracking-widest">* Required for authoritative compliance</p>
          </div>

          <div class="form-group u-flex u-items-center u-gap-3 u-mt-2">
            <input type="checkbox" id="is_public" v-model="newArtifact.is_public" class="w-5 h-5 rounded border-slate-300 text-primary focus:ring-primary">
            <label for="is_public" class="u-text-sm u-font-bold u-text-main">Make Publicly Available</label>
            <p class="u-text-[9px] u-text-muted u-mt-1 w-full basis-full">If checked, approved documents will be visible on the public portal.</p>
          </div>
          
          <div class="u-flex u-justify-end u-gap-3 u-mt-4">
            <button type="button" @click="showNewModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill" :disabled="isRegistering">
              <span v-if="isRegistering" class="animate-pulse">Registering...</span>
              <span v-else>Confirm Registration</span>
            </button>
          </div>
        </form>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useArtifactStore } from '../stores/artifactStore';
import { useAuthStore } from '@/store/auth';
import ArtifactTable from '../components/ArtifactTable.vue';
import BaseModal from '@/components/Common/BaseModal.vue';

const artifactStore = useArtifactStore();
const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

const userRole = computed(() => authStore.user?.role || 'citizen');

const filteredNodes = computed(() => {
  if (!filters.value.registry) return artifactStore.nodes;
  return artifactStore.nodes.filter(n => n.registry === filters.value.registry);
});

const showNewModal = ref(false);
const isRegistering = ref(false);
const isEditing = ref(false);
const editingId = ref(null);

const defaultArtifact = {
  title: '',
  artifact_type: '',
  phase: '',
  node: '',
  is_public: false,
  submission_deadline: ''
};

const newArtifact = ref({ ...defaultArtifact });

const closeModal = () => {
  showNewModal.value = false;
  isEditing.value = false;
  editingId.value = null;
  newArtifact.value = { ...defaultArtifact };
};

const openEditModal = (artifact) => {
  isEditing.value = true;
  editingId.value = artifact.id;
  newArtifact.value = {
    title: artifact.title,
    artifact_type: artifact.artifact_type?.id || '',
    phase: artifact.phase?.id || '',
    node: artifact.node?.id || '',
    is_public: artifact.is_public || false,
    submission_deadline: artifact.submission_deadline || ''
  };
  showNewModal.value = true;
};

const handleRegister = async () => {
  try {
    isRegistering.value = true;
    if (isEditing.value) {
      await artifactStore.updateArtifact(editingId.value, newArtifact.value);
    } else {
      await artifactStore.registerArtifact(newArtifact.value);
    }
    closeModal();
    fetchArtifacts();
  } catch (err) {
    alert(artifactStore.error || "Failed to save artifact");
  } finally {
    isRegistering.value = false;
  }
};

const filters = ref({
  search: '',
  registry: '',
  node: '',
  artifact_type: '',
  status: ''
});

let debounceTimeout = null;

const debouncedFetch = () => {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    fetchArtifacts();
  }, 500);
};

const fetchArtifacts = async () => {
  const query = {};
  if (filters.value.search) query.search = filters.value.search;
  if (filters.value.registry) query.registry = filters.value.registry;
  if (filters.value.node) query.node = filters.value.node;
  if (filters.value.artifact_type) query.artifact_type = filters.value.artifact_type;
  if (filters.value.status) query.status = filters.value.status;
  
  await artifactStore.fetchArtifacts(query);
};

const handleTypeChange = () => {
  if (filters.value.artifact_type) {
    router.push({ name: 'ArtifactRegistryCategory', params: { typeId: filters.value.artifact_type } });
  } else {
    router.push({ name: 'ArtifactRegistry' });
  }
};

// Handle category changes via route
watch(() => route.params.typeId, (newId) => {
  filters.value.artifact_type = newId || '';
  fetchArtifacts();
}, { immediate: true });

const deleteArtifact = async (id) => {
  if(confirm("Are you sure you want to delete this artifact?")) {
      try {
          await artifactStore.deleteArtifact(id);
          fetchArtifacts();
      } catch(err) {
          alert("Failed to delete. It might be in use.");
      }
  }
};

onMounted(() => {
  artifactStore.fetchRegistries();
  artifactStore.fetchArtifactTypes();
  artifactStore.fetchNodes();
  artifactStore.fetchPhases();
  // fetchArtifacts is now handled by the watch immediate
});
</script>
