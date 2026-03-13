<template>
  <div class="page__wrapper">
     <div v-if="loading && !artifact" class="flex items-center justify-center min-h-[50vh]">
        <div class="animate-spin h-12 w-12 border-4 border-primary border-t-transparent rounded-full"></div>
     </div>
     
     <template v-else-if="artifact">
        <!-- Hierarchical Navigation Breadcrumb -->
        <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-4 mb-6 flex items-center gap-3 text-xs text-slate-500 overflow-x-auto whitespace-nowrap">
           <router-link to="/public-repository" class="hover:text-primary flex items-center gap-2 font-bold transition-colors">
              <i class="bi bi-house"></i> Repository Index
           </router-link>
           <i class="bi bi-chevron-right text-[10px] opacity-50"></i>
           <span class="flex items-center gap-2 font-bold text-slate-700">🏢 {{ artifact.node?.registry?.name || 'GOK Registry' }}</span>
           <i class="bi bi-chevron-right text-[10px] opacity-50"></i>
           <span class="flex items-center gap-2 text-primary font-bold border-b border-primary border-dashed pb-0.5">📁 {{ artifact.node?.full_path || 'Unmapped Path' }}</span>
           <i class="bi bi-chevron-right text-[10px] opacity-50"></i>
           <span class="text-slate-800 font-black">📦 {{ artifact.title }}</span>
        </div>
        
        <!-- Artifact Header Card -->
        <div class="card overflow-hidden border-0 shadow-xl rounded-3xl u-bg-white p-8 mb-8 relative">
           
           <div class="flex justify-between items-start mb-8">
              <div>
                <div class="flex flex-wrap items-center gap-3 mb-4">
                   <span class="bg-emerald-50 border border-emerald-200 text-emerald-600 text-[10px] px-3 py-1 rounded-xl uppercase font-black tracking-widest flex items-center gap-2 shadow-sm">
                     <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div> {{ artifact.status }}
                   </span>
                   <span class="bg-slate-100 border border-slate-200 text-slate-500 text-[10px] px-3 py-1 rounded-xl font-mono font-bold">
                      ID: {{ artifact.id }}
                   </span>
                   <span class="bg-indigo-50 border border-indigo-200 text-primary text-[10px] px-3 py-1 rounded-xl font-bold uppercase tracking-widest flex items-center gap-1">
                      <i class="bi bi-tag-fill"></i> {{ artifact.artifact_type?.name || 'General Record' }}
                   </span>
                </div>
                <h1 class="page__title text-premium flex items-center gap-4">
                   📦 {{ artifact.title }}
                </h1>
              </div>
           </div>
           
           <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <!-- Artifact Core Metadata -->
              <div class="lg:col-span-2 grid grid-cols-2 md:grid-cols-3 gap-6 bg-slate-50 border border-slate-100 p-6 rounded-2xl">
                 <div>
                   <div class="text-slate-400 text-[10px] uppercase font-black tracking-[0.2em] mb-2 flex items-center gap-2"><i class="bi bi-bank2 text-primary"></i> Owner MDA</div>
                   <div class="text-sm font-bold text-slate-800">{{ artifact.mda_owner?.name || 'GOK Central' }}</div>
                 </div>
                 <div>
                   <div class="text-slate-400 text-[10px] uppercase font-black tracking-[0.2em] mb-2 flex items-center gap-2"><i class="bi bi-diagram-3 text-primary"></i> Location Node</div>
                   <div class="text-sm font-bold text-slate-800 truncate" :title="artifact.node?.full_path">{{ artifact.node?.full_path }}</div>
                 </div>
                 <div>
                   <div class="text-slate-400 text-[10px] uppercase font-black tracking-[0.2em] mb-2 flex items-center gap-2"><i class="bi bi-calendar-check text-primary"></i> Registration</div>
                   <div class="text-sm font-bold text-slate-800">{{ new Date(artifact.created_at).toLocaleDateString() }}</div>
                 </div>
                 <div v-if="artifact.tags && artifact.tags.length > 0" class="col-span-full pt-4 mt-2 border-t border-slate-200 border-dashed">
                   <div class="text-slate-400 text-[10px] uppercase font-black tracking-[0.2em] mb-3 flex items-center gap-2"><i class="bi bi-tags text-primary"></i> Schema Tags</div>
                   <div class="flex flex-wrap gap-2">
                     <span v-for="tag in artifact.tags" :key="tag" class="bg-white border border-slate-200 px-2 py-1 rounded-lg text-[10px] text-slate-600 font-bold hover:text-primary transition-colors cursor-pointer before:content-['#'] before:text-slate-300">
                        {{ tag }}
                     </span>
                   </div>
                 </div>
              </div>

              <!-- Project Context Visualizer -->
              <div v-if="artifact.phase" class="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 p-6 rounded-2xl border-l-4 border-l-amber-500 flex flex-col justify-center relative overflow-hidden">
                 <div class="absolute -right-4 -top-4 text-6xl opacity-10 grayscale">📊</div>
                 <div class="text-[10px] text-amber-600 font-black uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
                    <i class="bi bi-kanban"></i> Project Context Integration
                 </div>
                 <div class="space-y-4 relative before:absolute before:inset-y-0 before:left-[5px] before:w-px before:bg-amber-200 before:my-2">
                    <div class="relative pl-6">
                       <div class="absolute left-0 top-1.5 w-3 h-3 rounded-full bg-white border-2 border-amber-300 z-10"></div>
                       <div class="text-[10px] text-slate-500 font-black uppercase tracking-widest mb-1">Parent Project</div>
                       <div class="text-sm text-slate-800 font-bold">{{ artifact.phase.project?.name || 'Linked Project Implementation' }}</div>
                    </div>
                    <div class="relative pl-6">
                       <div class="absolute left-0 top-1.5 w-3 h-3 rounded-full bg-amber-500 z-10 shadow-[0_0_8px_rgba(245,158,11,0.5)]"></div>
                       <div class="text-[10px] text-amber-600 font-black uppercase tracking-widest mb-1">Active Phase {{ artifact.phase.sequence }}</div>
                       <div class="text-sm text-slate-800 font-bold">{{ artifact.phase.name }}</div>
                    </div>
                 </div>
              </div>
              <div v-else class="bg-slate-50 border border-slate-200 border-dashed p-6 rounded-2xl flex items-center justify-center text-center">
                 <p class="text-xs text-slate-400 font-medium"><i class="bi bi-info-circle mb-2 block text-2xl opacity-50"></i> This artifact operates independently outside of sequenced project timelines.</p>
              </div>
           </div>
        </div>
        
        <!-- Documents Grouping List -->
        <div class="mb-12">
           <div class="flex items-center justify-between mb-6 pb-2 border-b border-slate-200">
              <h2 class="text-xl font-black text-slate-800 flex items-center gap-3">
                 <span class="text-primary text-2xl">📄</span> Artifact Documents
                 <span class="bg-indigo-50 border border-indigo-100 text-primary text-xs px-3 py-1 rounded-full font-black">{{ documents.length }}</span>
              </h2>
           </div>
           
           <div class="space-y-6">
              <div v-for="doc in documents" :key="doc.uuid" class="card overflow-hidden border border-slate-200 rounded-3xl u-bg-white p-6 shadow-md hover:shadow-lg transition-all relative group">
                 <div class="flex flex-col xl:flex-row gap-8">
                    
                    <!-- Doc Core & Metadata -->
                    <div class="flex-1">
                       <div class="flex justify-between items-start mb-6">
                          <div class="flex gap-4">
                             <div class="w-14 h-14 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-2xl text-primary shrink-0">
                               📄
                             </div>
                             <div>
                                <h3 class="text-lg font-black text-slate-800 mb-2 group-hover:text-primary transition-colors">{{ doc.title }}</h3>
                                <div class="text-xs text-slate-500 flex items-center gap-3 font-medium">
                                   <span class="bg-slate-100 border border-slate-200 px-2 py-1 rounded-md">{{ doc.document_type || 'Document' }}</span>
                                   <span class="flex items-center gap-1 text-primary bg-indigo-50 px-2 py-1 rounded-md"><i class="bi bi-diagram-2"></i> Schema Bound</span>
                                </div>
                             </div>
                          </div>
                          <!-- Classification Badge -->
                          <div class="shrink-0">
                             <span class="text-[10px] px-3 py-1.5 rounded-xl font-black uppercase tracking-widest border shadow-sm" :class="getClassificationStyle(doc.classification_level)">
                                <i class="bi bi-shield-lock-fill mr-1"></i> {{ doc.classification_level }}
                             </span>
                          </div>
                       </div>
                       
                       <!-- Audit & Linkage Grid -->
                       <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-slate-50 p-5 rounded-2xl border border-slate-100">
                          <div class="flex flex-col gap-1.5">
                             <span class="text-slate-400 text-[9px] uppercase font-black tracking-widest flex items-center gap-1.5" title="Uploaded By"><i class="bi bi-person text-primary"></i> Uploader</span>
                             <span class="text-slate-800 text-xs truncate font-bold">{{ doc.uploaded_by?.username || 'System' }}</span>
                          </div>
                          <div class="flex flex-col gap-1.5">
                             <span class="text-slate-400 text-[9px] uppercase font-black tracking-widest flex items-center gap-1.5" title="Creation Date"><i class="bi bi-calendar-plus text-primary"></i> Added</span>
                             <span class="text-slate-800 text-xs font-bold">{{ new Date(doc.created_at).toLocaleDateString() }}</span>
                          </div>
                          <div class="flex flex-col gap-1.5">
                             <span class="text-slate-400 text-[9px] uppercase font-black tracking-widest flex items-center gap-1.5" title="Current Version"><i class="bi bi-signpost-split text-primary"></i> Release</span>
                             <span class="text-slate-800 text-xs font-mono font-black">v{{ doc.current_version_number }}</span>
                          </div>
                          <div class="flex flex-col gap-1.5">
                             <span class="text-slate-400 text-[9px] uppercase font-black tracking-widest flex items-center gap-1.5" title="Schema Link"><i class="bi bi-link-45deg text-primary"></i> Bindings</span>
                             <span class="text-slate-800 text-xs font-bold truncate" :title="doc.content_type ? `Generic Link: ${doc.content_type}` : 'Direct Artifact'">
                                {{ doc.content_type ? 'Linked Entity' : 'Direct' }}
                             </span>
                          </div>
                       </div>
                    </div>
                    
                    <!-- Versions Timeline & Downloads -->
                    <div class="w-full xl:w-96 border-t xl:border-t-0 xl:border-l border-slate-200 pt-6 xl:pt-0 xl:pl-8 flex flex-col">
                       <div class="flex-1">
                          <div class="flex items-center justify-between mb-5 pb-3 border-b border-slate-200 border-dashed">
                             <span class="text-slate-700 text-sm font-black flex items-center gap-2"><i class="bi bi-clock-history text-primary"></i> Revision History</span>
                             <span class="text-slate-400 text-[10px] uppercase font-black tracking-widest">{{ doc.versions?.length || 0 }} Entries</span>
                          </div>
                          
                          <div class="space-y-4 relative before:absolute before:inset-y-0 before:left-[7px] before:w-px before:bg-slate-200 before:my-2">
                             <div v-for="(v, index) in (doc.versions || []).slice(0, 3)" :key="v.id" class="relative pl-6">
                                <div class="absolute left-0 top-1 w-[15px] h-[15px] bg-white border-2 rounded-full z-10 flex items-center justify-center" :class="index === 0 ? 'border-emerald-500 shadow-[0_0_5px_rgba(16,185,129,0.3)]' : 'border-slate-300'"></div>
                                <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-xl hover:border-primary/30 hover:bg-indigo-50/30 transition-colors">
                                   <div class="flex justify-between items-center text-slate-800 font-mono mb-2">
                                      <span class="font-black text-xs">v{{ v.version_number }}</span>
                                      <span class="text-slate-500 text-[10px] bg-white border border-slate-200 px-2 py-0.5 rounded-md font-bold">{{ formatSize(v.file_size) }}</span>
                                   </div>
                                   <p class="text-slate-600 text-xs mb-3 line-clamp-2 font-medium leading-relaxed" :title="v.change_summary">{{ v.change_summary || 'Standard version iteration' }}</p>
                                   <div class="flex flex-wrap gap-2">
                                     <span class="text-[9px] bg-emerald-50 text-emerald-600 px-2 py-1 rounded-md font-mono border border-emerald-100 flex items-center gap-1.5 font-bold">
                                        <i class="bi bi-shield-check"></i> {{ v.checksum?.substring(0,12) || 'Verified' }}
                                     </span>
                                     <span class="text-[9px] bg-white border border-slate-200 text-slate-500 px-2 py-1 rounded-md font-mono uppercase font-bold">{{ v.mime_type?.split('/').pop() || 'File' }}</span>
                                   </div>
                                </div>
                             </div>
                          </div>
                       </div>
                       
                       <div class="mt-6 flex gap-3">
                          <button @click="openPreview(doc)" class="flex-1 button button--secondary button--pill py-3 text-xs font-black uppercase tracking-widest flex items-center justify-center gap-2">
                             <i class="bi bi-eye"></i> Preview
                          </button>
                          <button @click="download(doc.uuid, doc.title)" class="flex-1 button button--primary button--pill py-3 text-xs font-black uppercase tracking-widest flex items-center justify-center gap-2 shadow-lg hover:shadow-xl">
                             <i class="bi bi-cloud-arrow-down-fill"></i> Download
                          </button>
                       </div>
                    </div>
                 </div>
              </div>
           </div>
        </div>
        
        <!-- Related Schema Lineage (Bottom Section) -->
        <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
           <div class="card border-0 shadow-lg rounded-3xl u-bg-white p-8">
              <h3 class="text-sm font-black text-slate-800 mb-6 uppercase tracking-[0.2em] flex items-center gap-3 pb-4 border-b border-slate-100">
                 <i class="bi bi-diagram-3 text-primary text-xl"></i> Structural Lineage
              </h3>
              <div class="space-y-4">
                 <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl">
                    <span class="text-slate-500 font-bold text-xs">Parent Node Path</span>
                    <span class="text-slate-800 text-xs font-mono font-bold max-w-[200px] truncate" :title="artifact.node?.full_path">{{ artifact.node?.full_path || 'None' }}</span>
                 </div>
                 <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl">
                    <span class="text-slate-500 font-bold text-xs">Schema Metadata</span>
                    <span class="text-primary text-xs font-black cursor-pointer hover:underline bg-indigo-50 px-2 py-1 rounded-lg">{{ Object.keys(artifact.metadata || {}).length }} Fields Configured</span>
                 </div>
                 <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl">
                    <span class="text-slate-500 font-bold text-xs">Artifact Type Base</span>
                    <span class="bg-slate-200 text-slate-700 px-2 py-1 rounded-lg text-[10px] font-mono font-black">{{ artifact.artifact_type?.code || 'GENERIC_RECORD' }}</span>
                 </div>
              </div>
           </div>
           
           <div class="card border-0 shadow-lg rounded-3xl u-bg-white p-8">
              <h3 class="text-sm font-black text-slate-800 mb-6 uppercase tracking-[0.2em] flex items-center gap-3 pb-4 border-b border-slate-100">
                 <i class="bi bi-shield-check text-emerald-500 text-xl"></i> Audit & Governance
              </h3>
              <div class="space-y-4">
                 <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl">
                    <span class="text-slate-500 font-bold text-xs">Approval Consensus</span>
                    <span class="text-emerald-600 text-xs font-black uppercase tracking-wider flex items-center gap-1.5 bg-emerald-50 px-2 py-1 rounded-lg"><i class="bi bi-check2-circle"></i> {{ artifact.status }}</span>
                 </div>
                 <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl">
                    <span class="text-slate-500 font-bold text-xs">Last Registry Modification</span>
                    <span class="text-slate-800 text-xs font-bold">{{ new Date(artifact.updated_at).toLocaleString() }}</span>
                 </div>
                 <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl">
                    <span class="text-slate-500 font-bold text-xs">Custodial Jurisdiction</span>
                    <span class="text-slate-800 text-xs font-bold">{{ artifact.mda_owner?.name || 'GOK Central' }}</span>
                 </div>
              </div>
           </div>
        </div>
     </template>

     <!-- Public Preview Modal -->
     <PublicDocumentPreview 
       v-model="previewModalOpen" 
       :document="selectedDoc" 
       @close="selectedDoc = null" 
     />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { usePublicArtifactStore } from '../stores/publicArtifactStore';
