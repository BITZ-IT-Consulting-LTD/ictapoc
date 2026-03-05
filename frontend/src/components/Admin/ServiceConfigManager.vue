<template>
  <section class="page service-config-manager">
    <WogDashboardStats v-if="auditStats" :stats="auditStats" class="mb-8" />

    <header class="page__header u-mb-8">
      <div class="page__title-group">
        <h1 class="page__title">National Service Registry</h1>
        <p class="page__subtitle">Centralized configuration for government services and data schemas</p>
      </div>
      <div class="page__actions">
        <button @click="openCreateModal" class="button button--primary button--pill">
          <i class="bi bi-plus-lg"></i> Register New Service
        </button>
      </div>
    </header>

    <div class="toolbar u-mb-6">
      <div class="toolbar__filters">
        <!-- Search -->
        <div class="toolbar__filter-group">
          <i class="bi bi-search toolbar__filter-icon"></i>
          <input type="text" v-model="searchQuery" placeholder="Search Services..." class="toolbar__filter-input">
          <i v-if="searchQuery" @click="searchQuery = ''" class="bi bi-x-circle-fill toolbar__clear-icon"></i>
        </div>

        <!-- Family Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-diagram-3-fill toolbar__filter-icon"></i>
          <input type="text" v-model="familySearchLocal" placeholder="Filter by Family..."
            @focus="showFamilyFilterDropdown = true" @blur="setTimeout(() => showFamilyFilterDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showFamilyFilterDropdown }"></i>
          <i v-if="familyFilter" @click="selectFamilyFilter('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showFamilyFilterDropdown" class="dropdown-menu">
              <div @click="selectFamilyFilter('')" class="dropdown-item dropdown-item--header">All Families</div>
              <div v-for="f in filteredFamiliesList" :key="f" @click="selectFamilyFilter(f)" class="dropdown-item">
                {{ f }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Agency Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-building toolbar__filter-icon"></i>
          <input type="text" v-model="mdaFilterSearchLocal" placeholder="Filter by Agency..."
            @focus="showMdaFilterDropdown = true" @blur="setTimeout(() => showMdaFilterDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showMdaFilterDropdown }"></i>
          <i v-if="mdaFilter" @click="selectMdaFilter('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showMdaFilterDropdown" class="dropdown-menu">
              <div @click="selectMdaFilter('')" class="dropdown-item dropdown-item--header">
                All Agencies
              </div>
              <div v-for="mda in filteredMdasForFilter" :key="mda.id" @click="selectMdaFilter(mda)"
                class="dropdown-item">
                <i class="bi bi-building u-mr-2"></i> {{ mda.name }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Life Event Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-calendar-event toolbar__filter-icon"></i>
          <input type="text" v-model="lifeEventSearchLocal" placeholder="Filter by Life Event..."
            @focus="showLifeEventFilterDropdown = true"
            @blur="setTimeout(() => showLifeEventFilterDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showLifeEventFilterDropdown }"></i>
          <i v-if="lifeEventFilter" @click="selectLifeEventFilter('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showLifeEventFilterDropdown" class="dropdown-menu">
              <div @click="selectLifeEventFilter('')" class="dropdown-item dropdown-item--header">All Events</div>
              <div v-for="e in filteredLifeEvents" :key="e" @click="selectLifeEventFilter(e)" class="dropdown-item">
                {{ e }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Type Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-tag-fill toolbar__filter-icon"></i>
          <input type="text" v-model="typeSearchLocal" placeholder="Filter by Type..."
            @focus="showTypeFilterDropdown = true" @blur="setTimeout(() => showTypeFilterDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showTypeFilterDropdown }"></i>
          <i v-if="typeFilter" @click="selectTypeFilter('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showTypeFilterDropdown" class="dropdown-menu">
              <div @click="selectTypeFilter('')" class="dropdown-item dropdown-item--header">All Types</div>
              <div v-for="t in filteredTypesList" :key="t" @click="selectTypeFilter(t)" class="dropdown-item">
                {{ t }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Group Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-collection-fill toolbar__filter-icon"></i>
          <input type="text" v-model="groupSearchLocal" placeholder="Filter by Group..."
            @focus="showGroupFilterDropdown = true" @blur="setTimeout(() => showGroupFilterDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showGroupFilterDropdown }"></i>
          <i v-if="groupFilter" @click="selectGroupFilter('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showGroupFilterDropdown" class="dropdown-menu">
              <div @click="selectGroupFilter('')" class="dropdown-item dropdown-item--header">All Lifecycle Groups</div>
              <div v-for="g in filteredGroupsForFilter" :key="g.id" @click="selectGroupFilter(g)" class="dropdown-item">
                {{ g.name }}
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
      <div v-if="familyFilter" :key="'f-' + familyFilter" class="filter-chip" @click="selectFamilyFilter('')">
        <span class="filter-chip__label">Family:</span>
        <span class="filter-chip__value">{{ familyFilter }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="mdaFilter" :key="'m-' + mdaFilter" class="filter-chip" @click="selectMdaFilter('')">
        <span class="filter-chip__label">Agency:</span>
        <span class="filter-chip__value">{{ getMdaName(mdaFilter).split('(')[0] }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="lifeEventFilter" :key="'l-' + lifeEventFilter" class="filter-chip" @click="selectLifeEventFilter('')">
        <span class="filter-chip__label">Event:</span>
        <span class="filter-chip__value">{{ lifeEventFilter }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="categoryFilter" :key="'c-' + categoryFilter" class="filter-chip" @click="selectCategoryFilter('')">
        <span class="filter-chip__label">Category:</span>
        <span class="filter-chip__value">{{ categoryFilter }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="typeFilter" :key="'t-' + typeFilter" class="filter-chip" @click="selectTypeFilter('')">
        <span class="filter-chip__label">Type:</span>
        <span class="filter-chip__value">{{ typeFilter }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="groupFilter" :key="'g-' + groupFilter" class="filter-chip" @click="selectGroupFilter('')">
        <span class="filter-chip__label">Group:</span>
        <span class="filter-chip__value">{{ getGroupName(groupFilter) }}</span>
        <i class="bi bi-x"></i>
      </div>
    </transition-group>

    <!-- Service Registry Table -->
    <div class="card u-overflow-hidden">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr class="table__header-row">
              <th class="table__header-cell table__header-cell--with-left-padding">Registry Code</th>
              <th class="table__header-cell">Official Service Name</th>
              <th class="table__header-cell">Institutional Owner (MDA)</th>
              <th class="table__header-cell">Type</th>
              <th class="table__header-cell">Strategic Family</th>
              <th class="table__header-cell table__header-cell--align-right table__header-cell--with-right-padding">
                Management</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in filteredServices" :key="service.id" class="table__row">
              <td class="table__cell table__cell--with-left-padding">
                <span class="table__code-badge">
                  {{ service.service_code }}
                </span>
              </td>
              <td class="table__cell table__cell--bold">{{ service.service_name }}</td>
              <td class="table__cell">
                <div class="table__mda-info">
                  <i class="bi bi-building table__mda-icon"></i> {{ getMdaName(service.mda) }}
                </div>
              </td>
              <td class="table__cell">
                <span class="badge" :class="{
                    'badge--primary': service.service_type === 'G2C',
                    'badge--success': service.service_type === 'G2G',
                    'badge--info': service.service_type === 'G2B',
                    'badge--warning': service.service_type === 'C2G'
                  }">{{ service.service_type || 'N/A' }}</span>
              </td>
              <td class="table__cell">
                <span v-if="service.service_family_details" class="badge"
                  style="background: var(--bg-page); color: var(--text-main); border: 1px solid var(--border-color); font-size: 10px; font-weight: 800; text-transform: uppercase;">
                  <i class="bi bi-diagram-2 me-1"></i> {{ service.service_family_details.name }}
                </span>
                <span v-else class="u-text-muted text-[10px] u-italic">Uncategorized</span>
              </td>
              <td class="table__cell table__cell--align-right table__cell--with-right-padding">
                <div class="table__actions">
                  <button @click="openEditModal(service)" class="button button--secondary button--small">
                    <i class="bi bi-sliders"></i> Configure
                  </button>
                  <button @click="deleteService(service.id)" class="button button--ghost button--small">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredServices.length === 0">
              <td colspan="5" class="table__cell u-text-center u-p-12 u-text-muted" style="font-style: italic">
                No services found matching your criteria
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Configuration Modal -->
    <BaseModal v-model:show="showModal"
      :title="editForm.id ? 'Modify Service Configuration' : 'Onboard New National Service'"
      subtitle="Define technical data schemas and internal agency workflows" icon="bi-gear-wide-connected" size="full">
      <form @submit.prevent="handleUpdate" class="form flex flex-col gap-6">
        <!-- High-Fidelity Configuration Journey -->
        <div class="u-flex u-gap-10">
          <!-- Strategic Navigation Sidebar -->
          <aside class="u-w-80 u-flex-shrink-0">
            <div class="u-sticky u-top-4">
              <div class="u-mb-8">
                <div class="u-flex u-items-center u-gap-3 u-mb-2">
                  <div class="u-w-1.5 u-h-6 u-bg-primary u-rounded-full"></div>
                  <h4 class="u-text-[11px] u-font-black u-text-muted u-uppercase u-tracking-[0.2em]">Config Registry
                  </h4>
                </div>
                <p class="u-text-[11px] u-text-muted/60 u-pl-4">Administrative Service Lifecycle</p>
              </div>

              <div class="u-flex u-flex-col u-gap-3">
                <!-- Identity Step -->
                <button type="button" @click="currentConfigTab = 'identity'" class="config-nav-item"
                  :class="{ 'config-nav-item--active': currentConfigTab === 'identity' }">
                  <div class="config-nav-item__index">01</div>
                  <div class="config-nav-item__content">
                    <span class="config-nav-item__title">Service Identity</span>
                    <span class="config-nav-item__desc">Registry Mapping</span>
                  </div>
                  <i v-if="currentConfigTab === 'identity'"
                    class="bi bi-chevron-right u-ml-auto u-text-primary u-text-sm"></i>
                </button>

                <!-- Schema Step -->
                <button type="button" @click="currentConfigTab = 'schema'" class="config-nav-item"
                  :class="{ 'config-nav-item--active': currentConfigTab === 'schema' }">
                  <div class="config-nav-item__index">02</div>
                  <div class="config-nav-item__content">
                    <span class="config-nav-item__title">Technical Schema</span>
                    <span class="config-nav-item__desc">Data Intake Definition</span>
                  </div>
                  <i v-if="currentConfigTab === 'schema'"
                    class="bi bi-chevron-right u-ml-auto u-text-success u-text-sm"></i>
                </button>

                <!-- Workflow Step -->
                <button type="button" @click="currentConfigTab = 'workflow'" :disabled="!editForm.id"
                  class="config-nav-item" :class="{
                    'config-nav-item--active': currentConfigTab === 'workflow',
                    'config-nav-item--disabled': !editForm.id
                  }">
                  <div class="config-nav-item__index">03</div>
                  <div class="config-nav-item__content">
                    <span class="config-nav-item__title">Process Pipeline</span>
                    <span class="config-nav-item__desc">Orchestration Nodes</span>
                    <span v-if="!editForm.id" class="u-text-[9px] u-text-warning u-font-black u-uppercase u-mt-1">
                      <i class="bi bi-lock-fill"></i> Save Identity First
                    </span>
                  </div>
                  <i v-if="currentConfigTab === 'workflow'"
                    class="bi bi-chevron-right u-ml-auto u-text-secondary u-text-sm"></i>
                </button>
              </div>

              <!-- Journey Progress Summary -->
              <div
                class="u-mt-10 u-p-5 u-bg-bg-page u-rounded-2xl u-border u-border-border-color u-relative u-overflow-hidden">
                <div class="u-absolute u-top-0 u-left-0 u-w-full u-h-1 u-bg-slate-100">
                  <div class="u-h-full u-bg-primary transition-all duration-700"
                    :style="{ width: currentConfigTab === 'identity' ? '33%' : currentConfigTab === 'schema' ? '66%' : '100%' }">
                  </div>
                </div>
                <div class="u-flex u-justify-between u-items-center">
                  <span class="u-text-[10px] u-font-black u-text-muted u-uppercase">Onboarding Progress</span>
                  <span class="u-text-[10px] u-font-black u-text-primary">{{ currentConfigTab === 'identity' ? '33%' :
                    currentConfigTab === 'schema' ? '66%' : '100%' }}</span>
                </div>
              </div>
            </div>
          </aside>

          <!-- Right Content Area -->
          <div class="flex-1 min-w-0">
            <!-- Identity Tab -->
            <div v-show="currentConfigTab === 'identity'" class="tab-content animate-fade-in">
              <div class="card border-0 shadow-sm">
                <div class="card__header bg-gradient-to-r from-primary/5 to-primary/10">
                  <h3 class="card__title flex items-center gap-2">
                    <i class="bi bi-card-heading text-primary"></i>
                    Service Identity & Ownership
                  </h3>
                  <p class="card__subtitle">Basic information and institutional mapping</p>
                </div>
                <div class="card__body">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="form__group">
                      <label class="form__label">
                        <i class="bi bi-tag me-1"></i>Official Service Designation
                      </label>
                      <input type="text" v-model="editForm.service_name" class="form__input" required
                        placeholder="e.g. Passport Application">
                      <p class="text-xs text-muted mt-1">
                        <i class="bi bi-info-circle me-1"></i>User-facing service name
                      </p>
                    </div>
                    <div class="form__group">
                      <label class="form__label">
                        <i class="bi bi-upc-scan me-1"></i>Unique Registry Code
                      </label>
                      <input type="text" v-model="editForm.service_code" class="form__input font-mono" required
                        placeholder="e.g. FOR-CON-003">
                      <p class="text-xs text-muted mt-1">
                        <i class="bi bi-info-circle me-1"></i>System identifier (uppercase, no spaces)
                      </p>
                    </div>
                    <div class="form__group md:col-span-2">
                      <label class="form__label">
                        <i class="bi bi-building me-1"></i>Institutional Ownership (MDA)
                      </label>
                      <div class="space-y-2">
                        <input type="text" v-model="mdaDropdownSearch" placeholder="🔍 Filter agencies..."
                          class="form__input">
                        <select v-model="editForm.mda" class="form__select" required>
                          <option v-for="mda in filteredMdasForDropdown" :key="mda.id" :value="mda.id">
                            {{ mda.name }} ({{ mda.code }})
                          </option>
                        </select>
                      </div>
                      <div class="alert alert--info mt-3">
                        <i class="bi bi-shield-check me-2"></i>
                        Mapping a service to an MDA ensures proper data sovereignty and access control.
                      </div>
                    </div>
                    <div class="form__group md:col-span-2">
                      <label class="form__label">
                        <i class="bi bi-diagram-2-fill me-1"></i>Service Strategic Family
                      </label>
                      <select v-model="editForm.service_family" class="form__select">
                        <option :value="null">Uncategorized (Independent Service)</option>
                        <option v-for="fam in families" :key="fam.id" :value="fam.id">
                          {{ fam.name }}
                        </option>
                      </select>
                      <p class="text-xs text-muted mt-1">
                        <i class="bi bi-info-circle me-1"></i>Strategic clustering for shared workflows
                      </p>
                    </div>

                    <!-- New Fields -->
                    <div class="form__group">
                      <label class="form__label">
                        <i class="bi bi-person-check me-1"></i>Service Model (Type)
                      </label>
                      <select v-model="editForm.service_type" class="form__select">
                        <option value="G2C">G2C (Gov to Citizen)</option>
                        <option value="G2G">G2G (Gov to Gov)</option>
                        <option value="G2B">G2B (Gov to Business)</option>
                        <option value="C2G">C2G (Citizen to Gov)</option>
                        <option value="B2G">B2G (Business to Gov)</option>
                        <option value="Internal">Internal Agency Process</option>
                      </select>
                    </div>

                    <div class="form__group md:col-span-2">
                       <label class="form__label">
                        <i class="bi bi-collection me-1"></i>Catalogue Life-Cycle Groups
                      </label>
                      <div class="u-flex u-flex-wrap u-gap-3 u-p-4 u-bg-bg-page u-rounded-xl u-border">
                         <label v-for="grp in groups" :key="grp.id" class="u-flex u-items-center u-gap-2 u-cursor-pointer hover:u-text-primary transition-colors">
                            <input type="checkbox" :value="grp.id" v-model="editForm.service_groups" class="u-w-4 u-h-4 accent-primary">
                            <span class="u-text-xs u-font-bold">{{ grp.name }}</span>
                         </label>
                      </div>
                      <p class="u-text-[10px] u-text-muted u-mt-2 italic">Select all that apply. Services in "Cradle to Death" sub-stages should also be checked in the main "Cradle to Death" group.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Schema Tab -->
            <div v-show="currentConfigTab === 'schema'" class="tab-content animate-fade-in">
              <div class="card border-0 shadow-sm">
                <div class="card__header bg-gradient-to-r from-success/5 to-success/10">
                  <h3 class="card__title flex items-center gap-2">
                    <i class="bi bi-ui-checks-grid text-success"></i>
                    Data Intake Schema
                  </h3>
                  <p class="card__subtitle">Define the form fields citizens will fill</p>
                </div>
                <div class="card__body">
                  <FormSchemaBuilder v-model="editForm.config" />
                </div>
              </div>
            </div>

            <!-- Workflow Tab: Strategic Orchestration -->
            <div v-show="currentConfigTab === 'workflow'" class="tab-content u-animate-fade-in">
              <div v-if="editForm.id" class="u-mt-4">
                <WorkflowStepManager :service-config-id="editForm.id" />
              </div>
              <div v-else
                class="u-p-12 u-text-center u-bg-warning/5 u-rounded-3xl u-border-2 u-border-dashed u-border-warning/20">
                <i class="bi bi-shield-lock u-text-6xl u-text-warning u-opacity-30 u-mb-4 u-block"></i>
                <h4 class="u-font-black u-text-main u-uppercase u-tracking-widest u-mb-2">Identity Locked</h4>
                <p class="u-text-xs u-text-muted/60 u-mb-8">Complete the service identity registration to unlock the
                  orchestration pipeline.</p>
                <button type="button" @click="currentConfigTab = 'identity'"
                  class="u-text-xs u-font-black u-uppercase u-text-primary u-tracking-widest hover:u-underline">
                  Return to Identity 01
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Strategic Action Footer -->
        <div class="u-flex u-justify-between u-items-center u-mt-10 u-pt-8 u-border-t">
          <button type="button" @click="closeModal"
            class="button button--ghost u-text-xs u-font-black u-uppercase u-tracking-widest">
            <i class="bi bi-x-circle u-mr-2"></i> Discard Configuration
          </button>

          <div class="u-flex u-gap-4">
            <button type="submit"
              class="button button--primary u-px-10 u-py-4 u-rounded-xl u-text-xs u-font-black u-uppercase u-tracking-[0.2em]">
              <i class="bi bi-shield-check-fill u-text-sm"></i>
              Commit Registry Update
            </button>
          </div>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useServiceConfigStore } from '../../store/serviceConfig';
  import { useMdaStore } from '../../store/mda';
  import WorkflowStepManager from './WorkflowStepManager.vue';
  import FormSchemaBuilder from './FormSchemaBuilder.vue';
  import WogDashboardStats from './WogDashboardStats.vue';
  import BaseModal from '../Common/BaseModal.vue';

  const serviceConfigStore = useServiceConfigStore();
  const mdaStore = useMdaStore();

  const auditStats = computed(() => serviceConfigStore.catalogueSummary);
  const services = computed(() => serviceConfigStore.services);
  const families = computed(() => serviceConfigStore.families);
  const groups = computed(() => serviceConfigStore.groups);
  const mdas = computed(() => mdaStore.mdas);
  const searchQuery = ref('');
  const mdaFilter = ref('');
  const familyFilter = ref('');
  const categoryFilter = ref('');
  const lifeEventFilter = ref('');
  const typeFilter = ref('');
  const groupFilter = ref('');

  const mdaFilterSearchLocal = ref('');
  const familySearchLocal = ref('');
  const categorySearchLocal = ref('');
  const lifeEventSearchLocal = ref('');
  const typeSearchLocal = ref('');
  const groupSearchLocal = ref('');

  const showMdaFilterDropdown = ref(false);
  const showFamilyFilterDropdown = ref(false);
  const showCategoryFilterDropdown = ref(false);
  const showLifeEventFilterDropdown = ref(false);
  const showTypeFilterDropdown = ref(false);
  const showGroupFilterDropdown = ref(false);

  const currentConfigTab = ref('identity'); // Tab state for modal

  const familiesSet = computed(() => {
    const list = new Set();
    services.value.forEach(s => {
      if (s.service_family_details?.name) list.add(s.service_family_details.name);
    });
    return [...list].sort();
  });

  const categoriesList = computed(() => {
    const list = new Set();
    services.value.forEach(s => {
      if (s.category_details?.name) list.add(s.category_details.name);
    });
    return [...list].sort();
  });

  const lifeEventsList = computed(() => {
    const list = new Set();
    services.value.forEach(s => {
      if (s.life_event_group) list.add(s.life_event_group);
    });
    return [...list].sort();
  });

  const filteredMdasForFilter = computed(() => {
    if (!mdaFilterSearchLocal.value) return mdas.value;
    const q = mdaFilterSearchLocal.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q));
  });

  const filteredFamiliesList = computed(() => {
    if (!familySearchLocal.value) return familiesSet.value;
    const q = familySearchLocal.value.toLowerCase();
    return familiesSet.value.filter(d => d.toLowerCase().includes(q));
  });

  const filteredCategories = computed(() => {
    if (!categorySearchLocal.value) return categoriesList.value;
    const q = categorySearchLocal.value.toLowerCase();
    return categoriesList.value.filter(c => c.toLowerCase().includes(q));
  });

  const filteredLifeEvents = computed(() => {
    if (!lifeEventSearchLocal.value) return lifeEventsList.value;
    const q = lifeEventSearchLocal.value.toLowerCase();
    return lifeEventsList.value.filter(l => l.toLowerCase().includes(q));
  });

  const typesList = computed(() => {
    const list = new Set();
    services.value.forEach(s => {
      if (s.service_type) list.add(s.service_type);
    });
    return [...list].sort();
  });

  const filteredTypesList = computed(() => {
    if (!typeSearchLocal.value) return typesList.value;
    const q = typeSearchLocal.value.toLowerCase();
    return typesList.value.filter(t => t.toLowerCase().includes(q));
  });

  const filteredGroupsForFilter = computed(() => {
    if (!groupSearchLocal.value) return groups.value;
    const q = groupSearchLocal.value.toLowerCase();
    return groups.value.filter(g => g.name.toLowerCase().includes(q));
  });

  const selectMdaFilter = (mda) => {
    if (mda === '') {
      mdaFilter.value = '';
      mdaFilterSearchLocal.value = '';
    } else {
      mdaFilter.value = mda.id;
      mdaFilterSearchLocal.value = mda.name;
    }
    showMdaFilterDropdown.value = false;
  };

  const selectFamilyFilter = (val) => {
    familyFilter.value = val;
    familySearchLocal.value = val;
    showFamilyFilterDropdown.value = false;
  };

  const selectCategoryFilter = (val) => {
    categoryFilter.value = val;
    categorySearchLocal.value = val;
    showCategoryFilterDropdown.value = false;
  };

  const selectLifeEventFilter = (val) => {
    lifeEventFilter.value = val;
    lifeEventSearchLocal.value = val;
    showLifeEventFilterDropdown.value = false;
  };

  const selectTypeFilter = (val) => {
    typeFilter.value = val;
    typeSearchLocal.value = val;
    showTypeFilterDropdown.value = false;
  };

  const selectGroupFilter = (group) => {
    if (group === '') {
      groupFilter.value = '';
      groupSearchLocal.value = '';
    } else {
      groupFilter.value = group.id;
      groupSearchLocal.value = group.name;
    }
    showGroupFilterDropdown.value = false;
  };

  const filteredServices = computed(() => {
    let result = services.value;

    if (mdaFilter.value) {
      result = result.filter(s => s.mda === Number(mdaFilter.value));
    }

    if (familyFilter.value) {
      result = result.filter(s => s.service_family_details?.name === familyFilter.value);
    }

    if (categoryFilter.value) {
      result = result.filter(s => s.category_details?.name === categoryFilter.value);
    }

    if (lifeEventFilter.value) {
      result = result.filter(s => s.life_event_group === lifeEventFilter.value);
    }

    if (typeFilter.value) {
      result = result.filter(s => s.service_type === typeFilter.value);
    }

    if (groupFilter.value) {
      result = result.filter(s => s.service_groups && s.service_groups.includes(Number(groupFilter.value)));
    }

    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter(s =>
        s.service_name.toLowerCase().includes(q) ||
        s.service_code.toLowerCase().includes(q) ||
        getMdaName(s.mda).toLowerCase().includes(q)
      );
    }

    return result;
  });

  const mdaDropdownSearch = ref('');
  const filteredMdasForDropdown = computed(() => {
    if (!mdaDropdownSearch.value) return mdas.value;
    const q = mdaDropdownSearch.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q) || (m.code && m.code.toLowerCase().includes(q)));
  });

  const showModal = ref(false);
  const editForm = ref({
    id: null,
    service_code: '',
    service_name: '',
    mda: null,
    service_family: null,
    service_type: 'G2C',
    service_groups: [],
    config: { rules: { schema: { properties: {}, required: [] } } },
  });

  onMounted(() => {
    serviceConfigStore.fetchServices();
    serviceConfigStore.fetchFamilies();
    serviceConfigStore.fetchGroups();
    mdaStore.fetchMdas();
    serviceConfigStore.fetchCatalogueSummary();
  });

  const resetFilters = () => {
    searchQuery.value = '';
    mdaFilter.value = '';
    familyFilter.value = '';
    categoryFilter.value = '';
    lifeEventFilter.value = '';

    mdaFilterSearchLocal.value = '';
    familySearchLocal.value = '';
    categorySearchLocal.value = '';
    lifeEventSearchLocal.value = '';
    typeFilter.value = '';
    groupFilter.value = '';
    typeSearchLocal.value = '';
    groupSearchLocal.value = '';
  };

  const isAnyFilterActive = computed(() => {
    return searchQuery.value || mdaFilter.value || familyFilter.value || categoryFilter.value || lifeEventFilter.value || typeFilter.value || groupFilter.value;
  });

  const getMdaName = (mdaId) => {
    const mda = mdas.value.find(m => m.id === mdaId);
    if (!mda) return 'N/A';
    return mda.code ? `${mda.name} (${mda.code})` : mda.name;
  };

  const getGroupName = (groupId) => {
    const group = groups.value.find(g => g.id === Number(groupId));
    return group ? group.name : 'Unknown Group';
  };

  const handleUpdate = async () => {
    if (editForm.value.id) {
      await serviceConfigStore.updateService(editForm.value);
    } else {
      try {
        await serviceConfigStore.createService(editForm.value);
      } catch (e) {
        alert('Failed to create service. Ensure Service Code is unique.');
        return;
      }
    }
    closeModal();
  };

  const openCreateModal = () => {
    editForm.value = {
      id: null,
      service_code: '',
      service_name: '',
      mda: mdas.value.length > 0 ? mdas.value[0].id : null,
      service_type: 'G2C',
      service_groups: [],
      config: { rules: { schema: { properties: {}, required: [] } } },
    };
    showModal.value = true;
  };

  const openEditModal = (service) => {
    // Deep copy to avoid reactive mutations outside of the store
    editForm.value = JSON.parse(JSON.stringify(service));

    // Ensure IDs are flat for select/checkbox bindings
    if (service.service_family_details) {
      editForm.value.service_family = service.service_family_details.id;
    }
    
    // Explicitly set service_groups to a list of IDs for binary checkbox binding
    if (service.service_groups) {
      editForm.value.service_groups = service.service_groups;
    }

    if (!editForm.value.config || !editForm.value.config.rules || !editForm.value.config.rules.schema) {
      editForm.value.config = { rules: { schema: { properties: {}, required: [] } } };
    }
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
  };

  const deleteService = async (id) => {
    if (confirm('Are you sure you want to delete this Service Configuration? It will also delete all associated workflow steps.')) {
      await serviceConfigStore.deleteService(id);
    }
  };
</script>

<style scoped>
  .text-muted {
    color: var(--text-muted);
  }

  .text-main {
    color: var(--text-main);
  }

  .text-primary {
    color: var(--primary);
  }

  .text-danger {
    color: var(--danger);
  }

  .bg-bg-page {
    background-color: var(--bg-page);
  }

  .border-border-color {
    border-color: var(--border-color);
  }

  /* Configuration Journey Navigation */
  .config-nav-item {
    box-sizing: border-box;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1rem 1.25rem;
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 1rem;
    text-align: left;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .config-nav-item:hover:not(.config-nav-item--disabled) {
    border-color: var(--primary);
    transform: translateX(4px);
    box-shadow: 0 10px 20px -10px rgba(0, 0, 0, 0.1);
  }

  .config-nav-item--active {
    background: var(--bg-page);
    border-color: var(--primary);
    border-width: 2px;
    box-shadow: 0 10px 25px -10px rgba(var(--primary-rgb), 0.2);
  }

  .config-nav-item--disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background: #f8fafc;
  }

  .config-nav-item__index {
    width: 2.25rem;
    height: 2.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f1f5f9;
    border-radius: 0.75rem;
    font-size: 0.7rem;
    font-weight: 900;
    color: var(--text-muted);
    transition: all 0.3s ease;
  }

  .config-nav-item--active .config-nav-item__index {
    background: var(--primary);
    color: white;
    transform: scale(1.1);
  }

  .config-nav-item__content {
    display: flex;
    flex-direction: column;
  }

  .config-nav-item__title {
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--text-main);
    text-transform: uppercase;
    letter-spacing: -0.01em;
  }

  .config-nav-item__desc {
    font-size: 0.7rem;
    color: var(--text-muted);
    opacity: 0.7;
  }

  .config-nav-item--active .config-nav-item__title {
    color: var(--primary);
  }

  /* ICTA Premium Design System for Registry */
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

  /* Table Adjustments */
  .table__header-row {
    background: var(--grad-premium) !important;
    color: white !important;
  }

  .table__header-cell {
    color: white !important;
  }

</style>
