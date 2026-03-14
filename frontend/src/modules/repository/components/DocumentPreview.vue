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
        <button @click="initiateDownload" class="button button--primary button--tiny button--pill">
          <i class="bi bi-download u-mr-1"></i> Download Securely
        </button>
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

      <!-- Markdown Viewer -->
      <div v-else-if="markdownContent && isMarkdown" class="u-flex-1 u-bg-white u-overflow-y-auto u-flex u-flex-col">
        <!-- Renderer Toolbar -->
        <div class="u-border-b u-border-slate-100 u-p-4 u-flex u-justify-between u-items-center u-bg-slate-50/50 shrink-0">
           <div class="u-flex u-items-center u-gap-3">
              <div class="u-flex u-items-center u-gap-2">
                <i class="bi bi-cpu text-primary"></i>
                <span class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest">DRMS Markdown Engine</span>
              </div>
              <div class="u-h-4 u-w-px u-bg-slate-300"></div>
              <span class="u-text-[10px] u-font-bold u-text-muted u-uppercase tracking-wider">Mermaid v10 Enabled</span>
           </div>
            <div class="u-flex u-bg-slate-200/50 u-p-1 u-rounded-xl border border-slate-200">
               <button 
                 @click="markdownMode = 'rendered'" 
                 class="u-px-4 u-py-1.5 u-rounded-lg u-text-[10px] u-font-black u-uppercase u-transition-all" 
                 :class="markdownMode === 'rendered' ? 'u-bg-white u-text-primary u-shadow-sm' : 'u-text-slate-500 hover:u-text-primary'"
               >
                 View Rendered
               </button>
               <button 
                 @click="markdownMode = 'source'" 
                 class="u-px-4 u-py-1.5 u-rounded-lg u-text-[10px] u-font-black u-uppercase u-transition-all" 
                 :class="markdownMode === 'source' ? 'u-bg-white u-text-primary u-shadow-sm' : 'u-text-slate-500 hover:u-text-primary'"
               >
                 Source Code
               </button>
            </div>
        </div>

        <!-- Rendered Content -->
        <div class="u-flex-1 u-p-8 u-overflow-y-auto custom-scrollbar">
          <div v-if="markdownMode === 'rendered'" class="u-max-w-4xl u-mx-auto prose prose-slate prose-indigo">
            <div ref="markdownBody" v-html="renderedMarkdown" class="markdown-body"></div>
          </div>
          <!-- Raw Source Code -->
          <div v-else class="u-max-w-4xl u-mx-auto">
             <div class="u-bg-slate-900 u-rounded-2xl u-overflow-hidden u-shadow-2xl border border-slate-800">
                <div class="u-flex u-items-center u-justify-between u-px-4 u-py-2 u-bg-slate-800/50 u-border-b u-border-slate-700">
                   <span class="u-text-[9px] u-font-mono u-text-slate-400 uppercase tracking-widest">markdown_source.md</span>
                   <i class="bi bi-code-slash u-text-slate-500"></i>
                </div>
                <pre class="u-p-6 u-text-slate-300 u-font-mono u-text-xs u-leading-relaxed u-overflow-x-auto"><code>{{ markdownContent }}</code></pre>
             </div>
          </div>
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
import { ref, watch, computed, nextTick, onMounted } from 'vue';
import repositoryApi from '../services/repositoryApi';
import BaseModal from '@/components/Common/BaseModal.vue';
import VuePdfEmbed from 'vue-pdf-embed';
import 'vue-pdf-embed/dist/styles/annotationLayer.css';
import 'vue-pdf-embed/dist/styles/textLayer.css';
import { marked } from 'marked';
import mermaid from 'mermaid';
import DOMPurify from 'dompurify';

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
const markdownContent = ref('');
const markdownMode = ref('rendered'); // 'rendered' | 'source'
const isLoading = ref(false);
const markdownBody = ref(null);

const renderedMarkdown = computed(() => {
  if (!markdownContent.value) return '';
  const html = marked.parse(markdownContent.value);
  // Ensure we allow the classes needed for mermaid and other stylings
  return DOMPurify.sanitize(html, {
    ADD_ATTR: ['class', 'data-processed'],
    ADD_TAGS: ['style']
  });
});

watch(() => props.modelValue, (val) => {
  isOpen.value = val;
  if (val && props.document) {
    if (isMarkdown.value) {
      fetchMarkdownContent();
    } else {
      fetchPreviewUrl();
    }
  } else {
    previewUrl.value = null;
    downloadUrl.value = null;
    markdownContent.value = '';
  }
});

watch(renderedMarkdown, () => {
  if (isMarkdown.value && markdownMode.value === 'rendered' && !isLoading.value) {
    renderMermaid();
  }
});

watch(markdownMode, (mode) => {
  if (mode === 'rendered' && !isLoading.value) {
    renderMermaid();
  }
});

watch(isLoading, (loading) => {
  if (!loading && isMarkdown.value && markdownMode.value === 'rendered') {
    renderMermaid();
  }
});

watch(isOpen, (val) => {
  emit('update:modelValue', val);
});

onMounted(() => {
  mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'Outfit, Inter, sans-serif',
    flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'basis' },
    sequence: { useMaxWidth: false },
  });
});

