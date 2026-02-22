<template>
  <div class="registry-mapper">
    <div v-if="loading" class="u-flex u-justify-center u-p-4">
      <i class="bi bi-arrow-repeat u-animate-spin u-text-2xl u-text-primary"></i>
    </div>

    <div v-else-if="endpoint" class="u-animate-fade-in">
      <!-- Endpoint Summary -->
      <div class="u-bg-bg-page u-p-3 u-rounded-lg u-mb-4 u-flex u-items-center u-justify-between">
        <div>
          <div class="u-text-xs u-font-bold u-text-primary u-uppercase">{{ endpoint.method }}</div>
          <div class="u-font-bold u-text-sm">{{ endpoint.path }}</div>
        </div>
        <div class="u-text-right">
          <div class="u-text-[10px] u-text-muted u-uppercase">Registry Adapter</div>
          <div class="u-font-bold u-text-xs">{{ endpoint.adapter_name || 'System' }}</div>
        </div>
      </div>

      <!-- Input Mapping Section -->
      <div class="u-mb-6">
        <h5 class="u-text-xs u-font-black u-uppercase u-text-muted u-mb-2">
          <i class="bi bi-box-arrow-in-right u-mr-1"></i> Data Input Mapping
        </h5>

        <div v-if="endpoint.input_schema && endpoint.input_schema.length > 0"
          class="u-border u-border-border-color u-rounded-lg u-overflow-hidden">
          <table class="table u-w-full u-text-sm">
            <thead class="u-bg-bg-page">
              <tr>
                <th class="u-p-2 u-text-left u-font-bold u-text-xs u-text-muted">Registry Field</th>
                <th class="u-p-2 u-text-left u-font-bold u-text-xs u-text-muted">Type</th>
                <th class="u-p-2 u-text-left u-font-bold u-text-xs u-text-muted">Source Data (Service Form)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="field in endpoint.input_schema" :key="field.key" class="u-border-t u-border-border-color">
                <td class="u-p-2">
                  <div class="u-font-bold">{{ field.label }}</div>
                  <div class="u-text-[10px] u-font-mono u-text-primary">{{ field.key }}</div>
                  <span v-if="field.required" class="u-text-[9px] u-text-danger u-font-bold u-uppercase">Required</span>
                </td>
                <td class="u-p-2">
                  <span class="badge badge--small">{{ field.type }}</span>
                </td>
                <td class="u-p-2">
                  <select v-model="mapping[field.key]" @change="updateMapping" class="form__select u-w-full u-text-xs"
                    :class="{ 'u-border-primary': mapping[field.key] }">
                    <option value="" disabled>Select Source Variable...</option>
                    <optgroup label="Form Fields">
                      <option v-for="formField in serviceFormFields" :key="formField" :value="`{{form.${formField}}}`">
                        {{ formField }} (Form)
                      </option>
                    </optgroup>
                    <optgroup label="System Context">
                      <option value="{{citizen.id}}">Citizen ID</option>
                      <option value="{{citizen.email}}">Citizen Email</option>
                      <option value="{{request.id}}">Request ID</option>
                    </optgroup>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="u-p-4 u-text-center u-text-sm u-text-muted u-italic u-bg-bg-page u-rounded-lg">
          No input parameters required for this endpoint.
        </div>
      </div>

      <!-- Output Reference Section -->
      <div class="u-mb-6">
        <h5 class="u-text-xs u-font-black u-uppercase u-text-success u-mb-2">
          <i class="bi bi-box-arrow-right u-mr-1"></i> Available Data Outputs
        </h5>

        <div v-if="endpoint.output_schema && endpoint.output_schema.length > 0" class="u-grid u-grid-cols-2 u-gap-2">
          <div v-for="output in endpoint.output_schema" :key="output.key"
            class="u-p-2 u-bg-success/5 u-border u-border-success/20 u-rounded u-flex u-items-center u-justify-between">
            <div>
              <div class="u-text-xs u-font-bold">{{ output.label }}</div>
              <div class="u-text-[10px] u-font-mono u-text-muted">{{ output.key }}</div>
            </div>
            <span class="badge badge--success u-text-[9px]">{{ output.type }}</span>
          </div>
        </div>
        <div v-else class="u-p-4 u-text-center u-text-sm u-text-muted u-italic u-bg-bg-page u-rounded-lg">
          No structured output schema defined.
        </div>
      </div>

      <!-- Logic Integration Note -->
      <div class="u-p-4 u-bg-primary-soft/30 u-border u-border-primary/20 u-rounded-xl">
        <div class="u-flex u-gap-3">
          <i class="bi bi-robot u-text-primary u-text-lg"></i>
          <div>
            <div class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest">Automation Note</div>
            <p class="u-text-[10px] u-text-muted/80 u-mb-0">
              Machine reasoning uses these outputs to determine the next stage.
              Configure branching rules in the <b>Dispositions</b> section above.
            </p>
          </div>
        </div>
      </div>

    </div>

    <div v-else-if="error" class="u-p-8 u-text-center u-bg-danger/5 u-border u-border-danger/20 u-rounded-lg">
      <i class="bi bi-exclamation-triangle u-text-2xl u-text-danger u-mb-2 u-block"></i>
      <div class="u-text-sm u-font-bold u-text-danger">{{ error }}</div>
      <button type="button" @click="fetchEndpointDetails(endpointId)" class="button button--ghost button--small u-mt-4">
        <i class="bi bi-arrow-clockwise me-1"></i> Retry Handshake
      </button>
    </div>

    <div v-else class="u-p-8 u-text-center u-text-muted">
      Select a Registry Endpoint to configure mapping.
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, onMounted } from 'vue';
  import api from '../../services/api';

  const props = defineProps({
    endpointId: {
      type: [Number, String],
      default: null
    },
    serviceFormFields: {
      type: Array,
      default: () => []
    },
    modelValue: {
      type: Object,
      default: () => ({})
    }
  });

  const emit = defineEmits(['update:modelValue']);

  const loading = ref(false);
  const endpoint = ref(null);
  const mapping = ref({});

  const error = ref(null);

  // Initialize mapping from prop or default to empty
  watch(() => props.modelValue, (val) => {
    if (val) {
      mapping.value = { ...val };
    }
  }, { immediate: true });

  watch(() => props.endpointId, async (newId) => {
    console.log("RegistryMapper: endpointId changed to", newId);
    if (!newId) {
      endpoint.value = null;
      return;
    }
    await fetchEndpointDetails(newId);
  }, { immediate: true });

  const fetchEndpointDetails = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.get(`/registry-endpoints/${id}/`);
      endpoint.value = response.data;
      console.log("RegistryMapper: Loaded endpoint", endpoint.value);
      // Auto-populate mapping if keys match exactly? Optional enhancement.
      // For now, respect existing mapping.
    } catch (err) {
      console.error("Failed to fetch registry endpoint details", err);
      error.value = "Failed to load authoritative schema. Ensure the registry registry is reachable.";
      endpoint.value = null;
    } finally {
      loading.value = false;
    }
  };

  const updateMapping = () => {
    emit('update:modelValue', mapping.value);
  };
</script>

<style scoped>
  .table th {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.7rem;
  }
</style>
