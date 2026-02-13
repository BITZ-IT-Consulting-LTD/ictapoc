<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-gray-100">
      <div>
        <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
          <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
          Registry & Correspondence
        </h2>
        <p class="text-sm text-gray-500">Authoritative Government Internal Service (G2G)</p>
      </div>
      <div class="flex gap-2">
        <button @click="showComposeModal = true" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium flex items-center gap-2 transition-colors shadow-sm">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
          Initiate Correspondence
        </button>
      </div>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
       <div class="bg-blue-50 border border-blue-100 p-4 rounded-xl">
          <p class="text-blue-600 font-medium text-[10px] uppercase">Registry Inbox</p>
          <p class="text-2xl font-bold text-gray-800">{{ inboundMemos.length }}</p>
       </div>
       <div class="bg-orange-50 border border-orange-100 p-4 rounded-xl" v-if="isRegistrar">
          <p class="text-orange-600 font-medium text-[10px] uppercase">Pending Registration</p>
          <p class="text-2xl font-bold text-gray-800">{{ pendingRegistration.length }}</p>
       </div>
       <div class="bg-indigo-50 border border-indigo-100 p-4 rounded-xl">
          <p class="text-indigo-600 font-medium text-[10px] uppercase">Action Queue</p>
          <p class="text-2xl font-bold text-gray-800">{{ actionQueue.length }}</p>
       </div>
       <div class="bg-gray-50 border border-gray-200 p-4 rounded-xl">
          <p class="text-gray-600 font-medium text-[10px] uppercase">Signed & Issued</p>
          <p class="text-2xl font-bold text-gray-800">{{ signedMemosCount }}</p>
       </div>
    </div>

    <!-- Tabs -->
    <div class="flex space-x-1 bg-gray-100 p-1 rounded-lg w-fit border border-gray-200">
      <button @click="activeTab = 'inbox'" :class="[activeTab === 'inbox' ? 'bg-white shadow text-indigo-600' : 'text-gray-500 hover:text-gray-700', 'px-4 py-2 rounded-md text-sm font-medium transition-all']">
        Inbox
      </button>
      <button @click="activeTab = 'sent'" :class="[activeTab === 'sent' ? 'bg-white shadow text-indigo-600' : 'text-gray-500 hover:text-gray-700', 'px-4 py-2 rounded-md text-sm font-medium transition-all']">
        Sent
      </button>
      <button v-if="isRegistrar" @click="activeTab = 'registry'" :class="[activeTab === 'registry' ? 'bg-white shadow text-orange-600' : 'text-gray-500 hover:text-gray-700', 'px-4 py-2 rounded-md text-sm font-medium transition-all']">
        Registry Queue
      </button>
      <button @click="activeTab = 'files'" :class="[activeTab === 'files' ? 'bg-white shadow text-gray-800' : 'text-gray-500 hover:text-gray-700', 'px-4 py-2 rounded-md text-sm font-medium transition-all']">
        File Registry
      </button>
    </div>

    <!-- Main List Container -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden min-h-[400px]">
      <div v-if="loading" class="p-12 text-center text-gray-500">
         <div class="animate-spin h-8 w-8 text-indigo-600 mx-auto mb-4 border-4 border-indigo-200 border-t-indigo-600 rounded-full"></div>
         Syncing with GoK Registry...
      </div>
      
      <!-- Files Tab -->
      <div v-else-if="activeTab === 'files'" class="p-0">
          <div v-if="govFiles.length === 0" class="p-12 text-center text-gray-400 italic">No files found in registry.</div>
          <ul class="divide-y divide-gray-100">
             <li v-for="file in govFiles" :key="file.id" class="p-4 hover:bg-gray-50 flex justify-between items-center cursor-pointer">
                <div class="flex items-center gap-3">
                   <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500">
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>
                   </div>
                   <div>
                      <p class="font-bold text-gray-800">{{ file.file_number }}</p>
                      <p class="text-xs text-gray-500">{{ file.subject }}</p>
                   </div>
                </div>
                <span class="px-2 py-1 bg-green-50 text-green-700 text-[10px] font-bold rounded border border-green-200 uppercase">{{ file.status }}</span>
             </li>
          </ul>
      </div>

      <!-- Correspondence/Memos List -->
      <div v-else-if="activeList.length === 0" class="p-12 text-center text-gray-400">
        <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
        No official correspondence found in {{ activeTab }}.
      </div>

      <ul v-else class="divide-y divide-gray-100">
        <li v-for="memo in activeList" :key="memo.id" 
            @click="viewMemo(memo)"
            class="hover:bg-indigo-50/40 cursor-pointer transition-colors p-4 flex items-start gap-4"
            :class="{'bg-blue-50/20': memo.status === 'registered' && !memo.is_read}"
        >
           <!-- Status Indicator -->
           <div class="w-1 self-stretch rounded-full" :class="statusBg(memo.status)"></div>

           <div class="flex-1 min-w-0">
             <div class="flex justify-between mb-1">
               <div class="flex items-center gap-2">
                 <span class="text-[10px] font-bold px-1.5 py-0.5 rounded border" :class="memoTypeColor(memo.memo_type)">{{ memo.memo_type.toUpperCase() }}</span>
                 <p class="text-sm font-bold text-gray-900 truncate">{{ memo.subject }}</p>
               </div>
               <span class="text-[10px] font-mono text-gray-400">{{ formatDate(memo.created_at) }}</span>
             </div>
             
             <div class="flex justify-between items-end">
                <div class="text-[11px] text-gray-500">
                  <span v-if="activeTab === 'inbox'">From: <span class="font-medium text-gray-700">{{ memo.sender_mda?.name }}</span></span>
                  <span v-else>To: <span class="font-medium text-gray-700">{{ memo.recipient_mda_details?.name }}</span></span>
                  <span class="mx-2 text-gray-300">|</span>
                  <span class="font-mono text-indigo-600 font-bold" v-if="memo.official_ref">{{ memo.official_ref }}</span>
                  <span class="text-gray-400 italic" v-else>UNREGISTERED</span>
                </div>
                
                <div class="flex gap-2">
                   <span v-if="memo.digitally_signed" class="flex items-center text-[10px] text-green-600 font-bold bg-green-50 px-1.5 py-0.5 rounded border border-green-200">
                      <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                      SIGNED
                   </span>
                   <span v-if="memo.priority === 'urgent'" class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-700 border border-red-200 uppercase">Urgent</span>
                </div>
             </div>
           </div>
        </li>
      </ul>
    </div>

    <!-- Initiation Modal -->
    <Teleport to="body">
       <div v-if="showComposeModal" class="fixed inset-0 z-[9999] bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden border border-gray-200">
             <div class="bg-indigo-900 px-6 py-4 border-b border-indigo-800 flex justify-between items-center text-white">
                <div>
                   <h3 class="font-bold">Initiate Official Correspondence</h3>
                   <p class="text-[10px] text-indigo-300">Governed by GoK Registry Rules</p>
                </div>
                <button @click="showComposeModal = false" class="text-indigo-300 hover:text-white">
                   <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
             </div>
             
             <form @submit.prevent="sendMemo" class="p-6 space-y-4">
                <div class="grid grid-cols-2 gap-4">
                   <div>
                      <label class="block text-[11px] font-bold text-gray-500 uppercase mb-1">Correspondence Mode</label>
                      <div class="flex bg-gray-100 p-1 rounded-lg">
                         <button type="button" @click="newMemo.is_letter = false" :class="[!newMemo.is_letter ? 'bg-white shadow text-indigo-700' : 'text-gray-500', 'flex-1 py-1.5 text-xs font-bold rounded-md transition-all']">Internal Memo</button>
                         <button type="button" @click="newMemo.is_letter = true" :class="[newMemo.is_letter ? 'bg-white shadow text-indigo-700' : 'text-gray-500', 'flex-1 py-1.5 text-xs font-bold rounded-md transition-all']">Official Letter</button>
                      </div>
                   </div>
                    <div>
                      <label class="block text-[11px] font-bold text-gray-500 uppercase mb-1">Type/Purpose</label>
                      <select v-model="newMemo.memo_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm">
                         <option value="policy">Policy Memo</option>
                         <option value="operational">Operational Request</option>
                         <option value="instruction">Instruction</option>
                         <option value="concurrence">Concurrence</option>
                         <option value="escalation">Escalation</option>
                         <option value="information">Information</option>
                         <option v-if="newMemo.is_letter" value="external">External Dispatch</option>
                      </select>
                   </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                   <div>
                      <label class="block text-[11px] font-bold text-gray-500 uppercase mb-1">Recipient MDA</label>
                      <select v-model="newMemo.recipient_mda" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm">
                         <option value="" disabled>Select Department...</option>
                         <option v-for="mda in mdas" :key="mda.id" :value="mda.id">{{ mda.name }}</option>
                      </select>
                   </div>
                   <div>
                       <label class="block text-[11px] font-bold text-gray-500 uppercase mb-1">Priority</label>
                       <select v-model="newMemo.priority" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm">
                          <option value="normal">Normal</option>
                          <option value="high">High</option>
                          <option value="urgent">Urgent</option>
                       </select>
                   </div>
                </div>
                
                <div>
                   <label class="block text-[11px] font-bold text-gray-500 uppercase mb-1">Subject</label>
                   <input v-model="newMemo.subject" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm" placeholder="Official Subject Line">
                </div>
                
                <div>
                   <label class="block text-[11px] font-bold text-gray-500 uppercase mb-1">Content</label>
                   <textarea v-model="newMemo.content" rows="6" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm resize-none" placeholder="Draft your memo content here..."></textarea>
                </div>
                
                <div class="pt-2 flex justify-end gap-3">
                   <button type="button" @click="showComposeModal = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-600 font-medium hover:bg-gray-50 text-sm">Save Draft</button>
                   <button type="submit" class="px-6 py-2 bg-indigo-900 text-white rounded-lg font-bold hover:bg-black shadow-lg transition-all text-sm flex items-center gap-2">
                     <span>Initiate Approval</span>
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                   </button>
                </div>
             </form>
          </div>
       </div>
    </Teleport>

    <!-- Detailed Reader Modal -->
    <Teleport to="body">
       <div v-if="selectedMemo" class="fixed inset-0 z-[9999] bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl overflow-hidden border border-gray-200 flex flex-col max-h-[90vh]">
             <!-- Header -->
             <div class="p-6 border-b border-gray-100 flex justify-between items-start">
                 <div>
                    <h2 class="text-xl font-bold text-gray-900 uppercase tracking-tight">{{ selectedMemo.subject }}</h2>
                    <div class="flex items-center gap-2 mt-1">
                       <span class="text-xs font-mono text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100 font-bold" v-if="selectedMemo.official_ref">REF: {{ selectedMemo.official_ref }}</span>
                       <span class="text-xs bg-red-50 text-red-600 px-2 py-0.5 rounded font-bold" v-else>UNREGISTERED DRAFT</span>
                       <span class="text-xs text-gray-400">&bull; {{ formatDate(selectedMemo.created_at) }}</span>
                    </div>
                 </div>
                 <button @click="selectedMemo = null" class="text-gray-400 hover:text-gray-600">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                 </button>
             </div>

             <div class="flex-1 overflow-auto flex">
                <!-- Main Content -->
                <div class="flex-1 p-8 bg-white overflow-auto border-r border-gray-100">
                   <div class="mb-8 border-b-2 border-double border-gray-200 pb-4">
                      <div class="flex justify-between text-xs font-medium text-gray-500 uppercase tracking-widest mb-4">
                         <span>GoK FORM 004</span>
                         <span>CONFIDENTIAL</span>
                      </div>
                      <div class="space-y-2 text-sm">
                         <p><span class="inline-block w-24 text-gray-400 font-bold uppercase text-[10px]">From:</span> <span class="font-bold">{{ selectedMemo.sender_mda?.name }}</span></p>
                         <p><span class="inline-block w-24 text-gray-400 font-bold uppercase text-[10px]">To:</span> <span class="font-bold">{{ selectedMemo.recipient_mda_details?.name }}</span></p>
                         <p><span class="inline-block w-24 text-gray-400 font-bold uppercase text-[10px]">Subject:</span> <span class="font-bold">{{ selectedMemo.subject }}</span></p>
                         <p><span class="inline-block w-24 text-gray-400 font-bold uppercase text-[10px]">Type:</span> <span class="font-bold text-indigo-700">{{ selectedMemo.memo_type?.toUpperCase() }}</span></p>
                      </div>
                   </div>

                   <div class="prose prose-sm max-w-none text-gray-800 leading-relaxed whitespace-pre-wrap font-serif text-lg">
                      {{ selectedMemo.content }}
                   </div>

                   <div class="mt-12 flex justify-end" v-if="selectedMemo.digitally_signed">
                      <div class="text-right border-t border-gray-200 pt-4 w-64">
                         <div class="mb-2">
                             <svg class="w-12 h-12 text-green-600 ml-auto opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                         </div>
                         <p class="font-bold text-gray-900 border-b border-gray-400 pb-1">DIGITALLY SIGNED</p>
                         <p class="text-[10px] text-gray-500 mt-1">Officer: {{ selectedMemo.signed_by?.username }}</p>
                         <p class="text-[10px] text-gray-400">{{ formatDate(selectedMemo.updated_at) }}</p>
                      </div>
                   </div>
                </div>

                <!-- Action Sidebar -->
                <div class="w-72 bg-gray-50 p-6 space-y-6">
                  <div class="space-y-4">
                     <div v-if="selectedMemo.status === 'draft' && selectedMemo.sender_mda.id === user?.mda" class="p-4 bg-orange-50 border border-orange-100 rounded-xl">
                        <label class="block text-[10px] font-bold text-orange-600 uppercase mb-2">Internal Submission</label>
                        <p class="text-[11px] text-orange-700 mb-3">Draft complete. Send to Director for internal verification.</p>
                        <button @click="requestReview" class="w-full py-2 bg-orange-600 text-white rounded font-bold text-xs hover:bg-orange-700">Send for Internal Review</button>
                     </div>

                     <div v-if="selectedMemo.status === 'reviewing' && canSign && selectedMemo.sender_mda.id === user?.mda" class="p-4 bg-blue-50 border border-blue-100 rounded-xl">
                        <label class="block text-[10px] font-bold text-blue-600 uppercase mb-2">Internal Approval</label>
                        <p class="text-[11px] text-blue-700 mb-3">As Supervisor, you must approve the content.</p>
                        <button @click="approveMemo" class="w-full py-2 bg-blue-600 text-white rounded font-bold text-xs hover:bg-blue-700">Grant Minute Approval</button>
                     </div>

                     <div v-if="selectedMemo.status === 'approved' && isRegistrar && selectedMemo.sender_mda.id === user?.mda" class="p-4 bg-indigo-50 border border-indigo-100 rounded-xl">
                        <label class="block text-[10px] font-bold text-indigo-600 uppercase mb-2">Registry Registration</label>
                        <input v-model="registrationFileNumber" placeholder="File Ref (e.g. ICTA/5/2)" class="w-full px-3 py-2 border rounded text-xs mb-2">
                        <button @click="registerMemo" class="w-full py-2 bg-indigo-600 text-white rounded font-bold text-xs hover:bg-indigo-700">Assign Ref & Register</button>
                     </div>

                     <div v-if="selectedMemo.status === 'registered' && canSign && selectedMemo.sender_mda.id === user?.mda" class="p-4 bg-emerald-50 border border-emerald-100 rounded-xl">
                        <label class="block text-[10px] font-bold text-emerald-600 uppercase mb-2">Issuance & Signing</label>
                        <button @click="signMemo" class="w-full py-2 bg-emerald-600 text-white rounded font-bold text-xs hover:bg-emerald-700">Apply Digital Signature</button>
                     </div>

                     <div v-if="selectedMemo.status === 'actioning' && selectedMemo.recipient_mda === user?.mda" class="p-4 bg-violet-50 border border-violet-100 rounded-xl">
                        <label class="block text-[10px] font-bold text-violet-600 uppercase mb-2">Action Assignment</label>
                        <select v-model="assignmentData.user_id" class="w-full p-2 border rounded text-xs mb-2">
                           <option v-for="staff in staffUsers" :key="staff.id" :value="staff.id">{{ staff.username }}</option>
                        </select>
                        <textarea v-model="assignmentData.instruction" placeholder="Instructions..." class="w-full p-2 border rounded text-xs mb-2 h-16"></textarea>
                        <button @click="assignAction" class="w-full py-2 bg-violet-600 text-white rounded font-bold text-xs hover:bg-violet-700">Assign Task</button>
                     </div>
                  </div>

                  <div v-if="selectedMemo.actions?.length > 0" class="space-y-3">
                    <h4 class="text-xs font-bold text-gray-400 uppercase">Tracked Actions</h4>
                    <div v-for="action in selectedMemo.actions" :key="action.id" class="p-3 bg-white rounded border border-gray-100 text-[10px]">
                       <p class="font-bold">{{ action.assigned_to_details?.username }}</p>
                       <p class="text-gray-500 my-1">{{ action.instruction }}</p>
                       <span :class="action.is_completed ? 'text-green-600' : 'text-orange-600 font-bold'">{{ action.is_completed ? 'DONE' : 'PENDING' }}</span>
                    </div>
                  </div>
                </div>
             </div>

             <!-- Footer -->
             <div class="p-4 border-t border-gray-100 bg-gray-50 text-right">
                <button @click="selectedMemo = null" class="px-6 py-2 bg-white border border-gray-300 rounded font-bold text-gray-700 hover:bg-gray-100 transition-all text-xs">Close Dossier</button>
             </div>
          </div>
       </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../../services/api';
