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
        <div class="u-mt-1 u-text-[10px] u-font-bold u-text-muted u-uppercase u-tracking-tighter group-hover:u-text-primary transition-colors">
          {{ s.sublabel }}
        </div>
      </div>
    </div>

    <!-- Header & Actions -->
    <header class="u-flex u-flex-col md:u-flex-row u-justify-between u-items-start md:u-items-center u-gap-4">
      <div class="page__title-group">
        <h2 class="u-text-2xl u-font-black u-text-main u-mb-1">WOG Desktop Reviews</h2>
        <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest">Comprehensive process assessment data from the 2024 ICTA Study</p>
      </div>
      
      <div class="u-flex u-gap-4 u-w-full md:u-w-auto">
        <div class="u-relative u-flex-1 md:u-w-64">
          <div class="toolbar__filter-group u-shadow-none u-border u-border-border-color">
            <i class="bi bi-building toolbar__filter-icon"></i>
            <input type="text" v-model="mdaSearchLocal" placeholder="Filter by Agency..." 
              @focus="showMdaDropdown = true" 
              class="toolbar__filter-input u-w-full" />
            
            <div v-if="showMdaDropdown" class="u-absolute u-top-full u-left-0 u-w-full u-bg-white u-border u-shadow-xl u-rounded-lg u-mt-1 u-z-dropdown u-max-h-60 u-overflow-y-auto u-p-1">
              <div @click="selectMda('')" class="u-p-3 hover:u-bg-bg-page u-rounded u-text-xs u-font-black u-text-primary u-cursor-pointer">ALL AGENCIES</div>
              <div v-for="m in filteredMdaOptions" :key="m.id" @click="selectMda(m.id)" 
                class="u-p-3 hover:u-bg-bg-page u-rounded u-text-xs u-font-bold u-text-main u-cursor-pointer">
                {{ m.name }}
              </div>
            </div>
          </div>
        </div>
        <button @click="fetchReviews" class="button button--secondary button--pill" :disabled="loading">
          <i class="bi bi-arrow-clockwise u-mr-2" :class="{ 'animate-spin': loading }"></i>
          <span>Sync Study</span>
        </button>
      </div>
    </header>

    <!-- Master List: Grid for scanning -->
    <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 lg:u-grid-cols-3 xl:u-grid-cols-4 u-gap-6">
      <div v-if="loading" v-for="i in 8" :key="i" class="card u-p-6 u-animate-pulse">
        <div class="u-h-4 u-bg-slate-100 u-rounded u-w-1/3 u-mb-4"></div>
        <div class="u-h-6 u-bg-slate-100 u-rounded u-w-3/4 u-mb-6"></div>
        <div class="u-h-12 u-bg-slate-50 u-rounded"></div>
      </div>
      
      <div v-else v-for="review in filteredReviews" :key="review.id" 
        @click="openReviewModal(review)"
        class="card u-p-6 u-cursor-pointer transition-all hover:u-shadow-xl hover:u-border-primary hover:-translate-y-1 group">
        <div class="u-flex u-justify-between u-items-start u-mb-4">
          <span class="u-text-[9px] u-font-black u-text-primary u-uppercase u-tracking-widest">{{ review.metadata?.sector || 'GOK SECTOR' }}</span>
          <span class="badge" :class="getMaturityClass(review.process_maturity?.score || 2)">Lvl {{ review.process_maturity?.score || 2 }}</span>
        </div>
        <h4 class="u-text-base u-font-black u-text-main u-mb-1 leading-snug group-hover:u-text-primary transition-colors">{{ review.mda_details?.name || 'Inferred MDA' }}</h4>
        <div class="u-flex u-items-center u-gap-2 u-mt-4 u-pt-4 u-border-t u-border-slate-50">
          <i class="bi bi-file-earmark-text u-text-muted u-text-xs"></i>
          <span class="u-text-[9px] u-font-black u-text-muted u-uppercase">ID: {{ review.process_id || 'BPA-2024' }}</span>
          <span class="u-ms-auto u-text-[9px] u-font-black u-text-primary u-uppercase group-hover:u-underline">View Full Report <i class="bi bi-arrow-right"></i></span>
        </div>
      </div>
    </div>

    <!-- BPA Mapping Report Modal -->
    <BaseModal :show="showModal" @close="closeModal" size="full" headerClass="modal-header-premium">
      <template #header>
        <div class="u-flex u-justify-between u-items-center u-w-full u-pr-8">
          <div class="u-flex-1">
            <div class="u-flex u-items-center u-gap-3 u-mb-2">
              <span class="u-bg-primary/20 u-text-primary u-px-2 u-py-0.5 u-rounded u-text-[10px] u-font-black u-uppercase">BPA Process ID: {{ selectedReview?.process_id || 'BPA-2024-STD' }}</span>
              <span v-if="linkedService" class="u-bg-success/20 u-text-success u-px-2 u-py-0.5 u-rounded u-text-[10px] u-font-black u-uppercase u-flex u-items-center u-gap-1">
                <i class="bi bi-check-circle-fill"></i> Operational Node Linked
              </span>
            </div>
            <h3 class="u-text-2xl u-font-black u-tracking-tight u-text-main">{{ selectedReview?.mda_details?.name }}</h3>
            <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest u-mt-1">authoritative Business Process Analysis & Re-engineering Report</p>
          </div>
          <div class="u-flex u-items-center u-gap-8">
            <div class="u-text-right">
              <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-1">Assessment Index</div>
              <div class="u-text-3xl u-font-black text-premium-gold">{{ selectedReview?.process_maturity?.score || '2.0' }}<span class="u-text-sm u-text-muted">/5.0</span></div>
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
          <button v-for="tab in reportTabs" :key="tab.id" @click="activeTab = tab.id"
            class="tab-bar__item" :class="{ 'tab-bar__item--active': activeTab === tab.id }">
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
              <h4 class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-2">Executive Summary</h4>
              <p class="u-text-sm u-text-main u-leading-relaxed u-font-medium">{{ selectedReview.executive_summary }}</p>
            </div>

            <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-6">
              <div class="card u-bg-bg-page u-p-6 u-border u-border-border-color">
                <h5 class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-2">Primary Objective</h5>
                <p class="u-text-xs u-font-bold u-text-main leading-relaxed">
                  {{ selectedReview.process_overview?.process_objective || 'To facilitate administrative service delivery within the institution\'s mandate.' }}
                </p>
              </div>
              <div class="card u-bg-bg-page u-p-6 u-border u-border-border-color">
                <h5 class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-2">Legal Context</h5>
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
                  <tr v-for="i in Math.max(selectedReview.inputs_outputs_dependencies?.inputs?.length || 0, selectedReview.inputs_outputs_dependencies?.outputs?.length || 0)" :key="i" class="table__row">
                    <td class="table__cell">
                      <div v-if="selectedReview.inputs_outputs_dependencies?.inputs?.[i-1]" class="u-flex u-items-center u-gap-2">
                        <i class="bi bi-arrow-right-circle u-text-primary no-print"></i>
                        <span class="u-text-xs u-font-bold">{{ selectedReview.inputs_outputs_dependencies.inputs[i-1] }}</span>
                      </div>
                    </td>
                    <td class="table__cell">
                      <div v-if="selectedReview.inputs_outputs_dependencies?.outputs?.[i-1]" class="u-flex u-items-center u-gap-2">
                        <i class="bi bi-file-earmark-check u-text-success no-print"></i>
                        <span class="u-text-xs u-font-bold">{{ selectedReview.inputs_outputs_dependencies.outputs[i-1] }}</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Maturity Tab -->
          <section v-if="activeTab === 'stakeholders' || isPrinting" class="u-space-y-8 print-section page-break-before">
             <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Digital Maturity Snapshot</h4>
             <div class="u-grid u-grid-cols-2 lg:u-grid-cols-4 u-gap-6">
                <div v-for="(v, k) in maturityMetrics" :key="k" class="u-p-6 u-border u-rounded-xl">
                  <span class="u-text-[9px] u-font-black u-text-muted u-uppercase u-block u-mb-4">{{ k.replace(/_/g, ' ') }}</span>
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
                <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Legacy Analysis (As-Is State)</h4>
                <p class="u-text-[10px] u-font-bold u-text-muted u-uppercase u-mt-1">Documented manual processes and administrative friction points</p>
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
                    <div v-for="(step, idx) in selectedReview.as_is_steps" :key="idx" class="u-flex u-items-start u-gap-3 u-p-3 u-bg-slate-50 u-rounded-lg u-border">
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
                <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Optimized Transformation (To-Be State)</h4>
                <p class="u-text-[10px] u-font-bold u-text-muted u-uppercase u-mt-1">Re-engineered Business Process Model (BPMN 2.0 Vision)</p>
              </header>

              <div class="u-grid u-grid-cols-1 lg:u-grid-cols-12 u-gap-8">
                <div class="lg:u-col-span-8">
                  <BpmnRenderer :steps="toBeSteps" stage="to_be" />
                </div>
                <div class="lg:u-col-span-4 u-space-y-6">
                  <div class="u-space-y-4">
                    <div v-for="(step, idx) in toBeSteps" :key="idx" class="u-flex u-items-start u-gap-4 u-p-4 u-border u-border-primary/20 u-bg-primary-soft/10 u-rounded-lg">
                      <div class="u-w-8 u-h-8 u-rounded-full u-bg-primary u-flex u-items-center u-justify-center u-text-[10px] u-font-black u-text-white">
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

                  <div class="u-p-6 card u-bg-slate-50 u-border-dashed u-border-2 u-flex u-flex-col u-items-center u-text-center">
                    <i class="bi bi-diagram-3 u-text-4xl u-text-primary u-mb-4"></i>
                    <h5 class="u-text-sm u-font-black u-text-main u-uppercase">BPMN Visualizer Active</h5>
                    <p class="u-text-xs u-text-muted u-mt-2">This sequence is optimized for low-friction digital delivery using shared government enablers.</p>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>

        <template #footer>
          <div class="u-flex u-justify-between u-items-center u-w-full">
            <p class="u-text-[10px] u-font-bold u-text-muted u-uppercase italic">Confidential BPA Mapping Document - ICTA Audit 2024</p>
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

