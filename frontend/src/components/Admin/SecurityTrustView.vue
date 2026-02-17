<template>
    <div class="u-flex u-flex-col u-gap-8 animate-fade-in">
    <!-- Security Header -->
    <header class="card card--dark shadow-xl">
      <div class="card__body u-flex u-justify-between u-items-center u-p-8 u-bg-gradient-dark">
        <div class="page__title-group">
          <h3 class="u-text-2xl u-font-black u-text-white u-mb-1 flex items-center">
            <span class="u-mr-3 text-primary">🛡️</span>
            Security & Trust Enforcement Layer
          </h3>
          <p class="u-text-xs u-font-bold u-uppercase u-tracking-[0.2em] u-text-primary u-opacity-70">
            Zero-Trust Architecture | AES-256 | RSA-4096
          </p>
        </div>
        <div class="u-text-right">
          <p class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Global Security Score</p>
          <div class="u-flex u-items-baseline u-gap-2">
            <span class="u-text-4xl u-font-black u-text-success">A+</span>
            <span class="u-text-xs u-text-success-dark u-font-bold">STANDARDS MET</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Security Summary Grid -->
    <div class="stats-grid">
      <!-- Encryption at Rest -->
      <article class="stats-card stats-card--primary">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
            <div class="stats-card__icon-container">
              <div class="stats-card__icon-glow"></div>
              <div class="stats-card__icon"><i class="bi bi-shield-lock-fill"></i></div>
            </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Data Encryption</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">AES-256</span>
            </div>
            <p class="stats-card__sublabel">100% Volume Encrypted</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <div class="progress-bar progress-bar--sm u-bg-white/10">
            <div class="progress-bar__fill u-bg-white" style="width: 100%"></div>
          </div>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- Identity Trust -->
      <article class="stats-card stats-card--success">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
            <div class="stats-card__icon-container">
              <div class="stats-card__icon-glow"></div>
              <div class="stats-card__icon"><i class="bi bi-person-check-fill"></i></div>
            </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Identity Trust</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">mTLS + OIDC</span>
            </div>
            <p class="stats-card__sublabel">MFA Enforced Region-wide</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <span class="badge badge--success badge--small">SECURE CONNECTION</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- Audit Integrity -->
      <article class="stats-card stats-card--info">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
            <div class="stats-card__icon-container">
              <div class="stats-card__icon-glow"></div>
              <div class="stats-card__icon"><i class="bi bi-journal-check"></i></div>
            </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Log Integrity</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">SHA-512</span>
            </div>
            <p class="stats-card__sublabel">Chain of Trust Validated</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base u-flex u-items-center u-gap-2">
           <i class="bi bi-patch-check-fill u-text-info"></i>
           <span class="u-text-[10px] u-font-black u-text-info u-uppercase">Verified Audit Trail</span>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>

      <!-- Token Lifecycle -->
      <article class="stats-card stats-card--warning">
        <div class="stats-card__overlay"></div>
        <div class="stats-card__content">
          <div class="stats-card__icon-wrapper">
            <div class="stats-card__icon-container">
              <div class="stats-card__icon-glow"></div>
              <div class="stats-card__icon"><i class="bi bi-key-fill"></i></div>
            </div>
          </div>
          <div class="stats-card__text-content">
            <p class="stats-card__label">Active Sessions</p>
            <div class="stats-card__value-wrapper">
              <span class="stats-card__value">{{ activeSessions }}</span>
              <span class="stats-card__unit">LIVE</span>
            </div>
            <p class="stats-card__sublabel">Real-time Anomaly Detection</p>
          </div>
        </div>
        <div class="u-px-6 u-pb-6 u-relative u-z-base">
          <div class="u-flex u-items-center u-gap-2">
            <span class="u-w-2 u-h-2 u-bg-warning u-rounded-full animate-pulse"></span>
            <span class="u-text-[10px] u-font-black u-text-warning u-uppercase">Active Monitoring</span>
          </div>
        </div>
        <div class="stats-card__accent-line"></div>
      </article>
    </div>

    <!-- Threat Map & Consent Registry -->
    <div class="u-grid u-grid-cols-1 lg:u-grid-cols-3 u-gap-8">
      <!-- Consent Monitor -->
      <article class="lg:u-col-span-2 card shadow-xl overflow-hidden">
        <header class="card__header u-bg-page u-py-4">
          <h4 class="card__title u-text-xs u-uppercase u-tracking-widest u-text-muted u-flex u-items-center">
            <span class="u-w-2 u-h-2 u-bg-primary u-rounded-full u-mr-2"></span>
            Citizen Data Consent Registry
          </h4>
        </header>
        <div class="card__body u-p-0">
          <div class="u-divide-y">
            <div v-for="consent in consentLogs" :key="consent.id" class="u-p-6 u-flex u-justify-between u-items-center hover:u-bg-primary-soft transition-colors">
              <div class="u-flex u-items-center u-gap-4">
                <div class="u-w-12 u-h-12 u-bg-primary-soft u-text-primary u-rounded-full u-flex u-items-center u-justify-center u-font-black u-text-xs">
                  {{ consent.mda }}
                </div>
                <div>
                  <p class="u-text-sm u-font-black u-text-main u-mb-1">{{ consent.service }}</p>
                  <p class="u-text-xs u-text-muted">Citizen: <span class="u-font-bold">{{ consent.citizen }}</span> | Issued: {{ consent.date }}</p>
                </div>
              </div>
              <span class="badge badge--success badge--pill">ACTIVE CONSENT</span>
            </div>
          </div>
        </div>
      </article>

      <!-- Policy Enforcement -->
      <article class="card card--dark shadow-xl u-overflow-hidden relative">
        <div class="u-absolute -u-right-10 -u-bottom-10 u-w-40 u-h-40 u-bg-primary/10 u-rounded-full u-blur-3xl"></div>
        <header class="card__header u-bg-transparent u-py-6">
          <h4 class="card__title u-text-xs u-uppercase u-tracking-widest u-text-primary-soft">Policy Enforcement</h4>
        </header>
        <div class="card__body u-p-8 u-pt-0">
          <div class="u-flex u-flex-col u-gap-8">
            <div v-for="policy in policies" :key="policy.name" class="group">
              <div class="u-flex u-justify-between u-items-center u-mb-2">
                <span class="u-text-xs u-font-bold u-text-white u-opacity-80">{{ policy.name }}</span>
                <span class="u-text-[10px] u-font-black u-text-success">ENFORCED</span>
              </div>
              <div class="progress-bar progress-bar--sm u-bg-slate-800">
                <div class="progress-bar__fill u-bg-primary shadow-sm" :style="{ width: `${policy.strength}%` }"></div>
              </div>
            </div>
          </div>

          <div class="u-mt-12 u-p-5 u-bg-slate-800 u-rounded-xl u-border u-border-white/10">
            <p class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest u-mb-3">Bridge Digital Signature</p>
            <code class="u-text-[10px] u-font-mono u-text-muted u-break-all">
              RS256_TRUST_KEY_0x77...9f22_ICTA_SIG
            </code>
          </div>
        </div>
      </article>
    </div>

    <!-- Security Warnings -->
    <div class="card u-bg-warning-soft u-border u-border-warning/20 u-p-6 u-flex u-flex-col u-md-flex-row u-items-center u-justify-between u-gap-6 shadow-lg">
      <div class="u-flex u-items-center u-gap-6">
        <div class="u-w-14 u-h-14 u-bg-warning u-text-white u-rounded-2xl u-flex u-items-center u-justify-center u-text-3xl shadow-lg">
          <i class="bi bi-exclamation-triangle-fill"></i>
        </div>
        <div>
          <p class="u-text-lg u-font-black u-text-warning-dark u-mb-1">Anomaly Detection Alert</p>
          <p class="u-text-sm u-font-medium u-text-warning-dark u-opacity-80">
            3 failed login attempts detected from unusual IP: 192.168.x.x. Source blocked for 15 mins.
          </p>
        </div>
      </div>
      <button class="button button--warning button--pill shadow-md">
        View Threat Details
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const activeSessions = ref(12);

const consentLogs = ref([
  { id: 1, mda: 'KRA', service: 'Tax Identity Verification', citizen: 'John Omondi', date: '2026-02-04 05:30' },
  { id: 2, mda: 'IPRS', service: 'National Registry Validation', citizen: 'Sarah Juma', date: '2026-02-04 05:42' },
  { id: 3, mda: 'HUDUMA', service: 'Service Application Data Access', citizen: 'Jane Doe', date: '2026-02-04 05:45' }
]);

const policies = ref([
  { name: 'Role-Based Access Control', strength: 100 },
  { name: 'API Payload Validation', strength: 95 },
  { name: 'Encryption Strength', strength: 100 },
  { name: 'Audit Log Finality', strength: 100 }
]);

onMounted(() => {
  // Simulate rotation of active sessions
  setInterval(() => {
    activeSessions.value = Math.floor(Math.random() * 5) + 10;
  }, 5000);
});
</script>
