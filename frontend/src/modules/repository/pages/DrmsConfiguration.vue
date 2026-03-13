<template>
  <div class="page__wrapper">
    <header class="page__header u-mb-8">
      <div class="page__title-group">
        <h1 class="page__title text-premium flex items-center gap-3">
          <i class="bi bi-gear-fill u-text-primary"></i>
          DRMS Configuration
        </h1>
        <p class="page__subtitle u-mt-2">Authoritative Control Center for Repository Schemas, Hierarchy, and Project Context.</p>
      </div>
      
      <div class="page__actions">
        <router-link to="/repository/artifacts" class="button button--secondary button--tiny button--pill u-px-4">
           <i class="bi bi-arrow-left u-mr-2"></i> Back to Registry
        </router-link>
      </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <!-- Sidebar / Tabs -->
      <aside class="lg:col-span-1">
        <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-4">
           <h3 class="text-[10px] font-black text-slate-400 uppercase tracking-widest px-4 mb-4 mt-2">Core Schema</h3>
           <ul class="space-y-1">
             <li>
               <button @click="activeTab = 'artifact_types'" class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors flex items-center gap-3" :class="activeTab === 'artifact_types' ? 'bg-indigo-50 text-primary shadow-sm' : 'text-slate-600 hover:bg-slate-50'">
                 <i class="bi bi-box-seam"></i> Artifact Types
               </button>
             </li>
             <li>
               <button @click="activeTab = 'registries'" class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors flex items-center gap-3" :class="activeTab === 'registries' ? 'bg-indigo-50 text-primary shadow-sm' : 'text-slate-600 hover:bg-slate-50'">
                 <i class="bi bi-hdd-rack"></i> Root Registries
               </button>
             </li>
             <li>
               <button @click="activeTab = 'node_types'" class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors flex items-center gap-3" :class="activeTab === 'node_types' ? 'bg-indigo-50 text-primary shadow-sm' : 'text-slate-600 hover:bg-slate-50'">
                 <i class="bi bi-diagram-3"></i> Hierarchy Node Types
               </button>
             </li>
             <li>
               <button @click="activeTab = 'nodes'" class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors flex items-center gap-3" :class="activeTab === 'nodes' ? 'bg-indigo-50 text-primary shadow-sm' : 'text-slate-600 hover:bg-slate-50'">
                 <i class="bi bi-folder-plus"></i> Structural Nodes
               </button>
             </li>
           </ul>

           <h3 class="text-[10px] font-black text-slate-400 uppercase tracking-widest px-4 mb-4 mt-6">Execution Context</h3>
           <ul class="space-y-1">
             <li>
               <button @click="activeTab = 'projects'" class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors flex items-center gap-3" :class="activeTab === 'projects' ? 'bg-indigo-50 text-primary shadow-sm' : 'text-slate-600 hover:bg-slate-50'">
                 <i class="bi bi-kanban"></i> Projects
               </button>
             </li>
             <li>
               <button @click="activeTab = 'phases'" class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors flex items-center gap-3" :class="activeTab === 'phases' ? 'bg-indigo-50 text-primary shadow-sm' : 'text-slate-600 hover:bg-slate-50'">
                 <i class="bi bi-layers-half"></i> Project Phases
               </button>
             </li>
           </ul>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="lg:col-span-3">
        
        <!-- Artifact Types Tab -->
        <div v-if="activeTab === 'artifact_types'" class="space-y-6">
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 flex justify-between items-center">
             <div>
               <h2 class="text-lg font-black text-slate-800">Artifact Types (Categories)</h2>
               <p class="text-xs text-slate-500 font-medium">Define metadata schemas and classification codes for deliverables.</p>
             </div>
             <button @click="showArtifactTypeModal = true" class="button button--primary button--sm button--pill">
                <i class="bi bi-plus-lg mr-2"></i> New Type
             </button>
           </div>
           
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white">
             <table class="table">
               <thead>
                 <tr class="table__header-row bg-slate-50">
                   <th class="table__header-cell py-4">Name</th>
                   <th class="table__header-cell">Code</th>
                   <th class="table__header-cell">Description</th>
                   <th class="table__header-cell text-right px-6">Actions</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="t in artifactTypes" :key="t.id" class="table__row hover:bg-slate-50/50">
                   <td class="table__cell font-bold text-slate-800">{{ t.name }}</td>
                   <td class="table__cell"><span class="bg-slate-100 px-2 py-1 rounded text-[10px] font-mono font-black text-slate-600 uppercase">{{ t.code }}</span></td>
                   <td class="table__cell text-xs text-slate-500 truncate max-w-[200px]">{{ t.description }}</td>
                   <td class="table__cell text-right px-6">
                     <button @click="deleteItem('artifactType', t.id)" class="text-red-400 hover:text-red-600 transition-colors p-2"><i class="bi bi-trash"></i></button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
        </div>

        <!-- Registries Tab -->
        <div v-if="activeTab === 'registries'" class="space-y-6">
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 flex justify-between items-center">
             <div>
               <h2 class="text-lg font-black text-slate-800">Root Registries</h2>
               <p class="text-xs text-slate-500 font-medium">Top-level authoritative containers. Root level of the hierarchy tree.</p>
             </div>
             <button @click="showRegistryModal = true" class="button button--primary button--sm button--pill">
                <i class="bi bi-plus-lg mr-2"></i> New Registry
             </button>
           </div>
           
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white">
             <table class="table">
               <thead>
                 <tr class="table__header-row bg-slate-50">
                   <th class="table__header-cell py-4">Registry Name</th>
                   <th class="table__header-cell">Slug</th>
                   <th class="table__header-cell">Owner MDA</th>
                   <th class="table__header-cell text-right px-6">Actions</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="r in registries" :key="r.id" class="table__row hover:bg-slate-50/50">
                   <td class="table__cell font-bold text-slate-800">{{ r.name }}</td>
                   <td class="table__cell"><span class="text-xs font-mono text-slate-500">/{{ r.slug }}</span></td>
                   <td class="table__cell"><span class="badge badge--primary text-[10px]">{{ r.mda_owner?.code || 'SYSTEM' }}</span></td>
                   <td class="table__cell text-right px-6">
                     <button @click="deleteItem('registry', r.id)" class="text-red-400 hover:text-red-600 transition-colors p-2"><i class="bi bi-trash"></i></button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
        </div>

        <!-- Node Types Tab -->
        <div v-if="activeTab === 'node_types'" class="space-y-6">
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 flex justify-between items-center">
             <div>
               <h2 class="text-lg font-black text-slate-800">Hierarchy Node Types</h2>
               <p class="text-xs text-slate-500 font-medium">Define what nodes in the tree represent (e.g. Phase, County, Plot).</p>
             </div>
             <button @click="showNodeTypeModal = true" class="button button--primary button--sm button--pill">
                <i class="bi bi-plus-lg mr-2"></i> New Node Type
             </button>
           </div>
           
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white">
             <table class="table">
               <thead>
                 <tr class="table__header-row bg-slate-50">
                   <th class="table__header-cell py-4">Type Name</th>
                   <th class="table__header-cell">Code</th>
                   <th class="table__header-cell text-right px-6">Actions</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="nt in nodeTypes" :key="nt.id" class="table__row hover:bg-slate-50/50">
                   <td class="table__cell font-bold text-slate-800">{{ nt.name }}</td>
                   <td class="table__cell"><span class="bg-slate-100 px-2 py-1 rounded text-[10px] font-mono font-black text-slate-600 uppercase">{{ nt.code }}</span></td>
                   <td class="table__cell text-right px-6">
                     <button @click="deleteItem('nodeType', nt.id)" class="text-red-400 hover:text-red-600 transition-colors p-2"><i class="bi bi-trash"></i></button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
        </div>

        <!-- Nodes Tab -->
        <div v-if="activeTab === 'nodes'" class="space-y-6">
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 flex justify-between items-center">
             <div>
               <h2 class="text-lg font-black text-slate-800">Structural Nodes</h2>
               <p class="text-xs text-slate-500 font-medium">Manage the folder hierarchy tree for artifacts.</p>
             </div>
             <button @click="showNodeModal = true" class="button button--primary button--sm button--pill">
                <i class="bi bi-plus-lg mr-2"></i> New Node
             </button>
           </div>
           
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white">
             <table class="table">
               <thead>
                 <tr class="table__header-row bg-slate-50">
                   <th class="table__header-cell py-4">Node Path</th>
                   <th class="table__header-cell">Type</th>
                   <th class="table__header-cell">Registry</th>
                   <th class="table__header-cell text-right px-6">Actions</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="n in nodes" :key="n.id" class="table__row hover:bg-slate-50/50">
                   <td class="table__cell font-bold text-slate-800 text-xs">{{ n.full_path }}</td>
                   <td class="table__cell text-[10px] font-black uppercase text-slate-500">{{ n.node_type_name }}</td>
                   <td class="table__cell text-xs text-slate-500">{{ getRegistryNameFromNode(n.registry) }}</td>
                   <td class="table__cell text-right px-6">
                     <button @click="deleteItem('node', n.id)" class="text-red-400 hover:text-red-600 transition-colors p-2"><i class="bi bi-trash"></i></button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
        </div>

        <!-- Projects Tab -->
        <div v-if="activeTab === 'projects'" class="space-y-6">
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 flex justify-between items-center">
             <div>
               <h2 class="text-lg font-black text-slate-800">Operational Projects</h2>
               <p class="text-xs text-slate-500 font-medium">High-level contexts for digital artifact grouping.</p>
             </div>
             <button @click="showProjectModal = true" class="button button--primary button--sm button--pill">
                <i class="bi bi-plus-lg mr-2"></i> New Project
             </button>
           </div>
           
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white">
             <table class="table">
               <thead>
                 <tr class="table__header-row bg-slate-50">
                   <th class="table__header-cell py-4">Project Name</th>
                   <th class="table__header-cell">Status</th>
                   <th class="table__header-cell">Timeline</th>
                   <th class="table__header-cell text-right px-6">Actions</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="p in projects" :key="p.id" class="table__row hover:bg-slate-50/50">
                   <td class="table__cell font-bold text-slate-800">{{ p.name }}</td>
                   <td class="table__cell"><span class="badge badge--success text-[10px] uppercase font-black tracking-widest">{{ p.status }}</span></td>
                   <td class="table__cell text-xs text-slate-500">{{ p.start_date }} → {{ p.end_date || 'Ongoing' }}</td>
                   <td class="table__cell text-right px-6">
                     <button @click="deleteItem('project', p.id)" class="text-red-400 hover:text-red-600 transition-colors p-2"><i class="bi bi-trash"></i></button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
        </div>

        <!-- Project Phases Tab -->
        <div v-if="activeTab === 'phases'" class="space-y-6">
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white p-6 flex justify-between items-center">
             <div>
               <h2 class="text-lg font-black text-slate-800">Project Phases</h2>
               <p class="text-xs text-slate-500 font-medium">Sequential stages within established projects.</p>
             </div>
             <button @click="showPhaseModal = true" class="button button--primary button--sm button--pill">
                <i class="bi bi-plus-lg mr-2"></i> New Phase
             </button>
           </div>
           
           <div class="card overflow-hidden border-0 shadow-lg rounded-3xl u-bg-white">
             <table class="table">
               <thead>
                 <tr class="table__header-row bg-slate-50">
                   <th class="table__header-cell py-4">Phase Name</th>
                   <th class="table__header-cell">Sequence</th>
                   <th class="table__header-cell">Parent Project</th>
                   <th class="table__header-cell text-right px-6">Actions</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="ph in phases" :key="ph.id" class="table__row hover:bg-slate-50/50">
                   <td class="table__cell font-bold text-slate-800">{{ ph.name }}</td>
                   <td class="table__cell"><span class="bg-indigo-50 text-primary font-black px-2 py-1 rounded text-xs">#{{ ph.sequence }}</span></td>
                   <td class="table__cell text-xs font-bold text-slate-600">{{ getProjectName(ph.project) }}</td>
                   <td class="table__cell text-right px-6">
                     <button @click="deleteItem('projectPhase', ph.id)" class="text-red-400 hover:text-red-600 transition-colors p-2"><i class="bi bi-trash"></i></button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
        </div>

      </main>
    </div>

    <!-- MODALS -->

    <!-- Artifact Type Modal -->
    <BaseModal v-model:show="showArtifactTypeModal" title="Create Artifact Type" @close="showArtifactTypeModal = false">
      <div class="p-6">
        <form @submit.prevent="createItem('artifactType', newArtifactType, () => newArtifactType = { name: '', code: '', description: '', metadata_schema: {} })" class="flex flex-col gap-4">
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Display Name</label>
            <input type="text" v-model="newArtifactType.name" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. Technical Drawing">
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">System Code</label>
            <input type="text" v-model="newArtifactType.code" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. TECH_DRAWING">
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Description</label>
            <textarea v-model="newArtifactType.description" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" rows="2"></textarea>
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Metadata Schema (JSON)</label>
            <textarea v-model="metadataSchemaInput" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1 font-mono text-xs" rows="4" placeholder='{"required": ["author"], "properties": {"author": {"type": "string"}}}'></textarea>
          </div>
          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="showArtifactTypeModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill">Create Category</button>
          </div>
        </form>
      </div>
    </BaseModal>

    <!-- Registry Modal -->
    <BaseModal v-model:show="showRegistryModal" title="Create Root Registry" @close="showRegistryModal = false">
      <div class="p-6">
        <form @submit.prevent="createItem('registry', newRegistry, () => newRegistry = { name: '', slug: '', description: '' })" class="flex flex-col gap-4">
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Registry Name</label>
            <input type="text" v-model="newRegistry.name" @input="autoSlug" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. Health Records">
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Slug Identifier</label>
            <input type="text" v-model="newRegistry.slug" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. health-records">
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Description</label>
            <textarea v-model="newRegistry.description" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" rows="2"></textarea>
          </div>
          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="showRegistryModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill">Create Registry</button>
          </div>
        </form>
      </div>
    </BaseModal>

    <!-- Node Type Modal -->
    <BaseModal v-model:show="showNodeTypeModal" title="Create Hierarchy Node Type" @close="showNodeTypeModal = false">
      <div class="p-6">
        <form @submit.prevent="createItem('nodeType', newNodeType, () => newNodeType = { name: '', code: '' })" class="flex flex-col gap-4">
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Type Name</label>
            <input type="text" v-model="newNodeType.name" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. County">
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Type Code</label>
            <input type="text" v-model="newNodeType.code" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. COUNTY">
          </div>
          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="showNodeTypeModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill">Create Node Type</button>
          </div>
        </form>
      </div>
    </BaseModal>

    <!-- Node Modal -->
    <BaseModal v-model:show="showNodeModal" title="Create Structural Hierarchy Node" @close="showNodeModal = false">
      <div class="p-6">
        <form @submit.prevent="createItem('node', newNode, () => newNode = { name: '', registry: '', node_type: '', parent: null })" class="flex flex-col gap-4">
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Node Name</label>
            <input type="text" v-model="newNode.name" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. Phase 1 Documents">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label text-xs font-black uppercase text-slate-500">Registry</label>
              <select v-model="newNode.registry" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1 bg-white" required>
                 <option value="" disabled>Select Registry...</option>
                 <option v-for="r in registries" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label text-xs font-black uppercase text-slate-500">Node Type</label>
              <select v-model="newNode.node_type" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1 bg-white" required>
                 <option value="" disabled>Select Type...</option>
                 <option v-for="nt in nodeTypes" :key="nt.id" :value="nt.id">{{ nt.name }}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Parent Node (Optional)</label>
            <select v-model="newNode.parent" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1 bg-white">
               <option :value="null">None (Root Level)</option>
               <option v-for="n in filteredNodesForCreation" :key="n.id" :value="n.id">{{ n.full_path }}</option>
            </select>
          </div>
          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="showNodeModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill">Create Node</button>
          </div>
        </form>
      </div>
    </BaseModal>

    <!-- Project Modal -->
    <BaseModal v-model:show="showProjectModal" title="Create Execution Project" @close="showProjectModal = false">
      <div class="p-6">
        <form @submit.prevent="createItem('project', newProject, () => newProject = { name: '', description: '', start_date: '', end_date: '', status: 'active' })" class="flex flex-col gap-4">
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Project Name</label>
            <input type="text" v-model="newProject.name" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required>
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Project Description</label>
            <textarea v-model="newProject.description" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" rows="2"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="form-label text-xs font-black uppercase text-slate-500">Start Date</label>
              <input type="date" v-model="newProject.start_date" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required>
            </div>
            <div class="form-group">
              <label class="form-label text-xs font-black uppercase text-slate-500">End Date (Optional)</label>
              <input type="date" v-model="newProject.end_date" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1">
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="showProjectModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill">Create Project</button>
          </div>
        </form>
      </div>
    </BaseModal>

    <!-- Phase Modal -->
    <BaseModal v-model:show="showPhaseModal" title="Create Project Phase" @close="showPhaseModal = false">
      <div class="p-6">
        <form @submit.prevent="createItem('projectPhase', newPhase, () => newPhase = { name: '', sequence: 1, project: '' })" class="flex flex-col gap-4">
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Parent Project</label>
            <select v-model="newPhase.project" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1 bg-white" required>
               <option value="" disabled>Select Project...</option>
               <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Phase Name</label>
            <input type="text" v-model="newPhase.name" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required placeholder="e.g. Design & Planning">
          </div>
          <div class="form-group">
            <label class="form-label text-xs font-black uppercase text-slate-500">Sequence Number</label>
            <input type="number" v-model="newPhase.sequence" class="form-input w-full p-3 rounded-xl border border-slate-200 mt-1" required>
          </div>
          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="showPhaseModal = false" class="button button--secondary button--pill">Cancel</button>
            <button type="submit" class="button button--primary button--pill">Create Phase</button>
          </div>
        </form>
      </div>
    </BaseModal>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import repositoryApi from '../services/repositoryApi';
