<template>
  <div class="o-page">
    <div v-if="service" class="u-animate-slide">
      <!-- Glass Header -->
      <div
        class="u-glass p-8 rounded-2xl mb-8 shadow-xl border-indigo-100 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="text-left">
          <h1 class="text-3xl font-bold text-slate-900 mb-2">{{ service.service_name }}</h1>
          <p class="text-slate-500 font-medium">Authoritative Government Service Application</p>
        </div>
        <div class="flex items-center gap-4 bg-white/50 p-2 rounded-xl border border-white">
          <div class="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center text-white shadow-lg">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Digital Trust</div>
            <div class="text-sm font-bold text-indigo-900">Verified identity required</div>
          </div>
        </div>
      </div>

      <!-- Wizard Progress -->
      <div v-if="formSteps.length > 1" class="c-wizard-progress px-10">
        <div v-for="(step, index) in formSteps" :key="index" class="c-wizard-step"
          :class="{ 'c-wizard-step--active': currentStepIndex === index, 'c-wizard-step--completed': currentStepIndex > index }">
          <div class="c-wizard-dot">
            <template v-if="currentStepIndex > index">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </template>
            <template v-else>{{ index + 1 }}</template>
          </div>
          <span class="c-wizard-label hidden md:block">{{ step.title }}</span>
        </div>
      </div>

      <!-- Form Body -->
      <div class="c-card u-glass border-none shadow-2xl relative overflow-visible">
        <div class="c-card__body p-10">
          <form @submit.prevent="handleSubmit" class="space-y-8">
            <div v-if="currentStep" class="u-animate-slide" :key="currentStepIndex">
              <div class="mb-8">
                <h2 class="text-2xl font-bold text-slate-900">{{ currentStep.title }}</h2>
                <p v-if="currentStep.description" class="text-slate-500 mt-1">{{ currentStep.description }}</p>
                <div class="h-1 w-20 bg-indigo-600 mt-4 rounded-full"></div>
              </div>

              <div class="space-y-6">
                <!-- Explicit Field Rendering for maximal reliability -->
                <div v-for="key in currentStep.fields" :key="key" class="c-field">
                  <label :for="key" class="c-field__label flex items-center justify-between">
                    <span>{{ schema.properties[key].title }}</span>
                    <span v-if="isRequired(key)"
                      class="text-[10px] text-rose-500 font-bold bg-rose-50 px-1.5 py-0.5 rounded">REQUIRED</span>
                  </label>

                  <!-- Select / Dropdown -->
                  <select v-if="schema.properties[key].enum" :id="key" v-model="formData[key]"
                    class="c-select w-full outline-none focus:ring-2 focus:ring-indigo-500/20"
                    :class="{ 'opacity-60 bg-slate-100 cursor-not-allowed': schema.properties[key].readOnly }"
                    :disabled="schema.properties[key].readOnly" :required="isRequired(key)">
                    <option value="" disabled>Select option...</option>
                    <option v-for="opt in schema.properties[key].enum" :key="opt" :value="opt">{{ opt }}</option>
                  </select>

                  <!-- File Upload -->
                  <label v-else-if="schema.properties[key].format === 'data-url'"
                    class="c-file-upload group h-32 flex flex-col justify-center items-center bg-indigo-50/20 border-indigo-200 border-2 border-dashed rounded-xl hover:bg-indigo-50 hover:border-indigo-400 transition-all cursor-pointer">
                    <input type="file" @change="handleFileUpload($event, key)" class="hidden">
                    <svg class="w-8 h-8 text-indigo-400 mb-2 group-hover:scale-110 transition-transform" fill="none"
                      stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <span class="text-indigo-600 font-bold text-sm">
                      {{ formData[key]?.name || 'Upload document' }}
                    </span>
                  </label>

                  <!-- Textarea -->
                  <textarea v-else-if="schema.properties[key].format === 'textarea'" :id="key" v-model="formData[key]"
                    class="c-editor h-32 w-full outline-none focus:ring-2 focus:ring-indigo-500/20"
                    :class="{ 'opacity-60 bg-slate-100 cursor-not-allowed': schema.properties[key].readOnly }"
                    :disabled="schema.properties[key].readOnly" :required="isRequired(key)"></textarea>

                  <!-- Radio Buttons -->
                  <div v-else-if="schema.properties[key].widget === 'radio'" class="flex gap-4 p-2">
                    <label v-for="opt in schema.properties[key].enum" :key="opt"
                      class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" :name="key" :value="opt" v-model="formData[key]"
                        class="w-4 h-4 accent-indigo-600">
                      <span class="text-sm text-slate-600">{{ opt }}</span>
                    </label>
                  </div>

                  <!-- Checkbox Group (Multi-select) -->
                  <div v-else-if="schema.properties[key].widget === 'checkbox-group'"
                    class="grid grid-cols-2 gap-3 p-2">
                    <label v-for="opt in (schema.properties[key].items?.enum || schema.properties[key].enum)" :key="opt"
                      class="flex items-center gap-2 cursor-pointer p-3 bg-slate-50 border border-slate-200 rounded-lg hover:bg-white transition-all">
                      <input type="checkbox" :value="opt" v-model="formData[key]"
                        class="w-4 h-4 accent-indigo-600 rounded">
                      <span class="text-xs font-medium text-slate-700">{{ opt }}</span>
                    </label>
                  </div>

                  <!-- Boolean Checkbox (Single) -->
                  <label v-else-if="schema.properties[key].type === 'boolean'"
                    class="flex items-center gap-3 p-4 bg-slate-50 border border-slate-200 rounded-xl cursor-pointer hover:bg-slate-100">
                    <input type="checkbox" class="w-5 h-5 accent-indigo-600" v-model="formData[key]"
                      :required="isRequired(key)">
                    <span class="text-sm font-medium text-slate-700">{{ schema.properties[key].title }}</span>
                  </label>

                  <!-- Standard Input (Date, Number, Text) with Lookup Support -->
                  <div class="relative flex gap-2">
                    <input :type="getFieldType(schema.properties[key])" :id="key" v-model="formData[key]"
                      class="c-input flex-1 outline-none focus:ring-2 focus:ring-indigo-500/20"
                      :class="{ 'opacity-60 bg-slate-100 cursor-not-allowed': schema.properties[key].readOnly }"
                      :required="isRequired(key)" :placeholder="schema.properties[key].title"
                      :disabled="schema.properties[key].readOnly" @input="clearVerification(key)">
                    <button v-if="schema.properties[key].lookup_service" type="button"
                      @click="performLookup(key, schema.properties[key])"
                      class="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-xl text-xs font-bold hover:bg-indigo-100 transition-colors whitespace-nowrap flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3"
                          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                      Fetch Record
                    </button>
                  </div>

                  <p v-if="schema.properties[key].description" class="text-xs text-slate-400 mt-1">
                    {{ schema.properties[key].description }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Navigation -->
            <div class="flex items-center justify-between pt-10 border-t border-slate-100 mt-10">
              <button type="button" v-if="currentStepIndex > 0" @click="prevStep"
                class="px-8 py-3 bg-slate-100 text-slate-600 rounded-xl font-bold hover:bg-slate-200 transition-all flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Back
              </button>
              <div v-else></div>

              <button v-if="currentStepIndex < formSteps.length - 1" type="button" @click="handleNext"
                class="px-10 py-3 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all flex items-center gap-2">
                Continue
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>

              <button v-else type="submit"
                class="px-12 py-4 bg-emerald-600 text-white rounded-xl font-bold hover:bg-emerald-700 shadow-lg shadow-emerald-200 transition-all flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Finalize & Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="flex flex-col items-center justify-center py-20">
      <div class="w-16 h-16 border-4 border-indigo-100 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
      <p class="text-slate-500 font-bold animate-pulse">Initializing Secure Portal...</p>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useServiceConfigStore } from '../store/serviceConfig';
  import { useCitizenStore } from '../store/citizen';
  import { useAuthStore } from '../store/auth';

  const route = useRoute();
  const router = useRouter();
  const serviceConfigStore = useServiceConfigStore();
  const citizenStore = useCitizenStore();
  const authStore = useAuthStore();

  const serviceCode = route.params.service_code;
  const service = ref(null);
  const formData = ref({});
  const currentStepIndex = ref(0);
  const verifiedFields = ref(new Set());

  onMounted(async () => {
    await serviceConfigStore.fetchServices();
    service.value = serviceConfigStore.services.find(s => s.service_code === serviceCode);

    if (service.value) {
      initializeForm();
    }
  });

  const schema = computed(() => service.value?.config?.rules?.schema);

  // Group fields into steps based on section_headers
  const formSteps = computed(() => {
    if (!schema.value) return [];

    const steps = [];
    let currentStepInfo = { title: 'Information', description: '', fields: [] };

    Object.keys(schema.value.properties).forEach(key => {
      const field = schema.value.properties[key];
      if (field.type === 'section_header') {
        if (currentStepInfo.fields.length > 0) {
          steps.push(currentStepInfo);
        }
        currentStepInfo = {
          title: field.title || 'Next Section',
          description: field.description || '',
          fields: []
        };
      } else {
        currentStepInfo.fields.push(key);
      }
    });

    if (currentStepInfo.fields.length > 0) {
      steps.push(currentStepInfo);
    }

    return steps;
  });

  const currentStep = computed(() => formSteps.value[currentStepIndex.value]);

  const initializeForm = () => {
    if (!schema.value) return;
    const user = authStore.user || {};

    Object.keys(schema.value.properties).forEach(key => {
      const field = schema.value.properties[key];
      if (field.type === 'section_header') return;

      if (field.widget === 'checkbox-group') {
        formData.value[key] = [];
      } else {
        // Intelligent Prefill (Core profile data)
        let prefill = '';
        if (key.includes('id_number') || key === 'national_id' || key === 'mother_id' || key === 'primary_owner_id') prefill = user.id_number || '';
        else if (key.includes('passport')) prefill = user.passport_number || '';
        else if (key.includes('phone')) prefill = user.phone_number || '';
        else if (key.includes('email')) prefill = user.email || '';
        else if (key.includes('owner_name') || key === 'full_name' || key === 'applicant_name') prefill = user.full_name || user.first_name + ' ' + user.last_name || '';
        else if (key.includes('owner_kra')) prefill = user.kra_pin || '';
        else if (key === 'gender') prefill = user.gender || '';
        else if (key === 'tax_payer_type') prefill = 'individual';

        // Wallet-based Prefill (Birth Certificate details)
        if (user.saved_documents?.length) {
          const birthCert = user.saved_documents.find(d => d.doctype === 'BIRTH_CERTIFICATE');
          if (birthCert && birthCert.metadata) {
            const meta = birthCert.metadata;
            // Map BEN and ID
            if (key === 'birth_entry_number' || key === 'ben') prefill = birthCert.authoritative_id || meta.ben || '';
            else if (key === 'national_id' || key === 'id_number') prefill = user.id_number || meta.id_number || '';

            // Map Parents
            else if (key === 'mother_name') prefill = meta.mother_name || '';
            else if (key === 'mother_id') prefill = meta.mother_id || '';
            else if (key === 'father_name') prefill = meta.father_name || '';
            else if (key === 'father_id') prefill = meta.father_id || '';

            // Map Personal details from birth record if missing in profile
            else if ((key === 'full_name' || key === 'applicant_name') && !prefill) prefill = meta.full_name || '';
            else if ((key === 'date_of_birth' || key === 'dob') && !prefill) prefill = meta.date_of_birth || '';
            else if (key === 'place_of_birth' || key === 'county_of_birth') prefill = meta.place_of_birth || meta.county || '';
            else if (key === 'gender' && !prefill) prefill = meta.gender || meta.sex || '';
          }

          const nemisCard = user.saved_documents.find(d => d.doctype === 'NEMIS_CARD');
          if (nemisCard && nemisCard.metadata) {
            if (key === 'nemis_upi' || key === 'upi') prefill = nemisCard.authoritative_id || nemisCard.metadata.upi || '';
          }
        }

        formData.value[key] = prefill;

        // Trust pre-filled data as verified
        if (prefill && (field.lookup_service || key.includes('mother_') || key.includes('father_'))) {
          verifiedFields.value.add(key);
        }
      }
    });
  };

  const isRequired = (key) => schema.value?.required?.includes(key);

  const getFieldType = (field) => {
    if (field.type === 'number') return 'number';
    if (field.format === 'date') return 'date';
    return 'text';
  };

  const clearVerification = (key) => {
    if (verifiedFields.value.has(key)) {
      verifiedFields.value.delete(key);
    }
  };

  const performLookup = async (key, field) => {
    const val = formData.value[key];
    if (!val) {
      alert(`Please enter a valid ${field.title} first.`);
      return;
    }

    try {
      const params = {
        [key]: val,
        action: field.lookup_action,
        is_guardian: formData.value.is_guardian_app || false
      };
      const result = await citizenStore.queryRegistry(field.lookup_service, params);

      if (result.status === 'SUCCESS' && result.data) {
        // Mark as Verified
        verifiedFields.value.add(key);

        // Map retrieved data to form fields
        // 1. Direct key mapping
        Object.keys(result.data).forEach(dataKey => {
          if (formData.value.hasOwnProperty(dataKey)) {
            formData.value[dataKey] = result.data[dataKey];
          }
        });

        // 2. Contextual Prefix Mapping (e.g. mother_id lookup should map 'full_name' to 'mother_name')
        const prefix = key.split('_')[0]; // 'mother', 'father', etc
        const contextualMappings = {
          'full_name': `${prefix}_name`,
          'gender': `${prefix}_gender`,
          'date_of_birth': `${prefix}_dob`
        };

        Object.keys(contextualMappings).forEach(sourceKey => {
          const targetKey = contextualMappings[sourceKey];
          if (result.data[sourceKey] && formData.value.hasOwnProperty(targetKey)) {
            formData.value[targetKey] = result.data[sourceKey];
          }
        });

        // Explicit Parent Mapping for Birth Certificate Lookups (BEN)
        // This ensures that when a BEN is fetched, the parent IDs are automatically populated
        if (key.includes('birth_entry') || key.includes('birth_cert') || key === 'ben') {
          // Expanded list to include Applicant's own details from the Birth Certificate
          const directMaps = [
            'mother_id', 'father_id', 'mother_name', 'father_name',
            'date_of_birth', 'full_name', 'gender'
          ];
          directMaps.forEach(dm => {
            if (result.data[dm]) {
              formData.value[dm] = result.data[dm];
              // Mark these as verified too since they came from a trusted source
              verifiedFields.value.add(dm);
            }
          });
        }

        alert(result.message || 'Record found and data pre-filled!');
      } else {
        verifiedFields.value.delete(key);
        alert(result.message || 'No matching record found in authoritative registry.');
      }
    } catch (error) {
      verifiedFields.value.delete(key);
      alert('Lookup failed. Please try again or fill the details manually.');
    }
  };

  const handleNext = () => {
    if (!currentStep.value) return;

    // Validation check
    for (const key of currentStep.value.fields) {
      if (isRequired(key)) {
        const val = formData.value[key];
        const fieldSchema = schema.value.properties[key];
        const fieldTitle = fieldSchema.title;

        // 1. Basic Empty Check
        if (val === undefined || val === null || val === '') {
          alert(`The field "${fieldTitle}" is required to proceed.`);
          return;
        }

        // 2. Lookup Verification Check
        if (fieldSchema.lookup_service && !verifiedFields.value.has(key)) {
          alert(`Please click 'Fetch Record' to verify your ${fieldTitle} before proceeding.`);
          return;
        }
      }
    }

    currentStepIndex.value++;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const prevStep = () => {
    currentStepIndex.value--;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleFileUpload = (event, key) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        formData.value[key] = {
          name: file.name,
          size: file.size,
          type: file.type,
          content: e.target.result
        };
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    try {
      await citizenStore.submitRequest(serviceCode, formData.value);
      router.push('/dashboard');
    } catch (error) {
      alert('Submission error. Please check your network and try again.');
    }
  };
</script>

<style scoped>

  /* Scoped overrides for premium feel */
  :deep(.c-input),
  :deep(.c-select),
  :deep(.c-editor) {
    background-color: #f8fafc;
    border-color: #e2e8f0;
    border-radius: 12px;
    font-weight: 500;
    padding: 12px 16px;
    transition: all 0.2s ease;
  }

  :deep(.c-input:focus),
  :deep(.c-select:focus),
  :deep(.c-editor:focus) {
    background-color: #fff;
    border-color: #6366f1;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
  }

  :deep(.c-field__label) {
    margin-bottom: 6px;
    text-transform: none;
    font-size: 13px;
    color: #64748b;
    letter-spacing: normal;
    font-weight: 600;
  }
</style>
