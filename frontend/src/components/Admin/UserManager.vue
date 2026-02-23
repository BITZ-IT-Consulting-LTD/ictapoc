<template>
  <section class="page user-manager">
    <header class="page__header flex-col md:flex-row gap-4 items-start md:items-center">
      <div class="page__title-group">
        <h1 class="page__title">User Management</h1>
        <p class="page__subtitle">Control system access and assign institutional roles</p>
      </div>
      <div class="page__actions ms-auto">
        <button @click="openCreateModal"
          class="button button--primary button--pill shadow-lg hover:shadow-xl transition-all">
          <i class="bi bi-person-plus-fill me-2"></i> Provision User
        </button>
      </div>
    </header>

    <div class="toolbar mb-8">
      <div class="flex flex-wrap gap-4 w-full">
        <!-- Search Users -->
        <div class="relative flex-1 min-w-[250px]">
          <i class="bi bi-search absolute left-4 top-1/2 -translate-y-1/2 text-muted"></i>
          <input type="text" v-model="searchQuery" placeholder="Search users by name, email or ID..."
            class="form__input pl-12 w-full">
        </div>

        <!-- Role Filter -->
        <div class="relative flex-1 min-w-[200px]">
          <i class="bi bi-shield-check absolute left-4 top-1/2 -translate-y-1/2 text-muted"></i>
          <input type="text" v-model="roleSearchLocal" placeholder="Filter by System Role..."
            @focus="showRoleDropdown = true" @blur="setTimeout(() => showRoleDropdown = false, 200)"
            class="form__input pl-12 pr-10 w-full cursor-pointer">
          <i class="bi bi-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-muted transition-transform"
            :class="{ 'rotate-180': showRoleDropdown }"></i>

          <div v-if="showRoleDropdown"
            class="absolute top-full left-0 w-full bg-white border border-border-color shadow-xl rounded-xl mt-2 z-50 max-h-60 overflow-y-auto p-2">
            <div @click="selectRole('')"
              class="p-3 hover:bg-bg-page rounded-lg cursor-pointer font-bold text-primary mb-1">
              All Roles
            </div>
            <div v-for="role in filteredRoles" :key="role.id" @click="selectRole(role)"
              class="p-3 hover:bg-bg-page rounded-lg cursor-pointer flex items-center gap-3 text-sm font-medium transition-colors">
              <i class="bi bi-shield-check text-muted"></i> {{ role.name }}
            </div>
          </div>
        </div>

        <!-- MDA Filter -->
        <div class="relative flex-1 min-w-[250px]">
          <i class="bi bi-building absolute left-4 top-1/2 -translate-y-1/2 text-muted"></i>
          <input type="text" v-model="mdaFilterSearchLocal" placeholder="Filter by Institution (MDA)..."
            @focus="showMdaFilterDropdown = true" @blur="setTimeout(() => showMdaFilterDropdown = false, 200)"
            class="form__input pl-12 pr-10 w-full cursor-pointer">
          <i class="bi bi-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-muted transition-transform"
            :class="{ 'rotate-180': showMdaFilterDropdown }"></i>

          <div v-if="showMdaFilterDropdown"
            class="absolute top-full left-0 w-full bg-white border border-border-color shadow-xl rounded-xl mt-2 z-50 max-h-60 overflow-y-auto p-2">
            <div @click="selectMdaFilter('')"
              class="p-3 hover:bg-bg-page rounded-lg cursor-pointer font-bold text-primary mb-1">
              All Institutions
            </div>
            <div @click="selectMdaFilter(null)"
              class="p-3 hover:bg-bg-page rounded-lg cursor-pointer flex items-center gap-3 text-sm font-medium transition-colors text-indigo-600 bg-indigo-50/50 mb-1">
              <i class="bi bi-globe"></i> Global / Common Pool
            </div>
            <div v-for="mda in filteredMdasForFilter" :key="mda.id" @click="selectMdaFilter(mda)"
              class="p-3 hover:bg-bg-page rounded-lg cursor-pointer flex items-center gap-3 text-sm font-medium transition-colors">
              <i class="bi bi-building text-muted"></i> {{ mda.name }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Table -->
    <div class="card border-0 shadow-lg overflow-hidden">
      <div class="table-container rounded-none border-0">
        <table class="table">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="table__th pl-8 text-xs uppercase tracking-widest text-muted font-bold">User Profile</th>
              <th class="table__th text-xs uppercase tracking-widest text-muted font-bold">Account Type</th>
              <th class="table__th text-xs uppercase tracking-widest text-muted font-bold">Institutional Authority</th>
              <th class="table__th text-xs uppercase tracking-widest text-muted font-bold">Status</th>
              <th class="table__th text-right pr-8 text-xs uppercase tracking-widest text-muted font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in filteredUsers" :key="u.id" class="table__row group hover:bg-blue-50/50 transition-colors">
              <td class="table__td pl-8">
                <div class="flex items-center gap-4">
                  <div class="avatar avatar--sm avatar--primary font-bold shadow-sm">
                    {{ u.username.charAt(0).toUpperCase() }}
                  </div>
                  <div class="flex flex-col">
                    <span class="font-bold text-main group-hover:text-primary transition-colors">{{ u.username }}</span>
                    <span class="text-xs text-muted font-mono">{{ u.email }}</span>
                  </div>
                </div>
              </td>
              <td class="table__td">
                <span class="badge badge--small font-mono uppercase tracking-wider"
                  :class="getRoleBadgeClass(u.role)">{{ u.role }}</span>
              </td>
              <td class="table__td">
                <span v-if="u.mda" class="flex items-center gap-2 text-sm text-main">
                  <i class="bi bi-building text-muted"></i> {{ getMdaName(u.mda) }}
                </span>
                <span v-else
                  class="flex items-center gap-2 text-sm text-indigo-600 font-medium bg-indigo-50 px-2 py-1 rounded w-max">
                  <i class="bi bi-globe"></i> Global Access
                </span>
              </td>
              <td class="table__td">
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                  <span class="text-sm font-bold text-emerald-700">Active</span>
                </div>
              </td>
              <td class="table__td text-right pr-8">
                <div class="flex justify-end gap-2 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="openEditModal(u)"
                    class="button button--secondary button--small hover:border-primary hover:text-primary transition-colors"
                    title="Edit Profile">
                    <i class="bi bi-pencil-square me-1"></i> Edit
                  </button>
                  <button @click="deleteUser(u.id)"
                    class="button button--ghost button--small text-danger hover:bg-red-50 hover:text-red-600 transition-colors"
                    title="Revoke Access">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredUsers.length === 0">
              <td colspan="5" class="p-12 text-center text-muted italic">
                No users found matching your search criteria
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <BaseModal v-model:show="showModal" :title="modalTitle" :subtitle="modalSubtitle" icon="bi-person-badge">
      <form @submit.prevent="handleSubmit" class="flex flex-col gap-5 w-full">

        <!-- CREATE MODE: Existing Grid Layout -->
        <div class="grid grid--2 gap-5" v-if="!form.id">
          <div class="form__group">
            <label class="form__label">Username</label>
            <div class="relative">
              <i class="bi bi-person absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input v-model="form.username" type="text" class="form__input pl-10" required
                placeholder="Enter username">
            </div>
          </div>
          <div class="form__group">
            <label class="form__label">Email Address</label>
            <div class="relative">
              <i class="bi bi-envelope absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input v-model="form.email" type="email" class="form__input pl-10" required
                placeholder="email@domain.com">
            </div>
          </div>
          <div class="form__group md:col-span-2">
            <label class="form__label">Initial Password</label>
            <div class="relative">
              <i class="bi bi-key absolute left-3 top-1/2 -translate-y-1/2 text-muted"></i>
              <input v-model="form.password" type="password" class="form__input pl-10" required
                placeholder="Secure password">
            </div>
            <p class="form__help mt-1">Must contain at least 8 characters with mixed case and numbers.</p>
          </div>
        </div>

        <!-- EDIT MODE: Refactored Layout -->
        <template v-if="form.id">
          <div class="form__group">
            <div class="alert alert--info flex items-center gap-3">
              <i class="bi bi-info-circle-fill text-xl"></i>
              <span>Modifying access assignments for <strong>{{ form.username }}</strong></span>
            </div>
          </div>

          <div class="flex flex-col md:flex-row gap-5 pt-4 border-t border-border-color">
            <div class="form__group flex-1">
              <label class="form__label">System Role</label>
              <select v-model="form.user_role_id" class="form__select w-full">
                <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
              </select>
            </div>

            <div class="form__group flex-1">
              <label class="form__label">MDA Authority</label>
              <div class="space-y-2">
                <input type="text" v-model="mdaDropdownSearch" placeholder="Search MDAs..."
                  class="form__input form__input--sm mb-2 w-full">
                <select v-model="form.mda" class="form__select w-full">
                  <option :value="null">Global / Independent</option>
                  <option v-for="mda in filteredMdasForDropdown" :key="mda.id" :value="mda.id">{{ mda.name }} ({{
                    mda.code }})</option>
                </select>
              </div>
              <p class="form__help mt-1">Staff will only see workflows associated with this MDA.</p>
            </div>
          </div>
        </template>

        <!-- FOOTER: Buttons -->
        <div class="flex justify-end gap-3 pt-6 border-t border-border-color mt-2">
          <button type="button" @click="closeModal" class="button button--secondary">Cancel</button>
          <button type="submit"
            class="button button--primary shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            {{ form.id ? 'Save Changes' : 'Create User' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import api from '../../services/api';
  import { useMdaStore } from '../../store/mda';
  import BaseModal from '../Common/BaseModal.vue';

  const mdaStore = useMdaStore();
  const mdas = computed(() => mdaStore.mdas);

  const users = ref([]);
  const roles = ref([]);
  const searchQuery = ref('');
  const roleFilter = ref('');
  const mdaFilter = ref('');

  const roleSearchLocal = ref('');
  const mdaFilterSearchLocal = ref('');
  const showRoleDropdown = ref(false);
  const showMdaFilterDropdown = ref(false);

  const filteredRoles = computed(() => {
    if (!roleSearchLocal.value) return roles.value;
    const q = roleSearchLocal.value.toLowerCase();
    return roles.value.filter(r => r.name.toLowerCase().includes(q));
  });

  const filteredMdasForFilter = computed(() => {
    if (!mdaFilterSearchLocal.value) return mdas.value;
    const q = mdaFilterSearchLocal.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q));
  });

  const selectRole = (role) => {
    if (role === '') {
      roleFilter.value = '';
      roleSearchLocal.value = '';
    } else {
      roleFilter.value = role.id;
      roleSearchLocal.value = role.name;
    }
    showRoleDropdown.value = false;
  };

  const selectMdaFilter = (mda) => {
    if (mda === '') {
      mdaFilter.value = '';
      mdaFilterSearchLocal.value = '';
    } else if (mda === null) {
      mdaFilter.value = null;
      mdaFilterSearchLocal.value = 'Global / Citizen';
    } else {
      mdaFilter.value = mda.id;
      mdaFilterSearchLocal.value = mda.name;
    }
    showMdaFilterDropdown.value = false;
  };

  const filteredUsers = computed(() => {
    let result = users.value;

    if (roleFilter.value) {
      result = result.filter(u => u.user_role === Number(roleFilter.value));
    }

    if (mdaFilter.value !== '') {
      // If user selected "All MDAs", mdaFilter is empty string
      // If user selected "Global / Citizen", mdaFilter is null (from the option value)
      // Otherwise it's the MDA ID
      const filterValue = mdaFilter.value === null ? null : (mdaFilter.value === '' ? undefined : Number(mdaFilter.value));

      if (filterValue !== undefined) {
        result = result.filter(u => u.mda === filterValue);
      }
    }

    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter(u =>
        u.username.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q)
      );
    }

    return result;
  });

  const mdaDropdownSearch = ref('');
  const filteredMdasForDropdown = computed(() => {
    if (!mdaDropdownSearch.value) return mdas.value;
    const q = mdaDropdownSearch.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q) || (m.code && m.code.toLowerCase().includes(q)));
  });
  const showModal = ref(false);
  const form = ref({
    id: null,
    username: '',
    email: '',
    password: '',
    user_role_id: null,
    mda: null,
  });

  const modalTitle = computed(() => form.value.id ? 'Edit User' : 'Create New User');
  const modalSubtitle = computed(() => form.value.id
    ? 'Modify user details and permissions'
    : 'Onboard a new user to the platform'
  );

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users/');
      users.value = response.data;
    } catch (e) {
      console.error("Failed to fetch users", e);
    }
  };

  const fetchRoles = async () => {
    try {
      const response = await api.get('/roles/');
      roles.value = response.data;
    } catch (e) {
      console.error("Failed to fetch roles", e);
    }
  };

  const getMdaName = (mdaId) => {
    if (!mdaId) return 'Global / Citizen';
    const mda = mdas.value.find(m => m.id === mdaId);
    return mda ? `${mda.name} (${mda.code})` : 'Unknown MDA';
  };

  const getRoleBadgeClass = (roleName) => {
    const map = {
      'admin': 'badge--danger',
      'staff': 'badge--primary',
      'citizen': 'badge--secondary'
    };
    return map[roleName?.toLowerCase()] || 'badge--secondary';
  };

  onMounted(() => {
    fetchUsers();
    fetchRoles();
    mdaStore.fetchMdas();
  });

  const openCreateModal = () => {
    form.value = {
      id: null,
      username: '',
      email: '',
      password: '',
      user_role_id: roles.value.length > 0 ? roles.value[0].id : null,
      mda: null,
    };
    showModal.value = true;
  };

  const openEditModal = (u) => {
    form.value = {
      id: u.id,
      username: u.username,
      email: u.email,
      user_role_id: u.user_role || null,
      mda: u.mda || null,
    };
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
  };

  const handleSubmit = async () => {
    try {
      if (form.value.id) {
        await api.patch(`/users/${form.value.id}/`, {
          user_role: form.value.user_role_id,
          mda: form.value.mda
        });
      } else {
        await api.post(`/users/register/`, {
          username: form.value.username,
          email: form.value.email,
          password: form.value.password,
          user_role: form.value.user_role_id,
          mda: form.value.mda,
          role: 'staff' // Default to staff role for admin creation
        });
      }
      await fetchUsers();
      closeModal();
      alert(form.value.id ? "User updated successfully." : "User created successfully.");
    } catch (e) {
      console.error(e);
      alert("Failed to save user: " + (e.response?.data?.message || e.message));
    }
  };

  const deleteUser = async (id) => {
    if (confirm('Are you sure you want to delete this user? This cannot be undone.')) {
      try {
        await api.delete(`/users/${id}/`);
        await fetchUsers();
      } catch (e) {
        alert("Failed to delete user.");
      }
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

  .bg-bg-page {
    background-color: var(--bg-page);
  }

  .border-border-color {
    border-color: var(--border-color);
  }

  .avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;
  }

  .avatar--sm {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 0.9rem;
  }

  .avatar--primary {
    background: var(--primary-soft);
    color: var(--primary);
  }
</style>