const mdaSearchLocal = ref('');
const showMdaDropdown = ref(false);
const selectedMda = ref('');

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
  return mdas.value.filter(m => m.name.toLowerCase().includes(mdaSearchLocal.value.toLowerCase()));
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

const selectMda = (id) => {
  selectedMda.value = id;
  const match = mdas.value.find(m => m.id === id);
  mdaSearchLocal.value = match ? match.name : '';
  showMdaDropdown.value = false;
};

const filteredReviews = computed(() => {
  let result = reviews.value;
  if (selectedMda.value) {
    result = result.filter(r => r.mda === selectedMda.value);
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
.u-bg-primary-soft { background-color: rgba(37, 99, 235, 0.05); }
.u-bg-success-soft { background-color: rgba(22, 163, 74, 0.05); }
.u-bg-warning-soft { background-color: rgba(217, 119, 6, 0.05); }
.u-bg-info-soft { background-color: rgba(8, 145, 178, 0.05); }
.u-border-primary\/20 { border-color: rgba(37, 99, 235, 0.2); }
.text-premium-gold { color: #fbbf24; text-shadow: 0 0 10px rgba(251, 191, 36, 0.3); }

.report-content-wrapper {
  background: white;
  min-height: 100%;
}

.modal-header-premium {
  background: var(--color-background-soft);
  padding: 1.5rem 2rem !important;
  border-bottom: 2px solid var(--color-border);
}

.print-only { display: none; }

@media print {
  .no-print { display: none !important; }
  .print-only { display: block !important; }
  
  body * { visibility: hidden; }
  #bpa-report-print, #bpa-report-print * { visibility: visible; }
  #bpa-report-print {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    margin: 0;
    padding: 0;
  }
  
  .page-break-before { page-break-before: always; }
  .print-section { 
    margin-bottom: 3rem; 
    padding-bottom: 2rem;
    border-bottom: 1px solid #eee;
  }
  
  .badge { border: 1px solid #000 !important; color: #000 !important; background: none !important; }
}

/* Animations */
.animate-fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
