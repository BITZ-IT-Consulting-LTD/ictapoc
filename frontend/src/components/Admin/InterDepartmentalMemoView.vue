<template>
   <div class="u-flex u-flex-col u-gap-8">
      <!-- Header -->
      <header class="page__header u-bg-white u-p-6 u-rounded-lg u-shadow-sm u-border">
         <div class="page__title-group">
            <h1 class="page__title u-flex u-items-center u-gap-3">
               <i class="bi bi-envelope-paper u-text-primary"></i>
               Registry & Correspondence
            </h1>
            <p class="page__subtitle">Authoritative Government Internal Service (G2G)</p>
         </div>
         <div class="page__actions">
            <button @click="showComposeModal = true" class="button button--primary button--pill">
               <i class="bi bi-plus-lg"></i>
               Initiate Correspondence
            </button>
         </div>
      </header>

      <!-- Stats Overview -->
      <div class="stats-grid">
         <div class="stats-card stats-card--info">
            <div class="stats-card__content">
               <div class="stats-card__icon-wrapper">
                  <i class="bi bi-inbox"></i>
               </div>
               <div class="stats-card__text-content">
                  <span class="stats-card__label">Registry Inbox</span>
                  <span class="stats-card__value">{{ inboundMemos.length }}</span>
               </div>
            </div>
         </div>
         <div v-if="isRegistrar" class="stats-card stats-card--warning">
            <div class="stats-card__content">
               <div class="stats-card__icon-wrapper">
                  <i class="bi bi-hourglass-split"></i>
               </div>
               <div class="stats-card__text-content">
                  <span class="stats-card__label">Pending Registration</span>
                  <span class="stats-card__value">{{ pendingRegistration.length }}</span>
               </div>
            </div>
         </div>
         <div class="stats-card stats-card--primary">
            <div class="stats-card__content">
               <div class="stats-card__icon-wrapper">
                  <i class="bi bi-list-check"></i>
               </div>
               <div class="stats-card__text-content">
                  <span class="stats-card__label">Action Queue</span>
                  <span class="stats-card__value">{{ actionQueue.length }}</span>
               </div>
            </div>
         </div>
         <div class="stats-card stats-card--success">
            <div class="stats-card__content">
               <div class="stats-card__icon-wrapper">
                  <i class="bi bi-check-circle"></i>
               </div>
               <div class="stats-card__text-content">
                  <span class="stats-card__label">Signed & Issued</span>
                  <span class="stats-card__value">{{ signedMemosCount }}</span>
               </div>
            </div>
         </div>
      </div>

      <!-- Tabs -->
      <div class="tab-bar">
         <button @click="activeTab = 'inbox'" :class="{ 'tab-bar__item--active': activeTab === 'inbox' }"
            class="tab-bar__item">
            Inbox
         </button>
         <button @click="activeTab = 'sent'" :class="{ 'tab-bar__item--active': activeTab === 'sent' }"
            class="tab-bar__item">
            Sent
         </button>
         <button v-if="isRegistrar" @click="activeTab = 'registry'"
            :class="{ 'tab-bar__item--active': activeTab === 'registry' }" class="tab-bar__item">
            Registry Queue
         </button>
         <button @click="activeTab = 'files'" :class="{ 'tab-bar__item--active': activeTab === 'files' }"
            class="tab-bar__item">
            File Registry
         </button>
      </div>

      <!-- Main List Container -->
      <div class="card u-overflow-hidden" style="min-height: 400px">
         <div v-if="loading" class="u-p-20 u-text-center u-text-muted">
            <div class="animate-spin u-text-3xl u-text-primary u-mb-4 mx-auto">
               <i class="bi bi-arrow-clockwise u-block"></i>
            </div>
            <p class="u-text-sm u-font-bold u-uppercase u-tracking-widest">Syncing with GoK Registry...</p>
         </div>

         <!-- Files Tab -->
         <div v-else-if="activeTab === 'files'" class="u-p-0">
            <div v-if="govFiles.length === 0" class="u-p-20 u-text-center u-text-muted u-italic">No files found in
               registry.</div>
            <div class="list">
               <div v-for="file in govFiles" :key="file.id"
                  class="list__item u-justify-between u-items-center cursor-pointer">
                  <div class="u-flex u-items-center u-gap-4">
                     <div
                        class="u-w-10 u-h-10 u-bg-bg-alt u-rounded-lg u-flex u-items-center u-justify-center u-text-muted">
                        <i class="bi bi-folder2 text-xl"></i>
                     </div>
                     <div>
                        <p class="u-font-bold u-text-main">{{ file.file_number }}</p>
                        <p class="u-text-xs u-text-muted">{{ file.subject }}</p>
                     </div>
                  </div>
                  <span class="badge badge--success">{{ file.status.toUpperCase() }}</span>
               </div>
            </div>
         </div>

         <!-- Correspondence/Memos List -->
         <div v-else-if="activeList.length === 0" class="u-p-20 u-text-center u-text-muted">
            <i class="bi bi-file-earmark-text u-text-5xl u-mb-4 u-opacity-20 u-block"></i>
            <p class="u-text-sm u-font-bold u-uppercase u-tracking-widest">No official correspondence found in {{
               activeTab }}.</p>
         </div>

         <div v-else class="list">
            <div v-for="memo in activeList" :key="memo.id" @click="viewMemo(memo)"
               class="list__item u-items-start u-gap-4 cursor-pointer"
               :class="{ 'u-bg-primary-soft': memo.status === 'registered' && !memo.is_read }">
               <!-- Status Indicator -->
               <div class="u-block u-self-stretch u-rounded-full" style="width: 4px" :class="statusBg(memo.status)">
               </div>

               <div class="u-flex-1 u-min-w-0">
                  <div class="u-flex u-justify-between u-mb-1">
                     <div class="u-flex u-items-center u-gap-2">
                        <span class="badge badge--small" :class="memoTypeColor(memo.memo_type)">{{
                           memo.memo_type.toUpperCase() }}</span>
                        <p class="u-text-sm u-font-bold u-text-main u-truncate">{{ memo.subject }}</p>
                     </div>
                     <span class="u-text-[10px] u-font-mono u-text-muted">{{ formatDate(memo.created_at) }}</span>
                  </div>

                  <div class="u-flex u-justify-between u-items-end">
                     <div class="u-text-[11px] u-text-muted">
                        <span v-if="activeTab === 'inbox'">From: <span class="u-font-bold u-text-main">{{
                           memo.sender_mda?.name }}</span></span>
                        <span v-else>To: <span class="u-font-bold u-text-main">{{ memo.recipient_mda_details?.name
                              }}</span></span>
                        <span class="u-mx-2 u-opacity-30">|</span>
                        <span class="u-font-mono u-text-primary u-font-bold" v-if="memo.official_ref">{{
                           memo.official_ref }}</span>
                        <span class="u-text-muted u-italic" v-else>UNREGISTERED</span>
                     </div>

                     <div class="u-flex u-gap-2">
                        <span v-if="memo.digitally_signed" class="badge badge--success u-gap-1">
                           <i class="bi bi-patch-check-fill"></i>
                           SIGNED
                        </span>
                        <span v-if="memo.priority === 'urgent'" class="badge badge--danger">URGENT</span>
                     </div>
                  </div>
               </div>
            </div>
         </div>
         <!-- Pagination Footer -->
         <footer v-if="memoMeta.count > 0"
            class="card__footer u-bg-page u-py-3 u-px-6 u-flex u-justify-between u-items-center u-border-t">
            <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">
               Total Correspondence: {{ memoMeta.count }} items
            </span>
            <div class="u-flex u-gap-2">
               <button @click="fetchMemos(currentPage - 1)" :disabled="!memoMeta.previous"
                  class="button button--secondary button--small button--pill px-4 py-1 flex items-center justify-center">
                  <i class="bi bi-chevron-left mr-2"></i> Previous
               </button>
               <button @click="fetchMemos(currentPage + 1)" :disabled="!memoMeta.next"
                  class="button button--secondary button--small button--pill px-4 py-1 flex items-center justify-center">
                  Next <i class="bi bi-chevron-right ml-2"></i>
               </button>
            </div>
         </footer>
      </div>

      <!-- Initiation Modal -->
      <BaseModal :show="showComposeModal" @close="showComposeModal = false" size="lg" headerClass="modal__header--dark">
         <template #header>
            <div class="u-flex u-flex-col">
               <h3 class="modal__title">Initiate Official Correspondence</h3>
               <p class="modal__subtitle">Governed by GoK Registry Rules</p>
            </div>
         </template>

         <form @submit.prevent="sendMemo" id="memoForm" class="u-flex u-flex-col u-gap-4">
            <div class="u-flex u-gap-4">
               <div class="u-flex-1">
                  <label class="u-block u-text-[11px] u-font-bold u-text-muted u-uppercase u-mb-1">Correspondence
                     Mode</label>
                  <div class="tab-bar u-w-full">
                     <button type="button" @click="newMemo.is_letter = false"
                        :class="{ 'tab-bar__item--active': !newMemo.is_letter }" class="tab-bar__item u-flex-1">Internal
                        Memo</button>
                     <button type="button" @click="newMemo.is_letter = true"
                        :class="{ 'tab-bar__item--active': newMemo.is_letter }" class="tab-bar__item u-flex-1">Official
                        Letter</button>
                  </div>
               </div>
               <div class="u-flex-1">
                  <label class="u-block u-text-[11px] u-font-bold u-text-muted u-uppercase u-mb-1">Type/Purpose</label>
                  <div class="u-relative">
                     <input type="text" v-model="memoTypeSearchLocal" placeholder="Select Type..." readonly
                        @focus="showMemoTypeDropdown = true" @blur="closeDropdownWithDelay('memoType')"
                        class="form__input u-cursor-pointer">
                     <div v-if="showMemoTypeDropdown"
                        class="u-absolute u-top-full u-left-0 u-w-full bg-white u-border u-shadow-xl u-rounded-lg u-mt-1 u-z-dropdown u-p-1">
                        <div
                           v-for="t in ['policy', 'operational', 'instruction', 'concurrence', 'escalation', 'information', 'external']"
                           :key="t" @click="selectMemoType(t)"
                           class="u-p-2 hover:u-bg-bg-page u-rounded u-cursor-pointer u-text-xs u-text-main transition-colors capitalize">
                           {{ t }}
                        </div>
                     </div>
                     <i class="bi bi-chevron-down u-absolute u-right-3 u-top-2.5 u-text-muted"></i>
                  </div>
               </div>
            </div>

            <div class="u-flex u-gap-4">
               <div class="u-flex-1">
                  <label class="u-block u-text-[11px] u-font-bold u-text-muted u-uppercase u-mb-1">Recipient MDA</label>
                  <div class="u-relative">
                     <input type="text" v-model="recipientMdaSearchLocal" placeholder="Search MDA..."
                        @focus="showRecipientDropdown = true" @blur="closeDropdownWithDelay('recipient')"
                        class="form__input u-cursor-pointer">
                     <div v-if="showRecipientDropdown"
                        class="u-absolute u-top-full u-left-0 u-w-full bg-white u-border u-shadow-xl u-rounded-lg u-mt-1 u-z-dropdown u-p-1 u-max-h-48 u-overflow-auto">
                        <div v-for="mda in filteredMdasForRecipient" :key="mda.id" @click="selectRecipient(mda)"
                           class="u-p-2 hover:u-bg-bg-page u-rounded u-cursor-pointer u-text-xs u-text-main transition-colors">
                           {{ mda.name }}
                        </div>
                     </div>
                     <i class="bi bi-search u-absolute u-right-3 u-top-2.5 u-text-muted"></i>
                  </div>
               </div>
               <div class="u-flex-1">
                  <label class="u-block u-text-[11px] u-font-bold u-text-muted u-uppercase u-mb-1">Priority</label>
                  <div class="u-relative">
                     <input type="text" v-model="prioritySearchLocal" placeholder="Select Priority..." readonly
                        @focus="showPriorityDropdown = true" @blur="closeDropdownWithDelay('priority')"
                        class="form__input u-cursor-pointer">
                     <div v-if="showPriorityDropdown"
                        class="u-absolute u-top-full u-left-0 u-w-full bg-white u-border u-shadow-xl u-rounded-lg u-mt-1 u-z-dropdown u-p-1">
                        <div v-for="p in ['normal', 'high', 'urgent']" :key="p" @click="selectPriority(p)"
                           class="u-p-2 hover:u-bg-bg-page u-rounded u-cursor-pointer u-text-xs u-text-main transition-colors capitalize u-flex u-items-center u-gap-2">
                           <span class="u-block u-w-2 u-h-2 u-rounded-full"
                              :style="{ background: p === 'urgent' ? 'var(--color-danger)' : p === 'high' ? 'var(--color-warning)' : 'var(--color-info)' }"></span>
                           {{ p }}
                        </div>
                     </div>
                     <i class="bi bi-chevron-down u-absolute u-right-3 u-top-2.5 u-text-muted"></i>
                  </div>
               </div>
            </div>

            <div>
               <label class="u-block u-text-[11px] u-font-bold u-text-muted u-uppercase u-mb-1">Subject</label>
               <input v-model="newMemo.subject" type="text" required class="form__input"
                  placeholder="Official Subject Line">
            </div>

            <div>
               <label class="u-block u-text-[11px] u-font-bold u-text-muted u-uppercase u-mb-1">Content</label>
               <textarea v-model="newMemo.content" rows="6" required class="form__input"
                  style="resize: none; min-height: 15rem" placeholder="Draft your memo content here..."></textarea>
            </div>
         </form>

         <template #footer>
            <button type="button" @click="showComposeModal = false" class="button button--secondary">Save Draft</button>
            <button type="submit" form="memoForm" class="button button--primary">
               Initiate Approval
               <i class="bi bi-send-check"></i>
            </button>
         </template>
      </BaseModal>

      <!-- Detailed Reader Modal -->
      <BaseModal :show="!!selectedMemo" @close="selectedMemo = null" size="full" headerClass="modal__header--dark">
         <template #header>
            <div class="u-flex u-flex-col">
               <h2 class="modal__title u-uppercase">{{ selectedMemo.subject }}</h2>
               <div class="modal-subtitle u-flex u-items-center u-gap-2">
                  <span v-if="selectedMemo.official_ref" class="u-font-bold">REF: {{ selectedMemo.official_ref }}</span>
                  <span v-else class="u-font-bold u-text-warning">UNREGISTERED DRAFT</span>
                  <span class="u-opacity-50">&bull; {{ formatDate(selectedMemo.created_at) }}</span>
               </div>
            </div>
         </template>

         <div class="u-flex u-h-full u-overflow-hidden" style="margin: -var(--spacing-6)">
            <div class="modal-body u-flex u-p-0 u-w-full">
               <!-- Main Content -->
               <div class="u-flex-1 u-p-10 u-bg-white u-overflow-auto u-border-r">
                  <div class="u-mb-8 u-border-b u-border-border-color u-pb-6">
                     <div
                        class="u-flex u-justify-between u-text-[10px] u-font-bold u-text-muted u-uppercase u-tracking-widest u-mb-6">
                        <span>GoK FORM 004</span>
                        <span>AUTHORITATIVE SYSTEM OUTPUT</span>
                     </div>
                     <div class="u-grid u-gap-3">
                        <div class="u-flex u-items-center"><span
                              class="u-block u-w-24 u-text-[10px] u-font-black u-text-muted u-uppercase">From:</span>
                           <span class="u-font-bold u-text-main">{{ selectedMemo.sender_mda?.name }}</span>
                        </div>
                        <div class="u-flex u-items-center"><span
                              class="u-block u-w-24 u-text-[10px] u-font-black u-text-muted u-uppercase">To:</span>
                           <span class="u-font-bold u-text-main">{{ selectedMemo.recipient_mda_details?.name }}</span>
                        </div>
                        <div class="u-flex u-items-center"><span
                              class="u-block u-w-24 u-text-[10px] u-font-black u-text-muted u-uppercase">Subject:</span>
                           <span class="u-font-black u-text-primary">{{ selectedMemo.subject }}</span>
                        </div>
                        <div class="u-flex u-items-center"><span
                              class="u-block u-w-24 u-text-[10px] u-font-black u-text-muted u-uppercase">Type:</span>
                           <span class="badge badge--info">{{ selectedMemo.memo_type?.toUpperCase() }}</span>
                        </div>
                     </div>
                  </div>

                  <div class="prose u-text-lg u-leading-relaxed u-text-main"
                     style="white-space: pre-wrap; font-family: 'Georgia', serif;">
                     {{ selectedMemo.content }}
                  </div>

                  <div class="u-mt-12 u-flex u-justify-end" v-if="selectedMemo.digitally_signed">
                     <div class="u-text-right u-border-t u-pt-4 u-w-64">
                        <div class="u-mb-2">
                           <i class="bi bi-patch-check-fill u-text-5xl u-text-success u-opacity-30"></i>
                        </div>
                        <p class="u-font-bold u-text-main u-border-b u-pb-1">DIGITALLY SIGNED</p>
                        <p class="u-text-[10px] u-text-muted u-mt-1">Officer: {{ selectedMemo.signed_by?.username }}</p>
                        <p class="u-text-[10px] u-text-muted">{{ formatDate(selectedMemo.updated_at) }}</p>
                     </div>
                  </div>
               </div>

               <!-- Action Sidebar -->
               <div class="u-w-80 u-bg-bg-alt u-p-6 u-flex u-flex-col u-gap-6 u-overflow-y-auto">
                  <div class="u-flex u-flex-col u-gap-4">
                     <div v-if="selectedMemo.status === 'draft' && selectedMemo.sender_mda.id === user?.mda"
                        class="u-p-4 u-bg-bg u-rounded-lg u-border">
                        <label class="u-block u-text-[10px] u-font-black u-text-warning u-uppercase u-mb-2">Internal
                           Submission</label>
                        <p class="u-text-[11px] u-text-muted u-mb-3">Draft complete. Send to Director for internal
                           verification.</p>
                        <button @click="requestReview" class="button button--primary button--small u-w-full">Send for
                           Internal
                           Review</button>
                     </div>

                     <div
                        v-if="selectedMemo.status === 'reviewing' && canSign && selectedMemo.sender_mda.id === user?.mda"
                        class="u-p-4 u-bg-bg u-rounded-lg u-border">
                        <label class="u-block u-text-[10px] u-font-black u-text-primary u-uppercase u-mb-2">Internal
                           Approval</label>
                        <p class="u-text-[11px] u-text-muted u-mb-3">As Supervisor, you must approve the content.</p>
                        <button @click="approveMemo" class="button button--primary button--small u-w-full">Grant Minute
                           Approval</button>
                     </div>

                     <div
                        v-if="selectedMemo.status === 'approved' && isRegistrar && selectedMemo.sender_mda.id === user?.mda"
                        class="u-p-4 u-bg-bg u-rounded-lg u-border">
                        <label class="u-block u-text-[10px] u-font-black u-text-info u-uppercase u-mb-2">Registry
                           Registration</label>
                        <input v-model="registrationFileNumber" placeholder="File Ref (e.g. ICTA/5/2)"
                           class="form__input u-mb-2">
                        <button @click="registerMemo" class="button button--primary button--small u-w-full">Assign Ref &
                           Register</button>
                     </div>

                     <div
                        v-if="selectedMemo.status === 'registered' && canSign && selectedMemo.sender_mda.id === user?.mda"
                        class="u-p-4 u-bg-bg u-rounded-lg u-border">
                        <label class="u-block u-text-[10px] u-font-black u-text-success u-uppercase u-mb-2">Issuance &
                           Signing</label>
                        <button @click="signMemo" class="button button--success button--small u-w-full">Apply Digital
                           Signature</button>
                     </div>

                     <div v-if="selectedMemo.status === 'actioning' && selectedMemo.recipient_mda === user?.mda"
                        class="u-p-4 u-bg-bg u-rounded-lg u-border">
                        <label class="u-block u-text-[10px] u-font-black u-text-primary u-uppercase u-mb-2">Action
                           Assignment</label>
                        <select v-model="assignmentData.user_id" class="form__input u-mb-2">
                           <option v-for="staff in staffUsers" :key="staff.id" :value="staff.id">{{ staff.username }}
                           </option>
                        </select>
                        <textarea v-model="assignmentData.instruction" placeholder="Instructions..."
                           class="form__input u-mb-2" style="resize: none; height: 5rem"></textarea>
                        <button @click="assignAction" class="button button--primary button--small u-w-full">Assign
                           Task</button>
                     </div>
                  </div>

                  <div v-if="selectedMemo.actions?.length > 0" class="u-flex u-flex-col u-gap-3">
                     <h4 class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Tracked Actions
                     </h4>
                     <div v-for="action in selectedMemo.actions" :key="action.id"
                        class="u-p-3 u-bg-bg u-rounded u-border u-text-[10px]">
                        <p class="u-font-bold u-text-main">{{ action.assigned_to_details?.username }}</p>
                        <p class="u-text-muted u-my-1">{{ action.instruction }}</p>
                        <span :class="action.is_completed ? 'u-text-success' : 'u-text-warning u-font-bold'">{{
                           action.is_completed ? 'DONE' : 'PENDING' }}</span>
                     </div>
                  </div>
               </div>
            </div>
         </div>

         <template #footer>
            <div></div>
            <button @click="selectedMemo = null" class="button button--secondary">Close Dossier</button>
         </template>
      </BaseModal>
   </div>
