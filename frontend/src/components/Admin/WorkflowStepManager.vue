<template>
  <div class="workflow-step-manager">
    <!-- Header Area: Consistent with App BEM Patterns -->
    <div class="page__header u-mb-6">
      <div class="page__title-group">
        <h4 class="page__title u-text-xl">Workflow Pipeline Designer</h4>
        <p class="page__subtitle u-text-xs">Configure the sequence of manual and automated processing stages</p>
      </div>
      <div class="page__actions">
        <button type="button" @click.stop="openCreateModal" class="button button--primary button--small shadow-sm">
          <i class="bi bi-plus-lg me-1"></i> Append Stage
        </button>
      </div>
    </div>

    <!-- Search/Filter Bar: Consistent with .toolbar pattern -->
    <div class="toolbar u-mb-6">
      <div class="toolbar__filter-group">
        <i class="bi bi-search toolbar__filter-icon"></i>
        <input type="text" v-model="searchQuery" placeholder="Filter pipeline stages..."
          class="toolbar__filter-input w-full" />
      </div>
    </div>

    <!-- Step List: Semantic Flow Visualization -->
    <div class="list u-relative u-pl-12">
      <!-- Logic Backbone Line (Custom but themed) -->
      <div v-if="filteredSteps.length > 0"
        class="u-absolute u-left-4 u-top-0 u-bottom-0 u-w-1 u-bg-gradient-to-b u-from-primary/20 u-via-primary/5 u-to-transparent u-rounded-full u-z-0">
      </div>

      <div class="u-flex u-flex-col u-gap-6">
        <div v-for="(step, index) in filteredSteps" :key="step.id" class="u-relative u-z-10 group">
          <!-- Connector Path -->
          <div v-if="index < filteredSteps.length - 1"
            class="u-absolute u-left-[-2.1rem] u-top-[3.5rem] u-w-[2px] u-h-full u-bg-gradient-to-b u-from-primary u-to-transparent u-opacity-20">
          </div>

          <!-- Step Marker Node -->
          <div
            class="u-absolute -u-left-12 u-top-6 u-w-9 u-h-9 u-rounded-full u-bg-white u-border-4 u-border-primary/10 u-flex u-items-center u-justify-center u-shadow-md group-hover:u-border-primary transition-all">
            <span class="u-text-[10px] u-font-black u-text-primary">{{ step.sequence }}</span>
          </div>

          <!-- Component Card -->
          <div class="card hover:u-border-primary/40 hover:u-shadow-xl transition-all u-relative u-overflow-hidden">
            <!-- Glass Overlay -->
            <div
              class="u-absolute u-inset-0 u-bg-gradient-to-r u-from-primary/5 u-to-transparent u-opacity-0 group-hover:u-opacity-100 transition-opacity">
            </div>

            <div class="card__body u-relative u-z-10 u-p-6">
              <!-- Node Info & Controls -->
              <div class="u-flex u-items-center u-justify-between u-mb-4">
                <div class="u-flex u-items-center u-gap-4">
                  <div class="u-w-10 u-h-10 u-rounded-xl u-flex u-items-center u-justify-center"
                    :class="step.step_type === 'manual' ? 'u-bg-primary-soft u-text-primary' : 'u-bg-warning-soft u-text-warning'">
                    <i :class="step.step_type === 'manual' ? 'bi bi-person-gear' : 'bi bi-robot'"></i>
                  </div>
                  <div>
                    <h5 class="u-font-black u-text-main u-text-sm u-uppercase u-tracking-widest">{{ step.step_name }}
                    </h5>
                    <div class="u-flex u-items-center u-gap-2">
                      <span class="u-text-[9px] u-font-black u-uppercase u-tracking-[0.15em]"
                        :class="step.step_type === 'manual' ? 'u-text-primary' : 'u-text-warning'">
                        {{ step.step_type === 'manual' ? 'Manual' : 'Automated' }}
                      </span>
                      <span v-if="step.api_config?.outcomes?.length"
                        class="u-text-[9px] u-bg-success/10 u-text-success-dark u-px-2 u-py-0.5 u-rounded-full u-font-bold">
                        {{ step.api_config.outcomes.length }} Outcomes
                      </span>
                    </div>
                  </div>
                </div>

                <div class="u-flex u-gap-2">
                  <button type="button" @click.stop="editStep(step)"
                    class="button button--secondary button--small u-p-2" title="Edit Stage">
                    <i class="bi bi-pencil-fill"></i>
                  </button>
                  <button type="button" @click.stop="deleteStep(step.id)"
                    class="button button--danger button--small u-p-2" title="Remove Stage">
                    <i class="bi bi-trash-fill"></i>
                  </button>
                </div>
              </div>

              <!-- Functional Details Context Box -->
              <div class="u-p-4 u-bg-bg-page u-rounded-xl u-border u-border-border-color/50">
                <div v-if="step.step_type === 'manual'" class="u-flex u-items-center u-gap-6">
                  <div class="u-flex u-items-center u-gap-2">
                    <i class="bi bi-shield-lock u-text-muted u-text-xs"></i>
                    <span class="u-text-[10px] u-font-black u-text-muted/60 u-uppercase">Role:</span>
                    <span
                      class="u-text-[10px] u-font-black u-text-main u-uppercase u-bg-white u-px-2 u-py-1 u-rounded-md u-border">{{
                        step.role }}</span>
                  </div>
                  <div class="u-w-px u-h-4 u-bg-border-color"></div>
                  <div class="u-flex u-items-center u-gap-2">
                    <i class="bi bi-cursor-fill u-text-muted u-text-xs"></i>
                    <span class="u-text-[10px] u-font-black u-text-muted/60 u-uppercase">Action:</span>
                    <span class="u-text-[10px] u-font-black u-text-primary u-uppercase">{{ getActionLabel(step)
                    }}</span>
                  </div>
                </div>

                <div v-if="step.step_type === 'api_call'" class="u-flex u-items-center u-gap-4">
                  <div class="u-w-8 u-h-8 u-rounded-lg u-bg-warning-soft u-flex u-items-center u-justify-center">
                    <i class="bi bi-cpu u-text-warning u-text-sm"></i>
                  </div>
                  <div class="u-flex u-flex-col flex-grow">
                    <span class="u-text-[9px] u-font-black u-text-muted u-uppercase u-tracking-widest">Registry
                      Integration</span>
                    <span class="u-text-[11px] u-font-mono u-font-bold u-text-warning-dark">{{ getApiUrlLabel(step)
                      }}</span>
                  </div>
                </div>

                <!-- Outcomes Preview -->
                <div v-if="step.api_config?.outcomes?.length" class="u-mt-3 u-pt-3 u-border-t u-border-border-color/30">
                  <div class="u-flex u-flex-wrap u-gap-2">
                    <div v-for="outcome in step.api_config.outcomes" :key="outcome.label"
                      class="u-flex u-items-center u-gap-2 u-px-3 u-py-1 u-bg-white u-border u-rounded-lg">
                      <span class="u-text-[9px] u-font-black u-text-main u-uppercase">{{ outcome.label }}</span>
                      <i class="bi bi-arrow-right u-text-[8px] u-text-muted"></i>
                      <span class="u-text-[9px] u-font-mono u-font-bold"
                        :class="outcome.target_sequence ? 'u-text-primary' : 'u-text-danger'">
                        {{ outcome.target_sequence ? 'STEP ' + outcome.target_sequence : 'END' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State: Guided Action -->
      <div v-if="filteredSteps.length === 0"
        class="u-p-16 u-text-center u-bg-bg-page u-rounded-[2.5rem] u-border-2 u-border-dashed u-border-border-color/60">
        <div
          class="u-w-16 u-h-16 u-bg-white u-rounded-2xl u-flex u-items-center u-justify-center u-mx-auto u-mb-4 u-shadow-inner u-border">
          <i class="bi bi-bezier2 u-text-3xl u-text-primary/30"></i>
        </div>
        <h5 class="u-font-black u-text-main u-uppercase u-tracking-[0.2em] u-text-xs u-mb-2">Pipeline Empty</h5>
        <p class="u-text-xs u-text-muted/60 u-max-w-xs u-mx-auto u-mb-6">Start by defining the first manual review or
          automated processing node.</p>
        <button type="button" @click.stop="openCreateModal" class="button button--primary button--small">
          Initialize Pipeline
        </button>
      </div>
    </div>

    <!-- Live Visual Blueprint: Single Source of Truth for BPMN -->
    <div v-if="filteredSteps.length > 0" class="u-mt-12 u-border-t u-pt-12">
      <div class="u-flex u-items-center u-justify-between u-mb-6">
        <div>
          <h5 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Visual Blueprint</h5>
          <p class="u-text-[10px] u-text-muted u-mt-1">Real-time BPMN 2.0 orchestration model synchronized with catalogue matrix</p>
        </div>
        <span class="badge badge--primary u-font-mono u-text-[9px]">GOK-ADMIN-01 Compliance</span>
      </div>
      
      <BpmnRenderer :steps="filteredSteps" stage="to_be" />
    </div>

    <BaseModal v-model:show="showModal" :title="stepForm.id ? 'Modify Workflow Node' : 'Initialize Workflow Node'"
      subtitle="Define technical data schemas and internal agency workflows" icon="bi-gear-wide-connected" size="md">
      <form @submit.prevent="handleStepSubmit" class="u-flex u-flex-col u-gap-8 u-p-2">
        <!-- Structural synthesis preview -->
        <div class="u-bg-slate-900 u-rounded-2xl u-p-6 u-relative u-overflow-hidden">
          <div class="u-absolute u-top-0 u-right-0 u-p-4 u-opacity-10">
            <i class="bi bi-cpu u-text-6xl u-text-white"></i>
          </div>
          <div class="u-relative u-z-10">
            <div class="u-flex u-items-center u-gap-3 u-mb-3">
              <span class="u-w-2 u-h-2 u-bg-primary u-rounded-full animate-pulse"></span>
              <span class="u-text-[10px] u-font-black u-text-white/40 u-uppercase u-tracking-[0.2em]">Structural
                Synthesis</span>
            </div>
            <div class="u-flex u-items-end u-gap-4">
              <div class="u-text-3xl u-font-black u-text-white">{{ stepForm.sequence || '0' }}</div>
              <div class="u-flex-1">
                <div class="u-text-xs u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-1">
                  {{ stepForm.step_type === 'manual' ? 'Manual Institutional Action' : 'Automated API Handshake' }}
                </div>
                <div class="u-text-sm u-font-bold u-text-white/90">{{ stepForm.step_name || 'UNDEFINED_BACKBONE_NODE' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Configuration Grid -->
        <div class="grid grid--2 u-gap-6">
          <div class="form__group">
            <label class="form__label u-flex u-items-center u-gap-2">
              <i class="bi bi-sort-numeric-down text-primary"></i>
              Execution Sequence
            </label>
            <input type="number" v-model.number="stepForm.sequence" class="form__input font-mono font-bold" required>
            <p class="u-text-[10px] u-text-muted u-mt-1">Order in which this step occurs</p>
          </div>

          <div class="form__group">
            <label class="form__label u-flex u-items-center u-gap-2">
              <i class="bi bi-cpu text-primary"></i>
              Node Mechanism
            </label>
            <select v-model="stepForm.step_type" class="form__select">
              <option value="manual">Human Staff Disposition</option>
              <option value="api_call">Machine Reasoning (API Bridge)</option>
            </select>
            <p class="u-text-[10px] u-text-muted u-mt-1">Manual review vs automated logic</p>
          </div>

          <div class="form__group md:u-col-span-2">
            <label class="form__label u-flex u-items-center u-gap-2">
              <i class="bi bi-info-circle text-primary"></i>
              Functional Designation
            </label>
            <input type="text" v-model="stepForm.step_name" class="form__input font-bold" required
              placeholder="e.g. Identity Verification Service">
          </div>
        </div>

        <!-- Logic & Dispositions Section -->
        <div class="card u-bg-bg-page u-border-primary/10 u-shadow-none">
          <div class="card__body u-p-6">
            <div class="u-flex u-items-center u-justify-between u-mb-4">
              <label class="form__label u-mb-0 u-flex u-items-center u-gap-2">
                <i class="bi bi-diagram-3 text-primary"></i>
                Dispositions (Outcomes)
              </label>
              <button type="button" @click="addOutcome" class="button button--ghost button--small text-primary">
                <i class="bi bi-plus-lg me-1"></i> Add Outcome
              </button>
            </div>

            <div class="u-flex u-flex-col u-gap-3">
              <div v-for="(outcome, idx) in stepForm.api_config.outcomes" :key="idx"
                class="u-flex u-items-center u-gap-4 u-p-3 u-bg-white u-border u-rounded-xl hover:u-border-primary/30 transition-all">
                <div class="u-flex-1">
                  <input type="text" v-model="outcome.label" class="form__input form__input--small"
                    placeholder="Outcome (e.g. Approve)">
                </div>
                <div class="u-w-32">
                  <select v-model="outcome.target_sequence" class="form__select form__select--small">
                    <option :value="null">End Flow</option>
                    <option v-for="s in sortedSteps" :key="s.id" :value="s.sequence">
                      Step {{ s.sequence }}
                    </option>
                    <option v-if="!sortedSteps.find(s => s.sequence === 10)" :value="10">Step 10</option>
                    <option v-if="!sortedSteps.find(s => s.sequence === 20)" :value="20">Step 20</option>
                    <option v-if="!sortedSteps.find(s => s.id)" :value="30">Step 30</option>
                  </select>
                </div>
                <button type="button" @click="removeOutcome(idx)" class="u-text-danger u-p-2">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
              <div v-if="!stepForm.api_config?.outcomes?.length"
                class="u-p-6 u-text-center u-bg-slate-50 u-rounded-xl u-border u-border-dashed">
                <p class="u-text-[10px] u-text-muted u-uppercase">No branching logic - strictly linear</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Mechanism-Specific Options -->
        <div class="u-relative">
          <div v-if="stepForm.step_type === 'manual'" class="card u-bg-bg-page u-border-primary/20 u-shadow-none">
            <div class="card__header u-py-3 u-bg-primary/5">
              <div class="u-flex u-items-center u-gap-2">
                <i class="bi bi-shield-lock text-primary"></i>
                <h6 class="u-text-[11px] u-font-black u-text-primary u-uppercase u-tracking-widest">Manual Node
                  Parameters</h6>
              </div>
            </div>
            <div class="card__body u-p-6">
              <div class="grid grid--2 u-gap-6">
                <div class="form__group">
                  <label class="form__label">Assigned Institutional Role</label>
                  <div class="u-relative">
                    <i class="bi bi-shield-check u-absolute u-left-3 u-top-1/2 -u-translate-y-1/2 u-text-muted"></i>
                    <select v-model="stepForm.role" class="form__select u-pl-10">
                       <option value="" disabled>Select Role</option>
                       <option v-for="r in roles" :key="r.id" :value="r.name">{{ r.name }} ({{ r.permissions?.length || 0 }} perms)</option>
                    </select>
                  </div>
                  <p class="u-text-[10px] u-text-muted u-mt-1">Staff role authorized to handle this step</p>
                </div>
                <div class="form__group">
                  <label class="form__label">Functional Action Label</label>
                  <div class="u-relative">
                    <i class="bi bi-lightning-charge u-absolute u-left-3 u-top-1/2 -u-translate-y-1/2 u-text-muted"></i>
                    <input type="text" v-model="stepForm.action" class="form__input u-pl-10" placeholder="e.g. approve">
                  </div>
                  <p class="u-text-[10px] u-text-muted u-mt-1">Text displayed on the primary action button</p>
                </div>
              </div>
            </div>
          </div>

          <div v-if="stepForm.step_type === 'api_call'" class="card u-bg-bg-page u-border-warning/20 u-shadow-none">
            <div class="card__header u-py-3 u-bg-warning/5">
              <div class="u-flex u-items-center u-gap-2">
                <i class="bi bi-hdd-network text-warning"></i>
                <h6 class="u-text-[11px] u-font-black u-text-warning-dark u-uppercase u-tracking-widest">Automated Node
                  Logic</h6>
              </div>
            </div>
            <div class="card__body u-p-6">

              <!-- Registry Selector -->
              <div class="form__group u-mb-4">
                <label class="form__label">Target Registry</label>
                <select v-model="stepForm.registry_adapter_id" @change="handleAdapterChange" class="form__select">
                  <option :value="null" disabled>Select an Authoritative Registry</option>
                  <option v-for="adapter in registryStore.adapters" :key="adapter.id" :value="adapter.id">
                    {{ adapter.name }} ({{ adapter.code }})
                  </option>
                </select>
                <p class="u-text-[10px] u-text-muted u-mt-1">System to authenticate and exchange data with</p>
              </div>

              <!-- Endpoint Selector -->
              <div class="form__group u-mb-4">
                <label class="form__label">Registry Action</label>
                <select v-model="stepForm.registry_endpoint" @change="handleEndpointChange" class="form__select"
                  :disabled="!stepForm.registry_adapter_id">
                  <option :value="null" disabled>Select Action</option>
                  <option v-for="endpoint in filteredEndpoints" :key="endpoint.id" :value="endpoint.id">
                    {{ endpoint.name }} ({{ endpoint.method }})
                  </option>
                </select>
                <p class="u-text-[10px] u-text-muted u-mt-1">Specific operation to execute</p>
              </div>


              <!-- Read-only Preview -->
              <!-- <div v-if="stepForm.api_config" class="u-p-3 u-bg-slate-50 u-rounded-lg u-border u-border-slate-200">
                <div class="u-text-[10px] u-font-bold u-text-slate-500 u-mb-1">GENERATED CONFIGURATION</div>
                <pre class="u-text-[10px] u-font-mono u-text-slate-700">{{ JSON.stringify(stepForm.api_config, null, 2) }}</pre>
              </div> -->

              <!-- Registry Mapper Integration -->
              <div v-if="stepForm.registry_endpoint && stepForm.api_config" class="u-mt-4">
                <RegistryMapper :endpoint-id="stepForm.registry_endpoint" :service-form-fields="availableFormFields"
                  v-model="stepForm.api_config.input_mapping" />
              </div>

            </div>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="u-flex u-justify-between u-items-center u-mt-4 u-pt-6 u-border-t u-border-border-color">
          <button type="button" @click="closeModal" class="button button--secondary">
            <i class="bi bi-x-lg u-me-2"></i> Cancel
          </button>
          <button type="submit" class="button button--primary u-px-8 u-shadow-lg">
            <i class="bi bi-shield-check u-me-2"></i> {{ stepForm.id ? 'Sync Registry Node' : 'Initialize Node' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
  import { ref, computed, watch, onMounted } from 'vue';
  import api from '../../services/api';
  import { useWorkflowStepStore } from '../../store/workflowStep';
  import { useRegistryStore } from '../../store/registry';
  import { useServiceConfigStore } from '../../store/serviceConfig';
  import BaseModal from '../Common/BaseModal.vue';
  import RegistryMapper from './RegistryMapper.vue';
  import BpmnRenderer from './BpmnRenderer.vue';

  const props = defineProps({
    serviceConfigId: {
      type: Number,
      required: true,
    },
  });

  const stepStore = useWorkflowStepStore();
  const registryStore = useRegistryStore();
  const serviceConfigStore = useServiceConfigStore();
  const roles = ref([]);
  const showModal = ref(false);
  const searchQuery = ref('');

  const fetchRoles = async () => {
    try {
      const response = await api.get('/roles/');
      roles.value = response.data;
    } catch (e) {
      console.error("Failed to fetch roles", e);
    }
  };

  const stepForm = ref({
    id: null,
    service_config: props.serviceConfigId,
    sequence: 1,
    step_name: '',
    step_type: 'manual',
    role: '',
    action: '',
    registry_adapter_id: null,
    registry_endpoint: null,
    api_config: { input_mapping: {} },
  });

  onMounted(() => {
    registryStore.fetchAdapters();
    registryStore.fetchEndpoints();
    fetchRoles();
  });

  const filteredEndpoints = computed(() => {
    if (!stepForm.value.registry_adapter_id) return [];
    return registryStore.endpoints.filter(e => e.adapter === stepForm.value.registry_adapter_id);
  });

  const availableFormFields = computed(() => {
    const service = serviceConfigStore.services.find(s => s.id === props.serviceConfigId);
    if (service && service.config && service.config.rules && service.config.rules.schema && service.config.rules.schema.properties) {
      return Object.keys(service.config.rules.schema.properties);
    }
    return [];
  });

  const handleAdapterChange = () => {
    stepForm.value.registry_endpoint = null;
    stepForm.value.api_config = { input_mapping: {} };
  };

  const handleEndpointChange = () => {
    if (!stepForm.value.registry_endpoint) return;

    const endpointId = parseInt(stepForm.value.registry_endpoint);
    const endpoint = registryStore.endpoints.find(e => e.id === endpointId);
    const adapter = registryStore.adapters.find(a => a.id === stepForm.value.registry_adapter_id);

    if (endpoint && adapter) {
      // Auto-generate API Config
      stepForm.value.api_config = {
        url: `${adapter.base_url}${endpoint.path}`,
        method: endpoint.method,
        headers: adapter.auth_config?.headers || {},
        input_mapping: stepForm.value.api_config?.input_mapping || {}
      };

      // Auto-set step name if empty or generic
      if (!stepForm.value.step_name || stepForm.value.step_name === 'UNDEFINED_BACKBONE_NODE') {
        stepForm.value.step_name = endpoint.name;
      }
    }
  };

  const getRoleLabel = (step) => step.role || 'GOK_OFFICER';
  const getActionLabel = (step) => step.action || 'Default Review';
  const getApiUrlLabel = (step) => step.api_config?.url || 'INTERNAL_REGISTRY_BRIDGE';

  watch(() => props.serviceConfigId, (newId) => {
    if (newId) {
      stepStore.fetchSteps(newId);
      stepForm.value.service_config = newId;
    }
  }, { immediate: true });

  const sortedSteps = computed(() => stepStore.steps ? stepStore.steps.slice().sort((a, b) => a.sequence - b.sequence) : []);

  const filteredSteps = computed(() => {
    if (!searchQuery.value) return sortedSteps.value;
    const q = searchQuery.value.toLowerCase();
    return sortedSteps.value.filter(s =>
      s.step_name.toLowerCase().includes(q) ||
      (s.role && s.role.toLowerCase().includes(q))
    );
  });

  const addOutcome = () => {
    if (!stepForm.value.api_config.outcomes) {
      stepForm.value.api_config.outcomes = [];
    }
    stepForm.value.api_config.outcomes.push({ label: '', target_sequence: null });
  };

  const removeOutcome = (index) => {
    stepForm.value.api_config.outcomes.splice(index, 1);
  };

  const handleStepSubmit = async () => {
    const payload = { ...stepForm.value };

    if (!payload.service_config) {
      alert("Critical Error: Service Reference ID missing.");
      return;
    }

    if (payload.step_type === 'manual') {
      // Keep api_config if it contains outcomes, otherwise null
      if (!payload.api_config?.outcomes?.length) {
        payload.api_config = null;
      }
      payload.registry_endpoint = null;
    } else {
      payload.role = null;
      payload.action = null;
      if (!payload.registry_endpoint) {
        alert("Please select a Registry Action.");
        return;
      }
    }

    delete payload.registry_adapter_id;

    try {
      let success = false;
      if (payload.id) {
        success = await stepStore.updateStep(payload);
      } else {
        success = await stepStore.createStep(payload);
      }

      if (success) {
        closeModal();
      }
    } catch (error) {
      console.error("WorkflowStep Submit Error:", error);
      alert("Deployment Error: " + (error.response?.data ? JSON.stringify(error.response.data) : error.message));
    }
  };

  const openCreateModal = () => {
    resetStepForm();
    showModal.value = true;
  };

  const editStep = (step) => {
    stepForm.value = { ...step };

    if (step.registry_endpoint_details) {
      stepForm.value.registry_adapter_id = step.registry_endpoint_details.adapter;
      stepForm.value.registry_endpoint = step.registry_endpoint_details.id;
    }

    if (!stepForm.value.api_config) {
      stepForm.value.api_config = { input_mapping: {}, outcomes: [] };
    } else {
      if (!stepForm.value.api_config.input_mapping) stepForm.value.api_config.input_mapping = {};
      if (!stepForm.value.api_config.outcomes) stepForm.value.api_config.outcomes = [];
    }

    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
    resetStepForm();
  };

  const deleteStep = async (id) => {
    if (confirm('Decommission this workflow step? This cannot be undone.')) {
      await stepStore.deleteStep(id);
    }
  };

  const resetStepForm = () => {
    let nextSequence = 10;
    if (sortedSteps.value && sortedSteps.value.length > 0) {
      const maxSeq = Math.max(...sortedSteps.value.map(s => parseInt(s.sequence || 0)));
      nextSequence = isNaN(maxSeq) ? 10 : maxSeq + 10;
    }

    stepForm.value = {
      id: null,
      service_config: props.serviceConfigId,
      sequence: nextSequence,
      step_name: '',
      step_type: 'manual',
      role: 'officer',
      action: 'Initiate Review',
      registry_adapter_id: null,
      registry_endpoint: null,
      api_config: { input_mapping: {}, outcomes: [] },
    };
  };
</script>

<style scoped>

  /* Local color system mapping to app variables */
  .u-bg-primary-soft {
    background-color: var(--color-primary-soft);
  }

  .u-bg-warning-soft {
    background-color: var(--color-warning-soft);
  }

  .u-text-warning-dark {
    color: var(--color-warning-dark);
  }

  .u-animate-fade-in {
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
