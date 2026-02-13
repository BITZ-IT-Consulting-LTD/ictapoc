<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 relative overflow-hidden">
    <!-- Decorative Background Elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
      <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/30 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-200/30 rounded-full blur-3xl animate-pulse" style="animation-delay: 2s;"></div>
    </div>

    <div class="w-full max-w-5xl z-10 grid grid-cols-1 md:grid-cols-2 gap-0 shadow-2xl rounded-2xl overflow-hidden animate-fade-in-up">
      
      <!-- Left Panel: Branding & Information -->
      <div class="bg-gradient-to-br from-indigo-900 to-slate-900 p-12 text-white flex flex-col justify-between relative">
        <div class="absolute inset-0 bg-[url('https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonalds_Golden_Arches.svg/1024px-McDonalds_Golden_Arches.svg.png')] bg-cover opacity-5"></div> <!-- Placeholder Pattern -->
        
        <div>
           <div class="flex items-center gap-3 mb-8">
              <div class="w-12 h-12 bg-white/10 backdrop-blur rounded-lg flex items-center justify-center border border-white/20">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
              </div>
              <div>
                <h1 class="font-bold text-xl tracking-wide uppercase">Huduma Digital</h1>
                <p class="text-indigo-200 text-xs">Republic of Kenya</p>
              </div>
           </div>
           
           <h2 class="text-4xl font-bold mb-6 leading-tight">Secure Access to Government Services</h2>
           <p class="text-indigo-100/80 leading-relaxed mb-8">
             Access over 5,000 government services securely using your Maisha Digital ID or Government PKI credentials.
           </p>

           <div class="space-y-4">
              <div class="flex items-center gap-4 bg-white/5 p-4 rounded-xl border border-white/10">
                <div class="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                </div>
                <div>
                  <div class="font-bold text-sm">Verified Identity</div>
                  <div class="text-xs text-indigo-200">Biometric & PKI Security</div>
                </div>
              </div>

              <div class="flex items-center gap-4 bg-white/5 p-4 rounded-xl border border-white/10">
                 <div class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
                </div>
                <div>
                  <div class="font-bold text-sm">Single Sign-On</div>
                  <div class="text-xs text-indigo-200">One credential for all MDAs</div>
                </div>
              </div>
           </div>
        </div>

        <div class="text-xs text-indigo-400 mt-12">
          &copy; 2026 ICT Authority. All Rights Reserved.
        </div>
      </div>

      <!-- Right Panel: Login Methods -->
      <div class="bg-white p-12 flex flex-col justify-center relative">
        <div class="absolute top-4 right-4 group">
           <button @click="showLegacy = !showLegacy" class="text-slate-300 hover:text-slate-500 transition-colors">
             <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
           </button>
           <div class="absolute right-0 top-8 bg-slate-800 text-white text-xs p-2 rounded hidden group-hover:block w-32 text-center z-50">
             Toggle Developer Login
           </div>
        </div>

        <div v-if="!showLegacy" class="max-w-sm mx-auto w-full">
           <h3 class="text-2xl font-bold text-slate-800 mb-2">Welcome Back</h3>
           <p class="text-slate-500 mb-8">Choose your secure login method</p>

           <!-- SSO Login Button -->
           <button @click="startSSOFlow" class="w-full group relative flex items-center justify-between p-4 mb-4 bg-indigo-50 border-2 border-indigo-100 rounded-xl hover:bg-indigo-600 hover:border-indigo-600 hover:shadow-lg transition-all duration-300">
             <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-sm group-hover:bg-indigo-500">
                  <svg class="w-6 h-6 text-indigo-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                </div>
                <div class="text-left">
                  <div class="font-bold text-slate-700 group-hover:text-white">Maisha Digital ID</div>
                  <div class="text-xs text-slate-500 group-hover:text-indigo-100">Citizen & Resident SSO</div>
                </div>
             </div>
             <svg class="w-5 h-5 text-slate-300 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
           </button>

           <!-- PKI Login Button -->
           <button @click="startPKIFlow" class="w-full group relative flex items-center justify-between p-4 mb-8 bg-slate-50 border-2 border-slate-100 rounded-xl hover:bg-slate-800 hover:border-slate-800 hover:shadow-lg transition-all duration-300">
             <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-sm group-hover:bg-slate-700">
                  <svg class="w-6 h-6 text-slate-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" /></svg>
                </div>
                <div class="text-left">
                  <div class="font-bold text-slate-700 group-hover:text-white">Gov PKI / Smart Card</div>
                  <div class="text-xs text-slate-500 group-hover:text-slate-300">Officers & Government Staff</div>
                </div>
             </div>
             <svg class="w-5 h-5 text-slate-300 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
           </button>

           <div class="text-center text-xs text-slate-400 mb-8">
              <span class="inline-flex items-center gap-1">
                <svg class="w-3 h-3 text-emerald-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg>
                System Operational
              </span>
              <span class="mx-2">•</span>
              <span class="hover:underline cursor-pointer">Help & Support</span>
           </div>

           <!-- Quick Login Section -->
           <div class="border-t border-slate-100 pt-6">
               <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                   <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                   POC Quick Access (RBAC Testing)
               </p>
               <div class="grid grid-cols-2 gap-2">
                   <button @click="quickLogin('global.officer')" class="text-[10px] bg-indigo-50 text-indigo-700 font-bold py-2 rounded-lg hover:bg-indigo-100 transition-colors border border-indigo-100">Global Officer</button>
                   <button @click="quickLogin('global.supervisor')" class="text-[10px] bg-indigo-50 text-indigo-700 font-bold py-2 rounded-lg hover:bg-indigo-100 transition-colors border border-indigo-100">Global Supervisor</button>
                   <button @click="quickLogin('moh.officer')" class="text-[10px] bg-emerald-50 text-emerald-700 font-bold py-2 rounded-lg hover:bg-emerald-100 transition-colors border border-emerald-100">MOH Officer</button>
                   <button @click="quickLogin('moh.supervisor')" class="text-[10px] bg-emerald-50 text-emerald-700 font-bold py-2 rounded-lg hover:bg-emerald-100 transition-colors border border-emerald-100">MOH Supervisor</button>
                   <button @click="quickLogin('moe.officer')" class="text-[10px] bg-blue-50 text-blue-700 font-bold py-2 rounded-lg hover:bg-blue-100 transition-colors border border-blue-100">MOE Officer</button>
                   <button @click="quickLogin('maggy1')" class="text-[10px] bg-slate-100 text-slate-700 font-bold py-2 rounded-lg hover:bg-slate-200 transition-colors border border-slate-200">Citizen (Maggy)</button>
               </div>
           </div>
        </div>

        <!-- Legacy Login Form (Hidden by default, for fallback) -->
        <div v-else class="max-w-sm mx-auto w-full animate-fade-in">
           <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-bold text-slate-800">System Login</h3>
              <button @click="showLegacy = false" class="text-sm text-slate-500 hover:text-indigo-600">Back to SSO</button>
           </div>
           
           <form @submit.prevent="handleLegacyLogin">
              <div class="mb-4">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Username / Email</label>
                <input type="text" v-model="username" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" required>
              </div>
              <div class="mb-6">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Password</label>
                <input type="password" v-model="password" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" required>
              </div>
              <button type="submit" class="w-full bg-slate-800 text-white py-3 rounded-lg font-bold hover:bg-slate-700 hover:shadow-lg transition-all">
                Authenticate
              </button>
              <div class="mt-4 text-center">
                <router-link to="/register" class="text-sm text-indigo-600 font-bold hover:text-indigo-500">
                    Register New Account
                </router-link>
              </div>
              <p v-if="errorMessage" class="mt-4 text-sm text-rose-500 text-center bg-rose-50 p-2 rounded border border-rose-100">{{ errorMessage }}</p>
           </form>
        </div>
      </div>
    </div>

    <!-- SIMULATION MODALS -->
    
    <!-- 1. SSO Identity Provider Simulation -->
    <div v-if="ssoModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm animate-fade-in">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-2xl overflow-hidden transform scale-100 transition-all">
         <!-- IdP Header -->
         <div class="bg-[#009639] p-4 text-white flex items-center justify-between">
            <div class="flex items-center gap-2">
               <!-- Kenya Flag Colors Simulation -->
               <div class="h-4 w-6 bg-black border border-white/20"></div> 
               <span class="font-bold tracking-wide">Maisha Namba Identity Provider</span>
            </div>
            <button @click="ssoModalOpen = false" class="text-white/70 hover:text-white">&times;</button>
         </div>
         
         <div class="p-8">
            <h3 class="text-lg font-bold text-slate-800 mb-2">Select Digital Identity</h3>
            <p class="text-sm text-slate-500 mb-6">Redirected from <strong>Huduma Service Portal</strong>. Choose an identity to continue.</p>
            
            <div class="space-y-3">
               <button @click="simulateSSOLogin('maggy1', 'citizen')" class="w-full flex items-center gap-4 p-3 border border-slate-200 rounded-xl hover:bg-emerald-50 hover:border-emerald-200 transition-colors text-left group">
                  <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-500 group-hover:bg-emerald-100 group-hover:text-emerald-700">M</div>
                  <div>
                     <div class="font-bold text-slate-700">Maggy One</div>
                     <div class="text-xs text-slate-400">Citizen • ID 555555</div>
                  </div>
               </button>

                <button @click="simulateSSOLogin('citizen1', 'citizen')" class="w-full flex items-center gap-4 p-3 border border-slate-200 rounded-xl hover:bg-emerald-50 hover:border-emerald-200 transition-colors text-left group">
                  <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-500 group-hover:bg-emerald-100 group-hover:text-emerald-700">C</div>
                  <div>
                     <div class="font-bold text-slate-700">Citizen One (Test)</div>
                     <div class="text-xs text-slate-400">Citizen • ID 100</div>
                  </div>
               </button>

               <div class="border-t border-slate-100 my-2"></div>
               
               <button @click="simulateSSOLogin('officer1', 'officer')" class="w-full flex items-center gap-4 p-3 border border-slate-200 rounded-xl hover:bg-blue-50 hover:border-blue-200 transition-colors text-left group">
                  <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-500 group-hover:bg-blue-100 group-hover:text-blue-700">O</div>
                  <div>
                     <div class="font-bold text-slate-700">Officer One</div>
                     <div class="text-xs text-slate-400">Civil Registration Officer</div>
                  </div>
               </button>
            </div>
         </div>
         <div class="bg-slate-50 p-4 border-t border-slate-100 text-center text-xs text-slate-400">
            Secure OpenID Connect Federation
         </div>
      </div>
    </div>

    <!-- 2. PKI Smart Card Simulation -->
    <div v-if="pkiModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/90 backdrop-blur-sm animate-fade-in">
       <div class="bg-white w-full max-w-sm rounded-2xl shadow-2xl p-8 text-center">
          
          <!-- Phase 1: Scanning -->
          <div v-if="pkiPhase === 'scanning'" class="py-8">
             <div class="w-20 h-20 mx-auto bg-indigo-50 rounded-full flex items-center justify-center mb-6 relative">
                <div class="absolute inset-0 border-4 border-indigo-500/20 rounded-full animate-ping"></div>
                <svg class="w-10 h-10 text-indigo-600 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.131A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" /></svg>
             </div>
             <h3 class="text-lg font-bold text-slate-800">Reading Smart Card...</h3>
             <p class="text-sm text-slate-500 mt-2">Please keep your device connected.</p>
          </div>

          <!-- Phase 2: PIN Entry -->
          <div v-if="pkiPhase === 'pin'">
             <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
                <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
             </div>
             <h3 class="text-lg font-bold text-slate-800 mb-1">Certificate Verified</h3>
             <p class="text-sm text-slate-500 mb-6">Subject: <strong>Officer One (MOI)</strong><br>Issuer: GOK Root CA</p>
             
             <div class="mb-6">
                <input type="password" placeholder="Enter Card PIN" class="w-full text-center text-2xl tracking-[0.5em] font-mono px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" autofocus>
             </div>
             
             <button @click="verifyPinAndLogin" class="w-full bg-indigo-600 text-white py-3 rounded-xl font-bold hover:bg-indigo-700 transition-colors">
               Unlock Private Key & Login
             </button>
          </div>

       </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const authStore = useAuthStore()