const handleClose = () => {
  isOpen.value = false;
  emit('close');
  
  // Cleanup browser memory holding the active BLOB streams
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  if (downloadUrl.value) URL.revokeObjectURL(downloadUrl.value);
  
  previewUrl.value = null;
  downloadUrl.value = null;
  markdownContent.value = '';
};

const renderMermaid = async () => {
  if (!markdownContent.value) return;
  await nextTick();
  
  if (!markdownBody.value) {
    console.warn('Mermaid: markdownBody ref not found');
    return;
  }

  // Search for anything that looks like a mermaid block
  // We check for language-mermaid class, but also fall back to checking content
  const allCodeBlocks = markdownBody.value.querySelectorAll('pre code, code');
  const blocksToProcess = [];

  for (const block of allCodeBlocks) {
    const content = block.textContent.trim();
    const isMermaidClass = block.className.includes('mermaid') || 
                          (block.parentElement && block.parentElement.className.includes('mermaid'));
    const isMermaidContent = content.startsWith('graph ') || 
                             content.startsWith('sequenceDiagram') || 
                             content.startsWith('gannt') || 
                             content.startsWith('classDiagram') ||
                             content.startsWith('stateDiagram') ||
                             content.startsWith('pie') ||
                             content.startsWith('flowchart');

    if ((isMermaidClass || isMermaidContent) && !block.getAttribute('data-mermaid-processed')) {
      blocksToProcess.push(block);
    }
  }

  if (blocksToProcess.length === 0) {
    console.log('Mermaid: No blocks to process');
    return;
  }

  const nodesToProcess = [];

  for (const block of blocksToProcess) {
    const pre = block.parentElement;
    const code = block.textContent.trim();

    // Create a styled wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'mermaid-wrapper relative group bg-slate-50 rounded-xl p-8 border border-slate-100 my-8 transition-all hover:shadow-lg flex justify-center w-full';
    
    block.setAttribute('data-mermaid-processed', 'true');

    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid';
    mermaidDiv.textContent = code;
    const id = `mermaid-v10-${Math.random().toString(36).substring(2, 11)}`;
    mermaidDiv.id = id;

    wrapper.appendChild(mermaidDiv);
    
    // Replace the container (pre or code)
    if (pre && pre.tagName === 'PRE') {
      pre.replaceWith(wrapper);
    } else {
      block.replaceWith(wrapper);
    }
    
    nodesToProcess.push(mermaidDiv);
  }

  try {
    console.log(`Mermaid: Running transformation on ${nodesToProcess.length} nodes...`);
    await mermaid.run({
      nodes: nodesToProcess,
      suppressErrors: true
    });
    console.log('Mermaid: Transformation complete.');
  } catch (e) {
    console.error('Mermaid render error:', e);
  }
};

const fetchMarkdownContent = async () => {
  isLoading.value = true;
  try {
    const res = await repositoryApi.previewDocument(props.document.uuid);
    const text = await res.data.text();
    markdownContent.value = text;
    
    const resDownload = await repositoryApi.downloadDocument(props.document.uuid);
    const blobDownload = new Blob([resDownload.data], { type: resDownload.headers['content-type'] });
    downloadUrl.value = URL.createObjectURL(blobDownload);
  } catch (error) {
    console.error("Failed to fetch markdown content.", error);
  } finally {
    isLoading.value = false;
  }
};

const formatCategory = (cat) => {
  if (!cat) return '';
  return cat.charAt(0).toUpperCase() + cat.slice(1);
};

const initiateDownload = async () => {
   try {
       const res = await repositoryApi.downloadDocument(props.document.uuid);
       const contentType = res.headers['content-type'];
       const blob = new Blob([res.data], { type: contentType });
       const url = window.URL.createObjectURL(blob);
       const link = document.createElement('a');
       link.href = url;
       
       let extension = '';
       if (contentType === 'application/pdf') extension = '.pdf';
       else if (contentType === 'text/markdown' || contentType === 'text/x-markdown') extension = '.md';
       else if (contentType === 'image/png') extension = '.png';
       else if (contentType === 'image/jpeg') extension = '.jpg';
       
       let fileName = props.document.title || `document_${props.document.uuid}`;
       if (extension && !fileName.toLowerCase().endsWith(extension)) {
           fileName += extension;
       }
       
       link.setAttribute('download', fileName);
       document.body.appendChild(link);
       link.click();
       window.URL.revokeObjectURL(url);
   } catch(err) {
       console.error("Failed to download file", err);
       alert("Failed to download file.");
   }
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

const isMarkdown = computed(() => {
  const mt = currentVersionMimeType.value;
  if (mt && (mt === 'text/markdown' || mt === 'text/x-markdown' || mt === 'application/octet-stream')) {
      // Some browsers/environments might return octet-stream for .md files
      return true;
  }
  
  const title = props.document?.title?.toLowerCase() || '';
  if (title.endsWith('.md') || title.endsWith('.markdown')) return true;
  
  // Also check filename in versions if available
  const versions = props.document?.versions;
  if (versions && versions.length > 0) {
    const latest = versions[0];
    if (latest.file && latest.file.toLowerCase().endsWith('.md')) return true;
  }
  
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
<style scoped>
.markdown-body {
  font-family: inherit;
}
:deep(.mermaid-svg) {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  margin: 2rem 0;
}
:deep(.markdown-body pre) {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
}
</style>
