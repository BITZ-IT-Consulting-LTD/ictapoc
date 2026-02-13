<template>
   <div class="space-y-6">
      <div class="flex justify-between items-center">
         <div>
            <h2 class="text-2xl font-bold text-gray-900">Whole-of-Government Service Catalogue</h2>
            <p class="text-sm text-gray-500">Business Process → Services → Systems → Actors Mapping</p>
         </div>
         <div>
            <button @click="fetchMatrix"
               class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">
               Refresh Data
            </button>
         </div>
      </div>

      <div v-if="loading" class="text-center py-12">
         <svg class="animate-spin h-8 w-8 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
               d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
         </svg>
         <p class="mt-2 text-gray-500">Loading catalogue matrix...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
         <p>{{ error }}</p>
         <button @click="fetchMatrix" class="mt-2 text-sm underline hover:text-red-800">Try Again</button>
      </div>

      <div v-else class="space-y-8">
         <!-- Whole-of-Government Mini Dashboard -->
         <WogDashboardStats v-if="auditStats" :stats="auditStats" />

         <!-- Filters -->
         <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div>
               <label class="block text-xs font-semibold text-gray-500 mb-1">Search Services</label>
               <input v-model="searchQuery" type="text" placeholder="e.g. Passport"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            <div>
               <label class="block text-xs font-semibold text-gray-500 mb-1">Filter by Domain</label>
               <select v-model="selectedDomain"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500">
                  <option value="">All Domains</option>
                  <option v-for="d in domainsList" :key="d" :value="d">{{ d }}</option>
               </select>
            </div>
            <div>
               <label class="block text-xs font-semibold text-gray-500 mb-1">Filter by Agency (MDA)</label>
               <select v-model="selectedMda"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500">
                  <option value="">All Agencies</option>
                  <option v-for="m in mdaList" :key="m" :value="m">{{ m }}</option>
               </select>
            </div>
            <div class="self-end">
               <button @click="resetFilters"
                  class="w-full px-4 py-2 bg-white border border-gray-300 text-gray-600 rounded-md text-sm hover:bg-gray-50 transition-colors">Reset
                  Filters</button>
            </div>
         </div>

         <div v-for="domain in filteredMatrixData" :key="domain.domain_name"
            class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
               <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                  <span class="w-2 h-8 bg-indigo-600 rounded-full"></span>
                  {{ domain.domain_name }}
               </h3>
               <span
                  class="text-xs font-mono bg-white border border-gray-300 px-2 py-1 rounded text-gray-500">Domain</span>
            </div>

            <div class="divide-y divide-gray-100">
               <div v-for="process in domain.processes" :key="process.process_name" class="p-6">
                  <div class="mb-4">
                     <h4 class="text-md font-semibold text-indigo-700 flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10">
                           </path>
                        </svg>
                        {{ process.process_name }}
                     </h4>
                     <p class="text-xs text-gray-400 ml-7">Business Process</p>
                  </div>

                  <div class="ml-7 overflow-x-auto">
                     <table class="min-w-full divide-y divide-gray-200 border border-gray-100 rounded-lg">
                        <thead class="bg-gray-50">
                           <tr>
                              <th scope="col"
                                 class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 Service Name</th>
                              <th scope="col"
                                 class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 Type / Maturity</th>
                              <th scope="col"
                                 class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 Complexity / Channels</th>
                              <th scope="col"
                                 class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 Pain Points</th>
                              <th scope="col"
                                 class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 Workflow Config</th>
                              <th scope="col"
                                 class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 Actions</th>
                           </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                           <tr v-for="service in process.services" :key="service.service_name"
                              class="hover:bg-gray-50 transition-colors">
                              <td class="px-4 py-3 text-sm">
                                 <div class="font-medium text-gray-900">{{ service.service_name }}</div>
                                 <div class="text-[10px] text-gray-400 mt-0.5">{{ service.mda }}</div>
                                 <div v-if="service.description"
                                    class="text-[10px] text-gray-500 mt-1 italic line-clamp-1"
                                    :title="service.description">{{ service.description }}</div>
                              </td>
                              <td class="px-4 py-3 text-sm text-gray-500">
                                 <div class="flex flex-col gap-1">
                                    <span class="text-xs font-semibold text-indigo-600">{{ service.service_type || 'N/A'
                                       }}</span>
                                    <div class="flex items-center gap-1">
                                       <div class="flex gap-0.5">
                                          <template v-for="i in 5" :key="i">
                                             <div :class="i <= service.maturity ? 'bg-green-500' : 'bg-gray-200'"
                                                class="w-2.5 h-1 rounded-full"></div>
                                          </template>
                                       </div>
                                       <span class="text-[10px] text-gray-400">Level {{ service.maturity }}</span>
                                    </div>
                                 </div>
                              </td>
                              <td class="px-4 py-3 text-sm text-gray-500">
                                 <div class="flex flex-col gap-1">
                                    <span class="text-xs">{{ service.process_complexity || 'Normal' }}</span>
                                    <div class="flex flex-wrap gap-1">
                                       <span v-for="ch in service.delivery_channels" :key="ch"
                                          class="px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded text-[10px]">
                                          {{ ch }}
                                       </span>
                                    </div>
                                 </div>
                              </td>
                              <td class="px-4 py-3 text-sm text-gray-500">
                                 <div class="flex flex-wrap gap-1 max-w-[200px]">
                                    <span v-for="pp in service.pain_points" :key="pp"
                                       class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-red-50 text-red-700 border border-red-100">
                                       {{ pp }}
                                    </span>
                                    <span v-if="!service.pain_points || service.pain_points.length === 0"
                                       class="text-gray-400 italic text-[10px]">None reported</span>
                                 </div>
                              </td>
                              <td class="px-4 py-3 text-sm">
                                 <span v-if="service.workflow_configured"
                                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                    <svg class="mr-1.5 h-2 w-2 text-green-400" fill="currentColor" viewBox="0 0 8 8">
                                       <circle cx="4" cy="4" r="3" />
                                    </svg>
                                    Active
                                 </span>
                                 <span v-else
                                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200">
                                    <svg class="mr-1.5 h-2 w-2 text-red-400" fill="currentColor" viewBox="0 0 8 8">
                                       <circle cx="4" cy="4" r="3" />
                                    </svg>
                                    Missing
                                 </span>
                              </td>
                              <td class="px-4 py-3 text-right text-sm">
                                 <button v-if="service.workflow_configured" @click="visualizeWorkflow(service)"
                                    class="text-indigo-600 hover:text-indigo-900 font-bold text-[10px] uppercase tracking-wider border border-indigo-200 px-3 py-1.5 rounded-lg hover:bg-indigo-50 transition-all shadow-sm">
                                    BPMN Model
                                 </button>
                              </td>
                           </tr>
                        </tbody>
                     </table>
                  </div>
               </div>
            </div>
         </div>

         <div v-if="matrixData.length === 0"
            class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
            <p class="text-gray-500">No catalogue data found. Please run the seeding script.</p>
         </div>
      </div>

      <!-- Workflow Modal -->
      <Teleport to="body">
         <div v-if="showWorkflowModal"
            class="fixed inset-0 z-[9999] overflow-y-auto h-full w-full flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm">
            <div
               class="relative mx-auto p-0 border w-full max-w-5xl shadow-2xl rounded-2xl bg-white transform transition-all scale-100 overflow-hidden flex flex-col max-h-[90vh]">
               <div
                  class="bg-indigo-900 px-6 py-4 flex flex-col md:flex-row justify-between items-center text-white gap-4">
                  <div>
                     <h3 class="text-xl font-bold">{{ selectedService?.service_name }}</h3>
                     <p class="text-xs text-indigo-200 font-mono tracking-widest uppercase mt-0.5">BPMN 2.0 Process
                        Orchestration Model</p>
                  </div>

                  <div class="flex bg-indigo-950/50 p-1 rounded-lg border border-indigo-700">
                     <button @click="switchStage('as_is')"
                        :class="activeLifecycle === 'as_is' ? 'bg-indigo-600 text-white' : 'text-indigo-300 hover:text-white'"
                        class="px-4 py-1.5 rounded-md text-xs font-bold transition-all uppercase tracking-tighter">
                        As-Is Model
                     </button>
                     <button @click="switchStage('to_be')"
                        :class="activeLifecycle === 'to_be' ? 'bg-indigo-600 text-white' : 'text-indigo-300 hover:text-white'"
                        class="px-4 py-1.5 rounded-md text-xs font-bold transition-all uppercase tracking-tighter">
                        To-Be (Optimized)
                     </button>
                  </div>

                  <button @click="closeWorkflowModal"
                     class="text-white hover:text-gray-200 absolute top-4 right-4 md:static">
                     <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                     </svg>
                  </button>
               </div>
               <div class="flex-1 p-8 bg-slate-50 overflow-auto border-b border-gray-100">
                  <div class="mb-4 flex items-center justify-center gap-6">
                     <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-green-500"></span><span
                           class="text-[10px] uppercase font-bold text-gray-400">Start</span></div>
                     <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-md bg-blue-500"></span><span
                           class="text-[10px] uppercase font-bold text-gray-400">User Task</span></div>
                     <div class="flex items-center gap-2"><span
                           class="w-3 h-3 rounded-md border-2 border-dashed border-purple-500"></span><span
                           class="text-[10px] uppercase font-bold text-gray-400">Service Task</span></div>
                     <div class="flex items-center gap-2"><span
                           class="w-4 h-4 rotate-45 border-2 border-orange-500"></span><span
                           class="text-[10px] uppercase font-bold text-gray-400">Gateway</span></div>
                     <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-red-500"></span><span
                           class="text-[10px] uppercase font-bold text-gray-400">End</span></div>
                  </div>
                  <div class="mermaid flex justify-center" ref="mermaidContainer">
                     {{ mermaidDefinition }}
                  </div>
               </div>
               <div class="bg-white px-6 py-4 flex justify-between items-center sticky bottom-0">
                  <div class="text-[10px] text-gray-400 font-mono italic">
                     Mapping Level: {{ activeLifecycle === 'to_be' ? 'Optimized digital flow' : 'Documented current state' }}
                  </div>
                  <button @click="closeWorkflowModal"
                     class="px-6 py-2 bg-gray-900 text-white rounded-lg hover:bg-black font-bold text-xs uppercase tracking-widest transition-all">Close
                     Model</button>
               </div>
            </div>
         </div>
      </Teleport>
   </div>
