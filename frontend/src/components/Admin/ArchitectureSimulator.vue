<template>
  <div class="bg-slate-900 text-white p-6 rounded-xl shadow-2xl mt-4 border border-slate-700">
    <div class="flex justify-between items-center mb-8 border-b border-slate-700 pb-4">
      <div>
        <h3 class="text-2xl font-black tracking-tighter text-indigo-400 uppercase">Architecture Pilot & Simulator</h3>
        <div class="flex items-center gap-2 mt-1">
          <p class="text-xs text-slate-400 uppercase font-bold tracking-widest">Cross-Layer Stress Test & Orchestration Trace</p>
          <div v-if="monitoringStore.isLive" class="flex items-center gap-1.5 px-2 py-0.5 bg-green-500/10 border border-green-500/20 rounded-full">
            <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
            <span class="text-[9px] font-black text-green-500 uppercase tracking-tighter">Live Monitoring Active</span>
          </div>
        </div>
      </div>
      <div class="flex gap-4">
         <button @click="resetSimulation" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-bold transition-all border border-slate-600">
           RESET ENVIRONMENT
         </button>
         <button @click="runFullTrace" :disabled="isSimulating" class="px-6 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-black transition-all shadow-lg shadow-indigo-500/20 flex items-center gap-2">
           <span v-if="isSimulating" class="animate-spin text-lg">⚙️</span>
           <span v-else>🚀 RUN FULL TRACE</span>
         </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <!-- Layer Control Panels -->
      <div class="space-y-6">
        <h4 class="text-xs font-bold text-slate-500 uppercase tracking-widest">Fault Injection</h4>
        
        <!-- Connectivity Layer -->
        <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
          <div class="flex justify-between items-center mb-3">
             <span class="text-xs font-bold text-indigo-300">HUB CONNECTIVITY</span>
             <span :class="bridgeStatus === 'Online' ? 'text-green-400' : 'text-red-400'" class="text-[10px] font-mono">{{ bridgeStatus }}</span>
          </div>
          <div class="grid grid-cols-2 gap-2">
             <button @click="bridgeStatus = 'Online'" :class="bridgeStatus === 'Online' ? 'bg-indigo-600' : 'bg-slate-700'" class="p-1 text-[9px] rounded font-bold transition-colors uppercase">Online</button>
             <button @click="bridgeStatus = 'Isolated'" :class="bridgeStatus === 'Isolated' ? 'bg-red-600' : 'bg-slate-700'" class="p-1 text-[9px] rounded font-bold transition-colors uppercase">Cut</button>
          </div>
        </div>

        <!-- Security Layer -->
        <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
          <div class="flex justify-between items-center mb-3">
             <span class="text-xs font-bold text-indigo-300">SECURITY & TRUST</span>
          </div>
          <button @click="injectSecurityThreat" class="w-full p-2 bg-orange-600/20 hover:bg-orange-600/40 border border-orange-600/50 text-[10px] text-orange-400 rounded font-bold transition-all uppercase">Inject Threat</button>
        </div>

        <!-- Recent Events History -->
        <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700 max-h-[300px] flex flex-col">
           <h4 class="text-[10px] font-bold text-slate-500 uppercase mb-4">Event History</h4>
           <div class="overflow-y-auto space-y-2 flex-1">
              <div v-for="h in traceHistory" :key="h.id" 
                   @click="replayTrace(h)"
                   class="p-2 bg-slate-900 rounded border border-slate-800 hover:border-indigo-500 cursor-pointer transition-colors">
                 <div class="flex justify-between items-start">
                    <span class="text-[9px] font-black text-indigo-400 uppercase tracking-tighter">{{ h.type }}</span>
                    <span class="text-[9px] text-slate-500 font-mono">{{ h.time }}</span>
                 </div>
                 <p class="text-[10px] text-slate-300 truncate">{{ h.details || h.requestId }}</p>
              </div>
              <div v-if="traceHistory.length === 0" class="text-[10px] text-slate-600 italic text-center py-8">
                 No recent activity detected
              </div>
           </div>
        </div>
      </div>

      <!-- Live Trace Visualization -->
      <div class="lg:col-span-3 bg-slate-950 rounded-2xl p-6 border border-slate-800 relative min-h-[500px]">
        <h4 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-8">Architectural Flow Trace</h4>
        
        <div class="space-y-6 relative z-10">
          <div v-for="(step, index) in traceSteps" :key="index" 
               :class="[
                 step.status === 'pending' ? 'opacity-20 translate-x-4' : 'opacity-100 translate-x-0',
                 step.status === 'processing' ? 'border-indigo-500 shadow-indigo-500/20' : 'border-slate-800'
               ]"
               class="flex items-center gap-4 bg-slate-900 p-4 rounded-xl border transition-all duration-700">
            
            <div :class="[
              step.status === 'completed' ? 'bg-green-500 shadow-green-500/50' : 
              step.status === 'processing' ? 'bg-indigo-500 animate-pulse' : 'bg-slate-800'
            ]" class="h-10 w-10 shrink-0 rounded-full flex items-center justify-center font-bold text-white shadow-lg">
              <span v-if="step.status === 'completed'">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>

            <div class="flex-1">
              <div class="flex justify-between">
                <p class="text-[10px] font-black text-indigo-400 uppercase tracking-tighter">{{ step.layer }}</p>
                <p v-if="step.latency" class="text-[10px] font-mono text-slate-500">{{ step.latency }}ms</p>
              </div>
              <p class="text-sm font-bold text-slate-100">{{ step.activity }}</p>
              <p v-if="step.output" class="text-[10px] font-mono text-green-400 mt-1 bg-black/40 p-1 px-2 rounded">{{ step.output }}</p>
            </div>
            
            <div v-if="step.status === 'processing'" class="flex gap-1">
               <span class="h-1 w-1 bg-indigo-500 rounded-full animate-bounce"></span>
               <span class="h-1 w-1 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
               <span class="h-1 w-1 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
            </div>
          </div>
        </div>

        <!-- Connection Lines (Visual Decor) -->
        <div class="absolute left-11 top-24 bottom-24 w-0.5 bg-slate-800 -z-1"></div>
        
        <!-- Empty State -->
        <div v-if="!isSimulating && traceSteps.every(s => s.status === 'pending')" class="absolute inset-0 flex items-center justify-center flex-col opacity-40">
           <span class="text-4xl mb-4">📡</span>
           <p class="text-sm font-bold tracking-widest uppercase">Awaiting Activation</p>
           <p class="text-[10px] text-slate-400 mt-1">Real-world system activity will appear here automatically</p>
        </div>
      </div>
    </div>

    <!-- Alert Banner -->
    <transition name="fade">
      <div v-if="activeAlert" :class="activeAlert.type === 'error' ? 'bg-red-900/30 text-red-400 border-red-900/50' : 'bg-orange-900/30 text-orange-400 border-orange-900/50'" 
           class="mt-8 p-4 rounded-xl border flex items-center justify-between animate-pulse">
        <div class="flex items-center">
          <span class="mr-4 text-xl">{{ activeAlert.type === 'error' ? '🚫' : '⚠️' }}</span>
          <div>
            <p class="text-xs font-black uppercase tracking-widest">{{ activeAlert.title }}</p>
            <p class="text-xs opacity-70">{{ activeAlert.msg }}</p>
          </div>
        </div>
        <button @click="activeAlert = null" class="text-xs underline font-bold uppercase">Acknowledge</button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useSystemMonitoringStore } from '../../store/systemMonitoring';

