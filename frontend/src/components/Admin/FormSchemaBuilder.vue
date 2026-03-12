<template>
  <div class="schema-builder">
    <!-- Strategic Header: Data Definition -->
    <div class="u-flex u-justify-between u-items-center u-mb-6">
      <div class="page__title-group">
        <h4 class="page__title u-text-lg">Technical Schema Registry</h4>
        <p class="page__subtitle u-text-xs">Define institutional data requirements for this service</p>
      </div>
      <button type="button" @click="openCreateModal" class="button button--primary button--small shadow-md">
        <i class="bi bi-plus-lg me-1"></i> Register New Data Field
      </button>
    </div>

    <!-- Field List: Institutional Blueprint -->
    <div class="u-mb-10">
      <div v-if="!modelValue || !modelValue.properties || Object.keys(modelValue.properties).length === 0"
        class="u-p-16 u-text-center u-bg-bg-page u-rounded-[2.5rem] u-border-2 u-border-dashed u-border-border-color/60">
        <div
          class="u-w-16 u-h-16 u-bg-white u-rounded-2xl u-flex u-items-center u-justify-center u-mx-auto u-mb-4 u-shadow-inner u-border">
          <i class="bi bi-ui-checks-grid u-text-3xl u-text-primary/30"></i>
        </div>
        <h5 class="u-font-black u-text-main u-uppercase u-tracking-[0.2em] u-text-xs u-mb-2">Schema Undefined</h5>
        <p class="u-text-xs u-text-muted/60 u-max-w-xs u-mx-auto u-mb-6">Initialize the institutional data blueprint by
          adding your first required field.</p>
        <button type="button" @click="openCreateModal" class="button button--primary button--small">
          Initialize Schema
        </button>
      </div>

      <div v-else class="u-flex u-flex-col u-gap-3">
        <div v-for="(field, key) in modelValue.properties" :key="key"
          class="card hover:u-border-primary/40 hover:u-shadow-lg transition-all group u-border-border-color">
          <div class="card__body u-p-4">
            <div class="u-flex u-items-center u-justify-between">
              <div class="u-flex-1">
                <div class="u-flex u-items-center u-gap-3 u-mb-1">
                  <div class="u-w-8 u-h-8 u-rounded-lg u-bg-bg-page u-flex u-items-center u-justify-center">
                    <i :class="getFieldIcon(field.type, field.format, field.widget)"
                      class="u-text-primary u-text-base"></i>
                  </div>
                  <div>
                    <h5 class="u-font-black u-text-main u-text-sm u-uppercase u-tracking-widest">{{ field.title }}</h5>
                    <div
                      class="u-flex u-items-center u-gap-3 u-text-[10px] u-font-black u-uppercase u-tracking-widest u-mt-0.5">
                      <span class="u-text-muted/60 font-mono">{{ key }}</span>
                      <span class="u-w-1 u-h-1 u-bg-border-color u-rounded-full"></span>
                      <span class="u-text-primary">{{ getFieldTypeLabel(field.type, field.format, field.widget)
                        }}</span>
                      <span v-if="isRequired(key)" class="u-text-danger u-flex u-items-center u-gap-1">
                        <i class="bi bi-shield-fill-exclamation"></i> Mandatory
                      </span>
                      <span v-if="field.internal_only" class="u-text-muted/60 u-flex u-items-center u-gap-1">
                        <i class="bi bi-person-lock"></i> Staff Only
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="u-flex u-gap-2 u-ml-4">
                <button type="button" @click.stop="editField(key)" class="button button--secondary button--small u-p-2"
                  title="Modify Parameters">
                  <i class="bi bi-pencil-fill"></i>
                </button>
                <button type="button" @click.stop="removeField(key)" class="button button--danger button--small u-p-2"
                  title="Remove Field">
                  <i class="bi bi-trash-fill"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Schema Editor Modal -->
    <BaseModal v-model:show="showModal" :title="isEditing ? 'Modify Field Parameters' : 'Register Service Field'"
      subtitle="Define technical data acquisition parameters for this registry stage" icon="bi-input-cursor-text"
      size="md">
      <form @submit.prevent="addField" class="u-flex u-flex-col u-gap-8 u-p-2">
        <div class="u-grid u-gap-6">
          <div class="grid grid--2 u-gap-4">
            <!-- Field Name -->
            <div class="form__group">
              <label class="form__label u-flex u-items-center u-gap-2">
                <i class="bi bi-code-slash text-primary"></i>
                Technical ID (Slug)
              </label>
              <input type="text" v-model="fieldForm.name" class="form__input font-mono u-font-bold"
                :disabled="isEditing" placeholder="e.g. applicant_name" required>
              <p class="u-text-[10px] u-text-muted u-mt-1">Machine identifier (no spaces)</p>
            </div>

            <!-- Field Label -->
            <div class="form__group">
              <label class="form__label u-flex u-items-center u-gap-2">
                <i class="bi bi-tag text-primary"></i>
                Institutional Designation
              </label>
              <input type="text" v-model="fieldForm.title" class="form__input font-bold"
                placeholder="e.g. Applicant Full Name" required>
              <p class="u-text-[10px] u-text-muted u-mt-1">Human-readable label</p>
            </div>
          </div>

          <div class="grid grid--2 u-gap-4">
            <!-- Field Type -->
            <div class="form__group">
              <label class="form__label u-flex u-items-center u-gap-2">
                <i class="bi bi-ui-radios text-primary"></i>
                Data Mechanism
              </label>
              <select v-model="fieldForm.type" class="form__select">
                <optgroup label="📝 Basic Input">
                  <option value="string">Text (Single Line)</option>
                  <option value="textarea">Text (Multi-Line)</option>
                  <option value="number">Number</option>
                  <option value="email">Email Address</option>
                  <option value="tel">Phone Number</option>
                  <option value="currency">Currency (KES)</option>
                  <option value="date">Date Picker</option>
                  <option value="boolean">Checkbox (Yes/No)</option>
                </optgroup>
                <optgroup label="🎯 Selection">
                  <option value="select">Dropdown (Select)</option>
                  <option value="radio">Radio Buttons</option>
                  <option value="checkbox-group">Multi-Select (Checkboxes)</option>
                </optgroup>
                <optgroup label="📎 Advanced">
                  <option value="file">File Upload</option>
                  <option value="registry_lookup">Registry Search (Lookup)</option>
                </optgroup>
              </select>
            </div>

            <!-- Options for Select/Radio/Checkbox -->
            <div v-if="['select', 'radio', 'checkbox-group'].includes(fieldForm.type)" class="form__group">
              <label class="form__label u-flex u-items-center u-gap-2">
                <i class="bi bi-list-ul text-primary"></i>
                Mechanism Options
              </label>
              <input type="text" v-model="fieldForm.enum" class="form__input"
                placeholder="e.g. Option 1, Option 2, Option 3">
              <p class="u-text-[10px] u-text-muted u-mt-1">Separate options with commas</p>
            </div>

            <!-- Registry Lookup Configuration -->
            <div v-if="fieldForm.type === 'registry_lookup'" class="form__group">
                <label class="form__label u-flex u-items-center u-gap-2">
                    <i class="bi bi-hdd-network text-primary"></i>
                    Registry Source
                </label>
                <div class="u-space-y-2">
                    <select v-model="fieldForm.registry_adapter" class="form__select icon-select">
                        <option :value="null" disabled>Select Registry...</option>
                        <option v-for="adapter in registryStore.adapters" :key="adapter.id" :value="adapter.id">
                            {{ adapter.name }} ({{ adapter.code }})
                        </option>
                    </select>
                    
                    <select v-model="fieldForm.registry_endpoint" class="form__select" :disabled="!fieldForm.registry_adapter">
                        <option :value="null" disabled>Select Data Operation...</option>
                        <option v-for="ep in availableEndpoints" :key="ep.id" :value="ep.id">
                           {{ ep.name }} ({{ ep.method }})
                        </option>
                    </select>
                </div>
                <p class="u-text-[10px] u-text-muted u-mt-1">External system to fetch data from</p>
            </div>
          </div>

          <!-- Description -->
          <div class="form__group">
            <label class="form__label u-flex u-items-center u-gap-2">
              <i class="bi bi-chat-left-text text-primary"></i>
              Instructional Helper Text
            </label>
            <input type="text" v-model="fieldForm.description" class="form__input"
              placeholder="Provide guidance for citizens completing this field">
          </div>
        </div>

        <!-- Strategy Options -->
        <div class="u-flex u-flex-col u-gap-3 u-p-4 u-bg-bg-page u-rounded-xl u-border u-border-border-color">
          <div class="u-flex u-justify-between u-items-center">
            <div class="u-flex u-items-center u-gap-3">
              <input type="checkbox" v-model="fieldForm.required" id="required-field" class="form__checkbox">
              <label for="required-field"
                class="u-text-xs u-font-black u-text-main u-uppercase u-tracking-widest cursor-pointer">
                Mandatory Institutional Data
              </label>
            </div>
            <div class="u-flex u-gap-2">
              <i class="bi bi-shield-fill-check u-text-success text-sm"></i>
            </div>
          </div>

          <div class="u-border-t u-border-border-color/40 my-1"></div>

          <div class="u-flex u-justify-between u-items-center">
            <div class="u-flex u-items-center u-gap-3">
              <input type="checkbox" v-model="fieldForm.internal_only" id="internal-only-field" class="form__checkbox">
              <label for="internal-only-field"
                class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest cursor-pointer">
                Internal Agency Field (Staff Only)
              </label>
            </div>
            <div class="u-flex u-gap-2">
              <i class="bi bi-person-lock u-text-muted text-sm"></i>
            </div>
          </div>
        </div>

        <!-- Strategic Actions -->
        <div class="u-flex u-justify-between u-items-center u-mt-4 u-pt-6 u-border-t">
          <button type="button" @click="closeModal" class="button button--secondary button--small">
            <i class="bi bi-x-lg u-me-2"></i> Cancel
          </button>
          <button type="submit" class="button button--primary u-px-8 u-shadow-lg">
            <i class="bi bi-cloud-arrow-up u-me-2"></i> {{ isEditing ? 'Sync Field configuration' : 'Commit Data Field'
            }}
          </button>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
  import { ref, computed, watch, onMounted } from 'vue';
  import BaseModal from '../Common/BaseModal.vue';
  import { useRegistryStore } from '../../store/registry'; // Import Registry Store

  const props = defineProps({
    modelValue: {
      type: Object,
      required: true,
    },
  });

  const registryStore = useRegistryStore(); // Initialize Store

  const emit = defineEmits(['update:modelValue']);

  const schema = ref({ properties: {}, required: [] });
  const isEditing = ref(false);
  const showModal = ref(false);
  const originalFieldName = ref(null);

  const fieldForm = ref({
    name: '',
    title: '',
    type: 'string',
    description: '',
    enum: '',
    required: false,
    internal_only: false,
    registry_adapter: null,
    registry_endpoint: null
  });

  const availableEndpoints = computed(() => {
      if (!fieldForm.value.registry_adapter) return [];
      return registryStore.endpoints.filter(e => e.adapter === fieldForm.value.registry_adapter && e.method === 'GET'); // Only GET for lookups
  });

  watch(() => props.modelValue, (newSchema) => {
    if (newSchema && newSchema.properties) {
      schema.value = JSON.parse(JSON.stringify(newSchema)); // Deep copy
      if (!schema.value.required) schema.value.required = [];
    } else {
      schema.value = { type: 'object', properties: {}, required: [] };
    }
  }, { immediate: true, deep: true });

  onMounted(() => {
    registryStore.fetchAdapters();
    registryStore.fetchEndpoints();
  });

  const isRequired = (key) => props.modelValue?.required?.includes(key);

  const updateParent = () => {
    emit('update:modelValue', { ...schema.value });
  };

  const openCreateModal = () => {
    resetFieldForm();
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
    resetFieldForm();
  };

  const addField = () => {
    const { name, title, type, required, internal_only, description, enum: enumStr, registry_adapter, registry_endpoint } = fieldForm.value;
    if (!name || !title) return;

    if (isEditing.value && originalFieldName.value && originalFieldName.value !== name) {
      delete schema.value.properties[originalFieldName.value];
      const reqIndex = schema.value.required.indexOf(originalFieldName.value);
      if (reqIndex > -1) schema.value.required.splice(reqIndex, 1);
    }

    let newField = { title };
    if (description) newField.description = description;
    if (internal_only) newField.internal_only = true;

    switch (type) {
      case 'string':
        newField.type = 'string';
        break;
      case 'textarea':
        newField.type = 'string';
        newField.format = 'textarea';
        break;
      case 'number':
        newField.type = 'number';
        break;
      case 'email':
        newField.type = 'string';
        newField.format = 'email';
        break;
      case 'tel':
        newField.type = 'string';
        newField.format = 'tel';
        break;
      case 'currency':
        newField.type = 'number';
        newField.format = 'currency';
        break;
      case 'date':
        newField.type = 'string';
        newField.format = 'date';
        break;
      case 'boolean':
        newField.type = 'boolean';
        break;
      case 'file':
        newField.type = 'string';
        newField.format = 'data-url';
        break;
      case 'select':
        newField.type = 'string';
        newField.enum = enumStr ? enumStr.split(',').map(s => s.trim()) : [];
        break;
      case 'radio':
        newField.type = 'string';
        newField.enum = enumStr ? enumStr.split(',').map(s => s.trim()) : [];
        newField.widget = 'radio';
        break;
      case 'checkbox-group':
        newField.type = 'string';
        newField.widget = 'checkbox-group';
        newField.enum = enumStr ? enumStr.split(',').map(s => s.trim()) : [];
        break;
      case 'registry_lookup':
        newField.type = 'string';
        newField.format = 'registry_lookup';
        newField['x-registry-config'] = {
            adapter_id: registry_adapter,
            endpoint_id: registry_endpoint
        };
        break;
      default:
        newField.type = 'string';
    }

    schema.value.properties[name] = newField;

    if (!schema.value.required) schema.value.required = [];
    const reqIndex = schema.value.required.indexOf(name);
    if (required && reqIndex === -1) {
      schema.value.required.push(name);
    } else if (!required && reqIndex > -1) {
      schema.value.required.splice(reqIndex, 1);
    }

    updateParent();
    closeModal();
  };

  const editField = (key) => {
    const field = schema.value.properties[key];
    fieldForm.value.name = key;
    fieldForm.value.title = field.title;
    fieldForm.value.description = field.description || '';

    if (field.format === 'textarea') fieldForm.value.type = 'textarea';
    else if (field.format === 'email') fieldForm.value.type = 'email';
    else if (field.format === 'tel') fieldForm.value.type = 'tel';
    else if (field.format === 'currency') fieldForm.value.type = 'currency';
    else if (field.format === 'date') fieldForm.value.type = 'date';
    else if (field.format === 'data-url') fieldForm.value.type = 'file';
    else if (field.type === 'boolean') fieldForm.value.type = 'boolean';
    else if (field.widget === 'radio') fieldForm.value.type = 'radio';
    else if (field.widget === 'checkbox-group') fieldForm.value.type = 'checkbox-group';
    else if (field.enum) fieldForm.value.type = 'select';
    else if (field.type === 'number') fieldForm.value.type = 'number';
    else if (field.format === 'registry_lookup') {
        fieldForm.value.type = 'registry_lookup';
        if (field['x-registry-config']) {
            fieldForm.value.registry_adapter = field['x-registry-config'].adapter_id;
            fieldForm.value.registry_endpoint = field['x-registry-config'].endpoint_id;
        }
    }
    else fieldForm.value.type = 'string';

    if (field.enum) {
      fieldForm.value.enum = field.enum.join(', ');
    } else {
      fieldForm.value.enum = '';
    }

    fieldForm.value.required = isRequired(key);
    fieldForm.value.internal_only = !!field.internal_only;
    originalFieldName.value = key;
    isEditing.value = true;
    showModal.value = true;
  };

  const removeField = (key) => {
    if (confirm(`Are you sure you want to delete field "${key}"?`)) {
      delete schema.value.properties[key];
      const reqIndex = schema.value.required?.indexOf(key);
      if (reqIndex > -1) schema.value.required.splice(reqIndex, 1);
      updateParent();
    }
  };

  const resetFieldForm = () => {
    fieldForm.value = {
      name: '',
      title: '',
      type: 'string',
      description: '',
      enum: '',
      required: false,
      internal_only: false,
      registry_adapter: null,
      registry_endpoint: null
    };
    isEditing.value = false;
    originalFieldName.value = null;
  };

  const getFieldIcon = (type, format, widget) => {
    if (format === 'textarea') return 'bi bi-textarea-t';
    if (format === 'email') return 'bi bi-envelope-at';
    if (format === 'tel') return 'bi bi-telephone';
    if (format === 'currency') return 'bi bi-currency-exchange';
    if (format === 'date') return 'bi bi-calendar-date';
    if (format === 'data-url') return 'bi bi-paperclip';
    if (type === 'boolean') return 'bi bi-check-square';
    if (type === 'number') return 'bi bi-123';
    if (widget === 'radio') return 'bi bi-ui-radios';
    if (widget === 'checkbox-group') return 'bi bi-ui-checks';
    if (format === 'registry_lookup') return 'bi bi-cloud-download';
    return 'bi bi-input-cursor-text';
  };

  const getFieldTypeLabel = (type, format, widget) => {
    if (format === 'textarea') return 'Multi-Line Text';
    if (format === 'email') return 'Email';
    if (format === 'tel') return 'Phone';
    if (format === 'currency') return 'Currency';
    if (format === 'date') return 'Date';
    if (format === 'data-url') return 'File Upload';
    if (format === 'registry_lookup') return 'Registry Lookup';
    if (type === 'boolean') return 'Checkbox';
    if (type === 'number') return 'Number';
    if (widget === 'radio') return 'Radio Buttons';
    if (widget === 'checkbox-group') return 'Multi-Select';
    if (type === 'string') return 'Text';
    return type;
  };
</script>
