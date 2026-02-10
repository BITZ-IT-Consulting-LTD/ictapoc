<template>
  <div class="bg-white p-6 rounded-lg shadow mt-4">
    <div class="flex justify-between items-center mb-8 pb-4 border-b">
      <div>
        <h3 class="text-xl font-bold text-gray-900 flex items-center">
          <span class="mr-2 text-indigo-600">🛡️</span>
          Security & Trust Enforcement Layer
        </h3>
        <p class="text-xs text-gray-500 mt-1 uppercase tracking-widest font-semibold">Zero-Trust Architecture | AES-256 | RSA-4096</p>
      </div>
      <div class="flex items-center space-x-4">
        <div class="text-right">
          <p class="text-[10px] font-bold text-gray-400 uppercase">System Security Score</p>
          <p class="text-2xl font-black text-green-600">A+</p>
        </div>
      </div>
    </div>

    <!-- Security Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Encryption at Rest -->
      <div class="bg-slate-900 p-5 rounded-2xl shadow-xl text-white border border-slate-700">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 bg-slate-800 rounded-lg">🔒</div>
          <span class="text-[10px] font-bold text-green-400 border border-green-400/30 px-2 py-0.5 rounded">ACTIVE</span>
        </div>
        <p class="text-[10px] font-bold text-slate-400 uppercase">Data Encryption</p>
        <p class="text-xl font-bold mt-1">AES-256 GCM</p>
        <div class="mt-4 h-1 w-full bg-slate-800 rounded-full overflow-hidden">
          <div class="h-full bg-indigo-500 w-full"></div>
        </div>
        <p class="text-[10px] text-slate-500 mt-2">100% of Document Store Encrypted</p>
      </div>

      <!-- Identity Trust -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 bg-indigo-50 rounded-lg text-indigo-600">👤</div>
          <span class="text-[10px] font-bold text-indigo-600 border border-indigo-200 px-2 py-0.5 rounded">SECURE</span>
        </div>
        <p class="text-[10px] font-bold text-slate-400 uppercase">Identity Verification</p>
        <p class="text-xl font-bold mt-1">OIDC/JWT 2.0</p>
        <p class="text-[10px] text-slate-500 mt-4">Multi-Factor Authentication Enforced</p>
        <p class="text-[10px] text-slate-500">Mutual TLS for Bridge Connections</p>
      </div>

      <!-- Audit Integrity -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 bg-emerald-50 rounded-lg text-emerald-600">📜</div>
          <span class="text-[10px] font-bold text-emerald-600 border border-emerald-200 px-2 py-0.5 rounded">VERIFIED</span>
        </div>
        <p class="text-[10px] font-bold text-slate-400 uppercase">Log Integrity</p>
        <p class="text-xl font-bold mt-1">SHA-512 Hash</p>
        <div class="flex items-center mt-4 text-[10px] text-emerald-600 font-bold italic">
          <span class="mr-1">✓</span> Chain of Trust Validated
        </div>
      </div>

      <!-- Token Lifecycle -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 bg-orange-50 rounded-lg text-orange-600">🔑</div>
          <span class="text-[10px] font-bold text-orange-600 border border-orange-200 px-2 py-0.5 rounded">MONITORING</span>
        </div>
        <p class="text-[10px] font-bold text-slate-400 uppercase">Active Sessions</p>
        <p class="text-xl font-bold mt-1">{{ activeSessions }} Live</p>
        <p class="text-[10px] text-slate-500 mt-4">Auto-revoked on anomaly detection</p>
      </div>
    </div>

    <!-- Threat Map & Consent Registry -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Consent Monitor -->
      <div class="lg:col-span-2 bg-slate-50 rounded-2xl p-6 border border-slate-200">
        <h4 class="text-sm font-bold text-gray-700 uppercase mb-6 flex items-center">
          <span class="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
          Citizen Data Consent Registry
        </h4>
        <div class="space-y-4">
          <div v-for="consent in consentLogs" :key="consent.id" class="bg-white p-4 rounded-xl border border-slate-100 flex justify-between items-center shadow-sm">
            <div class="flex items-center space-x-4">
              <div class="h-10 w-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold text-xs uppercase">
                {{ consent.mda }}
              </div>
              <div>
                <p class="text-sm font-bold text-gray-800">{{ consent.service }}</p>
                <p class="text-[10px] text-gray-500">Citizen: {{ consent.citizen }} | Granted: {{ consent.date }}</p>
              </div>
            </div>
            <div class="text-right">
              <span class="px-3 py-1 bg-green-50 text-green-700 text-[10px] font-bold rounded-full border border-green-100">
                ACTIVE CONSENT
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Policies -->
      <div class="bg-slate-900 rounded-2xl p-6 text-white overflow-hidden relative">
        <div class="absolute -right-10 -bottom-10 h-40 w-40 bg-indigo-500/10 rounded-full blur-3xl"></div>
        <h4 class="text-sm font-bold text-indigo-400 uppercase mb-6">Policy Enforcement</h4>
        <div class="space-y-6">
          <div v-for="policy in policies" :key="policy.name">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-medium">{{ policy.name }}</span>
              <span class="text-[10px] font-bold text-green-400">ENFORCED</span>
            </div>
            <div class="h-1.5 w-full bg-slate-800 rounded-full">
              <div class="h-full bg-indigo-400 rounded-full" :style="`width: ${policy.strength}%`"></div>
            </div>
          </div>
        </div>

        <div class="mt-12 p-4 bg-slate-800 rounded-xl border border-slate-700">
          <p class="text-[10px] font-bold text-indigo-400 uppercase mb-2">Bridge Digital Signature</p>
          <code class="text-[10px] text-gray-400 font-mono break-all">
            RS256_TRUST_KEY_0x77...9f22_ICTA_SIG
          </code>
        </div>
      </div>
    </div>

    <!-- Security Warnings -->
    <div class="mt-8 p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-center justify-between">
      <div class="flex items-center">
        <span class="text-2xl mr-4">⚠️</span>
        <div>
          <p class="text-sm font-bold text-amber-800">Anomaly Detection Alert</p>
          <p class="text-xs text-amber-700">3 failed login attempts detected from unusual IP: 192.168.x.x. Source blocked for 15 mins.</p>
        </div>
      </div>
      <button class="px-4 py-2 bg-amber-200 text-amber-800 text-xs font-bold rounded-lg hover:bg-amber-300 transition-colors">
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
