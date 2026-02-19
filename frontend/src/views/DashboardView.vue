<template>
  <div class="dashboard-wrapper">
    <!-- Top Header Bar -->
    <header class="page__header u-mb-8">
      <div class="page__title-group">
        <h1 class="page__title text-premium">National Registry Dashboard</h1>
        <p v-if="user" class="page__subtitle u-flex u-items-center u-gap-3">
          Secure Registry Access for <span class="u-text-primary u-font-bold u-uppercase">{{ user.username }}</span>
          <span class="u-text-muted">|</span>
          <span class="badge badge--info">{{ user.role.toUpperCase() }}</span>
        </p>
      </div>
      <div class="page__actions" v-if="user">
        <router-link to="/profile" class="button button--secondary button--pill button--small">
          <i class="bi bi-person-circle u-mb-1"></i> Authenticated Profile
        </router-link>
      </div>
    </header>

    <div v-if="user" class="dashboard-main">

      <!-- CITIZEN PORTAL VIEW -->
      <section v-if="user.role && user.role.toLowerCase() === 'citizen'" class="citizen-portal">
        <div class="dashboard-layout">
          <!-- Left Sidebar Navigation -->
          <aside class="dashboard-sidebar">
            <div class="card">
              <div class="card__body p-0">
                <nav class="sidebar-nav" aria-label="Citizen portal navigation">
                  <button @click="citizenCurrentTab = 'inbox'" class="sidebar-nav__item"
                    :class="{ 'sidebar-nav__item--active': citizenCurrentTab === 'inbox' }">
                    <i class="bi bi-envelope-paper-fill sidebar-nav__icon"></i>
                    <span class="sidebar-nav__text">Official Inbox</span>
                    <i v-if="citizenCurrentTab === 'inbox'" class="bi bi-chevron-right sidebar-nav__arrow"></i>
                  </button>

                  <button @click="citizenCurrentTab = 'services'" class="sidebar-nav__item"
                    :class="{ 'sidebar-nav__item--active': citizenCurrentTab === 'services' }">
                    <i class="bi bi-grid-3x3-gap-fill sidebar-nav__icon"></i>
                    <span class="sidebar-nav__text">Apply for Services</span>
                    <i v-if="citizenCurrentTab === 'services'" class="bi bi-chevron-right sidebar-nav__arrow"></i>
                  </button>

                  <router-link to="/profile/consent" class="sidebar-nav__item">
                    <i class="bi bi-shield-check sidebar-nav__icon"></i>
                    <span class="sidebar-nav__text">Privacy & Consents</span>
                  </router-link>
                </nav>
              </div>
            </div>
          </aside>

          <!-- Main Content Area -->
          <div class="dashboard-content">
            <div v-if="citizenCurrentTab === 'inbox'" class="tab-content flex flex-col gap-8">
              <!-- Digital Wallet Component -->
              <!-- Digital Wallet Component (Enhanced) -->
              <div v-if="user.saved_documents?.length" class="card border-0 shadow-2xl overflow-hidden relative"
                style="background: var(--grad-premium); color: white; border-radius: 1rem;" role="region"
                aria-label="Digital Wallet Section">

                <!-- Background Decor -->
                <div
                  class="absolute top-0 right-0 p-0 transform translate-x-1/3 -translate-y-1/3 opacity-5 pointer-events-none">
                  <i class="bi bi-wallet2" style="font-size: 20rem; color: white;"></i>
                </div>
                <!-- Ambient Glow -->
                <div class="absolute top-1/2 left-0 w-64 h-64 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2"
                  style="background-color: rgba(236, 35, 42, 0.1);">
                </div>

                <div class="card__body p-8 relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
                  <div class="flex-1 text-center md:text-left">
                    <div
                      class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-black uppercase tracking-widest mb-4 backdrop-blur-sm"
                      style="color: var(--icta-green);">
                      <i class="bi bi-shield-check"></i> Identity Verified
                    </div>
                    <h2 class="text-3xl font-black mb-2 text-white tracking-tight">Authoritative <span
                        style="color: var(--icta-red);">Wallet</span></h2>
                    <p class="text-slate-400 text-sm mb-6 leading-relaxed max-w-lg">
                      Secure access to your {{ user.saved_documents.length }} official government credentials.
                      Documents are cryptographically signed for offline verification and sharing.
                    </p>
                    <div class="flex flex-wrap gap-3 justify-center md:justify-start">
                      <router-link to="/profile"
                        class="button button--pill px-8 shadow-lg transition-transform flex items-center gap-2"
                        style="border: none; background: var(--icta-red); color: white; font-weight: 700; box-shadow: 0 4px 12px rgba(236, 35, 42, 0.3);"
                        aria-label="Open Digital Wallet to view documents">
                        <i class="bi bi-wallet2"></i> Open Wallet
                      </router-link>
                    </div>
                  </div>

                  <!-- Stacked Cards Visual -->
                  <div class="relative w-64 h-48 flex-shrink-0 perspective md:mr-8 hidden md:block" aria-hidden="true">
                    <div v-for="(doc, i) in user.saved_documents.slice(0, 3)" :key="i"
                      class="absolute top-0 left-0 w-full h-40 bg-white rounded-xl shadow-2xl border border-slate-200 p-4 transition-all duration-500"
                      :style="{
                        transform: `translateY(${i * 12}px) scale(${1 - (i * 0.05)})`,
                        zIndex: 3 - i,
                        opacity: 0.95 + (i * 0.02),
                        filter: 'drop-shadow(0 10px 15px rgba(0,0,0,0.2))'
                      }">
                      <div class="flex items-center gap-3 mb-3 border-b border-slate-100 pb-2">
                        <div
                          class="w-8 h-8 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-100">
                          <i :class="doc.type === 'AUTHORITATIVE_OUTPUT' ? 'bi bi-patch-check-fill' : 'bi bi-file-text-fill'"
                            class="text-sm"></i>
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="h-2 bg-slate-800 rounded w-3/4 mb-1"></div>
                          <div class="h-1.5 bg-slate-300 rounded w-1/2"></div>
                        </div>
                      </div>
                      <div class="space-y-2 opacity-50">
                        <div class="h-1.5 bg-slate-200 rounded w-full"></div>
                        <div class="h-1.5 bg-slate-200 rounded w-5/6"></div>
                        <div class="h-1.5 bg-slate-200 rounded w-4/6"></div>
                      </div>

                      <!-- Type Badge -->
                      <div
                        class="absolute bottom-3 right-3 px-2 py-0.5 bg-slate-50 text-slate-400 border border-slate-100 rounded text-[8px] font-bold uppercase tracking-wider">
                        GOK-VERIFIED
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- National Lifecycle Journey (Cradle-to-Grave) -->
              <!-- Application Tracking Section -->
              <div class="card shadow-lg">
                <header class="card__header u-flex-col u-md-flex-row u-gap-4 u-items-start u-md-items-center">
                  <div class="card__title-group">
                    <h2 class="card__title">Recent Submissions</h2>
                    <p class="card__subtitle">Track the lifecycle of your active applications</p>
                  </div>
                  <div class="toolbar ms-auto u-w-full u-md-w-auto">
                    <div class="toolbar__filters">
                      <div class="toolbar__filter-group">
                        <i class="bi bi-search toolbar__filter-icon"></i>
                        <input type="text" v-model="requestSearchQuery" placeholder="Tracking ID..."
                          class="toolbar__filter-input">
                      </div>
                      <div class="toolbar__filter-group">
                        <i class="bi bi-filter toolbar__filter-icon"></i>
                        <select v-model="myRequestsStatusFilter"
                          class="toolbar__filter-input toolbar__filter-input--with-arrow">
                          <option value="">Status Filter</option>
                          <option value="received">Received</option>
                          <option value="in_progress">In Progress</option>
                          <option value="approved">Approved</option>
                          <option value="rejected">Rejected</option>
                        </select>
                        <i class="bi bi-chevron-down toolbar__filter-arrow"></i>
                      </div>
                    </div>
                  </div>
                </header>

                <div class="card__body p-0">
                  <div v-if="filteredMyRequests.length === 0"
                    class="flex flex-col items-center justify-center py-20 text-muted">
                    <i class="bi bi-folder2-open text-5xl mb-4 opacity-20"></i>
                    <p class="font-bold uppercase tracking-widest text-xs">No active applications found</p>
                  </div>
                  <div v-else class="list">
                    <div v-for="request in filteredMyRequests" :key="request.id"
                      class="list__item hover:bg-slate-50 transition-colors p-4 border-b border-border-color flex items-center justify-between">
                      <router-link :to="`/service-request/${request.id}`" class="flex items-center gap-6 flex-1">
                        <div
                          class="w-10 h-10 rounded bg-primary-soft text-primary flex items-center justify-center font-bold text-lg">
                          {{ request.service_config.service_name.charAt(0) }}
                        </div>
                        <div>
                          <div class="font-black text-main text-sm">{{ request.service_config.service_name }}</div>
                          <div
                            class="text-xs font-mono text-muted uppercase tracking-tighter flex items-center gap-2 mt-1">
                            <span>TRK# {{ request.request_id }}</span>
                            <span class="w-1 h-1 rounded-full bg-slate-300"></span>
                            <span>{{ new Date(request.created_at).toLocaleDateString() }}</span>
                          </div>
                        </div>
                      </router-link>
                      <div class="flex items-center gap-4">
                        <span class="badge" :class="statusClass(request.status)">
                          {{ request.status.toUpperCase().replace('_', ' ') }}
                        </span>
                        <i class="bi bi-chevron-right text-muted"></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tab: Apply for Services -->
            <div v-if="citizenCurrentTab === 'services'" class="tab-content animate-slide-in u-flex u-flex-col u-gap-8">
              <header class="page__header u-justify-between u-items-end u-mb-4 u-gap-4"
                style="border-bottom: 1px solid var(--color-border); padding-bottom: 1rem;">
                <div>
                  <h2 class="page__title" style="font-size: 1.5rem">Unified Service Catalogue</h2>
                  <p class="page__subtitle">Access authoritative G2C services through the secure Huduma Bridge</p>
                </div>
                <div class="toolbar">
                  <div class="toolbar__filters">
                    <div class="toolbar__filter-group">
                      <i class="bi bi-building toolbar__filter-icon"></i>
                      <select v-model="mdaFilter" class="toolbar__filter-input toolbar__filter-input--with-arrow">
                        <option value="">All Government Agencies</option>
                        <option v-for="mda in mdas" :key="mda.id" :value="mda.id">{{ mda.name }}</option>
                      </select>
                      <i class="bi bi-chevron-down toolbar__filter-arrow"></i>
                    </div>
                    <div class="toolbar__filter-group">
                      <i class="bi bi-search toolbar__filter-icon"></i>
                      <input type="text" v-model="serviceSearchQuery" placeholder="Search services..."
                        class="toolbar__filter-input">
                    </div>
                  </div>
                </div>
              </header>

              <div v-if="filteredAvailableServices.length === 0"
                class="u-flex u-flex-col u-items-center u-justify-center u-py-20 u-text-muted u-w-full">
                <i class="bi bi-cloud-slash u-text-5xl u-mb-4 u-opacity-20"></i>
                <p class="u-font-black u-uppercase u-tracking-widest u-text-xs">No services currently available</p>
                <p class="u-text-xs u-mt-2 u-opacity-60">The authoritative catalogue is being updated. Please check back
                  shortly.</p>
              </div>
              <div v-else class="stats-grid">
                <div v-for="service in filteredAvailableServices" :key="service.id"
                  class="card u-p-8 u-flex u-flex-col u-items-center u-text-center transition-all hover:u-shadow-xl"
                  style="border: none;">
                  <div class="u-flex u-items-center u-justify-center u-mb-6 u-rounded-lg"
                    style="width: 4rem; height: 4rem; background: var(--color-primary-soft); color: var(--color-primary); font-size: 1.5rem;">
                    <i class="bi bi-lightning-charge-fill"></i>
                  </div>
                  <h3 class="u-font-bold u-text-main u-mb-2" style="font-size: 1.125rem;">{{ service.service_name }}
                  </h3>
                  <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-mb-8 u-p-1 u-rounded"
                    style="background: var(--color-background-alt); letter-spacing: 0.1em;">
                    {{ getMdaName(service.mda).split('(')[0] }}
                  </p>
                  <router-link :to="`/apply/${service.service_code}`"
                    class="button button--primary button--pill u-w-full">
                    Begin Application
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- STAFF OPERATIONS VIEW -->
      <section
        v-else-if="['officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(user.role)"
        class="staff-portal flex flex-col gap-8">

        <!-- Top Stats Row -->
        <WogDashboardStats :stats="serviceConfigStore.catalogueSummary || {}" />

        <div class="grid grid--sidebar gap-8">
          <!-- Priority Queue -->
          <div class="card u-overflow-hidden">
            <header class="card__header u-flex-col u-md-flex-row u-gap-4 u-justify-between">
              <div class="card__title-group">
                <h2 class="card__title u-flex u-items-center u-gap-2">
                  <i class="bi bi-inboxes u-text-primary"></i> Priority Work Queue
                </h2>
                <p class="card__subtitle">Tasks specifically assigned to your workstation</p>
              </div>
              <div class="toolbar u-w-full u-md-w-auto">
                <div class="toolbar__filters">
                  <div class="toolbar__filter-group">
                    <i class="bi bi-search toolbar__filter-icon"></i>
                    <input type="text" v-model="queueSearchQuery" placeholder="Filter queue..."
                      class="toolbar__filter-input">
                  </div>
                </div>
              </div>
            </header>
            <div class="card__body u-p-0">
              <div v-if="filteredAssignedRequests.length === 0"
                class="u-flex u-flex-col u-items-center u-justify-center u-p-20 u-text-muted">
                <i class="bi bi-check2-circle u-text-5xl u-mb-4 u-text-success"></i>
                <p class="u-font-bold u-uppercase u-tracking-widest u-text-xs">Workstation Queue Empty</p>
                <p class="u-text-xs u-mt-2 u-opacity-60">Acquire new tasks from the Universal Pool</p>
              </div>
              <div v-else class="u-divide-y">
                <div v-for="request in filteredAssignedRequests" :key="request.id"
                  class="u-p-4 u-flex u-flex-col u-md-flex-row u-gap-4 u-items-start u-md-items-center u-justify-between hover:u-bg-bg-page transition-colors">
                  <div class="u-flex-1">
                    <div class="u-flex u-flex-wrap u-items-center u-gap-3 u-mb-2">
                      <span class="u-font-bold u-text-main u-text-sm">{{ request.service_config.service_name }}</span>
                      <span class="table__code-badge">#{{ request.request_id }}</span>
                      <span class="badge" :class="priorityClass(request.priority)">{{ request.priority.toUpperCase()
                      }}</span>
                    </div>
                    <div
                      class="u-flex u-items-center u-gap-4 u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-tighter">
                      <span><i class="bi bi-diagram-3-fill u-mb-1"></i> {{ request.current_step?.step_name ||
                        'Processing' }}</span>
                      <span><i class="bi bi-clock-fill u-mb-1"></i> {{ new Date(request.created_at).toLocaleDateString()
                      }}</span>
                    </div>
                  </div>
                  <div class="u-flex u-gap-2 u-w-full u-md-u-w-auto u-z-base">
                    <button @click="openCompleteStepModal(request)" class="button button--primary button--small">
                      <i class="bi bi-shield-check"></i> Process
                    </button>
                    <button @click="releaseTask(request.id)" class="button button--ghost button--small"
                      title="Release to Pool">
                      <i class="bi bi-arrow-left-circle"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Activity / KPIs Sidebar -->
          <div class="card" style="background: var(--color-background-alt)">
            <header class="card__header u-bg-transparent">
              <h2 class="card__title u-text-xs u-uppercase u-tracking-widest u-text-muted">Processing Activity</h2>
            </header>
            <div class="card__body u-p-0">
              <div class="u-flex u-flex-col">
                <div v-for="request in filteredMyRequests.slice(0, 8)" :key="request.id"
                  class="u-p-3 u-border-b u-border-border-color last:u-border-0 u-flex u-justify-between u-items-center">
                  <div class="u-min-w-0">
                    <div class="u-font-bold u-text-main u-text-xs u-truncate" style="max-width: 140px">{{
                      request.service_config.service_name }}</div>
                    <div class="u-text-[9px] u-font-mono u-text-muted">{{ request.request_id }}</div>
                  </div>
                  <span class="badge badge--small u-scale-90" :class="statusClass(request.status)">{{
                    request.status.replace('_', ' ') }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Universal Pool -->
        <section class="card u-overflow-hidden">
          <header class="card__header u-flex-col u-md-flex-row u-gap-4 u-justify-between">
            <div class="card__title-group">
              <h2 class="card__title u-flex u-items-center u-gap-2">
                <i class="bi bi-globe u-text-info"></i> National Task Pool
              </h2>
              <p class="card__subtitle">Unassigned requests awaiting institutional action</p>
            </div>
            <div class="toolbar u-w-full u-md-w-auto">
              <div class="toolbar__filters">
                <div class="toolbar__filter-group">
                  <i class="bi bi-search toolbar__filter-icon"></i>
                  <input type="text" v-model="unassignedSearchQuery" placeholder="Search pool..."
                    class="toolbar__filter-input">
                </div>
              </div>
            </div>
          </header>
          <div class="table-container">
            <table class="table">
              <thead>
                <tr class="table__header-row">
                  <th class="table__header-cell table__header-cell--with-left-padding">Registry Service</th>
                  <th class="table__header-cell">Internal Ref</th>
                  <th class="table__header-cell">Priority</th>
                  <th class="table__header-cell">Submission Date</th>
                  <th class="table__header-cell table__header-cell--align-right table__header-cell--with-right-padding">
                    Acquisition</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in filteredUnassignedRequests" :key="request.id" class="table__row">
                  <td class="table__cell table__cell--with-left-padding">
                    <div class="table__cell--bold">{{ request.service_config.service_name }}</div>
                    <div class="u-text-primary u-font-bold u-uppercase" style="font-size: 10px">{{
                      request.current_step?.step_name }}</div>
                  </td>
                  <td class="table__cell">
                    <span class="table__code-badge">{{ request.request_id }}</span>
                  </td>
                  <td class="table__cell">
                    <span class="badge" :class="priorityClass(request.priority)">{{ request.priority.toUpperCase()
                    }}</span>
                  </td>
                  <td class="table__cell u-text-muted">{{ new Date(request.created_at).toLocaleDateString() }}</td>
                  <td class="table__cell table__cell--align-right table__cell--with-right-padding">
                    <button @click="claimTask(request.id)" class="button button--secondary button--small button--pill">
                      <i class="bi bi-box-arrow-in-right"></i> Claim
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredUnassignedRequests.length === 0">
                  <td colspan="5" class="table__cell u-text-center u-p-12 u-text-muted" style="font-style: italic">
                    All registry systems nominal. No pending unassigned requests detected.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Management Reporting -->
        <section v-if="['supervisor', 'GLOBAL_SUPERVISOR', 'MDA_SUPERVISOR', 'mda_admin'].includes(user.role)"
          class="pt-8">
          <header class="mb-4">
            <h2 class="text-xl font-black text-main">Institutional Oversight Analytics</h2>
            <p class="text-muted text-sm">Executive monitoring of registry throughput and bottleneck detection</p>
          </header>
          <ReportsDashboard />
        </section>
      </section>

      <!-- SYSTEM ADMINISTRATION VIEW -->
      <section v-if="user.role === 'admin'" class="admin-portal">
        <div class="dashboard-layout">
          <!-- Left Sidebar Navigation -->
          <aside class="dashboard-sidebar">
            <div class="card">
              <div class="card__body p-0">
                <div class="flex flex-col">
                  <div v-for="group in adminTabGroups" :key="group.title"
                    class="p-4 border-b border-border-color last:border-0">
                    <div
                      class="text-[10px] font-black text-muted uppercase tracking-widest mb-3 flex items-center gap-2">
                      <i :class="group.icon"></i> {{ group.title }}
                    </div>
                    <div class="flex flex-col gap-1">
                      <button v-for="tab in group.tabs" :key="tab" @click="currentTab = tab" class="sidebar-nav__item"
                        :class="{ 'sidebar-nav__item--active': currentTab === tab }">
                        <span class="sidebar-nav__text">{{ tab }}</span>
                        <span v-if="tab === 'System Docs'"
                          class="ml-2 bg-success text-white text-[8px] font-black px-2 py-0.5 rounded-full animate-pulse">UPDATED</span>
                        <i v-if="currentTab === tab" class="bi bi-chevron-right sidebar-nav__arrow"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </aside>

          <!-- System Configuration Workstation -->
          <div class="dashboard-content">
            <div class="card shadow-lg border-0 overflow-hidden">
              <header class="card__header bg-secondary text-white border-0 flex justify-between items-center p-6">
                <div>
                  <h2 class="card__title text-white text-2xl mb-1">{{ currentTab }}</h2>
                  <p class="text-slate-300 text-xs font-mono opacity-80">Active Governance Module | Security:
                    GOK-ADMIN-01</p>
                </div>
                <div
                  class="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center text-white backdrop-blur-sm">
                  <i class="bi bi-cpu text-xl"></i>
                </div>
              </header>
              <div class="card__body p-6">
                <component :is="activeAdminComponent" />

                <div v-if="currentTab === 'System Docs'"
                  class="docs-workstation mt-8 border-t border-border-color pt-8">
                  <div class="mb-8 p-6 bg-primary-soft rounded-2xl border-2 border-primary border-dashed">
                    <h2 class="text-2xl font-black text-primary flex items-center gap-3">
                      <i class="bi bi-journal-richtext"></i>
                      Authoritative System Documentation Registry
                      <span class="badge badge--primary uppercase tracking-widest text-[10px]">Activated</span>
                    </h2>
                    <p class="text-primary/70 text-sm mt-1 font-medium">Organized Governance & Technical Specifications
                      Library</p>
                  </div>
                  <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
                    <!-- Documentation Navigation Sidebar -->
                    <div class="lg:col-span-1 space-y-6">
                      <div v-for="group in categorizedDocs" :key="group.category" class="doc-category">
                        <h3
                          class="flex items-center gap-2 text-[10px] font-black text-muted uppercase tracking-widest mb-3">
                          <i :class="group.icon" class="text-primary"></i> {{ group.category }}
                        </h3>
                        <div class="flex flex-col gap-1">
                          <button v-for="doc in group.docs" :key="doc.file" @click="selectedDoc = doc.file"
                            class="text-left py-2 px-3 rounded-lg text-xs transition-all flex items-center justify-between"
                            :class="selectedDoc === doc.file ? 'bg-primary-soft text-primary font-bold border-l-4 border-primary' : 'hover:bg-slate-50 text-slate-600'">
                            {{ doc.name }}
                            <i v-if="selectedDoc === doc.file" class="bi bi-chevron-right text-[10px]"></i>
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Documentation Content Area -->
                    <div class="lg:col-span-3">
                      <div class="border border-border-color rounded-2xl overflow-hidden shadow-inner bg-white">
                        <DocViewer :url="`/${selectedDoc}`" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Lifecycle Decision Modal -->
    <BaseModal v-model:show="showCompleteStepModal" title="Administrative Disposition"
      subtitle="Define the legal outcome for this transaction stage" icon="bi-shield-shaded">
      <form @submit.prevent="completeStep" class="form flex flex-col gap-6">
        <div class="form__group">
          <label class="form__label">Final Stage Outcome</label>
          <select v-model="stepAction.action" class="form__select w-full" required>
            <option value="" disabled>Select disposition...</option>
            <option value="approve">Approve & Advance</option>
            <option value="reject">Deny Transaction</option>
            <option value="request_changes">Revert for Correction</option>
          </select>
        </div>
        <div class="form__group">
          <label class="form__label">Official Statement / Audit Remarks</label>
          <textarea v-model="stepAction.details" rows="4" class="form__textarea w-full"
            placeholder="Enter findings or evidence details for the national audit trail..."></textarea>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t border-border-color mt-4">
          <button type="button" @click="closeCompleteStepModal" class="button button--secondary">Discard</button>
          <button type="submit"
            class="button button--primary shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            Finalize Stage Decision
          </button>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useAuthStore } from '../store/auth';
  import { useCitizenStore } from '../store/citizen';
  import { useMdaStore } from '../store/mda';
  import { useStaffStore } from '../store/staff';
  import { useServiceConfigStore } from '../store/serviceConfig';

  // Component Imports
  import ReportsDashboard from '../components/Supervisor/ReportsDashboard.vue';
  import MdaManager from '../components/Admin/MdaManager.vue';
  import ServiceConfigManager from '../components/Admin/ServiceConfigManager.vue';
  import WorkflowStepManager from '../components/Admin/WorkflowStepManager.vue';
  import DocViewer from '../components/Admin/DocViewer.vue';
  import AdminRolesView from './AdminRolesView.vue';
  import UserManager from '../components/Admin/UserManager.vue';
  import ApiRegistry from '../components/Admin/ApiRegistry.vue';
  import AuditLogManager from '../components/Admin/AuditLogManager.vue';
  import SystemHealthView from '../components/Admin/SystemHealthView.vue';
  import SecurityTrustView from '../components/Admin/SecurityTrustView.vue';
  import ArchitectureSimulator from '../components/Admin/ArchitectureSimulator.vue';
  import ServiceCatalogueMatrix from '../components/Admin/ServiceCatalogueMatrix.vue';
  import DesktopReviewManager from '../components/Admin/DesktopReviewManager.vue';
  import InterDepartmentalMemoView from '../components/Admin/InterDepartmentalMemoView.vue';
  import BpmnRenderer from '../components/Admin/BpmnRenderer.vue';
  import RegistriesMonitor from '../components/Admin/RegistriesMonitor.vue';
  import BaseModal from '../components/Common/BaseModal.vue';

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
  const stepAction = ref({ action: '', details: '' });

  const serviceSearchQuery = ref('');
  const requestSearchQuery = ref('');
  const queueSearchQuery = ref('');
  const unassignedSearchQuery = ref('');
  const incompleteSearchQuery = ref('');
  const myRequestsStatusFilter = ref('');
  const citizenCurrentTab = ref('inbox');
  const queueStatusFilter = ref('');
  const priorityFilter = ref('');
  const prioritySearchLocal = ref('');
  const showPriorityDropdown = ref(false);

  const selectPriority = (p) => {
    priorityFilter.value = p;
    prioritySearchLocal.value = p ? p.charAt(0).toUpperCase() + p.slice(1) : 'Any Priority';
    showPriorityDropdown.value = false;
  };

  const mdaFilter = ref('');
  const mdaSearchLocal = ref('');
  const showMdaDropdown = ref(false);
  const mdaIncompleteRequests = computed(() => staffStore.mdaIncompleteRequests);

  const filteredMdas = computed(() => {
    if (!mdaSearchLocal.value) return mdas.value;
    const q = mdaSearchLocal.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q));
  });

  const selectMda = (mda) => {
    if (!mda) { mdaFilter.value = ''; mdaSearchLocal.value = ''; }
    else { mdaFilter.value = mda.id; mdaSearchLocal.value = mda.name; }
    showMdaDropdown.value = false;
  };

  const filteredAvailableServices = computed(() => {
    let result = availableServices.value;
    if (mdaFilter.value) result = result.filter(s => s.mda === parseInt(mdaFilter.value));
    if (priorityFilter.value) result = result.filter(s => s.priority === priorityFilter.value);
    if (serviceSearchQuery.value) {
      const q = serviceSearchQuery.value.toLowerCase();
      result = result.filter(s =>
        s.service_name.toLowerCase().includes(q) ||
        getMdaName(s.mda).toLowerCase().includes(q)
      );
    }
    return result;
  });

  const filteredMyRequests = computed(() => {
    let result = myRequests.value;
    if (myRequestsStatusFilter.value) result = result.filter(r => r.status === myRequestsStatusFilter.value);
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
    if (queueStatusFilter.value) result = result.filter(r => r.status === queueStatusFilter.value);
    if (priorityFilter.value) result = result.filter(r => r.priority === priorityFilter.value);
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
    if (priorityFilter.value) result = result.filter(r => r.priority === priorityFilter.value);
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

  const adminTabGroups = [
    { title: 'Entity Management', icon: 'bi-people-fill', tabs: ['Users', 'Roles', 'MDAs'] },
    { title: 'Operations', icon: 'bi-briefcase-fill', tabs: ['Services', 'Whole-of-Gov Catalogue'] },
    { title: 'Process Engineering', icon: 'bi-diagram-3-fill', tabs: ['Workflow Orchestration', 'Architecture Pilot', 'Desktop Reviews', 'Registries'] },
    { title: 'Governance & Comms', icon: 'bi-shield-lock-fill', tabs: ['Reports', 'Audit Logs', 'System Health', 'API Docs', 'Security & Trust', 'Inter-Dept Memos', 'System Docs'] }
  ];
  const currentTab = ref('System Docs');

  // Dynamic Component Mapping
  const activeAdminComponent = computed(() => {
    const map = {
      'MDAs': MdaManager,
      'Services': ServiceConfigManager,
      'Users': UserManager,
      'Workflow Orchestration': WorkflowStepManager,
      'Reports': ReportsDashboard,
      'Roles': AdminRolesView,
      'API Docs': ApiRegistry,
      'Audit Logs': AuditLogManager,
      'System Health': SystemHealthView,
      'Security & Trust': SecurityTrustView,
      'Architecture Pilot': ArchitectureSimulator,
      'Whole-of-Gov Catalogue': ServiceCatalogueMatrix,
      'Desktop Reviews': DesktopReviewManager,
      'Inter-Dept Memos': InterDepartmentalMemoView,
      'Registries': RegistriesMonitor
    };
    return map[currentTab.value] || null;
  });

  const categorizedDocs = [
    {
      category: 'Architecture & Logic',
      icon: 'bi-diagram-3-fill',
      docs: [
        { name: 'System Architecture', file: 'docs/architecture/architecture_three.md' },
        { name: 'Workflow Engine', file: 'docs/architecture/poc_algorithm_workflow_documentation.md' },
        { name: 'RBAC Implementation', file: 'docs/architecture/RBAC_IMPLEMENTATION_SUMMARY.md' },
        { name: 'BPMN Enhancements', file: 'docs/architecture/BPMN_WORKFLOW_ENHANCEMENT.md' },
      ]
    },
    {
      category: 'POC Core Documents',
      icon: 'bi-file-earmark-medical-fill',
      docs: [
        { name: 'Project Overview', file: 'docs/poc/poc_project_overview_concept_note.md' },
        { name: 'Functional Specs', file: 'docs/poc/poc_functional_non_functional_requirements.md' },
        { name: 'System Design', file: 'docs/poc/poc_system_design_documents.md' },
        { name: 'Test & Validation', file: 'docs/poc/poc_test_validation_plan.md' },
      ]
    },
    {
      category: 'Operational Guides',
      icon: 'bi-journal-check',
      docs: [
        { name: 'Deployment Plan', file: 'docs/guides/poc_deployment_dev_ops_plan.md' },
        { name: 'Huduma Bridge', file: 'docs/guides/huduma_bridge_instructions.md' },
        { name: 'BEM UI Standards', file: 'docs/style-guide/BEM-DOCUMENTATION.md' },
      ]
    },
    {
      category: 'Governance Reports',
      icon: 'bi-clipboard-data-fill',
      docs: [
        { name: 'POC Final Report', file: 'docs/reports/ICTA_POC_Comprehensive_Report.md' },
        { name: 'Consolidated Actions', file: 'docs/reports/ICTA_WB_CONSOLIDATED_ACTIONS.md' },
        { name: 'Meeting Actions', file: 'docs/reports/ICTA_MEETING_ACTIONS.md' },
      ]
    }
  ];
  const selectedDoc = ref('docs/architecture/architecture_three.md');

  onMounted(async () => {
    const role = user.value?.role;
    if (role === 'citizen') {
      await authStore.fetchCurrentUser();
    }

    if (['citizen', 'officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(role)) {
      citizenStore.fetchAvailableServices();
      citizenStore.fetchMyRequests();
      mdaStore.fetchMdas();
    }
    if (['officer', 'supervisor', 'registrar', 'mda_admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(role)) {
      staffStore.fetchIncompleteMdaRequests();
      staffStore.fetchUnassignedRequests();
      staffStore.fetchAssignedRequests();
      if (['supervisor', 'GLOBAL_SUPERVISOR', 'MDA_SUPERVISOR', 'mda_admin'].includes(role)) {
        staffStore.fetchTeamRequests();
        staffStore.fetchEscalatedRequests();
      }
    } else if (role === 'admin') {
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
      received: 'bg-blue-100 text-blue-800', in_progress: 'bg-yellow-100 text-yellow-800', escalated: 'bg-orange-100 text-orange-800',
      approved: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800', closed: 'bg-gray-100 text-gray-800', validation_failed: 'bg-red-100 text-red-800',
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
  };

  const priorityClass = (priority) => {
    const classes = {
      low: 'bg-slate-100 text-slate-600', normal: 'bg-indigo-100 text-indigo-700', high: 'bg-amber-100 text-amber-700', critical: 'bg-rose-100 text-rose-700 animate-pulse',
    };
    return classes[priority?.toLowerCase()] || 'bg-gray-100 text-gray-600';
  };

  const openCompleteStepModal = (request) => {
    currentRequestToComplete.value = request;
    showCompleteStepModal.value = true;
    stepAction.value = { action: '', details: '' };
  };

  const closeCompleteStepModal = () => { showCompleteStepModal.value = false; currentRequestToComplete.value = null; };

  const completeStep = async () => {
    if (!currentRequestToComplete.value) return;
    try {
      await staffStore.completeWorkflowStep(currentRequestToComplete.value.id, stepAction.value.action, stepAction.value.details);
      closeCompleteStepModal();
      await staffStore.fetchAssignedRequests();
      await staffStore.fetchUnassignedRequests();
      await staffStore.fetchIncompleteMdaRequests();
      if (user.value?.role === 'supervisor') {
        await staffStore.fetchTeamRequests();
        await staffStore.fetchEscalatedRequests();
      }
    } catch (error) { alert('Failed to complete step: ' + (error.response?.data?.detail || error.message)); }
  };

  const escalateRequest = async (requestId) => {
    if (confirm('Are you sure you want to escalate this request?')) {
      try { await staffStore.escalateRequest(requestId); staffStore.fetchAssignedRequests(); } catch (error) { alert('Failed to escalate request: ' + error.message); }
    }
  };

  const claimTask = async (requestId) => {
    try { await staffStore.claimTask(requestId); } catch (error) { alert('Claim failed: ' + (error.response?.data?.detail || error.message)); }
  };

  const releaseTask = async (requestId) => {
    if (confirm('Are you sure you want to release this task back to the pool?')) {
      try { await staffStore.releaseTask(requestId); } catch (error) { alert('Release failed: ' + (error.response?.data?.detail || error.message)); }
    }
  };
</script>

<style scoped>

  /* Scoped Utility Classes to Replace Tailwind */
  .bg-secondary {
    background-color: var(--secondary);
  }

  .bg-primary-soft {
    background-color: var(--primary-soft);
  }

  .text-main {
    color: var(--text-main);
  }

  .text-muted {
    color: var(--text-muted);
  }

  .text-primary {
    color: var(--primary);
  }

  .text-white {
    color: white;
  }

  .border-border-color {
    border-color: var(--border-color);
  }

  .shadow-lg {
    box-shadow: var(--shadow-lg);
  }

  .shadow-xl {
    box-shadow: var(--shadow-xl);
  }

  /* Custom "Tailwind-like" Utilities used in template */
  .hover\:shadow-md:hover {
    box-shadow: var(--shadow-md);
  }

  .hover\:shadow-xl:hover {
    box-shadow: var(--shadow-xl);
  }

  .hover\:-translate-y-1:hover {
    transform: translateY(-4px);
  }

  .hover\:bg-slate-50:hover {
    background-color: #f8fafc;
  }

  .hover\:bg-blue-50\/30:hover {
    background-color: rgba(239, 246, 255, 0.3);
  }

  .hover\:text-primary:hover {
    color: var(--primary);
  }

  .hover\:text-danger:hover {
    color: var(--danger);
  }

  .hover\:bg-red-50:hover {
    background-color: #fef2f2;
  }

  .group:hover .group-hover\:bg-blue-50\/30 {
    background-color: rgba(239, 246, 255, 0.3);
  }

  .opacity-80 {
    opacity: 0.8;
  }

  .opacity-60 {
    opacity: 0.6;
  }

  .scale-90 {
    transform: scale(0.9);
  }

  .blur-3xl {
    filter: blur(64px);
  }

  .backdrop-blur-sm {
    backdrop-filter: blur(4px);
  }

  .bg-white\/5 {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .bg-white\/10 {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .bg-primary\/20 {
    background-color: rgba(236, 35, 42, 0.2);
  }

  /* Layout Utilities */
  .w-full {
    width: 100%;
  }

  .h-full {
    height: 100%;
  }

  .w-12 {
    width: 3rem;
  }

  .h-12 {
    height: 3rem;
  }

  .w-16 {
    width: 4rem;
  }

  .h-16 {
    height: 4rem;
  }

  .min-w-0 {
    min-width: 0;
  }

  .flex {
    display: flex;
  }

  .flex-col {
    flex-direction: column;
  }

  .items-center {
    align-items: center;
  }

  .justify-between {
    justify-content: space-between;
  }

  .justify-center {
    justify-content: center;
  }

  .justify-end {
    justify-content: flex-end;
  }

  .gap-1 {
    gap: 0.25rem;
  }

  .gap-2 {
    gap: 0.5rem;
  }

  .gap-3 {
    gap: 0.75rem;
  }

  .gap-4 {
    gap: 1rem;
  }

  .gap-6 {
    gap: 1.5rem;
  }

  .gap-8 {
    gap: 2rem;
  }

  .p-4 {
    padding: 1rem;
  }

  .p-6 {
    padding: 1.5rem;
  }

  .p-8 {
    padding: 2rem;
  }

  .px-2 {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .px-3 {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }

  .py-2 {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }

  .pb-4 {
    padding-bottom: 1rem;
  }

  .mt-1 {
    margin-top: 0.25rem;
  }

  .mt-4 {
    margin-top: 1rem;
  }

  .mt-8 {
    margin-top: 2rem;
  }

  .mb-2 {
    margin-bottom: 0.5rem;
  }

  .mb-4 {
    margin-bottom: 1rem;
  }

  .mb-6 {
    margin-bottom: 1.5rem;
  }

  .mb-8 {
    margin-bottom: 2rem;
  }

  .pt-4 {
    padding-top: 1rem;
  }

  .border-t {
    border-top: 1px solid var(--border-color);
  }

  .rounded {
    border-radius: 0.25rem;
  }

  .rounded-lg {
    border-radius: 0.5rem;
  }

  .rounded-xl {
    border-radius: 0.75rem;
  }

  .rounded-2xl {
    border-radius: 1rem;
  }

  .rounded-full {
    border-radius: 9999px;
  }

  .rounded-none {
    border-radius: 0;
  }

  .border {
    border-width: 1px;
    border-style: solid;
  }

  .border-b {
    border-bottom-width: 1px;
    border-bottom-style: solid;
  }

  .border-b-4 {
    border-bottom-width: 4px;
    border-bottom-style: solid;
  }

  .border-0 {
    border-width: 0;
  }

  .border-transparent {
    border-color: transparent;
  }

  .border-gray-100 {
    border-color: #f3f4f6;
  }

  .border-slate-200 {
    border-color: #e2e8f0;
  }

  .text-xs {
    font-size: 0.75rem;
  }

  .text-sm {
    font-size: 0.875rem;
  }

  .text-lg {
    font-size: 1.125rem;
  }

  .text-xl {
    font-size: 1.25rem;
  }

  .text-2xl {
    font-size: 1.5rem;
  }

  .font-bold {
    font-weight: 700;
  }

  .font-black {
    font-weight: 900;
  }

  .uppercase {
    text-transform: uppercase;
  }

  .tracking-widest {
    letter-spacing: 0.1em;
  }

  .tracking-tighter {
    letter-spacing: -0.05em;
  }

  .truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .relative {
    position: relative;
  }

  .absolute {
    position: absolute;
  }

  .sticky {
    position: sticky;
  }

  .top-8 {
    top: 2rem;
  }

  .left-3 {
    left: 0.75rem;
  }

  .translate-y-1\/2 {
    transform: translateY(-50%);
  }

  .overflow-hidden {
    overflow: hidden;
  }

  .transition-all {
    transition: all 0.2s;
  }

  /* Custom Component Styles */
  .dashboard {
    color: var(--text-main);
    padding-bottom: 3rem;
  }

  .wallet-banner {
    background: var(--secondary);
    color: white;
    border-radius: var(--radius-lg);
    padding: 2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-xl);
  }

  .wallet-banner__deco {
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(99, 102, 241, 0.2);
    border-radius: 50%;
    pointer-events: none;
  }

  .wallet-doc-icon {
    width: 3rem;
    height: 3rem;
    background: white;
    border-radius: var(--radius-sm);
    border: 2px solid var(--secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    box-shadow: var(--shadow-md);
    transition: transform 0.2s;
    margin-left: -0.5rem;
  }

  .wallet-doc-icon:hover {
    transform: translateY(-4px);
    z-index: 5;
  }

  /* Sidebar Specifics */
  .admin-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 2rem;
    min-height: 800px;
  }

  .sidebar__item {
    width: 100%;
    text-align: left;
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #475569;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .sidebar__item:hover {
    background: #f1f5f9;
    color: var(--primary);
  }

  .sidebar__item--active {
    background: var(--primary);
    color: white;
  }

  .sidebar__item--active:hover {
    background: var(--primary);
    color: white;
  }

  /* Dashboard Layout - Sidebar + Content */
  .dashboard-layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  @media (min-width: 1024px) {
    .dashboard-layout {
      grid-template-columns: 280px 1fr;
    }
  }

  .dashboard-sidebar {
    position: sticky;
    top: 2rem;
    height: fit-content;
  }

  .dashboard-content {
    min-width: 0;
  }

  /* Sidebar Navigation */
  .sidebar-nav {
    display: flex;
    flex-direction: column;
  }

  .sidebar-nav__item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    border: none;
    background: transparent;
    color: var(--text-main);
    font-size: 0.9375rem;
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    transition: var(--transition);
    border-left: 3px solid transparent;
    position: relative;
  }

  .sidebar-nav__item:hover {
    background: var(--bg-hover);
    color: var(--primary);
  }

  .sidebar-nav__item--active {
    background: var(--primary-soft);
    color: var(--primary);
    font-weight: 700;
    border-left-color: var(--primary);
  }

  .sidebar-nav__icon {
    font-size: 1.125rem;
    flex-shrink: 0;
  }

  .sidebar-nav__text {
    flex: 1;
  }

  .sidebar-nav__arrow {
    font-size: 0.875rem;
    opacity: 0.7;
  }

  /* Tab Content Animation */
  .tab-content {
    animation: fadeIn 0.3s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Full-Width Dashboard Wrapper */
  .dashboard-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--bg-page);
  }

  .dashboard-header {
    background: white;
    border-bottom: 1px solid var(--border-color);
    padding: 1.5rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  .dashboard-header__content {
    max-width: 1600px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
    flex-wrap: wrap;
  }

  .dashboard-main {
    flex: 1;
    display: flex;
  }

  /* Override dashboard-layout for full width */
  .citizen-portal .dashboard-layout,
  .staff-portal .dashboard-layout,
  .admin-portal .dashboard-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: calc(100vh - 120px);
    max-width: none;
    margin: 0;
    gap: 0;
  }

  @media (max-width: 1023px) {

    .citizen-portal .dashboard-layout,
    .staff-portal .dashboard-layout,
    .admin-portal .dashboard-layout {
      grid-template-columns: 1fr;
    }
  }

  /* Sidebar - Full Height */
  .citizen-portal .dashboard-sidebar,
  .staff-portal .dashboard-sidebar,
  .admin-portal .dashboard-sidebar {
    background: white;
    border-right: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
  }

  @media (max-width: 1023px) {

    .citizen-portal .dashboard-sidebar,
    .staff-portal .dashboard-sidebar,
    .admin-portal .dashboard-sidebar {
      position: static;
      height: auto;
      border-right: none;
      border-bottom: 1px solid var(--border-color);
    }
  }

  /* Content Area - Full Width */
  .citizen-portal .dashboard-content,
  .staff-portal .dashboard-content,
  .admin-portal .dashboard-content {
    flex: 1;
    padding: 2rem;
    max-width: none;
    overflow-x: hidden;
  }

  @media (min-width: 1400px) {

    .citizen-portal .dashboard-content,
    .staff-portal .dashboard-content,
    .admin-portal .dashboard-content {
      padding: 3rem;
    }
  }

  /* Sidebar Navigation - Enhanced */
  .sidebar-nav {
    padding: 1rem 0;
  }

  .sidebar-nav__item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.5rem;
    border: none;
    background: transparent;
    color: var(--text-main);
    font-size: 0.9375rem;
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    transition: var(--transition);
    border-left: 3px solid transparent;
    position: relative;
  }

  .sidebar-nav__item:hover {
    background: var(--bg-hover);
    color: var(--primary);
  }

  .sidebar-nav__item--active {
    background: var(--primary-soft);
    color: var(--primary);
    font-weight: 700;
    border-left-color: var(--primary);
  }

  .sidebar-nav__icon {
    font-size: 1.125rem;
    flex-shrink: 0;
  }

  .sidebar-nav__text {
    flex: 1;
  }

  .sidebar-nav__arrow {
    font-size: 0.875rem;
    opacity: 0.7;
  }

  /* Remove container constraints */
  .citizen-portal,
  .staff-portal,
  .admin-portal {
    width: 100%;
    max-width: none;
  }
</style>
