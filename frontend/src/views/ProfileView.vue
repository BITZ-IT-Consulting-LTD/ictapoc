<template>
  <main class="page profile-page">
    <header class="page__header">
      <div class="page__title-group">
        <h1 class="page__title">Authentic Citizen Profile</h1>
        <p class="page__subtitle">Manage your verified credentials and authoritative digital identity</p>
      </div>
    </header>

    <!-- Document View Modal -->
    <BaseModal :show="!!selectedPreviewDoc" 
               @close="selectedPreviewDoc = null" 
               size="lg"
               :title="selectedPreviewDoc?.name">
      <template #header v-if="selectedPreviewDoc?.authoritative_id">
        <div class="modal__header-content">
          <h3 class="modal__title">{{ selectedPreviewDoc.name }}</h3>
          <p class="modal__subtitle u-font-mono u-text-primary u-font-bold">
            Auth ID: {{ selectedPreviewDoc.authoritative_id }}
          </p>
        </div>
      </template>

      <div class="u-bg-bg-page u-flex u-justify-center u-overflow-y-auto" style="margin: -var(--spacing-6); min-height: 60vh;">
        <!-- Simulated Certificate Layout -->
        <div v-if="selectedPreviewDoc?.type === 'AUTHORITATIVE_OUTPUT'"
          class="u-bg-white u-w-[595px] u-min-h-[842px] u-shadow-xl u-p-16 u-relative u-border-[12px] u-border-double u-border-primary-soft u-scale-90 sm:u-scale-100 u-origin-top u-my-8">
          <!-- Ornamental Border -->
          <div class="u-absolute u-inset-4 u-border-2 u-border-primary-soft u-pointer-events-none"></div>

          <div class="u-text-center u-mb-16">
            <div class="u-flex u-justify-center u-mb-6">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Coat_of_arms_of_Kenya_%28Official%29.svg/1200px-Coat_of_arms_of_Kenya_%28Official%29.svg.png"
                class="u-h-28 u-grayscale u-opacity-80" alt="GOK Coat of Arms">
            </div>
            <h1 class="u-text-2xl u-font-serif u-font-black u-text-main u-uppercase u-tracking-[0.2em] u-mb-2">{{
              selectedPreviewDoc.issued_by }}</h1>
            <h2 class="u-text-lg u-font-serif u-text-primary u-italic">Official Certificate of Registry Action</h2>
          </div>

          <div class="u-space-y-10 u-text-main">
            <div class="u-text-center">
              <p class="u-text-xs u-uppercase u-tracking-[0.3em] u-text-muted u-mb-4">This is to officially certify that
              </p>
              <p class="u-text-4xl u-font-serif u-font-black u-text-primary-darker">{{ selectedPreviewDoc.issued_to }}</p>
            </div>

            <div class="u-text-center u-border-y u-border-border-color u-py-10">
              <p class="u-text-sm u-font-bold u-text-muted u-mb-2 u-uppercase u-tracking-widest">Has successfully completed
                the statutory requirement for</p>
              <p class="u-text-2xl u-font-black u-text-main">{{ selectedPreviewDoc.name.split('-')[0] }}</p>
            </div>

            <div class="u-grid u-grid-cols-2 u-gap-12 u-text-sm u-border-b u-border-border-color u-pb-10">
              <div>
                <p class="u-text-[10px] u-text-muted u-uppercase u-font-black u-tracking-widest u-mb-1">Authoritative
                  Reference</p>
                <p class="u-font-mono u-font-black u-text-primary">{{ selectedPreviewDoc.authoritative_id }}</p>
              </div>
              <div>
                <p class="u-text-[10px] u-text-muted u-uppercase u-font-black u-tracking-widest u-mb-1">Cryptographic Issue
                  Date</p>
                <p class="u-font-black">{{ new Date(selectedPreviewDoc.issue_date).toLocaleDateString() }}</p>
              </div>
            </div>

            <!-- Signature Section -->
            <div class="u-pt-16 u-flex u-justify-between u-items-end">
              <div class="u-max-w-[240px]">
                <div class="u-h-[1px] u-w-full u-bg-border-color u-mb-4"></div>
                <p class="u-text-[10px] u-uppercase u-font-black u-text-muted u-tracking-widest u-mb-2">Electronic Registrar
                  Signature</p>
                <p class="u-text-[9px] font-mono u-text-primary-soft u-break-all u-leading-tight">{{
                  selectedPreviewDoc.metadata?.digital_signature }}</p>
              </div>
              <!-- Mock Barcode -->
              <div class="u-text-right">
                <div class="u-bg-main u-w-36 u-h-12 u-flex u-gap-1 u-p-1 u-px-2 u-items-center u-justify-center u-rounded-sm">
                  <div class="u-bg-white u-w-0.5 u-h-full" v-for="i in 18" :key="i"
                    :style="{ width: Math.random() * 4 + 'px' }"></div>
                </div>
                <p class="u-text-[8px] u-font-mono u-mt-2 u-tracking-[0.2em] u-text-muted u-uppercase">{{
                  selectedPreviewDoc.authoritative_id }}</p>
              </div>
            </div>
          </div>
        </div>
        <!-- Default File Viewer -->
        <iframe v-else-if="selectedPreviewDoc" :src="selectedPreviewDoc.content"
          class="u-w-full u-h-full u-min-h-[600px] u-bg-white u-rounded u-shadow-inner u-border-0"></iframe>
      </div>

      <template #footer>
        <button @click="selectedPreviewDoc = null" class="button button--secondary">Close Preview</button>
        <a v-if="selectedPreviewDoc?.content" :href="selectedPreviewDoc.content" :download="selectedPreviewDoc.name"
          class="button button--primary button--pill">
          <i class="bi bi-download"></i> Download Authoritative Copy
        </a>
      </template>
    </BaseModal>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left: Personal Info Form -->
      <section class="lg:col-span-2 space-y-8">
        <div class="card">
          <header class="card__header">
            <div class="card__title-group">
              <h2 class="card__title">Demographic Verification</h2>
              <p class="card__subtitle">Update your core demographic details for Faster registry processing</p>
            </div>
          </header>
          <div class="card__body">
            <form @submit.prevent="updateProfile" class="form">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="form__group">
                  <label class="form__label">Registry Username</label>
                  <input type="text" :value="user.username" disabled class="form__input bg-gray-50 cursor-not-allowed">
                </div>

                <div class="form__group">
                  <label class="form__label">Primary Email Address</label>
                  <input type="email" v-model="form.email" class="form__input" placeholder="Enter your email...">
                </div>

                <div class="form__group">
                  <label class="form__label">National Identity Number (ID No.)</label>
                  <input type="text" v-model="form.id_number" class="form__input" placeholder="8-digit ID number">
                </div>

                <div class="form__group">
                  <label class="form__label">International Passport Number</label>
                  <input type="text" v-model="form.passport_number" class="form__input" placeholder="Passport No.">
                </div>

                <div class="form__group">
                  <label class="form__label">Official Phone Number</label>
                  <input type="tel" v-model="form.phone_number" class="form__input" placeholder="+254...">
                </div>

                <div class="form__group md:col-span-2">
                  <label class="form__label">Authoritative Proof of Identity (Required for Verification)</label>
                  <div
                    class="border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center hover:border-primary transition-all cursor-pointer bg-gray-50 relative group">
                    <input type="file" @change="handleVerificationDoc"
                      class="absolute inset-0 opacity-0 cursor-pointer z-10" accept=".pdf,.png,.jpg">
                    <div class="flex flex-col items-center">
                      <i
                        class="bi bi-cloud-arrow-up text-3xl text-gray-300 group-hover:text-primary transition-colors mb-2"></i>
                      <p class="text-xs font-black text-gray-500 uppercase tracking-widest">Attach ID or Passport Scan
                      </p>
                      <p class="text-[10px] text-gray-400 mt-1">High-resolution PDF, PNG, or JPG required</p>
                    </div>
                  </div>
                  <div v-if="verificationDoc"
                    class="mt-4 p-4 bg-indigo-50 rounded-xl border border-indigo-100 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <i class="bi bi-file-earmark-check-fill text-indigo-500 text-xl"></i>
                      <div>
                        <div class="text-xs font-bold text-indigo-900">{{ verificationDoc.name }}</div>
                        <div class="text-[10px] text-indigo-400 uppercase font-mono">{{ (verificationDoc.size /
                          1024).toFixed(1) }} KB</div>
                      </div>
                    </div>
                    <button type="button" @click="verificationDoc = null" class="text-red-400 hover:text-red-600">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
              <div class="mt-8 flex justify-end">
                <button type="submit" class="button button--primary button--pill">
                  <i class="bi bi-shield-lock me-2"></i> Commit Profile Updates
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- Right: Wallet Sidebar -->
      <section class="space-y-8">
        <div class="card card--primary">
          <header class="card__header border-indigo-800">
            <div class="card__title-group">
              <h2 class="card__title text-white">Digital Wallet</h2>
              <p class="card__subtitle text-indigo-300">Authored Vault for Official Credentials</p>
            </div>
            <button @click="showUpload = !showUpload"
              class="button button--pill button--small bg-white/10 hover:bg-white/20 text-white border-0">
              <i class="bi bi-plus-lg"></i>
            </button>
          </header>

          <div v-if="showUpload" class="p-6 bg-indigo-800/50 border-b border-indigo-800 space-y-4">
            <div class="form__group">
              <label class="form__label text-white/70">Credential Alias</label>
              <input type="text" v-model="newDocName" placeholder="e.g. Birth Certificate"
                class="form__input bg-white/5 border-white/10 text-white placeholder:text-white/30">
            </div>

            <div class="form__group">
              <label class="form__label text-white/70">Credential File</label>
              <div class="relative overflow-hidden">
                <button class="button button--secondary button--small w-full">Select Authoritative File</button>
                <input type="file" @change="handleFileSelect" class="absolute inset-0 opacity-0 cursor-pointer">
              </div>
              <p v-if="newDocFile" class="text-[10px] text-indigo-200 mt-2 font-mono truncate">{{ newDocFile.name }}</p>
            </div>

            <button @click="uploadDocument" :disabled="!newDocFile || !newDocName"
              class="button button--primary button--pill w-full">
              <i class="bi bi-cloud-upload me-2"></i> Vault Document
            </button>
          </div>

          <div class="card__body p-0 max-h-[600px] overflow-y-auto">
            <div class="list list--compact">
              <div v-for="(doc, index) in savedDocs" :key="index"
                class="list__item hover:bg-indigo-800 transition-colors border-indigo-800/50">
                <div class="list__content flex items-center gap-4">
                  <div class="avatar-sm avatar-sm--square bg-indigo-700 text-white">
                    <i v-if="doc.type === 'AUTHORITATIVE_OUTPUT' || doc.doctype === 'BIRTH_CERTIFICATE'"
                      class="bi bi-patch-check-fill text-emerald-400"></i>
                    <i v-else class="bi bi-file-earmark-text"></i>
                  </div>
                  <div class="overflow-hidden">
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-black text-white truncate">{{ doc.name || doc.title }}</span>
                      <span v-if="doc.type === 'AUTHORITATIVE_OUTPUT'"
                        class="badge badge--success badge--small scale-75 origin-left">Verified</span>
                    </div>
                    <div class="text-[10px] text-indigo-400 font-mono truncate">
                      {{ doc.authoritative_id ? 'ID: ' + doc.authoritative_id : (doc.size / 1024).toFixed(1) + ' KB' }}
                    </div>
                  </div>
                </div>
                <div class="list__actions">
                  <button @click="viewDoc(doc)"
                    class="button button--ghost button--small text-white/70 hover:text-white">
                    <i class="bi bi-eye"></i>
                  </button>
                  <button v-if="doc.type !== 'AUTHORITATIVE_OUTPUT' && doc.doctype !== 'BIRTH_CERTIFICATE'"
                    @click="removeDoc(index)"
                    class="button button--ghost button--small text-red-400 hover:text-red-500">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
              <div v-if="savedDocs.length === 0" class="p-12 text-center text-indigo-400">
                <i class="bi bi-inboxes text-4xl mb-4 block opacity-30"></i>
                <p class="text-xs font-black uppercase tracking-widest leading-relaxed">Your authoritative digital vault
                  is empty</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useAuthStore } from '../store/auth';
  import { useCitizenStore } from '../store/citizen'; // Import Citizen Store
  import api from '../services/api';
  import { useRouter } from 'vue-router'; // Import Router
  import BaseModal from '../components/Common/BaseModal.vue';

  const authStore = useAuthStore();
  const citizenStore = useCitizenStore();
  const router = useRouter();
  const user = computed(() => authStore.user || {});

  const form = ref({
    email: '',
    id_number: '',
    passport_number: '',
    phone_number: ''
  });

  const savedDocs = ref([]);
  const verificationDoc = ref(null);
  const showUpload = ref(false);
  const newDocName = ref('');
  const newDocFile = ref(null);
  const selectedPreviewDoc = ref(null);

  const viewDoc = (doc) => {
    selectedPreviewDoc.value = doc;
  };

  onMounted(async () => {
    // Force refresh user data to catch newly issued certificates
    await authStore.fetchCurrentUser();

    if (authStore.user) {
      form.value.email = authStore.user.email || '';
      form.value.id_number = authStore.user.id_number || '';
      form.value.passport_number = authStore.user.passport_number || '';
      form.value.phone_number = authStore.user.phone_number || '';
      savedDocs.value = authStore.user.saved_documents || [];
    }
  });

  const handleVerificationDoc = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        verificationDoc.value = {
          name: file.name,
          size: file.size,
          type: file.type,
          content: e.target.result
        };
      };
      reader.readAsDataURL(file);
    }
  };

  const updateProfile = async () => {
    if (!verificationDoc.value) {
      alert("Please attach a supporting document (ID/Passport) to verify these changes.");
      return;
    }

    try {
      // Construct Payload for PROFILE_UPDATE service
      const payload = {
        ...form.value,
        supporting_document: verificationDoc.value
      };

      // Submit Request
      const response = await citizenStore.submitRequest('PROFILE_UPDATE', payload);

      alert(`Profile Update Request Submitted (ID: ${response.request_id}). It will be reviewed by an officer.`);
      router.push('/dashboard');
    } catch (e) {
      console.error(e);
      alert("Failed to submit profile update request.");
    }
  };

  // ... Document Wallet Logic (Separate immediate update) ...
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        newDocFile.value = {
          name: file.name, // Original filename
          size: file.size,
          type: file.type,
          content: e.target.result // Base64
        };
      };
      reader.readAsDataURL(file);
    }
  };

  const updateWallet = async () => {
    try {
      const payload = { saved_documents: savedDocs.value };
      // This 'patch' only updates the wallet, not sensitive info
      const response = await api.patch(`/users/${user.value.id}/`, payload);
      authStore.user = response.data; // Update local store
    } catch (e) {
      alert("Failed to update wallet.");
    }
  };

  const uploadDocument = async () => {
    if (newDocFile.value) {
      savedDocs.value.push({
        name: newDocName.value,
        ...newDocFile.value
      });
      await updateWallet();
      showUpload.value = false;
      newDocName.value = '';
      newDocFile.value = null;
    }
  };

  const removeDoc = async (index) => {
    if (confirm("Remove this document?")) {
      savedDocs.value.splice(index, 1);
      await updateWallet();
    }
  }
</script>
