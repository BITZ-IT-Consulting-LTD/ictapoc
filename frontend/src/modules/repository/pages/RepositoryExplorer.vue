<template>
  <div class="page__wrapper">
    <!-- Breadcrumbs / Path Indicator -->
    <div class="u-mb-6 u-flex u-items-center u-gap-3 u-bg-white u-p-4 u-rounded-2xl shadow-sm border border-slate-100">
      <router-link to="/repository/artifacts" class="u-text-primary u-font-bold u-text-xs uppercase tracking-widest flex items-center gap-2">
        <i class="bi bi-hdd-rack"></i> Root
      </router-link>
      <span class="u-text-slate-300">/</span>
      <div class="u-flex u-items-center u-gap-2 overflow-x-auto u-no-scrollbar">
        <template v-for="(part, index) in pathParts" :key="index">
          <span v-if="index > 0" class="u-text-slate-300">/</span>
          <button @click="navigateToPart(index)" class="u-text-xs u-font-black u-text-main u-uppercase u-tracking-widest whitespace-nowrap hover:u-text-primary transition-colors">
            {{ part }}
          </button>
        </template>
      </div>
    </div>

    <!-- Global Toolbar / Filters -->
    <div class="toolbar u-p-3 u-bg-white u-rounded-3xl shadow-lg border-0 u-mb-8">
      <div class="u-flex u-flex-wrap u-items-center u-justify-between u-gap-6">
        <!-- Search -->
        <div class="toolbar__filter-group u-bg-slate-50 u-flex-1 min-w-[300px]">
           <i class="bi bi-search toolbar__filter-icon"></i>
           <input 
             type="text" 
             v-model="filters.search" 
             class="toolbar__filter-input" 
             placeholder="Search within this branch..."
             @input="debounceSearch"
           >
        </div>

        <!-- Right Side: Views -->
        <div class="u-flex u-items-center u-gap-2">
           <div class="u-text-[9px] u-font-black u-text-muted u-uppercase u-mr-4">Branch Explorer</div>
           <button class="button button--ghost button--tiny u-p-2 rounded-xl border border-slate-100 u-bg-slate-50">
             <i class="bi bi-list-task"></i>
           </button>
        </div>
      </div>
    </div>
    <div v-if="loading" class="u-p-20 u-flex u-flex-col u-items-center">
      <div class="animate-spin u-h-12 u-w-12 u-border-4 u-border-primary u-border-t-transparent u-rounded-full mb-4"></div>
      <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">Traversing Hierarchy...</p>
    </div>

    <div v-else-if="currentData" class="u-grid u-grid-cols-1 lg:u-grid-cols-4 u-gap-8">
      
      <!-- Left: Folder Tree / Sub-folders -->
      <div class="lg:u-col-span-1 u-flex u-flex-col u-gap-6">
        <div class="card u-p-6 u-bg-white rounded-3xl shadow-xl border-0">
          <h3 class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-6 flex items-center justify-between">
            Sub-Folders
            <span class="badge badge--secondary text-[8px]">{{ currentData.nodes.length }}</span>
          </h3>
          
          <div class="u-flex u-flex-col u-gap-2">
            <button 
              v-for="subNode in currentData.nodes" 
              :key="subNode.id"
              @click="navigateTo(subNode.full_path)"
              class="u-flex u-items-center u-gap-3 u-p-3 u-rounded-xl hover:u-bg-slate-50 transition-all u-text-left group"
            >
              <div class="u-w-8 u-h-8 u-bg-primary/10 u-rounded-lg u-flex u-items-center u-justify-center u-text-primary group-hover:u-bg-primary group-hover:u-text-white transition-colors">
                <i class="bi bi-folder2-open"></i>
              </div>
              <div>
                <div class="u-text-xs u-font-black u-text-main group-hover:u-text-primary">{{ subNode.name }}</div>
                <div class="u-text-[9px] u-text-muted u-uppercase u-font-bold">{{ subNode.node_type_name }}</div>
              </div>
            </button>
            <div v-if="currentData.nodes.length === 0" class="u-text-[10px] u-text-center u-text-muted u-py-4 u-font-bold uppercase">
              End of Branch
            </div>
          </div>
        </div>

        <!-- Node Metadata -->
        <div class="card u-p-6 u-bg-slate-900 u-text-white rounded-3xl shadow-xl border-0">
          <h3 class="u-text-[10px] u-font-black u-text-slate-400 u-uppercase u-tracking-widest u-mb-4">Location Info</h3>
          <div class="u-flex u-flex-col u-gap-4">
             <div>
               <div class="u-text-[9px] u-font-bold u-text-slate-500 uppercase">Current Level</div>
               <div class="u-text-sm u-font-black">{{ currentData.node.node_type_name }}</div>
             </div>
             <div v-if="currentData.node.inherited_metadata && Object.keys(currentData.node.inherited_metadata).length > 0">
                <div class="u-text-[9px] u-font-bold u-text-slate-500 uppercase mb-2">Recursive Context</div>
                <div class="u-flex u-flex-col u-gap-2">
                  <div v-for="(v, k) in currentData.node.inherited_metadata" :key="k" class="u-p-2 u-bg-slate-800 u-rounded u-text-[9px] u-font-bold flex justify-between">
                    <span class="u-text-slate-500 uppercase">{{ k }}</span>
                    <span class="u-text-primary">{{ v }}</span>
                  </div>
                </div>
             </div>
          </div>
        </div>
      </div>

      <!-- Right: Artifacts & Records -->
      <div class="lg:u-col-span-3 u-flex u-flex-col u-gap-6">
         <!-- Folder Header -->
         <div class="u-flex u-justify-between u-items-center u-mb-2">
           <div>
             <h2 class="u-text-2xl u-font-black u-text-main u-uppercase u-tracking-tighter">{{ currentData.node.name }}</h2>
             <p class="u-text-xs u-text-muted font-medium">Authoritative records mapped to this location.</p>
           </div>
           <button class="button button--secondary button--tiny button--pill u-px-4">
             <i class="bi bi-share u-mr-2"></i> Share Link
           </button>
         </div>

         <!-- Artifact Table -->
         <ArtifactTable :artifacts="currentData.artifacts" />
      </div>

    </div>

    <div v-else class="u-p-20 u-text-center">
       <i class="bi bi-shield-slash u-text-4xl u-text-danger u-mb-4 block"></i>
       <h3 class="u-text-sm u-font-black u-text-main u-uppercase">Access Denied or Invalid Path</h3>
       <p class="u-text-xs u-text-muted u-mt-2">This hierarchy branch does not exist in the official DRMS registry.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import repositoryApi from '../services/repositoryApi';
