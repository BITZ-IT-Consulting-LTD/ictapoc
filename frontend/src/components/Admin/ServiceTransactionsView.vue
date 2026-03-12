<template>
  <section class="page service-transactions-view">
    <header class="page__header flex-col md:flex-row gap-4 items-start md:items-center u-mb-8">
      <div class="page__title-group">
        <div class="u-flex u-items-center u-gap-3 u-mb-2">
           <button @click="$emit('go-back-services')" class="button button--ghost button--small p-0 hover:bg-transparent">
              <i class="bi bi-arrow-left-circle-fill text-primary text-xl"></i>
           </button>
           <span class="badge badge--primary u-font-mono u-text-[10px] u-tracking-widest">{{ service.service_code }}</span>
           <span class="u-text-[10px] u-font-black u-text-muted/60 u-tracking-widest uppercase">{{ getMdaName(service.mda) }}</span>
        </div>
        <h1 class="page__title">{{ service.service_name }}</h1>
        <p class="page__subtitle">Live transaction stream and operational audit trail</p>
      </div>
      <div class="page__actions ms-auto u-flex u-gap-3">
        <button @click="$emit('go-back-services')" class="button button--secondary button--pill">
          <i class="bi bi-arrow-left me-2"></i> Back to Services
        </button>
        <button @click="$emit('configure-service', service)" class="button button--primary button--pill shadow-lg">
          <i class="bi bi-gear-wide-connected me-2"></i> Configure Service
        </button>
      </div>
    </header>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 u-mb-8">
       <div class="card p-6 u-flex u-items-center u-gap-4">
          <div class="u-w-12 u-h-12 u-rounded-2xl u-bg-primary/10 u-flex u-items-center u-justify-center text-primary">
             <i class="bi bi-activity text-2xl"></i>
          </div>
          <div>
             <div class="u-text-[10px] u-font-black u-text-muted u-uppercase">Total Volume</div>
             <div class="u-text-2xl u-font-black text-main">{{ transactions.length }}</div>
          </div>
       </div>
       <div class="card p-6 u-flex u-items-center u-gap-4">
          <div class="u-w-12 u-h-12 u-rounded-2xl u-bg-success/10 u-flex u-items-center u-justify-center text-success">
             <i class="bi bi-check-all text-2xl"></i>
          </div>
          <div>
             <div class="u-text-[10px] u-font-black u-text-muted u-uppercase">Completed</div>
             <div class="u-text-2xl u-font-black text-main">{{ transactions.filter(t => ['approved', 'closed'].includes(t.status)).length }}</div>
          </div>
       </div>
       <div class="card p-6 u-flex u-items-center u-gap-4">
          <div class="u-w-12 u-h-12 u-rounded-2xl u-bg-warning/10 u-flex u-items-center u-justify-center text-warning">
             <i class="bi bi-hourglass-split text-2xl"></i>
          </div>
          <div>
             <div class="u-text-[10px] u-font-black u-text-muted u-uppercase">In Progress</div>
             <div class="u-text-2xl u-font-black text-main">{{ transactions.filter(t => t.status === 'in_progress').length }}</div>
          </div>
       </div>
       <div class="card p-6 u-flex u-items-center u-gap-4">
          <div class="u-w-12 u-h-12 u-rounded-2xl u-bg-danger/10 u-flex u-items-center u-justify-center text-danger">
             <i class="bi bi-exclamation-triangle text-2xl"></i>
          </div>
          <div>
             <div class="u-text-[10px] u-font-black u-text-muted u-uppercase">Critical / Escalated</div>
             <div class="u-text-2xl u-font-black text-main">{{ transactions.filter(t => t.priority === 'critical' || t.is_escalated).length }}</div>
          </div>
       </div>
    </div>

    <div class="toolbar u-mb-6">
      <div class="u-flex u-items-center u-gap-4 w-full md:w-1/2">
        <div class="u-relative u-flex-1">
          <i class="bi bi-search u-absolute u-left-4 u-top-1/2 -u-translate-y-1/2 u-text-muted"></i>
          <input type="text" v-model="searchQuery" placeholder="Search by Tracking ID or Citizen..." class="form__input u-pl-12 w-full">
        </div>
        <select v-model="statusFilter" class="form__select u-w-40">
           <option value="">All Statuses</option>
           <option value="received">Received</option>
           <option value="in_progress">In Progress</option>
           <option value="escalated">Escalated</option>
           <option value="approved">Approved</option>
           <option value="rejected">Rejected</option>
        </select>
      </div>
    </div>

    <!-- Transactions Table -->
    <div class="card border-0 shadow-lg overflow-hidden">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr class="u-bg-slate-50 border-b border-border-color">
              <th class="table__th u-pl-8 text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Tracking ID</th>
              <th class="table__th text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Citizen Participant</th>
              <th class="table__th text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Submission Date</th>
              <th class="table__th text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Current Node / Stage</th>
              <th class="table__th text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Status</th>
              <th class="table__th text-right u-pr-8 text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in filteredTransactions" :key="tx.id" class="table__row group hover:u-bg-blue-50/30 transition-colors">
              <td class="table__td u-pl-8">
                <span class="u-font-mono u-text-xs u-font-bold u-text-slate-700 bg-slate-100 u-px-2 u-py-1 u-rounded border border-slate-200">
                  {{ tx.request_id }}
                </span>
              </td>
              <td class="table__td">
                <div class="u-flex u-items-center u-gap-3">
                   <div class="u-w-8 u-h-8 u-rounded-full u-bg-slate-200 u-flex u-items-center u-justify-center u-text-[10px] u-font-black u-text-slate-500">
                      {{ getInitials(tx.citizen_details?.username) }}
                   </div>
                   <div class="u-flex u-flex-col">
                      <span class="u-font-bold text-main text-sm">{{ tx.citizen_details?.first_name }} {{ tx.citizen_details?.last_name || tx.citizen_details?.username }}</span>
                      <span class="u-text-[10px] u-text-muted italic">{{ tx.citizen_details?.email }}</span>
                   </div>
                </div>
              </td>
              <td class="table__td">
                 <div class="u-text-xs text-main">{{ formatDate(tx.created_at) }}</div>
                 <div class="u-text-[10px] u-text-muted">{{ formatTime(tx.created_at) }}</div>
              </td>
              <td class="table__td">
                 <div v-if="tx.current_step" class="u-flex u-items-center u-gap-2">
                    <span class="badge badge--pill bg-slate-100 text-slate-600 border border-slate-200 u-text-[9px] font-black uppercase">
                       Step {{ tx.current_step.sequence }}
                    </span>
                    <span class="u-text-xs u-font-bold text-main">{{ tx.current_step.step_name }}</span>
                 </div>
                 <div v-else class="u-text-xs u-text-muted italic">Process Terminated</div>
              </td>
              <td class="table__td">
                 <span class="badge" :class="getStatusClass(tx.status)">
                    {{ tx.status.replace('_', ' ').toUpperCase() }}
                 </span>
                 <i v-if="tx.is_escalated" class="bi bi-exclamation-triangle-fill text-danger u-ml-2" title="Escalated"></i>
              </td>
              <td class="table__td text-right u-pr-8">
                 <button @click="viewRequestDetails(tx)" class="button button--ghost button--small text-primary hover:u-underline">
                    View Trail <i class="bi bi-chevron-right u-ml-1"></i>
                 </button>
              </td>
            </tr>
            <tr v-if="transactions.length === 0">
               <td colspan="6" class="u-p-12 u-text-center u-text-muted u-italic">
                  <i class="bi bi-inbox u-text-4xl u-opacity-20 u-mb-4 u-block"></i>
                  No active transactions recorded for this service configuration yet.
               </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useStaffStore } from '../../store/staff';
  import { useMdaStore } from '../../store/mda';

  const props = defineProps({
    service: { type: Object, required: true }
  });

  const emit = defineEmits(['go-back-services', 'configure-service', 'view-request']);

  const staffStore = useStaffStore();
  const mdaStore = useMdaStore();
  
  const transactions = ref([]);
  const searchQuery = ref('');
  const statusFilter = ref('');

  onMounted(async () => {
    // We'll use a specialized fetch or filter the large pool
    // For POC, we'll fetch from the unassigned and assigned pools to build a view
    // In a real scenario, this would be an API call: GET /api/service-requests/?service_config=ID
    
    // For now, let's simulate the fetch or use the existing store if it has them
    await staffStore.fetchAssignedRequests({ service_config: props.service.id });
    // This is just a POC shortcut. Ideally we'd have a specific list for this view
    transactions.value = [
       ...staffStore.assignedRequests,
       ...staffStore.unassignedRequests
    ].filter(r => r.service_config.id === props.service.id || r.service_config === props.service.id);
  });

  const filteredTransactions = computed(() => {
    let result = transactions.value;
    if (statusFilter.value) {
      result = result.filter(t => t.status === statusFilter.value);
    }
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter(t => 
        t.request_id.toLowerCase().includes(q) ||
        (t.citizen_details?.username || '').toLowerCase().includes(q) ||
        (t.citizen_details?.first_name || '').toLowerCase().includes(q)
      );
    }
    return result;
  });

  const getMdaName = (mdaId) => {
    const mda = mdaStore.mdas.find(m => m.id === mdaId || (mdaId && mdaId.id === m.id));
    return mda ? mda.name : 'Unknown Agency';
  };

  const getInitials = (name) => {
    if (!name) return '??';
    return name.substring(0, 2).toUpperCase();
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  };

  const formatTime = (dateStr) => {
    return new Date(dateStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getStatusClass = (status) => {
    const map = {
      'received': 'badge--info',
      'in_progress': 'badge--primary',
      'approved': 'badge--success',
      'rejected': 'badge--danger',
      'escalated': 'badge--warning'
    };
    return map[status] || 'bg-slate-100 text-slate-500';
  };

  const viewRequestDetails = (tx) => {
     emit('view-request', tx);
  };
</script>
