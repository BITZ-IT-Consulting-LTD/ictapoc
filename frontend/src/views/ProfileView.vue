<template>
  <div class="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8 relative">
    <!-- Document View Modal -->
    <Teleport to="body">
      <div v-if="selectedPreviewDoc"
        class="fixed inset-0 z-[9999] overflow-y-auto flex items-center justify-center bg-gray-900/80 p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden">
          <div class="p-6 border-b flex justify-between items-center bg-slate-50">
            <div>
              <h3 class="text-xl font-bold text-slate-900">{{ selectedPreviewDoc.name }}</h3>
              <p class="text-xs text-slate-500 font-mono" v-if="selectedPreviewDoc.authoritative_id">Auth ID: {{
                selectedPreviewDoc.authoritative_id }}</p>
            </div>
            <button @click="selectedPreviewDoc = null" class="text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div class="flex-1 overflow-y-auto p-4 bg-slate-100 flex justify-center">
            <!-- Simulated Certificate Layout -->
            <div v-if="selectedPreviewDoc.type === 'AUTHORITATIVE_OUTPUT'"
              class="bg-white w-[595px] min-h-[842px] shadow-lg p-12 relative border-8 border-double border-indigo-100 scale-90 sm:scale-100 origin-top">
              <!-- Ornamental Border -->
              <div class="absolute inset-4 border-2 border-indigo-50 pointer-events-none"></div>

              <div class="text-center mb-12">
                <div class="flex justify-center mb-4">
                  <img
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Coat_of_arms_of_Kenya_%28Official%29.svg/1200px-Coat_of_arms_of_Kenya_%28Official%29.svg.png"
                    class="h-24 grayscale opacity-80" alt="GOK Coat of Arms">
                </div>
                <h1 class="text-2xl font-serif font-bold text-gray-900 uppercase tracking-widest">{{
                  selectedPreviewDoc.issued_by }}</h1>
                <h2 class="text-lg font-serif text-gray-600 italic">Certificate of Service Completion</h2>
              </div>

              <div class="space-y-8 text-slate-800">
                <div class="text-center">
                  <p class="text-sm uppercase tracking-widest text-slate-400 mb-2">This is to certify that</p>
                  <p class="text-3xl font-serif font-bold text-indigo-900">{{ selectedPreviewDoc.issued_to }}</p>
                </div>

                <div class="text-center border-y border-slate-100 py-8">
                  <p class="text-sm font-medium text-slate-500 mb-2">Has successfully completed the requirement for</p>
                  <p class="text-xl font-bold text-slate-900">{{ selectedPreviewDoc.name.split('-')[0] }}</p>
                </div>

                <div class="grid grid-cols-2 gap-8 text-sm">
                  <div>
                    <p class="text-[10px] text-slate-400 uppercase font-bold">Authoritative ID</p>
                    <p class="font-mono font-bold">{{ selectedPreviewDoc.authoritative_id }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] text-slate-400 uppercase font-bold">Issue Date</p>
                    <p class="font-bold">{{ new Date(selectedPreviewDoc.issue_date).toLocaleDateString() }}</p>
                  </div>
                </div>

                <!-- Signature Section -->
                <div class="pt-20 flex justify-between items-end">
                  <div>
                    <div class="h-[1px] w-48 bg-slate-300"></div>
                    <p class="text-[10px] mt-2 uppercase font-bold text-slate-400">Electronic Registrar Signature</p>
                    <p class="text-xs font-mono text-indigo-600">{{ selectedPreviewDoc.metadata?.digital_signature }}
                    </p>
                  </div>
                  <!-- Mock Barcode -->
                  <div class="text-right">
                    <div class="bg-gray-900 w-32 h-10 flex gap-1 p-1 px-2 items-center justify-center">
                      <div class="bg-white w-0.5 h-full" v-for="i in 15" :key="i"
                        :style="{ width: Math.random() * 3 + 'px' }"></div>
                    </div>
                    <p class="text-[9px] font-mono mt-1">{{ selectedPreviewDoc.authoritative_id }}</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- Default File Viewer -->
            <iframe v-else :src="selectedPreviewDoc.content"
              class="w-full h-full min-h-[600px] bg-white rounded shadow-inner"></iframe>
          </div>
          <div class="p-4 bg-white border-t flex justify-end gap-3">
            <button @click="selectedPreviewDoc = null"
              class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-medium transition-colors">Close</button>
            <a v-if="selectedPreviewDoc.content" :href="selectedPreviewDoc.content" :download="selectedPreviewDoc.name"
              class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium transition-colors">Download
              Copies</a>
          </div>
        </div>
      </div>
    </Teleport>
    <h1 class="text-3xl font-bold text-gray-900 mb-8">My Profile</h1>

    <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-8">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Personal Information</h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">Update your details for faster service application.</p>
      </div>
      <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
        <form @submit.prevent="updateProfile">
          <div class="grid grid-cols-6 gap-6">
            <div class="col-span-6 sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Username</label>
              <input type="text" :value="user.username" disabled
                class="mt-1 block w-full bg-gray-100 border border-gray-300 rounded-md shadow-sm p-2">
            </div>

            <div class="col-span-6 sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" v-model="form.email"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            </div>

            <div class="col-span-6 sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">National ID Number</label>
              <input type="text" v-model="form.id_number"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            </div>

            <div class="col-span-6 sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Passport Number</label>
              <input type="text" v-model="form.passport_number"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            </div>

            <div class="col-span-6 sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Phone Number</label>
              <input type="tel" v-model="form.phone_number"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            </div>

            <div class="col-span-6">
              <label class="block text-sm font-medium text-gray-700">Supporting Document for Verification
                (Required)</label>
              <input type="file" @change="handleVerificationDoc" class="mt-1 block w-full text-sm text-gray-500"
                accept=".pdf,.png,.jpg">
              <p class="text-xs text-gray-500 mt-1">Please attach ID or Passport scan to verify these changes.</p>
            </div>
          </div>
          <div class="mt-6 text-right">
            <button type="submit"
              class="bg-indigo-600 border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none">
              Submit Updates for Verification
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Document Wallet -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Document Wallet</h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">Securely store documents (ID Scans, Certificates) for reuse.
          </p>
        </div>
        <button @click="showUpload = !showUpload" class="text-sm text-indigo-600 hover:text-indigo-900">+ Add
          Document</button>
      </div>

      <div v-if="showUpload" class="border-t border-gray-200 px-4 py-5 sm:p-6 bg-gray-50">
        <div class="grid grid-cols-1 gap-4">
          <label class="block text-sm font-medium text-gray-700">Document Name</label>
          <input type="text" v-model="newDocName" placeholder="e.g. National ID Front"
            class="block w-full border border-gray-300 rounded-md p-2">

          <label class="block text-sm font-medium text-gray-700">File</label>
          <input type="file" @change="handleFileSelect"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">

          <button @click="uploadDocument" :disabled="!newDocFile || !newDocName"
            class="mt-2 w-full bg-green-600 text-white py-2 rounded disabled:bg-gray-300">
            Upload to Wallet
          </button>
        </div>
      </div>

      <div class="border-t border-gray-200">
        <ul class="divide-y divide-gray-200">
          <li v-for="(doc, index) in savedDocs" :key="index"
            class="px-4 py-4 sm:px-6 flex justify-between items-center group">
            <div class="flex items-center space-x-3 overflow-hidden">
              <div
                :class="[doc.type === 'AUTHORITATIVE_OUTPUT' || doc.doctype === 'BIRTH_CERTIFICATE' ? 'bg-indigo-100' : 'bg-gray-100', 'p-2 rounded-lg']">
                <svg v-if="doc.type === 'AUTHORITATIVE_OUTPUT' || doc.doctype === 'BIRTH_CERTIFICATE'"
                  class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                <svg v-else class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="flex flex-col truncate">
                <div class="flex items-center space-x-2">
                  <span class="text-sm font-bold text-gray-900 truncate">{{ doc.name || doc.title }}</span>
                  <span v-if="doc.type === 'AUTHORITATIVE_OUTPUT' || doc.doctype === 'BIRTH_CERTIFICATE'"
                    class="bg-blue-100 text-blue-700 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wide">Verified</span>
                </div>
                <div class="flex items-center gap-2" v-if="doc.authoritative_id">
                  <span class="text-xs text-gray-500 font-mono bg-gray-50 px-1 rounded border border-gray-200">ID: {{
                    doc.authoritative_id }}</span>
                </div>
                <span v-else class="text-xs text-gray-400">{{ (doc.size / 1024).toFixed(1) }} KB</span>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <button v-if="doc.content || doc.doc_id || doc.type === 'AUTHORITATIVE_OUTPUT'" @click="viewDoc(doc)"
                class="text-indigo-600 hover:text-indigo-900 text-sm font-semibold">View</button>
              <button v-if="doc.type !== 'AUTHORITATIVE_OUTPUT' && doc.doctype !== 'BIRTH_CERTIFICATE'"
                @click="removeDoc(index)"
                class="text-red-400 hover:text-red-700 text-sm opacity-0 group-hover:opacity-100 transition-opacity">Remove</button>
            </div>
          </li>
          <li v-if="savedDocs.length === 0" class="px-4 py-8 text-center text-gray-500 text-sm">
            Your digital wallet is empty. Once your requests are approved, your certificates will appear here.
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useAuthStore } from '../store/auth';
  import { useCitizenStore } from '../store/citizen'; // Import Citizen Store
  import api from '../services/api';
  import { useRouter } from 'vue-router'; // Import Router

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