import ArtifactTable from '../components/ArtifactTable.vue';

const route = useRoute();
const router = useRouter();

const currentData = ref(null);
const loading = ref(true);
const filters = ref({
  search: ''
});

let searchTimeout = null;
const debounceSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchRepoData();
  }, 400);
};

const currentPath = computed(() => {
  const parts = route.params.path || [];
  return '/' + (Array.isArray(parts) ? parts.join('/') : parts);
});

const pathParts = computed(() => {
  return currentPath.value.split('/').filter(p => p !== '');
});

const fetchRepoData = async () => {
  try {
    loading.value = true;
    const params = {};
    if (filters.value.search) params.search = filters.value.search;
    
    // We update exploration endpoint to handle query params
    const res = await repositoryApi.explorePathWithParams(currentPath.value, params);
    currentData.value = res.data;
  } catch (err) {
    console.error("Path resolution failed", err);
    currentData.value = null;
  } finally {
    loading.value = false;
  }
};

const navigateTo = (path) => {
  // Ensure path doesn't have leading slash for the route param
  const clean = path.startsWith('/') ? path.substring(1) : path;
  router.push(`/repository/explore/${clean}`);
};

const navigateToPart = (index) => {
  const parts = pathParts.value.slice(0, index + 1);
  navigateTo('/' + parts.join('/'));
};

watch(() => route.params.path, () => {
  fetchRepoData();
}, { deep: true });

onMounted(() => {
  fetchRepoData();
});
</script>
