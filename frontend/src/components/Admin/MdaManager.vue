<template>
  <section class="page mda-manager">
    <WogDashboardStats v-if="auditStats" :stats="auditStats" class="mb-8" />

    <header class="page__header flex-col md:flex-row gap-4 items-start md:items-center">
      <div class="page__title-group">
        <h1 class="page__title">Authoritative MDA Registry</h1>
        <p class="page__subtitle">Manage government ministry, department, or agency registration</p>
      </div>
      <div class="page__actions ms-auto">
        <button @click="openCreateModal"
          class="button button--primary button--pill shadow-lg hover:shadow-xl transition-all">
          <i class="bi bi-plus-lg me-2"></i> Create New MDA
        </button>
      </div>
    </header>

    <div class="toolbar mb-8">
      <div class="relative w-full md:w-1/2 lg:w-1/3">
        <i class="bi bi-search absolute left-4 top-1/2 -translate-y-1/2 text-muted"></i>
        <input type="text" v-model="searchQuery" placeholder="Filter MDAs..." class="form__input pl-12 w-full">
      </div>
    </div>

    <!-- MDA List -->
    <div class="card border-0 shadow-lg overflow-hidden">
      <div class="table-container rounded-none border-0">
        <table class="table">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="table__th pl-8 text-xs uppercase tracking-widest text-muted font-bold">Code</th>
              <th class="table__th text-xs uppercase tracking-widest text-muted font-bold">MDA Name</th>
              <th class="table__th text-xs uppercase tracking-widest text-muted font-bold">Priority Status</th>
              <th class="table__th text-xs uppercase tracking-widest text-muted font-bold">Head of MDA</th>
              <th class="table__th text-right pr-8 text-xs uppercase tracking-widest text-muted font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mda in filteredMdas" :key="mda.id"
              class="table__row group hover:bg-blue-50/50 transition-colors">
              <td class="table__td pl-8">
                <span
                  class="font-mono text-xs font-black bg-slate-100 text-slate-700 px-2 py-1 rounded border border-slate-200">
                  {{ mda.code || 'N/A' }}
                </span>
              </td>
              <td class="table__td">
                <div class="flex flex-col">
                  <span class="font-bold text-main group-hover:text-primary transition-colors text-base">{{ mda.name
                  }}</span>
                  <a v-if="mda.website" :href="mda.website" target="_blank"
                    class="text-xs text-primary hover:underline flex items-center gap-1 mt-1">
                    <i class="bi bi-link-45deg"></i> {{ mda.website }}
                  </a>
                </div>
              </td>
              <td class="table__td">
                <span v-if="mda.is_priority" class="badge badge--primary u-flex u-items-center u-gap-1 u-w-fit">
                    <i class="bi bi-star-fill u-text-[8px]"></i> Priority
                </span>
                <span v-else class="text-muted text-xs">Normal</span>
              </td>
              <td class="table__td">
                <div class="flex flex-col">
                  <span class="font-bold text-sm text-main mb-1">{{ mda.head_of_mda || 'N/A' }}</span>
                  <span v-if="mda.contact_email" class="text-xs text-muted flex items-center gap-1">
                    <i class="bi bi-envelope"></i> {{ mda.contact_email }}
                  </span>
                </div>
              </td>
              <td class="table__td text-right pr-8">
                <div class="flex justify-end gap-2 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="openEditModal(mda)"
                    class="button button--secondary button--small hover:border-primary hover:text-primary transition-colors"
                    title="Edit Details">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button @click="deleteMda(mda.id)"
                    class="button button--ghost button--small text-danger hover:bg-red-50 hover:text-red-600 transition-colors"
                    title="Remove MDA">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="mdas.length === 0">
              <td colspan="4" class="p-12 text-center text-muted italic">
                <div class="flex flex-col items-center gap-2">
                  <i class="bi bi-building-add text-4xl text-slate-200"></i>
                  <span>No MDAs found. Create one to get started.</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <BaseModal v-model:show="showModal" :title="form.id ? 'Edit MDA' : 'Create New MDA'"
      subtitle="Manage government ministry, department, or agency registration" icon="bi-building" size="lg">
      <form @submit.prevent="handleSubmit" class="form flex flex-col gap-6">
        <div class="grid grid--2 gap-6">
          <div class="form__group">
            <label class="form__label">MDA Name</label>
            <input type="text" v-model="form.name" class="form__input" required placeholder="e.g. Ministry of Health">
          </div>
          <div class="form__group">
            <label class="form__label">Official Code</label>
            <input type="text" v-model="form.code" class="form__input font-mono" placeholder="e.g. MOH">
          </div>
          <div class="form__group md:col-span-2">
            <label class="form__label">Description</label>
            <textarea v-model="form.description" rows="2" class="form__textarea"
              placeholder="Brief description of responsibilities"></textarea>
          </div>
          <div class="form-group">
            <label class="form__label">Head of MDA</label>
            <div class="relative">
              <i class="bi bi-person-badge absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input type="text" v-model="form.head_of_mda" class="form__input pl-10" placeholder="e.g. CS Health">
            </div>
          </div>
          <div class="form-group">
            <label class="form__label">Contact Email</label>
            <div class="relative">
              <i class="bi bi-envelope absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input type="email" v-model="form.contact_email" class="form__input pl-10"
                placeholder="email@domain.go.ke">
            </div>
          </div>
          <div class="form-group">
            <label class="form__label">Contact Phone</label>
            <div class="relative">
              <i class="bi bi-telephone absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input type="text" v-model="form.contact_phone" class="form__input pl-10" placeholder="+254...">
            </div>
          </div>
          <div class="form-group">
            <label class="form__label">Website URL</label>
            <div class="relative">
              <i class="bi bi-globe absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input type="url" v-model="form.website" class="form__input pl-10" placeholder="https://...">
            </div>
          </div>
          <div class="form__group md:col-span-2">
            <label class="form__label">Physical Address</label>
            <div class="relative">
              <i class="bi bi-geo-alt absolute left-3 top-4 text-muted"></i>
              <textarea v-model="form.address" rows="2" class="form__textarea pl-10"
                placeholder="Building, Street, City"></textarea>
            </div>
          </div>
          <div class="form__group md:col-span-2 mt-2">
            <label class="flex items-center gap-3 cursor-pointer p-4 bg-slate-50 rounded-lg border border-slate-100 hover:bg-white transition-all shadow-sm">
                <input type="checkbox" v-model="form.is_priority" class="w-5 h-5 accent-primary rounded cursor-pointer">
                <div>
                    <span class="font-bold text-main block text-sm">Designate as Priority MDA</span>
                    <span class="text-xs text-muted block italic">Priority MDAs are featured in the whole-of-government service catalogue.</span>
                </div>
            </label>
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t border-border-color mt-4">
          <button type="button" @click="closeModal" class="button button--secondary">Cancel</button>
          <button type="submit"
            class="button button--primary shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <i class="bi bi-check-circle-fill me-2"></i> {{ form.id ? 'Update MDA' : 'Create MDA' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useMdaStore } from '../../store/mda';
  import { useServiceConfigStore } from '../../store/serviceConfig';
  import WogDashboardStats from './WogDashboardStats.vue';
  import BaseModal from '../Common/BaseModal.vue';

  const mdaStore = useMdaStore();
  const serviceConfigStore = useServiceConfigStore();
  const mdas = computed(() => mdaStore.mdas);
  const auditStats = computed(() => serviceConfigStore.catalogueSummary);
  const searchQuery = ref('');

  const filteredMdas = computed(() => {
    if (!searchQuery.value) return mdas.value;
    const q = searchQuery.value.toLowerCase();
    return mdas.value.filter(m =>
      m.name.toLowerCase().includes(q) ||
      (m.code && m.code.toLowerCase().includes(q)) ||
      (m.description && m.description.toLowerCase().includes(q))
    );
  });

  const showModal = ref(false);
  const form = ref({
    id: null,
    name: '',
    code: '',
    description: '',
    head_of_mda: '',
    contact_email: '',
    contact_phone: '',
    website: '',
    address: '',
    is_priority: false,
  });

  onMounted(() => {
    mdaStore.fetchMdas();
    serviceConfigStore.fetchCatalogueSummary();
  });

  const openCreateModal = () => {
    form.value = {
      id: null,
      name: '',
      code: '',
      description: '',
      head_of_mda: '',
      contact_email: '',
      contact_phone: '',
      website: '',
      address: '',
      is_priority: false,
    };
    showModal.value = true;
  };

  const openEditModal = (mda) => {
    form.value = { ...mda };
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
  };

  const handleSubmit = async () => {
    if (form.value.id) {
      await mdaStore.updateMda(form.value);
    } else {
      await mdaStore.createMda(form.value);
    }
    closeModal();
  };

  const deleteMda = async (id) => {
    if (confirm('Are you sure you want to delete this MDA? This action cannot be undone.')) {
      await mdaStore.deleteMda(id);
    }
  };
