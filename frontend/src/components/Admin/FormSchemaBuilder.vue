<template>
  <div class="schema-builder">
    <!-- Field List -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-sm font-black uppercase tracking-widest text-muted flex items-center gap-2">
          <i class="bi bi-list-check"></i>
          <span>Form Fields</span>
          <span class="badge badge--small badge--secondary">{{ Object.keys(schema.properties).length }}</span>
        </h4>
      </div>

      <div v-if="Object.keys(schema.properties).length === 0"
        class="relative overflow-hidden rounded-xl border-2 border-dashed border-slate-200 bg-gradient-to-br from-slate-50 to-white p-12 text-center">
        <div class="relative z-10">
          <div
            class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-primary/10 to-primary/5 mb-4">
            <i class="bi bi-inbox text-5xl text-primary/40"></i>
          </div>
          <h5 class="font-black text-lg text-main mb-2">No Fields Defined Yet</h5>
          <p class="text-sm text-muted mb-4 max-w-md mx-auto">
            Start building your form by adding fields below. Define the data you need to collect from citizens.
          </p>
          <div class="flex items-center justify-center gap-2 text-xs text-muted">
            <i class="bi bi-arrow-down-circle"></i>
            <span>Add your first field using the form below</span>
          </div>
        </div>
        <!-- Decorative background -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -z-0"></div>
        <div class="absolute bottom-0 left-0 w-48 h-48 bg-success/5 rounded-full blur-3xl -z-0"></div>
      </div>

      <div v-else class="space-y-2">
        <div v-for="(field, key) in schema.properties" :key="key"
          class="card border border-border-color hover:border-primary transition-all group">
          <div class="card__body p-4">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <i :class="getFieldIcon(field.type, field.format, field.widget)" class="text-primary text-lg"></i>
                  <div>
                    <h5 class="font-bold text-main">{{ field.title }}</h5>
                    <div class="flex items-center gap-2 text-xs text-muted mt-1">
                      <span class="font-mono bg-slate-100 px-2 py-0.5 rounded">{{ key }}</span>
                      <span class="badge badge--small" :class="getTypeBadgeClass(field.type, field.format)">
                        {{ getFieldTypeLabel(field.type, field.format, field.widget) }}
                      </span>
                      <span v-if="isRequired(key)" class="badge badge--small badge--danger">
                        <i class="bi bi-asterisk text-[8px]"></i> Required
                      </span>
                    </div>
                  </div>
                </div>
                <p v-if="field.description" class="text-sm text-muted mt-2 pl-8">
                  <i class="bi bi-info-circle me-1"></i>{{ field.description }}
                </p>
                <div v-if="field.enum" class="mt-2 pl-8">
                  <div class="flex flex-wrap gap-1">
                    <span v-for="(option, idx) in field.enum" :key="idx"
                      class="text-xs bg-primary-soft text-primary px-2 py-1 rounded font-medium">
                      {{ option }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex gap-2 ml-4">
                <button type="button" @click.stop="editField(key)"
                  class="button button--ghost button--small text-primary hover:bg-primary-soft">
                  <i class="bi bi-pencil"></i>
                </button>
                <button type="button" @click.stop="removeField(key)"
                  class="button button--ghost button--small text-danger hover:bg-red-50">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Field Form -->
    <div class="relative">
      <!-- Animated gradient border effect -->
      <div
        class="absolute -inset-0.5 bg-gradient-to-r from-primary via-success to-secondary rounded-xl opacity-20 blur">
      </div>

      <div
        class="relative card border-2 border-dashed border-primary/30 bg-gradient-to-br from-white to-primary-soft/10 shadow-lg">
        <div class="card__header bg-gradient-to-r from-primary/10 to-primary/5 border-b border-primary/20">
          <div class="flex items-center justify-between">
            <h5 class="card__title text-primary flex items-center gap-3">
              <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
                <i :class="isEditing ? 'bi bi-pencil-square' : 'bi bi-plus-circle'" class="text-primary"></i>
              </div>
              <span>{{ isEditing ? 'Edit Field Configuration' : 'Add New Field' }}</span>
            </h5>
            <span v-if="!isEditing" class="badge badge--success badge--small">
              <i class="bi bi-stars me-1"></i>New
            </span>
          </div>
          <p class="text-xs text-muted mt-2">
            {{ isEditing ? 'Modify the field properties below' : 'Define a new form field for data collection' }}
          </p>
        </div>
        <div class="card__body">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <!-- Field Name -->
            <div class="form__group">
              <label class="form__label">
                <i class="bi bi-code-slash me-1"></i>Field Name (Key)
              </label>
              <input type="text" v-model="fieldForm.name" class="form__input font-mono" :disabled="isEditing"
                placeholder="e.g. applicant_name" required>
              <p class="text-xs text-muted mt-1">
                <i class="bi bi-info-circle me-1"></i>Unique identifier (no spaces)
              </p>
            </div>

            <!-- Field Label -->
            <div class="form__group">
              <label class="form__label">
                <i class="bi bi-tag me-1"></i>Display Label
              </label>
              <input type="text" v-model="fieldForm.title" class="form__input" placeholder="e.g. Applicant Full Name"
                required>
              <p class="text-xs text-muted mt-1">
                <i class="bi bi-info-circle me-1"></i>User-facing label
              </p>
            </div>

            <!-- Field Type -->
            <div class="form__group">
              <label class="form__label">
                <i class="bi bi-ui-radios me-1"></i>Field Type
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
                </optgroup>
                <optgroup label="🎨 Layout">
                  <option value="section_header">Section Header</option>
                  <option value="info_text">Info Text</option>
                </optgroup>
              </select>
            </div>

            <!-- Options for Select/Radio/Checkbox -->
            <div v-if="['select', 'radio', 'checkbox-group'].includes(fieldForm.type)" class="form__group">
              <label class="form__label">
                <i class="bi bi-list-ul me-1"></i>Options (Comma Separated)
              </label>
              <input type="text" v-model="fieldForm.enum" class="form__input"
                placeholder="e.g. Option 1, Option 2, Option 3">
              <p class="text-xs text-muted mt-1">
                <i class="bi bi-info-circle me-1"></i>Separate with commas
              </p>
            </div>

            <!-- Description -->
            <div class="form__group md:col-span-2">
              <label class="form__label">
                <i class="bi bi-chat-left-text me-1"></i>Help Text / Description
              </label>
              <input type="text" v-model="fieldForm.description" class="form__input"
                placeholder="Optional helper text for users">
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-between pt-4 border-t border-border-color">
            <div class="flex items-center gap-2">
              <input type="checkbox" v-model="fieldForm.required" id="required-field" class="form__checkbox">
              <label for="required-field" class="text-sm font-medium text-main cursor-pointer">
                <i class="bi bi-asterisk text-danger text-xs me-1"></i>Required Field
              </label>
            </div>
            <div class="flex gap-2">
              <button v-if="isEditing" type="button" @click.stop="resetFieldForm" class="button button--secondary">
                <i class="bi bi-x-lg me-2"></i>Cancel
              </button>
              <button type="button" @click.stop="addField"
                class="button button--primary shadow-lg hover:shadow-xl transition-all">
                <i :class="isEditing ? 'bi bi-check-lg' : 'bi bi-plus-lg'" class="me-2"></i>
                {{ isEditing ? 'Update Field' : 'Add Field' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, watch } from 'vue';

  const props = defineProps({
    modelValue: {
      type: Object,
      required: true,
    },
  });

  const emit = defineEmits(['update:modelValue']);

  const schema = ref({ properties: {}, required: [] });
  const isEditing = ref(false);
  const originalFieldName = ref(null);

  const fieldForm = ref({
    name: '',
    title: '',
    type: 'string', // This is the UI type selection
    description: '',
    enum: '',
    required: false,
  });

  watch(() => props.modelValue, (newConfig) => {
    if (newConfig && newConfig.rules && newConfig.rules.schema) {
      schema.value = JSON.parse(JSON.stringify(newConfig.rules.schema)); // Deep copy
    } else {
      schema.value = { properties: {}, required: [] };
    }
  }, { immediate: true, deep: true });

  const isRequired = (key) => schema.value.required?.includes(key);

  const updateParent = () => {
    const newConfig = { ...props.modelValue, rules: { ...props.modelValue.rules, schema: schema.value } };
    emit('update:modelValue', newConfig);
  };

  const addField = () => {
    const { name, title, type, required, description, enum: enumStr } = fieldForm.value;
    if (!name || !title) return;

    // If editing, remove the old field first (simple way to update)
    if (isEditing.value && originalFieldName.value && originalFieldName.value !== name) {
      delete schema.value.properties[originalFieldName.value];
      const reqIndex = schema.value.required.indexOf(originalFieldName.value);
      if (reqIndex > -1) schema.value.required.splice(reqIndex, 1);
    }

    // Build the Schema Property Object
    let newField = { title };
    if (description) newField.description = description;

    // Type Mapping Logic
    // UI Type -> JSON Schema Type + Format/Widget
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
      case 'section_header':
        newField.type = 'section_header';
        break;
      case 'info_text':
        newField.type = 'info_text';
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
        newField.type = 'string'; // Or array? Usually checkboxes imply array of strings, but my simplified backend uses string for storing simple values. Let's start with string for single select or simple structure. Actually, multi-select should probably be an array in JSON schema, but my form engine might treat it loosely.
        // Let's stick to the convention I used in ServiceApplicationView:
        // It expects `field.enum`. Ideally value is an array.
        // My seed data used type: 'string' for agencies_consulted, implying it might store a comma-joined string?
        // Wait, in ServiceApplicationView I do `v-model="formData[key]"` with an array context.
        // Let's set type to 'array' ideally, but for now 'string' with widget 'checkbox-group' works if I handle it.
        // Let's explicitly mark it so the viewer knows.
        newField.type = 'string';
        newField.widget = 'checkbox-group';
        newField.enum = enumStr ? enumStr.split(',').map(s => s.trim()) : [];
        break;
      default:
        newField.type = 'string';
    }

    // Update Schema
    schema.value.properties[name] = newField;

    // Handle Required
    if (type !== 'section_header' && type !== 'info_text') {
      if (!schema.value.required) schema.value.required = [];
      const reqIndex = schema.value.required.indexOf(name);
      if (required && reqIndex === -1) {
        schema.value.required.push(name);
      } else if (!required && reqIndex > -1) {
        schema.value.required.splice(reqIndex, 1);
      }
    }

    updateParent();
    resetFieldForm();
  };

  const editField = (key) => {
    const field = schema.value.properties[key];
    fieldForm.value.name = key;
    fieldForm.value.title = field.title;
    fieldForm.value.description = field.description || '';

    // Reverse Map Type
    if (field.type === 'section_header') fieldForm.value.type = 'section_header';
    else if (field.type === 'info_text') fieldForm.value.type = 'info_text';
    else if (field.format === 'textarea') fieldForm.value.type = 'textarea';
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
    else fieldForm.value.type = 'string';

    if (field.enum) {
      fieldForm.value.enum = field.enum.join(', ');
    } else {
      fieldForm.value.enum = '';
    }

    fieldForm.value.required = isRequired(key);

    originalFieldName.value = key;
    isEditing.value = true;
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
      required: false
    };
    isEditing.value = false;
    originalFieldName.value = null;
  };

  // Helper methods for UI
  const getFieldIcon = (type, format, widget) => {
    if (type === 'section_header') return 'bi bi-type-h1';
    if (type === 'info_text') return 'bi bi-info-circle-fill';
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
    if (type === 'string' && format !== 'textarea') {
      // Check for enum (select dropdown)
      return widget ? 'bi bi-menu-button-wide' : 'bi bi-input-cursor-text';
    }
    return 'bi bi-input-cursor-text';
  };

  const getFieldTypeLabel = (type, format, widget) => {
    if (type === 'section_header') return 'Section Header';
    if (type === 'info_text') return 'Info Text';
    if (format === 'textarea') return 'Multi-Line Text';
    if (format === 'email') return 'Email';
    if (format === 'tel') return 'Phone';
    if (format === 'currency') return 'Currency';
    if (format === 'date') return 'Date';
    if (format === 'data-url') return 'File Upload';
    if (type === 'boolean') return 'Checkbox';
    if (type === 'number') return 'Number';
    if (widget === 'radio') return 'Radio Buttons';
    if (widget === 'checkbox-group') return 'Multi-Select';
    if (type === 'string') return 'Text';
    return type;
  };

  const getTypeBadgeClass = (type, format) => {
    if (type === 'section_header' || type === 'info_text') return 'badge--secondary';
    if (format === 'data-url') return 'badge--warning';
    if (type === 'boolean') return 'badge--success';
    return 'badge--primary';
  };
</script>
