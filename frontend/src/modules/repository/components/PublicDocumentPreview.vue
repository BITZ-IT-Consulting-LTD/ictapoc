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
          Public Repository Preview • v{{ document.current_version_number || 1 }}
        </p>
      </div>
      <div class="u-flex u-gap-3">
        <button @click="initiateDownload" class="button button--primary button--tiny button--pill">
          <i class="bi bi-download u-mr-1"></i> Download Public Record
        </button>
      </div>
    </template>

    <div class="u-flex u-flex-col u-h-[80vh] u-bg-slate-100">
      <!-- Loading State -->
      <div v-if="isLoading" class="u-flex-1 u-flex u-flex-col u-items-center u-justify-center">
        <div class="animate-spin u-h-12 u-w-12 u-border-4 u-border-primary u-border-t-transparent u-rounded-full u-mx-auto mb-4"></div>
        <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">Streaming Public Document...</p>
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

      <!-- Image Preview -->
      <div v-else-if="previewUrl && isImage" class="u-flex-1 u-flex u-items-center u-justify-center u-p-10 u-overflow-auto">
        <img :src="previewUrl" alt="Document Preview" class="u-max-w-full u-max-h-full u-object-contain u-rounded-2xl u-shadow-2xl">
      </div>

      <!-- Fallback -->
      <div v-else class="u-flex-1 u-flex u-flex-col u-items-center u-justify-center u-text-muted">
        <i class="bi bi-exclamation-triangle u-text-5xl mb-4 text-warning"></i>
        <p class="u-font-black u-text-main u-uppercase u-tracking-widest">Preview Unavailable</p>
        <p class="u-text-xs u-mt-2 font-bold max-w-md text-center">
          This record cannot be rendered natively in the browser.
          Please download the file to view it using your local applications.
        </p>
        <button @click="initiateDownload" class="button button--secondary button--pill u-mt-6">
          Initiate Download
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import publicRepositoryApi from '../services/publicRepositoryApi';
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
const isLoading = ref(false);

watch(() => props.modelValue, (val) => {
  isOpen.value = val;
  if (val && props.document) {
    fetchPreviewUrl();
  } else {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
    previewUrl.value = null;
  }
});

watch(isOpen, (val) => {
  emit('update:modelValue', val);
});

const handleClose = () => {
  isOpen.value = false;
  emit('close');
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = null;
};

const fetchPreviewUrl = async () => {
  isLoading.value = true;
  try {
    const resPreview = await publicRepositoryApi.previewDocument(props.document.uuid);
    const blobPreview = new Blob([resPreview.data], { type: resPreview.headers['content-type'] });
    previewUrl.value = URL.createObjectURL(blobPreview);
  } catch (error) {
    console.error("Failed to generate public document stream.", error);
  } finally {
    isLoading.value = false;
  }
};

const initiateDownload = async () => {
   try {
       const res = await publicRepositoryApi.downloadDocument(props.document.uuid);
       const url = window.URL.createObjectURL(new Blob([res.data]));
       const link = document.createElement('a');
       link.href = url;
       const title = props.document.title;
       const fileName = title ? (title.toLowerCase().endsWith('.pdf') ? title : `${title}.pdf`) : `document_${props.document.uuid}.pdf`;
       link.setAttribute('download', fileName);
       document.body.appendChild(link);
       link.click();
       window.URL.revokeObjectURL(url);
   } catch(err) {
       console.error("Failed to download file", err);
       alert("Failed to download file.");
   }
};

const currentVersionMimeType = computed(() => {
  const versions = props.document?.versions;
  if (versions && versions.length > 0) {
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

const isImage = computed(() => {
  const mt = currentVersionMimeType.value;
  if (mt && mt.startsWith('image/')) return true;
  const title = props.document?.title?.toLowerCase() || '';
  return title.match(/\.(jpeg|jpg|gif|png|webp|svg)$/) != null;
});
</script>