const monitoringStore = useSystemMonitoringStore();
const isSimulating = ref(false);
const bridgeStatus = ref('Online');
const selectedRegistry = ref('IPRS');
const activeAlert = ref(null);
const traceHistory = ref([]);
let pollingInterval = null;

const traceSteps = ref([
  { layer: 'Presentation Layer', activity: 'Citizen submits Application via HTTPS', status: 'pending', output: null },
  { layer: 'Security & Trust Layer', activity: 'Validating Device Fingerprint & Token Signature', status: 'pending', output: null },
  { layer: 'Interoperability Bridge', activity: 'KESEL Bridge: Identity Handshake Request', status: 'pending', output: null },
  { layer: 'Authoritative Layer', activity: 'IPRS: Verified National ID Status', status: 'pending', output: null, latency: null },
  { layer: 'Orchestration Layer', activity: 'Workflow Step: G-Notify Response Triggered', status: 'pending', output: null },
  { layer: 'Data Layer', activity: 'EDRM: Artifact Serialized to Central Archive', status: 'pending', output: null }
]);

// Listen for actual system events
watch(() => monitoringStore.activeTrace, (newTrace) => {
  if (newTrace && !isSimulating.value) {
    console.log("Real System Event Detected:", newTrace);
    
    // Add to history
    traceHistory.value.unshift({
      id: Date.now(),
      time: new Date().toLocaleTimeString(),
      ...newTrace
    });
    
    // Limit history size
    if (traceHistory.value.length > 20) traceHistory.value.pop();

    processTrace(newTrace);
  }
});

