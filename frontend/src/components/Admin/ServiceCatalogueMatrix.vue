<template>
   <div class="space-y-6">
      <header class="page__header u-mb-8">
         <div class="page__title-group">
            <h1 class="page__title">Whole-of-Government Service Catalogue</h1>
            <p class="page__subtitle">Business Process → Services → Systems → Actors Mapping</p>
         </div>
         <div class="page__actions">
            <button @click="fetchMatrix"
               class="button button--secondary button--small button--pill">
               <i class="bi bi-arrow-clockwise"></i> Refresh Data
            </button>
         </div>
      </header>

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
         <!-- Filters -->
         <div class="toolbar u-mb-8">
            <div class="toolbar__filters">
               <div class="toolbar__filter-group">
                  <i class="bi bi-search toolbar__filter-icon"></i>
                  <input v-model="searchQuery" type="text" placeholder="Search Services..."
                     class="toolbar__filter-input">
               </div>
               
               <!-- Searchable Domain Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-diagram-2 toolbar__filter-icon"></i>
                  <input type="text" v-model="domainSearchLocal" placeholder="Filter by Domain..."
                     @focus="showDomainDropdown = true"
                     @blur="setTimeout(() => showDomainDropdown = false, 200)"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow" style="cursor: pointer">
                  <i class="bi bi-chevron-down toolbar__filter-arrow" :class="{'toolbar__filter-arrow--open': showDomainDropdown}"></i>
                  
                  <div v-if="showDomainDropdown" class="u-absolute u-top-full u-left-0 u-w-full bg-white u-border u-shadow-xl u-rounded-lg u-mt-2 u-z-dropdown u-overflow-auto u-p-2" style="max-height: 240px">
                     <div @click="selectDomain('')" class="u-p-3 hover:bg-bg-page u-rounded u-font-bold u-text-primary u-mb-1" style="cursor: pointer">All Domains</div>
                     <div v-for="d in filteredDomains" :key="d" @click="selectDomain(d)"
                        class="u-p-3 hover:bg-bg-page u-rounded u-flex u-items-center u-gap-3 u-font-medium transition-colors" style="cursor: pointer; font-size: 14px">
                        {{ d }}
                     </div>
                  </div>
               </div>

               <!-- Searchable MDA Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-building toolbar__filter-icon"></i>
                  <input type="text" v-model="mdaSearchLocal" placeholder="Filter by Agency (MDA)..."
                     @focus="showMdaDropdown = true"
                     @blur="setTimeout(() => showMdaDropdown = false, 200)"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow" style="cursor: pointer">
                  <i class="bi bi-chevron-down toolbar__filter-arrow" :class="{'toolbar__filter-arrow--open': showMdaDropdown}"></i>
                  
                  <div v-if="showMdaDropdown" class="u-absolute u-top-full u-left-0 u-w-full bg-white u-border u-shadow-xl u-rounded-lg u-mt-2 u-z-dropdown u-overflow-auto u-p-2" style="max-height: 240px">
                     <div @click="selectMda('')" class="u-p-3 hover:bg-bg-page u-rounded u-font-bold u-text-primary u-mb-1" style="cursor: pointer">All Agencies</div>
                     <div v-for="m in filteredMdas" :key="m" @click="selectMda(m)"
                        class="u-p-3 hover:bg-bg-page u-rounded u-flex u-items-center u-gap-3 u-font-medium transition-colors" style="cursor: pointer; font-size: 14px">
                        {{ m }}
                     </div>
                  </div>
               </div>

               <div class="u-flex u-items-end">
                  <button @click="resetFilters"
                     class="button button--secondary u-w-full">
                     Reset Filters
                  </button>
               </div>
            </div>
         </div>

         <div v-for="domain in filteredMatrixData" :key="domain.domain_name"
            class="card u-overflow-hidden u-mb-8">
            <header class="card__header u-justify-between u-items-center" style="background: var(--color-background-hover); border-bottom: 1px solid var(--color-border);">
               <h3 class="card__title u-flex u-items-center u-gap-2">
                  <span class="u-block u-rounded-full" style="width: 0.5rem; height: 2rem; background: var(--color-primary);"></span>
                  {{ domain.domain_name }}
               </h3>
               <span class="table__code-badge">Domain</span>
            </header>

            <div class="u-p-6">
               <div v-for="process in domain.processes" :key="process.process_name" class="u-mb-8 last:u-mb-0">
                  <div class="u-mb-4">
                     <h4 class="u-flex u-items-center u-gap-2 u-text-primary u-font-bold">
                        <i class="bi bi-diagram-3"></i>
                        {{ process.process_name }}
                     </h4>
                     <p class="u-text-xs u-text-muted u-ml-7">Business Process</p>
                  </div>

                  <div class="table-container u-ml-7 u-border u-rounded">
                     <table class="table">
                        <thead>
                           <tr class="table__header-row">
                              <th class="table__header-cell" style="padding-left: 1rem;">Service Name</th>
                              <th class="table__header-cell">Type / Maturity</th>
                              <th class="table__header-cell">Complexity / Channels</th>
                              <th class="table__header-cell">Pain Points</th>
                              <th class="table__header-cell">Workflow Config</th>
                              <th class="table__header-cell table__header-cell--align-right" style="padding-right: 1rem;">Actions</th>
                           </tr>
                        </thead>
                        <tbody>
                           <tr v-for="service in process.services" :key="service.service_name"
                              class="table__row">
                              <td class="table__cell" style="padding-left: 1rem;">
                                 <div class="table__cell--bold">{{ service.service_name }}</div>
                                 <div class="u-text-xs u-text-muted u-mt-0.5">{{ service.mda }}</div>
                              </td>
                              <td class="table__cell">
                                 <div class="u-flex u-flex-col u-gap-1">
                                    <span class="u-text-xs u-font-bold u-text-primary">{{ service.service_type || 'N/A' }}</span>
                                    <div class="u-flex u-items-center u-gap-1">
                                       <div class="u-flex u-gap-0.5">
                                          <template v-for="i in 5" :key="i">
                                             <div :class="i <= service.maturity ? 'u-text-success' : 'u-text-muted'"
                                                class="u-block u-rounded-full" style="width: 0.625rem; height: 0.25rem; background: currentColor;"></div>
                                          </template>
                                       </div>
                                       <span class="u-text-xs u-text-muted">Level {{ service.maturity }}</span>
                                    </div>
                                 </div>
                              </td>
                              <td class="table__cell">
                                 <div class="u-flex u-flex-col u-gap-1">
                                    <span class="u-text-xs">{{ service.process_complexity || 'Normal' }}</span>
                                    <div class="u-flex u-flex-wrap u-gap-1">
                                       <span v-for="ch in service.delivery_channels" :key="ch"
                                          class="table__code-badge" style="font-size: 10px; padding: 2px 6px;">
                                          {{ ch }}
                                       </span>
                                    </div>
                                 </div>
                              </td>
                              <td class="table__cell">
                                 <div class="u-flex u-flex-wrap u-gap-1" style="max-width: 200px">
                                    <span v-for="pp in service.pain_points" :key="pp"
                                       class="badge badge--danger" style="font-size: 10px; padding: 2px 6px;">
                                       {{ pp }}
                                    </span>
                                    <span v-if="!service.pain_points || service.pain_points.length === 0"
                                       class="u-text-muted u-text-xs" style="font-style: italic">None reported</span>
                                 </div>
                              </td>
                              <td class="table__cell">
                                 <span v-if="service.workflow_configured"
                                    class="badge badge--success">
                                    Active
                                 </span>
                                 <span v-else
                                    class="badge badge--danger">
                                    Missing
                                 </span>
                              </td>
                              <td class="table__cell table__cell--align-right" style="padding-right: 1rem;">
                                 <button v-if="service.workflow_configured" @click="visualizeWorkflow(service)"
                                    class="button button--secondary button--small" style="font-size: 10px; padding: 4px 8px;">
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
      <BaseModal :show="showWorkflowModal" 
                 @close="closeWorkflowModal" 
                 size="full"
                 headerClass="modal__header--dark">
         <template #header>
            <div class="u-flex-1">
               <h3 class="modal__title">{{ selectedService?.service_name }}</h3>
               <p class="modal__subtitle u-font-mono u-uppercase" style="letter-spacing: 0.1em">BPMN 2.0 Process Orchestration Model</p>
            </div>

            <div class="tab-bar" style="background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.1)">
               <button @click="switchStage('as_is')"
                  :class="{'tab-bar__item--active': activeLifecycle === 'as_is'}"
                  class="tab-bar__item u-text-xs u-py-1.5" style="border: none">
                  As-Is
               </button>
               <button @click="switchStage('to_be')"
                  :class="{'tab-bar__item--active': activeLifecycle === 'to_be'}"
                  class="tab-bar__item u-text-xs u-py-1.5" style="border: none">
                  To-Be
               </button>
            </div>
         </template>

         <div class="u-mb-6 u-flex u-items-center u-justify-center u-gap-6">
            <div class="u-flex u-items-center u-gap-2">
               <span class="u-block u-rounded-full" style="width: 0.75rem; height: 0.75rem; background: var(--color-success);"></span>
               <span class="u-text-xs u-font-bold u-text-muted u-uppercase">Start</span>
            </div>
            <div class="u-flex u-items-center u-gap-2">
               <span class="u-block u-rounded" style="width: 0.75rem; height: 0.75rem; background: var(--color-primary);"></span>
               <span class="u-text-xs u-font-bold u-text-muted u-uppercase">User Task</span>
            </div>
            <div class="u-flex u-items-center u-gap-2">
               <span class="u-block u-rounded u-border" style="width: 0.75rem; height: 0.75rem; border-color: var(--color-info); border-style: dashed; border-width: 2px"></span>
               <span class="u-text-xs u-font-bold u-text-muted u-uppercase">Service Task</span>
            </div>
            <div class="u-flex u-items-center u-gap-2">
               <div class="u-block u-border" style="width: 0.8rem; height: 0.8rem; border-color: var(--color-warning); border-width: 2px; transform: rotate(45deg)"></div>
               <span class="u-text-xs u-font-bold u-text-muted u-uppercase">Gateway</span>
            </div>
            <div class="u-flex u-items-center u-gap-2">
               <span class="u-block u-rounded-full" style="width: 0.75rem; height: 0.75rem; background: var(--color-danger);"></span>
               <span class="u-text-xs u-font-bold u-text-muted u-uppercase">End</span>
            </div>
         </div>
         
         <div class="mermaid u-flex u-justify-center" ref="mermaidContainer">
            {{ mermaidDefinition }}
         </div>

         <template #footer>
            <div class="u-text-xs u-text-muted u-font-mono" style="font-style: italic">
               Mapping Level: {{ activeLifecycle === 'to_be' ? 'Optimized digital flow' : 'Documented current state' }}
            </div>
            <button @click="closeWorkflowModal" class="button button--secondary button--pill">
               Close Model
            </button>
         </template>
      </BaseModal>
   </div>