import BaseModal from '@/components/Common/BaseModal.vue';

const activeTab = ref('artifact_types');

const artifactTypes = ref([]);
const registries = ref([]);
const nodeTypes = ref([]);
const nodes = ref([]);
const projects = ref([]);
const phases = ref([]);

const showArtifactTypeModal = ref(false);
const showRegistryModal = ref(false);
const showNodeTypeModal = ref(false);
const showNodeModal = ref(false);
const showProjectModal = ref(false);
const showPhaseModal = ref(false);

const newArtifactType = ref({ name: '', code: '', description: '', metadata_schema: {} });
const metadataSchemaInput = ref('');
const newRegistry = ref({ name: '', slug: '', description: '' });
const newNodeType = ref({ name: '', code: '' });
const newNode = ref({ name: '', registry: '', node_type: '', parent: null });
const newProject = ref({ name: '', description: '', start_date: '', end_date: '', status: 'active' });
const newPhase = ref({ name: '', sequence: 1, project: '' });

const filteredNodesForCreation = computed(() => {
    if (!newNode.value.registry) return [];
    return nodes.value.filter(n => n.registry === newNode.value.registry);
});

const autoSlug = () => {
    newRegistry.value.slug = newRegistry.value.name
        .toLowerCase()
        .replace(/[^\w ]+/g, '')
        .replace(/ +/g, '-');
};

