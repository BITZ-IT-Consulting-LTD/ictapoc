<template>
   <div class="space-y-6">
      <header class="page__header u-mb-8">
         <div class="page__title-group">
            <div class="u-flex u-items-center u-gap-3 u-mb-2">
               <span class="badge badge--primary u-font-mono u-text-[10px] u-tracking-widest">Active Governance Module</span>
               <span class="u-text-[10px] u-font-black u-text-muted/60 u-tracking-widest">SECURITY: GOK-ADMIN-01</span>
            </div>
            <h1 class="page__title">
               {{ activeTab === 'Priority MDAs' ? 'Priority MDAs Service Matrix' :
                  activeTab === 'Priority Services' ? 'High-Impact Priority Services Matrix' :
                  activeTab === 'Cradle to Death' ? 'Cradle to Death Lifecycle Matrix' :
                  'Whole-of-Government Service Catalogue' }}
            </h1>
            <p class="page__subtitle">
               {{ activeTab === 'Cradle to Death' ? 'From Birth Registration to Probate & Succession' :
                  'Cluster → Service Family → Services → Systems → Actors Mapping' }}
            </p>
         </div>
         <div class="page__actions">
            <button @click="fetchMatrix" class="button button--secondary button--small button--pill no-print">
               <i class="bi bi-arrow-clockwise"></i> Refresh Data
            </button>
            <button @click="printCatalogue" class="button button--primary button--small button--pill no-print ml-2">
               <i class="bi bi-printer"></i> Print Report
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
         <WogDashboardStats v-if="auditStats" :stats="auditStats" class="print-section" />

         <!-- Print Only Header -->
         <div class="print-only u-mb-10 u-border-b-4 u-border-slate-900 u-pb-6">
            <h1 class="u-text-4xl u-font-black">National Service Registry</h1>
            <p class="u-text-xl u-font-bold u-mt-2">Whole-of-Government Governance Catalogue Matrix</p>
            <div class="u-flex u-justify-between u-mt-4 u-text-sm u-font-bold">
               <span>Generated: {{ new Date().toLocaleDateString() }}</span>
               <span>Classification: OFFICIAL / SENSITIVE</span>
            </div>
         </div>

         <!-- Filters -->
         <div class="toolbar u-mb-6 no-print">
            <div class="toolbar__filters">
               <!-- Search Core -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-search toolbar__filter-icon"></i>
                  <input v-model="searchQuery" type="text" placeholder="Search Services..."
                     class="toolbar__filter-input">
                  <i v-if="searchQuery" @click="searchQuery = ''" class="bi bi-x-circle-fill toolbar__clear-icon"></i>
               </div>

               <!-- Searchable Family Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-diagram-3 toolbar__filter-icon"></i>
                  <input type="text" v-model="domainSearchLocal" placeholder="Filter by Family..."
                     @focus="showDomainDropdown = true" @blur="closeDropdownWithDelay('domain')"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow">
                  <i class="bi bi-chevron-down toolbar__filter-arrow"
                     :class="{ 'toolbar__filter-arrow--open': showDomainDropdown }"></i>
                  <i v-if="selectedDomain" @click="selectDomain('')"
                     class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                  <transition name="dropdown">
                     <div v-if="showDomainDropdown" class="dropdown-menu">
                        <div @click="selectDomain('')" class="dropdown-item dropdown-item--header">All Families</div>
                        <div v-for="d in filteredDomains" :key="d" @click="selectDomain(d)" class="dropdown-item">
                           {{ d }}
                        </div>
                     </div>
                  </transition>
               </div>

               <!-- Searchable MDA Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-building toolbar__filter-icon"></i>
                  <input type="text" v-model="mdaSearchLocal" placeholder="Filter by Agency..."
                     @focus="showMdaDropdown = true" @blur="closeDropdownWithDelay('mda')"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow">
                  <i class="bi bi-chevron-down toolbar__filter-arrow"
                     :class="{ 'toolbar__filter-arrow--open': showMdaDropdown }"></i>
                  <i v-if="selectedMda" @click="selectMda('')"
                     class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                  <transition name="dropdown">
                     <div v-if="showMdaDropdown" class="dropdown-menu">
                        <div @click="selectMda('')" class="dropdown-item dropdown-item--header">All Agencies</div>
                        <div v-for="m in filteredMdas" :key="m" @click="selectMda(m)" class="dropdown-item">
                           {{ m }}
                        </div>
                     </div>
                  </transition>
               </div>

               <!-- Searchable Life Event Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-calendar-event toolbar__filter-icon"></i>
                  <input type="text" v-model="lifeEventSearchLocal" placeholder="Filter by Life Event..."
                     @focus="showLifeEventDropdown = true" @blur="closeDropdownWithDelay('lifeEvent')"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow">
                  <i class="bi bi-chevron-down toolbar__filter-arrow"
                     :class="{ 'toolbar__filter-arrow--open': showLifeEventDropdown }"></i>
                  <i v-if="selectedLifeEvent" @click="selectLifeEvent('')"
                     class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                  <transition name="dropdown">
                     <div v-if="showLifeEventDropdown" class="dropdown-menu">
                        <div @click="selectLifeEvent('')" class="dropdown-item dropdown-item--header">All Life Events
                        </div>
                        <div v-for="e in filteredLifeEvents" :key="e" @click="selectLifeEvent(e)" class="dropdown-item">
                           {{ e }}
                        </div>
                     </div>
                  </transition>
               </div>

               <!-- Type Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-tag-fill toolbar__filter-icon"></i>
                  <input type="text" v-model="typeSearchLocal" placeholder="Filter by Type..."
                     @focus="showTypeDropdown = true" @blur="closeDropdownWithDelay('type')"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow">
                  <i class="bi bi-chevron-down toolbar__filter-arrow"
                     :class="{ 'toolbar__filter-arrow--open': showTypeDropdown }"></i>
                  <i v-if="selectedType" @click="selectType('')"
                     class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                  <transition name="dropdown">
                     <div v-if="showTypeDropdown" class="dropdown-menu">
                        <div @click="selectType('')" class="dropdown-item dropdown-item--header">All Types</div>
                        <div v-for="t in filteredTypes" :key="t" @click="selectType(t)" class="dropdown-item">
                           {{ t }}
                        </div>
                     </div>
                  </transition>
               </div>

               <!-- Group Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-collection-fill toolbar__filter-icon"></i>
                  <input type="text" v-model="groupSearchLocal" placeholder="Filter by Group..."
                     @focus="showGroupDropdown = true" @blur="closeDropdownWithDelay('group')"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow">
                  <i class="bi bi-chevron-down toolbar__filter-arrow"
                     :class="{ 'toolbar__filter-arrow--open': showGroupDropdown }"></i>
                  <i v-if="selectedGroup" @click="selectGroup('')"
                     class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                  <transition name="dropdown">
                     <div v-if="showGroupDropdown" class="dropdown-menu">
                        <div @click="selectGroup('')" class="dropdown-item dropdown-item--header">All Lifecycle Groups
                        </div>
                        <div v-for="g in filteredGroups" :key="g" @click="selectGroup(g)" class="dropdown-item">
                           {{ g }}
                        </div>
                     </div>
                  </transition>
               </div>

               <!-- Searchable Category Filter -->
               <div class="toolbar__filter-group">
                  <i class="bi bi-tag toolbar__filter-icon"></i>
                  <input type="text" v-model="categorySearchLocal" placeholder="Filter by Category..."
                     @focus="showCategoryDropdown = true" @blur="closeDropdownWithDelay('category')"
                     class="toolbar__filter-input toolbar__filter-input--with-arrow">
                  <i class="bi bi-chevron-down toolbar__filter-arrow"
                     :class="{ 'toolbar__filter-arrow--open': showCategoryDropdown }"></i>
                  <i v-if="selectedCategory" @click="selectCategory('')"
                     class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                  <transition name="dropdown">
                     <div v-if="showCategoryDropdown" class="dropdown-menu">
                        <div @click="selectCategory('')" class="dropdown-item dropdown-item--header">All Categories
                        </div>
                        <div v-for="c in filteredCategories" :key="c" @click="selectCategory(c)" class="dropdown-item">
                           {{ c }}
                        </div>
                     </div>
                  </transition>
               </div>

               <!-- Reset Action -->
               <button v-if="isAnyFilterActive" @click="resetFilters" class="btn-reset">
                  <i class="bi bi-arrow-counterclockwise"></i>
                  <span>Reset</span>
               </button>
            </div>
         </div>

         <!-- Active Filter Chips -->
         <transition-group name="list" tag="div" class="u-flex u-flex-wrap u-gap-2 u-mb-8">
            <div v-if="searchQuery" :key="'s-' + searchQuery" class="filter-chip" @click="searchQuery = ''">
               <span class="filter-chip__label">Search:</span>
               <span class="filter-chip__value">{{ searchQuery }}</span>
               <i class="bi bi-x"></i>
            </div>
            <div v-if="selectedDomain" :key="'d-' + selectedDomain" class="filter-chip" @click="selectDomain('')">
               <span class="filter-chip__label">Family:</span>
               <span class="filter-chip__value">{{ selectedDomain }}</span>
               <i class="bi bi-x"></i>
            </div>
            <div v-if="selectedMda" :key="'m-' + selectedMda" class="filter-chip" @click="selectMda('')">
               <span class="filter-chip__label">MDA:</span>
               <span class="filter-chip__value">{{ selectedMda }}</span>
               <i class="bi bi-x"></i>
            </div>
            <div v-if="selectedLifeEvent" :key="'l-' + selectedLifeEvent" class="filter-chip"
               @click="selectedLifeEvent = ''">
               <span class="filter-chip__label">Event:</span>
               <span class="filter-chip__value">{{ selectedLifeEvent }}</span>
               <i class="bi bi-x"></i>
            </div>
            <div v-if="selectedType" :key="'t-' + selectedType" class="filter-chip" @click="selectedType = ''">
               <span class="filter-chip__label">Type:</span>
               <span class="filter-chip__value">{{ selectedType }}</span>
               <i class="bi bi-x"></i>
            </div>
            <div v-if="selectedGroup" :key="'g-' + selectedGroup" class="filter-chip" @click="selectedGroup = ''">
               <span class="filter-chip__label">Group:</span>
               <span class="filter-chip__value">{{ selectedGroup }}</span>
               <i class="bi bi-x"></i>
            </div>
            <div v-if="selectedCategory" :key="'c-' + selectedCategory" class="filter-chip" @click="selectCategory('')">
               <span class="filter-chip__label">Category:</span>
               <span class="filter-chip__value">{{ selectedCategory }}</span>
               <i class="bi bi-x"></i>
            </div>
         </transition-group>

         <div v-for="domain in filteredMatrixData" :key="domain.domain_name"
            class="card u-overflow-hidden u-mb-8 print-section">
            <header class="card__header u-justify-between u-items-center"
               style="background: var(--color-background-hover); border-bottom: 1px solid var(--color-border);">
               <h3 class="card__title u-flex u-items-center u-gap-2">
                  <span class="u-block u-rounded-full"
                     style="width: 0.5rem; height: 2rem; background: var(--color-primary);"></span>
                  {{ domain.domain_name }}
               </h3>
               <span class="table__code-badge">National Cluster</span>
            </header>

            <div class="u-p-6">
               <div v-for="process in domain.processes" :key="process.process_name" class="u-mb-8 last:u-mb-0">
                  <div class="u-mb-4">
                     <h4 class="u-flex u-items-center u-gap-2 u-text-primary u-font-bold">
                        <i class="bi bi-tags"></i>
                        {{ process.process_name }}
                     </h4>
                     <p class="u-text-xs u-text-muted u-ml-7">Service Family</p>
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
                              <th class="table__header-cell table__header-cell--align-right"
                                 style="padding-right: 1rem;">Actions</th>
                           </tr>
                        </thead>
                        <tbody>
                           <tr v-for="service in process.services" :key="service.service_name" class="table__row">
                              <td class="table__cell" style="padding-left: 1rem;">
                                 <div class="u-flex u-items-center u-gap-2">
                                    <div class="table__cell--bold">{{ service.service_name }}</div>
                                    <i v-if="service.mda_priority" class="bi bi-star-fill u-text-primary"
                                       title="Priority MDA"></i>
                                 </div>
                                 <div class="u-text-xs u-text-muted u-mt-0.5">{{ service.mda }}</div>
                              </td>
                              <td class="table__cell">
                                 <div class="u-flex u-flex-col u-gap-1">
                                    <span class="u-text-xs u-font-bold u-text-primary">{{ service.service_type || 'N/A'
                                    }}</span>
                                    <div class="u-flex u-items-center u-gap-1">
                                       <div class="u-flex u-gap-0.5">
                                          <template v-for="i in 5" :key="i">
                                             <div :class="i <= service.maturity ? 'u-text-success' : 'u-text-muted'"
                                                class="u-block u-rounded-full"
                                                style="width: 0.625rem; height: 0.25rem; background: currentColor;">
                                             </div>
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
                                       <span v-for="ch in service.delivery_channels" :key="ch" class="table__code-badge"
                                          style="font-size: 10px; padding: 2px 6px;">
                                          {{ ch }}
                                       </span>
                                    </div>
                                 </div>
                              </td>
                              <td class="table__cell">
                                 <div class="u-flex u-flex-wrap u-gap-1" style="max-width: 200px">
                                    <span v-for="pp in service.pain_points" :key="pp" class="badge badge--danger"
                                       style="font-size: 10px; padding: 2px 6px;">
                                       {{ pp }}
                                    </span>
                                    <span v-if="!service.pain_points || service.pain_points.length === 0"
                                       class="u-text-muted u-text-xs" style="font-style: italic">None reported</span>
                                 </div>
                              </td>
                              <td class="table__cell">
                                 <span v-if="service.workflow_configured" class="badge badge--success">
                                    Active
                                 </span>
                                 <span v-else class="badge badge--danger">
                                    Missing
                                 </span>
                              </td>
                              <td class="table__cell table__cell--align-right" style="padding-right: 1rem;">
                                 <button v-if="service.workflow_configured" @click="visualizeWorkflow(service)"
                                    class="button button--secondary button--small"
                                    style="font-size: 10px; padding: 4px 8px;">
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
      <BaseModal :show="showWorkflowModal" @close="closeWorkflowModal" size="full" headerClass="modal__header--dark">
         <template #header>
            <div class="u-flex-1">
               <h3 class="modal__title">{{ selectedService?.service_name }}</h3>
               <p class="modal__subtitle u-font-mono u-uppercase" style="letter-spacing: 0.1em">BPMN 2.0 Process
                  Orchestration Model</p>
            </div>

            <div class="tab-bar" style="background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.1)">
               <button @click="switchStage('as_is')" :class="{ 'tab-bar__item--active': activeLifecycle === 'as_is' }"
                  class="tab-bar__item u-text-xs u-py-1.5" style="border: none">
                  As-Is
               </button>
               <button @click="switchStage('to_be')" :class="{ 'tab-bar__item--active': activeLifecycle === 'to_be' }"
                  class="tab-bar__item u-text-xs u-py-1.5" style="border: none">
                  To-Be
               </button>
            </div>
         </template>

         <!-- Use Single Source of Truth for BPMN Rendering -->
         <div class="u-flex u-justify-center">
            <BpmnRenderer 
               v-if="selectedService" 
               :steps="filteredWorkflowSteps" 
               :stage="activeLifecycle" 
               class="u-w-full"
            />
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
   import BpmnRenderer from './BpmnRenderer.vue';

   const props = defineProps({
      activeTab: { type: String, default: 'Whole-of-Gov Catalogue' }
   });

   const serviceConfigStore = useServiceConfigStore();
   const auditStats = computed(() => serviceConfigStore.catalogueSummary);
   const matrixData = computed(() => serviceConfigStore.matrixData);
   const loading = computed(() => serviceConfigStore.loadingSummary);
   const error = ref(null);
   const isPrinting = ref(false);

   const searchQuery = ref('');
   const selectedDomain = ref('');
   const selectedMda = ref('');
   const selectedCategory = ref('');
   const selectedType = ref('');
   const selectedLifeEvent = ref('');
   const selectedGroup = ref('');

   const domainSearchLocal = ref('');
   const mdaSearchLocal = ref('');
   const categorySearchLocal = ref('');
   const typeSearchLocal = ref('');
   const lifeEventSearchLocal = ref('');
   const groupSearchLocal = ref('');

   const showDomainDropdown = ref(false);
   const showMdaDropdown = ref(false);
   const showCategoryDropdown = ref(false);
   const showTypeDropdown = ref(false);
   const showLifeEventDropdown = ref(false);
   const showGroupDropdown = ref(false);

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

   const categoryList = computed(() => {
      const cats = new Set();
      matrixData.value.forEach(d => {
         d.processes.forEach(p => {
            p.services.forEach(s => {
               if (s.service_category) cats.add(s.service_category);
            });
         });
      });
      return [...cats].sort();
   });

   const typeList = computed(() => {
      const types = new Set();
      matrixData.value.forEach(d => {
         d.processes.forEach(p => {
            p.services.forEach(s => {
               if (s.service_type) types.add(s.service_type);
            });
         });
      });
      return [...types].sort();
   });

   const lifeEventList = computed(() => {
      const events = new Set();
      matrixData.value.forEach(d => {
         d.processes.forEach(p => {
            p.services.forEach(s => {
               if (s.life_event_group) events.add(s.life_event_group);
            });
         });
      });
      return [...events].sort();
   });

   const groupList = computed(() => {
      const grps = new Set();
      matrixData.value.forEach(d => {
         d.processes.forEach(p => {
            p.services.forEach(s => {
               if (s.service_group_details) {
                  s.service_group_details.forEach(g => grps.add(g.name));
               }
            });
         });
      });
      return [...grps].sort();
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

   const filteredCategories = computed(() => {
      if (!categorySearchLocal.value) return categoryList.value;
      const q = categorySearchLocal.value.toLowerCase();
      return categoryList.value.filter(c => c.toLowerCase().includes(q));
   });

   const filteredTypes = computed(() => {
      if (!typeSearchLocal.value) return typeList.value;
      const q = typeSearchLocal.value.toLowerCase();
      return typeList.value.filter(t => t.toLowerCase().includes(q));
   });

   const filteredLifeEvents = computed(() => {
      if (!lifeEventSearchLocal.value) return lifeEventList.value;
      const q = lifeEventSearchLocal.value.toLowerCase();
      return lifeEventList.value.filter(l => l.toLowerCase().includes(q));
   });

   const filteredGroups = computed(() => {
      if (!groupSearchLocal.value) return groupList.value;
      const q = groupSearchLocal.value.toLowerCase();
      return groupList.value.filter(g => g.toLowerCase().includes(q));
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

   const selectCategory = (category) => {
      selectedCategory.value = category;
      categorySearchLocal.value = category;
      showCategoryDropdown.value = false;
   };

   const selectType = (type) => {
      selectedType.value = type;
      typeSearchLocal.value = type;
      showTypeDropdown.value = false;
   };

   const selectLifeEvent = (event) => {
      selectedLifeEvent.value = event;
      lifeEventSearchLocal.value = event;
      showLifeEventDropdown.value = false;
   };

   const selectGroup = (group) => {
      selectedGroup.value = group;
      groupSearchLocal.value = group;
      showGroupDropdown.value = false;
   };

   const closeDropdownWithDelay = (type) => {
      setTimeout(() => {
         if (type === 'domain') showDomainDropdown.value = false;
         if (type === 'mda') showMdaDropdown.value = false;
         if (type === 'category') showCategoryDropdown.value = false;
         if (type === 'type') showTypeDropdown.value = false;
         if (type === 'lifeEvent') showLifeEventDropdown.value = false;
         if (type === 'group') showGroupDropdown.value = false;
      }, 200);
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
               // Baseline context filters
               if (props.activeTab === 'Priority MDAs') {
                  const mdaPriority = s.mda_priority === true;
                  if (!mdaPriority) return false;
               }

               if (props.activeTab === 'Priority Services') {
                  const sPriority = s.service_priority === 'high' || s.service_priority === 'critical' || s.mda_priority === true;
                  if (!sPriority) return false;
               }

               if (props.activeTab === 'Cradle to Death') {
                  const cradleGroups = ['The Cradle', 'Childhood & Education', 'Coming of Age', 'Adulthood', 'The Sunset'];
                  const cradleFamilies = [
                     'Identity & Civil Registration',
                     'Civil Registration & Identity',
                     'Social Protection & Welfare',
                     'Education & Skills Development',
                     'Health & Public Health Regulation'
                  ];
                  
                  const isCradleContext = (s.service_group_details || []).some(sg => cradleGroups.includes(sg.name)) ||
                                          cradleGroups.includes(d.domain_name) ||
                                          cradleGroups.includes(p.process_name) ||
                                          cradleFamilies.includes(s.service_family_details?.name);
                  
                  const isLC = s.service_priority === 'critical' || isCradleContext;
                  if (!isLC) return false;
               }

               const matchesMda = !selectedMda.value || s.mda === selectedMda.value;
               const matchesCategory = !selectedCategory.value || s.service_category === selectedCategory.value;
               const matchesType = !selectedType.value || s.service_type === selectedType.value;
               const matchesLifeEvent = !selectedLifeEvent.value || s.life_event_group === selectedLifeEvent.value;
               const matchesGroup = !selectedGroup.value || (s.service_group_details && s.service_group_details.some(g => g.name === selectedGroup.value));
               const matchesSearch = !searchQuery.value ||
                  s.service_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                  s.mda.toLowerCase().includes(searchQuery.value.toLowerCase());
               return matchesMda && matchesCategory && matchesType && matchesLifeEvent && matchesGroup && matchesSearch;
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

   const filteredWorkflowSteps = computed(() => {
      if (!selectedService.value) return [];
      return (selectedService.value.workflow_steps || []).filter(s => s.lifecycle_stage === activeLifecycle.value);
   });

   const visualizeWorkflow = (service, stage = 'as_is') => {
      selectedService.value = service;
      activeLifecycle.value = stage;
      
      // Heuristic: If selected stage is empty but other stage has steps, switch
      const steps = (service.workflow_steps || []).filter(s => s.lifecycle_stage === stage);
      if (steps.length === 0 && service.workflow_steps?.length > 0) {
         const otherStage = stage === 'as_is' ? 'to_be' : 'as_is';
         const otherSteps = service.workflow_steps.filter(s => s.lifecycle_stage === otherStage);
         if (otherSteps.length > 0) {
            activeLifecycle.value = otherStage;
         }
      }
      
      showWorkflowModal.value = true;
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
      selectedCategory.value = '';
      selectedType.value = '';
      selectedLifeEvent.value = '';
      domainSearchLocal.value = '';
      mdaSearchLocal.value = '';
      categorySearchLocal.value = '';
      typeSearchLocal.value = '';
      lifeEventSearchLocal.value = '';
      groupSearchLocal.value = '';
      selectedGroup.value = '';
   };

   const isAnyFilterActive = computed(() => {
      return searchQuery.value || selectedDomain.value || selectedMda.value ||
         selectedCategory.value || selectedType.value || selectedLifeEvent.value;
   });

   const printCatalogue = () => {
      isPrinting.value = true;
      nextTick(() => {
         window.print();
         isPrinting.value = false;
      });
   };

   onMounted(() => {
      mermaid.initialize({ startOnLoad: false, theme: 'default' });
      fetchMatrix();
   });
</script>

<style scoped>

   /* ICTA Premium Design System for Whole of Government */
   .animate-fade-in {
      animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
   }

   @keyframes fadeIn {
      from {
         opacity: 0;
         transform: translateY(15px);
      }

      to {
         opacity: 1;
         transform: translateY(0);
      }
   }

   /* Glassmorphism Toolbar */
   .toolbar {
      background: rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.3);
      padding: 1.5rem;
      border-radius: var(--border-radius-lg);
      box-shadow: var(--shadow-lg);
   }

   .toolbar__filter-input {
      background: white;
      border: 2px solid var(--color-border-light);
      font-weight: 600;
      transition: all 0.3s ease;
   }

   .toolbar__filter-input:focus {
      border-color: var(--color-primary);
      box-shadow: 0 0 0 4px var(--color-primary-soft);
      transform: translateY(-1px);
   }

   .toolbar__clear-icon {
      position: absolute;
      right: 1rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--color-text-muted);
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s ease;
      opacity: 0.5;
   }

   .toolbar__clear-icon:hover {
      color: var(--color-primary);
      opacity: 1;
      transform: translateY(-50%) scale(1.1);
   }

   .toolbar__clear-icon--with-arrow {
      right: 2.5rem;
   }

   /* Classy Dropdown Menu */
   .dropdown-menu {
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      right: 0;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(15px);
      border: 1px solid rgba(0, 0, 0, 0.05);
      border-radius: 12px;
      margin-top: 0.5rem;
      z-index: 1000;
      overflow: auto;
      padding: 0.5rem;
      max-height: 300px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
   }

   .dropdown-item {
      padding: 0.75rem 1rem;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      color: var(--color-text-main);
      cursor: pointer;
      transition: all 0.2s ease;
   }

   .dropdown-item:hover {
      background: var(--color-primary-soft);
      color: var(--color-primary);
      transform: translateX(4px);
   }

   .dropdown-item--header {
      color: var(--color-primary);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--color-border-light);
      margin-bottom: 0.25rem;
      border-radius: 0;
   }

   /* Reset Button */
   .btn-reset {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.75rem 1.25rem;
      background: white;
      border: 1px solid var(--color-border);
      border-radius: 8px;
      font-weight: 800;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--color-text-muted);
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
   }

   .btn-reset:hover {
      border-color: var(--color-primary);
      color: var(--color-primary);
      background: var(--color-primary-soft);
      transform: rotate(-5deg) scale(1.05);
   }

   /* Filter Chips */
   .filter-chip {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      background: var(--grad-premium);
      color: white;
      border-radius: 40px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: var(--shadow-md);
   }

   .filter-chip:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
      filter: brightness(1.1);
   }

   .filter-chip__label {
      opacity: 0.6;
      text-transform: uppercase;
      font-size: 9px;
   }

   /* Vue Transitions */
   .dropdown-enter-active,
   .dropdown-leave-active {
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
   }

   .dropdown-enter-from,
   .dropdown-leave-to {
      opacity: 0;
      transform: translateY(-10px) scale(0.95);
   }

   .list-enter-active,
   .list-leave-active {
      transition: all 0.4s ease;
   }

   .list-enter-from,
   .list-leave-to {
      opacity: 0;
      transform: scale(0.5) translateY(10px);
   }

   /* Premium Table Header */
   .table__header-row {
      background: var(--grad-premium) !important;
      color: white !important;
      border: none;
   }

   .table__header-cell {
      color: white !important;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      font-size: 11px;
      padding: 1.25rem 1rem;
   }

   /* Sleek Table Rows */
   .table__row {
      transition: all 0.2s ease;
      border-bottom: 1px solid var(--color-border-light);
   }

   .table__row:hover {
      background: var(--color-primary-soft) !important;
      box-shadow: inset 4px 0 0 var(--color-primary);
   }

   .table__cell {
      padding: 1.25rem 1rem;
      font-weight: 600;
      color: var(--color-text-main);
   }

   /* Badge Refinement */
   .badge {
      padding: 0.4rem 0.8rem;
      border-radius: var(--border-radius-full);
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      box-shadow: var(--shadow-sm);
   }

   .badge--primary {
      background: var(--grad-accent);
      color: white;
   }

   /* Category Sections */
   .category-header {
      background: #f8fafc;
      border-left: 4px solid var(--color-primary);
      padding: 0.75rem 1.5rem;
      margin: 2rem 0 1rem 0;
      border-radius: 0 8px 8px 0;
   }

   .category-title {
      font-size: 13px;
      font-weight: 900;
      color: var(--color-primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
   }

   /* High-Density Grid Improvements */
   .systems-list {
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
   }

   .system-tag {
      background: white;
      border: 1px solid var(--color-border);
      padding: 0.2rem 0.6rem;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 700;
      color: var(--color-text-muted);
   }

   /* Legend Dots Refinement */
   .legend-dot {
      display: block;
      aspect-ratio: 1/1;
      width: 0.75rem;
   }

   .legend-dot--start {
      background: var(--color-success);
      border-radius: 50%;
   }

   .legend-dot--user {
      background: var(--color-primary);
      border-radius: 4px;
   }

   .legend-dot--service {
      border: 2px dashed var(--color-info);
      border-radius: 4px;
   }

   .legend-dot--gateway {
      border: 2px solid var(--color-warning);
      transform: rotate(45deg);
      width: 0.65rem;
   }

   .legend-dot--end {
      background: var(--color-danger);
      border-radius: 50%;
   }

   /* Print Styles */
   @media print {
      .no-print {
         display: none !important;
      }

      .print-only {
         display: block !important;
      }

      .card {
         border: 1px solid #eee !important;
         box-shadow: none !important;
         break-inside: avoid !important;
         margin-bottom: 2rem !important;
      }

      .table-container {
         border: 1px solid #eee !important;
         overflow: visible !important;
      }

      .table__row {
         break-inside: avoid !important;
      }

      .badge {
         border: 1px solid #ccc !important;
         color: black !important;
         background: transparent !important;
      }

      body {
         background: white !important;
         color: black !important;
      }

      .page__header {
         border-bottom: 2px solid black !important;
         margin-bottom: 3rem !important;
      }

      .print-section {
         break-inside: avoid !important;
         page-break-inside: avoid !important;
      }
   }

   .print-only {
      display: none;
   }
</style>
