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

    <transition name="modal-fade">
      <div v-if="actionFeedback.message" class="action-toast" :class="actionFeedback.type">
        <i
          :class="actionFeedback.type === 'success' ? 'bi bi-check-circle-fill' : (actionFeedback.type === 'error' ? 'bi bi-exclamation-octagon-fill' : 'bi bi-info-circle-fill')"></i>
        <span>{{ actionFeedback.message }}</span>
      </div>
    </transition>

    <div v-if="user" class="dashboard-main">

      <section class="citizen-portal" v-if="user.role && (user.role.toLowerCase() === 'citizen' || user.role.toLowerCase() === 'hospital_staff')">
        <div class="dashboard-layout u-p-8">
          <!-- Sidebar Navigation -->
          <aside class="dashboard-sidebar">
            <div class="card card--glass overflow-hidden border-0 shadow-xl rounded-[2rem]">
              <div class="sidebar-nav py-6">
                <button @click="citizenCurrentTab = 'inbox'" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-indigo-50/50 group"
                  :class="{ 'bg-indigo-50/80 border-l-4 border-indigo-600': citizenCurrentTab === 'inbox' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-inbox-fill"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest" :class="citizenCurrentTab === 'inbox' ? 'text-indigo-900' : 'text-slate-500'">Official Inbox</div>
                    <div class="text-[10px] text-slate-400 font-bold">Registry Dispatch</div>
                  </div>
                  <span v-if="pendingActions.length > 0" class="badge badge--danger scale-75">{{ pendingActions.length }}</span>
                </button>
                
                <button @click="citizenCurrentTab = 'services'" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-indigo-50/50 group"
                  :class="{ 'bg-indigo-50/80 border-l-4 border-indigo-600': citizenCurrentTab === 'services' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-grid-fill"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest" :class="citizenCurrentTab === 'services' ? 'text-indigo-900' : 'text-slate-500'">Apply for Services</div>
                    <div class="text-[10px] text-slate-400 font-bold">Service Discovery</div>
                  </div>
                </button>

                <div class="mx-6 my-4 border-t border-slate-100"></div>

                <router-link to="/profile" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-indigo-50/50 group">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-person-badge-fill"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest text-slate-500">My Profile</div>
                    <div class="text-[10px] text-slate-400 font-bold">Identity & Vault</div>
                  </div>
                </router-link>

                <div class="mx-6 my-4 border-t border-slate-100"></div>

                <router-link to="/repository/artifacts" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-emerald-50/50 group">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-bank2"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest text-slate-500">EDRMS</div>
                    <div class="text-[10px] text-slate-400 font-bold">Electronic Records</div>
                  </div>
                </router-link>
              </div>
            </div>

            <!-- Promotion / Help Card -->
            <div class="mt-8 px-2">
               <div class="p-6 rounded-[2rem] bg-indigo-900 text-white relative overflow-hidden group shadow-2xl">
                  <div class="absolute -top-10 -right-10 w-32 h-32 bg-white/5 rounded-full group-hover:scale-150 transition-transform duration-700"></div>
                  <h4 class="text-[10px] font-black uppercase tracking-widest mb-2 opacity-60">Need Assistance?</h4>
                  <p class="text-xs font-bold mb-6 leading-relaxed">Connect with a citizen support advocate instantly.</p>
                  <button class="w-full bg-white/10 hover:bg-white/20 border border-white/20 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all">
                    Open Support Link
                  </button>
               </div>
            </div>
          </aside>

          <!-- Main Content -->
          <div class="dashboard-content">
            <!-- Inbox / Action Feed -->
            <div v-if="citizenCurrentTab === 'inbox'" class="tab-content flex flex-col gap-10">
              <AuthoritativeWallet :documents="user.saved_documents" />
              <ActionFeed 
                :pending-actions="pendingActions" 
                :active-applications="activeApplications" 
                @explore="citizenCurrentTab = 'services'"
              />
            </div>

            <!-- Life-Event Oriented Service Discovery -->
            <div v-else-if="citizenCurrentTab === 'services'" class="tab-content flex flex-col gap-10">
              <ServiceDiscovery :life-events="lifeEvents" />
            </div>

            <!-- Multi-step Application Flow -->
            <div v-else-if="citizenCurrentTab === 'application'" class="tab-content u-flex u-flex-col u-gap-10">
              <div class="u-flex u-items-center u-gap-4 u-mb-4">
                <button @click="citizenCurrentTab = 'services'" class="u-w-10 u-h-10 u-rounded-full u-bg-slate-100 u-flex u-items-center u-justify-center hover:u-bg-primary-soft transition-colors">
                  <i class="bi bi-arrow-left"></i>
                </button>
                <h1 class="u-text-2xl u-font-black u-text-main">{{ selectedService?.display_name || 'Service Application' }}</h1>
              </div>

              <!-- Linear Progress Bar -->
              <nav class="u-mb-10">
                <ul class="u-flex u-items-center u-list-none u-gap-4 u-overflow-x-auto u-pb-4">
                  <li v-for="(step, idx) in workflowSteps" :key="step.id" class="u-flex u-items-center u-gap-4 u-flex-shrink-0">
                    <div class="u-flex u-items-center u-gap-3">
                      <span class="u-w-10 u-h-10 u-rounded-full u-flex u-items-center u-justify-center u-text-sm u-font-black transition-all"
                        :class="idx <= currentStepIndex ? 'u-bg-primary u-text-white u-shadow-lg' : 'u-bg-slate-100 u-text-slate-400'">
                        <i v-if="idx < currentStepIndex" class="bi bi-check-lg"></i>
                        <span v-else>{{ idx + 1 }}</span>
                      </span>
                      <span class="u-text-xs u-font-black u-uppercase u-tracking-widest"
                        :class="idx === currentStepIndex ? 'u-text-main' : 'u-text-muted'">
                        {{ step.title }}
                      </span>
                    </div>
                    <div v-if="idx < workflowSteps.length - 1" class="u-w-10 u-h-px u-bg-slate-200"></div>
                  </li>
                </ul>
              </nav>

              <!-- Form Body -->
              <div class="card u-p-10 shadow-2xl border-0 u-rounded-[2.5rem]">
                <form @submit.prevent="submitStep" class="u-flex u-flex-col u-gap-8">
                  <div class="u-grid u-gap-8 lg:u-grid-cols-2">
                    <div v-for="field in currentStep.fields" :key="field.name" class="u-flex u-flex-col u-gap-2">
                      <label :for="field.name" class="u-text-sm u-font-black u-text-main u-uppercase u-tracking-widest flex items-center gap-2">
                        {{ field.label }}
                        <span v-if="field.help" class="u-cursor-help u-text-muted" :title="field.help">
                          <i class="bi bi-info-circle-fill"></i>
                        </span>
                      </label>
                      <component :is="field.component" v-model="formData[field.name]" v-bind="field.props" :id="field.name" 
                        class="u-p-4 u-border-2 u-border-slate-100 u-rounded-2xl u-bg-slate-50 focus:u-border-primary focus:u-bg-white transition-all outline-none"></component>
                    </div>
                  </div>
                  
                  <div class="u-flex u-justify-between u-items-center u-mt-10 u-pt-10 u-border-t u-border-slate-100">
                    <button type="button" @click="currentStepIndex--" :disabled="currentStepIndex === 0" 
                      class="button button--secondary button--pill px-10 u-font-black u-text-[10px] u-uppercase disabled:u-opacity-30">
                      Previous Step
                    </button>
                    <button type="submit" class="button button--primary button--pill px-12 py-4 shadow-xl hover:-translate-y-1 transition-all u-font-black u-text-xs u-uppercase">
                      {{ isLastStep ? 'Submit Application' : 'Continue to next stage' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>


      <!-- STAFF OPERATIONS VIEW -->
      <section
        v-else-if="['officer', 'supervisor', 'registrar', 'mda_admin', 'employee', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR'].includes(user.role)"
        class="staff-portal">
        
        <!-- Contextual Operational Stats Row -->
        <div class="u-mb-8 u-grid u-grid-cols-1 md:u-grid-cols-3 u-gap-6">
          <div class="card card--glass u-p-6 u-flex u-items-center u-gap-6 shadow-xl border-0 u-rounded-3xl">
            <div class="u-w-14 u-h-14 u-bg-primary/10 u-rounded-2xl u-flex u-items-center u-justify-center u-text-primary">
              <i class="bi bi-person-workspace u-text-2xl"></i>
            </div>
            <div>
              <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">My Active Tasks</div>
              <div class="u-text-2xl u-font-black u-text-main">{{ filteredAssignedRequests.length }}</div>
            </div>
          </div>
          <div class="card card--glass u-p-6 u-flex u-items-center u-gap-6 shadow-xl border-0 u-rounded-3xl">
            <div class="u-w-14 u-h-14 u-bg-info/10 u-rounded-2xl u-flex u-items-center u-justify-center u-text-info">
              <i class="bi bi-globe u-text-2xl"></i>
            </div>
            <div>
              <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">Department Pool</div>
              <div class="u-text-2xl u-font-black u-text-main">{{ filteredUnassignedRequests.length }}</div>
            </div>
          </div>
          <div class="card card--glass u-p-6 u-flex u-items-center u-gap-6 shadow-xl border-0 u-rounded-3xl">
            <div class="u-w-14 u-h-14 u-bg-success/10 u-rounded-2xl u-flex u-items-center u-justify-center u-text-success">
              <i class="bi bi-gear-wide-connected u-text-2xl"></i>
            </div>
            <div>
              <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">Processing (System)</div>
              <div class="u-text-2xl u-font-black u-text-main">{{ processingRequests.length }}</div>
            </div>
          </div>
        </div>

        <div class="dashboard-layout">
          <!-- Sidebar Navigation -->
          <aside class="dashboard-sidebar">
            <div class="card card--glass overflow-hidden border-0 shadow-xl rounded-[2rem]">
              <div class="sidebar-nav py-6">
                <button @click="staffCurrentTab = 'workstation'" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-red-50/50 group"
                  :class="{ 'bg-red-50/80 border-l-4 border-primary': staffCurrentTab === 'workstation' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-primary group-hover:scale-110 transition-transform">
                    <i class="bi bi-inboxes-fill"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest" :class="staffCurrentTab === 'workstation' ? 'text-red-900' : 'text-slate-500'">Workstation</div>
                    <div class="text-[10px] text-slate-400 font-bold">My Personal Queue</div>
                  </div>
                </button>
                
                <button @click="staffCurrentTab = 'pool'" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-blue-50/50 group"
                  :class="{ 'bg-blue-50/80 border-l-4 border-info': staffCurrentTab === 'pool' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-info group-hover:scale-110 transition-transform">
                    <i class="bi bi-globe-central-south"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest" :class="staffCurrentTab === 'pool' ? 'text-blue-900' : 'text-slate-500'">
                      {{ ['GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR'].includes(user.role) ? 'Global Pool' : 'Dept. Pool' }}
                    </div>
                    <div class="text-[10px] text-slate-400 font-bold">
                      {{ ['GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR'].includes(user.role) ? 'Universal Backlog' : 'Section Inbox' }}
                    </div>
                  </div>
                </button>

                <div class="mx-6 my-4 border-t border-slate-100"></div>

                <button v-if="['supervisor', 'GLOBAL_SUPERVISOR', 'MDA_SUPERVISOR', 'mda_admin'].includes(user.role)"
                  @click="staffCurrentTab = 'analytics'" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-amber-50/50 group"
                  :class="{ 'bg-amber-50/80 border-l-4 border-amber-600': staffCurrentTab === 'analytics' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-amber-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-graph-up-arrow"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest" :class="staffCurrentTab === 'analytics' ? 'text-amber-900' : 'text-slate-500'">Oversight</div>
                    <div class="text-[10px] text-slate-400 font-bold">Analytics & SLA</div>
                  </div>
                </button>

                <button @click="staffCurrentTab = 'directory'" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-slate-50/50 group"
                  :class="{ 'bg-slate-50/80 border-l-4 border-slate-600': staffCurrentTab === 'directory' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-slate-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-diagram-3-fill"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest" :class="staffCurrentTab === 'directory' ? 'text-slate-900' : 'text-slate-500'">Directory</div>
                    <div class="text-[10px] text-slate-400 font-bold">WOG Catalogue</div>
                  </div>
                </button>

                <button v-if="user.role === 'mda_admin'" @click="staffCurrentTab = 'configuration'"
                  class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-emerald-50/50 group"
                  :class="{ 'bg-emerald-50/80 border-l-4 border-emerald-600': staffCurrentTab === 'configuration' }">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-ui-checks-grid"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest"
                      :class="staffCurrentTab === 'configuration' ? 'text-emerald-900' : 'text-slate-500'">Service Configuration</div>
                    <div class="text-[10px] text-slate-400 font-bold">Forms & Workflows</div>
                  </div>
                </button>

                <div class="mx-6 my-4 border-t border-slate-100"></div>

                <router-link to="/repository/artifacts" class="sidebar-nav__item px-6 py-4 flex items-center gap-4 transition-all hover:bg-emerald-50/50 group">
                  <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-transform">
                    <i class="bi bi-bank2"></i>
                  </div>
                  <div class="flex-1 text-left">
                    <div class="text-xs font-black uppercase tracking-widest text-slate-500">EDRMS</div>
                    <div class="text-[10px] text-slate-400 font-bold">Electronic Records</div>
                  </div>
                </router-link>
              </div>
            </div>
            
            <!-- Support Card -->
            <div class="mt-8 px-2">
               <div class="p-6 rounded-[2rem] bg-slate-900 text-white relative overflow-hidden group shadow-2xl">
                  <div class="absolute -top-10 -right-10 w-32 h-32 bg-white/5 rounded-full group-hover:scale-150 transition-transform duration-700"></div>
                  <h4 class="text-[10px] font-black uppercase tracking-widest mb-2 opacity-60">Operations Unit</h4>
                  <p class="text-xs font-bold mb-6 leading-relaxed">Registry helpdesk is active for all institutional officers.</p>
                  <button class="w-full bg-white/10 hover:bg-white/20 border border-white/20 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all">
                    Internal Portal Docs
                  </button>
               </div>
            </div>
          </aside>

          <!-- Main Content -->
          <div class="dashboard-content">
            
            <!-- Workstation Tab -->
            <div v-if="staffCurrentTab === 'workstation'" class="tab-content u-flex-col u-gap-8">
               <div class="card overflow-hidden border-0 shadow-xl rounded-3xl">
                  <header class="u-p-6 u-bg-white u-border-b u-flex u-justify-between u-items-center">
                    <div>
                      <h2 class="u-text-lg u-font-black u-text-main u-uppercase u-tracking-widest flex items-center gap-3">
                        <i class="bi bi-person-workspace u-text-primary"></i> My Active Production Queue
                      </h2>
                      <p class="u-text-xs u-text-muted font-bold uppercase tracking-widest">Authenticated Workstation ID: {{ user.id }}</p>
                    </div>
                    <div class="u-flex u-gap-2">
                      <div class="toolbar__filter-group u-bg-slate-50">
                        <i class="bi bi-search toolbar__filter-icon"></i>
                        <input type="text" v-model="queueSearchQuery" placeholder="Filter my queue..." class="toolbar__filter-input">
                      </div>
                    </div>
                  </header>
                  
                  <div class="card__body u-p-0">
                    <div v-if="filteredAssignedRequests.length === 0" class="u-p-20 u-text-center">
                      <div class="u-w-20 u-h-20 u-bg-success/10 u-rounded-full u-flex u-items-center u-justify-center u-mx-auto u-mb-6">
                        <i class="bi bi-check2-circle u-text-4xl u-text-success"></i>
                      </div>
                      <h3 class="u-text-base u-font-black u-text-main u-uppercase u-tracking-widest">Workstation Clear</h3>
                      <p class="u-text-xs u-text-muted u-mt-2">No active tasks assigned. Switch to Dept. Pool to acquire new items.</p>
                    </div>
                    
                    <div v-else class="u-divide-y u-divide-slate-100">
                      <!-- Active Human Action Tasks -->
                      <div v-for="request in actionableRequests" :key="request.id" 
                        class="u-p-6 hover:u-bg-slate-50/50 transition-all u-flex u-flex-col md:u-flex-row u-gap-6 u-items-start md:u-items-center border-l-4 border-l-primary">
                        <div class="u-flex-1">
                          <div class="u-flex u-items-center u-gap-3 u-mb-3">
                            <span class="badge" :class="priorityClass(request.priority)">{{ request.priority }}</span>
                            <span class="u-text-sm u-font-black u-text-main uppercase tracking-tight">{{ request.service_config.service_name }}</span>
                            <span class="u-text-[10px] u-font-mono u-bg-slate-100 u-px-2 u-py-0.5 u-rounded">#{{ request.request_id }}</span>
                          </div>
                          <div class="u-flex u-flex-wrap u-gap-4 u-items-center u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">
                            <div class="u-flex u-items-center u-gap-1.5"><i class="bi bi-diagram-3"></i> {{ request.current_step?.step_name }}</div>
                            <div class="u-flex u-items-center u-gap-1.5"><i class="bi bi-building"></i> {{ getMdaName(request.service_config.mda) }}</div>
                            <div class="u-flex u-items-center u-gap-1.5" :class="getTimeInQueue(request.created_at).variant">
                              <i class="bi bi-clock-history"></i> {{ getTimeInQueue(request.created_at).label }}
                            </div>
                          </div>
                        </div>
                        <div class="u-flex u-gap-3">
                          <button @click="openCompleteStepModal(request)" class="button button--primary button--small button--pill shadow-lg hover:-translate-y-0.5 transition-all u-px-6">
                            Execute Task
                          </button>
                          <button @click="releaseTask(request.id)" class="button button--secondary button--small button--pill border-dashed" title="Release to Pool">
                            <i class="bi bi-arrow-left-circle"></i>
                          </button>
                        </div>
                      </div>

                      <!-- System Processing Tasks -->
                      <div v-for="request in processingRequests" :key="request.id" 
                        class="u-p-6 u-bg-slate-50/30 opacity-70 grayscale-[0.5] hover:grayscale-0 hover:opacity-100 transition-all u-flex u-flex-col md:u-flex-row u-gap-6 u-items-start md:u-items-center">
                        <div class="u-flex-1">
                          <div class="u-flex u-items-center u-gap-3 u-mb-3">
                            <span class="badge badge--secondary u-scale-90">SYSTEM</span>
                            <span class="u-text-sm u-font-bold u-text-slate-500 uppercase tracking-tight">{{ request.service_config.service_name }}</span>
                            <span class="u-text-[10px] u-font-mono u-bg-slate-100/50 u-px-2 u-py-0.5 u-rounded">#{{ request.request_id }}</span>
                          </div>
                          <div class="u-flex u-flex-wrap u-gap-4 u-items-center u-text-[10px] u-font-bold u-text-slate-400 u-uppercase u-tracking-widest">
                            <div class="u-flex u-items-center u-gap-1.5"><i class="bi bi-gear-wide-connected animate-spin"></i> {{ request.current_step?.step_name || 'KeSEL Background Engine' }}</div>
                            <div class="u-flex u-items-center u-gap-1.5"><i class="bi bi-clock"></i> Established {{ new Date(request.created_at).toLocaleDateString() }}</div>
                          </div>
                        </div>
                        <button disabled class="button button--secondary button--small button--pill u-opacity-50 u-cursor-not-allowed u-text-[10px]">
                          Syncing Backend...
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <footer v-if="staffStore.assignedMeta.count > 0" class="u-p-4 u-bg-slate-50/50 u-border-t u-flex u-justify-between u-items-center">
                     <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Loaded {{ filteredAssignedRequests.length }} of {{ staffStore.assignedMeta.count }} total</div>
                     <div class="u-flex u-gap-2">
                       <button @click="fetchAssignedRequests(assignedPage - 1)" :disabled="!staffStore.assignedMeta.previous" class="button button--secondary button--tiny button--pill px-4">Prev</button>
                       <button @click="fetchAssignedRequests(assignedPage + 1)" :disabled="!staffStore.assignedMeta.next" class="button button--secondary button--tiny button--pill px-4">Next</button>
                     </div>
                  </footer>
               </div>
            </div>

            <!-- Pool Tab -->
            <div v-else-if="staffCurrentTab === 'pool'" class="tab-content u-flex-col u-gap-8">
               <div class="card overflow-hidden border-0 shadow-xl rounded-3xl">
                  <header class="u-p-6 u-bg-white u-border-b u-flex u-justify-between u-items-center">
                    <div>
                      <h2 class="u-text-lg u-font-black u-text-main u-uppercase u-tracking-widest flex items-center gap-3">
                        <i class="bi bi-globe u-text-info"></i> National Task Reservoir
                      </h2>
                      <p class="u-text-xs u-text-muted font-bold uppercase tracking-widest">Universal unassigned backlog pool</p>
                    </div>
                    <div class="toolbar__filter-group u-bg-slate-50">
                      <i class="bi bi-search toolbar__filter-icon"></i>
                      <input type="text" v-model="unassignedSearchQuery" placeholder="Scan pool..." class="toolbar__filter-input">
                    </div>
                  </header>

                  <div class="table-container">
                    <table class="table">
                      <thead>
                        <tr class="table__header-row u-bg-slate-50/50">
                          <th class="table__header-cell u-py-4">Service Cluster</th>
                          <th class="table__header-cell">Priority</th>
                          <th class="table__header-cell">Time in Pool</th>
                          <th class="table__header-cell u-text-right">Acquisition</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="request in filteredUnassignedRequests" :key="request.id" class="table__row hover:u-bg-blue-50/20">
                          <td class="table__cell">
                            <div class="u-font-black u-text-main u-text-xs uppercase">{{ request.service_config.service_name }}</div>
                            <div class="u-text-[10px] u-text-primary u-font-black u-uppercase u-mt-1">{{ request.current_step?.step_name }}</div>
                          </td>
                          <td class="table__cell">
                            <span class="badge" :class="priorityClass(request.priority)">{{ request.priority }}</span>
                          </td>
                          <td class="table__cell">
                            <span class="badge badge--secondary u-text-[10px]" :class="getTimeInQueue(request.created_at).variant">
                              {{ getTimeInQueue(request.created_at).label }}
                            </span>
                          </td>
                          <td class="table__cell u-text-right">
                             <button @click="claimTask(request.id)" :disabled="claimingId === request.id" class="button button--primary button--tiny button--pill u-px-4">
                               <i class="bi bi-plus-lg u-mr-1"></i> Claim Task
                             </button>
                          </td>
                        </tr>
                        <tr v-if="filteredUnassignedRequests.length === 0">
                          <td colspan="4" class="u-p-20 u-text-center u-text-muted u-font-bold u-uppercase u-tracking-widest u-text-[10px]">
                            Pool is completely synchronized. No backlog found.
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <footer v-if="staffStore.unassignedMeta.count > 0" class="u-p-4 u-bg-slate-50/50 u-border-t u-flex u-justify-between u-items-center">
                    <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Total Global Pool: {{ staffStore.unassignedMeta.count }} items</div>
                    <div class="u-flex u-gap-2">
                       <button @click="fetchUnassignedRequests(unassignedPage - 1)" :disabled="!staffStore.unassignedMeta.previous" class="button button--secondary button--tiny button--pill px-4">Prev</button>
                       <button @click="fetchUnassignedRequests(unassignedPage + 1)" :disabled="!staffStore.unassignedMeta.next" class="button button--secondary button--tiny button--pill px-4">Next</button>
                    </div>
                  </footer>
               </div>
            </div>

            <!-- Oversight Tab -->
            <div v-else-if="staffCurrentTab === 'analytics'" class="tab-content u-flex-col u-gap-8">
               <div v-if="escalatedRequests.length > 0" class="card overflow-hidden border-0 shadow-xl rounded-3xl u-bg-amber-50">
                  <header class="u-p-6 u-flex u-justify-between u-items-center">
                    <div>
                      <h2 class="u-text-lg u-font-black u-text-amber-900 u-uppercase u-tracking-widest flex items-center gap-3">
                        <i class="bi bi-exclamation-triangle-fill"></i> Critical Escalations
                      </h2>
                      <p class="u-text-xs u-text-amber-700 font-bold uppercase tracking-widest">Requiring immediate supervisor intervention</p>
                    </div>
                    <span class="badge badge--danger animate-pulse">{{ escalatedRequests.length }} BLOCKED</span>
                  </header>
                  <div class="card__body u-p-0 u-px-6 u-pb-6">
                    <div class="u-flex u-flex-col u-gap-3">
                      <div v-for="req in escalatedRequests" :key="req.id" class="u-p-4 u-bg-white u-rounded-2xl u-flex u-justify-between u-items-center shadow-sm">
                        <div>
                          <div class="u-text-xs u-font-black u-text-main u-uppercase">{{ req.service_config.service_name }}</div>
                          <div class="u-text-[10px] u-text-muted u-font-bold u-mt-1">ID: #{{ req.request_id }} • Escalated by {{ req.assigned_to_details?.username || 'Officer' }}</div>
                        </div>
                        <button class="button button--secondary button--tiny button--pill border-amber-200">Review Block</button>
                      </div>
                    </div>
                  </div>
               </div>

               <ReportsDashboard />
            </div>

            <!-- Directory Tab -->
            <div v-else-if="staffCurrentTab === 'directory'" class="tab-content u-flex-col u-gap-8">
               <div class="card overflow-hidden border-0 shadow-xl rounded-3xl">
                  <header class="u-p-6 u-bg-slate-900 u-text-white u-flex u-justify-between u-items-center">
                    <div>
                      <h2 class="u-text-lg u-font-black u-uppercase u-tracking-widest flex items-center gap-3">
                        <i class="bi bi-diagram-3-fill u-text-primary"></i> WOG Service Blueprint
                      </h2>
                      <p class="u-text-xs u-text-slate-400 font-bold uppercase tracking-widest">Authoritative Registry Mapping tree</p>
                    </div>
                    <button @click="serviceConfigStore.fetchCatalogueSummary(true)" class="button button--secondary button--small button--pill text-white border-white/20">
                      Sync Clusters
                    </button>
                  </header>
                  
                  <div class="card__body u-p-8 u-bg-slate-50/50">
                    <div v-if="serviceConfigStore.loadingSummary" class="u-p-20 u-text-center">
                      <div class="animate-spin u-h-12 u-w-12 u-border-4 u-border-primary u-border-t-transparent u-rounded-full u-mx-auto mb-4"></div>
                      <p class="u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">Rebuilding Registry Model...</p>
                    </div>
                    
                    <div v-else class="wog-tree">
                      <div v-for="domain in serviceConfigStore.matrixData" :key="domain.domain_name" class="domain-group u-mb-12 last:mb-0">
                        <div class="u-flex u-items-center u-gap-4 u-mb-6">
                           <div class="u-h-8 u-w-1.5 u-bg-primary u-rounded-full"></div>
                           <h3 class="u-text-base u-font-black u-text-main u-uppercase u-tracking-widest">{{ domain.domain_name }}</h3>
                        </div>
                        
                        <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 lg:u-grid-cols-3 u-gap-6">
                          <div v-for="process in domain.processes" :key="process.process_name" class="card u-border-slate-100 shadow-sm hover:shadow-md transition-all rounded-2xl overflow-hidden">
                            <div class="u-p-4 u-bg-slate-50 u-border-b u-flex u-items-center u-gap-2">
                               <i class="bi bi-tags-fill u-text-primary u-text-xs"></i>
                               <h4 class="u-text-[10px] u-font-black u-text-main u-uppercase u-tracking-widest">{{ process.process_name }}</h4>
                            </div>
                            <div class="u-p-4 u-flex u-flex-col u-gap-3">
                               <div v-for="svc in process.services" :key="svc.service_name" class="u-p-3 u-rounded-xl u-bg-white u-border u-border-slate-50 u-flex u-justify-between u-items-center">
                                  <div class="u-min-w-0">
                                     <div class="u-text-[11px] u-font-bold u-text-main u-truncate mr-2">{{ svc.service_name }}</div>
                                     <div class="u-text-[9px] u-text-muted u-font-black u-uppercase u-mt-0.5">{{ svc.mda }}</div>
                                  </div>
                                  <div class="u-flex u-gap-1">
                                     <button @click="openBpmnModal(svc, 'as_is')" class="u-w-7 u-h-7 u-rounded-lg u-bg-slate-100 u-flex u-items-center u-justify-center hover:u-bg-primary-soft transition-colors" title="As-Is">
                                        <i class="bi bi-diagram-2 u-text-[10px]"></i>
                                     </button>
                                     <button @click="openBpmnModal(svc, 'to_be')" class="u-w-7 u-h-7 u-rounded-lg u-bg-primary/10 u-text-primary u-flex u-items-center u-justify-center hover:u-bg-primary hover:u-text-white transition-colors" title="To-Be">
                                        <i class="bi bi-lightning-charge u-text-[10px]"></i>
                                     </button>
                                  </div>
                               </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
               </div>
            </div>

            <!-- MDA-scoped Forms & Workflow Configuration -->
            <div v-else-if="staffCurrentTab === 'configuration' && user.role === 'mda_admin'" class="tab-content">
              <ServiceConfigManager :mda-filter-id="user.mda" :mda-details="user.mda_details" />
            </div>
          </div>
        </div>
      </section>

      <!-- Staff Catalogue Modal -->
      <BaseModal v-model:show="showStaffCatalogueModal" @close="showStaffCatalogueModal = false"
        :title="'Unified Service Catalogue'" size="full">
        <div class="u-p-6"
          style="max-height: 80vh; overflow-y: auto; background: var(--color-background); border-radius: 0.5rem;">
          <div class="tab-content animate-slide-in u-flex u-flex-col u-gap-8">
            <header class="page__header u-justify-between u-items-end u-mb-4 u-gap-4"
              style="border-bottom: 1px solid var(--color-border); padding-bottom: 1rem;">
              <div>
                <h2 class="page__title" style="font-size: 1.5rem">Unified Service Catalogue</h2>
                <p class="page__subtitle">Access authoritative G2C services through the secure Huduma Bridge</p>
              </div>
              <div class="toolbar u-w-full">
                <div class="toolbar__filters">
                  <!-- Search -->
                  <div class="toolbar__filter-group">
                    <i class="bi bi-search toolbar__filter-icon"></i>
                    <input type="text" v-model="serviceSearchQuery" placeholder="Search services..."
                      class="toolbar__filter-input">
                    <i v-if="serviceSearchQuery" @click="serviceSearchQuery = ''"
                      class="bi bi-x-circle-fill toolbar__clear-icon"></i>
                  </div>

                  <!-- Agency Filter -->
                  <div class="toolbar__filter-group">
                    <i class="bi bi-building toolbar__filter-icon"></i>
                    <input type="text" v-model="mdaSearchLocal" placeholder="Filter by Agency..."
                      @focus="showMdaDropdown = true" @blur="closeDropdownWithDelay('mda')"
                      class="toolbar__filter-input toolbar__filter-input--with-arrow">
                    <i class="bi bi-chevron-down toolbar__filter-arrow"
                      :class="{ 'toolbar__filter-arrow--open': showMdaDropdown }"></i>
                    <i v-if="mdaFilter" @click="selectMda('')"
                      class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                    <transition name="dropdown">
                      <div v-if="showMdaDropdown" class="dropdown-menu">
                        <div @click="selectMda('')" class="dropdown-item dropdown-item--header">All Agencies</div>
                        <div v-for="mda in filteredMdas" :key="mda.id" @click="selectMda(mda)" class="dropdown-item">
                          {{ mda.name }}
                        </div>
                      </div>
                    </transition>
                  </div>

                  <!-- Life Event Filter -->
                  <div class="toolbar__filter-group">
                    <i class="bi bi-calendar-event toolbar__filter-icon"></i>
                    <input type="text" v-model="lifeEventSearchLocal" placeholder="Filter by Life Event..."
                      @focus="showLifeEventDropdown = true" @blur="closeDropdownWithDelay('lifeEvent')"
                      class="toolbar__filter-input toolbar__filter-input--with-arrow">
                    <i class="bi bi-chevron-down toolbar__filter-arrow"
                      :class="{ 'toolbar__filter-arrow--open': showLifeEventDropdown }"></i>
                    <i v-if="lifeEventFilter" @click="selectLifeEvent('')"
                      class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>

                    <transition name="dropdown">
                      <div v-if="showLifeEventDropdown" class="dropdown-menu">
                        <div @click="selectLifeEvent('')" class="dropdown-item dropdown-item--header">All Life Events
                        </div>
                        <div v-for="event in filteredLifeEvents" :key="event" @click="selectLifeEvent(event)"
                          class="dropdown-item">
                          {{ event }}
                        </div>
                      </div>
                    </transition>
                  </div>

                  <!-- Family Filter -->
                  <div class="toolbar__filter-group">
                    <i class="bi bi-diagram-3-fill toolbar__filter-icon"></i>
                    <input type="text" v-model="familySearchLocal" placeholder="Filter by Family..."
                      @focus="showFamilyDropdown = true" @blur="closeDropdownWithDelay('family')"
                      class="toolbar__filter-input toolbar__filter-input--with-arrow">
                    <i class="bi bi-chevron-down toolbar__filter-arrow"
                      :class="{ 'toolbar__filter-arrow--open': showFamilyDropdown }"></i>
                    <i v-if="familyFilter" @click="selectFamily('')"
                      class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>
                    <transition name="dropdown">
                      <div v-if="showFamilyDropdown" class="dropdown-menu">
                        <div @click="selectFamily('')" class="dropdown-item dropdown-item--header">All Families</div>
                        <div v-for="fam in filteredFamilies" :key="fam" @click="selectFamily(fam)"
                          class="dropdown-item">
                          {{ fam }}
                        </div>
                      </div>
                    </transition>
                  </div>

                  <!-- Group Filter -->
                  <div class="toolbar__filter-group">
                    <i class="bi bi-collection toolbar__filter-icon"></i>
                    <input type="text" v-model="groupSearchLocal" placeholder="Filter by Group..."
                      @focus="showGroupDropdown = true" @blur="closeDropdownWithDelay('group')"
                      class="toolbar__filter-input toolbar__filter-input--with-arrow">
                    <i class="bi bi-chevron-down toolbar__filter-arrow"
                      :class="{ 'toolbar__filter-arrow--open': showGroupDropdown }"></i>
                    <i v-if="groupFilter" @click="selectGroup('')"
                      class="bi bi-x-circle-fill toolbar__clear-icon toolbar__clear-icon--with-arrow"></i>
                    <transition name="dropdown">
                      <div v-if="showGroupDropdown" class="dropdown-menu">
                        <div @click="selectGroup('')" class="dropdown-item dropdown-item--header">All Groups</div>
                        <div v-for="grp in filteredGroups" :key="grp" @click="selectGroup(grp)" class="dropdown-item">
                          {{ grp }}
                        </div>
                      </div>
                    </transition>
                  </div>

                  <!-- Reset Action -->
                  <button v-if="isAnyServiceFilterActive" @click="resetServiceFilters" class="btn-reset">
                    <i class="bi bi-arrow-counterclockwise"></i>
                    <span>Reset</span>
                  </button>
                </div>
              </div>
            </header>

            <!-- Active Filter Chips -->
            <transition-group name="list" tag="div" class="u-flex u-flex-wrap u-gap-2 u-mb-8">
              <div v-if="serviceSearchQuery" :key="'s-' + serviceSearchQuery" class="filter-chip"
                @click="serviceSearchQuery = ''">
                <span class="filter-chip__label">Search:</span>
                <span class="filter-chip__value">{{ serviceSearchQuery }}</span>
                <i class="bi bi-x"></i>
              </div>
              <div v-if="mdaFilter" :key="'m-' + mdaFilter" class="filter-chip" @click="selectMda('')">
                <span class="filter-chip__label">Agency:</span>
                <span class="filter-chip__value">{{ getMdaName(mdaFilter) }}</span>
                <i class="bi bi-x"></i>
              </div>
              <div v-if="lifeEventFilter" :key="'e-' + lifeEventFilter" class="filter-chip"
                @click="selectLifeEvent('')">
                <span class="filter-chip__label">Event:</span>
                <span class="filter-chip__value">{{ lifeEventFilter }}</span>
                <i class="bi bi-x"></i>
              </div>
              <div v-if="familyFilter" :key="'f-' + familyFilter" class="filter-chip" @click="selectFamily('')">
                <span class="filter-chip__label">Family:</span>
                <span class="filter-chip__value">{{ familyFilter }}</span>
                <i class="bi bi-x"></i>
              </div>
              <div v-if="groupFilter" :key="'g-' + groupFilter" class="filter-chip" @click="selectGroup('')">
                <span class="filter-chip__label">Group:</span>
                <span class="filter-chip__value">{{ groupFilter }}</span>
                <i class="bi bi-x"></i>
              </div>
            </transition-group>

            <div v-if="filteredAvailableServices.length === 0"
              class="u-flex u-flex-col u-items-center u-justify-center u-py-20 u-text-muted u-w-full">
              <i class="bi bi-cloud-slash u-text-5xl u-mb-4 u-opacity-20"></i>
              <p class="u-font-black u-uppercase u-tracking-widest u-text-xs">No services currently available</p>
              <p class="u-text-xs u-mt-2 u-opacity-60">The authoritative catalogue is being updated. Please check back
                shortly.</p>
            </div>
            <div v-else class="u-flex u-flex-col u-gap-12">
              <!-- If no family is selected and no other filters, show the list of families -->
              <div v-if="!selectedFamilyForView && !isAnyServiceFilterActive" class="stats-grid">
                <div v-for="group in groupedServicesByFamily" :key="group.name" @click="selectFamily(group.name)"
                  class="card u-p-8 u-flex u-flex-col u-items-center u-text-center transition-all hover:u-shadow-xl u-cursor-pointer"
                  style="border: 1px solid var(--border-color);">
                  <div class="u-flex u-items-center u-justify-center u-mb-6 u-rounded-lg"
                    style="width: 4rem; height: 4rem; background: var(--color-primary-soft); color: var(--color-primary); font-size: 1.5rem;">
                    <i :class="getServiceFamilyIcon(group.name)"></i>
                  </div>
                  <h3 class="u-font-bold u-text-main u-mb-2" style="font-size: 1.125rem;">{{ group.name }}</h3>
                  <p class="u-text-xs u-text-muted u-mb-4 u-line-clamp-2" style="min-height: 2.5rem;">{{
                    group.family?.description || 'View all associated services' }}</p>
                  <div class="u-mt-auto">
                    <span class="badge badge--info">{{ group.services.length }} Services</span>
                  </div>
                </div>
              </div>

              <!-- If a family is selected or filters are active, show services directly -->
              <div v-else class="service-family-group animate-slide-in">
                <div class="u-flex u-items-center u-justify-between u-mb-6">
                  <div class="u-flex u-items-center u-gap-3">
                    <button @click="resetServiceFiltersAndView" class="button button--ghost button--small u-mr-2">
                      <i class="bi bi-arrow-left"></i> Back to Families
                    </button>
                    <div class="u-w-1 u-h-8 u-bg-primary u-rounded-full"></div>
                    <div>
                      <h3 class="u-text-lg u-font-black u-text-main u-uppercase u-tracking-widest">{{
                        selectedFamilyForView || 'Filtered Search Results' }}</h3>
                    </div>
                  </div>
                </div>

                <div class="stats-grid">
                  <div
                    v-for="service in (selectedFamilyForView ? (groupedServicesByFamily.find(g => g.name === selectedFamilyForView)?.services || []) : filteredAvailableServices)"
                    :key="service.id"
                    class="card u-p-8 u-flex u-flex-col u-items-center u-text-center transition-all hover:u-shadow-xl"
                    style="border: none;">
                    <div class="u-flex u-items-center u-justify-center u-mb-6 u-rounded-lg"
                      style="width: 4rem; height: 4rem; background: var(--color-primary-soft); color: var(--color-primary); font-size: 1.5rem;">
                      <i :class="getServiceFamilyIcon(service.service_family_details?.name)"></i>
                    </div>
                    <h3 class="u-font-bold u-text-main u-mb-2" style="font-size: 1.125rem;">{{ service.service_name }}
                    </h3>
                    <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-mb-8 u-p-1 u-rounded"
                      style="background: var(--color-background-alt); letter-spacing: 0.1em;">
                      {{ getMdaName(service.mda) }}
                    </p>
                    <router-link :to="`/apply/${service.service_code}`"
                      class="button button--primary button--pill u-w-full u-mt-auto">
                      Begin Application
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </BaseModal>

      <!-- BPMN Visualization Modal -->
      <BaseModal v-model:show="showBpmnModal" @close="closeBpmnModal" size="full" headerClass="modal__header--dark">
        <template #header>
          <div class="u-flex-1">
            <h3 class="modal__title">{{ selectedServiceForBpmn?.service_name }}</h3>
            <p class="modal__subtitle u-font-mono u-uppercase" style="letter-spacing: 0.1em">Authoritative BPMN 2.0 Process orchestration Model</p>
          </div>

          <div class="tab-bar" style="background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.1)">
            <button @click="activeBpmnStage = 'as_is'" :class="{ 'tab-bar__item--active': activeBpmnStage === 'as_is' }"
              class="tab-bar__item u-text-xs u-py-1.5" style="border: none">
              As-Is Manual Friction
            </button>
            <button @click="activeBpmnStage = 'to_be'" :class="{ 'tab-bar__item--active': activeBpmnStage === 'to_be' }"
              class="tab-bar__item u-text-xs u-py-1.5" style="border: none">
              To-Be Optimized Flow
            </button>
          </div>
        </template>

        <div class="u-flex u-justify-center u-p-6" style="background: var(--bg-page); min-height: 500px;">
          <BpmnRenderer 
            v-if="selectedServiceForBpmn" 
            :steps="selectedServiceForBpmn.workflow_steps?.filter(s => s.lifecycle_stage === activeBpmnStage) || []" 
            :stage="activeBpmnStage" 
            class="u-w-full"
          />
          <div v-else-if="!selectedServiceForBpmn?.workflow_configured" class="u-flex u-flex-col u-items-center u-justify-center u-text-muted">
            <i class="bi bi-exclamation-triangle u-text-5xl mb-4"></i>
            <p class="u-font-bold">No workflow configured for this service.</p>
          </div>
        </div>

        <template #footer>
          <div class="u-text-xs u-text-muted u-font-mono" style="font-style: italic">
            Source: Unified Governance Registry | Level: {{ activeBpmnStage === 'to_be' ? 'Optimized digital flow' : 'Documented current state' }}
          </div>
          <button @click="closeBpmnModal" class="button button--secondary button--pill">
            Exit Visualization
          </button>
        </template>
      </BaseModal>

      <!-- SYSTEM ADMINISTRATION VIEW -->
      <section v-if="['admin', 'system_admin'].includes(user.role)" class="admin-portal">
        <div class="dashboard-layout">
          <!-- Left Sidebar Navigation -->
          <aside class="dashboard-sidebar">
            <div class="card architecture-nav">
              <div class="card__body p-0">
                <header class="architecture-nav__header">
                  <span class="architecture-nav__eyebrow"><i class="bi bi-bounding-box-circles"></i> Platform map</span>
                  <strong>Reference Architecture</strong>
                  <small>Select a capability within each layer</small>
                </header>

                <div class="architecture-nav__stack">
                  <div v-for="group in adminTabGroups" :key="group.title"
                    class="architecture-nav__layer" :class="[`architecture-nav__layer--${group.tone}`, { 'is-active': group.tabs.some(tab => tab.name === currentTab) }]">
                    <div class="architecture-nav__layer-heading">
                      <span class="architecture-nav__number">{{ group.layer }}</span>
                      <span class="architecture-nav__layer-icon"><i :class="group.icon"></i></span>
                      <span>
                        <strong>{{ group.title }}</strong>
                        <small>{{ group.description }}</small>
                      </span>
                    </div>
                    <div class="architecture-nav__capabilities">
                      <button v-for="tab in group.tabs" :key="tab.name" @click="currentTab = tab.name" class="sidebar-nav__item"
                        :class="{ 'sidebar-nav__item--active': currentTab === tab.name }">
                        <i :class="tab.icon" class="sidebar-nav__capability-icon"></i>
                        <span class="sidebar-nav__text">{{ tab.name }}</span>
                        <i v-if="currentTab === tab.name" class="bi bi-chevron-right sidebar-nav__arrow"></i>
                      </button>
                    </div>
                  </div>
                </div>
                
                <div class="architecture-nav__foundation">
                  <div class="architecture-nav__foundation-title">
                    <i class="bi bi-layers-fill"></i>
                    <span><strong>Evidence & Records Plane</strong><small>Cross-platform foundation</small></span>
                  </div>
                  <div class="architecture-nav__foundation-links">
                    <router-link to="/repository/artifacts" class="sidebar-nav__item">
                      <i class="bi bi-bank2 sidebar-nav__capability-icon"></i>
                      <span class="sidebar-nav__text">EDRMS</span>
                      <i class="bi bi-box-arrow-up-right sidebar-nav__arrow opacity-50 text-[10px]"></i>
                    </router-link>
                    <button @click="currentTab = 'Technical Specs'" class="sidebar-nav__item"
                      :class="{ 'sidebar-nav__item--active': currentTab === 'Technical Specs' }">
                      <i class="bi bi-journal-richtext sidebar-nav__capability-icon"></i>
                      <span class="sidebar-nav__text">Technical Evidence</span>
                      <span class="architecture-nav__doc-count">30</span>
                      <i v-if="currentTab === 'Technical Specs'" class="bi bi-chevron-right sidebar-nav__arrow"></i>
                    </button>
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
                <component :is="activeAdminComponent" 
                  :active-tab="currentTab"
                  :mda-filter-id="selectedDrilldownMda?.id"
                  :service="selectedDrilldownService"
                  @drilldown-services="(mda) => { selectedDrilldownMda = mda }"
                  @drilldown-transactions="(svc) => { selectedDrilldownService = svc }"
                  @go-back-mdas="selectedDrilldownMda = null"
                  @go-back-services="selectedDrilldownService = null"
                />

                <div v-if="currentTab === 'Technical Specs'"
                  class="docs-workstation mt-8 border-t border-border-color pt-8">
                  <section class="architect-hero">
                    <div class="architect-hero__copy">
                      <span class="architect-eyebrow"><i class="bi bi-cpu-fill"></i> System Architect View</span>
                      <h2>Platform Architecture & Technical Evidence</h2>
                      <p>Inspect how channels, orchestration, interoperability, shared registries, and trust controls
                        work together as one government digital public infrastructure.</p>
                      <div class="architect-standards">
                        <span>GEA aligned</span><span>DPI architecture</span><span>API first</span><span>Zero-trust exchange</span>
                      </div>
                    </div>
                    <div class="architect-scorecard">
                      <article><strong>{{ architectureLayers.length }}</strong><small>Architecture layers</small></article>
                      <article><strong>5</strong><small>Shared DPI rails</small></article>
                      <article><strong>67</strong><small>Orchestrated services</small></article>
                      <article><strong>{{ technicalDocumentCount }}</strong><small>Evidence documents</small></article>
                    </div>
                  </section>

                  <section class="architect-blueprint" aria-labelledby="architecture-blueprint-title">
                    <header>
                      <div>
                        <span class="architect-section-kicker">Logical reference architecture</span>
                        <h3 id="architecture-blueprint-title">Trace the platform from channel to authoritative source</h3>
                      </div>
                      <span class="architect-live"><i class="bi bi-circle-fill"></i> POC architecture active</span>
                    </header>
                    <div class="architect-layer-flow">
                      <button v-for="(layer, index) in architectureLayers" :key="layer.id" type="button"
                        class="architect-layer" :class="[`architect-layer--${layer.id}`, { active: selectedDoc === layer.document }]"
                        @click="selectedDoc = layer.document">
                        <span class="architect-layer__number">0{{ index + 1 }}</span>
                        <span class="architect-layer__icon"><i :class="layer.icon"></i></span>
                        <strong>{{ layer.name }}</strong>
                        <small>{{ layer.description }}</small>
                        <span class="architect-layer__tech">{{ layer.technology }}</span>
                      </button>
                    </div>
                    <footer class="architect-cross-cutting">
                      <span><i class="bi bi-shield-lock-fill"></i> Security & NPKI</span>
                      <span><i class="bi bi-person-check-fill"></i> Identity & consent</span>
                      <span><i class="bi bi-journal-check"></i> Auditability</span>
                      <span><i class="bi bi-activity"></i> Observability</span>
                      <span><i class="bi bi-arrow-repeat"></i> Resilience & DR</span>
                    </footer>
                  </section>

                  <section class="architect-evidence">
                    <header class="architect-evidence__heading">
                      <div>
                        <span class="architect-section-kicker">Architecture decision evidence</span>
                        <h3>Technical documentation workbench</h3>
                      </div>
                      <span class="architect-document-count">{{ technicalDocumentCount }} controlled documents</span>
                    </header>
                    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
                    <!-- Documentation Navigation Sidebar -->
                    <aside class="architect-library lg:col-span-1 space-y-6">
                      <div class="architect-library__title">
                        <i class="bi bi-collection-fill"></i>
                        <div><strong>Evidence Library</strong><small>Select an artifact to inspect</small></div>
                      </div>
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
                    </aside>

                    <!-- Documentation Content Area -->
                    <div class="lg:col-span-3">
                      <header class="architect-document-header">
                        <div class="architect-document-header__icon"><i class="bi bi-file-earmark-code-fill"></i></div>
                        <div>
                          <span>{{ selectedDocMeta.category }}</span>
                          <h4>{{ selectedDocMeta.name }}</h4>
                          <code>{{ selectedDoc }}</code>
                        </div>
                        <span class="architect-format">{{ selectedDocFormat }}</span>
                      </header>
                      <div class="architect-document-viewer border border-border-color rounded-b-2xl overflow-hidden shadow-inner bg-white">
                        <DocViewer :url="`/${selectedDoc}`" />
                      </div>
                    </div>
                  </div>
                  </section>
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
      <div v-if="currentRequestToComplete" class="u-mb-6">
        <div class="u-flex u-items-center u-justify-between u-mb-4">
          <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Process Roadmap</div>
          <button @click="showBpmnBlueprint = !showBpmnBlueprint" type="button"
            class="button button--ghost button--small u-text-[10px] u-font-bold u-uppercase" style="padding: 2px 8px">
            <i class="bi" :class="showBpmnBlueprint ? 'bi-eye-slash' : 'bi-eye'"></i>
            {{ showBpmnBlueprint ? 'Hide Blueprint' : 'Show BPMN Blueprint' }}
          </button>
        </div>

        <div v-if="showBpmnBlueprint"
          class="u-mb-4 u-p-4 u-bg-bg-page u-rounded-xl u-border u-border-dashed u-border-primary/30 animate-fade-in">
          <div class="mermaid u-flex u-justify-center" ref="mermaidContainer"></div>
          <div class="u-text-[8px] u-text-center u-text-muted u-mt-2 u-italic">Generated from authoritative GOV-BPMN
            schema</div>
        </div>

        <div class="u-flex u-items-center u-gap-2 u-overflow-x-auto u-pb-2">
          <template v-for="(step, index) in sortedWorkflowSteps" :key="step.id">
            <div class="u-flex u-items-center u-gap-2">
              <div class="u-flex u-flex-col u-items-center u-gap-1" style="min-width: 80px">
                <div
                  class="u-w-6 u-h-6 u-rounded-full u-flex u-items-center u-justify-center u-text-[10px] u-font-bold transition-all"
                  :class="[
                    step.id === currentRequestToComplete.current_step?.id ? 'u-bg-primary u-text-white u-ring-4 u-ring-primary-soft' :
                      (step.sequence < currentRequestToComplete.current_step?.sequence ? 'u-bg-success u-text-white' : 'u-bg-slate-100 u-text-slate-400')
                  ]">
                  <i v-if="step.sequence < currentRequestToComplete.current_step?.sequence" class="bi bi-check"></i>
                  <span v-else>{{ step.sequence }}</span>
                </div>
                <div class="u-text-[8px] u-font-black u-uppercase u-text-center u-leading-tight"
                  :class="step.id === currentRequestToComplete.current_step?.id ? 'u-text-primary' : 'u-text-muted'">
                  {{ step.step_name }}
                </div>
              </div>
              <div v-if="index < sortedWorkflowSteps.length - 1" class="u-w-8 u-h-px u-bg-slate-200"></div>
            </div>
          </template>
        </div>
      </div>

      <form @submit.prevent="completeStep" class="form flex flex-col gap-6">
        <div class="u-p-4 u-bg-bg-page u-rounded-xl u-border u-border-border-color u-relative u-overflow-hidden">
          <div class="u-absolute u-top-0 u-left-0 u-w-1 u-h-full u-bg-primary"></div>
          <div class="u-text-[10px] u-font-black u-text-primary u-uppercase u-mb-3 flex items-center gap-2">
            <i class="bi bi-person-badge animate-pulse"></i> Active Disposition
          </div>
          <div class="form__group">
            <label class="form__label">Final Stage Outcome</label>
            <select v-model="stepAction.action" class="form__select w-full" required>
              <option value="" disabled>Select outcome...</option>
              <option value="approve">Approve & Advance Track</option>
              <option value="reject">Deny & Terminate</option>
              <option value="request_changes">Revert for Correction</option>
            </select>
          </div>
        </div>

        <div v-if="activeStepFormFields.length > 0" class="u-p-6 u-bg-slate-50 u-rounded-2xl u-border u-border-border-color/60">
          <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-4 flex items-center gap-2">
            <i class="bi bi-ui-checks-grid text-primary"></i> Data Engagement Fields
          </div>
          <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-6">
            <div v-for="fieldKey in activeStepFormFields" :key="fieldKey" class="form__group">
              <label class="form__label u-flex u-items-center u-gap-2">
                {{ getFieldTitle(fieldKey) }}
                <span v-if="isFieldRequired(fieldKey)" class="u-text-danger">*</span>
              </label>
              
              <!-- Simple Select Rendering -->
              <select v-if="getFieldSchema(fieldKey).enum" v-model="stepFormData[fieldKey]" class="form__select w-full" :required="isFieldRequired(fieldKey)">
                <option value="" disabled>Select option...</option>
                <option v-for="opt in getFieldSchema(fieldKey).enum" :key="opt" :value="opt">{{ opt }}</option>
              </select>
              
              <!-- Simple Toggle/Checkbox -->
              <div v-else-if="getFieldSchema(fieldKey).type === 'boolean'" class="u-flex u-items-center u-gap-3 u-p-3 u-bg-white u-border u-rounded-xl">
                 <input type="checkbox" v-model="stepFormData[fieldKey]" :id="'field-' + fieldKey" class="form__checkbox">
                 <label :for="'field-' + fieldKey" class="u-text-xs u-font-bold u-text-main cursor-pointer">Confirm {{ getFieldTitle(fieldKey) }}</label>
              </div>

              <!-- Standard Input -->
              <input v-else :type="getFieldSchema(fieldKey).type === 'number' ? 'number' : 'text'" 
                v-model="stepFormData[fieldKey]" class="form__input w-full" 
                :required="isFieldRequired(fieldKey)"
                :placeholder="'Enter ' + getFieldTitle(fieldKey) + '...'">
              
              <p v-if="getFieldSchema(fieldKey).description" class="u-text-[10px] u-text-muted u-mt-1">{{ getFieldSchema(fieldKey).description }}</p>
            </div>
          </div>
        </div>

        <div class="form__group">
          <label class="form__label">Registry Trail / Official Statement</label>
          <textarea v-model="stepAction.details" rows="3" class="form__textarea w-full"
            placeholder="Document findings or rationale for this stage outcome..."></textarea>
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
  import { ref, onMounted, computed, nextTick, watch } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import mermaid from 'mermaid';
  import { useAuthStore } from '../store/auth';
  import { useCitizenStore } from '../store/citizen';
  import { useMdaStore } from '../store/mda';
  import { useStaffStore } from '../store/staff';
  import { useServiceConfigStore } from '../store/serviceConfig';

  // Component Imports
  import ReportsDashboard from '../components/Supervisor/ReportsDashboard.vue';
  import MdaManager from '../components/Admin/MdaManager.vue';
  import ServiceConfigManager from '../components/Admin/ServiceConfigManager.vue';
  import WogDashboardStats from '../components/Admin/WogDashboardStats.vue';
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
  import ServiceTransactionsView from '../components/Admin/ServiceTransactionsView.vue';
  import BaseModal from '../components/Common/BaseModal.vue';
  
  // Citizen Premium Components
  import AuthoritativeWallet from '../components/Citizen/AuthoritativeWallet.vue';
  import ActionFeed from '../components/Citizen/ActionFeed.vue';
  import ServiceDiscovery from '../components/Citizen/ServiceDiscovery.vue';

  const authStore = useAuthStore();
  const citizenStore = useCitizenStore();
  const mdaStore = useMdaStore();
  const staffStore = useStaffStore();
  const serviceConfigStore = useServiceConfigStore();

  const user = computed(() => authStore.user);
  const availableServices = computed(() => citizenStore.availableServices);
  const myRequests = computed(() => citizenStore.myRequests);
  const claimingId = ref(null);
  const releasingId = ref(null);
  const processingId = ref(null);
  const actionFeedback = ref({ message: '', type: '' });
  const mdas = computed(() => mdaStore.mdas);

  const sortedWorkflowSteps = computed(() => {
    if (!currentRequestToComplete.value?.service_config?.workflow_steps) return [];
    const stage = currentRequestToComplete.value.current_step?.lifecycle_stage || 'as_is';
    return [...currentRequestToComplete.value.service_config.workflow_steps]
      .filter(s => s.lifecycle_stage === stage)
      .sort((a, b) => a.sequence - b.sequence);
  });

  const assignedRequests = computed(() => staffStore.assignedRequests);
  const unassignedRequests = computed(() => staffStore.unassignedRequests);
  const teamRequests = computed(() => staffStore.teamRequests);
  const escalatedRequests = computed(() => staffStore.escalatedRequests);

  const showCompleteStepModal = ref(false);
  const showStaffCatalogueModal = ref(false);
  const showBpmnModal = ref(false);
  const selectedServiceForBpmn = ref(null);
  const activeBpmnStage = ref('as_is');
  const currentRequestToComplete = ref(null);
  const stepAction = ref({ action: '', details: '' });
  const stepFormData = ref({});
  const showBpmnBlueprint = ref(false);
  const mermaidContainer = ref(null);

  const activeStepFormFields = computed(() => {
    return currentRequestToComplete.value?.current_step?.api_config?.form_fields || [];
  });

  const getServiceSchema = (request) => {
    const config = request?.service_config?.config || {};
    return config.rules?.schema?.properties || {};
  };

  const getFieldSchema = (fieldKey) => {
    const properties = getServiceSchema(currentRequestToComplete.value);
    return properties[fieldKey] || {};
  };

  const getFieldTitle = (fieldKey) => {
    return getFieldSchema(fieldKey).title || fieldKey;
  };

  const isFieldRequired = (fieldKey) => {
    const schema = currentRequestToComplete.value?.service_config?.config?.rules?.schema || {};
    return schema.required?.includes(fieldKey);
  };

  const mermaidDefinition = computed(() => {
    if (!currentRequestToComplete.value) return '';
    const steps = sortedWorkflowSteps.value;

    let graph = 'graph TD;\n';
    steps.forEach((step, index) => {
      const nodeId = `S${step.sequence}`;
      const safeLabel = step.step_name.replace(/"/g, "'");
      let bType = step.bpmn_element_type || 'user_task';

      const isActive = step.id === currentRequestToComplete.value.current_step?.id;
      const isPast = step.sequence < currentRequestToComplete.value.current_step?.sequence;

      if (bType === 'start_event') {
        graph += `    ${nodeId}(("${safeLabel}"))\n`;
        graph += `    class ${nodeId} startEvent;\n`;
      } else if (bType === 'end_event') {
        graph += `    ${nodeId}(("${safeLabel}"))\n`;
        graph += `    class ${nodeId} endEvent;\n`;
      } else if (bType === 'exclusive_gateway') {
        graph += `    ${nodeId}{{"${safeLabel}"}}\n`;
        graph += `    class ${nodeId} gateway;\n`;
      } else if (bType === 'service_task') {
        graph += `    ${nodeId}[["${safeLabel}<br/>(System)"]]\n`;
        graph += `    class ${nodeId} serviceTask;\n`;
      } else {
        graph += `    ${nodeId}["${safeLabel}<br/>(${step.role})"]\n`;
        graph += `    class ${nodeId} userTask;\n`;
      }

      if (isActive) graph += `    class ${nodeId} activeStep;\n`;
      if (isPast) graph += `    class ${nodeId} pastStep;\n`;

      if (index < steps.length - 1) {
        const nextStep = steps[index + 1];
        const nextNodeId = `S${nextStep.sequence}`;
        graph += `    ${nodeId} --> ${nextNodeId}\n`;
      }
    });

    graph += '    classDef startEvent fill:#f0fdf4,stroke:#16a34a,stroke-width:2px;\n';
    graph += '    classDef endEvent fill:#fef2f2,stroke:#dc2626,stroke-width:2px;\n';
    graph += '    classDef gateway fill:#fff7ed,stroke:#c2410c,stroke-width:2px;\n';
    graph += '    classDef userTask fill:#eff6ff,stroke:#2563eb,stroke-width:1px;\n';
    graph += '    classDef serviceTask fill:#faf5ff,stroke:#7c3aed,stroke-width:1px,stroke-dasharray: 5 5;\n';
    graph += '    classDef activeStep stroke:#ec232a,stroke-width:4px,filter:drop-shadow(0 0 5px rgba(236,35,42,0.5));\n';
    graph += '    classDef pastStep opacity:0.5;\n';

    return graph;
  });

  watch(showBpmnBlueprint, async (val) => {
    if (val) {
      await nextTick();
      if (mermaidContainer.value) {
        mermaidContainer.value.removeAttribute('data-processed');
        mermaidContainer.value.innerHTML = mermaidDefinition.value;
        try {
          await mermaid.run({ nodes: [mermaidContainer.value] });
        } catch (e) {
          console.error('Mermaid error', e);
        }
      }
    }
  });

  const serviceSearchQuery = ref('');
  const requestSearchQuery = ref('');
  const queueSearchQuery = ref('');
  const unassignedSearchQuery = ref('');
  const incompleteSearchQuery = ref('');
  const myRequestsStatusFilter = ref('');
  const citizenCurrentTab = ref('inbox');
  const staffCurrentTab = ref('workstation');
  
  // Missing logic for new citizen portal
  const pendingActions = computed(() => {
    const actions = [];
    myRequests.value.filter(r => r.status === 'request_changes').forEach(r => {
      actions.push({
        id: `action-req-${r.id}`,
        type: 'danger',
        icon: 'bi-exclamation-triangle-fill',
        title: 'Action Required',
        message: `Changes requested on your ${r.service_config.service_name} application.`,
        date: r.updated_at,
        link: `/service-request/${r.id}`
      });
    });
    if (user.value?.saved_documents?.length) {
       actions.push({
         id: 'system-wallet',
         type: 'success',
         icon: 'bi-shield-check',
         title: 'Wallet Active',
         message: `You have ${user.value.saved_documents.length} authoritative documents ready for use.`,
         date: new Date().toISOString(),
         link: '/profile',
         isSystem: true
       });
    }
    return actions.sort((a, b) => new Date(b.date) - new Date(a.date));
  });

  const activeApplications = computed(() => {
    return myRequests.value.filter(r => ['received', 'in_progress', 'payment_pending', 'verification_pending'].includes(r.status)).map(r => ({
      id: r.id,
      service_name: r.service_config.service_name,
      mda_name: getMdaName(r.service_config.mda),
      current_step_index: r.current_step?.sequence || 1,
      total_steps: r.service_config.workflow_steps?.length || 5,
      current_step_name: r.current_step?.step_name || 'Processing'
    }));
  });

  const lifeEvents = computed(() => {
    const groups = {};
    availableServices.value.forEach(svc => {
      const gName = svc.life_event_group || 'General Services';
      if (!groups[gName]) {
        groups[gName] = {
          id: gName.toLowerCase().replace(/\s+/g, '-'),
          name: gName,
          description: `Authoritative G2C services for ${gName.toLowerCase()}.`,
          services: []
        };
      }
      groups[gName].services.push({
        id: svc.service_code,
        display_name: svc.service_name,
        mda: svc.mda
      });
    });
    return Object.values(groups);
  });

  const selectedService = ref(null);
  const currentStepIndex = ref(0);
  const formData = ref({});
  const workflowSteps = computed(() => selectedService.value?.workflow_steps || []);
  const currentStep = computed(() => workflowSteps.value[currentStepIndex.value] || {});
  const isLastStep = computed(() => currentStepIndex.value === workflowSteps.value.length - 1);

  const submitStep = async () => {
    if (isLastStep.value) {
      citizenCurrentTab.value = 'inbox';
    } else {
      currentStepIndex.value++;
    }
  };

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
  const lifeEventFilter = ref('');
  const familyFilter = ref('');
  const groupFilter = ref('');
  const selectedFamilyForView = ref(null);

  const mdaSearchLocal = ref('');
  const lifeEventSearchLocal = ref('');
  const familySearchLocal = ref('');
  const groupSearchLocal = ref('');
  const showMdaDropdown = ref(false);
  const showLifeEventDropdown = ref(false);
  const showFamilyDropdown = ref(false);
  const showGroupDropdown = ref(false);

  const selectLifeEvent = (val) => {
    lifeEventFilter.value = val;
    lifeEventSearchLocal.value = val;
    showLifeEventDropdown.value = false;
  };

  const selectFamily = (val) => {
    familyFilter.value = val;
    familySearchLocal.value = val;
    showFamilyDropdown.value = false;
  };

  const selectGroup = (val) => {
    groupFilter.value = val;
    groupSearchLocal.value = val;
    showGroupDropdown.value = false;
  };

  const resetServiceFilters = () => {
    mdaFilter.value = '';
    lifeEventFilter.value = '';
    familyFilter.value = '';
    groupFilter.value = '';
    serviceSearchQuery.value = '';
    mdaSearchLocal.value = '';
    lifeEventSearchLocal.value = '';
    familySearchLocal.value = '';
    groupSearchLocal.value = '';
  };

  const resetServiceFiltersAndView = () => {
    resetServiceFilters();
    selectedFamilyForView.value = null;
  };

  const isAnyServiceFilterActive = computed(() => {
    return mdaFilter.value || lifeEventFilter.value || familyFilter.value || groupFilter.value || serviceSearchQuery.value;
  });

  const filteredLifeEvents = computed(() => {
    if (!lifeEventSearchLocal.value) return uniqueLifeEvents.value;
    const q = lifeEventSearchLocal.value.toLowerCase();
    return uniqueLifeEvents.value.filter(e => e.toLowerCase().includes(q));
  });

  const filteredFamilies = computed(() => {
    if (!familySearchLocal.value) return uniqueFamilies.value;
    const q = familySearchLocal.value.toLowerCase();
    return uniqueFamilies.value.filter(f => f.toLowerCase().includes(q));
  });

  const filteredGroups = computed(() => {
    if (!groupSearchLocal.value) return uniqueGroups.value;
    const q = groupSearchLocal.value.toLowerCase();
    return uniqueGroups.value.filter(g => g.toLowerCase().includes(q));
  });
  const mdaIncompleteRequests = computed(() => staffStore.mdaIncompleteRequests);

  const uniqueLifeEvents = computed(() => {
    const events = availableServices.value.map(s => s.life_event_group).filter(Boolean);
    return [...new Set(events)].sort();
  });

  const uniqueFamilies = computed(() => {
    const fams = availableServices.value.map(s => s.service_family_details?.name || s.service_family).filter(Boolean);
    return [...new Set(fams.map(String))].sort();
  });

  const uniqueGroups = computed(() => {
    const grps = [];
    availableServices.value.forEach(s => {
      if (s.service_group_details) {
        s.service_group_details.forEach(g => grps.push(g.name));
      }
    });
    return [...new Set(grps)].sort();
  });

  const filteredMdas = computed(() => {
    if (!mdaSearchLocal.value) return mdas.value;
    const q = mdaSearchLocal.value.toLowerCase();
    return mdas.value.filter(m => m.name.toLowerCase().includes(q));
  });

  const actionableRequests = computed(() => {
    return sortRequestsByUrgency(filteredAssignedRequests.value.filter(r => getActionState(r) === 'action_required'));
  });

  const processingRequests = computed(() => {
    return filteredAssignedRequests.value.filter(r => getActionState(r) !== 'action_required');
  });

  const getMdaName = (mdaId) => {
    if (!mdaId) return 'All Agencies';
    if (mdaId && typeof mdaId === 'object') return mdaId.name;
    const mda = mdas.value.find(m => String(m.id) === String(mdaId));
    return mda ? mda.name : `Agency #${mdaId}`;
  }

  const getServiceFamilyIcon = (familyName) => {
    const icons = {
      'Identity & Civil Registration': 'bi-person-badge-fill',
      'Civil Registration & Identity': 'bi-person-badge-fill',
      'Immigration & Border Management': 'bi-passport',
      'Business & Commercial Regulation': 'bi-briefcase-fill',
      'Taxation & Revenue Administration': 'bi-bank2',
      'Social Protection & Welfare': 'bi-heart-pulse-fill',
      'Education & Skills Development': 'bi-mortarboard-fill',
      'Health & Public Health Regulation': 'bi-capsule',
      'Land, Housing & Property Administration': 'bi-house-heart-fill',
      'Justice & Legal Services': 'bi-scales',
      'Security & Public Safety': 'bi-shield-shaded',
      'Trade, Industry & Investment': 'bi-graph-up-arrow',
      'Environmental & Natural Resources': 'bi-tree-fill',
      'Transport & Mobility': 'bi-truck',
      'Public Finance & Procurement': 'bi-cash-coin',
      'Governance & Intergovernmental Coordination': 'bi-building-fill',
      'Tourism, Heritage & Sports': 'bi-palette-fill',
      'Uncategorized': 'bi-grid-fill'
    };
    return icons[familyName] || 'bi-grid-fill';
  };

  const getEventIcon = (eventName) => {
    const icons = {
      'Getting Married': 'bi-heart-fill',
      'Starting a Business': 'bi-briefcase-fill',
      'Buying Property': 'bi-house-fill',
      'Having a Child': 'bi-baby-carriage',
      'Education': 'bi-mortarboard-fill',
      'Retirement': 'bi-sun-fill',
      'Death & Cemetery': 'bi-flower1',
      'Legal Matters': 'bi-scales',
      'Health & Wellness': 'bi-heart-pulse-fill',
      'Transport': 'bi-truck'
    };
    return icons[eventName] || 'bi-stars';
  };

  // --- Helper Functions for UI Focus ---

  const getActionState = (request) => {
    if (!user.value) return 'processing';
    
    // Normalize IDs for comparison (handle both integer and nested object cases)
    const userId = Number(user.value.id);
    const assignedId = request.assigned_to && typeof request.assigned_to === 'object' 
      ? Number(request.assigned_to.id) 
      : Number(request.assigned_to);

    // If status is 'in_progress' and assigned to me -> Action Required
    if (request.status === 'in_progress' && assignedId === userId) {
      // Double check if step role matches just in case (Case-insensitive 'system' check)
      const stepRole = request.current_step?.role?.toLowerCase();
      if (stepRole === 'system') return 'processing';
      return 'action_required';
    }
    return 'processing';
  };

  const getActionStateClass = (request) => {
    const state = getActionState(request);
    if (state === 'action_required') {
      return 'bg-white border-l-4 border-l-primary shadow-sm hover:shadow-md';
    }
    return 'bg-slate-50 opacity-75 grayscale-[0.5] hover:grayscale-0 hover:opacity-100';
  };

  const sortRequestsByUrgency = (requests) => {
    // Sort strategy:
    // 1. Action Required > Processing
    // 2. High Priority > Low Priority
    // 3. Oldest > Newest
    return [...requests].sort((a, b) => {
      const stateA = getActionState(a);
      const stateB = getActionState(b);

      if (stateA === 'action_required' && stateB !== 'action_required') return -1;
      if (stateA !== 'action_required' && stateB === 'action_required') return 1;

      // Priority logic (assuming enum: high, normal, low)
      const pMap = { high: 3, normal: 2, low: 1 };
      const pA = pMap[a.priority] || 0;
      const pB = pMap[b.priority] || 0;
      if (pA !== pB) return pB - pA; // Descending

      return new Date(a.created_at) - new Date(b.created_at); // ASC (FIFO)
    });
  };

  const selectMda = (mda) => {
    if (!mda) { mdaFilter.value = ''; mdaSearchLocal.value = ''; }
    else { mdaFilter.value = mda.id; mdaSearchLocal.value = mda.name; }
    showMdaDropdown.value = false;
  };

  const getTimeInQueue = (createdAt) => {
    const created = new Date(createdAt);
    const now = new Date();
    const diffHours = Math.floor((now - created) / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
      return { 
        label: `${diffDays}d ago`, 
        variant: diffDays > 3 ? 'badge--danger' : (diffDays > 1 ? 'badge--warning' : 'badge--info')
      };
    }
    return { 
      label: `${diffHours}h ago`, 
      variant: diffHours > 12 ? 'badge--warning' : 'badge--info'
    };
  };

  const filteredAvailableServices = computed(() => {
    let result = availableServices.value;
    if (mdaFilter.value) {
      const targetMdaId = String(typeof mdaFilter.value === 'object' ? mdaFilter.value.id : mdaFilter.value);
      result = result.filter(s => {
        const sMdaId = String((s.mda && typeof s.mda === 'object') ? s.mda.id : s.mda);
        return sMdaId === targetMdaId;
      });
    }
    if (lifeEventFilter.value) result = result.filter(s => s.life_event_group === lifeEventFilter.value);
    if (familyFilter.value) {
      result = result.filter(s => {
        const famName = s.service_family_details?.name || s.service_family || 'Uncategorized';
        return String(famName) === String(familyFilter.value);
      });
    }
    if (groupFilter.value) result = result.filter(s => s.service_group_details && s.service_group_details.some(g => g.name === groupFilter.value));
    if (priorityFilter.value) result = result.filter(s => s.priority === priorityFilter.value);

    // If search is active, we should narrow the results, but if the user just started searching 
    // from a family view, they might expect to find anything. For now, we keep it additive 
    // but ensure the empty state is clear.
    if (serviceSearchQuery.value) {
      const q = serviceSearchQuery.value.toLowerCase();
      result = result.filter(s =>
        s.service_name.toLowerCase().includes(q) ||
        getMdaName(s.mda).toLowerCase().includes(q) ||
        (s.catalogue_tags && s.catalogue_tags.some(t => t.toLowerCase().includes(q)))
      );
    }
    return result;
  });

  const closeDropdownWithDelay = (type) => {
    setTimeout(() => {
      if (type === 'mda') showMdaDropdown.value = false;
      if (type === 'lifeEvent') showLifeEventDropdown.value = false;
      if (type === 'family') showFamilyDropdown.value = false;
      if (type === 'group') showGroupDropdown.value = false;
    }, 200);
  };

  watch([serviceSearchQuery, mdaFilter, lifeEventFilter, familyFilter], (newVals, oldVals) => {
    const [newSearch, newMda, newLife, newFam] = newVals;
    const [oldSearch, oldMda, oldLife, oldFam] = oldVals || [];

    // If the family filter was explicitly set
    if (newFam && newFam !== oldFam) {
      selectedFamilyForView.value = newFam;
    }
    // If the family filter was cleared, OR any other structural search/filter changed, clear the category view constraint
    else if ((!newFam && newFam !== oldFam) || newSearch !== oldSearch || newMda !== oldMda || newLife !== oldLife) {
      selectedFamilyForView.value = null;
    }
  });

  const groupedServicesByFamily = computed(() => {
    const services = filteredAvailableServices.value;
    const families = serviceConfigStore.families;

    // Group services by their family name from service_family_details
    const groupMap = services.reduce((acc, svc) => {
      const famName = String(svc.service_family_details?.name || svc.service_family || 'Uncategorized');
      if (!acc[famName]) acc[famName] = [];
      acc[famName].push(svc);
      return acc;
    }, {});

    // Sort family names: defined families first, then Uncategorized
    const sortedFamilyNames = Object.keys(groupMap).sort((a, b) => {
      if (a === 'Uncategorized') return 1;
      if (b === 'Uncategorized') return -1;
      return a.localeCompare(b);
    });

    return sortedFamilyNames.map(name => ({
      name,
      services: groupMap[name],
      family: Object.keys(groupMap).length === 1 && familyFilter.value ? families.find(f => f.name === name) : families.find(f => f.name === name)
    }));
  });

  const myRequestsPage = ref(1);
  const assignedPage = ref(1);
  const unassignedPage = ref(1);
  const mdaPage = ref(1);

  const fetchMyRequests = (page = 1) => {
    myRequestsPage.value = page;
    citizenStore.fetchMyRequests({
      status: myRequestsStatusFilter.value,
      search: requestSearchQuery.value,
      page
    });
  };

  const fetchAssignedRequests = (page = 1) => {
    assignedPage.value = page;
    staffStore.fetchAssignedRequests({
      status: queueStatusFilter.value,
      priority: priorityFilter.value,
      search: queueSearchQuery.value,
      page
    });
  };

  const fetchUnassignedRequests = (page = 1) => {
    unassignedPage.value = page;
    staffStore.fetchUnassignedRequests({
      search: unassignedSearchQuery.value,
      priority: priorityFilter.value,
      page
    });
  };

  const fetchMdaRequests = (page = 1) => {
    mdaPage.value = page;
    staffStore.fetchIncompleteMdaRequests({
      search: incompleteSearchQuery.value,
      page
    });
  };

  // Transactional datasets are now filtered server-side.
  const filteredMyRequests = computed(() => myRequests.value);
  const filteredAssignedRequests = computed(() => assignedRequests.value);
  const filteredIncompleteRequests = computed(() => mdaIncompleteRequests.value);
  const filteredUnassignedRequests = computed(() => unassignedRequests.value);

  // Watchers to trigger API-based filtering
  watch([myRequestsStatusFilter, requestSearchQuery], () => {
    fetchMyRequests(1);
  }, { debounce: 300 });

  watch([queueStatusFilter, priorityFilter, queueSearchQuery], () => {
    fetchAssignedRequests(1);
  }, { debounce: 300 });

  watch([unassignedSearchQuery, priorityFilter], () => {
    fetchUnassignedRequests(1);
  }, { debounce: 300 });

  watch([incompleteSearchQuery], () => {
    fetchMdaRequests(1);
  }, { debounce: 300 });


  const adminTabGroups = [
    {
      layer: '01',
      title: 'Digital Frontend Channels',
      description: 'Citizen, officer and assisted access',
      icon: 'bi bi-window-stack',
      tone: 'channels',
      tabs: [
        { name: 'Citizen Service Channels', icon: 'bi bi-person-vcard-fill' },
        { name: 'Whole-of-Gov Catalogue', icon: 'bi bi-grid-1x2-fill' },
        { name: 'Cradle to Death', icon: 'bi bi-signpost-split-fill' }
      ]
    },
    {
      layer: '02',
      title: 'Core & Orchestration',
      description: 'Workflows, forms and decisions',
      icon: 'bi bi-bezier2',
      tone: 'core',
      tabs: [
        { name: 'API Gateway', icon: 'bi bi-hdd-network-fill' },
        { name: 'Orchestration Studio', icon: 'bi bi-ui-checks-grid' },
        { name: 'Dynamic Forms & Schemas', icon: 'bi bi-file-earmark-code-fill' },
        { name: 'Architecture Designer', icon: 'bi bi-diagram-3-fill' }
      ]
    },
    {
      layer: '03',
      title: 'Interoperability Bridge',
      description: 'Huduma Bridge and secure exchange',
      icon: 'bi bi-arrow-left-right',
      tone: 'exchange',
      tabs: [
        { name: 'Huduma Bridge', icon: 'bi bi-share-fill' },
        { name: 'Registry Adapters', icon: 'bi bi-plugin' },
        { name: 'Central Service Catalogue', icon: 'bi bi-journal-bookmark-fill' }
      ]
    },
    {
      layer: '04',
      title: 'Authoritative Data & Payments',
      description: 'Master registries and financial rails',
      icon: 'bi bi-database-fill-check',
      tone: 'data',
      tabs: [
        { name: 'National Master Registries', icon: 'bi bi-database-fill' },
        { name: 'Government Payments', icon: 'bi bi-credit-card-2-front-fill' },
        { name: 'Revenue & Reconciliation', icon: 'bi bi-cash-stack' }
      ]
    },
    {
      layer: 'T',
      title: 'Trust & Identity Hub',
      description: 'Cross-cutting security controls',
      icon: 'bi bi-shield-lock-fill',
      tone: 'trust',
      tabs: [
        { name: 'Consent Manager', icon: 'bi bi-check2-square' },
        { name: 'Identity Federation & NPKI', icon: 'bi bi-fingerprint' },
        { name: 'Access Governance', icon: 'bi bi-person-lock' },
        { name: 'Identity Directory', icon: 'bi bi-people-fill' }
      ]
    },
    {
      layer: 'O',
      title: 'Governance & Operations',
      description: 'Ownership, assurance and health',
      icon: 'bi bi-activity',
      tone: 'operations',
      tabs: [
        { name: 'MDAs', icon: 'bi bi-buildings-fill' },
        { name: 'Prioritization', icon: 'bi bi-bar-chart-steps' },
        { name: 'Audit Logs', icon: 'bi bi-clipboard2-pulse-fill' },
        { name: 'Platform Health', icon: 'bi bi-heart-pulse-fill' }
      ]
    }
  ];
  const route = useRoute();
  const router = useRouter();

  const currentTab = ref(route.query.tab || 'Orchestration Studio');
  const selectedDrilldownMda = ref(null);
  const selectedDrilldownService = ref(null);

  // Sync state from URL on mount
  onMounted(async () => {
    if (route.query.mdaId) {
      // If we have an MDA ID, we might need the full object or just the ID
      // Most components just need the ID in props
      selectedDrilldownMda.value = { id: route.query.mdaId };
    }
    if (route.query.serviceId) {
      selectedDrilldownService.value = { id: route.query.serviceId };
    }
  });

  // Update URL when state changes
  watch([currentTab, selectedDrilldownMda, selectedDrilldownService], () => {
    const query = { ...route.query, tab: currentTab.value };
    
    if (selectedDrilldownMda.value) query.mdaId = selectedDrilldownMda.value.id;
    else delete query.mdaId;
    
    if (selectedDrilldownService.value) query.serviceId = selectedDrilldownService.value.id;
    else delete query.serviceId;

    router.replace({ query });
  });

  watch(currentTab, (newTab, oldTab) => {
    if (newTab !== oldTab) {
      selectedDrilldownMda.value = null;
      selectedDrilldownService.value = null;
    }
  });

  // Dynamic Component Mapping
  const activeAdminComponent = computed(() => {
    if (currentTab.value === 'MDAs') {
      if (selectedDrilldownService.value) return ServiceTransactionsView;
      if (selectedDrilldownMda.value) return ServiceConfigManager;
      return MdaManager;
    }

    const map = {
      'MDAs': MdaManager,
      'Prioritization': ServiceCatalogueMatrix,
      'Access Governance': AdminRolesView,
      'Identity Directory': UserManager,
      
      'Citizen Service Channels': ServiceCatalogueMatrix,
      'Orchestration Studio': ServiceConfigManager,
      'Dynamic Forms & Schemas': ServiceConfigManager,
      'Whole-of-Gov Catalogue': ServiceCatalogueMatrix,
      'Cradle to Death': ServiceCatalogueMatrix,
      'Architecture Designer': ArchitectureSimulator,
      
      'API Gateway': ApiRegistry,
      'Huduma Bridge': ApiRegistry,
      'Registry Adapters': RegistriesMonitor,
      'Central Service Catalogue': ServiceCatalogueMatrix,
      'National Master Registries': RegistriesMonitor,
      'Government Payments': ApiRegistry,
      'Revenue & Reconciliation': ApiRegistry,

      'Consent Manager': SecurityTrustView,
      'Identity Federation & NPKI': SecurityTrustView,
      
      'Audit Logs': AuditLogManager,
      'Platform Health': SystemHealthView
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
        { name: 'Configurable Workflows', file: 'docs/architecture/CONFIGURABLE_WORKFLOWS_COMPLETE.md' },
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
        { name: 'POC Report (PDF)', file: 'docs/poc/%23 PROOF OF CONCEPT (POC) REPORT_ REPEATABLE GOVERNMENT SERVICES PLATFORM.pdf' },
        { name: 'Proof of Concept (PDF)', file: 'docs/poc/Proof of Concept .pdf' },
      ]
    },
    {
      category: 'Operational Guides',
      icon: 'bi-journal-check',
      docs: [
        { name: 'Deployment Plan', file: 'docs/guides/poc_deployment_dev_ops_plan.md' },
        { name: 'Deployment Guide', file: 'docs/guides/DEPLOYMENT.md' },
        { name: 'Huduma Bridge', file: 'docs/guides/huduma_bridge_instructions.md' },
        { name: 'Frontend Cache Guide', file: 'docs/guides/FRONTEND_CACHE_ISSUE.md' },
        { name: 'BEM UI Standards', file: 'docs/style-guide/BEM-DOCUMENTATION.md' },
        { name: 'BEM Quick Reference', file: 'docs/style-guide/BEM-QUICK-REFERENCE.md' },
        { name: 'BEM Transformation', file: 'docs/style-guide/BEM-TRANSFORMATION-COMPARISON.md' },
        { name: 'BEM Overview', file: 'docs/style-guide/README-BEM.md' },
        { name: 'Service Registry UI', file: 'docs/style-guide/service-registry-bem.html' },
      ]
    },
    {
      category: 'Governance Reports',
      icon: 'bi-clipboard-data-fill',
      docs: [
        { name: 'POC Final Report', file: 'docs/reports/ICTA_POC_Comprehensive_Report.md' },
        { name: 'POC Final Report (HTML)', file: 'docs/reports/ICTA_POC_Comprehensive_Report.html' },
        { name: 'POC Report Outline', file: 'docs/reports/POC_Report_Outline.md' },
        { name: 'Consolidated Actions', file: 'docs/reports/ICTA_WB_CONSOLIDATED_ACTIONS.md' },
        { name: 'Meeting Actions', file: 'docs/reports/ICTA_MEETING_ACTIONS.md' },
      ]
    },
    {
      category: 'Exports & Evidence',
      icon: 'bi-box-arrow-up-right',
      docs: [
        { name: 'All Service Forms', file: 'docs/exports/ALL_SERVICES_FORMS_COMPLETE.md' },
        { name: 'All Service Forms (HTML)', file: 'docs/exports/ALL_SERVICES_FORMS_COMPLETE.html' },
        { name: 'Architecture Export', file: 'docs/exports/architecture_three.html' },
        { name: 'Catalogue Verification', file: 'docs/exports/verify_catalogue_data.html' },
        { name: 'Repeatable Services Presentation', file: 'docs/exports/Presentation - Repeatable Services Algorithm.pdf' },
      ]
    }
  ];

  const architectureLayers = [
    {
      id: 'channels',
      name: 'Digital Channels',
      description: 'Citizen, business, officer and assisted access',
      technology: 'Web · Mobile · USSD',
      icon: 'bi bi-window-stack',
      document: 'docs/poc/poc_project_overview_concept_note.md'
    },
    {
      id: 'orchestration',
      name: 'Core & Orchestration',
      description: 'Workflows, decisions, schemas and dynamic forms',
      technology: 'BPMN · JSON Schema',
      icon: 'bi bi-bezier2',
      document: 'docs/architecture/poc_algorithm_workflow_documentation.md'
    },
    {
      id: 'exchange',
      name: 'Interoperability',
      description: 'Secure policy-driven exchange between agencies',
      technology: 'KeSEL · X-Road · APIs',
      icon: 'bi bi-arrow-left-right',
      document: 'docs/architecture/architecture_three.md'
    },
    {
      id: 'foundations',
      name: 'Data & Payments',
      description: 'Authoritative registries and government payments',
      technology: 'IPRS · KRA · GPA',
      icon: 'bi bi-database-fill-check',
      document: 'docs/poc/poc_system_design_documents.md'
    },
    {
      id: 'operations',
      name: 'Operations & Assurance',
      description: 'Monitoring, audit, security, resilience and validation',
      technology: 'NPKI · Audit · DR',
      icon: 'bi bi-shield-check',
      document: 'docs/poc/poc_test_validation_plan.md'
    }
  ];

  const selectedDoc = ref('docs/poc/poc_system_design_documents.md');
  const technicalDocumentCount = computed(() => categorizedDocs.reduce((total, group) => total + group.docs.length, 0));
  const selectedDocMeta = computed(() => {
    for (const group of categorizedDocs) {
      const document = group.docs.find(doc => doc.file === selectedDoc.value);
      if (document) return { ...document, category: group.category };
    }
    return { name: 'Technical Document', category: 'Architecture Evidence' };
  });
  const selectedDocFormat = computed(() => {
    const extension = selectedDoc.value.split('.').pop()?.toUpperCase();
    return extension === 'MD' ? 'MARKDOWN' : extension || 'DOCUMENT';
  });

  onMounted(async () => {
    // 1. Ensure user data is loaded (essential for role-based logic)
    if (authStore.isAuthenticated && !authStore.user) {
      await authStore.fetchCurrentUser();
    }

    const role = user.value?.role?.toLowerCase();

    if (role === 'mda_admin') {
      staffCurrentTab.value = 'configuration';
    }
    
    // 2. Fetch data based on role
    const citizenRoles = ['citizen', 'hospital_staff'];
    const staffRoles = ['officer', 'supervisor', 'registrar', 'mda_admin', 'employee', 'global_officer', 'global_supervisor', 'mda_officer', 'mda_supervisor'];
    
    // Data relevant to citizen portal (can also be seen by staff for catalogue view)
    if (citizenRoles.includes(role) || staffRoles.includes(role)) {
      citizenStore.fetchAvailableServices();
      citizenStore.fetchMyRequests();
      mdaStore.fetchMdas();
      serviceConfigStore.fetchFamilies();
    }

    // Staff specific data
    if (staffRoles.includes(role)) {
      serviceConfigStore.fetchCatalogueSummary();
      staffStore.fetchIncompleteMdaRequests();
      staffStore.fetchUnassignedRequests();
      staffStore.fetchAssignedRequests();
      
      if (['supervisor', 'global_supervisor', 'mda_supervisor', 'mda_admin'].includes(role)) {
        staffStore.fetchTeamRequests();
        staffStore.fetchEscalatedRequests();
      }
    } 
    // Admin specific data
    else if (['admin', 'system_admin'].includes(role)) {
      mdaStore.fetchMdas();
      serviceConfigStore.fetchServices();
      serviceConfigStore.fetchFamilies();
      serviceConfigStore.fetchCatalogueSummary();
    }
  });

  const statusClass = (status) => {
    const classes = {
      received: 'bg-blue-100 text-blue-800 border border-blue-200',
      in_progress: 'bg-amber-50 text-amber-700 border border-amber-100',
      escalated: 'bg-rose-50 text-rose-800 border border-rose-100 block animate-pulse',
      approved: 'bg-emerald-50 text-emerald-700 border border-emerald-100',
      rejected: 'bg-slate-100 text-slate-700 border border-slate-200',
      closed: 'bg-gray-100 text-gray-800 border border-gray-200',
      validation_failed: 'bg-red-50 text-red-700 border border-red-100',
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
  };

  const statusIcon = (status) => {
    const icons = {
      received: 'bi-clock-history',
      in_progress: 'bi-gear-wide-connected',
      escalated: 'bi-exclamation-triangle-fill',
      approved: 'bi-patch-check-fill',
      rejected: 'bi-x-circle-fill',
      closed: 'bi-archive-fill',
      validation_failed: 'bi-shield-exclamation',
    };
    return icons[status] || 'bi-info-circle';
  };

  const formatStatusLabel = (status) => {
    const labels = {
      received: 'Received',
      in_progress: 'Under Review',
      escalated: 'Expedited Review',
      approved: 'Issued / Approved',
      rejected: 'Declined',
      closed: 'Completed',
      validation_failed: 'Verification Error',
    };

    // Custom logic for system-triggered steps
    const request = myRequests.value.find(r => r.status === status); // This is risky, status is just a string
    // Better to handle this where we have the context
    return labels[status] || status?.toUpperCase();
  };

  const getStatusLabelWithContext = (request) => {
    if (request.status === 'in_progress' && request.current_step?.role === 'System') {
      return 'Automated Engine Processing';
    }
    return formatStatusLabel(request.status);
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
    
    // Initialize form data from existing payload
    const fields = request.current_step?.api_config?.form_fields || [];
    const initialData = {};
    fields.forEach(f => {
      initialData[f] = request.payload?.[f] || '';
    });
    stepFormData.value = initialData;
    
    showBpmnBlueprint.value = false;
  };

  const closeCompleteStepModal = () => { showCompleteStepModal.value = false; currentRequestToComplete.value = null; };

  const completeStep = async () => {
    if (!currentRequestToComplete.value) return;
    processingId.value = currentRequestToComplete.value.id;
    try {
      await staffStore.completeWorkflowStep(
        currentRequestToComplete.value.id, 
        stepAction.value.action, 
        stepAction.value.details,
        stepFormData.value
      );
      closeCompleteStepModal();
      showFeedback('Task disposition finalized successfully.', 'success');
      await staffStore.fetchAssignedRequests();
      await staffStore.fetchUnassignedRequests();
      await staffStore.fetchIncompleteMdaRequests();
      if (user.value?.role === 'supervisor') {
        await staffStore.fetchTeamRequests();
        await staffStore.fetchEscalatedRequests();
      }
    } catch (error) {
      showFeedback('Failed to complete step: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      processingId.value = null;
    }
  };

  const escalateRequest = async (requestId) => {
    if (confirm('Are you sure you want to escalate this request?')) {
      try { await staffStore.escalateRequest(requestId); staffStore.fetchAssignedRequests(); } catch (error) { alert('Failed to escalate request: ' + error.message); }
    }
  };

  const openBpmnModal = (service, stage = 'as_is') => {
    selectedServiceForBpmn.value = service;
    activeBpmnStage.value = stage;
    showBpmnModal.value = true;
  };

  const closeBpmnModal = () => {
    showBpmnModal.value = false;
    selectedServiceForBpmn.value = null;
  };

  const claimTask = async (requestId) => {
    claimingId.value = requestId;
    try {
      await staffStore.claimTask(requestId);
      claimingId.value = 'success-' + requestId;
      showFeedback('Task successfully acquired and moved to your workstation.', 'success');
      setTimeout(() => {
        if (claimingId.value === 'success-' + requestId) claimingId.value = null;
      }, 1500);
    } catch (error) {
      showFeedback('Claim failed: ' + (error.response?.data?.detail || error.message), 'error');
      claimingId.value = null;
    }
  };

  const releaseTask = async (requestId) => {
    if (confirm('Are you sure you want to release this task back to the pool?')) {
      releasingId.value = requestId;
      try {
        await staffStore.releaseTask(requestId);
        showFeedback('Task released back to the universal pool.', 'info');
      } catch (error) {
        showFeedback('Release failed: ' + (error.response?.data?.detail || error.message), 'error');
      } finally {
        releasingId.value = null;
      }
    }
  };

  const showFeedback = (message, type = 'success') => {
    actionFeedback.value = { message, type };
    setTimeout(() => {
      actionFeedback.value = { message: '', type: '' };
    }, 4000);
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

  .grayscale-\[0\.5\] {
    filter: grayscale(0.5);
  }

  .hover\:grayscale-0:hover {
    filter: grayscale(0);
  }

  .animate-bounce-short {
    animation: bounceShort 2s infinite;
  }

  @keyframes bounceShort {

    0%,
    20%,
    50%,
    80%,
    100% {
      transform: translateY(0);
    }

    40% {
      transform: translateY(-4px);
    }

    60% {
      transform: translateY(-2px);
    }
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
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1/1;
    min-width: 3rem;
    background: white;
    border-radius: var(--radius-sm);
    border: 2px solid var(--secondary);
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

  /* Glassmorphism Toolbar & Classy Filters */
  .toolbar {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 1.5rem;
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-lg);
  }

  .toolbar__filter-input {
    background: white;
    border: 2px solid var(--color-border-light);
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .toolbar__filter-input:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 4px var(--color-primary-soft);
    transform: translateY(-1px);
  }

  .toolbar__clear-icon {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-muted);
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
    opacity: 0.5;
  }

  .toolbar__clear-icon:hover {
    color: var(--color-primary);
    opacity: 1;
    transform: translateY(-50%) scale(1.1);
  }

  .toolbar__clear-icon--with-arrow {
    right: 2.5rem;
  }

  /* Classy Dropdown Menu */
  .dropdown-menu {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 12px;
    margin-top: 0.5rem;
    z-index: 1000;
    overflow: auto;
    padding: 0.5rem;
    max-height: 300px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  .dropdown-item {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    color: var(--color-text-main);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .dropdown-item:hover {
    background: var(--color-primary-soft);
    color: var(--color-primary);
    transform: translateX(4px);
  }

  .dropdown-item--header {
    color: var(--color-primary);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--color-border-light);
    margin-bottom: 0.25rem;
    border-radius: 0;
  }

  /* Reset Button */
  .btn-reset {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    background: white;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    font-weight: 800;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .btn-reset:hover {
    border-color: var(--color-primary);
    color: var(--color-primary);
    background: var(--color-primary-soft);
    transform: rotate(-5deg) scale(1.05);
  }

  /* Filter Chips */
  .filter-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: var(--grad-premium);
    color: white;
    border-radius: 40px;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-md);
  }

  .filter-chip:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    filter: brightness(1.1);
  }

  .filter-chip__label {
    opacity: 0.6;
    text-transform: uppercase;
    font-size: 9px;
  }

  /* Vue Transitions */
  .dropdown-enter-active,
  .dropdown-leave-active {
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .dropdown-enter-from,
  .dropdown-leave-to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }

  .list-enter-active,
  .list-leave-active {
    transition: all 0.4s ease;
  }

  .list-enter-from,
  .list-leave-to {
    opacity: 0;
    transform: scale(0.5) translateY(10px);
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

  .action-toast {
    position: fixed;
    top: 2rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    padding: 1rem 2rem;
    border-radius: var(--radius-pill);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: white;
    font-size: 0.8125rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    backdrop-filter: blur(8px);
  }

  .action-toast.success {
    background: #10b981;
  }

  .action-toast.error {
    background: #ef4444;
  }

  .action-toast.info {
    background: #3b82f6;
  }

  @keyframes slideDown {
    from {
      transform: translate(-50%, -100%);
      opacity: 0;
    }

    to {
      transform: translate(-50%, 0);
      opacity: 1;
    }
  }

  /* Acquisition Animations */
  .button--success {
    background: #10b981 !important;
    border-color: #10b981 !important;
    color: white !important;
  }

  .animate-glow {
    animation: button-glow 1s infinite alternate;
  }

  @keyframes button-glow {
    from {
      box-shadow: 0 0 5px rgba(236, 35, 42, 0.4);
    }

    to {
      box-shadow: 0 0 15px rgba(236, 35, 42, 0.8);
    }
  }

  /* System Architect Technical Specs Workbench */
  .architect-hero {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(280px, .65fr);
    gap: 2rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    border-radius: 1.5rem;
    color: white;
    background:
      radial-gradient(circle at 85% 15%, rgba(45, 212, 191, .25), transparent 27%),
      linear-gradient(135deg, #101f35, #173f5d 58%, #0f5962);
  }

  .architect-hero::after {
    content: '';
    position: absolute;
    inset: 0;
    opacity: .12;
    background-image:
      linear-gradient(rgba(255, 255, 255, .32) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, .32) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
  }

  .architect-hero__copy,
  .architect-scorecard {
    position: relative;
    z-index: 1;
  }

  .architect-eyebrow,
  .architect-section-kicker {
    display: block;
    margin-bottom: .45rem;
    color: #2dd4bf;
    font-size: .64rem;
    font-weight: 900;
    letter-spacing: .16em;
    text-transform: uppercase;
  }

  .architect-eyebrow i {
    margin-right: .4rem;
  }

  .architect-hero h2 {
    margin: 0 0 .65rem;
    color: white;
    font-size: clamp(1.7rem, 3vw, 2.5rem);
    font-weight: 900;
    letter-spacing: -.045em;
    line-height: 1.1;
  }

  .architect-hero p {
    max-width: 660px;
    margin: 0;
    color: #d2e3eb;
    font-size: .86rem;
    line-height: 1.65;
  }

  .architect-standards {
    display: flex;
    flex-wrap: wrap;
    gap: .4rem;
    margin-top: 1rem;
  }

  .architect-standards span {
    padding: .3rem .58rem;
    border: 1px solid rgba(255, 255, 255, .18);
    border-radius: 999px;
    color: #d8edf0;
    background: rgba(255, 255, 255, .08);
    font-size: .56rem;
    font-weight: 900;
    text-transform: uppercase;
  }

  .architect-scorecard {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .65rem;
    align-self: center;
  }

  .architect-scorecard article {
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, .16);
    border-radius: 1rem;
    background: rgba(8, 29, 48, .42);
    backdrop-filter: blur(8px);
  }

  .architect-scorecard strong,
  .architect-scorecard small {
    display: block;
  }

  .architect-scorecard strong {
    color: white;
    font-size: 1.35rem;
    font-weight: 900;
  }

  .architect-scorecard small {
    margin-top: .15rem;
    color: #b8ced8;
    font-size: .58rem;
    font-weight: 800;
    text-transform: uppercase;
  }

  .architect-blueprint,
  .architect-evidence {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #e0e8ef;
    border-radius: 1.5rem;
    background: white;
    box-shadow: 0 12px 35px rgba(15, 35, 55, .05);
  }

  .architect-blueprint > header,
  .architect-evidence__heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  .architect-section-kicker {
    margin-bottom: .2rem;
    color: #0f766e;
  }

  .architect-blueprint h3,
  .architect-evidence h3 {
    margin: 0;
    color: #17243a;
    font-size: 1.15rem;
    font-weight: 900;
    letter-spacing: -.02em;
  }

  .architect-live,
  .architect-document-count {
    padding: .42rem .68rem;
    border-radius: 999px;
    color: #047857;
    background: #ecfdf5;
    font-size: .58rem;
    font-weight: 900;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .architect-live i {
    margin-right: .3rem;
    color: #10b981;
    font-size: .45rem;
  }

  .architect-layer-flow {
    position: relative;
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: .65rem;
    padding: 1.1rem;
    border: 1px solid #e4ebf1;
    border-radius: 1.15rem;
    background: linear-gradient(180deg, #f8fbfd, #f4f8fa);
  }

  .architect-layer-flow::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 8%;
    right: 8%;
    height: 2px;
    background: linear-gradient(90deg, #9fd5cf, #8db9d0, #d6acbc);
  }

  .architect-layer {
    --layer-color: #0f766e;
    position: relative;
    z-index: 1;
    min-width: 0;
    padding: .9rem;
    border: 1px solid #dce5ec;
    border-top: 3px solid var(--layer-color);
    border-radius: .85rem;
    text-align: left;
    background: white;
    cursor: pointer;
    transition: .2s ease;
  }

  .architect-layer:hover,
  .architect-layer.active {
    border-color: var(--layer-color);
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(20, 42, 65, .1);
  }

  .architect-layer--channels { --layer-color: #7c3aed; }
  .architect-layer--orchestration { --layer-color: #e11d48; }
  .architect-layer--exchange { --layer-color: #0284c7; }
  .architect-layer--foundations { --layer-color: #059669; }
  .architect-layer--operations { --layer-color: #d97706; }

  .architect-layer__number {
    position: absolute;
    top: .55rem;
    right: .6rem;
    color: #a1adba;
    font-family: monospace;
    font-size: .52rem;
    font-weight: 900;
  }

  .architect-layer__icon {
    display: grid;
    place-items: center;
    width: 2.15rem;
    height: 2.15rem;
    margin-bottom: .65rem;
    border-radius: .65rem;
    color: var(--layer-color);
    background: color-mix(in srgb, var(--layer-color) 10%, white);
  }

  .architect-layer strong,
  .architect-layer small,
  .architect-layer__tech {
    display: block;
  }

  .architect-layer strong {
    color: #253449;
    font-size: .7rem;
    font-weight: 900;
  }

  .architect-layer small {
    min-height: 2.3rem;
    margin-top: .25rem;
    color: #768596;
    font-size: .57rem;
    line-height: 1.35;
  }

  .architect-layer__tech {
    margin-top: .65rem;
    padding-top: .55rem;
    border-top: 1px solid #edf1f4;
    color: var(--layer-color);
    font-size: .5rem;
    font-weight: 900;
    text-transform: uppercase;
  }

  .architect-cross-cutting {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: .7rem 1.5rem;
    margin-top: .7rem;
    padding: .75rem;
    border: 1px dashed #bdcad4;
    border-radius: .8rem;
    color: #627386;
    background: #f8fafc;
  }

  .architect-cross-cutting span {
    font-size: .56rem;
    font-weight: 900;
    text-transform: uppercase;
  }

  .architect-cross-cutting i {
    margin-right: .3rem;
    color: #0f766e;
  }

  .architect-library {
    max-height: 78vh;
    padding: 1rem;
    overflow-y: auto;
    border: 1px solid #e2e8ee;
    border-radius: 1rem;
    background: #f8fafc;
  }

  .architect-library__title {
    display: flex;
    align-items: center;
    gap: .65rem;
    padding-bottom: .85rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid #dde5eb;
  }

  .architect-library__title > i {
    display: grid;
    place-items: center;
    width: 2.2rem;
    height: 2.2rem;
    border-radius: .65rem;
    color: #0f766e;
    background: #dff7f3;
  }

  .architect-library__title strong,
  .architect-library__title small {
    display: block;
  }

  .architect-library__title strong {
    color: #26364b;
    font-size: .72rem;
    font-weight: 900;
  }

  .architect-library__title small {
    margin-top: .1rem;
    color: #8390a0;
    font-size: .55rem;
  }

  .architect-document-header {
    display: flex;
    align-items: center;
    gap: .8rem;
    padding: 1rem 1.2rem;
    border: 1px solid #dfe7ed;
    border-radius: 1rem 1rem 0 0;
    color: white;
    background: #17243a;
  }

  .architect-document-header__icon {
    display: grid;
    place-items: center;
    width: 2.5rem;
    height: 2.5rem;
    flex: 0 0 auto;
    border-radius: .7rem;
    color: #5eead4;
    background: rgba(255, 255, 255, .08);
  }

  .architect-document-header > div:nth-child(2) {
    min-width: 0;
    flex: 1;
  }

  .architect-document-header span,
  .architect-document-header h4,
  .architect-document-header code {
    display: block;
  }

  .architect-document-header span {
    color: #5eead4;
    font-size: .52rem;
    font-weight: 900;
    letter-spacing: .1em;
    text-transform: uppercase;
  }

  .architect-document-header h4 {
    margin: .15rem 0;
    overflow: hidden;
    color: white;
    font-size: .82rem;
    font-weight: 900;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .architect-document-header code {
    overflow: hidden;
    color: #91a7b8;
    font-size: .56rem;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .architect-document-header .architect-format {
    padding: .35rem .55rem;
    border: 1px solid rgba(255, 255, 255, .15);
    border-radius: .45rem;
    color: #d9e7ed;
    background: rgba(255, 255, 255, .07);
    white-space: nowrap;
  }

  .architect-document-viewer :deep(.markdown-container) {
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }

  @media (max-width: 1100px) {
    .architect-hero {
      grid-template-columns: 1fr;
    }

    .architect-layer-flow {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .architect-layer-flow::before {
      display: none;
    }
  }

  @media (max-width: 680px) {
    .architect-hero,
    .architect-blueprint,
    .architect-evidence {
      padding: 1rem;
    }

    .architect-scorecard,
    .architect-layer-flow {
      grid-template-columns: 1fr;
    }

    .architect-blueprint > header,
    .architect-evidence__heading {
      flex-direction: column;
    }

    .architect-library {
      max-height: none;
    }
  }

  /* Admin navigation as a compact reference-architecture map */
  .architecture-nav {
    overflow: hidden;
    border: 1px solid #dce5ea;
    background: #f8fafc;
    box-shadow: 0 18px 45px rgba(15, 31, 45, .08);
  }

  .architecture-nav__header {
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: .2rem;
    padding: 1.15rem 1rem 1rem;
    color: white;
    background: linear-gradient(145deg, #0c2233, #123e4d);
  }

  .architecture-nav__header::after {
    position: absolute;
    right: -2rem;
    bottom: -3rem;
    width: 7rem;
    height: 7rem;
    border: 1px solid rgba(94, 234, 212, .25);
    border-radius: 50%;
    content: '';
  }

  .architecture-nav__header strong {
    font-size: .92rem;
    font-weight: 900;
    letter-spacing: -.015em;
  }

  .architecture-nav__header small {
    color: #9fb7c1;
    font-size: .58rem;
    font-weight: 700;
  }

  .architecture-nav__eyebrow {
    display: flex;
    align-items: center;
    gap: .4rem;
    color: #5eead4;
    font-size: .52rem;
    font-weight: 900;
    letter-spacing: .14em;
    text-transform: uppercase;
  }

  .architecture-nav__stack {
    position: relative;
    padding: .6rem .55rem .35rem;
  }

  .architecture-nav__stack::before {
    position: absolute;
    top: 1.9rem;
    bottom: 1.7rem;
    left: 1.47rem;
    width: 2px;
    background: linear-gradient(#38bdf8, #8b5cf6 24%, #14b8a6 45%, #16a34a 63%, #f59e0b 79%, #ef4444);
    content: '';
    opacity: .45;
  }

  .architecture-nav__layer {
    --layer-accent: #64748b;
    position: relative;
    padding: .48rem .35rem .55rem;
    border: 1px solid transparent;
    border-radius: .7rem;
    transition: background .2s ease, border-color .2s ease, box-shadow .2s ease;
  }

  .architecture-nav__layer + .architecture-nav__layer {
    margin-top: .18rem;
  }

  .architecture-nav__layer--channels { --layer-accent: #0ea5e9; }
  .architecture-nav__layer--core { --layer-accent: #8b5cf6; }
  .architecture-nav__layer--exchange { --layer-accent: #14b8a6; }
  .architecture-nav__layer--data { --layer-accent: #16a34a; }
  .architecture-nav__layer--trust { --layer-accent: #f59e0b; }
  .architecture-nav__layer--operations { --layer-accent: #ef4444; }

  .architecture-nav__layer.is-active {
    border-color: color-mix(in srgb, var(--layer-accent) 23%, white);
    background: color-mix(in srgb, var(--layer-accent) 5%, white);
    box-shadow: 0 5px 15px color-mix(in srgb, var(--layer-accent) 8%, transparent);
  }

  .architecture-nav__layer-heading {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1.05rem 1.65rem minmax(0, 1fr);
    align-items: center;
    gap: .4rem;
    padding: .18rem 0 .42rem;
  }

  .architecture-nav__number {
    color: var(--layer-accent);
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: .48rem;
    font-weight: 900;
  }

  .architecture-nav__layer-icon {
    display: grid;
    width: 1.65rem;
    height: 1.65rem;
    place-items: center;
    border: 2px solid white;
    border-radius: .52rem;
    color: white;
    background: var(--layer-accent);
    box-shadow: 0 3px 8px color-mix(in srgb, var(--layer-accent) 25%, transparent);
    font-size: .7rem;
  }

  .architecture-nav__layer-heading > span:last-child {
    min-width: 0;
  }

  .architecture-nav__layer-heading strong,
  .architecture-nav__layer-heading small {
    display: block;
  }

  .architecture-nav__layer-heading strong {
    overflow: hidden;
    color: #1e293b;
    font-size: .61rem;
    font-weight: 900;
    letter-spacing: .035em;
    text-overflow: ellipsis;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .architecture-nav__layer-heading small {
    margin-top: .06rem;
    overflow: hidden;
    color: #82919f;
    font-size: .48rem;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .architecture-nav__capabilities {
    display: flex;
    flex-direction: column;
    gap: .1rem;
    margin-left: 2.1rem;
  }

  .architecture-nav .sidebar-nav__item {
    min-width: 0;
    padding: .42rem .48rem;
    border-left-width: 2px;
    border-radius: .4rem;
    color: #526170;
    font-size: .58rem;
    line-height: 1.2;
  }

  .architecture-nav .sidebar-nav__item:hover {
    color: var(--layer-accent, #0f766e);
    background: white;
  }

  .architecture-nav__layer .sidebar-nav__item--active {
    border-left-color: var(--layer-accent);
    color: var(--layer-accent);
    background: white;
    box-shadow: 0 2px 9px rgba(15, 23, 42, .07);
  }

  .sidebar-nav__capability-icon {
    flex: 0 0 auto;
    width: .75rem;
    color: currentColor;
    font-size: .62rem;
    text-align: center;
    opacity: .78;
  }

  .architecture-nav__foundation {
    padding: .75rem .8rem .85rem;
    border-top: 1px solid #dce5ea;
    background: #eaf0f3;
  }

  .architecture-nav__foundation-title {
    display: flex;
    align-items: center;
    gap: .48rem;
    margin-bottom: .45rem;
    color: #334155;
  }

  .architecture-nav__foundation-title > i {
    color: #0f766e;
    font-size: .72rem;
  }

  .architecture-nav__foundation-title strong,
  .architecture-nav__foundation-title small {
    display: block;
  }

  .architecture-nav__foundation-title strong {
    font-size: .55rem;
    font-weight: 900;
    letter-spacing: .06em;
    text-transform: uppercase;
  }

  .architecture-nav__foundation-title small {
    color: #84929f;
    font-size: .46rem;
    font-weight: 700;
  }

  .architecture-nav__foundation-links {
    display: flex;
    flex-direction: column;
    gap: .18rem;
  }

  .architecture-nav__foundation .sidebar-nav__item {
    background: rgba(255, 255, 255, .68);
  }

  .architecture-nav__doc-count {
    display: grid;
    min-width: 1.15rem;
    height: 1.15rem;
    place-items: center;
    border-radius: 999px;
    color: white;
    background: #0f766e;
    font-size: .43rem;
    font-weight: 900;
  }
</style>
