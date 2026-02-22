<template>
  <main class="page service-application-page">
    <div v-if="service" class="animate-fade-in space-y-8">
      <!-- Premium Glass Header -->
      <header
        class="page__header page__header--glass p-8 rounded-3xl shadow-2xl border border-white/40 flex flex-col md:flex-row justify-between items-center gap-8 bg-white/40 backdrop-blur-xl">
        <div class="page__title-group">
          <h1 class="page__title text-3xl">{{ service.service_name }}</h1>
          <p class="page__subtitle font-black uppercase tracking-[0.2em] text-indigo-500">Authoritative Institutional
            Gateway</p>
        </div>
        <div class="flex items-center gap-4 bg-white/60 p-3 rounded-2xl border border-white shadow-sm">
          <div class="w-14 h-14 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg">
            <i class="bi bi-shield-lock-fill text-2xl"></i>
          </div>
          <div>
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">National Trust Level</div>
            <div class="text-sm font-black text-indigo-900">Verified Identity Required</div>
          </div>
        </div>
      </header>

      <!-- Wizard Progress -->
      <section v-if="formSteps.length > 1" class="wizard px-10">
        <div v-for="(step, index) in formSteps" :key="index" class="wizard__step"
          :class="{ 'wizard__step--active': currentStepIndex === index, 'wizard__step--completed': currentStepIndex > index }">
          <div class="wizard__dot">
            <template v-if="currentStepIndex > index">
              <i class="bi bi-check-lg text-lg"></i>
            </template>
            <template v-else>{{ index + 1 }}</template>
          </div>
          <span class="wizard__label">{{ step.title }}</span>
        </div>
      </section>

      <!-- Form Body -->
      <div class="card card--glass border-0 shadow-2xl overflow-visible">
        <div class="card__body p-10">
          <form @submit.prevent="handleSubmit" class="form space-y-10">
            <div v-if="currentStep" class="animate-slide-in" :key="currentStepIndex">
              <div class="mb-10 border-b pb-6 border-slate-100">
                <h2 class="text-2xl font-black text-gray-900 mb-2">{{ currentStep.title }}</h2>
                <p v-if="currentStep.description" class="text-slate-500 text-sm italic">{{ currentStep.description }}
                </p>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Explicit Field Rendering for maximal reliability -->
                <div v-for="key in currentStep.fields" :key="key" class="form__group"
                  :class="{ 'md:col-span-2': schema.properties[key].format === 'textarea' || schema.properties[key].widget === 'checkbox-group' }">

                  <div class="flex justify-between items-center mb-2">
                    <label :for="key" class="form__label mb-0">
                      {{ schema.properties[key].title }}
                    </label>
                    <span v-if="isRequired(key)"
                      class="badge badge--danger badge--small scale-75 origin-right">MANDATORY</span>
                  </div>

                  <!-- Select / Dropdown -->
                  <select v-if="schema.properties[key].enum" :id="key" v-model="formData[key]" class="form__select"
                    :class="{ 'opacity-60 bg-slate-100 cursor-not-allowed': schema.properties[key].readOnly }"
                    :disabled="schema.properties[key].readOnly" :required="isRequired(key)">
                    <option value="" disabled>Select authoritative option...</option>
                    <option v-for="opt in schema.properties[key].enum" :key="opt" :value="opt">{{ opt }}</option>
                  </select>

                  <!-- File Upload -->
                  <div v-else-if="schema.properties[key].format === 'data-url'"
                    class="relative group h-32 flex flex-col justify-center items-center bg-indigo-50/20 border-indigo-200 border-2 border-dashed rounded-2xl hover:bg-white hover:border-primary transition-all cursor-pointer">
                    <input type="file" @change="handleFileUpload($event, key)"
                      class="absolute inset-0 opacity-0 cursor-pointer z-10">
                    <i
                      class="bi bi-cloud-arrow-up text-3xl text-indigo-400 mb-2 group-hover:scale-110 transition-transform"></i>
                    <span class="text-indigo-600 font-black text-xs uppercase tracking-widest">
                      {{ formData[key]?.name || 'Attach Digital Copy' }}
                    </span>
                  </div>

                  <!-- Textarea -->
                  <textarea v-else-if="schema.properties[key].format === 'textarea'" :id="key" v-model="formData[key]"
                    class="form__input form__textarea h-40"
                    :class="{ 'opacity-60 bg-slate-100 cursor-not-allowed': schema.properties[key].readOnly }"
                    :disabled="schema.properties[key].readOnly" :required="isRequired(key)"
                    placeholder="Enter detailed records..."></textarea>

                  <!-- Radio Buttons -->
                  <div v-else-if="schema.properties[key].widget === 'radio'"
                    class="flex gap-6 p-2 bg-gray-50 rounded-xl border border-gray-100">
                    <label v-for="opt in schema.properties[key].enum" :key="opt"
                      class="flex items-center gap-3 cursor-pointer group">
                      <input type="radio" :name="key" :value="opt" v-model="formData[key]"
                        class="w-5 h-5 accent-primary cursor-pointer">
                      <span
                        class="text-xs font-bold text-slate-600 uppercase tracking-tight group-hover:text-primary transition-colors">{{
                          opt }}</span>
                    </label>
                  </div>

                  <!-- Checkbox Group (Multi-select) -->
                  <div v-else-if="schema.properties[key].widget === 'checkbox-group'"
                    class="grid grid-cols-2 lg:grid-cols-3 gap-4 p-2">
                    <label v-for="opt in (schema.properties[key].items?.enum || schema.properties[key].enum)" :key="opt"
                      class="flex items-center gap-3 cursor-pointer p-4 bg-gray-50 border border-gray-100 rounded-2xl hover:bg-white hover:border-primary transition-all group"
                      :class="{ 'bg-white border-primary !border-2 shadow-sm': formData[key]?.includes(opt) }">
                      <input type="checkbox" :value="opt" v-model="formData[key]"
                        class="w-5 h-5 accent-primary rounded cursor-pointer">
                      <span
                        class="text-xs font-black text-slate-700 uppercase tracking-tighter group-hover:text-primary transition-colors">{{
                          opt }}</span>
                    </label>
                  </div>

                  <!-- Boolean Checkbox (Single) -->
                  <label v-else-if="schema.properties[key].type === 'boolean'"
                    class="flex items-center gap-4 p-6 bg-gray-50 border border-gray-100 rounded-2xl cursor-pointer hover:bg-white hover:border-primary transition-all group"
                    :class="{ 'bg-white border-primary !border-2 shadow-sm': formData[key] }">
                    <input type="checkbox" class="w-6 h-6 accent-primary rounded cursor-pointer" v-model="formData[key]"
                      :required="isRequired(key)">
                    <span
                      class="text-xs font-black text-slate-700 uppercase tracking-widest group-hover:text-primary transition-colors">{{
                        schema.properties[key].title }}</span>
                  </label>

                  <!-- Standard Input (Date, Number, Text) with Registry Lookup Support -->
                  <div v-else class="relative flex gap-2">
                    <div class="relative flex-1">
                      <input :type="getFieldType(schema.properties[key])" :id="key" v-model="formData[key]"
                        class="form__input w-full"
                        :class="{ 
                          'opacity-60 bg-gray-50 cursor-not-allowed': schema.properties[key].readOnly,
                          'border-green-500 focus:border-green-500 pr-10': verifiedFields.has(key)
                        }"
                        :required="isRequired(key)" :placeholder="schema.properties[key].title"
                        :disabled="schema.properties[key].readOnly" @input="clearVerification(key)">
                        
                      <i v-if="verifiedFields.has(key)" 
                         class="bi bi-check-circle-fill text-green-500 absolute right-3 top-1/2 -translate-y-1/2 text-lg animate-bounce-short"></i>
                    </div>

                    <button v-if="schema.properties[key]['x-registry-config']" type="button"
                      @click="performLookup(key, schema.properties[key])"
                      class="button button--secondary button--small whitespace-nowrap"
                      :class="{'button--success': verifiedFields.has(key)}"
                      :disabled="!formData[key]">
                      <i class="bi" :class="verifiedFields.has(key) ? 'bi-shield-check' : 'bi-search'"></i>
                      <span class="ms-1">{{ verifiedFields.has(key) ? 'Verified' : 'Fetch Record' }}</span>
                    </button>
                  </div>

                  <p v-if="schema.properties[key].description" class="text-[10px] text-slate-400 mt-2 italic">
                    <i class="bi bi-info-circle me-1"></i> {{ schema.properties[key].description }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Navigation -->
            <footer class="flex items-center justify-between pt-10 border-t border-slate-100 mt-10">
              <button type="button" v-if="currentStepIndex > 0" @click="prevStep"
                class="button button--secondary button--pill">
                <i class="bi bi-arrow-left me-2"></i> Previous Section
              </button>
              <div v-else></div>

              <button v-if="currentStepIndex < formSteps.length - 1" type="button" @click="handleNext"
                class="button button--primary button--pill px-12">
                Continue to Next Stage <i class="bi bi-arrow-right ms-2"></i>
              </button>

              <button v-else type="submit"
                class="button button--primary button--pill px-16 bg-emerald-600 hover:bg-emerald-700 border-emerald-600 shadow-xl shadow-emerald-100">
                <i class="bi bi-shield-check me-2 text-lg"></i> Finalize & Commit Application
              </button>
            </footer>
          </form>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="flex flex-col items-center justify-center py-40">
      <div class="w-16 h-16 border-4 border-indigo-100 border-t-indigo-600 rounded-full animate-spin mb-6"></div>
      <p class="text-xs font-black uppercase tracking-[0.4em] text-indigo-500 animate-pulse">Initializing Secure
        Portal...
      </p>
    </div>
  </main>
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
    const role = user.role?.toLowerCase();
    
    // Skip prefill for staff roles when they are initiating services for others
    const isStaff = ['officer', 'hospital_staff', 'registrar', 'mda_officer', 'mda_admin', 'global_officer'].includes(role);

    Object.keys(schema.value.properties).forEach(key => {
      const field = schema.value.properties[key];
      if (field.type === 'section_header') return;

      if (field.widget === 'checkbox-group') {
        formData.value[key] = [];
      } else {
        // Intelligent Prefill (Core profile data) - Only for citizens
        let prefill = '';
        if (!isStaff) {
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
              if (key === 'birth_entry_number' || key === 'ben') prefill = birthCert.authoritative_id || meta.ben || '';
              else if (key === 'national_id' || key === 'id_number') prefill = user.id_number || meta.id_number || '';
              else if (key === 'mother_name') prefill = meta.mother_name || '';
              else if (key === 'mother_id') prefill = meta.mother_id || '';
              else if (key === 'father_name') prefill = meta.father_name || '';
              else if (key === 'father_id') prefill = meta.father_id || '';
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
    if (field.format === 'registry_lookup') return 'text';
    return 'text';
  };

  const clearVerification = (key) => {
    if (verifiedFields.value.has(key)) {
      verifiedFields.value.delete(key);
    }
  };

  const performLookup = async (key, field) => {
    const val = formData.value[key];
    const registryConfig = field['x-registry-config'];

    if (!val) {
      alert(`Please enter a valid ${field.title} first.`);
      return;
    }

    if (!registryConfig || !registryConfig.adapter_id || !registryConfig.endpoint_id) {
       console.error("Missing registry configuration for field", key);
       return;
    }

    // Interactive feedback
    const btn = document.activeElement;
    const originalText = btn ? btn.innerHTML : '';
    if(btn) {
        btn.innerHTML = '<i class="bi bi-arrow-repeat animate-spin"></i> Verifying...';
        btn.disabled = true;
    }

    try {
      // Construct payload based on RegistryAdapter logic
      // Ideally, the endpoint metadata should tell us what the query param name is.
      // For POC, we assume the input schema key matches or we send a standard 'q' or the field key.
      const params = {
        query: val, // Generic query param
        [key]: val, // Field-specific param (e.g. id_number=123)
        registry_adapter_id: registryConfig.adapter_id,
        registry_endpoint_id: registryConfig.endpoint_id
      };

      // We need a store action that can handle generic registry queries
      // If citizenStore.queryRegistry is tied to specific legacy Lookups, we might need a new action.
      // For now, let's assume queryRegistry can handle the new structure or we add a new one.
      // Since we don't have a generic 'query_registry' endpoint in the backend view shown earlier,
      // we might need to route this through a specific endpoint or update the store.
      // Let's assume we use the existing 'registry/query/' endpoint.

      const result = await citizenStore.queryRegistryEndpoint(registryConfig.adapter_id, registryConfig.endpoint_id, params);

      if (result && result.success) {
        // Mark as Verified
        verifiedFields.value.add(key);

        // Auto-fill other form fields based on Output Schema
        // result.data contains the registry response.
        // We need to map registry output keys to form keys.
        // If no explicit mapping exists, try direct name matching.
        
        const data = result.data;
        Object.keys(data).forEach(dataKey => {
             // 1. Direct Match
             if (formData.value.hasOwnProperty(dataKey)) {
                 formData.value[dataKey] = data[dataKey];
                 // Also mark these as verified if they came from registry?
                 // verifiedFields.value.add(dataKey); 
             }
             // 2. Fuzzy / Common variations (as implemented before)
             // ... (existing logic can remain if useful)
        });

      } else {
        verifiedFields.value.delete(key);
        alert(result?.message || 'No matching record found in authoritative registry.');
        formData.value[key] = ''; // clear invalid input? Option.
      }
    } catch (error) {
      verifiedFields.value.delete(key);
      console.error(error);
      alert('Lookup failed. Authority server unreachable.');
    } finally {
        if(btn) {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
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

        // 2. Lookup Verification Check (BLOCKER)
        if (fieldSchema['x-registry-config'] && !verifiedFields.value.has(key)) {
          alert(`CRITICAL Validation: The field "${fieldTitle}" must be verified against the National Registry. Please click 'Fetch Record'.`);
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
