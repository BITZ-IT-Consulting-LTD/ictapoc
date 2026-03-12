<template>
  <BaseModal
    v-if="document"
    v-model:show="isOpen"
    :title="document.title"
    size="full"
    headerClass="modal__header--dark"
    @close="handleClose"
  >
    <template #header>
      <div class="u-flex-1">
        <h3 class="modal__title flex items-center gap-3">
          <i class="bi bi-file-earmark-pdf u-text-primary"></i> 
          {{ document.title }}
        </h3>
        <p class="modal__subtitle u-font-mono u-uppercase" style="letter-spacing: 0.1em">
          Authoritative Preview • v{{ document.current_version_number || 1 }} • {{ formatCategory(document.classification_level) }}
        </p>
      </div>
      <div class="u-flex u-gap-3">
        <a :href="downloadUrl" target="_blank" class="button button--primary button--tiny button--pill" v-if="downloadUrl">
          <i class="bi bi-download u-mr-1"></i> Download Securely
        </a>
      </div>
    </template>

    <div class="u-flex u-flex-col u-h-[80vh] u-bg-slate-100">
      <!-- Loading State -->
      <div v-if="isLoading" class="u-flex-1 u-flex u-flex-col u-items-center u-justify-center">
        <div class="animate-spin u-h-12 u-w-12 u-border-4 u-border-primary u-border-t-transparent u-rounded-full u-mx-auto mb-4"></div>
        <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">Generating Secure Preview Token...</p>
      </div>

      <!-- Native PDF Viewer Component -->
      <div v-else-if="previewUrl && isPdf" class="u-flex-1 u-bg-slate-200 u-overflow-y-auto u-flex u-justify-center u-p-6">
         <div class="u-w-full u-max-w-4xl u-shadow-2xl u-rounded-xl u-bg-white overflow-hidden">
            <VuePdfEmbed
              :source="previewUrl"
              class="w-full"
            />
         </div>
      </div>

      <!-- General Iframe Fallback -->
      <iframe 
        v-else-if="previewUrl && isPdfOrRenderable" 
        :src="previewUrl" 
        class="u-w-full u-h-full u-border-0"
        title="Document Preview"
      ></iframe>

      <!-- Image Preview -->
      <div v-else-if="previewUrl && isImage" class="u-flex-1 u-flex u-items-center u-justify-center u-p-10 u-overflow-auto">
        <img :src="previewUrl" alt="Document Preview" class="u-max-w-full u-max-h-full u-object-contain u-rounded-2xl u-shadow-2xl">
      </div>

      <!-- Fallback -->
      <div v-else class="u-flex-1 u-flex u-flex-col u-items-center u-justify-center u-text-muted">
        <i class="bi bi-exclamation-triangle u-text-5xl mb-4 text-warning"></i>
        <p class="u-font-black u-text-main u-uppercase u-tracking-widest">Preview Unavailable</p>
        <p class="u-text-xs u-mt-2 font-bold max-w-md text-center">
          The requested file format cannot be rendered natively in the browser.
          Please downlaod the file securely to view it using your local applications.
        </p>
        <a :href="downloadUrl" target="_blank" class="button button--secondary button--pill u-mt-6" v-if="downloadUrl">
          Initiate Download
        </a>
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import repositoryApi from '../services/repositoryApi';
import BaseModal from '@/components/Common/BaseModal.vue';
import VuePdfEmbed from 'vue-pdf-embed';
import 'vue-pdf-embed/dist/styles/annotationLayer.css';
import 'vue-pdf-embed/dist/styles/textLayer.css';

const props = defineProps({
  document: {
    type: Object,
    default: null
  },
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'close']);

const isOpen = ref(props.modelValue);
const previewUrl = ref(null);
const downloadUrl = ref(null);
const isLoading = ref(false);

watch(() => props.modelValue, (val) => {
  isOpen.value = val;
  if (val && props.document) {
    fetchPreviewUrl();
  } else {
    previewUrl.value = null;
    downloadUrl.value = null;
  }
});

watch(isOpen, (val) => {
  emit('update:modelValue', val);
});

const handleClose = () => {
  isOpen.value = false;
  emit('close');
  
  // Cleanup browser memory holding the active BLOB streams
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  if (downloadUrl.value) URL.revokeObjectURL(downloadUrl.value);
  
  previewUrl.value = null;
  downloadUrl.value = null;
};

const formatCategory = (cat) => {
  if (!cat) return '';
  return cat.charAt(0).toUpperCase() + cat.slice(1);
};

// We assume the backend gives us a URL we can embed. 
// For a real architecture with S3, the backend would return a presigned URL.
// Generate local browser Blob URLs instead of relying on open docker container networks
const fetchPreviewUrl = async () => {
  isLoading.value = true;
  try {
    const resPreview = await repositoryApi.previewDocument(props.document.uuid);
    const blobPreview = new Blob([resPreview.data], { type: resPreview.headers['content-type'] });
    previewUrl.value = URL.createObjectURL(blobPreview);
    
    // For downloads, we map to the exact same logic. In a real environment we might just set the button to trigger the api directly.
    const resDownload = await repositoryApi.downloadDocument(props.document.uuid);
    const blobDownload = new Blob([resDownload.data], { type: resDownload.headers['content-type'] });
    downloadUrl.value = URL.createObjectURL(blobDownload);

  } catch (error) {
    console.error("Failed to generate secure document stream.", error);
  } finally {
    isLoading.value = false;
  }
};

const currentVersionMimeType = computed(() => {
  const versions = props.document?.versions;
  if (versions && versions.length > 0) {
    // Assuming the latest version is either the first or last, let's just find the one matching current_version_number
    const currentNum = props.document.current_version_number || 1;
    const version = versions.find(v => v.version_number === currentNum) || versions[0];
    return version.mime_type;
  }
  return props.document?.metadata?.mime_type || '';
});

const isPdf = computed(() => {
  const mt = currentVersionMimeType.value;
  if (mt && mt === 'application/pdf') return true;
  if (props.document?.title?.toLowerCase().endsWith('.pdf')) return true;
  return false;
});

const isPdfOrRenderable = computed(() => {
  const mt = currentVersionMimeType.value;
  if (mt && mt.includes('text/')) return true;
  return false;
});

const isImage = computed(() => {
  const mt = currentVersionMimeType.value;
  if (mt && mt.startsWith('image/')) return true;
  
  const title = props.document?.title?.toLowerCase() || '';
  return title.match(/\.(jpeg|jpg|gif|png|webp|svg)$/) != null;
});
</script>
