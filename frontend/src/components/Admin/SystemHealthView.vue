<template>
    <div class="u-flex u-flex-col u-gap-8 animate-fade-in">
    <!-- Health Header -->
    <header class="u-flex u-justify-between u-items-center">
      <div class="page__title-group">
        <h3 class="u-text-2xl u-font-black u-text-main u-mb-1 u-border-l-4 u-border-success u-pl-4">
          Infrastructure & Architecture Health
        </h3>
        <p class="u-text-xs u-font-bold u-text-muted u-uppercase u-tracking-widest">Global G2C Services Backbone</p>
      </div>
      <div class="status-indicator">
        <span class="status-indicator__dot status-indicator__dot--online animate-pulse"></span>
        <span class="status-indicator__label u-text-success">Live Monitoring Active</span>
      </div>
    </header>

    <!-- State Grid -->
    <div class="stats-grid">
      <!-- Frontend/UI State -->
      <article class="stats-card stats-card--primary">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
             <div class="stats-card__icon-container">
               <div class="stats-card__icon-glow"></div>
               <div class="stats-card__icon"><i class="bi bi-window-stack"></i></div>
             </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Frontend Interface</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">Operational</span>
            </div>
            <p class="stats-card__sublabel">Vue 3 + Vite Mesh</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <span class="badge badge--success badge--small">STABLE RELEASE</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- Backend API State -->
      <article class="stats-card stats-card--success">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
             <div class="stats-card__icon-container">
               <div class="stats-card__icon-glow"></div>
               <div class="stats-card__icon"><i class="bi bi-cpu-fill"></i></div>
             </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Backend Engine</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">34</span>
              <span class="stats-card__unit">ms</span>
            </div>
            <p class="stats-card__sublabel">Django Core Active</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <span class="badge badge--success badge--small">LATENCY: NOMINAL</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- KESEL Bridge -->
      <article class="stats-card stats-card--indigo">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
             <div class="stats-card__icon-container">
               <div class="stats-card__icon-glow"></div>
               <div class="stats-card__icon"><i class="bi bi-hdd-network-fill"></i></div>
             </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">KESEL Bridge</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">Active</span>
            </div>
            <p class="stats-card__sublabel">Cross-MDA Mesh Layer</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <span class="badge badge--primary badge--small u-bg-indigo-500 u-text-white">SYNCED</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- Huduma Bridge -->
      <article class="stats-card stats-card--cyan">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
             <div class="stats-card__icon-container">
               <div class="stats-card__icon-glow"></div>
               <div class="stats-card__icon"><i class="bi bi-cloud-check-fill"></i></div>
             </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Huduma Bridge</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">Online</span>
            </div>
            <p class="stats-card__sublabel">Citizen Service Hub</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <span class="badge badge--info badge--small u-bg-cyan-500 u-text-white">HEARTBEAT: OK</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- EDRM Status -->
      <article class="stats-card stats-card--info">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
             <div class="stats-card__icon-container">
               <div class="stats-card__icon-glow"></div>
               <div class="stats-card__icon"><i class="bi bi-archive-fill"></i></div>
             </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">EDRMS Archive</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">99.9</span>
              <span class="stats-card__unit">%</span>
            </div>
            <p class="stats-card__sublabel">S3 Object Storage</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <span class="badge badge--info badge--small">AVAILABILITY</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>
    </div>

    <!-- External Registry Latencies -->
    <article class="card shadow-lg">
      <header class="card__header u-bg-page u-py-4">
        <h4 class="card__title u-text-xs u-font-black u-text-muted u-uppercase u-tracking-widest">
          Authoritative Registry Latency (Real-time Simulation)
        </h4>
      </header>
      <div class="card__body u-p-8 u-flex u-flex-col u-gap-6">
        <div v-for="system in latencies" :key="system.name">
          <div class="u-flex u-justify-between u-items-center u-mb-2">
            <span class="u-text-xs u-font-black u-text-main u-uppercase u-tracking-tighter">{{ system.name }}</span>
            <span class="u-text-xs u-font-mono u-font-black" :class="system.ms > 300 ? 'u-text-danger' : 'u-text-primary'">{{ system.ms }}ms</span>
          </div>
          <div class="progress-bar shadow-inner">
            <div class="progress-bar__fill shadow-sm transition-all duration-500" 
                 :class="system.ms > 300 ? 'u-bg-danger' : 'u-bg-primary'"
                 :style="{ width: `${system.percent}%` }"></div>
          </div>
        </div>
      </div>
    </article>

    <!-- Node-RED / Workflow Engine Stats -->
    <div class="u-grid u-grid-cols-1 md:u-grid-cols-2 u-gap-8">
      <article class="card card--dark shadow-xl">
        <header class="card__header u-bg-transparent u-py-6">
          <h5 class="card__title u-text-xs u-font-black u-text-primary-soft u-uppercase u-tracking-widest">Workload Distribution</h5>
        </header>
        <div class="card__body u-p-8 u-pt-0">
          <div class="u-flex u-flex-col u-gap-4">
            <div class="u-flex u-justify-between u-items-center">
               <span class="u-text-sm u-text-muted">Manual Verification Tasks</span>
               <span class="u-text-lg u-font-black u-text-primary">{{ (142).toLocaleString() }}</span>
            </div>
            <div class="u-flex u-justify-between u-items-center">
               <span class="u-text-sm u-text-muted">Automated API Steps</span>
               <span class="u-text-lg u-font-black u-text-success">{{ (1085).toLocaleString() }}</span>
            </div>
            <div class="u-flex u-justify-between u-items-center">
               <span class="u-text-sm u-text-muted">Escalated Priority</span>
               <span class="u-text-lg u-font-black u-text-danger">12</span>
            </div>
          </div>
          <footer class="u-mt-10 u-pt-6 u-border-t u-border-white/10 u-flex u-justify-center u-gap-6">
             <div class="u-text-center">
                <p class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-1">Memory</p>
                <p class="u-text-xs u-font-bold u-text-white">4.2GB</p>
             </div>
             <div class="u-text-center">
                <p class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-1">CPU</p>
                <p class="u-text-xs u-font-bold u-text-white">12%</p>
             </div>
             <div class="u-text-center">
                <p class="u-text-[10px] u-font-black u-text-muted u-uppercase u-mb-1">Threads</p>
                <p class="u-text-xs u-font-bold u-text-white">64</p>
             </div>
          </footer>
        </div>
      </article>

      <article class="card shadow-xl overflow-hidden">
        <header class="card__header u-bg-page u-p-6">
          <h5 class="card__title u-text-xs u-uppercase u-tracking-widest u-text-muted">System Event Log (Live Stream)</h5>
        </header>
        <div class="card__body u-p-0">
          <div class="u-p-6 u-space-y-4 max-h-[220px] u-overflow-y-auto">
             <div v-for="event in events" :key="event.id" class="u-flex u-gap-4 u-items-start group">
                <span class="u-text-[10px] u-font-black u-text-muted u-font-mono u-mt-1">{{ event.time }}</span>
                <span class="badge badge--small u-flex-shrink-0" :class="event.type === 'INFO' ? 'badge--info' : 'badge--primary'">{{ event.type }}</span>
                <span class="u-text-xs u-font-medium u-text-main group-hover:u-text-primary transition-colors">{{ event.msg }}</span>
             </div>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const latencies = ref([
  { name: 'Identity (IPRS)', ms: 420, percent: 42 },
  { name: 'Revenue (KRA)', ms: 215, percent: 21 },
  { name: 'Huduma Gateway', ms: 110, percent: 11 },
  { name: 'EDRM Archive Cluster', ms: 145, percent: 14 },
  { name: 'Civil Registry', ms: 85, percent: 8 },
  { name: 'KESEL Bridge Core', ms: 14, percent: 2 }
]);

const events = ref([
  { id: 1, time: '05:40:12', type: 'INFO', msg: 'KESEL Heartbeat received from Hub_01' },
  { id: 2, time: '05:40:08', type: 'AUTH', msg: 'OIDC Auth Token Issued: citizen_john_doe' },
  { id: 3, time: '05:40:02', type: 'HUDUMA', msg: 'G-Notify SMS queued for REQ-2026-004' },
  { id: 4, time: '05:39:55', type: 'PROC', msg: 'Workflow Step triggered for REQ-2026-004' },
  { id: 5, time: '05:39:42', type: 'REST', msg: 'API Call to EDRMS Archive: 201 Created' },
  { id: 6, time: '05:39:35', type: 'FILE', msg: 'Document ID-SCAN-99.pdf successfully archived' }
]);

onMounted(() => {
  // Simulate live updates
  setInterval(() => {
    // Randomize Bridge Core
    latencies.value[5].ms = Math.floor(Math.random() * 5) + 12;
    latencies.value[5].percent = latencies.value[5].ms / 10;
    
    // Randomize Huduma
    latencies.value[2].ms = Math.floor(Math.random() * 10) + 105;
    latencies.value[2].percent = latencies.value[2].ms / 10;
  }, 2000);
});
</script>
