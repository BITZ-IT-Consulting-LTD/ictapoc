<template>
  <main class="page profile-page">
    <header class="page__header">
      <div class="page__title-group">
        <h1 class="page__title">Authentic Citizen Profile</h1>
        <p class="page__subtitle">Manage your verified credentials and authoritative digital identity</p>
      </div>
      <div class="page__actions">
        <router-link to="/profile/consent" class="button button--secondary button--pill button--small">
          <i class="bi bi-shield-check u-mb-1"></i> Privacy & Consents
        </router-link>
      </div>
    </header>

    <!-- Document View Modal -->
    <BaseModal :show="!!selectedPreviewDoc" @close="selectedPreviewDoc = null" size="lg"
      :title="selectedPreviewDoc?.name">
      <template #header v-if="selectedPreviewDoc?.authoritative_id">
        <div class="modal__header-content">
          <h3 class="modal__title">{{ selectedPreviewDoc.name }}</h3>
          <p class="modal__subtitle u-font-mono u-text-primary u-font-bold">
            Auth ID: {{ selectedPreviewDoc.authoritative_id }}
          </p>
        </div>
      </template>

      <div class="u-bg-bg-page u-flex u-justify-center u-overflow-y-auto"
        style="margin: -var(--spacing-6); min-height: 60vh;">
        <!-- Simulated Certificate Layout -->
        <div v-if="selectedPreviewDoc?.type === 'AUTHORITATIVE_OUTPUT'" class="birth-certificate">
          <div class="birth-certificate__header">
            <div class="birth-certificate__coat-of-arms">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Coat_of_arms_of_Kenya_%28Official%29.svg/1200px-Coat_of_arms_of_Kenya_%28Official%29.svg.png"
                alt="Coat of Arms" style="height: 80px; opacity: 0.8;">
            </div>
            <h1 class="birth-certificate__title">{{ selectedPreviewDoc.issued_by || 'Civil Registration Services' }}
            </h1>
            <h2 class="birth-certificate__subtitle">Official Certificate of Registry Action</h2>
          </div>

          <div class="birth-certificate__content">
            <p class="birth-certificate__text">This is to officially certify that</p>
            <div class="birth-certificate__field birth-certificate__field--highlight">{{ selectedPreviewDoc.issued_to ||
              user.username }}</div>

            <p class="birth-certificate__text">Has successfully completed the statutory requirement for</p>
            <div class="birth-certificate__field birth-certificate__field--highlight">{{ selectedPreviewDoc.name }}
            </div>

            <div class="birth-certificate__details-grid" v-if="selectedPreviewDoc.metadata">
              <!-- Basic details if metadata exists -->
              <div v-for="(value, key) in selectedPreviewDoc.metadata" :key="key">
                <span class="birth-certificate__label">{{ key.replace(/_/g, ' ') }}</span>
                <span class="birth-certificate__value">{{ value }}</span>
              </div>
            </div>
          </div>

          <div class="birth-certificate__footer">
            <div class="birth-certificate__signature-block">
              <div class="birth-certificate__signature-image"
                style="font-family: 'Dancing Script', cursive; font-size: 24px; color: #000080;">
                Digitally Signed
              </div>
              <div class="birth-certificate__signature-line">Registrar of Persons</div>
            </div>

            <div style="text-align: right;">
              <div class="birth-certificate__auth-id"
                style="font-family: monospace; font-size: 0.8rem; margin-bottom: 5px;">
                REF: {{ selectedPreviewDoc.authoritative_id }}
              </div>
              <div class="birth-certificate__date" style="font-weight: bold;">
                ISSUED: {{ new Date(selectedPreviewDoc.issue_date || Date.now()).toLocaleDateString() }}
              </div>
            </div>
          </div>

          <div class="birth-certificate__security">
            <div class="birth-certificate__qr">
              <i class="bi bi-qr-code" style="font-size: 60px; color: #000;"></i>
            </div>
            <div class="birth-certificate__seal">
              Official<br>Seal
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
      <!-- Right: Wallet Sidebar -->
      <section class="space-y-8">
        <div class="card shadow-2xl overflow-hidden border-0" style="background: var(--grad-premium);">
          <header class="p-6 border-b flex justify-between items-start" style="border-color: rgba(255,255,255,0.1);">
            <div>
              <h2 class="text-xl font-black tracking-tight flex items-center gap-2" style="color: white !important;">
                <i class="bi bi-wallet2" style="color: var(--icta-red) !important;"></i> Digital Wallet
              </h2>
              <p class="text-xs mt-1 font-medium" style="color: #9ca3af !important;">Secure Credential Vault</p>
            </div>
            <button @click="showUpload = !showUpload"
              class="w-10 h-10 rounded-xl hover:bg-white/10 text-white transition-all flex items-center justify-center border"
              style="background-color: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1);"
              :aria-label="showUpload ? 'Close upload form' : 'Upload new document'" :aria-expanded="showUpload">
              <i class="bi" :class="showUpload ? 'bi-x-lg' : 'bi-plus-lg'"></i>
            </button>
          </header>

          <!-- Upload Form (Collapsible) -->
          <div v-show="showUpload" class="p-6 bg-black/20 border-b border-indigo-500/30 space-y-4 transition-all"
            role="region" aria-label="Upload Document Form">
            <div class="space-y-1">
              <label class="text-[10px] uppercase font-black tracking-widest text-indigo-300" for="docName">Credential
                Name</label>
              <input id="docName" type="text" v-model="newDocName" placeholder="e.g. Tax Clearance"
                class="w-full bg-indigo-950/50 border border-indigo-500/30 rounded-lg px-3 py-2 text-sm text-white placeholder-indigo-400/50 focus:outline-none focus:border-indigo-400 focus:ring-1 focus:ring-indigo-400 transition-colors">
            </div>

            <div class="space-y-1">
              <label class="text-[10px] uppercase font-black tracking-widest text-indigo-300" for="docFile">File
                Upload</label>
              <div class="relative group">
                <input id="docFile" type="file" @change="handleFileSelect"
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                  aria-label="Choose file to upload">
                <div
                  class="w-full bg-indigo-950/50 border border-dashed border-indigo-500/40 rounded-lg px-3 py-3 text-center group-hover:border-indigo-400 transition-colors">
                  <p v-if="newDocFile"
                    class="text-xs text-emerald-400 font-bold truncate flex items-center justify-center gap-2">
                    <i class="bi bi-file-earmark-check"></i> {{ newDocFile.name }}
                  </p>
                  <p v-else class="text-xs text-indigo-400">
                    <i class="bi bi-cloud-arrow-up mr-1.5"></i> Select PDF or Image
                  </p>
                </div>
              </div>
            </div>

            <button @click="uploadDocument" :disabled="!newDocFile || !newDocName"
              class="w-full py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-black uppercase tracking-wider shadow-lg shadow-emerald-900/20 transition-all flex items-center justify-center gap-2"
              aria-label="Save document to wallet">
              <i class="bi bi-lock-fill"></i> Secure to Vault
            </button>
          </div>

          <!-- Document List -->
          <div class="max-h-[600px] overflow-y-auto custom-scrollbar p-2" role="list" aria-label="Saved Documents List">
            <div v-if="savedDocs.length === 0" class="p-8 text-center text-indigo-300/50">
              <i class="bi bi-safe text-4xl mb-2 block opacity-50"></i>
              <p class="text-xs font-black uppercase tracking-widest leading-relaxed">Vault is empty</p>
            </div>

            <div v-for="(doc, index) in savedDocs" :key="index" class="mb-4 relative group" role="listitem">

              <!-- Premium Credential Card for Authoritative Documents -->
              <div
                v-if="doc.type === 'AUTHORITATIVE_OUTPUT' || doc.doctype === 'BIRTH_CERTIFICATE' || doc.doctype === 'NEMIS_CARD' || doc.name?.includes('NEMIS')"
                class="credential-card w-full mb-2 cursor-pointer relative" @click="viewDoc(doc)"
                style="height: auto; min-height: 160px; --card-width: 100%;">

                <div class="credential-card__header">
                  <div class="credential-card__logo-group">
                    <span class="credential-card__wallet-name">Digital Wallet</span>
                    <span class="credential-card__vault-badge">
                      <i class="bi bi-shield-lock-fill credential-card__icon"></i> Secure Vault
                    </span>
                  </div>
                  <div class="credential-card__qr">
                    <i class="bi bi-qr-code"></i>
                  </div>
                </div>

                <div class="credential-card__content">
                  <div class="credential-card__status">
                    <!-- Dynamic Icon based on Credential Type -->
                    <span class="credential-card__status-icon">
                      <i v-if="doc.name?.includes('NEMIS') || doc.doctype === 'NEMIS_CARD'"
                        class="bi bi-mortarboard-fill"></i>
                      <i v-else class="bi bi-check-circle-fill"></i>
                    </span>

                    <!-- Dynamic Text based on Credential Type -->
                    <span class="credential-card__status-text">
                      {{ (doc.name?.includes('NEMIS') || doc.doctype === 'NEMIS_CARD') ? 'Education' : 'Official' }}
                    </span>

                    <span class="credential-card__verified-badge">Verified</span>
                  </div>
                  <div class="credential-card__document">
                    <h2 class="credential-card__document-title">{{ doc.name }}</h2>
                  </div>
                </div>

                <div class="credential-card__footer">
                  <div class="credential-card__details">
                    <span class="credential-card__label">
                      {{ (doc.name?.includes('NEMIS') || doc.doctype === 'NEMIS_CARD') ? 'UPI / Admission No' :
                      'Authoritative ID' }}
                    </span>
                    <div class="credential-card__id">{{ doc.authoritative_id || 'PENDING-GEN' }}</div>
                  </div>
                  <div class="credential-card__details text-right">
                    <span class="credential-card__label">Issued Date</span>
                    <div class="credential-card__date">{{ new Date(doc.issue_date || Date.now()).toLocaleDateString() }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Standard List Item for Non-Authoritative / Uploaded Docs -->
              <div v-else
                class="p-3 rounded-xl hover:bg-white/5 transition-colors border border-transparent hover:border-indigo-500/30 flex items-start gap-4 cursor-pointer relative"
                @click="viewDoc(doc)">
                <!-- Icon/Thumbnail -->
                <div
                  class="w-10 h-10 rounded-lg flex-shrink-0 flex items-center justify-center text-lg shadow-inner bg-indigo-950/50 border border-indigo-500/20">
                  <i class="bi bi-file-earmark-text-fill" style="color: var(--icta-red);" aria-hidden="true"></i>
                </div>

                <!-- Content -->
                <div class="flex-1 min-w-0 pt-0.5">
                  <div class="flex items-center justify-between mb-0.5">
                    <h3 class="text-sm font-bold truncate pr-2" style="color: white !important;">{{ doc.name ||
                      doc.title }}
                    </h3>
                  </div>

                  <div class="flex items-center gap-2 text-[10px] font-mono" style="color: #e2e8f0 !important;">
                    <span class="truncate max-w-[120px]">
                      {{ (doc.size / 1024).toFixed(1) + ' KB' }}
                    </span>
                    <span class="w-0.5 h-0.5 rounded-full" style="background-color: var(--icta-red);"></span>
                    <span>{{ new Date(doc.issue_date || Date.now()).toLocaleDateString() }}</span>
                  </div>
                </div>

                <!-- Hover Indicator -->
                <div
                  class="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                  <i class="bi bi-chevron-right text-indigo-400 text-xs"></i>
                </div>
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
