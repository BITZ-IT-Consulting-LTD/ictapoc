<template>
  <div class="page__wrapper">
    <!-- Header -->
    <header class="page__header u-mb-8">
      <div class="page__title-group">
        <h1 class="page__title text-premium flex items-center gap-3">
          <i class="bi bi-bank2 u-text-primary"></i>
          DRMS Portal
        </h1>
        <p class="page__subtitle u-mt-2">Authoritative Central Public Repository for Government Deliverables and Records</p>
      </div>
    </header>

    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Sidebar -->
      <aside class="lg:w-80 flex-shrink-0 flex flex-col gap-6">
        <!-- Registries Tree -->
        <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6">
          <h3 class="text-xs font-black text-slate-400 uppercase tracking-[0.2em] mb-4">Hierarchical Browser</h3>
          <ul class="space-y-2">
            <li v-for="reg in registries" :key="reg.id">
              <div class="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 cursor-pointer transition-all border-l-2" 
                   :class="activeRegistry === reg.id ? 'border-primary bg-indigo-50/50' : 'border-transparent'" 
                   @click="toggleRegistry(reg.id)">
                <div class="flex items-center gap-3">
                  <span class="text-xl">🏢</span>
                  <span class="text-sm font-bold text-slate-700">{{ reg.name }}</span>
                </div>
                <span class="bg-white text-primary text-[9px] px-2 py-1 rounded font-black uppercase tracking-widest border border-slate-100 shadow-sm">🏛️ {{ reg.mda_owner?.code || 'GOK' }}</span>
              </div>
              <!-- Nodes Tree -->
              <ul v-if="activeRegistry === reg.id" class="ml-6 mt-2 pl-2 border-l-2 border-slate-100 space-y-1">
                <li v-for="node in getNodesForRegistry(reg.id)" :key="node.id" 
                    class="p-2 flex items-center justify-between cursor-pointer text-sm rounded-lg hover:bg-slate-50 transition-colors" 
                    :class="filters.node === node.id ? 'text-primary font-bold bg-indigo-50/50' : 'text-slate-500 font-medium'" 
                    @click="selectNode(node.id)">
                  <div class="flex items-center gap-2 truncate pr-2">
                    <span class="text-lg">{{ getNodeIcon(node.node_type_name) }}</span>
                    <span class="truncate">{{ node.name }}</span>
                  </div>
                </li>
                <li v-if="getNodesForRegistry(reg.id).length === 0" class="p-2 text-xs text-slate-400 italic">
                   No visible nodes
                </li>
              </ul>
            </li>
          </ul>
        </div>
        
        <!-- Document Categories (Artifact Types) -->
        <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6">
           <h3 class="text-xs font-black text-slate-400 uppercase tracking-[0.2em] mb-4">Schema Categories</h3>
           <ul class="space-y-1">
             <li v-for="type in artifactTypes" :key="type.id" 
                 class="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 cursor-pointer transition-colors border-l-2" 
                 :class="filters.artifact_type === type.id ? 'border-primary bg-indigo-50/50 text-primary font-bold' : 'border-transparent text-slate-600 font-medium'" 
                 @click="toggleType(type.id)">
                <div class="flex items-center gap-3 text-sm">
                  <span class="text-lg">📦</span>
                  <span class="truncate">{{ type.name }}</span>
                </div>
                <span class="text-primary text-[9px] font-mono bg-indigo-50 px-1.5 py-0.5 rounded ml-2 shrink-0">Schema ✓</span>
             </li>
           </ul>
        </div>
        
        <!-- Classifications -->
        <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6">
           <h3 class="text-xs font-black text-slate-400 uppercase tracking-[0.2em] mb-4">Classifications</h3>
           <div class="flex flex-wrap gap-2">
             <button class="px-3 py-1.5 rounded-xl text-[10px] uppercase font-black tracking-wider flex items-center gap-2 border border-slate-200 text-slate-500 hover:border-emerald-500 hover:text-emerald-600 hover:bg-emerald-50 transition-colors bg-white shadow-sm">
               <div class="w-2 h-2 rounded-full bg-emerald-500"></div> Public
             </button>
             <button class="px-3 py-1.5 rounded-xl text-[10px] uppercase font-black tracking-wider flex items-center gap-2 border border-slate-200 text-slate-500 hover:border-amber-500 hover:text-amber-600 hover:bg-amber-50 transition-colors bg-white shadow-sm">
               <div class="w-2 h-2 rounded-full bg-amber-500"></div> Internal
             </button>
           </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 min-w-0 flex flex-col">
        <!-- Advanced Search and Breadcrumbs -->
        <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-4 mb-6">
          <div class="flex flex-col gap-4">
             <!-- Advanced Search -->
             <div class="toolbar__filter-group bg-slate-50 flex-1 w-full rounded-2xl relative">
                <i class="bi bi-search toolbar__filter-icon text-lg absolute left-4 top-1/2 -translate-y-1/2"></i>
                <input type="text" v-model="filters.search" @input="debouncedFetch" placeholder="Search across schemas, metadata, artifacts, and paths..." class="w-full bg-transparent border-0 text-slate-700 py-4 pl-12 pr-16 focus:outline-none focus:ring-0 text-sm font-medium placeholder-slate-400">
                <div class="absolute right-4 top-1/2 -translate-y-1/2 flex items-center">
                  <span class="bg-white text-slate-400 text-[10px] px-2 py-1 rounded font-mono border border-slate-200 flex items-center gap-1 shadow-sm">
                     <i class="bi bi-command"></i> K
                  </span>
                </div>
             </div>
             
             <!-- Hierarchical Breadcrumb -->
             <div class="flex items-center gap-2 text-xs text-slate-500 overflow-x-auto whitespace-nowrap px-2">
                <span class="hover:text-primary cursor-pointer font-bold flex items-center gap-2" @click="clearFilters">
                   <i class="bi bi-diagram-3"></i> Repository Root
                </span>
                <template v-if="filters.registry">
                  <i class="bi bi-chevron-right text-[10px] opacity-50"></i>
                  <span class="text-slate-800 font-bold flex items-center gap-1">🏢 {{ getRegistryName(filters.registry) }}</span>
                </template>
                <template v-if="filters.node">
                  <i class="bi bi-chevron-right text-[10px] opacity-50"></i>
                  <span class="text-primary font-bold flex items-center gap-1 border-b border-primary border-dashed pb-0.5">📁 {{ getNodeName(filters.node) }}</span>
                </template>
             </div>
          </div>
        </div>

        <!-- Bulk Operations Toolbar -->
        <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-2xl mb-6 flex flex-wrap justify-between items-center shadow-sm">
           <div class="flex items-center gap-4">
             <div class="flex items-center gap-3 pl-2">
               <input type="checkbox" :checked="selectedArtifacts.length === artifacts.length && artifacts.length > 0" @change="toggleSelectAll" class="rounded w-4 h-4 text-primary focus:ring-primary border-slate-300">
               <span class="text-xs font-black text-slate-700 tracking-wide uppercase">{{ selectedArtifacts.length }} Selected</span>
             </div>
             <div class="h-5 w-px bg-slate-300"></div>
             <span class="text-slate-500 text-xs font-mono font-bold">{{ meta.count }} Found</span>
           </div>
           <div class="flex gap-2 mt-2 sm:mt-0">
             <button class="bg-white hover:bg-slate-100 border border-slate-200 text-slate-600 px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-2 shadow-sm">
               <i class="bi bi-arrow-left-right text-slate-400"></i> Compare
             </button>
             <button class="bg-white hover:bg-slate-100 border border-slate-200 text-slate-600 px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-2 shadow-sm">
               <i class="bi bi-filetype-csv text-emerald-500"></i> Export Meta
             </button>
             <button class="button button--primary button--tiny button--pill px-4 py-1.5 flex items-center gap-2">
               <i class="bi bi-cloud-arrow-down-fill"></i> Batch ZIP
             </button>
           </div>
        </div>

        <!-- Active Loader -->
        <div v-if="loading && artifacts.length === 0" class="flex-1 flex flex-col items-center justify-center min-h-[300px]">
          <div class="animate-spin h-10 w-10 border-4 border-primary border-t-transparent rounded-full mb-4"></div>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.3em]">Querying DRMS Schema...</p>
        </div>

        <!-- Artifact Cards List -->
        <div v-else class="flex-1 space-y-4 pb-10">
          <div v-for="artifact in artifacts" :key="artifact.id" class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 relative group transition-all hover:shadow-xl hover:border-primary/30 border border-transparent">
             <!-- Highlight Accent -->
             <div class="absolute top-0 left-0 w-1.5 h-full bg-primary opacity-0 group-hover:opacity-100 transition-opacity"></div>
             
             <div class="flex flex-col sm:flex-row items-start justify-between gap-6">
                <div class="flex gap-4 items-start w-full">
                   <div class="mt-1">
                      <input type="checkbox" :value="artifact.id" v-model="selectedArtifacts" class="rounded w-4 h-4 text-primary focus:ring-primary border-slate-300">
                   </div>
                   <div class="flex-1 min-w-0">
                      <div class="flex flex-wrap items-center gap-2 mb-3">
                         <span class="bg-slate-100 border border-slate-200 text-slate-500 text-[9px] px-2 py-0.5 rounded font-mono uppercase font-bold">ID-{{ artifact.id }}</span>
                         <span class="bg-emerald-50 border border-emerald-100 text-emerald-600 text-[9px] px-2 py-0.5 rounded uppercase font-black tracking-wider flex items-center gap-1 shadow-sm">
                           <div class="w-1.5 h-1.5 rounded-full bg-emerald-500"></div> {{ artifact.status }}
                         </span>
                         <span v-if="artifact.latest_version" class="text-primary text-[10px] font-black font-mono bg-indigo-50 border border-indigo-100 px-1.5 py-0.5 rounded flex items-center gap-1">
                           <i class="bi bi-clock-history"></i> v{{ artifact.latest_version }}
                         </span>
                         <!-- Project Context Badge inline -->
                         <span v-if="artifact.phase" class="bg-amber-50 border border-amber-100 text-amber-600 text-[9px] px-2 py-0.5 rounded uppercase font-black tracking-wider flex items-center gap-1 ml-auto shadow-sm">
                            📊 Phase {{ artifact.phase.sequence }}
                         </span>
                      </div>
                      
                      <h2 class="text-xl font-black text-slate-800 mb-4 group-hover:text-primary transition-colors flex items-center gap-3 truncate" :title="artifact.title">
                         📦 {{ artifact.title }}
                      </h2>
                      
                      <!-- Metadata Grid -->
                      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-100">
                         <div class="flex flex-col gap-1 overflow-hidden">
                           <span class="text-slate-400 text-[9px] font-black uppercase tracking-widest flex items-center gap-1.5"><i class="bi bi-bank2 text-primary"></i> MDA</span>
                           <span class="text-slate-700 font-bold text-xs truncate">{{ artifact.mda_owner?.name || 'GOK Central' }}</span>
                         </div>
                         <div class="flex flex-col gap-1 overflow-hidden">
                           <span class="text-slate-400 text-[9px] font-black uppercase tracking-widest flex items-center gap-1.5"><i class="bi bi-diagram-3 text-primary"></i> Location</span>
                           <span class="text-slate-700 font-bold text-xs truncate" :title="artifact.node?.full_path">{{ artifact.node?.full_path || 'Unmapped' }}</span>
                         </div>
                         <div class="flex flex-col gap-1 overflow-hidden">
                           <span class="text-slate-400 text-[9px] font-black uppercase tracking-widest flex items-center gap-1.5"><i class="bi bi-box-seam text-primary"></i> Category</span>
                           <span class="text-slate-700 font-bold text-xs truncate">{{ artifact.artifact_type?.name || 'General' }}</span>
                         </div>
                         <div class="flex flex-col gap-1 overflow-hidden">
                           <span class="text-slate-400 text-[9px] font-black uppercase tracking-widest flex items-center gap-1.5"><i class="bi bi-calendar-event text-primary"></i> Updated</span>
                           <span class="text-slate-700 font-bold text-xs">{{ new Date(artifact.updated_at).toLocaleDateString() }}</span>
                         </div>
                      </div>
                   </div>
                </div>
                
                <div class="shrink-0 sm:mt-8 w-full sm:w-auto">
                  <router-link :to="`/public-repository/${artifact.id}`" class="button button--secondary button--pill w-full sm:w-auto justify-center flex items-center gap-2">
                    View Assets <i class="bi bi-arrow-right"></i>
                  </router-link>
                </div>
             </div>
             
             <!-- Metadata Preview Panel (Always visible for rich schema feel) -->
             <div v-if="Object.keys(artifact.metadata || {}).length > 0" class="pt-4 mt-4 border-t border-slate-100 border-dashed">
                <div class="flex items-center gap-2 mb-2">
                   <i class="bi bi-code-square text-primary text-xs"></i>
                   <span class="text-slate-500 font-black text-[9px] uppercase tracking-widest">Schema Metadata</span>
                </div>
                <div class="flex flex-wrap gap-2">
                   <span v-for="(val, key) in artifact.metadata" :key="key" class="bg-white border border-slate-200 text-slate-700 px-2.5 py-1 rounded-lg text-[10px] font-mono shadow-sm font-medium">
                      <span class="text-primary font-bold mr-1">{{ key }}:</span> {{ val }}
                   </span>
                </div>
             </div>
             
             <!-- Tag visualization -->
             <div v-if="artifact.tags && artifact.tags.length > 0" class="flex flex-wrap gap-2 mt-4 pt-4 border-t border-slate-100">
                <span v-for="tag in artifact.tags" :key="tag" class="text-[10px] font-bold text-slate-500 hover:text-primary cursor-pointer flex items-center gap-1 bg-slate-50 px-2 py-0.5 rounded-md border border-slate-100">
                   <span class="text-slate-300">#</span>{{ tag }}
                </span>
             </div>
          </div>
          
          <div v-if="artifacts.length === 0" class="flex flex-col items-center justify-center min-h-[300px] border-2 border-dashed border-slate-200 rounded-3xl p-10 bg-slate-50 shadow-inner">
             <span class="text-5xl mb-4 text-primary opacity-50">🔍</span>
             <h3 class="text-slate-800 font-black mb-2 text-lg">No Schema Matches</h3>
             <p class="text-slate-500 text-sm text-center max-w-md font-medium">Adjust your hierarchical filters or search query to find documents within the repository tree.</p>
             <button @click="clearFilters" class="mt-6 button button--secondary button--tiny button--pill">Clear All Filters</button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePublicArtifactStore } from '../stores/publicArtifactStore';