</template>

<script setup>
   import { ref, onMounted, computed, nextTick } from 'vue';
   import api from '../../services/api';
   import mermaid from 'mermaid';
   import { useServiceConfigStore } from '../../store/serviceConfig';
   import WogDashboardStats from './WogDashboardStats.vue';
   import BaseModal from '../Common/BaseModal.vue';

   const serviceConfigStore = useServiceConfigStore();
   const matrixData = ref([]);
   const auditStats = computed(() => serviceConfigStore.catalogueSummary);
   const loading = ref(true);
   const error = ref(null);

   const searchQuery = ref('');
   const selectedDomain = ref('');
   const selectedMda = ref('');
   
   const domainSearchLocal = ref('');
   const mdaSearchLocal = ref('');
   const showDomainDropdown = ref(false);
   const showMdaDropdown = ref(false);
   
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

   const filteredDomains = computed(() => {
      if (!domainSearchLocal.value) return domainsList.value;
      const q = domainSearchLocal.value.toLowerCase();
      return domainsList.value.filter(d => d.toLowerCase().includes(q));
   });

   const filteredMdas = computed(() => {
      if (!mdaSearchLocal.value) return mdaList.value;
      const q = mdaSearchLocal.value.toLowerCase();
      return mdaList.value.filter(m => m.toLowerCase().includes(q));
   });

   const selectDomain = (domain) => {
      selectedDomain.value = domain;
      domainSearchLocal.value = domain;
      showDomainDropdown.value = false;
   };

   const selectMda = (mda) => {
      selectedMda.value = mda;
      mdaSearchLocal.value = mda;
      showMdaDropdown.value = false;
   };

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
      domainSearchLocal.value = '';
      mdaSearchLocal.value = '';
   };

   onMounted(() => {
      mermaid.initialize({ startOnLoad: false, theme: 'default' });
      fetchMatrix();
   });
</script>