const fetchAll = async () => {
    try {
        const [types, regs, nt, prj, phs] = await Promise.all([
            repositoryApi.getArtifactTypes(),
            repositoryApi.getRegistries(),
            repositoryApi.getNodeTypes(),
            repositoryApi.getProjects(),
            repositoryApi.getProjectPhases()
        ]);
        
        artifactTypes.value = types.data.results || types.data;
        registries.value = regs.data.results || regs.data;
        nodeTypes.value = nt.data.results || nt.data;
        projects.value = prj.data.results || prj.data;
        phases.value = phs.data.results || phs.data;
    } catch(err) {
        console.error("Failed to load configs", err);
    }
};

const createItem = async (type, payload, resetFn) => {
    try {
        const methodMap = {
            artifactType: 'createArtifactType',
            registry: 'createRegistry',
            nodeType: 'createNodeType',
            node: 'createNode',
            project: 'createProject',
            projectPhase: 'createProjectPhase'
        };
        
        // Handle special parsing
        if (type === 'artifactType' && metadataSchemaInput.value) {
            try {
                payload.metadata_schema = JSON.parse(metadataSchemaInput.value);
            } catch(e) {
                alert("Invalid JSON in Metadata Schema");
                return;
            }
        }
        
        await repositoryApi[methodMap[type]](payload);
        resetFn();
        if (type === 'artifactType') metadataSchemaInput.value = '';
        
        showArtifactTypeModal.value = false;
        showRegistryModal.value = false;
        showNodeTypeModal.value = false;
        showNodeModal.value = false;
        showProjectModal.value = false;
        showPhaseModal.value = false;
        
        fetchAll();
    } catch(err) {
        const msg = err.response?.data ? JSON.stringify(err.response.data) : `Failed to create ${type}.`;
        alert(`Error: ${msg}`);
    }
};

const deleteItem = async (type, id) => {
    if(confirm(`Are you sure you want to delete this ${type}?`)) {
        try {
            const methodMap = {
                artifactType: 'deleteArtifactType',
                registry: 'deleteRegistry',
                nodeType: 'deleteNodeType',
                node: 'deleteNode',
                project: 'deleteProject',
                projectPhase: 'deleteProjectPhase'
            };
            await repositoryApi[methodMap[type]](id);
            fetchAll();
        } catch(err) {
            alert("Failed to delete. It might be in use by artifacts or nodes.");
        }
    }
};

const getProjectName = (id) => projects.value.find(p => p.id === id)?.name || id;
const getRegistryNameFromNode = (id) => registries.value.find(r => r.id === id)?.name || id;

onMounted(() => {
    fetchAll();
});
</script>