const store = usePublicArtifactStore();
const route = useRoute();
const router = useRouter();

const artifacts = computed(() => store.artifacts);
const meta = computed(() => store.meta);
const registries = computed(() => store.registries);
const nodes = computed(() => store.nodes);
const artifactTypes = computed(() => store.artifactTypes);
const loading = computed(() => store.loading);

const filters = ref({
  search: '',
  registry: '',
  node: '',
  artifact_type: ''
});

const selectedArtifacts = ref([]);
const activeRegistry = ref(null);

let debounceTimeout = null;

const debouncedFetch = () => {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    fetchArtifacts();
  }, 500);
};

const fetchArtifacts = () => {
  const query = {};
  if (filters.value.search) query.search = filters.value.search;
  if (filters.value.registry) query.registry = filters.value.registry;
  if (filters.value.node) query.node = filters.value.node;
  if (filters.value.artifact_type) query.artifact_type = filters.value.artifact_type;
  store.fetchArtifacts(query);
};

// Selection Logic
const toggleSelectAll = (e) => {
  if (e.target.checked) {
    selectedArtifacts.value = artifacts.value.map(a => a.id);
  } else {
    selectedArtifacts.value = [];
  }
};

// Hierarchy Navigation
const toggleRegistry = (id) => {
  if (activeRegistry.value === id) {
    activeRegistry.value = null;
    filters.value.registry = '';
    filters.value.node = '';
  } else {
    activeRegistry.value = id;
    filters.value.registry = id;
    filters.value.node = ''; // reset node when switching registry
  }
  fetchArtifacts();
};

