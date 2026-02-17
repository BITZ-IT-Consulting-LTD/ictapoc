<template>
  <div class="u-flex u-flex-col u-gap-8 animate-fade-in">
    <!-- Header with Sync -->
    <header class="u-flex u-justify-between u-items-center">
      <div class="page__title-group">
        <h3 class="u-text-2xl u-font-black u-text-main u-mb-1 u-border-l-4 u-border-slate-800 u-pl-4">
          Authoritative Registries
        </h3>
        <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest">National Digital Masterplan - Official Integrated Registry Nodes</p>
      </div>
      <button @click="fetchData" class="button button--primary button--pill" :disabled="loading">
        <i class="bi bi-arrow-clockwise u-mr-2" :class="{ 'animate-spin': loading }"></i>
        <span>{{ loading ? 'Syncing Records...' : 'Synchronize Node' }}</span>
      </button>
    </header>

    <!-- Domain Tab Bar -->
    <nav class="tab-bar">
      <button v-for="group in groups" :key="group.id" @click="activeGroupId = group.id" 
        class="tab-bar__item" :class="{ 'tab-bar__item--active': activeGroupId === group.id }">
        {{ group.name }}
      </button>
    </nav>

    <!-- Action Bar: Select & Search -->
    <article class="card u-bg-page u-p-6 shadow-sm">
      <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-6">
        <div class="form-group">
          <label class="u-block u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-2 u-tracking-widest">Registry Node Selection</label>
          <div class="toolbar__filter-group u-shadow-none u-border u-border-border-color">
            <i class="bi bi-diagram-3 toolbar__filter-icon"></i>
            <select v-model="activeRegistryId" class="toolbar__filter-input u-w-full">
              <option v-for="reg in availableRegistries" :key="reg.key" :value="reg.key">
                {{ reg.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label class="u-block u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-2 u-tracking-widest">Identity / Content Filter</label>
          <div class="toolbar__filter-group u-shadow-none u-border u-border-border-color">
            <i class="bi bi-search toolbar__filter-icon"></i>
            <input type="text" v-model="searchQuery" :placeholder="`Search ${activeRegistryId} database...`" class="toolbar__filter-input u-w-full" />
          </div>
        </div>
      </div>
    </article>

    <!-- Data State -->
    <div v-if="loading" class="u-py-24 u-text-center">
      <i class="bi bi-arrow-clockwise u-text-4xl u-text-primary animate-spin"></i>
      <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest u-mt-4">Establishing Secure Node Handshake...</p>
    </div>

    <div v-else-if="registryData" class="u-flex u-flex-col u-gap-6">
      <article v-if="filteredRecords.length > 0" class="card shadow-lg overflow-hidden">
        <header class="card__header u-bg-page u-flex u-justify-between u-items-center u-px-6 u-py-4">
          <div class="u-flex u-items-center u-gap-3">
            <span class="badge badge--primary">{{ activeRegistryId }}</span>
            <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-tighter">{{ activeRegistryLabel }}</h4>
          </div>
          <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">{{ filteredRecords.length }} Matches Signatures Found</span>
        </header>

        <div class="table-container">
          <table class="table">
            <thead>
              <tr class="table__header-row u-bg-slate-800">
                <th class="table__header-cell u-text-white u-pl-6">Identity Reference</th>
                <th class="table__header-cell u-text-white">Attributes & Authoritative Metadata</th>
                <th class="table__header-cell u-text-white u-text-right u-pr-6">Auth Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredRecords" :key="item.id" class="table__row">
                <td class="table__cell u-pl-6">
                  <span class="table__code-badge u-text-main font-mono">ID: {{ item.id }}</span>
                </td>
                <td class="table__cell">
                  <div class="u-text-xs u-font-black u-text-main u-mb-1">{{ item.name || 'Authoritative Record' }}</div>
                  <div class="u-flex u-flex-wrap u-gap-4">
                    <span v-for="(val, k) in item.meta" :key="k" class="u-text-[10px] u-font-bold u-text-muted">
                      <span class="u-text-primary u-uppercase u-mr-1">{{ k }}:</span>
                      <span class="u-text-main">{{ val }}</span>
                    </span>
                  </div>
                </td>
                <td class="table__cell u-text-right u-pr-6">
                  <span class="badge badge--small" :class="getStatusBadgeClass(item.status)">
                    {{ item.status || 'VERIFIED' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>

      <!-- Empty State -->
      <article v-else class="card u-py-20 u-text-center shadow-sm u-border-dashed u-border-2">
        <div class="u-flex u-flex-col u-items-center u-gap-3">
            <span class="u-text-4xl u-opacity-30">📁</span>
            <h4 class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest">Registry Query Returned Null</h4>
            <p class="u-text-xs u-text-muted u-max-w-xs u-mx-auto">
              No authoritative records found matching "{{ searchQuery }}" within the current {{ activeRegistryId }} partition.
            </p>
            <button @click="searchQuery = ''" class="button button--ghost button--small u-mt-2">Clear Parameters</button>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '../../services/api';

const loading = ref(false);
const registryData = ref(null);
const activeGroupId = ref('identity');
const activeRegistryId = ref('');
const searchQuery = ref('');

const groups = [
  { id: 'identity', name: 'Identity & Civil' },
  { id: 'business', name: 'Business & Entities' },
  { id: 'assets', name: 'Land & Assets' },
  { id: 'transport', name: 'Transport' },
  { id: 'education', name: 'Education & Prof' },
  { id: 'social', name: 'Social Services' },
  { id: 'other', name: 'Legal & Record' }
];

const groupMapping = {
  identity: [
    { key: 'IPRS', label: 'Integrated Population Registration System' },
    { key: 'NRB', label: 'National Registration Bureau (ID)' },
    { key: 'CRS', label: 'Civil Registration (Birth/Death)' },
    { key: 'IMMIGRATION', label: 'Department of Immigration' }
  ],
  business: [
    { key: 'BRS', label: 'Business Registration Service' },
    { key: 'KRA', label: 'Kenya Revenue Authority (KRA)' },
    { key: 'NGO_BOARD', label: 'NGO Coordination Board' }
  ],
  assets: [
    { key: 'ARDHISASA', label: 'Ardhisasa Land IMS' },
    { key: 'COLLATERAL', label: 'Collateral Registry' }
  ],
  transport: [
    { key: 'NTSA', label: 'National Transport Authority' },
    { key: 'KCAA', label: 'Civil Aviation Authority' }
  ],
  education: [
    { key: 'NEMIS', label: 'Education Management (NEMIS)' },
    { key: 'PROFESSIONAL_BODIES', label: 'Professional Bodies Registers' }
  ],
  social: [
    { key: 'SOCIAL_PROTECTION', label: 'Single Registry (Inua Jamii)' },
    { key: 'SHA', label: 'Social Health Authority' },
    { key: 'NSSF', label: 'National Social Security Fund' }
  ],
  other: [
    { key: 'JUDICIARY', label: 'Case Tracking System (CTS)' },
    { key: 'GAZETTE', label: 'The Kenya Gazette' },
    { key: 'IEBC', label: 'Independent Electoral Commission' }
  ]
};

const availableRegistries = computed(() => groupMapping[activeGroupId.value] || []);
const activeRegistryLabel = computed(() => availableRegistries.value.find(r => r.key === activeRegistryId.value)?.label || 'Registry');

watch(activeGroupId, (newVal) => {
  searchQuery.value = '';
  const firstReg = groupMapping[newVal]?.[0];
  if (firstReg) {
    activeRegistryId.value = firstReg.key;
  }
}, { immediate: true });

const filteredRecords = computed(() => {
  if (!registryData.value || !activeRegistryId.value) return [];
  const raw = registryData.value[activeRegistryId.value] || {};
  let list = [];

  Object.keys(raw).forEach(attrName => {
    const set = raw[attrName];
    if (typeof set === 'object') {
      Object.keys(set).forEach(id => {
        const entry = set[id];
        const meta = { ...entry };
        delete meta.full_name;
        delete meta.name;
        delete meta.title;
        delete meta.status;

        list.push({
          id,
          name: entry.name || entry.full_name || entry.title,
          status: entry.status,
          meta
        });
      });
    }
  });

  if (!searchQuery.value) return list;
  const q = searchQuery.value.toLowerCase();
  return list.filter(item =>
    item.id.toLowerCase().includes(q) ||
    item.name?.toLowerCase().includes(q) ||
    Object.values(item.meta).some(v => String(v).toLowerCase().includes(q))
  );
});

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge--success';
  const s = status.toUpperCase();
  const patterns = {
    success: ['ACTIVE', 'ALIVE', 'COMPLIANT', 'VALID', 'PRACTICING', 'REGISTERED', 'ISSUED', 'ADMITTED', 'PUBLISHED', 'CLEAN', 'CONTRIBUTING', 'AIRWORTHY'],
    warning: ['PENDING', 'SUSPENDED', 'EXPIRED', 'CHARGED', 'NON_COMPLIANT', 'ARREARS'],
  };
  
  if (patterns.success.some(w => s.includes(w))) return 'badge--success';
  if (patterns.warning.some(w => s.includes(w))) return 'badge--warning';
  return 'badge--danger';
};

const fetchData = async () => {
  loading.value = true;
  try {
    const response = await api.get('/registry/query/');
    registryData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch registry data:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>

<style scoped>
/* Scoped styles removed in favor of canonical BEM design system */
</style>