</script>

<style scoped>
  .text-muted {
    color: var(--text-muted);
  }

  .text-main {
    color: var(--text-main);
  }

  .text-primary {
    color: var(--primary);
  }

  .text-danger {
    color: var(--danger);
  }

  .border-border-color {
    border-color: var(--border-color);
  }

  /* Utilities replacement */
  .relative {
    position: relative;
  }

  .absolute {
    position: absolute;
  }

  .left-3 {
    left: 0.75rem;
  }

  .left-4 {
    left: 1rem;
  }

  .top-1\/2 {
    top: 50%;
  }

  .top-4 {
    top: 1rem;
  }

  .-translate-y-1\/2 {
    transform: translateY(-50%);
  }

  .pl-8 {
    padding-left: 2rem;
  }

  .pl-10 {
    padding-left: 2.5rem;
  }

  .pl-12 {
    padding-left: 3rem;
  }

  .pr-8 {
    padding-right: 2rem;
  }

  .p-12 {
    padding: 3rem;
  }

  .w-full {
    width: 100%;
  }

  .md\:col-span-2 {
    grid-column: span 2;
  }

  .opacity-100 {
    opacity: 1;
  }

  .group:hover .group-hover\:text-primary {
    color: var(--primary);
  }

  .hover\:underline:hover {
    text-decoration: underline;
  }

  .hover\:bg-blue-50\/50:hover {
    background-color: rgba(239, 246, 255, 0.5);
  }

  .hover\:bg-red-50:hover {
    background-color: #fef2f2;
  }

  .hover\:text-red-600:hover {
    color: #dc2626;
  }

  .text-4xl {
    font-size: 2.25rem;
  }

  .text-base {
    font-size: 1rem;
  }

  .font-black {
    font-weight: 900;
  }

  .bg-slate-100 {
    background-color: #f1f5f9;
  }

  .text-slate-700 {
    color: #334155;
  }

  .text-slate-200 {
    color: #e2e8f0;
  }

  .border-slate-200 {
    border-color: #e2e8f0;
  }

  .bg-gray-50 {
    background-color: #f9fafb;
  }

  .border-gray-200 {
    border-color: #e5e7eb;
  }

  @media (min-width: 768px) {
    .md\:opacity-0 {
      opacity: 0;
    }

    .group:hover .group-hover\:opacity-100 {
      opacity: 1;
    }

    .md\:flex-row {
      flex-direction: row;
    }

    .md\:items-center {
      align-items: center;
    }

    .md\:w-1\/2 {
      width: 50%;
    }
  }

  @media (min-width: 1024px) {
    .lg\:w-1\/3 {
      width: 33.333333%;
    }
  }
</style>