</template>

<script setup>
   import { ref, computed, onMounted, watch } from 'vue';
   import api from '../../services/api';
   import { useAuthStore } from '../../store/auth';
   import { useMdaStore } from '../../store/mda';
   import BaseModal from '../Common/BaseModal.vue';

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

   const memoTypeSearchLocal = ref('Operational Request');
   const showMemoTypeDropdown = ref(false);
   const selectMemoType = (type) => {
      newMemo.value.memo_type = type;
      memoTypeSearchLocal.value = type.charAt(0).toUpperCase() + type.slice(1);
      showMemoTypeDropdown.value = false;
   };

   const recipientMdaSearchLocal = ref('');
   const showRecipientDropdown = ref(false);
   const filteredMdasForRecipient = computed(() => {
      if (!recipientMdaSearchLocal.value) return mdas.value;
      const q = recipientMdaSearchLocal.value.toLowerCase();
      return mdas.value.filter(m => m.name.toLowerCase().includes(q));
   });
   const selectRecipient = (mda) => {
      newMemo.value.recipient_mda = mda.id;
      recipientMdaSearchLocal.value = mda.name;
      showRecipientDropdown.value = false;
   };

   const prioritySearchLocal = ref('Normal');
   const showPriorityDropdown = ref(false);
   const selectPriority = (p) => {
      newMemo.value.priority = p;
      prioritySearchLocal.value = p.charAt(0).toUpperCase() + p.slice(1);
      showPriorityDropdown.value = false;
   };

   const closeDropdownWithDelay = (type) => {
      setTimeout(() => {
         if (type === 'memoType') showMemoTypeDropdown.value = false;
         if (type === 'recipient') showRecipientDropdown.value = false;
         if (type === 'priority') showPriorityDropdown.value = false;
      }, 200);
   };

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

   const memoMeta = ref({ count: 0, next: null, previous: null });
   const currentPage = ref(1);

   const fetchMemos = async (page = 1) => {
      loading.value = true;
      currentPage.value = page;
      try {
         const params = {
            page: page,
            memo_type: activeTab.value === 'files' ? undefined : undefined, // Handled differently if needed
         };

         // Map tabs to backend filters if applicable
         if (activeTab.value === 'inbox') {
            // Explicitly handled by queryset on backend usually, but we can pass filters
         }

         const res = await api.get('/memos/', { params });
         // If global pagination is on, data will be { results: [], count: 0, ... }
         if (res.data.results) {
            memos.value = res.data.results;
            memoMeta.value = {
               count: res.data.count,
               next: res.data.next,
               previous: res.data.previous
            };
         } else {
            memos.value = res.data;
            memoMeta.value = { count: res.data.length, next: null, previous: null };
         }

         if (activeTab.value === 'files') {
            const filesRes = await api.get('/government-files/');
            // Files also paginated?
            govFiles.value = filesRes.data.results || filesRes.data;
         }
      } catch (e) {
         console.error(e);
      } finally {
         loading.value = false;
      }
   };

   // Re-fetch when tab changes
   watch(activeTab, () => {
      fetchMemos(1);
   });

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
         } catch (e) { }
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
