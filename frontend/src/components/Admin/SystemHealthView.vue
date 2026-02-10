<template>
  <div class="bg-white p-6 rounded-lg shadow mt-4">
    <div class="flex justify-between items-center mb-8">
      <h3 class="text-xl font-bold text-gray-900 border-l-4 border-green-500 pl-4">Infrastructure & Architecture Health</h3>
      <div class="flex items-center space-x-2">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
        </span>
        <span class="text-xs font-bold text-green-600 uppercase">Live Monitoring</span>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
      <!-- Frontend/UI State -->
      <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
        <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">Frontend Interface</p>
        <div class="flex justify-between items-end">
          <p class="text-xl font-bold text-slate-800">Operational</p>
          <span class="text-[10px] text-green-500 font-bold">STABLE</span>
        </div>
        <div class="mt-2 text-[10px] text-slate-500">Vue 3 + Tailwind</div>
      </div>

      <!-- Backend API State -->
      <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
        <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">Backend Engine</p>
        <div class="flex justify-between items-end">
          <p class="text-xl font-bold text-slate-800">Connected</p>
          <span class="text-[10px] text-green-500 font-bold">34ms</span>
        </div>
        <div class="mt-2 text-[10px] text-slate-500">Django + DRF</div>
      </div>

       <!-- Bridges Status -->
       <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-200">
        <p class="text-[10px] font-bold text-indigo-400 uppercase mb-1">KESEL Bridge</p>
        <div class="flex justify-between items-end">
          <p class="text-xl font-bold text-indigo-900">Active</p>
          <span class="text-[10px] text-green-500 font-bold">SYNCED</span>
        </div>
        <div class="mt-2 text-[10px] text-indigo-500">Cross-MDA Mesh</div>
      </div>

      <div class="bg-cyan-50 p-4 rounded-xl border border-cyan-200">
        <p class="text-[10px] font-bold text-cyan-400 uppercase mb-1">Huduma Bridge</p>
        <div class="flex justify-between items-end">
          <p class="text-xl font-bold text-cyan-900">Online</p>
          <span class="text-[10px] text-green-500 font-bold">Active</span>
        </div>
        <div class="mt-2 text-[10px] text-cyan-500">Citizen Service Layer</div>
      </div>

      <!-- EDRM Status -->
      <div class="bg-blue-50 p-4 rounded-xl border border-blue-200">
        <p class="text-[10px] font-bold text-blue-400 uppercase mb-1">EDRM Archive</p>
        <div class="flex justify-between items-end">
          <p class="text-xl font-bold text-blue-900">Healthy</p>
          <span class="text-[10px] text-green-500 font-bold">99.9%</span>
        </div>
        <div class="mt-2 text-[10px] text-blue-500">Object Storage S3</div>
      </div>
    </div>

    <!-- External Registry Latencies -->
    <div class="mb-8">
      <h4 class="text-sm font-bold text-slate-700 uppercase mb-4">Authoritative Registry Latency (Real-time Simulation)</h4>
      <div class="space-y-4">
        <div v-for="system in latencies" :key="system.name" class="relative pt-1">
          <div class="flex mb-2 items-center justify-between">
            <div>
              <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-indigo-600 bg-indigo-200">
                {{ system.name }}
              </span>
            </div>
            <div class="text-right">
              <span class="text-xs font-semibold inline-block text-indigo-600">
                {{ system.ms }}ms
              </span>
            </div>
          </div>
          <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-indigo-100">
            <div :style="`width: ${system.percent}%`" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500 transition-all duration-500"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Node-RED / Workflow Engine Stats (Mocked) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="p-4 border rounded-xl bg-slate-900 text-white">
        <h5 class="text-xs font-bold text-indigo-400 uppercase mb-4">Workload Distribution</h5>
        <div class="space-y-3">
          <div class="flex justify-between text-sm">
             <span class="text-slate-400">Manual Verification Tasks</span>
             <span class="font-mono text-indigo-300">142</span>
          </div>
          <div class="flex justify-between text-sm">
             <span class="text-slate-400">Automated API Steps</span>
             <span class="font-mono text-indigo-300">1,085</span>
          </div>
          <div class="flex justify-between text-sm">
             <span class="text-slate-400">Escalated Priority</span>
             <span class="font-mono text-red-400">12</span>
          </div>
        </div>
        <div class="mt-6 pt-6 border-t border-slate-800 flex justify-center text-[10px] uppercase font-bold text-slate-500 gap-4">
           <span>Memory: 4.2GB</span>
           <span>CPU: 12%</span>
           <span>Threads: 64</span>
        </div>
      </div>

       <div class="p-4 border rounded-xl bg-white shadow-sm">
        <h5 class="text-xs font-bold text-slate-500 uppercase mb-4">System Event Log (Live Stream)</h5>
        <div class="space-y-2 max-h-[140px] overflow-y-auto font-mono text-[10px]">
           <div v-for="event in events" :key="event.id" class="flex gap-2 p-1 border-b border-slate-50 animate-pulse">
              <span class="text-slate-400">{{ event.time }}</span>
              <span class="text-green-600 font-bold">[{{ event.type }}]</span>
              <span class="text-slate-700">{{ event.msg }}</span>
           </div>
        </div>
      </div>
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
