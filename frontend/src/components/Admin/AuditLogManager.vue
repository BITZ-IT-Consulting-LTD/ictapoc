<template>
    <div class="u-flex u-flex-col u-gap-8 animate-fade-in">
    <!-- Audit Header -->
    <header class="u-flex u-justify-between u-items-center">
      <div class="page__title-group">
        <h3 class="u-text-2xl u-font-black u-text-main u-mb-1 u-border-l-4 u-border-slate-800 u-pl-4">
          System Activity & Audit Logs
        </h3>
        <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest">Permanent Ledger of Administrative Events</p>
      </div>
      <button @click="fetchLogs" class="button button--secondary button--small">
        <i class="bi bi-arrow-clockwise u-mr-1"></i> Refresh Logs
      </button>
    </header>

    <!-- Refined Filters -->
    <article class="card u-bg-page u-p-6 shadow-sm">
      <div class="u-grid u-grid-cols-1 md:u-grid-cols-3 u-gap-6">
        <div class="form-group">
          <label class="u-block u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-2 u-tracking-widest">Search Details</label>
          <div class="toolbar__filter-group u-shadow-none u-border u-border-border-color">
            <i class="bi bi-search toolbar__filter-icon"></i>
            <input type="text" v-model="searchQuery" placeholder="Reference ID or keyword..." class="toolbar__filter-input u-w-full" />
          </div>
        </div>
        <div class="form-group">
          <label class="u-block u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-2 u-tracking-widest">Actor Identity</label>
          <div class="toolbar__filter-group u-shadow-none u-border u-border-border-color">
            <i class="bi bi-person toolbar__filter-icon"></i>
            <input type="text" v-model="userFilter" placeholder="Staff Username..." class="toolbar__filter-input u-w-full" />
          </div>
        </div>
        <div class="form-group">
          <label class="u-block u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-2 u-tracking-widest">Legislative Action</label>
          <select v-model="actionFilter" class="toolbar__filter-input u-w-full u-border u-border-border-color u-rounded u-px-3">
             <option value="">All Administrative Actions</option>
             <option value="REQUEST_ESCALATED">Request Escalated</option>
             <option value="ESCALATION_ACKNOWLEDGED">Escalation Acknowledged</option>
             <option value="WORKFLOW_STEP_COMPLETED">Step Completed</option>
             <option value="USER_REGISTERED">User Registered</option>
          </select>
        </div>
      </div>
    </article>

    <!-- Audit Ledger Table -->
    <article class="card shadow-lg overflow-hidden">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr class="table__header-row u-bg-slate-800">
              <th class="table__header-cell u-text-white u-pl-6">Timestamp</th>
              <th class="table__header-cell u-text-white">Authoritative Actor</th>
              <th class="table__header-cell u-text-white">Action Integrity</th>
              <th class="table__header-cell u-text-white">Object Reference</th>
              <th class="table__header-cell u-text-white u-pr-6">Event Context</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in filteredLogs" :key="log.id" class="table__row">
              <td class="table__cell u-pl-6">
                <span class="u-text-[11px] u-font-mono u-text-muted u-font-bold">{{ formatTimestamp(log.timestamp) }}</span>
              </td>
              <td class="table__cell">
                <div class="u-flex u-items-center u-gap-3">
                  <div class="avatar avatar--sm" :class="getActorColor(log.actor)">
                    {{ log.actor?.username?.substring(0, 2) || 'S' }}
                  </div>
                  <div>
                    <div class="u-text-xs u-font-black u-text-main">{{ log.actor?.username || 'System' }}</div>
                    <div class="u-text-[10px] u-font-bold u-text-muted u-uppercase u-tracking-widest">{{ log.actor?.role || 'Service Account' }}</div>
                  </div>
                </div>
              </td>
              <td class="table__cell">
                <span class="badge badge--small" :class="actionBadgeClass(log.action)">
                  {{ log.action }}
                </span>
              </td>
              <td class="table__cell">
                <span class="table__code-badge u-text-primary">{{ log.service_request?.request_id || 'N/A' }}</span>
              </td>
              <td class="table__cell u-pr-6">
                <p class="u-text-xs u-text-muted u-max-w-xs u-truncate" :title="log.details">
                  {{ log.details }}
                </p>
              </td>
            </tr>
            <tr v-if="filteredLogs.length === 0">
               <td colspan="5" class="table__cell u-text-center u-py-20">
                 <div class="u-flex u-flex-col u-items-center u-gap-3">
                    <span class="u-text-3xl u-opacity-50">📑</span>
                    <p class="u-text-sm u-font-black u-text-muted u-uppercase u-tracking-widest">No audit signatures found in current scope</p>
                 </div>
               </td>
            </tr>
          </tbody>
        </table>
      </div>
      <footer class="card__footer u-bg-page u-py-4 u-px-6 u-text-right">
        <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">
          Total Validated Signatures: {{ logs.length }}
        </span>
      </footer>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../../services/api';

const logs = ref([]);
const searchQuery = ref('');
const userFilter = ref('');
const actionFilter = ref('');

const fetchLogs = async () => {
  try {
    const response = await api.get('/audit-logs/');
    logs.value = response.data;
  } catch (e) {
    console.error("Failed to fetch audit logs", e);
  }
};

const formatTimestamp = (ts) => {
  if (!ts) return 'N/A';
  const date = new Date(ts);
  return date.toLocaleString();
};

const getActorColor = (actor) => {
  if (!actor) return 'avatar--indigo';
  if (actor.role === 'Admin') return 'avatar--primary';
  if (actor.role === 'Supervisor') return 'avatar--success';
  return 'avatar--indigo';
};

const actionBadgeClass = (action) => {
  if (action?.includes('ESCALATED')) return 'badge--warning';
  if (action?.includes('COMPLETED')) return 'badge--success';
  if (action?.includes('ACKNOWLEDGED')) return 'badge--info';
  if (action?.includes('REGISTERED')) return 'badge--primary';
  return 'badge--secondary';
};

const filteredLogs = computed(() => {
  let result = logs.value;

  if (userFilter.value) {
    const u = userFilter.value.toLowerCase();
    result = result.filter(l => l.actor?.username?.toLowerCase().includes(u));
  }

  if (actionFilter.value) {
    result = result.filter(l => l.action === actionFilter.value);
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(l => 
      l.details?.toLowerCase().includes(q) || 
      l.service_request?.request_id?.toLowerCase().includes(q) ||
      l.action?.toLowerCase().includes(q)
    );
  }

  return result;
});

onMounted(() => {
  fetchLogs();
});
</script>