</template>

<script setup>
   import { ref, onMounted, computed, nextTick } from 'vue';
   import api from '../../services/api';
   import mermaid from 'mermaid';
   import { useServiceConfigStore } from '../../store/serviceConfig';
   import WogDashboardStats from './WogDashboardStats.vue';

   const serviceConfigStore = useServiceConfigStore();
   const matrixData = ref([]);
   const auditStats = computed(() => serviceConfigStore.catalogueSummary);
   const loading = ref(true);
   const error = ref(null);

   const searchQuery = ref('');
   const selectedDomain = ref('');
   const selectedMda = ref('');
   const activeLifecycle = ref('as_is'); // Default to showing current manual process friction

   const showWorkflowModal = ref(false);
   const selectedService = ref(null);
   const mermaidDefinition = ref('');
   const mermaidContainer = ref(null);

   const domainsList = computed(() => [...new Set(matrixData.value.map(d => d.domain_name))]);
   const mdaList = computed(() => {
      const mdas = new Set();
      matrixData.value.forEach(d => {
         d.processes.forEach(p => {
            p.services.forEach(s => mdas.add(s.mda));
         });
      });
      return [...mdas].sort();
   });

   const filteredMatrixData = computed(() => {
      let data = JSON.parse(JSON.stringify(matrixData.value));

      if (selectedDomain.value) {
         data = data.filter(d => d.domain_name === selectedDomain.value);
      }

      // Apply MDA and Search Filters
      data = data.map(d => {
         const matchingProcesses = d.processes.map(p => {
            const matchingServices = p.services.filter(s => {
               const matchesMda = !selectedMda.value || s.mda === selectedMda.value;
               const matchesSearch = !searchQuery.value ||
                  s.service_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                  s.mda.toLowerCase().includes(searchQuery.value.toLowerCase());
               return matchesMda && matchesSearch;
            });

            if (matchingServices.length > 0) {
               return { ...p, services: matchingServices };
            }
            return null;
         }).filter(p => p !== null);

         if (matchingProcesses.length > 0) {
            return { ...d, processes: matchingProcesses };
         }
         return null;
      }).filter(d => d !== null);

      return data;
   });

   const fetchMatrix = async () => {
      loading.value = true;
      error.value = null;
      try {
         const response = await api.get('/catalog/services/process_matrix/');
         matrixData.value = response.data;

         // Use Global Store for Stats
         await serviceConfigStore.fetchCatalogueSummary();

      } catch (err) {
         console.error('Failed to fetch matrix:', err);
         error.value = 'Failed to load catalogue data.';
      } finally {
         loading.value = false;
      }
   };

   const visualizeWorkflow = async (service, stage = 'as_is') => {
      selectedService.value = service;
      activeLifecycle.value = stage;
      showWorkflowModal.value = true;

      // Generate Mermaid Graph
      let graph = 'graph TD;\n';
      // Filter steps by active lifecycle stage
      let steps = (service.workflow_steps || []).filter(s => s.lifecycle_stage === activeLifecycle.value);

      // Fallback if no steps for selected stage
      if (steps.length === 0 && service.workflow_steps?.length > 0) {
         steps = service.workflow_steps.filter(s => s.lifecycle_stage === 'as_is');
         activeLifecycle.value = 'as_is';
      }

      steps.forEach((step, index) => {
         const nodeId = `S${step.sequence}`;
         const safeLabel = step.step_name.replace(/"/g, "'");
         let bType = step.bpmn_element_type || 'user_task';

         if (bType === 'start_event') {
            graph += `    ${nodeId}(("${safeLabel}"))\n`;
            graph += `    class ${nodeId} startEvent;\n`;
         } else if (bType === 'end_event') {
            graph += `    ${nodeId}(("${safeLabel}"))\n`;
            graph += `    class ${nodeId} endEvent;\n`;
         } else if (bType === 'exclusive_gateway') {
            graph += `    ${nodeId}{{"${safeLabel}"}}\n`;
            graph += `    class ${nodeId} gateway;\n`;
         } else if (bType === 'service_task') {
            graph += `    ${nodeId}[["${safeLabel}<br/>(System)"]]\n`;
            graph += `    class ${nodeId} serviceTask;\n`;
         } else {
            graph += `    ${nodeId}["${safeLabel}<br/>(${step.role})"]\n`;
            graph += `    class ${nodeId} userTask;\n`;
         }

         if (index < steps.length - 1) {
            const nextStep = steps[index + 1];
            const nextNodeId = `S${nextStep.sequence}`;
            graph += `    ${nodeId} --> ${nextNodeId}\n`;
         }
      });

      if (steps.length === 0) {
         graph += '    Start((No steps for this stage)) --> End((End))\n';
      }

      graph += '    classDef startEvent fill:#f0fdf4,stroke:#16a34a,stroke-width:4px;\n';
      graph += '    classDef endEvent fill:#fef2f2,stroke:#dc2626,stroke-width:4px;\n';
      graph += '    classDef gateway fill:#fff7ed,stroke:#c2410c,stroke-width:2px;\n';
      graph += '    classDef userTask fill:#eff6ff,stroke:#2563eb,stroke-width:2px;\n';
      graph += '    classDef serviceTask fill:#faf5ff,stroke:#7c3aed,stroke-width:2px,stroke-dasharray: 5 5;\n';

      mermaidDefinition.value = graph;

      await nextTick();
      if (mermaidContainer.value) {
         mermaidContainer.value.removeAttribute('data-processed');
         mermaidContainer.value.innerHTML = graph;
         try {
            await mermaid.run({
               nodes: [mermaidContainer.value]
            });
         } catch (e) {
            console.error('Mermaid error', e);
         }
      }
   };

   const switchStage = (stage) => {
      visualizeWorkflow(selectedService.value, stage);
   };

   const closeWorkflowModal = () => {
      showWorkflowModal.value = false;
      selectedService.value = null;
   };

   const resetFilters = () => {
      searchQuery.value = '';
      selectedDomain.value = '';
      selectedMda.value = '';
   };

   onMounted(() => {
      mermaid.initialize({ startOnLoad: false, theme: 'default' });
      fetchMatrix();
   });
</script>
