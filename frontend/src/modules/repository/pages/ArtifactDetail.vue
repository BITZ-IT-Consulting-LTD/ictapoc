<template>
  <div class="page__wrapper">
    <div class="u-mb-6 u-flex u-items-center u-gap-3">
      <router-link to="/repository/artifacts" class="button button--secondary button--tiny button--pill flex items-center gap-2 border-slate-200">
        <i class="bi bi-arrow-left"></i> Registry Index
      </router-link>
      <div class="u-h-6 u-w-px u-bg-slate-300"></div>
      <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Digital Asset View</span>
    </div>

    <!-- Loading State -->
    <div v-if="artifactStore.loading && !artifactStore.selectedArtifact" class="u-p-20 u-flex u-flex-col u-items-center">
      <div class="animate-spin u-h-12 u-w-12 u-border-4 u-border-primary u-border-t-transparent u-rounded-full mb-4"></div>
      <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">Decrypting Asset Metadata...</p>
    </div>

    <template v-else-if="artifactStore.selectedArtifact">
      <!-- Top Level Metadata -->
      <ArtifactMetadata :artifact="artifactStore.selectedArtifact" class="u-mb-8" />
      
      <!-- Primary Workspace -->
      <div class="u-grid u-grid-cols-1 lg:u-grid-cols-3 u-gap-8">
        
        <!-- Left Column: Document List -->
        <div class="lg:u-col-span-2 u-flex u-flex-col u-gap-8">
          <DocumentList 
            :documents="artifactStore.documents" 
            @preview="openPreview" 
          />
        </div>
        
        <!-- Right Column: Context & Actions -->
        <div class="u-flex u-flex-col u-gap-8">
          <!-- Action Panel (Upload) -->
          <DocumentUpload 
            v-if="canUpload" 
            :artifactId="artifactStore.selectedArtifact.id" 
            :metadataSchema="artifactStore.selectedArtifact.artifact_type?.metadata_schema"
            @uploaded="handleUploadSuccess" 
          />
          
          <!-- Quick Status Actions for Supervisors -->
          <div class="card overflow-hidden border-0 shadow-lg rounded-2xl u-bg-white" v-if="canManageStatus">
            <div class="u-p-6 u-border-b u-border-slate-100">
              <h3 class="u-text-xs u-font-black u-text-main u-uppercase u-tracking-widest">
                <i class="bi bi-shield-lock u-text-warning u-mr-2"></i> Executive Controls
              </h3>
            </div>
            <div class="u-p-6 flex flex-col gap-3">
               <button @click="updateStatus('reviewed')" class="button button--secondary button--sm button--pill u-w-full u-justify-between" :disabled="currentStatus === 'reviewed'">
                 Mark as Reviewed <i class="bi bi-check2-circle text-warning"></i>
               </button>
               <button @click="updateStatus('validated')" class="button button--secondary button--sm button--pill u-w-full u-justify-between" :disabled="currentStatus === 'validated'">
                 Validate Artifact <i class="bi bi-patch-check text-primary"></i>
               </button>
               <button @click="updateStatus('final')" class="button button--primary button--sm button--pill u-w-full u-justify-between" :disabled="currentStatus === 'final'">
                 Publish Final <i class="bi bi-bookmark-star"></i>
               </button>
            </div>
          </div>
        </div>
      </div>
    </template>
    <div v-else class="u-p-20 u-text-center u-text-muted u-font-bold u-uppercase u-tracking-widest u-text-[10px]">
       Asset Not Found in Registry.
    </div>

    <!-- Preview Modal globally managed -->
    <DocumentPreview 
      v-model="previewModalOpen" 
      :document="previewingDocument" 
      @close="previewingDocument = null" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useArtifactStore } from '../stores/artifactStore';
import { useAuthStore } from '@/store/auth';

import ArtifactMetadata from '../components/ArtifactMetadata.vue';
import DocumentList from '../components/DocumentList.vue';
import DocumentUpload from '../components/DocumentUpload.vue';
import DocumentPreview from '../components/DocumentPreview.vue';
import repositoryApi from '../services/repositoryApi';

const route = useRoute();
const artifactStore = useArtifactStore();
const authStore = useAuthStore();

const previewModalOpen = ref(false);
const previewingDocument = ref(null);

const userRole = computed(() => authStore.user?.role || 'citizen');

const canUpload = computed(() => {
  return userRole.value !== 'citizen';
});

const canManageStatus = computed(() => {
  return ['system_admin', 'supervisor', 'admin', 'mda_admin'].includes(userRole.value);
});

const currentStatus = computed(() => artifactStore.selectedArtifact?.status);

const openPreview = (doc) => {
  previewingDocument.value = doc;
  previewModalOpen.value = true;
};

const handleUploadSuccess = () => {
  // Re-fetch details to sync versions correctly (store does optimistic append but re-fetch is safer for timeline)
  artifactStore.fetchArtifactDetails(route.params.id);
};

const updateStatus = async (status) => {
  try {
    await repositoryApi.updateArtifactStatus(route.params.id, status);
    // Refresh to get new metadata
    artifactStore.fetchArtifactDetails(route.params.id);
    alert(`Artifact status updated to ${status}.`);
  } catch(err) {
    alert("Unauthorized to alter registry status.");
  }
};

onMounted(() => {
  const id = route.params.id;
  if(id) {
     artifactStore.fetchArtifactDetails(id);
  }
});
</script>