const replayTrace = (h) => {
  if (isSimulating.value) return;
  processTrace(h);
};

const processTrace = (newTrace) => {
    // Customize the trace labels based on the actual event
    if (newTrace.type === 'SERVICE_SUBMISSION') {
      traceSteps.value[0].activity = `Live Submission: ${newTrace.requestId || 'Incoming'}`;
      traceSteps.value[3].activity = `IPRS: National Identity Check initiated`;
    } else if (newTrace.type === 'WORKFLOW_STEP_COMPLETION') {
      traceSteps.value[0].activity = `Action by Officer: ${newTrace.requestId || 'Tracing'}`;
      traceSteps.value[4].activity = `Orchestration: Progressing Request ${newTrace.requestId}`;
    } else if (newTrace.type === 'BRIDGE_EXCHANGE') {
      traceSteps.value[2].activity = `KeSEL: Secure Handshake Verified`;
      traceSteps.value[3].output = `REGISTRY_OK: ${newTrace.details}`;
    } else if (newTrace.type === 'INTERNAL_PROFILE_UPDATE') {
      traceSteps.value[4].activity = `Orchestration: Internal Profile Update Executed`;
      traceSteps.value[3].activity = `Authority: Internal System Update`;
      traceSteps.value[3].output = `SUCCESS: Citizen Profile Synced`;
    } else if (newTrace.type === 'DIGITAL_SIGNATURE_VERIFIED') {
      traceSteps.value[1].status = 'completed';
      traceSteps.value[1].activity = 'Security Server: NPKI Signature Verified';
      traceSteps.value[1].output = 'PKI_STATUS: VALID (TRUSTED ROOT)';
    }

    runFullTrace();
};

onMounted(() => {
  pollingInterval = setInterval(() => {
    monitoringStore.pollForEvents();
  }, 3000);
});

onUnmounted(() => {
  if (pollingInterval) clearInterval(pollingInterval);
});

const runFullTrace = async () => {
  if (isSimulating.value) return;
  isSimulating.value = true;
  
  // Reset steps
  traceSteps.value.forEach(s => {
    s.status = 'pending';
    s.output = null;
    s.latency = null;
  });

  for (let i = 0; i < traceSteps.value.length; i++) {
    traceSteps.value[i].status = 'processing';
    
    // Simulate thinking/network time
    await new Promise(r => setTimeout(r, 1200 + Math.random() * 800));
    
    if (bridgeStatus.value === 'Isolated' && i >= 2) {
      traceSteps.value[i].status = 'error';
      activeAlert.value = {
        title: 'Connectivity Failure',
        msg: 'The Interoperability Bridge is unreachable. Simulation halted.',
        type: 'error'
      };
      isSimulating.value = false;
      return;
    }

    traceSteps.value[i].status = 'completed';
    
    // Add fake results
    if (i === 1) traceSteps.value[i].output = 'JWT_ALG_RS256 VALIDATED';
    if (i === 3) {
      traceSteps.value[i].latency = Math.floor(Math.random() * 300) + 150;
      traceSteps.value[i].output = 'IDENTITY: STATUS_ACTIVE';
    }
    if (i === 5) traceSteps.value[i].output = 'EDRM_UID: x992-bb82-f011';
  }

  isSimulating.value = false;
};

const injectSecurityThreat = () => {
  activeAlert.value = {
    title: 'Security Anomaly Detected',
    msg: 'IP: 197.x.x.x detected with mismatched session token. JWT invalidated.',
    type: 'warning'
  };
};

const simulateRegistryLatency = () => {
  const step = traceSteps.value[3];
  step.latency = 2500;
  activeAlert.value = {
    title: 'High Latency Spike',
    msg: `${selectedRegistry.value} is responding slower than usual (2.5s). Retries initiated.`,
    type: 'warning'
  };
};

const resetSimulation = () => {
  bridgeStatus.value = 'Online';
  activeAlert.value = null;
  traceSteps.value.forEach(s => s.status = 'pending');
  isSimulating.value = false;
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
