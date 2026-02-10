<template>
  <div class="mt-6 border-t pt-6">
    <h4 class="text-lg font-semibold mb-4">Form Schema Builder</h4>
    
    <!-- Field List -->
    <div class="space-y-2 mb-4">
      <div v-for="(field, key) in schema.properties" :key="key" class="flex items-center justify-between p-2 border rounded-lg">
        <div>
          <span class="font-medium">{{ field.title }}</span>
          <span class="text-sm text-gray-600 ml-2"> (Name: {{ key }}, Type: {{ field.type }})</span>
          <span v-if="isRequired(key)" class="text-sm text-red-500 ml-2">[Required]</span>
        </div>
        <div>
          <button type="button" @click.stop="editField(key)" class="text-indigo-600">Edit</button>
          <button type="button" @click.stop="removeField(key)" class="ml-4 text-red-600">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Field Form -->
    <div class="p-4 bg-gray-50 rounded-lg space-y-4">
      <h5 class="font-semibold mb-2">{{ isEditing ? 'Edit Field' : 'Add New Field' }}</h5>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium">Field Name (key)</label>
          <input type="text" v-model="fieldForm.name" class="mt-1 block w-full px-3 py-2 border rounded-md" :disabled="isEditing" required>
        </div>
        <div>
          <label class="block text-sm font-medium">Label (Title)</label>
          <input type="text" v-model="fieldForm.title" class="mt-1 block w-full px-3 py-2 border rounded-md" required>
        </div>
        <div>
          <label class="block text-sm font-medium">Type</label>
          <select v-model="fieldForm.type" class="mt-1 block w-full px-3 py-2 border rounded-md">
            <optgroup label="Basic">
                <option value="string">Text (Single Line)</option>
                <option value="textarea">Text (Long)</option>
                <option value="number">Number</option>
                <option value="email">Email</option>
                <option value="tel">Phone</option>
                <option value="currency">Currency (KES)</option>
                <option value="date">Date</option>
                <option value="boolean">Checkbox (Yes/No)</option>
            </optgroup>
            <optgroup label="Selection">
                <option value="select">Dropdown (Select)</option>
                <option value="radio">Radio Buttons</option>
                <option value="checkbox-group">Multi-Select (Checkboxes)</option>
            </optgroup>
            <optgroup label="Advanced">
                <option value="file">File Upload</option>
            </optgroup>
            <optgroup label="Layout">
                <option value="section_header">Section Header</option>
                <option value="info_text">Info Text</option>
            </optgroup>
          </select>
        </div>
        
        <!-- Options for Enums -->
        <div v-if="['select', 'radio', 'checkbox-group'].includes(fieldForm.type)">
           <label class="block text-sm font-medium">Options (Comma Separated)</label>
           <input type="text" v-model="fieldForm.enum" class="mt-1 block w-full px-3 py-2 border rounded-md" placeholder="e.g. Option 1, Option 2, Option 3">
        </div>

        <!-- Description -->
        <div class="col-span-2">
           <label class="block text-sm font-medium">Description / Help Text</label>
           <input type="text" v-model="fieldForm.description" class="mt-1 block w-full px-3 py-2 border rounded-md" placeholder="Helper text for the user">
        </div>
      </div>

      <div class="flex items-center justify-between pt-4">
          <div class="flex items-center">
            <input type="checkbox" v-model="fieldForm.required" id="required-field" class="h-4 w-4 bg-white border-gray-300 rounded">
            <label for="required-field" class="ml-2 block text-sm">Required Field?</label>
          </div>
          <div class="space-x-2">
            <button type="button" @click.stop="addField" class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">{{ isEditing ? 'Update Field' : 'Add Field' }}</button>
            <button v-if="isEditing" type="button" @click.stop="resetFieldForm" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300">Cancel</button>
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
</script>