// State
const showLegacy = ref(false)
const username = ref('')
const password = ref('')
const errorMessage = ref('')

// Simulation State
const ssoModalOpen = ref(false)
const pkiModalOpen = ref(false)
const pkiPhase = ref('scanning')

// --- SSO Logic ---
const startSSOFlow = () => {
  // Simulate Redirect delay
  const btn = document.activeElement;
  if(btn) btn.blur(); // Remove focus
  
  // Show "Redirecting..." spinner? For now just open modal after brief delay
  setTimeout(() => {
    ssoModalOpen.value = true;
  }, 300);
}

const simulateSSOLogin = async (simUser, role) => {
  ssoModalOpen.value = false; // Close modal
  await quickLogin(simUser);
}

const quickLogin = async (usr) => {
    // All POC users now use the standardized password
    const pwd = 'Starten1@';
    await performLogin(usr, pwd);
}

// --- PKI Logic ---
const startPKIFlow = () => {
  pkiModalOpen.value = true;
  pkiPhase.value = 'scanning';
  
  // Simulate Card Read Time
  setTimeout(() => {
    pkiPhase.value = 'pin';
  }, 2000); // 2 second scan
}

const verifyPinAndLogin = async () => {
    // Simulate PIN Verification (Instant)
    pkiPhase.value = 'scanning'; // Reset for next time
    pkiModalOpen.value = false;
    
    // Auth as Officer1
    await performLogin('officer1', 'Starten1@');
}

// --- Core Auth ---
const performLogin = async (usr, pwd) => {
    errorMessage.value = '';
    try {
        await authStore.login(usr, pwd);
        router.push('/dashboard');
    } catch (error) {
         if (error.response?.status === 401) {
            errorMessage.value = 'Authentication Failed. Please try again.';
        } else {
            errorMessage.value = 'System Error. Check connection.';
        }
        // If SSO/PKI fail (e.g. backend reset), show legacy form to see error
        showLegacy.value = true;
    }
}

const handleLegacyLogin = async () => {
  await performLogin(username.value, password.value);
}
</script>

<style scoped>
/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