import { useAuthStore } from '../../store/auth';
import { useMdaStore } from '../../store/mda';

const authStore = useAuthStore();
const mdaStore = useMdaStore();

const memos = ref([]);
const govFiles = ref([]);
const loading = ref(true);
const activeTab = ref('inbox');
const showComposeModal = ref(false);
const selectedMemo = ref(null);
const staffUsers = ref([]);

// Registry Data
const registrationFileNumber = ref('');
const assignmentData = ref({ user_id: '', instruction: '' });

const newMemo = ref({
  is_letter: false,
  memo_type: 'operational',
  recipient_mda: '',
  subject: '',
  content: '',
  priority: 'normal'
});

const user = computed(() => authStore.user);
const mdas = computed(() => mdaStore.mdas);
const isRegistrar = computed(() => user.value?.role === 'registrar' || user.value?.role === 'admin');
const canSign = computed(() => ['supervisor', 'mda_admin', 'admin'].includes(user.value?.role));

const inboundMemos = computed(() => memos.value.filter(m => m.recipient_mda === user.value?.mda && m.status !== 'draft'));
const outboundMemos = computed(() => memos.value.filter(m => m.sender_mda?.id === user.value?.mda));
const pendingRegistration = computed(() => memos.value.filter(m => m.status === 'draft' && m.sender_mda?.id === user.value?.mda));
const actionQueue = computed(() => memos.value.filter(m => m.status === 'actioning'));
const signedMemosCount = computed(() => memos.value.filter(m => m.digitally_signed).length);

