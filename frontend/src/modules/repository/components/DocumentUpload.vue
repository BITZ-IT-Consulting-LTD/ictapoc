<template>
  <div class="card border-2 border-dashed border-slate-300 u-bg-slate-50/50 u-p-6 rounded-2xl">
    <div class="u-flex u-justify-between u-items-center u-mb-6">
      <h3 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">
        <i class="bi bi-cloud-arrow-up u-text-primary u-mr-2"></i> Upload New Document
      </h3>
    </div>

    <!-- Upload Form -->
    <form @submit.prevent="handleUpload" class="u-flex u-flex-col u-gap-6">
      <!-- Drag & Drop Area -->
      <div 
        class="u-w-full u-p-8 u-border-2 u-border-dashed u-rounded-xl u-flex u-flex-col u-items-center u-justify-center u-cursor-pointer transition-all hover:u-bg-primary/5 u-bg-white"
        :class="{'u-border-primary u-bg-primary/5': isDragging, 'u-border-slate-300': !isDragging}"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        @click="$refs.fileInput.click()"
      >
        <input type="file" ref="fileInput" class="hidden" @change="handleFileSelect" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.xls,.xlsx" />
        
        <i class="bi bi-file-earmark-arrow-up u-text-4xl u-text-slate-400 u-mb-4" :class="{'u-text-primary': isDragging || selectedFile}"></i>
        <div class="u-text-sm u-font-black u-text-main" v-if="!selectedFile">Click to browse or drag file here</div>
        <div class="u-text-sm u-font-black u-text-primary" v-else>{{ selectedFile.name }}</div>
        
        <div class="u-text-[10px] u-font-bold u-text-muted u-mt-2 uppercase tracking-widest whitespace-nowrap">
          <span v-if="!selectedFile">Supported: PDF, DOCX, XLSX, JPG, PNG (Max 50MB)</span>
          <span v-else>{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB • Ready for upload</span>
        </div>
      </div>

      <!-- Metadata Fields -->
      <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-4">
        <div>
          <label class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest u-mb-1 block">Document Title</label>
          <input type="text" v-model="formData.title" class="toolbar__filter-input u-w-full u-h-12 border-slate-200" placeholder="E.g., Inception Report Final" required>
        </div>
        
        <div>
          <label class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest u-mb-1 block">Classification</label>
          <select v-model="formData.classification_level" class="toolbar__filter-input u-w-full u-h-12 border-slate-200" required>
            <option value="public">Public - Fully Open</option>
            <option value="internal">Internal - Government Use</option>
            <option value="restricted">Restricted - Need to Know</option>
            <option value="confidential">Confidential - Executive Only</option>
          </select>
        </div>

        <div>
           <label class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest u-mb-1 block">Document Type</label>
           <select v-model="formData.document_type" class="toolbar__filter-input u-w-full u-h-12 border-slate-200" required>
             <option value="report">Report</option>
             <option value="diagram">Process Diagram / Flow</option>
             <option value="evidence">Supporting Evidence</option>
             <option value="memo">Memo / Circular</option>
             <option value="other">Other</option>
           </select>
        </div>
        
        <div>
          <label class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest u-mb-1 block">Version Indicator</label>
          <input type="number" v-model="formData.version_number" class="toolbar__filter-input u-w-full u-h-12 border-slate-200 bg-slate-100" min="1" disabled>
        </div>
      </div>

      <!-- Dynamic Metadata (Business Logic) -->
      <div v-if="Object.keys(renderableMetadata).length > 0" class="u-p-6 u-bg-slate-100/50 u-rounded-xl u-mt-2">
        <h4 class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-4 flex items-center gap-2">
           <i class="bi bi-info-circle"></i> Type-Specific Registry Metadata
        </h4>
        <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-4">
          <div v-for="(field, key) in renderableMetadata" :key="key">
            <label class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest u-mb-1 block">{{ formatLabel(key) }}</label>
            <input 
              v-if="field.type === 'string'" 
              type="text" 
              v-model="metadataValues[key]" 
              class="toolbar__filter-input u-w-full u-h-12 border-slate-200" 
              :placeholder="`Enter ${formatLabel(key)}`"
            >
            <input 
              v-else-if="field.type === 'number'" 
              type="number" 
              v-model="metadataValues[key]" 
              class="toolbar__filter-input u-w-full u-h-12 border-slate-200"
            >
          </div>
        </div>
      </div>

      <div class="u-flex u-justify-end u-mt-4">
        <button type="submit" class="button button--primary button--pill u-px-8" :disabled="!selectedFile || isUploading">
          <i v-if="isUploading" class="bi bi-arrow-repeat animate-spin u-mr-2"></i>
          {{ isUploading ? 'Uploading to Vault...' : 'Deposit Artifact' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useArtifactStore } from '../stores/artifactStore';

const props = defineProps({
  artifactId: {
    type: [Number, String],
    required: true
  },
  metadataSchema: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['uploaded']);
const artifactStore = useArtifactStore();

const isDragging = ref(false);
const fileInput = ref(null);
const selectedFile = ref(null);
const isUploading = ref(false);

const formData = ref({
  title: '',
  classification_level: 'internal',
  document_type: 'report',
  version_number: 1
});

const metadataValues = ref({});

const renderableMetadata = computed(() => {
  return props.metadataSchema?.properties || {};
});

const formatLabel = (key) => {
  return key.replace(/_/g, ' ');
};

const handleDrop = (e) => {
  isDragging.value = false;
  if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    selectedFile.value = e.dataTransfer.files[0];
    if(!formData.value.title) {
       formData.value.title = formatFilename(selectedFile.value.name);
    }
  }
};

const handleFileSelect = (e) => {
  if (e.target.files && e.target.files.length > 0) {
    selectedFile.value = e.target.files[0];
    if(!formData.value.title) {
       formData.value.title = formatFilename(selectedFile.value.name);
    }
  }
};

const formatFilename = (filename) => {
    // Remove extension
    const name = filename.replace(/\.[^/.]+$/, "");
    return name.replace(/[-_]/g, ' ');
};

const handleUpload = async () => {
  if (!selectedFile.value) return;

  isUploading.value = true;
  
  const payload = new FormData();
  payload.append('file', selectedFile.value);
  payload.append('title', formData.value.title);
  payload.append('classification_level', formData.value.classification_level);
  payload.append('document_type', formData.value.document_type);
  payload.append('artifact_id', props.artifactId);
  payload.append('metadata', JSON.stringify(metadataValues.value));

  try {
    const newDoc = await artifactStore.uploadDocument(payload);
    emit('uploaded', newDoc);
    
    // Reset
    selectedFile.value = null;
    formData.value.title = '';
    formData.value.classification_level = 'internal';
    formData.value.document_type = 'report';
    metadataValues.value = {};
  } catch (error) {
    alert(error.response?.data?.message || 'Failed to upload document');
  } finally {
    isUploading.value = false;
  }
};
</script>

<style scoped>
.hidden { display: none; }
</style>