import publicRepositoryApi from '../services/publicRepositoryApi';
import PublicDocumentPreview from '../components/PublicDocumentPreview.vue';

const route = useRoute();
const store = usePublicArtifactStore();

const loading = computed(() => store.loading);
const artifact = computed(() => store.selectedArtifact);
const documents = computed(() => store.documents);

const previewModalOpen = ref(false);
const selectedDoc = ref(null);

const openPreview = (doc) => {
  selectedDoc.value = doc;
  previewModalOpen.value = true;
};

const getClassificationStyle = (level) => {
   const map = {
       'public': 'bg-emerald-50 text-emerald-600 border-emerald-200',
       'internal': 'bg-amber-50 text-amber-600 border-amber-200',
       'restricted': 'bg-red-50 text-red-600 border-red-200',
       'confidential': 'bg-indigo-50 text-indigo-600 border-indigo-200'
   };
   return map[level?.toLowerCase()] || 'bg-slate-50 text-slate-600 border-slate-200';
};

const formatSize = (bytes) => {
   if (!bytes) return '0 B';
   const k = 1024;
   const sizes = ['B', 'KB', 'MB', 'GB'];
   const i = Math.floor(Math.log(bytes) / Math.log(k));
   return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const download = async (uuid, title) => {
   try {
       const res = await publicRepositoryApi.downloadDocument(uuid);
       const url = window.URL.createObjectURL(new Blob([res.data]));
       const link = document.createElement('a');
       link.href = url;
       const fileName = title ? (title.toLowerCase().endsWith('.pdf') ? title : `${title}.pdf`) : `document_${uuid}.pdf`;
       link.setAttribute('download', fileName);
       document.body.appendChild(link);
       link.click();
       window.URL.revokeObjectURL(url);
   } catch(err) {
       console.error("Failed to securely download file", err);
       alert("Failed to download file. It may be restricted.");
   }
};

onMounted(() => {
  const id = route.params.id;
  if(id) {
     store.fetchArtifactDetails(id);
  }
});
</script>