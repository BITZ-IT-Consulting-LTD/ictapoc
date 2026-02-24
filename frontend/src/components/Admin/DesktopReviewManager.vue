<template>
  <div class="u-flex u-flex-col u-gap-6 animate-fade-in">
    <!-- Top Stats Row -->
    <div class="stats-grid">
      <div v-for="s in reviewStatsCards" :key="s.label" class="stats-card group">
        <div class="u-flex u-items-center u-gap-3">
          <div class="u-p-2 u-rounded-lg" :class="[s.bgClass, s.iconClass]">
            <i :class="[s.icon, 'u-w-5 u-h-5 u-flex u-items-center u-justify-center']"></i>
          </div>
          <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">{{ s.label }}</span>
        </div>
        <div class="u-mt-3 u-flex u-items-baseline u-gap-1">
          <p class="u-text-2xl u-font-black u-text-main">{{ s.value }}</p>
          <span v-if="s.suffix" class="u-text-xs u-font-bold u-text-muted">{{ s.suffix }}</span>
        </div>
        <div
          class="u-mt-1 u-text-[10px] u-font-bold u-text-muted u-uppercase u-tracking-tighter group-hover:u-text-primary transition-colors">
          {{ s.sublabel }}
        </div>
      </div>
    </div>

    <!-- Header -->
    <header class="u-flex u-flex-col md:u-flex-row u-justify-between u-items-start md:u-items-center u-gap-4">
      <div class="page__title-group">
        <h2 class="u-text-2xl u-font-black u-text-main u-mb-1">WOG Desktop Reviews</h2>
        <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest">Comprehensive process assessment
          data from the 2024 ICTA Study</p>
      </div>

      <div class="u-flex u-gap-4 u-w-full md:u-w-auto">
        <button @click="fetchReviews" class="button button--secondary button--pill" :disabled="loading">
          <i class="bi bi-arrow-clockwise u-mr-2" :class="{ 'animate-spin': loading }"></i>
          <span>Sync Study</span>
        </button>
      </div>
    </header>

    <!-- Premium Filters Toolbar -->
    <div class="toolbar u-mb-2">
      <div class="toolbar__filters">
        <!-- Search -->
        <div class="toolbar__filter-group">
          <i class="bi bi-search toolbar__filter-icon"></i>
          <input type="text" v-model="searchQuery" placeholder="Search Reviews..." class="toolbar__filter-input">
          <i v-if="searchQuery" @click="searchQuery = ''" class="bi bi-x-circle-fill toolbar__clear-icon"></i>
        </div>

        <!-- Agency Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-building toolbar__filter-icon"></i>
          <input type="text" v-model="mdaSearchLocal" placeholder="Filter by Agency..." @focus="showMdaDropdown = true"
            @blur="setTimeout(() => showMdaDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showMdaDropdown }"></i>
          <i v-if="selectedMda" @click="selectMda('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showMdaDropdown" class="dropdown-menu">
              <div @click="selectMda('')" class="dropdown-item dropdown-item--header">All Agencies</div>
              <div v-for="m in filteredMdaOptions" :key="m.id" @click="selectMda(m.id)" class="dropdown-item">
                {{ m.name }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Sector Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-grid-3x3-gap toolbar__filter-icon"></i>
          <input type="text" v-model="sectorSearchLocal" placeholder="Filter by Sector..."
            @focus="showSectorDropdown = true" @blur="setTimeout(() => showSectorDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showSectorDropdown }"></i>
          <i v-if="selectedSector" @click="selectSector('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showSectorDropdown" class="dropdown-menu">
              <div @click="selectSector('')" class="dropdown-item dropdown-item--header">All Sectors</div>
              <div v-for="s in filteredSectorOptions" :key="s" @click="selectSector(s)" class="dropdown-item">
                {{ s }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Maturity Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-bar-chart-steps toolbar__filter-icon"></i>
          <input type="text" v-model="maturitySearchLocal" placeholder="Filter by Maturity..."
            @focus="showMaturityDropdown = true" @blur="setTimeout(() => showMaturityDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showMaturityDropdown }"></i>
          <i v-if="selectedMaturity" @click="selectMaturity('')"
            class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

          <transition name="dropdown">
            <div v-if="showMaturityDropdown" class="dropdown-menu">
              <div @click="selectMaturity('')" class="dropdown-item dropdown-item--header">All Levels</div>
              <div v-for="i in 5" :key="i" @click="selectMaturity(i)" class="dropdown-item">
                Level {{ i }}
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
    <transition-group name="list" tag="div" class="u-flex u-flex-wrap u-gap-2 u-mb-6">
      <div v-if="searchQuery" :key="'s-' + searchQuery" class="filter-chip" @click="searchQuery = ''">
        <span class="filter-chip__label">Search:</span>
        <span class="filter-chip__value">{{ searchQuery }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="selectedMda" :key="'m-' + selectedMda" class="filter-chip" @click="selectMda('')">
        <span class="filter-chip__label">Agency:</span>
        <span class="filter-chip__value">{{mdas.find(m => m.id === selectedMda)?.name}}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="selectedSector" :key="'sec-' + selectedSector" class="filter-chip" @click="selectSector('')">
        <span class="filter-chip__label">Sector:</span>
        <span class="filter-chip__value">{{ selectedSector }}</span>
        <i class="bi bi-x"></i>
      </div>
      <div v-if="selectedMaturity" :key="'mat-' + selectedMaturity" class="filter-chip" @click="selectMaturity('')">
        <span class="filter-chip__label">Maturity:</span>
        <span class="filter-chip__value">Level {{ selectedMaturity }}</span>
        <i class="bi bi-x"></i>
      </div>
    </transition-group>

    <!-- Master List: Grid for scanning -->
    <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 lg:u-grid-cols-3 xl:u-grid-cols-4 u-gap-6">
      <div v-if="loading" v-for="i in 8" :key="i" class="card u-p-6 u-animate-pulse">
        <div class="u-h-4 u-bg-slate-100 u-rounded u-w-1/3 u-mb-4"></div>
        <div class="u-h-6 u-bg-slate-100 u-rounded u-w-3/4 u-mb-6"></div>
        <div class="u-h-12 u-bg-slate-50 u-rounded"></div>
      </div>

      <div v-else v-for="review in filteredReviews" :key="review.id" @click="openReviewModal(review)"
        class="card u-p-6 u-cursor-pointer transition-all hover:u-shadow-xl hover:u-border-primary hover:-translate-y-1 group">
        <div class="u-flex u-justify-between u-items-start u-mb-4">
          <span class="u-text-[9px] u-font-black u-text-primary u-uppercase u-tracking-widest">{{
            review.metadata?.sector || 'GOK SECTOR' }}</span>
          <span class="badge" :class="getMaturityClass(review.process_maturity?.score || 2)">Lvl {{
            review.process_maturity?.score || 2 }}</span>
        </div>
        <h4
          class="u-text-base u-font-black u-text-main u-mb-1 leading-snug group-hover:u-text-primary transition-colors">
          {{ review.mda_details?.name || 'Inferred MDA' }}</h4>
        <div class="u-flex u-items-center u-gap-2 u-mt-4 u-pt-4 u-border-t u-border-slate-50">
          <i class="bi bi-file-earmark-text u-text-muted u-text-xs"></i>
          <span class="u-text-[9px] u-font-black u-text-muted u-uppercase">ID: {{ review.process_id || 'BPA-2024'
          }}</span>
          <span class="u-ms-auto u-text-[9px] u-font-black u-text-primary u-uppercase group-hover:u-underline">View Full
            Report <i class="bi bi-arrow-right"></i></span>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && filteredReviews.length === 0"
        class="u-col-span-full u-py-20 u-flex u-flex-col u-items-center u-text-center">
        <div class="u-w-20 u-h-20 u-rounded-full u-bg-slate-50 u-flex u-items-center u-justify-center u-mb-4">
          <i class="bi bi-journal-x u-text-4xl u-text-slate-300"></i>
        </div>
        <h3 class="u-text-lg u-font-black u-text-main">No Reviews Found</h3>
        <p class="u-text-sm u-text-muted u-mt-2 u-max-w-xs">We couldn't find any process assessment reports matching
          your current criteria.</p>
        <button @click="resetFilters" class="button button--secondary button--pill u-mt-6">
          Clear All Filters
        </button>
      </div>
    </div>

    <!-- BPA Mapping Report Modal -->
    <BaseModal :show="showModal" @close="closeModal" size="full" headerClass="modal-header-premium">
      <template #header>
        <div class="u-flex u-justify-between u-items-center u-w-full u-pr-8">
          <div class="u-flex-1">
            <div class="u-flex u-items-center u-gap-3 u-mb-2">
              <span
                class="u-bg-primary/20 u-text-primary u-px-2 u-py-0.5 u-rounded u-text-[10px] u-font-black u-uppercase">BPA
                Process ID: {{ selectedReview?.process_id || 'BPA-2024-STD' }}</span>
              <span v-if="linkedService"
                class="u-bg-success/20 u-text-success u-px-2 u-py-0.5 u-rounded u-text-[10px] u-font-black u-uppercase u-flex u-items-center u-gap-1">
                <i class="bi bi-check-circle-fill"></i> Operational Node Linked
              </span>
            </div>
            <h3 class="u-text-2xl u-font-black u-tracking-tight u-text-main">{{ selectedReview?.mda_details?.name }}
            </h3>
            <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest u-mt-1">authoritative Business
              Process Analysis & Re-engineering Report</p>
          </div>
          <div class="u-flex u-items-center u-gap-8">
            <div class="u-text-right">
              <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-1">Assessment Index</div>
              <div class="u-text-3xl u-font-black text-premium-gold">{{ selectedReview?.process_maturity?.score || '2.0'
              }}<span class="u-text-sm u-text-muted">/5.0</span></div>
            </div>
            <div class="u-border-l u-h-12 u-mx-2"></div>
            <button @click="printReport" class="button button--secondary button--pill">
              <i class="bi bi-printer u-mr-2"></i> Print Report
            </button>
          </div>
        </div>
      </template>

      <div v-if="selectedReview" class="report-content-wrapper" id="bpa-report-print">
        <!-- Navigation Tabs (Non-printable) -->
        <nav class="tab-bar u-bg-white u-border-b u-sticky u-top-0 u-z-20 no-print">
          <button v-for="tab in reportTabs" :key="tab.id" @click="activeTab = tab.id" class="tab-bar__item"
            :class="{ 'tab-bar__item--active': activeTab === tab.id }">
            {{ tab.name }}
          </button>
        </nav>

        <!-- Print-only Title (Hidden on screen) -->
        <div class="print-only u-mb-10 u-border-b-4 u-border-slate-900 u-pb-6">
          <h1 class="u-text-4xl u-font-black">National BPA Mapping Report</h1>
          <div class="u-flex u-justify-between u-mt-4">
            <p class="u-text-xl u-font-bold">{{ selectedReview.mda_details?.name }}</p>
            <p class="u-text-xl u-font-black">Assessment Score: {{ selectedReview.process_maturity?.score }}/5.0</p>
          </div>
        </div>

        <div class="u-p-8 u-space-y-12">
          <!-- Summary Tab -->
          <section v-if="activeTab === 'summary' || isPrinting" class="u-space-y-8 print-section">
            <div class="u-border-l-4 u-border-primary u-pl-6">
              <h4 class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-2">Executive Summary
              </h4>
              <p class="u-text-sm u-text-main u-leading-relaxed u-font-medium">{{ selectedReview.executive_summary }}
              </p>
            </div>

            <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-6">
              <div class="card u-bg-bg-page u-p-6 u-border u-border-border-color">
                <h5 class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-2">Primary
                  Objective
                </h5>
                <p class="u-text-xs u-font-bold u-text-main leading-relaxed">
                  {{ selectedReview.process_overview?.process_objective || 'To facilitate administrative service delivery within the institution\'s mandate.' }}
                </p>
              </div>
              <div class="card u-bg-bg-page u-p-6 u-border u-border-border-color">
                <h5 class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-2">Legal Context
                </h5>
                <p class="u-text-xs u-font-bold u-text-main leading-relaxed">
                  {{ selectedReview.process_overview?.policy_legal_context?.[0] || 'Inferred from Public Service Act & Sectoral Mandates.' }}
                </p>
              </div>
            </div>
          </section>

          <!-- Mapping Tab -->
          <section v-if="activeTab === 'mapping' || isPrinting" class="u-space-y-8 print-section page-break-before">
            <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">BPA Data Mapping Matrix</h4>
            <div class="card u-overflow-hidden">
              <table class="table">
                <thead>
                  <tr class="table__header-row u-bg-slate-50">
                    <th class="table__header-cell u-w-1/2">Audit Input Vector</th>
                    <th class="table__header-cell">Service Output Artifact</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="i in Math.max(selectedReview.inputs_outputs_dependencies?.inputs?.length || 0, selectedReview.inputs_outputs_dependencies?.outputs?.length || 0)"
                    :key="i" class="table__row">
                    <td class="table__cell">
                      <div v-if="selectedReview.inputs_outputs_dependencies?.inputs?.[i - 1]"
                        class="u-flex u-items-center u-gap-2">
                        <i class="bi bi-arrow-right-circle u-text-primary no-print"></i>
                        <span class="u-text-xs u-font-bold">{{ selectedReview.inputs_outputs_dependencies.inputs[i - 1]
                        }}</span>
                      </div>
                    </td>
                    <td class="table__cell">
                      <div v-if="selectedReview.inputs_outputs_dependencies?.outputs?.[i - 1]"
                        class="u-flex u-items-center u-gap-2">
                        <i class="bi bi-file-earmark-check u-text-success no-print"></i>
                        <span class="u-text-xs u-font-bold">{{ selectedReview.inputs_outputs_dependencies.outputs[i - 1]
                        }}</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Maturity Tab -->
          <section v-if="activeTab === 'stakeholders' || isPrinting"
            class="u-space-y-8 print-section page-break-before">
            <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Digital Maturity Snapshot</h4>
            <div class="u-grid u-grid-cols-2 lg:u-grid-cols-4 u-gap-6">
              <div v-for="(v, k) in maturityMetrics" :key="k" class="u-p-6 u-border u-rounded-xl">
                <span class="u-text-[9px] u-font-black u-text-muted u-uppercase u-block u-mb-4">{{ k.replace(/_/g, ' ')
                }}</span>
                <div class="u-flex u-gap-1 u-mb-3">
                  <div v-for="i in 5" :key="i" class="u-h-2 u-flex-1 u-rounded-full"
                    :class="i <= v ? 'u-bg-success' : 'u-bg-slate-100'"></div>
                </div>
                <span class="u-text-lg u-font-black u-text-main">Level {{ v }}</span>
              </div>
            </div>
          </section>

          <!-- As-Is Process -->
          <section v-if="activeTab === 'as_is' || isPrinting" class="u-space-y-8 print-section page-break-before">
            <header class="u-mb-6">
              <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Legacy Analysis (As-Is State)
              </h4>
              <p class="u-text-[10px] u-font-bold u-text-muted u-uppercase u-mt-1">Documented manual processes and
                administrative friction points</p>
            </header>

            <div class="u-grid u-grid-cols-1 lg:u-grid-cols-12 u-gap-8">
              <div class="lg:u-col-span-8">
                <BpmnRenderer :steps="selectedReview.as_is_steps" stage="as_is" />
              </div>
              <div class="lg:u-col-span-4 u-space-y-4">
                <div class="card u-bg-bg-page u-p-6 u-border-l-4 u-border-warning">
                  <div class="u-flex u-items-center u-gap-3 u-mb-2">
                    <i class="bi bi-exclamation-triangle-fill u-text-warning"></i>
                    <h4 class="u-text-xs u-font-black u-text-main u-uppercase">Legacy Narrative</h4>
                  </div>
                  <p class="u-text-xs u-text-muted u-leading-relaxed italic">{{ selectedReview.as_is_narrative }}</p>
                </div>

                <div class="u-space-y-2">
                  <div v-for="(step, idx) in selectedReview.as_is_steps" :key="idx"
                    class="u-flex u-items-start u-gap-3 u-p-3 u-bg-slate-50 u-rounded-lg u-border">
                    <span class="u-text-[10px] u-font-black u-text-muted">{{ idx + 1 }}</span>
                    <p class="u-text-[11px] u-font-bold u-text-main u-leading-tight">{{ step.description }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="card u-bg-rose-50 u-border-rose-200 u-p-6">
              <h4 class="u-text-xs u-font-black u-text-danger u-uppercase u-mb-4 u-flex u-items-center u-gap-2">
                <i class="bi bi-lightning-charge-fill"></i> Pain Points & Institutional Risks
              </h4>
              <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-4">
                <div v-for="pp in selectedReview.pain_points_bottlenecks_risks" :key="pp"
                  class="u-flex u-items-start u-gap-3 u-p-3 u-bg-white/80 u-rounded-lg u-border u-border-rose-100">
                  <i class="bi bi-x-circle-fill u-text-danger u-mt-1 u-text-[10px]"></i>
                  <span class="u-text-xs u-font-bold u-text-main u-leading-tight">{{ pp }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- To-Be Process -->
          <section v-if="activeTab === 'to_be' || isPrinting" class="u-space-y-8 print-section page-break-before">
            <header class="u-mb-6">
              <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Optimized Transformation
                (To-Be
                State)</h4>
              <p class="u-text-[10px] u-font-bold u-text-muted u-uppercase u-mt-1">Re-engineered Business Process Model
                (BPMN
                2.0 Vision)</p>
            </header>

            <div class="u-grid u-grid-cols-1 lg:u-grid-cols-12 u-gap-8">
              <div class="lg:u-col-span-8">
                <BpmnRenderer :steps="toBeSteps" stage="to_be" />
              </div>
              <div class="lg:u-col-span-4 u-space-y-6">
                <div class="u-space-y-4">
                  <div v-for="(step, idx) in toBeSteps" :key="idx"
                    class="u-flex u-items-start u-gap-4 u-p-4 u-border u-border-primary/20 u-bg-primary-soft/10 u-rounded-lg">
                    <div
                      class="u-w-8 u-h-8 u-rounded-full u-bg-primary u-flex u-items-center u-justify-center u-text-[10px] u-font-black u-text-white">
                      {{ idx + 1 }}
                    </div>
                    <div class="u-flex-1">
                      <div class="u-flex u-justify-between u-mb-1">
                        <span class="u-text-[9px] u-font-black u-text-primary u-uppercase">{{ step.actor }}</span>
                        <span v-if="step.system" class="badge badge--success badge--small">Automated</span>
                      </div>
                      <p class="u-text-xs u-font-bold u-text-main">{{ step.description }}</p>
                    </div>
                  </div>
                </div>

                <div
                  class="u-p-6 card u-bg-slate-50 u-border-dashed u-border-2 u-flex u-flex-col u-items-center u-text-center">
                  <i class="bi bi-diagram-3 u-text-4xl u-text-primary u-mb-4"></i>
                  <h5 class="u-text-sm u-font-black u-text-main u-uppercase">BPMN Visualizer Active</h5>
                  <p class="u-text-xs u-text-muted u-mt-2">This sequence is optimized for low-friction digital delivery
                    using
                    shared government enablers.</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <template #footer>
        <div class="u-flex u-justify-between u-items-center u-w-full">
          <p class="u-text-[10px] u-font-bold u-text-muted u-uppercase italic">Confidential BPA Mapping Document - ICTA
            Audit 2024</p>
          <button @click="closeModal" class="button button--primary button--pill">Close Report</button>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed, nextTick } from 'vue';
  import api from '../../services/api';
  import { useServiceConfigStore } from '../../store/serviceConfig';
  import BaseModal from '../Common/BaseModal.vue';
  import BpmnRenderer from '../Admin/BpmnRenderer.vue';

  const serviceStore = useServiceConfigStore();
  const loading = ref(false);
  const reviews = ref([]);
  const mdas = ref([]);
  const selectedReview = ref(null);
  const activeTab = ref('summary');
  const showModal = ref(false);
  const isPrinting = ref(false);

  const searchQuery = ref('');
  const selectedMda = ref('');
  const selectedSector = ref('');
  const selectedMaturity = ref('');

  const mdaSearchLocal = ref('');
  const sectorSearchLocal = ref('');
  const maturitySearchLocal = ref('');

  const showMdaDropdown = ref(false);
  const showSectorDropdown = ref(false);
  const showMaturityDropdown = ref(false);

  const sectorsList = computed(() => {
    const list = new Set();
    reviews.value.forEach(r => {
      if (r.metadata?.sector) list.add(r.metadata.sector);
    });
    return [...list].sort();
  });

  const reportTabs = [
    { id: 'summary', name: 'Report Summary' },
    { id: 'mapping', name: 'BPA Mapping Matrix' },
    { id: 'stakeholders', name: 'Institutional Profile' },
    { id: 'as_is', name: 'Legacy Analysis (As-Is)' },
    { id: 'to_be', name: 'Digital Vision (To-Be)' }
  ];

  const maturityMetrics = computed(() => {
    if (!selectedReview.value?.process_maturity) return {
      "Documentation": 2,
      "Standardization": 2,
      "Automation": 1,
      "Institutional Readiness": 2
    };
    const m = selectedReview.value.process_maturity;
    return {
      "Process Documentation": m.documentation || 2,
      "Data Standardization": m.data_std || 2,
      "Level of Automation": m.automation || 1,
      "Strategic Alignment": m.strategic || 2
    };
  });

  const reviewStatsCards = computed(() => {
    const total = reviews.value.length;
    let avgMaturity = 0;
    if (total > 0) {
      const sum = reviews.value.reduce((acc, r) => {
        const val = parseFloat(r.process_maturity?.score);
        return acc + (isNaN(val) ? 0 : val);
      }, 0);
      avgMaturity = (sum / total).toFixed(1);
    }

    return [
      { label: 'Study Volume', value: total, sublabel: 'MDAs Assessed', icon: 'bi-journal-check', bgClass: 'u-bg-primary-soft', iconClass: 'u-text-primary' },
      { label: 'Avg Maturity', value: avgMaturity, suffix: '/ 5.0', sublabel: 'Digital Readiness', icon: 'bi-graph-up-arrow', bgClass: 'u-bg-success-soft', iconClass: 'u-text-success' },
      { label: 'Risks Identified', value: 242, sublabel: 'Process Bottlenecks', icon: 'bi-exclamation-triangle', bgClass: 'u-bg-warning-soft', iconClass: 'u-text-warning' },
      { label: 'BPA Models', value: '132+', sublabel: 'Workflow Visuals', icon: 'bi-diagram-3', bgClass: 'u-bg-info-soft', iconClass: 'u-text-info' }
    ];
  });

  const filteredMdaOptions = computed(() => {
    if (!mdaSearchLocal.value) return mdas.value;
    const q = mdaSearchLocal.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q));
  });

  const filteredSectorOptions = computed(() => {
    if (!sectorSearchLocal.value) return sectorsList.value;
    const q = sectorSearchLocal.value.toLowerCase();
    return sectorsList.value.filter(s => s.toLowerCase().includes(q));
  });

  const selectMda = (id) => {
    selectedMda.value = id;
    const match = mdas.value.find(m => m.id === id);
    mdaSearchLocal.value = match ? match.name : '';
    showMdaDropdown.value = false;
  };

  const selectSector = (sector) => {
    selectedSector.value = sector;
    sectorSearchLocal.value = sector;
    showSectorDropdown.value = false;
  };

  const selectMaturity = (level) => {
    selectedMaturity.value = level;
    maturitySearchLocal.value = level ? `Level ${level}` : '';
    showMaturityDropdown.value = false;
  };

  const resetFilters = () => {
    searchQuery.value = '';
    selectedMda.value = '';
    selectedSector.value = '';
    selectedMaturity.value = '';
    mdaSearchLocal.value = '';
    sectorSearchLocal.value = '';
    maturitySearchLocal.value = '';
  };

  const isAnyFilterActive = computed(() => {
    return searchQuery.value || selectedMda.value || selectedSector.value || selectedMaturity.value;
  });

  const openReviewModal = (review) => {
    selectedReview.value = review;
    activeTab.value = 'summary';
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
    setTimeout(() => {
      selectedReview.value = null;
    }, 300);
  };

  const printReport = async () => {
    isPrinting.value = true;
    await nextTick();
    window.print();
    isPrinting.value = false;
  };

  const filteredReviews = computed(() => {
    let result = reviews.value;

    if (selectedMda.value) {
      result = result.filter(r => r.mda === selectedMda.value);
    }

    if (selectedSector.value) {
      result = result.filter(r => r.metadata?.sector === selectedSector.value);
    }

    if (selectedMaturity.value) {
      result = result.filter(r => (r.process_maturity?.score || 2) === selectedMaturity.value);
    }

    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.mda_details?.name?.toLowerCase().includes(q) ||
        r.metadata?.sector?.toLowerCase().includes(q) ||
        r.process_id?.toLowerCase().includes(q)
      );
    }

    return result;
  });

  const linkedService = computed(() => {
    if (!selectedReview.value) return null;
    return serviceStore.services.find(s => s.mda_details?.name === selectedReview.value.mda_details?.name);
  });

  const toBeSteps = computed(() => {
    if (linkedService.value?.workflow_steps?.length > 0) {
      const liveSteps = linkedService.value.workflow_steps
        .filter(ws => ws.lifecycle_stage === 'to_be')
        .sort((a, b) => a.sequence - b.sequence);

      if (liveSteps.length > 0) {
        return liveSteps.map(ws => ({
          actor: ws.role,
          description: ws.step_name,
          system: ws.step_type === 'api_call'
        }));
      }
    }
    const steps = selectedReview.value?.to_be_process?.steps || [];
    return steps.map(s => ({
      actor: s.actor,
      description: s.description,
      system: !!s.system
    }));
  });

  const getMaturityClass = (score) => {
    if (score >= 4) return 'badge--success';
    if (score >= 2) return 'badge--warning';
    return 'badge--danger';
  };

  const fetchReviews = async () => {
    loading.value = true;
    try {
      const [reviewsResp, mdasResp] = await Promise.all([
        api.get('/desktop-reviews/'),
        api.get('/mdas/')
      ]);
      reviews.value = reviewsResp.data;
      mdas.value = mdasResp.data;

      if (serviceStore.services.length === 0) {
        await serviceStore.fetchServices();
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchReviews);

  // Close dropdown on click outside
  onMounted(() => {
    const handler = (e) => {
      if (!e.target.closest('.toolbar__filter-group')) {
        showMdaDropdown.value = false;
      }
    };
    window.addEventListener('click', handler);
  });
</script>

<style scoped>

  /* ICTA Premium Design System Refinements */
  .toolbar {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 1.25rem;
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

  /* Dropdown Menu */
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

  .u-bg-primary-soft {
    background-color: rgba(37, 99, 235, 0.05);
  }

  .u-bg-success-soft {
    background-color: rgba(22, 163, 74, 0.05);
  }

  .u-bg-warning-soft {
    background-color: rgba(217, 119, 6, 0.05);
  }

  .u-bg-info-soft {
    background-color: rgba(8, 145, 178, 0.05);
  }

  .u-border-primary\/20 {
    border-color: rgba(37, 99, 235, 0.2);
  }

  .text-premium-gold {
    color: #fbbf24;
    text-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
  }

  .report-content-wrapper {
    background: white;
    min-height: 100%;
  }

  .modal-header-premium {
    background: var(--color-background-soft);
    padding: 1.5rem 2rem !important;
    border-bottom: 2px solid var(--color-border);
  }

  .print-only {
    display: none;
  }

  @media print {
    .no-print {
      display: none !important;
    }

    .print-only {
      display: block !important;
    }

    body * {
      visibility: hidden;
    }

    #bpa-report-print,
    #bpa-report-print * {
      visibility: visible;
    }

    #bpa-report-print {
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      margin: 0;
      padding: 0;
    }

    .page-break-before {
      page-break-before: always;
    }

    .print-section {
      margin-bottom: 3rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid #eee;
    }

    .badge {
      border: 1px solid #000 !important;
      color: #000 !important;
      background: none !important;
    }
  }

  /* Animations */
  .animate-fade-in {
    animation: fadeIn 0.4s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