const activeList = computed(() => {
  if (activeTab.value === 'inbox') return inboundMemos.value;
  if (activeTab.value === 'sent') return outboundMemos.value;
  if (activeTab.value === 'registry') return pendingRegistration.value;
  return [];
});

const fetchMemos = async () => {
   loading.value = true;
   try {
      const res = await api.get('/memos/');
      memos.value = res.data;
      
      if (activeTab.value === 'files') {
        const filesRes = await api.get('/government-files/');
        govFiles.value = filesRes.data;
      }
   } catch (e) {
      console.error(e);
   } finally {
      loading.value = false;
   }
};

const fetchStaff = async () => {
    try {
        const res = await api.get('/users/');
        staffUsers.value = res.data.filter(u => u.mda === user.value?.mda);
    } catch (e) {
        console.error(e);
    }
}

const sendMemo = async () => {
   if (!newMemo.value.recipient_mda) {
      alert('Please select a recipient MDA');
      return;
   }
   const wasLetter = newMemo.value.is_letter;
   try {
      await api.post('/memos/', newMemo.value);
      showComposeModal.value = false;
      newMemo.value = { is_letter: false, memo_type: 'operational', recipient_mda: '', subject: '', content: '', priority: 'normal' };
      fetchMemos();
      alert(wasLetter ? 'Official Letter initiated successfully.' : 'Internal Memo initiated successfully.');
   } catch (e) {
      const errorMsg = e.response?.data?.detail || e.response?.data?.message || 'Failed to initiate correspondence. Ensure you belong to an MDA.';
      alert(errorMsg);
   }
};

