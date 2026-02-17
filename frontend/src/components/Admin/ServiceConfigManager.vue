<template>
  <section class="page service-config-manager">
    <WogDashboardStats v-if="auditStats" :stats="auditStats" class="mb-8" />

    <header class="page__header u-mb-8">
      <div class="page__title-group">
        <h1 class="page__title">National Service Registry</h1>
        <p class="page__subtitle">Centralized configuration for government services and data schemas</p>
      </div>
      <div class="page__actions">
        <button @click="openCreateModal"
          class="button button--primary button--pill">
          <i class="bi bi-plus-lg"></i> Register New Service
        </button>
      </div>
    </header>

    <div class="toolbar u-mb-8">
      <div class="toolbar__filters">
        <!-- Search -->
        <div class="toolbar__filter-group">
          <i class="bi bi-search toolbar__filter-icon"></i>
          <input type="text" v-model="searchQuery" placeholder="Filter by name, code or ID..."
            class="toolbar__filter-input">
        </div>

        <!-- Agency Filter -->
        <div class="toolbar__filter-group">
          <i class="bi bi-building toolbar__filter-icon"></i>
          <input type="text" v-model="mdaFilterSearchLocal" placeholder="Filter by Responsible Agency..."
            @focus="showMdaFilterDropdown = true" @blur="setTimeout(() => showMdaFilterDropdown = false, 200)"
            class="toolbar__filter-input toolbar__filter-input--with-arrow">
          <i class="bi bi-chevron-down toolbar__filter-arrow"
            :class="{ 'toolbar__filter-arrow--open': showMdaFilterDropdown }"></i>

          <div v-if="showMdaFilterDropdown"
            class="u-absolute u-top-full u-left-0 u-w-full bg-white u-border u-shadow-xl u-rounded-lg u-mt-2 u-z-dropdown u-overflow-auto u-p-2" style="max-height: 240px">
            <div @click="selectMdaFilter('')"
              class="u-p-3 hover:bg-bg-page u-rounded u-font-bold u-text-primary u-mb-1" style="cursor: pointer">
              All Institutions
            </div>
            <div v-for="mda in filteredMdasForFilter" :key="mda.id" @click="selectMdaFilter(mda)"
              class="u-p-3 hover:bg-bg-page u-rounded u-flex u-items-center u-gap-3 u-font-medium transition-colors" style="cursor: pointer; font-size: 14px">
              <i class="bi bi-building u-text-muted"></i> {{ mda.name }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Service Registry Table -->
    <div class="card u-overflow-hidden">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr class="table__header-row">
              <th class="table__header-cell table__header-cell--with-left-padding">Registry Code</th>
              <th class="table__header-cell">Official Service Name</th>
              <th class="table__header-cell">Institutional Owner (MDA)</th>
              <th class="table__header-cell table__header-cell--align-right table__header-cell--with-right-padding">Management</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in filteredServices" :key="service.id"
              class="table__row">
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
              <td class="table__cell table__cell--align-right table__cell--with-right-padding">
                <div class="table__actions">
                  <button @click="openEditModal(service)"
                    class="button button--secondary button--small">
                    <i class="bi bi-sliders"></i> Configure
                  </button>
                  <button @click="deleteService(service.id)"
                    class="button button--ghost button--small">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredServices.length === 0">
              <td colspan="4" class="table__cell u-text-center u-p-12 u-text-muted" style="font-style: italic">
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
        <!-- Vertical Tab Layout -->
        <div class="flex gap-8">
          <!-- Left Sidebar Navigation -->
          <aside class="w-72 flex-shrink-0">
            <div class="sticky top-6">
              <!-- Sidebar Header -->
              <div class="mb-6 px-4">
                <div class="flex items-center gap-2 mb-2">
                  <div class="w-1 h-6 bg-gradient-to-b from-primary to-secondary rounded-full"></div>
                  <h4 class="text-xs font-black uppercase tracking-widest text-muted">
                    Configuration Steps
                  </h4>
                </div>
                <p class="text-xs text-muted/70 ml-3">Complete each section to onboard the service</p>
              </div>

              <!-- Navigation Items -->
              <nav class="space-y-2">
                <!-- Service Identity -->
                <button type="button" @click="currentConfigTab = 'identity'"
                  class="group w-full relative overflow-hidden rounded-xl text-left transition-all duration-300"
                  :class="currentConfigTab === 'identity'
                    ? 'bg-gradient-to-br from-primary to-primary-dark text-white shadow-xl shadow-primary/40 scale-105'
                    : 'bg-white border-2 border-slate-100 text-muted hover:border-primary/30 hover:shadow-lg hover:scale-102'">

                  <!-- Decorative gradient overlay for active state -->
                  <div v-if="currentConfigTab === 'identity'"
                    class="absolute inset-0 bg-gradient-to-tr from-white/10 to-transparent"></div>

                  <div class="relative flex items-center gap-4 p-4">
                    <!-- Icon Container -->
                    <div class="flex items-center justify-center w-12 h-12 rounded-xl transition-all"
                      :class="currentConfigTab === 'identity'
                        ? 'bg-white/20 shadow-lg'
                        : 'bg-gradient-to-br from-primary/10 to-primary/5 group-hover:from-primary/20 group-hover:to-primary/10'">
                      <i class="bi bi-card-heading text-xl"
                        :class="currentConfigTab === 'identity' ? 'text-white' : 'text-primary'"></i>
                    </div>

                    <!-- Text Content -->
                    <div class="flex-1 min-w-0">
                      <div class="font-bold text-sm mb-0.5"
                        :class="currentConfigTab === 'identity' ? 'text-white' : 'text-main'">
                        Service Identity
                      </div>
                      <div class="text-xs" :class="currentConfigTab === 'identity' ? 'text-white/80' : 'text-muted'">
                        Basic info & MDA mapping
                      </div>
                    </div>

                    <!-- Status Indicator -->
                    <div class="flex items-center gap-2">
                      <div v-if="currentConfigTab === 'identity'" class="w-2 h-2 bg-white rounded-full animate-pulse">
                      </div>
                      <i v-if="currentConfigTab === 'identity'" class="bi bi-chevron-right text-white text-sm"></i>
                    </div>
                  </div>

                  <!-- Step Number Badge -->
                  <div class="absolute top-2 right-2">
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold" :class="currentConfigTab === 'identity'
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-100 text-muted'">
                      1
                    </div>
                  </div>
                </button>

                <!-- Form Schema -->
                <button type="button" @click="currentConfigTab = 'schema'"
                  class="group w-full relative overflow-hidden rounded-xl text-left transition-all duration-300"
                  :class="currentConfigTab === 'schema'
                    ? 'bg-gradient-to-br from-success to-success-dark text-white shadow-xl shadow-success/40 scale-105'
                    : 'bg-white border-2 border-slate-100 text-muted hover:border-success/30 hover:shadow-lg hover:scale-102'">

                  <!-- Decorative gradient overlay for active state -->
                  <div v-if="currentConfigTab === 'schema'"
                    class="absolute inset-0 bg-gradient-to-tr from-white/10 to-transparent"></div>

                  <div class="relative flex items-center gap-4 p-4">
                    <!-- Icon Container -->
                    <div class="flex items-center justify-center w-12 h-12 rounded-xl transition-all"
                      :class="currentConfigTab === 'schema'
                        ? 'bg-white/20 shadow-lg'
                        : 'bg-gradient-to-br from-success/10 to-success/5 group-hover:from-success/20 group-hover:to-success/10'">
                      <i class="bi bi-ui-checks-grid text-xl"
                        :class="currentConfigTab === 'schema' ? 'text-white' : 'text-success'"></i>
                    </div>

                    <!-- Text Content -->
                    <div class="flex-1 min-w-0">
                      <div class="font-bold text-sm mb-0.5"
                        :class="currentConfigTab === 'schema' ? 'text-white' : 'text-main'">
                        Form Schema
                      </div>
                      <div class="text-xs" :class="currentConfigTab === 'schema' ? 'text-white/80' : 'text-muted'">
                        Define data collection fields
                      </div>
                    </div>

                    <!-- Status Indicator -->
                    <div class="flex items-center gap-2">
                      <div v-if="currentConfigTab === 'schema'" class="w-2 h-2 bg-white rounded-full animate-pulse">
                      </div>
                      <i v-if="currentConfigTab === 'schema'" class="bi bi-chevron-right text-white text-sm"></i>
                    </div>
                  </div>

                  <!-- Step Number Badge -->
                  <div class="absolute top-2 right-2">
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold" :class="currentConfigTab === 'schema'
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-100 text-muted'">
                      2
                    </div>
                  </div>
                </button>

                <!-- Workflow Pipeline -->
                <button type="button" @click="currentConfigTab = 'workflow'" :disabled="!editForm.id"
                  class="group w-full relative overflow-hidden rounded-xl text-left transition-all duration-300" :class="[
                    currentConfigTab === 'workflow'
                      ? 'bg-gradient-to-br from-secondary to-secondary-dark text-white shadow-xl shadow-secondary/40 scale-105'
                      : 'bg-white border-2 border-slate-100 text-muted hover:border-secondary/30 hover:shadow-lg hover:scale-102',
                    !editForm.id ? 'opacity-60 cursor-not-allowed hover:scale-100 hover:shadow-none' : ''
                  ]">

                  <!-- Decorative gradient overlay for active state -->
                  <div v-if="currentConfigTab === 'workflow'"
                    class="absolute inset-0 bg-gradient-to-tr from-white/10 to-transparent"></div>

                  <div class="relative flex items-center gap-4 p-4">
                    <!-- Icon Container -->
                    <div class="flex items-center justify-center w-12 h-12 rounded-xl transition-all"
                      :class="currentConfigTab === 'workflow'
                        ? 'bg-white/20 shadow-lg'
                        : 'bg-gradient-to-br from-secondary/10 to-secondary/5 group-hover:from-secondary/20 group-hover:to-secondary/10'">
                      <i class="bi bi-diagram-3 text-xl"
                        :class="currentConfigTab === 'workflow' ? 'text-white' : 'text-secondary'"></i>
                    </div>

                    <!-- Text Content -->
                    <div class="flex-1 min-w-0">
                      <div class="font-bold text-sm mb-0.5"
                        :class="currentConfigTab === 'workflow' ? 'text-white' : 'text-main'">
                        Workflow Pipeline
                      </div>
                      <div class="text-xs" :class="currentConfigTab === 'workflow' ? 'text-white/80' : 'text-muted'">
                        <span v-if="!editForm.id" class="flex items-center gap-1">
                          <i class="bi bi-lock-fill text-warning"></i>
                          <span class="text-warning font-medium">Save service first</span>
                        </span>
                        <span v-else>Configure process stages</span>
                      </div>
                    </div>

                    <!-- Status Indicator -->
                    <div class="flex items-center gap-2">
                      <div v-if="currentConfigTab === 'workflow' && editForm.id"
                        class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                      <i v-if="currentConfigTab === 'workflow' && editForm.id"
                        class="bi bi-chevron-right text-white text-sm"></i>
                    </div>
                  </div>

                  <!-- Step Number Badge -->
                  <div class="absolute top-2 right-2">
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold" :class="currentConfigTab === 'workflow'
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-100 text-muted'">
                      3
                    </div>
                  </div>
                </button>
              </nav>

              <!-- Progress Indicator -->
              <div class="mt-6 px-4">
                <div class="bg-slate-100 rounded-full h-2 overflow-hidden">
                  <div
                    class="h-full bg-gradient-to-r from-primary via-success to-secondary transition-all duration-500 rounded-full"
                    :style="{ width: currentConfigTab === 'identity' ? '33%' : currentConfigTab === 'schema' ? '66%' : '100%' }">
                  </div>
                </div>
                <p class="text-xs text-muted text-center mt-2">
                  Step {{ currentConfigTab === 'identity' ? '1' : currentConfigTab === 'schema' ? '2' : '3' }} of 3
                </p>
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

            <!-- Workflow Tab -->
            <div v-show="currentConfigTab === 'workflow'" class="tab-content animate-fade-in">
              <div v-if="editForm.id" class="card border-0 shadow-sm">
                <div class="card__header bg-gradient-to-r from-secondary/5 to-secondary/10">
                  <h3 class="card__title flex items-center gap-2">
                    <i class="bi bi-diagram-3 text-secondary"></i>
                    Workflow Orchestration
                  </h3>
                  <p class="card__subtitle">Configure processing stages and approvals</p>
                </div>
                <div class="card__body p-0">
                  <WorkflowStepManager :service-config-id="editForm.id" />
                </div>
              </div>
              <div v-else class="card border-2 border-dashed border-warning/30 bg-warning/5">
                <div class="card__body text-center py-12">
                  <i class="bi bi-exclamation-triangle text-6xl text-warning mb-4 opacity-50"></i>
                  <h4 class="font-black text-xl text-main mb-2">Save Service First</h4>
                  <p class="text-muted mb-6">You must save the service identity before configuring the workflow
                    pipeline.
                  </p>
                  <button type="button" @click="currentConfigTab = 'identity'" class="button button--warning">
                    <i class="bi bi-arrow-left me-2"></i>Back to Identity
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex justify-between items-center pt-4 border-t border-border-color mt-4">
          <button type="button" @click="closeModal" class="button button--secondary">
            <i class="bi bi-x-lg me-2"></i>Discard Changes
          </button>
          <button type="submit"
            class="button button--primary shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <i class="bi bi-cloud-check me-2"></i> Commit Registry Update
          </button>
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
  const mdas = computed(() => mdaStore.mdas);
  const searchQuery = ref('');
  const mdaFilter = ref('');

  const mdaFilterSearchLocal = ref('');
  const showMdaFilterDropdown = ref(false);
  const currentConfigTab = ref('identity'); // Tab state for modal

  const filteredMdasForFilter = computed(() => {
    if (!mdaFilterSearchLocal.value) return mdas.value;
    const q = mdaFilterSearchLocal.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q));
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

  const filteredServices = computed(() => {
    let result = services.value;

    if (mdaFilter.value) {
      result = result.filter(s => s.mda === Number(mdaFilter.value));
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
    config: { rules: { schema: { properties: {}, required: [] } } },
  });

  onMounted(() => {
    serviceConfigStore.fetchServices();
    mdaStore.fetchMdas();
    serviceConfigStore.fetchCatalogueSummary();
  });

  const getMdaName = (mdaId) => {
    const mda = mdas.value.find(m => m.id === mdaId);
    if (!mda) return 'N/A';
    return mda.code ? `${mda.name} (${mda.code})` : mda.name;
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
      config: { rules: { schema: { properties: {}, required: [] } } },
    };
    showModal.value = true;
  };

  const openEditModal = (service) => {
    // Deep copy to avoid reactive mutations outside of the store
    editForm.value = JSON.parse(JSON.stringify(service));
    if (!editForm.value.config) {
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
</style>
