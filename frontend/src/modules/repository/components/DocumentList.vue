<template>
  <div class="card overflow-hidden border-0 shadow-xl rounded-2xl u-bg-white">
    <div class="u-p-6 u-border-b u-border-slate-100 u-flex u-justify-between u-items-center">
      <h3 class="u-text-base u-font-black u-text-main flex items-center gap-2">
        <i class="bi bi-stack u-text-primary"></i> 
        Formal Documents
      </h3>
      <div class="badge badge--secondary">{{ documents.length }} Entries</div>
    </div>
    
    <div class="u-divide-y u-divide-slate-100">
      <div v-for="doc in documents" :key="doc.uuid" class="u-p-6 transition-all hover:u-bg-slate-50/50">
        <div class="u-flex u-justify-between u-items-start u-gap-6">
          <!-- Document Info -->
          <div class="u-flex-1">
            <div class="u-flex u-items-center u-gap-2 u-mb-1">
               <span class="u-text-[9px] u-font-black u-bg-primary/10 u-text-primary u-px-2 u-py-0.5 u-rounded u-uppercase u-tracking-tighter">Authoritative Preview</span>
               <span class="u-text-[9px] u-font-black u-bg-slate-100 u-text-slate-500 u-px-2 u-py-0.5 u-rounded u-uppercase u-tracking-tighter">Verified Asset</span>
               <span v-if="doc.is_digitized" class="u-text-[9px] u-font-black u-bg-success/10 u-text-success u-px-2 u-py-0.5 u-rounded u-uppercase u-tracking-tighter">
                 <i class="bi bi-robot"></i> Digitized (Conf: {{ doc.extraction_confidence || 'N/A' }})
               </span>
               <span v-if="doc.needs_qa" class="u-text-[9px] u-font-black u-bg-danger/10 u-text-danger u-px-2 u-py-0.5 u-rounded u-uppercase u-tracking-tighter animate-pulse">
                 <i class="bi bi-exclamation-triangle"></i> Needs QA
               </span>
            </div>
            <h4 class="u-text-base u-font-black u-text-main u-leading-tight u-mb-2">
              {{ doc.title }}
            </h4>
            <div class="u-flex u-items-center u-gap-2 u-text-[10px] u-font-bold u-text-muted u-uppercase u-tracking-widest">
              <span class="u-flex u-items-center u-gap-1">
                <i class="bi bi-file-earmark-text u-text-slate-400"></i>
                {{ doc.document_type }}
              </span>
              <span class="u-text-slate-300">•</span>
              <span class="u-text-primary">v{{ doc.current_version_number }}</span>
              <span class="u-text-slate-300">•</span>
              <span :class="getClassificationColor(doc.classification_level)">{{ doc.classification_level }}</span>
            </div>

            <!-- OCR Text Preview (if Needs QA) -->
            <div v-if="doc.needs_qa && doc.ocr_text" class="u-mt-3 u-p-3 u-bg-amber-50 u-rounded-lg u-border u-border-amber-200">
              <div class="u-text-[10px] u-font-black u-text-amber-800 u-uppercase u-tracking-widest u-mb-1"><i class="bi bi-text-left"></i> Extracted OCR Text (Review Required)</div>
              <p class="u-text-xs u-text-amber-900 u-font-mono u-whitespace-pre-wrap">{{ doc.ocr_text }}</p>
            </div>

            <!-- Business Metadata Chips -->
            <div v-if="doc.metadata && Object.keys(doc.metadata).length > 0" class="u-mt-4 u-flex u-flex-wrap u-gap-2">
              <span v-for="(val, key) in doc.metadata" :key="key" class="u-px-2.5 u-py-1 u-bg-white u-border u-border-slate-200 u-text-slate-600 u-rounded-lg u-text-[9px] u-font-black u-uppercase u-tracking-tighter shadow-sm">
                {{ key.replace('_', ' ') }}: <span class="u-text-primary">{{ val }}</span>
              </span>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="u-flex u-items-center u-gap-3">
            <button v-if="!doc.is_digitized" @click="$emit('digitize', doc)" class="button button--secondary button--sm button--pill shadow-sm" title="Run Intelligent Document Processing">
              <i class="bi bi-cpu u-mr-1.5"></i> Digitize
            </button>
            <button v-if="doc.needs_qa" @click="$emit('approve-qa', doc)" class="button button--success button--sm button--pill shadow-sm" title="Approve OCR Text">
              <i class="bi bi-check-circle u-mr-1.5"></i> Approve QA
            </button>
            <button @click="$emit('preview', doc)" class="button button--ghost button--sm button--pill u-bg-slate-100 hover:u-bg-slate-200" title="Preview securely">
              <i class="bi bi-eye u-mr-1.5"></i> View
            </button>
            <a :href="`/api/v1/documents/${doc.uuid}/download/`" target="_blank" class="button button--primary button--sm button--pill shadow-lg shadow-primary/20" title="Download payload">
              <i class="bi bi-download"></i>
            </a>
            <button @click="$emit('delete', doc)" class="button button--danger button--sm button--pill shadow-sm ml-2" title="Delete Document">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>
        
        <!-- Versions Timeline -->
        <div class="u-mt-4 u-pt-4 u-border-t u-border-dashed u-border-slate-100 u-pl-6" v-if="doc.versions && doc.versions.length > 0">
          <div v-for="version in doc.versions" :key="version.id" class="u-flex u-items-start u-gap-4 u-mb-3 last:u-mb-0 u-relative">
            <!-- Timeline Connectors -->
            <div class="u-absolute -u-left-4 u-top-2 u-h-full u-w-px u-bg-slate-200 last:u-h-0"></div>
            <div class="u-w-2 u-h-2 u-bg-primary u-rounded-full u-absolute -u-left-[1.125rem] u-top-1.5 u-ring-4 u-ring-white"></div>
            
            <div class="u-flex-1 u-bg-slate-50 u-rounded-xl u-p-3 u-text-[10px] u-font-medium u-text-main flex flex-col sm:flex-row sm:justify-between sm:items-center">
              <div>
                <span class="u-font-black u-text-primary u-mr-2">v{{ version.version_number }}</span>
                Uploaded by {{ version.uploaded_by?.username || 'Officer' }}
              </div>
              <div class="u-text-muted font-bold mt-1 sm:mt-0">
                <i class="bi bi-calendar-check u-mr-1"></i> {{ getRelativeTime(version.created_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="documents.length === 0" class="u-p-10 u-text-center u-text-muted u-font-bold u-uppercase u-tracking-widest u-text-[10px]">
        No documents deposited yet for this artifact.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  documents: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['preview', 'digitize', 'approve-qa', 'delete']);

const getClassificationColor = (level) => {
  const map = {
    'public': 'u-text-success',
    'internal': 'u-text-primary',
    'restricted': 'u-text-warning',
    'confidential': 'u-text-danger'
  };
  return map[level] || 'u-text-slate-500';
};

const getRelativeTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
};
</script>