const selectNode = (id) => {
  filters.value.node = filters.value.node === id ? '' : id;
  fetchArtifacts();
};

const toggleType = (id) => {
  if (filters.value.artifact_type === id) {
    router.push({ name: 'PublicRepositoryPortal' });
  } else {
    router.push({ name: 'PublicRepositoryCategory', params: { typeId: id } });
  }
};

const clearFilters = () => {
  filters.value = { search: '', registry: '', node: '', artifact_type: '' };
  activeRegistry.value = null;
  router.push({ name: 'PublicRepositoryPortal' });
};

// Sync route to filters
watch(() => route.params.typeId, (newId) => {
  filters.value.artifact_type = newId || '';
  fetchArtifacts();
}, { immediate: true });

const getNodesForRegistry = (id) => {
  return nodes.value.filter(n => n.registry === id);
};

const getNodeIcon = (typeName) => {
  const map = {
    'Project': '📊',
    'Phase': '⏳',
    'County': '🗺️',
    'Plot': '📍'
  };
  return map[typeName] || '📁';
};

const getRegistryName = (id) => registries.value.find(r => r.id === id)?.name || id;
const getNodeName = (id) => nodes.value.find(n => n.id === id)?.name || id;

onMounted(() => {
  store.fetchRegistries();
  store.fetchArtifactTypes();
  store.fetchNodes();
  // fetchArtifacts is now handled by the watch immediate
});
</script>