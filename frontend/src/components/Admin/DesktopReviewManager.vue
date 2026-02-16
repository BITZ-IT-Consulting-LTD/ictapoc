<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
      <div v-for="s in reviewStatsCards" :key="s.label"
        class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm transition-all hover:shadow-md group">
        <div class="flex items-center gap-3">
          <div :class="`p-2 rounded-lg ${s.bgClass} ${s.iconClass}`">
            <component :is="s.icon" class="w-5 h-5" />
          </div>
          <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest leading-none">{{ s.label }}</span>
        </div>
        <div class="mt-2 flex items-baseline gap-1">
          <p class="text-2xl font-black text-gray-900">{{ s.value }}</p>
          <span v-if="s.suffix" class="text-xs text-gray-400 font-bold">{{ s.suffix }}</span>
        </div>
        <div class="mt-1 text-[10px] text-gray-400 group-hover:text-indigo-500 transition-colors">{{ s.sublabel }}</div>
      </div>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">WOG Desktop Reviews</h2>
        <p class="text-sm text-gray-500">Comprehensive process assessment data from the 2024 ICTA Study.</p>
      </div>
      <div class="flex gap-4 w-full md:w-auto">
        <div class="relative flex-1 md:w-64">
          <input type="text" v-model="mdaSearchLocal" placeholder="Filter by Agency..." @focus="showMdaDropdown = true"
            @blur="setTimeout(() => showMdaDropdown = false, 200)"
            class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all cursor-pointer">
          <div v-if="showMdaDropdown"
            class="absolute z-[100] mt-2 w-full bg-white border border-gray-100 rounded-xl shadow-2xl max-h-60 overflow-y-auto p-1 animate-in fade-in zoom-in duration-200">
            <div @click="selectMda('')"
              class="px-3 py-2 hover:bg-indigo-50 cursor-pointer text-xs font-bold text-indigo-600 rounded-lg">All
              Agencies</div>
            <div v-for="mda in uniqueMdas" :key="mda.id" @click="selectMda(mda)"
              class="px-3 py-2 hover:bg-indigo-50 cursor-pointer text-sm text-gray-700 rounded-lg transition-colors">
              {{ mda.name }}
            </div>
          </div>
          <svg class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor"
            viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        <input type="file" ref="fileInput" class="hidden" @change="handleFileUpload" accept=".json">
        <button @click="$refs.fileInput.click()"
          class="px-4 py-2 bg-white border border-gray-200 text-gray-600 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-gray-50 transition-all flex items-center gap-2 shadow-sm">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
          </svg>
          Import JSON
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Sidebar List -->
      <div
        class="lg:col-span-4 bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden flex flex-col h-[700px]">
        <div class="p-4 bg-gray-50 border-b border-gray-100">
          <span class="text-xs font-bold text-gray-400 uppercase tracking-widest">Available Reviews ({{
            filteredReviews.length }})</span>
        </div>
        <div class="flex-1 overflow-y-auto divide-y divide-gray-50">
          <div v-for="review in filteredReviews" :key="review.id" @click="selectedReview = review"
            :class="[selectedReview?.id === review.id ? 'bg-indigo-50 border-l-4 border-indigo-600' : 'hover:bg-gray-50 border-l-4 border-transparent', 'p-4 cursor-pointer transition-all']">
            <h3 class="font-bold text-gray-900 truncate">{{ review.mda_details?.name || 'Unknown MDA' }}</h3>
            <div class="flex items-center gap-2 mt-1">
              <span class="text-[10px] px-2 py-0.5 bg-gray-100 text-gray-600 rounded font-mono">{{ review.process_id ||
                'NO-ID' }}</span>
              <span class="text-xs text-gray-400 italic">Assessment Complete</span>
            </div>
          </div>
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
          </div>
        </div>
      </div>

      <!-- Detail View -->
      <div
        class="lg:col-span-8 bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden flex flex-col h-[700px]">
        <div v-if="selectedReview" class="flex flex-col h-full">
          <!-- Header -->
          <div class="p-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
            <div class="flex justify-between items-start">
              <div>
                <h2 class="text-2xl font-black text-gray-900 leading-tight">{{ selectedReview.mda_details?.name }}</h2>
                <div class="flex items-center gap-3 mt-2">
                  <span
                    class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wider">Process
                    ID: {{ selectedReview.process_id }}</span>
                  <span class="text-xs text-gray-400">Created: {{ new
                    Date(selectedReview.created_at).toLocaleDateString() }}</span>
                </div>
              </div>
              <button @click="exportReview" class="p-2 text-gray-400 hover:text-indigo-600 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Content Tabs -->
          <div class="flex border-b border-gray-100 px-6 bg-white overflow-x-auto">
            <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
              :class="[activeTab === tab.id ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700', 'py-4 px-4 border-b-2 font-bold text-sm transition-all whitespace-nowrap']">
              {{ tab.name }}
            </button>
          </div>

          <!-- Tab Content -->
          <div class="flex-1 overflow-y-auto p-6 space-y-8 prose prose-indigo max-w-none">
            <!-- Executive Summary -->
            <div v-if="activeTab === 'summary'">
              <h4 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Executive Summary
              </h4>
              <p class="text-gray-600 whitespace-pre-wrap leading-relaxed">{{ selectedReview.executive_summary || 'No summary available.' }}</p>

              <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4 not-prose">
                <div v-for="(val, key) in selectedReview.process_overview" :key="key"
                  class="bg-gray-50 p-4 rounded-xl border border-gray-100">
                  <dt class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ key.replace(/_/g, ' ')
                    }}</dt>
                  <dd class="text-sm font-bold text-gray-700 mt-1">{{ val }}</dd>
                </div>
              </div>
            </div>

            <!-- Stakeholders -->
            <div v-if="activeTab === 'stakeholders'">
              <h4 class="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z">
                  </path>
                </svg>
                Key Stakeholders
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-start not-prose">
                <div v-for="(sh, idx) in selectedReview.stakeholders" :key="idx"
                  class="bg-white border-l-4 border-indigo-500 p-4 rounded-r-xl shadow-sm border border-gray-200">
                  <div class="font-black text-indigo-700 text-sm mb-1 uppercase tracking-tight">{{ sh.name }}</div>
                  <div class="text-xs text-gray-500 font-medium">{{ sh.role }}</div>
                  <p class="text-[11px] text-gray-400 mt-2 leading-relaxed">{{ sh.responsibilities }}</p>
                </div>
              </div>
            </div>

            <!-- As-Is Process -->
            <div v-if="activeTab === 'as_is'">
              <div class="bg-amber-50 rounded-2xl p-6 mb-8 border border-amber-100 shadow-sm not-prose">
                <h5 class="text-amber-800 font-black uppercase tracking-widest text-xs mb-3">Pain Points & Bottlenecks
                </h5>
                <ul class="space-y-2">
                  <li v-for="(pp, idx) in selectedReview.pain_points_bottlenecks_risks" :key="idx"
                    class="flex gap-2 text-sm text-amber-900 font-medium">
                    <svg class="w-5 h-5 text-amber-500 flex-shrink-0" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z">
                      </path>
                    </svg>
                    {{ pp.description || pp }}
                  </li>
                </ul>
              </div>

              <h4 class="text-lg font-bold text-gray-900 mb-4 italic">Narrative Workflow</h4>
              <p class="text-gray-600 whitespace-pre-wrap leading-relaxed text-sm mb-8">{{
                selectedReview.as_is_narrative }}</p>

              <h4 class="text-lg font-bold text-gray-900 mb-6">Sequence of Steps (Current)</h4>
              <div class="space-y-4 not-prose">
                <div v-for="(step, idx) in selectedReview.as_is_steps" :key="idx" class="flex items-start gap-4">
                  <div
                    class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center font-black text-xs text-gray-400 flex-shrink-0 border border-gray-200">
                    {{ idx + 1 }}
                  </div>
                  <div class="flex-1 pt-1 pb-4 border-b border-gray-100 last:border-0">
                    <div class="font-bold text-gray-800 text-sm mb-1">{{ step.description }}</div>
                    <div class="text-[10px] text-indigo-600 font-black uppercase tracking-widest">{{ step.actor }}</div>
                  </div>
                </div>
              </div>
              <div class="mt-8 border-t pt-8 not-prose">
                <h4 class="text-lg font-bold text-gray-900 mb-4">Current Process Model (BPMN)</h4>
                <BpmnRenderer :steps="selectedReview.as_is_steps" stage="as_is" />
              </div>
            </div>

            <!-- To-Be Process -->
            <div v-if="activeTab === 'to_be'">
              <div class="bg-indigo-900 text-white rounded-2xl p-8 mb-8 shadow-xl relative overflow-hidden not-prose">
                <div class="absolute -right-20 -top-20 w-64 h-64 bg-indigo-800 rounded-full opacity-50"></div>
                <div class="relative z-10">
                  <h5 class="text-indigo-300 font-black uppercase tracking-widest text-[10px] mb-2">Optimization
                    Strategy</h5>
                  <h3 class="text-2xl font-black leading-tight mb-4">Digitization Opportunities</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div v-for="(opt, idx) in selectedReview.digitization_opportunities" :key="idx"
                      class="flex gap-3 items-start bg-indigo-800/50 p-4 rounded-xl backdrop-blur-sm border border-indigo-700/50">
                      <div class="w-6 h-6 rounded bg-indigo-500 flex items-center justify-center flex-shrink-0">
                        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                      </div>
                      <div class="text-sm font-bold">{{ opt.description || opt }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex items-center justify-between mb-6">
                <h4 class="text-lg font-bold text-gray-900">Optimized BPMN Steps (To-Be)</h4>
                <div v-if="linkedService?.workflow_steps?.length > 0"
                  class="flex items-center gap-1.5 px-2 py-1 bg-green-50 text-green-700 border border-green-200 rounded text-[10px] font-bold uppercase tracking-wider">
                  <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-ping"></span>
                  Live Sync
                </div>
              </div>
              <div class="space-y-4 not-prose">
                <div v-for="(step, idx) in toBeSteps" :key="idx" class="relative flex items-start gap-6 group">
                  <div
                    class="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center font-black text-indigo-600 flex-shrink-0 z-10 border border-indigo-100 shadow-sm transition-transform group-hover:scale-110">
                    {{ idx + 1 }}
                  </div>
                  <div v-if="idx < toBeSteps.length - 1" class="absolute left-5 top-10 w-0.5 h-full bg-indigo-50 -z-0">
                  </div>

                  <div
                    class="flex-1 bg-white border border-gray-100 rounded-2xl p-5 mb-4 shadow-sm group-hover:border-indigo-200 transition-all">
                    <div class="flex justify-between items-start mb-2">
                      <span class="text-[10px] font-black text-indigo-400 uppercase tracking-widest">{{ step.actor
                        }}</span>
                      <span v-if="step.system"
                        class="text-[8px] px-2 py-0.5 bg-green-50 text-green-600 rounded-full font-bold uppercase tracking-tighter border border-green-100">Automated</span>
                    </div>
                    <div class="font-bold text-gray-900 text-sm leading-relaxed">{{ step.description }}</div>
                    <div v-if="step.input" class="mt-3 flex flex-wrap gap-2">
                      <span v-for="inp in step.input" :key="inp"
                        class="text-[9px] px-2 py-0.5 bg-gray-50 text-gray-500 rounded border border-gray-100">{{ inp
                        }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-8 border-t pt-8 not-prose">
                <h4 class="text-lg font-bold text-gray-900 mb-4">Target Process Model (BPMN)</h4>
                <BpmnRenderer :steps="toBeSteps" stage="to_be" />
              </div>
            </div>
          </div>
        </div>

        <div v-else class="flex flex-col items-center justify-center h-full p-12 text-center text-gray-400">
          <div class="w-32 h-32 bg-gray-50 rounded-full flex items-center justify-center mb-6">
            <svg class="w-16 h-16 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-900">Select an assessment review</h3>
          <p class="max-w-xs mt-2">Deep-dive into the Whole-of-Government service catalogue analysis by selecting an MDA
            from the list.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import api from '../../services/api';
  import { useServiceConfigStore } from '../../store/serviceConfig';
  import BpmnRenderer from './BpmnRenderer.vue';

  const reviews = ref([]);
  const loading = ref(false);
  const selectedReview = ref(null);
  const searchQuery = ref('');
  const mdaSearchLocal = ref('');
  const selectedMda = ref('');
  const showMdaDropdown = ref(false);
  const activeTab = ref('summary');

  const fileInput = ref(null);

  const serviceStore = useServiceConfigStore();

  const tabs = [
    { id: 'summary', name: 'Executive Summary' },
    { id: 'stakeholders', name: 'Stakeholders' },
    { id: 'as_is', name: 'As-Is Workflow' },
    { id: 'to_be', name: 'To-Be Vision' }
  ];

  const fetchReviews = async () => {
    loading.value = true;
    try {
      const response = await api.get('/desktop-reviews/');
      reviews.value = response.data;
      // Also ensure services are loaded
      if (serviceStore.services.length === 0) {
        await serviceStore.fetchServices();
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
    } finally {
      loading.value = false;
    }
  };

  const linkedService = computed(() => {
    if (!selectedReview.value) return null;
    // Match by MDA ID and Process ID/Code or Process Name
    return serviceStore.services.find(s =>
      s.mda === selectedReview.value.mda &&
      (s.service_code === selectedReview.value.process_id || s.service_name === (selectedReview.value.process_name || selectedReview.value.mda_details?.name))
    );
  });

  const toBeSteps = computed(() => {
    // If we have a linked service with LIVE workflow steps for TO_BE lifecycle, use them!
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
    // Fallback to static JSON steps from DesktopReview
    return selectedReview.value?.to_be_process?.steps || [];
  });

  const filteredReviews = computed(() => {
    let result = reviews.value;
    if (selectedMda.value) {
      result = result.filter(r => r.mda === selectedMda.value);
    }
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.mda_details?.name.toLowerCase().includes(q) ||
        r.process_id.toLowerCase().includes(q) ||
        (r.executive_summary && r.executive_summary.toLowerCase().includes(q))
      );
    }
    return result;
  });

  const uniqueMdas = computed(() => {
    const mdas = [];
    const seen = new Set();
    reviews.value.forEach(r => {
      if (r.mda_details && !seen.has(r.mda)) {
        seen.add(r.mda);
        mdas.push({ id: r.mda, name: r.mda_details.name });
      }
    });
    return mdas.sort((a, b) => a.name.localeCompare(b.name));
  });

  const selectMda = (mda) => {
    if (mda === '') {
      selectedMda.value = '';
      mdaSearchLocal.value = '';
    } else {
      selectedMda.value = mda.id;
      mdaSearchLocal.value = mda.name;
    }
    showMdaDropdown.value = false;
  };

  const reviewStatsCards = computed(() => {
    const total = reviews.value.length;
    const avgMaturity = total > 0 ? (reviews.value.reduce((acc, r) => acc + (r.process_maturity || 0), 0) / total).toFixed(1) : 0;
    const totalSteps = reviews.value.reduce((acc, r) => acc + (r.as_is_steps?.length || 0), 0);
    const totalStakeholders = reviews.value.reduce((acc, r) => acc + (r.stakeholders?.length || 0), 0);

    return [
      { label: 'Assessments', value: total, sublabel: 'Completed Reviews', icon: { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' }, bgClass: 'bg-indigo-50', iconClass: 'text-indigo-600' },
      { label: 'Process Maturity', value: avgMaturity, suffix: '/ 5', sublabel: 'Average Score', icon: { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>' }, bgClass: 'bg-emerald-50', iconClass: 'text-emerald-600' },
      { label: 'Activity Map', value: totalSteps, sublabel: 'Total Process Steps', icon: { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>' }, bgClass: 'bg-orange-50', iconClass: 'text-orange-600' },
      { label: 'Governance', value: totalStakeholders, sublabel: 'Stakeholders Identified', icon: { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>' }, bgClass: 'bg-purple-50', iconClass: 'text-purple-600' }
    ];
  });

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const data = JSON.parse(e.target.result);
        // Simulate import or call API if exists
        console.log('Importing Review:', data);
        alert('Review data imported locally for visualization. In a production environment, this would be persisted to the National Registry.');
        selectedReview.value = data;
      } catch (err) {
        console.error('Invalid JSON file', err);
        alert('Failed to parse JSON file.');
      }
    };
    reader.readAsText(file);
  };

  const exportReview = () => {
    if (!selectedReview.value) return;
    const data = JSON.stringify(selectedReview.value, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `DesktopReview_${selectedReview.value.mda_details?.name.replace(/ /g, '_')}.json`;
    a.click();
  };

  onMounted(fetchReviews);
</script>

<style scoped>
  .prose h4 {
    margin-top: 2rem;
    margin-bottom: 1rem;
  }

  .prose p {
    margin-bottom: 1.5rem;
  }
</style>
