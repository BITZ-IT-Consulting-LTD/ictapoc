<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Dashboard</h1>
    <div v-if="user">
      <div class="flex justify-between items-center mb-6">
        <p class="text-gray-600">Welcome, {{ user.username }}! Your role is: {{ user.role }}</p>
        <router-link to="/profile"
          class="text-indigo-600 hover:text-indigo-800 font-semibold border border-indigo-200 px-4 py-2 rounded hover:bg-indigo-50">
          Manage Profile / Documents
        </router-link>
      </div>

      <!-- Citizen Specific Tabbed View -->
      <div v-if="user.role === 'citizen'" class="space-y-6">
        <!-- Tab Navigation -->
        <div class="flex border-b border-gray-200">
          <button @click="citizenCurrentTab = 'inbox'"
            :class="[citizenCurrentTab === 'inbox' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'flex-1 py-4 px-1 border-b-2 font-bold text-center transition-all']">
            <div class="flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              My Inbox
            </div>
          </button>
          <button @click="citizenCurrentTab = 'services'"
            :class="[citizenCurrentTab === 'services' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'flex-1 py-4 px-1 border-b-2 font-bold text-center transition-all']">
            <div class="flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              Available Services
            </div>
          </button>
        </div>

        <!-- Tab 1: Inbox content -->
        <div v-if="citizenCurrentTab === 'inbox'" class="space-y-6 animate-in fade-in duration-500">
          <!-- Citizen Wallet Snapshot (Only in Inbox) -->
          <div v-if="user.saved_documents?.length"
            class="bg-indigo-900 text-white p-6 rounded-2xl shadow-xl overflow-hidden relative">
            <div class="absolute -right-12 -top-12 w-48 h-48 bg-indigo-800 rounded-full opacity-50"></div>
            <div class="relative z-10 flex flex-col md:flex-row justify-between items-center gap-6">
              <div>
                <h2 class="text-2xl font-bold mb-1">Your Digital ID Wallet</h2>
                <p class="text-indigo-200 text-sm">You have {{ user.saved_documents.length }} authoritative documents
                  issued.</p>
              </div>
              <div class="flex -space-x-3">
                <div v-for="(doc, i) in user.saved_documents.slice(0, 3)" :key="i"
                  class="w-12 h-12 bg-white rounded-xl border-2 border-indigo-900 flex items-center justify-center shadow-lg transform hover:-translate-y-1 transition-transform">
                  <svg v-if="doc.type === 'AUTHORITATIVE_OUTPUT'" class="w-6 h-6 text-indigo-600" fill="none"
                    stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <svg v-else class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
              </div>
              <router-link to="/profile"
                class="px-6 py-2 bg-white text-indigo-900 rounded-xl font-bold hover:bg-indigo-50 transition-colors shadow-lg shadow-indigo-950/20">
                Open Wallet
              </router-link>
            </div>
          </div>

          <div class="space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <h2 class="text-2xl font-bold text-gray-900">Recent Service Applications</h2>
              <div class="flex gap-4 max-w-xl w-full">
                <input type="text" v-model="requestSearchQuery" placeholder="Search applications..."
                  class="flex-1 px-4 py-2 bg-white border border-gray-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all">
                <select v-model="myRequestsStatusFilter"
                  class="w-40 px-4 py-2 bg-white border border-gray-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 transition-all outline-none">
                  <option value="">All Statuses</option>
                  <option value="received">Received</option>
                  <option value="in_progress">In Progress</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            </div>

            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              <p v-if="filteredMyRequests.length === 0" class="p-12 text-center text-gray-400 italic">No applications
                found in your history.</p>
              <ul class="divide-y divide-gray-50">
                <li v-for="request in filteredMyRequests" :key="request.id" class="hover:bg-gray-50 transition-colors">
                  <router-link :to="`/service-request/${request.id}`"
                    class="block p-5 flex justify-between items-center">
                    <div class="flex items-center gap-4">
                      <div
                        class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center font-bold">
                        {{ request.service_config.service_name.charAt(0) }}
                      </div>
                      <div>
                        <div class="font-bold text-gray-900">{{ request.service_config.service_name }}</div>
                        <div class="text-xs text-gray-500 font-mono tracking-tighter">REF: {{ request.request_id }} • {{
                          new Date(request.created_at).toLocaleDateString() }}</div>
                      </div>
                    </div>
                    <div class="flex items-center gap-4">
                      <span
                        class="hidden md:inline-block px-3 py-1 text-[10px] font-black rounded-full uppercase tracking-widest border"
                        :class="statusClass(request.status)">
                        {{ request.status.replace('_', ' ') }}
                      </span>
                      <svg class="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Tab 2: Available Services content -->
        <div v-if="citizenCurrentTab === 'services'" class="space-y-6 animate-in slide-in-from-right-4 duration-500">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2
                class="text-2xl font-bold text-gray-900 text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
                Explore Government Services</h2>
              <p class="text-sm text-gray-500">Apply for various permits, licenses, and certificates digitally.</p>
            </div>
            <div class="relative max-w-sm w-full">
              <input type="text" v-model="serviceSearchQuery"
                placeholder="Search services (e.g. Identity, Education)..."
                class="block w-full px-4 py-3 bg-white border border-gray-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all pl-10">
              <svg class="w-5 h-5 text-gray-400 absolute left-3 top-3.5" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <!-- Services Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="service in filteredAvailableServices" :key="service.id"
              class="group bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl hover:border-indigo-200 transition-all transform hover:-translate-y-1">
              <div
                class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-lg flex items-center justify-center mb-4 font-bold group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="font-bold text-gray-900 mb-1 leading-tight">{{ service.service_name }}</h3>
              <p class="text-xs font-bold text-indigo-600 uppercase tracking-widest mb-4">{{
                getMdaName(service.mda).split('(')[0] }}</p>
              <router-link :to="`/apply/${service.service_code}`"
                class="flex items-center justify-center w-full px-4 py-2 bg-gray-50 text-indigo-600 rounded-xl font-bold hover:bg-indigo-600 hover:text-white transition-all">
                Start Application
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Officer/Supervisor/Other Staff View (Original List Layout) -->
      <div v-else-if="['officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(user.role)" class="space-y-8">
        <div>
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <h2 class="text-2xl font-semibold">Catalogue Monitor</h2>
            <div class="relative max-w-sm w-full">
              <input type="text" v-model="serviceSearchQuery" placeholder="Search services..."
                class="block w-full px-3 py-2 border border-gray-300 rounded-md">
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div v-for="service in filteredAvailableServices.slice(0, 6)" :key="service.id"
              class="bg-gray-50 border border-gray-200 p-4 rounded-lg">
              <h3 class="font-bold text-sm">{{ service.service_name }}</h3>
              <p class="text-[10px] text-gray-500">{{ getMdaName(service.mda) }}</p>
            </div>
          </div>
        </div>
        <div>
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <h2 class="text-2xl font-semibold">User Requests Monitor</h2>
            <div class="flex gap-4 max-w-xl w-full">
              <input type="text" v-model="requestSearchQuery" placeholder="Search requests..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md">
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <ul>
              <li v-for="request in filteredMyRequests.slice(0, 10)" :key="request.id" class="border-b">
                <router-link :to="`/service-request/${request.id}`"
                  class="block py-2 flex justify-between items-center">
                  <span class="text-sm font-medium">{{ request.service_config.service_name }} ({{ request.request_id
                    }})</span>
                  <span class="px-2 py-0.5 text-[10px] rounded-full uppercase" :class="statusClass(request.status)">{{
                    request.status }}</span>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Supervisor Reports -->
      <div v-if="['supervisor', 'GLOBAL_SUPERVISOR', 'MDA_SUPERVISOR', 'mda_admin'].includes(user.role)" class="mt-8">
        <h2 class="text-2xl font-semibold mb-4">System Reports</h2>
        <ReportsDashboard />
      </div>

      <!-- Work Queue (Officer, Supervisor, Registrar, MDA Admin) -->
      <div v-if="['officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(user.role)" class="space-y-8 mt-8">

        <!-- Section 1: My Active Tasks (Individual Accountability) -->
        <div class="bg-white border border-indigo-200 p-6 rounded-xl shadow-md">
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <div>
              <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <span class="w-3 h-3 bg-indigo-600 rounded-full animate-pulse"></span>
                My Active Tasks
              </h2>
              <p class="text-sm text-gray-600">Documents currently assigned to you for processing.</p>
            </div>
            <div class="flex gap-4 max-w-sm w-full">
              <input type="text" v-model="queueSearchQuery" placeholder="Search my tasks..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            </div>
          </div>

          <div class="space-y-4">
            <div v-for="request in filteredAssignedRequests" :key="request.id"
              class="bg-indigo-50/30 border border-indigo-100 rounded-lg p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:border-indigo-300 transition-all">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <span class="font-bold text-gray-900">{{ request.service_config.service_name }}</span>
                  <span class="text-xs font-mono bg-white px-2 py-0.5 rounded border border-gray-200">{{
                    request.request_id }}</span>
                </div>
                <div class="text-sm text-gray-600 flex flex-wrap gap-x-4">
                  <span>Step: <span class="font-medium">{{ request.current_step?.step_name || 'N/A' }}</span></span>
                  <span>Status: <span class="px-2 py-0.5 text-[10px] font-bold rounded-full uppercase tracking-wider"
                      :class="statusClass(request.status)">{{ request.status }}</span></span>
                </div>
              </div>
              <div class="flex items-center gap-2 w-full md:w-auto">
                <button @click="openCompleteStepModal(request)"
                  class="flex-1 md:flex-none px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 shadow-sm transition-colors">
                  Process Step
                </button>
                <button @click="releaseTask(request.id)"
                  class="px-4 py-2 bg-white text-gray-600 border border-gray-300 rounded-lg text-sm font-semibold hover:bg-gray-50 transition-colors"
                  title="Release back to pool">
                  Release
                </button>
                <button @click="escalateRequest(request.id)"
                  class="px-4 py-2 bg-rose-50 text-rose-600 border border-rose-200 rounded-lg text-sm font-semibold hover:bg-rose-100 transition-colors">
                  Escalate
                </button>
              </div>
            </div>
            <div v-if="filteredAssignedRequests.length === 0"
              class="py-12 text-center bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
              <p class="text-gray-400 italic">You have no active tasks. Claim one from the pool below!</p>
            </div>
          </div>
        </div>

        <!-- Section 2: Unassigned Task Pool (Role Inbox) -->
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-xl shadow-sm">
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <div>
              <h2 class="text-2xl font-bold text-slate-900">Task Pool (Unassigned)</h2>
              <p class="text-sm text-slate-600">Requests waiting for an officer to claim and process.</p>
            </div>
            <div class="flex gap-4 max-w-sm w-full">
              <input type="text" v-model="unassignedSearchQuery" placeholder="Find tasks in pool..."
                class="flex-1 px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:ring-slate-500 focus:border-slate-500 sm:text-sm">
            </div>
          </div>

          <div class="bg-white overflow-hidden rounded-lg border border-slate-200 shadow-sm">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-slate-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Service</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Request ID</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Applicant</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Wait Time</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-slate-500 uppercase">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="request in filteredUnassignedRequests" :key="request.id"
                  class="hover:bg-slate-50 transition-colors">
                  <td class="px-4 py-3">
                    <div class="text-sm font-semibold text-slate-900">{{ request.service_config.service_name }}</div>
                    <div class="text-xs text-slate-500">{{ request.current_step?.step_name }}</div>
                  </td>
                  <td class="px-4 py-3 text-sm text-slate-500 font-mono">{{ request.request_id }}</td>
                  <td class="px-4 py-3 text-sm text-slate-600 font-medium">
                    {{ request.citizen_details?.username || 'Unknown' }}
                  </td>
                  <td class="px-4 py-3 text-sm text-slate-500 italic">
                    {{ new Date(request.created_at).toLocaleDateString() }}
                  </td>
                  <td class="px-4 py-3 text-right">
                    <div class="flex justify-end gap-2">
                      <router-link :to="`/service-request/${request.id}`"
                        class="text-slate-400 hover:text-slate-600 text-sm">Preview</router-link>
                      <button @click="claimTask(request.id)"
                        class="px-3 py-1 bg-white border border-indigo-600 text-indigo-600 rounded-md text-xs font-bold hover:bg-indigo-600 hover:text-white transition-all">
                        Claim & Process
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredUnassignedRequests.length === 0">
                  <td colspan="4" class="px-4 py-12 text-center text-slate-400 italic font-medium bg-slate-50/50">
                    The pool is empty! Great job.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Section 3: Departmental Visibility (Monitor All) -->
        <div
          class="bg-gray-50 border border-gray-200 p-6 rounded-xl shadow-sm opacity-90 transition-opacity hover:opacity-100">
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <div>
              <h2 class="text-xl font-bold text-gray-700">All Department Documents</h2>
              <p class="text-xs text-gray-500 text-indigo-600">Full visibility for MDA oversight.</p>
            </div>
            <div class="flex gap-4 max-w-sm w-full">
              <input type="text" v-model="incompleteSearchQuery" placeholder="Search all..."
                class="flex-1 px-3 py-1.5 border border-gray-300 rounded-md text-sm">
            </div>
          </div>
          <div class="bg-white overflow-hidden rounded-lg border border-gray-200">
            <table class="min-w-full divide-y divide-gray-100">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase">Service</th>
                  <th class="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase">Officer</th>
                  <th class="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase">Status</th>
                  <th class="px-4 py-2 text-right text-[10px] font-bold text-gray-400 uppercase">View</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="request in filteredIncompleteRequests" :key="request.id" class="hover:bg-gray-50/50">
                  <td class="px-4 py-2 text-xs font-medium text-gray-900">{{ request.service_config.service_name }}</td>
                  <td class="px-4 py-2 text-xs text-gray-500">
                    <span v-if="request.assigned_to" class="flex items-center gap-1">
                      <span class="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                      {{ request.assigned_to_details?.username || 'Officer' }}
                    </span>
                    <span v-else class="text-gray-300 italic">Unassigned</span>
                  </td>
                  <td class="px-4 py-2">
                    <span class="px-2 py-0.5 text-[9px] font-bold rounded-full uppercase tracking-tighter"
                      :class="statusClass(request.status)">
                      {{ request.status }}
                    </span>
                  </td>
                  <td class="px-4 py-2 text-right">
                    <router-link :to="`/service-request/${request.id}`"
                      class="text-indigo-400 hover:text-indigo-600">&rarr;</router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Section 4: Communication (Inter-Dept Memos) -->
        <div class="bg-indigo-50/50 border border-slate-200 p-6 rounded-xl shadow-sm">
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <div>
              <h2 class="text-2xl font-bold text-slate-900 flex items-center gap-2">
                <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                  </path>
                </svg>
                Inter-Departmental Correspondence
              </h2>
              <p class="text-sm text-slate-600">Secure memos between different Ministries and Departments.</p>
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-inner border border-slate-200 p-4">
            <InterDepartmentalMemoView />
          </div>
        </div>

      </div>

      <!-- Admin View -->
      <div v-if="user.role === 'admin'" class="space-y-8">
        <div>
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8" aria-label="Tabs">
              <button v-for="tab in adminTabs" :key="tab.name" @click="currentTab = tab.name"
                :class="[currentTab === tab.name ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm']">
                {{ tab.name }}
              </button>
            </nav>
          </div>

          <div class="mt-8">
            <div v-if="currentTab === 'MDAs'">
              <MdaManager />
            </div>
            <div v-if="currentTab === 'Services'">
              <ServiceConfigManager />
            </div>
            <div v-if="currentTab === 'Users'">
              <UserManager />
            </div>
            <div v-if="currentTab === 'Reports'">
              <ReportsDashboard />
            </div>
            <div v-if="currentTab === 'Roles'">
              <AdminRolesView />
            </div>
            <div v-if="currentTab === 'API Docs'">
              <ApiRegistry />
            </div>
            <div v-if="currentTab === 'Audit Logs'">
              <AuditLogManager />
            </div>
            <div v-if="currentTab === 'System Health'">
              <SystemHealthView />
            </div>
            <div v-if="currentTab === 'Security & Trust'">
              <SecurityTrustView />
            </div>
            <div v-if="currentTab === 'Architecture Pilot'">
              <ArchitectureSimulator />
            </div>
            <div v-if="currentTab === 'Whole-of-Gov Catalogue'">
              <ServiceCatalogueMatrix />
            </div>
            <div v-if="currentTab === 'Inter-Dept Memos'">
              <InterDepartmentalMemoView />
            </div>
            <div v-if="currentTab === 'System Docs'" class="space-y-4">
              <div class="flex space-x-2 mb-4 overflow-x-auto pb-2">
                <button v-for="doc in availableDocs" :key="doc.file" @click="selectedDoc = doc.file"
                  :class="[selectedDoc === doc.file ? 'bg-indigo-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-100', 'px-4 py-2 rounded-full text-sm font-medium transition-colors border shadow-sm whitespace-nowrap']">
                  {{ doc.name }}
                </button>
              </div>
              <DocViewer :url="`/${selectedDoc}`" />
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Complete Step Modal -->
    <Teleport to="body">
      <div v-if="showCompleteStepModal"
        class="fixed inset-0 z-[9999] overflow-y-auto h-full w-full flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm">
        <div
          class="relative mx-auto p-8 border w-full max-w-md shadow-2xl rounded-2xl bg-white transform transition-all scale-100">
          <div class="mb-6 text-center">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-indigo-50 text-indigo-600 rounded-full mb-4">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 002-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4">
                </path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900">Decision Point</h3>
            <p class="text-sm text-gray-500 mt-1">Please select the authoritative outcome for this document.</p>
          </div>

          <form @submit.prevent="completeStep" class="space-y-5">
            <div>
              <label for="step-action" class="block text-sm font-bold text-gray-700 mb-1">Taxonomy Status
                (Action)</label>
              <select v-model="stepAction.action" id="step-action"
                class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none"
                required>
                <option value="" disabled>Select outcome...</option>
                <option value="approve">Approve / Proceed</option>
                <option value="reject">Reject Application</option>
                <option value="request_changes">Request Modifications</option>
              </select>
            </div>
            <div>
              <label for="step-details" class="block text-sm font-bold text-gray-700 mb-1">Officer's Notes
                (Optional)</label>
              <textarea v-model="stepAction.details" id="step-details" rows="4"
                placeholder="Add justification or specific reasons for your decision..."
                class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none resize-none"></textarea>
            </div>
            <div class="flex flex-col sm:flex-row gap-3 pt-4">
              <button type="submit"
                class="order-last sm:order-first flex-1 px-6 py-3 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Confirm Decision
              </button>
              <button type="button" @click="closeCompleteStepModal"
                class="flex-1 px-6 py-3 bg-white text-gray-600 border border-gray-200 rounded-xl font-bold hover:bg-gray-50 transition-all">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useAuthStore } from '../store/auth';
  import { useCitizenStore } from '../store/citizen';
  import { useMdaStore } from '../store/mda';
  import { useStaffStore } from '../store/staff';
  import { useServiceConfigStore } from '../store/serviceConfig';
  import ReportsDashboard from '../components/Supervisor/ReportsDashboard.vue';
  import MdaManager from '../components/Admin/MdaManager.vue';
  import ServiceConfigManager from '../components/Admin/ServiceConfigManager.vue';
  import WorkflowStepManager from '../components/Admin/WorkflowStepManager.vue';
  import FormSchemaBuilder from '../components/Admin/FormSchemaBuilder.vue';
  import DocViewer from '../components/Admin/DocViewer.vue';
  import AdminRolesView from './AdminRolesView.vue';
  import UserManager from '../components/Admin/UserManager.vue';
  import ApiRegistry from '../components/Admin/ApiRegistry.vue';
  import AuditLogManager from '../components/Admin/AuditLogManager.vue';
  import SystemHealthView from '../components/Admin/SystemHealthView.vue';
  import SecurityTrustView from '../components/Admin/SecurityTrustView.vue';
  import ArchitectureSimulator from '../components/Admin/ArchitectureSimulator.vue';
  import ServiceCatalogueMatrix from '../components/Admin/ServiceCatalogueMatrix.vue';
  import InterDepartmentalMemoView from '../components/Admin/InterDepartmentalMemoView.vue';

  const authStore = useAuthStore();
  const citizenStore = useCitizenStore();
  const mdaStore = useMdaStore();
  const staffStore = useStaffStore();
  const serviceConfigStore = useServiceConfigStore();

  const user = computed(() => authStore.user);
  const availableServices = computed(() => citizenStore.availableServices);
  const myRequests = computed(() => citizenStore.myRequests);
  const mdas = computed(() => mdaStore.mdas);
  const assignedRequests = computed(() => staffStore.assignedRequests);
  const unassignedRequests = computed(() => staffStore.unassignedRequests);
  const teamRequests = computed(() => staffStore.teamRequests);
  const escalatedRequests = computed(() => staffStore.escalatedRequests);

  const showCompleteStepModal = ref(false);
  const currentRequestToComplete = ref(null);
  const stepAction = ref({
    action: '',
    details: '',
  });

  const serviceSearchQuery = ref('');
  const requestSearchQuery = ref('');
  const queueSearchQuery = ref('');
  const unassignedSearchQuery = ref('');
  const incompleteSearchQuery = ref('');
  const myRequestsStatusFilter = ref('');
  const citizenCurrentTab = ref('inbox');
  const queueStatusFilter = ref('');
  const mdaIncompleteRequests = computed(() => staffStore.mdaIncompleteRequests);

  const filteredAvailableServices = computed(() => {
    if (!serviceSearchQuery.value) return availableServices.value;
    const q = serviceSearchQuery.value.toLowerCase();
    return availableServices.value.filter(s =>
      s.service_name.toLowerCase().includes(q) ||
      getMdaName(s.mda).toLowerCase().includes(q)
    );
  });

  const filteredMyRequests = computed(() => {
    let result = myRequests.value;

    if (myRequestsStatusFilter.value) {
      result = result.filter(r => r.status === myRequestsStatusFilter.value);
    }

    if (requestSearchQuery.value) {
      const q = requestSearchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.service_config?.service_name.toLowerCase().includes(q) ||
        r.request_id.toLowerCase().includes(q)
      );
    }
    return result;
  });

  const filteredAssignedRequests = computed(() => {
    let result = assignedRequests.value;

    if (queueStatusFilter.value) {
      result = result.filter(r => r.status === queueStatusFilter.value);
    }

    if (queueSearchQuery.value) {
      const q = queueSearchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.service_config?.service_name.toLowerCase().includes(q) ||
        r.request_id.toLowerCase().includes(q) ||
        r.current_step?.step_name?.toLowerCase().includes(q)
      );
    }
    return result;
  });

  const filteredIncompleteRequests = computed(() => {
    let result = mdaIncompleteRequests.value;
    if (incompleteSearchQuery.value) {
      const q = incompleteSearchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.service_config?.service_name.toLowerCase().includes(q) ||
        r.request_id.toLowerCase().includes(q)
      );
    }
    return result;
  });

  const filteredUnassignedRequests = computed(() => {
    let result = unassignedRequests.value;
    if (unassignedSearchQuery.value) {
      const q = unassignedSearchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.service_config?.service_name.toLowerCase().includes(q) ||
        r.request_id.toLowerCase().includes(q) ||
        r.current_step?.step_name?.toLowerCase().includes(q)
      );
    }
    return result;
  });

  // Admin tabs
  const adminTabs = [
    { name: 'MDAs' },
    { name: 'Services' },
    { name: 'Users' },
    { name: 'Roles' },
    { name: 'Reports' },
    { name: 'API Docs' },
    { name: 'Audit Logs' },
    { name: 'System Health' },
    { name: 'Security & Trust' },
    { name: 'Architecture Pilot' },
    { name: 'Whole-of-Gov Catalogue' },
    { name: 'Inter-Dept Memos' },
    { name: 'System Docs' }
  ];
  const currentTab = ref('Services');

  const availableDocs = [
    { name: 'System Architecture', file: 'architecture_three.md' },
    { name: 'Huduma Bridge Guide', file: 'huduma_bridge_instructions.md' },
    { name: 'Workflow Engine', file: 'poc_algorithm_workflow_documentation.md' },
    { name: 'Project Overview', file: 'poc_project_overview_concept_note.md' },
    { name: 'System Design', file: 'poc_system_design_documents.md' },
    { name: 'Deployment Plan', file: 'poc_deployment_dev_ops_plan.md' },
    { name: 'Actor Roles', file: 'poc_actor_roles_responsibilities.md' },
  ];
  const selectedDoc = ref('architecture_three.md');

  onMounted(async () => {
    const role = user.value?.role;

    // Refresh user data to catch newly issued wallet documents
    if (role === 'citizen') {
      await authStore.fetchCurrentUser();
    }

    // Common data for all dashboard users
    if (['citizen', 'officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(role)) {
      citizenStore.fetchAvailableServices();
      citizenStore.fetchMyRequests();
      mdaStore.fetchMdas();
    }

    // Specific data for staff roles
    if (['officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(role)) {
      staffStore.fetchIncompleteMdaRequests();
      staffStore.fetchUnassignedRequests();
      staffStore.fetchAssignedRequests();

      if (['supervisor', 'GLOBAL_SUPERVISOR', 'MDA_SUPERVISOR', 'mda_admin'].includes(role)) {
        staffStore.fetchTeamRequests();
        staffStore.fetchEscalatedRequests();
      }
    } else if (role === 'admin') {
      // Fetch data needed for all admin tabs
      mdaStore.fetchMdas();
      serviceConfigStore.fetchServices();
    }
  });

  const getMdaName = (mdaId) => {
    const mda = mdas.value.find(m => m.id === mdaId);
    if (!mda) return 'N/A';
    return mda.code ? `${mda.name} (${mda.code})` : mda.name;
  };

  const statusClass = (status) => {
    const classes = {
      received: 'bg-blue-100 text-blue-800',
      in_progress: 'bg-yellow-100 text-yellow-800',
      escalated: 'bg-orange-100 text-orange-800',
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
      closed: 'bg-gray-100 text-gray-800',
      validation_failed: 'bg-red-100 text-red-800',
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
  };

  const openCompleteStepModal = (request) => {
    currentRequestToComplete.value = request;
    showCompleteStepModal.value = true;
    stepAction.value = { action: '', details: '' }; // Reset form
  };

  const closeCompleteStepModal = () => {
    showCompleteStepModal.value = false;
    currentRequestToComplete.value = null;
  };

  const completeStep = async () => {
    if (!currentRequestToComplete.value) return;

    try {
      await staffStore.completeWorkflowStep(
        currentRequestToComplete.value.id,
        stepAction.value.action,
        stepAction.value.details
      );
      closeCompleteStepModal();

      // Global Refresh for all pools to ensure UI keeps sync
      await staffStore.fetchAssignedRequests();
      await staffStore.fetchUnassignedRequests();
      await staffStore.fetchIncompleteMdaRequests();

      if (user.value?.role === 'supervisor') {
        await staffStore.fetchTeamRequests();
        await staffStore.fetchEscalatedRequests();
      }
    } catch (error) {
      alert('Failed to complete step: ' + (error.response?.data?.detail || error.message));
    }
  };

  const escalateRequest = async (requestId) => {
    if (confirm('Are you sure you want to escalate this request?')) {
      try {
        await staffStore.escalateRequest(requestId);
        // Refresh requests for the officer
        staffStore.fetchAssignedRequests();
      } catch (error) {
        alert('Failed to escalate request: ' + error.message);
      }
    }
  };

  const acknowledgeEscalation = async (requestId) => {
    if (confirm('Are you sure you want to acknowledge this escalation? The request will be removed from this list.')) {
      try {
        await staffStore.acknowledgeEscalation(requestId);
      } catch (error) {
        alert('Failed to acknowledge escalation: ' + error.message);
      }
    }
  };

  const claimTask = async (requestId) => {
    try {
      await staffStore.claimTask(requestId);
    } catch (error) {
      alert('Claim failed: ' + (error.response?.data?.detail || error.message));
    }
  };

  const releaseTask = async (requestId) => {
    if (confirm('Are you sure you want to release this task back to the pool?')) {
      try {
        await staffStore.releaseTask(requestId);
      } catch (error) {
        alert('Release failed: ' + (error.response?.data?.detail || error.message));
      }
    }
  };
</script>
