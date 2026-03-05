<template>
  <section class="page role-manager">
    <header class="page__header">
      <div class="page__title-group">
        <h1 class="page__title">Institutional Access Controls</h1>
        <p class="page__subtitle">Manage RBAC policies and governance roles across the national registry</p>
      </div>
      <div class="page__actions">
        <button @click="openCreateModal" class="button button--primary button--pill">
          <i class="bi bi-shield-plus me-1"></i> Provision Role
        </button>
      </div>
    </header>

    <div class="toolbar mb-6">
      <div class="toolbar__group">
        <div class="search search--large">
          <i class="bi bi-search search__icon"></i>
          <input type="text" v-model="searchQuery" placeholder="Search institutional roles..." class="search__input">
        </div>
      </div>
    </div>

    <!-- Role List -->
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th class="table__th">Registry Role</th>
            <th class="table__th">Governance Scope</th>
            <th class="table__th">Policy Assignment</th>
            <th class="table__th text-right">Administrative Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in filteredRoles" :key="role.id" class="table__row">
            <td class="table__td">
              <div class="flex items-center gap-3">
                <div class="avatar-sm bg-slate-100 text-primary">
                  <i class="bi bi-shield-lock-fill"></i>
                </div>
                <div>
                  <div class="font-black text-gray-900">{{ role.name }}</div>
                  <div class="text-[10px] text-gray-400 font-mono">RID-{{ role.id }}</div>
                </div>
              </div>
            </td>
            <td class="table__td">
              <span class="text-xs text-gray-600 line-clamp-1">{{ role.description || 'Global Policy' }}</span>
            </td>
            <td class="table__td">
              <span class="badge badge--secondary badge--small">
                <i class="bi bi-people-fill me-1"></i> {{ role.users ? role.users.length : 0 }} Assigned
              </span>
            </td>
            <td class="table__td text-right">
              <div class="flex justify-end gap-2">
                <button @click="openEditModal(role)" class="button button--secondary button--small p-2"
                  title="Policy Editor">
                  <i class="bi bi-gear-fill"></i>
                </button>
                <button @click="deleteRoleDirect(role.id)"
                  class="button button--ghost button--small p-2 text-red-400 hover:text-red-500" title="Revoke Role">
                  <i class="bi bi-trash-fill"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Role Editor Modal -->
    <BaseModal v-model:show="showModal" :title="form.id ? 'Policy Configuration' : 'Institutional Provisioning'"
      subtitle="Define granular access vectors and cryptographic permissions" icon="bi-shield-lock" size="lg">
      <form @submit.prevent="saveRole" class="form">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="form__group">
            <label class="form__label">Institutional Role Name</label>
            <input v-model="form.name" type="text" class="form__input" required placeholder="e.g. Agency Administrator">
          </div>
          <div class="form__group">
            <label class="form__label">Governance Scope</label>
            <input v-model="form.description" type="text" class="form__input"
              placeholder="Defined operational boundary">
          </div>

          <div class="form__group md:col-span-2">
            <div class="flex justify-between items-end mb-4">
              <div>
                <label class="form__label mb-1">Granular Permission Matrix</label>
                <p class="text-[10px] text-gray-400 uppercase font-black">Cryptographic Access Vectors</p>
              </div>
              <span class="badge badge--primary badge--small">{{ form.permissions.length }} Active Policies</span>
            </div>

            <div class="card card--muted overflow-hidden">
              <div class="p-3 border-b bg-gray-50 flex items-center gap-3">
                <i class="bi bi-search text-gray-400"></i>
                <input type="text" v-model="permSearch" placeholder="Filter permission pool..."
                  class="bg-transparent border-0 text-xs w-full focus:ring-0">
              </div>

              <div class="max-h-[300px] overflow-y-auto p-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <label v-for="perm in filteredPermissions" :key="perm"
                    class="flex items-center gap-3 p-3 rounded-xl border border-transparent transition-all cursor-pointer hover:bg-white hover:border-gray-200"
                    :class="{ 'bg-white border-primary !border-2': form.permissions.includes(perm) }">
                    <input type="checkbox" :value="perm" v-model="form.permissions"
                      class="w-4 h-4 rounded text-primary focus:ring-primary">
                    <span class="text-xs font-bold text-gray-700 uppercase tracking-tighter">{{ perm.replace(/_/g, ' ')
                    }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>

      <template #footer>
        <div class="flex gap-3">
          <button type="button" @click="closeModal" class="button button--secondary">Discard</button>
          <button type="button" @click="saveRole" class="button button--primary">
            {{ form.id ? 'Commit Policy Updates' : 'Provision Governance Role' }}
          </button>
        </div>
      </template>
    </BaseModal>
  </section>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import api from '../services/api';
  import BaseModal from '../components/Common/BaseModal.vue';

  const roles = ref([]);
  const showModal = ref(false);
  const searchQuery = ref('');
  const permSearch = ref('');

  const filteredRoles = computed(() => {
    if (!searchQuery.value) return roles.value;
    const q = searchQuery.value.toLowerCase();
    return roles.value.filter(r => r.name.toLowerCase().includes(q));
  });

  const filteredPermissions = computed(() => {
    if (!permSearch.value) return systemPermissions;
    const q = permSearch.value.toLowerCase();
    return systemPermissions.filter(p => p.toLowerCase().includes(q));
  });

  const systemPermissions = [
    'view_request', 'create_request', 'view_own_request',
    'verify_document', 'approve_request', 'reject_request',
    'issue_certificate', 'view_reports', 'manage_users',
    'manage_roles', 'view_audit_logs', 'archive_record',
    'access_g2g_services', 'manage_mdas', 'manage_services',
    'manage_lifecycle_groups', 'view_priority_mdas',
    'all_mdas.view', 'all_mdas.claim', 'all_mdas.supervise',
    'mda.view', 'mda.claim', 'mda.initiate', 'mda.supervise',
    'global_manage', 'global_view', 'mda_manage_services',
    'request_action', 'request_approve', 'request_create',
    'request_view_own', 'saved_docs_manage',
    'all'
  ];

  const form = ref({
    id: null,
    name: '',
    description: '',
    permissions: []
  });

  const fetchRoles = async () => {
    try {
      const response = await api.get('/roles/');
      roles.value = response.data;
    } catch (e) {
      console.error("Failed to fetch roles", e);
    }
  };

  const openCreateModal = () => {
    form.value = {
      name: '',
      description: '',
      permissions: []
    };
    showModal.value = true;
  };

  const openEditModal = (role) => {
    form.value = { ...role };
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
  };

  const saveRole = async () => {
    try {
      if (form.value.id) {
        await api.put(`/roles/${form.value.id}/`, form.value);
      } else {
        await api.post('/roles/', form.value);
      }
      await fetchRoles();
      closeModal();
      alert("Role saved successfully.");
    } catch (e) {
      console.error(e);
      alert("Failed to save role.");
    }
  };

  const deleteRoleDirect = async (id) => {
    if (!confirm("Delete this role? Users assigned to it may lose access.")) return;
    try {
      await api.delete(`/roles/${id}/`);
      await fetchRoles();
    } catch (e) {
      alert("Failed to delete role.");
    }
  };

  onMounted(() => {
    fetchRoles();
  });
</script>

<style scoped>
  .role-manager {
    padding-top: 2rem;
  }

  .role-manager__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  .role-manager__title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
  }

  .role-manager__controls {
    margin-bottom: 2rem;
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #f1f5f9;
  }

  .search-wrapper {
    position: relative;
    max-width: 400px;
  }

  .search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    font-size: 1rem;
  }

  /* Table Styles */
  .table-container {
    overflow-x: auto;
  }

  .table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 0.75rem;
    margin-top: -0.75rem;
  }

  .table th {
    text-align: left;
    padding: 1rem 1.5rem;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    background: transparent;
    border: none;
  }

  .table tbody tr {
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
  }

  .table tbody tr:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    z-index: 10;
    position: relative;
  }

  .table td {
    padding: 1.25rem 1.5rem;
    border: none;
    vertical-align: middle;
  }

  .table td:first-child {
    border-top-left-radius: 1rem;
    border-bottom-left-radius: 1rem;
  }

  .table td:last-child {
    border-top-right-radius: 1rem;
    border-bottom-right-radius: 1rem;
  }

  .role-name-wrapper {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .role-icon {
    color: #4f46e5;
    font-size: 1.125rem;
  }

  .role-name {
    font-weight: 700;
    color: #0f172a;
    font-size: 0.9375rem;
  }

  .role-description {
    font-size: 0.875rem;
    color: #64748b;
  }

  .user-count-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.25rem 0.625rem;
    background: #f1f5f9;
    color: #475569;
    border-radius: 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
  }

  /* Permission Selector */
  .permission-selector {
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    overflow: hidden;
    background: white;
  }

  .permission-selector__search {
    padding: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
    background: #f8fafc;
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .permission-selector__search i {
    color: #94a3b8;
  }

  .permission-selector__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.5rem;
    padding: 1rem;
    max-height: 300px;
    overflow-y: auto;
  }

  .permission-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid transparent;
  }

  .permission-item:hover {
    background: #f1f5f9;
  }

  .permission-item--selected {
    background: #eef2ff;
    border-color: #c7d2fe;
  }

  .permission-item__checkbox {
    width: 1rem;
    height: 1rem;
    accent-color: #4f46e5;
  }

  .permission-item__label {
    font-size: 0.8125rem;
    color: #475569;
    text-transform: capitalize;
  }

  /* Action Buttons */
  .action-buttons {
    display: flex;
    gap: 0.5rem;
    justify-content: flex-end;
  }

  .btn-icon {
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    background: #f1f5f9;
    color: #64748b;
  }

  .btn-icon--primary:hover {
    background: #eef2ff;
    color: #4f46e5;
  }

  .btn-icon--danger:hover {
    background: #fff1f2;
    color: #e11d48;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .form-group--full {
    grid-column: 1 / -1;
  }

  @media (min-width: 768px) {
    .form-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