const requestReview = async () => {
    try {
        await api.post(`/memos/${selectedMemo.value.id}/request_review/`);
        fetchMemos();
        selectedMemo.value = null;
        alert('Memo sent for internal review.');
    } catch (e) {
        alert('Failed to send for review.');
    }
};

const approveMemo = async () => {
    try {
        await api.post(`/memos/${selectedMemo.value.id}/approve_memo/`);
        fetchMemos();
        selectedMemo.value = null;
        alert('Internal approval granted.');
    } catch (e) {
        alert('Approval failed.');
    }
};

const registerMemo = async () => {
   try {
      await api.post(`/memos/${selectedMemo.value.id}/register_memo/`, { file_number: registrationFileNumber.value });
      registrationFileNumber.value = '';
      fetchMemos();
      selectedMemo.value = null;
      alert('Memo successfully registered in GoK Registry.');
   } catch (e) {
      alert(e.response?.data?.detail || 'Registry registration failed.');
   }
};

const signMemo = async () => {
   try {
      await api.post(`/memos/${selectedMemo.value.id}/sign_memo/`);
      fetchMemos();
      selectedMemo.value = null;
      alert('Digital Signature Applied. Memo issued to recipient.');
   } catch (e) {
      alert('Signature failed.');
   }
};

const assignAction = async () => {
    try {
        await api.post(`/memos/${selectedMemo.value.id}/assign_action/`, { 
            assigned_to: assignmentData.value.user_id,
            instruction: assignmentData.value.instruction
        });
        assignmentData.value = { user_id: '', instruction: '' };
        fetchMemos();
        alert('Action assigned to officer.');
    } catch (e) {
        alert('Assignment failed.');
    }
}

const viewMemo = async (memo) => {
   selectedMemo.value = memo;
   if (memo.recipient_mda === user.value?.mda && !memo.is_read) {
      try {
         await api.post(`/memos/${memo.id}/mark_read/`);
         memo.is_read = true;
      } catch (e) {}
   }
};

const statusBg = (s) => {
   if (s === 'draft') return 'bg-gray-300';
   if (s === 'registered') return 'bg-orange-400';
   if (s === 'actioning') return 'bg-indigo-500';
   if (s === 'responded') return 'bg-green-500';
   return 'bg-blue-300';
}

const memoTypeColor = (t) => {
   if (t === 'policy') return 'bg-purple-50 text-purple-700 border-purple-200';
   if (t === 'instruction') return 'bg-red-50 text-red-700 border-red-200';
   if (t === 'concurrence') return 'bg-blue-50 text-blue-700 border-blue-200';
   return 'bg-gray-50 text-gray-700 border-gray-200';
}

const formatDate = (dateStr) => {
   if (!dateStr) return '';
   return new Date(dateStr).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
};

onMounted(() => {
   fetchMemos();
   fetchStaff();
   if (mdas.value.length === 0) mdaStore.fetchMdas();
});
</script>

