<template>
  <main class="page home-page">
    <section
      class="hero min-h-[80vh] flex flex-col items-center justify-center text-center p-10 relative overflow-hidden">
      <!-- Decorative Blobs -->
      <div class="absolute -top-40 -left-40 w-96 h-96 bg-indigo-500/10 rounded-full blur-[100px]"></div>
      <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-emerald-500/10 rounded-full blur-[100px]"></div>

      <header class="hero__header animate-fade-in mb-12">
        <div
          class="w-24 h-24 bg-primary text-white rounded-[2rem] flex items-center justify-center text-5xl mx-auto mb-10 shadow-2xl shadow-indigo-200 rotate-12 hover:rotate-0 transition-transform duration-500">
          <i class="bi bi-bank2"></i>
        </div>
        <h1 class="text-6xl font-black text-gray-900 mb-6 tracking-tighter leading-tight">
          The Authority of <br><span class="text-premium">Huduma Digital</span>
        </h1>
        <p class="text-xl text-gray-400 max-w-2xl mx-auto font-medium leading-relaxed">
          National Enterprise Gateway for Authoritative Registry Services.
          Unifying governance through secure, cryptographic lifecycle orchestration.
        </p>
      </header>

      <div class="flex flex-col sm:flex-row gap-6 animate-slide-in">
        <router-link to="/login"
          class="button button--primary button--pill px-10 py-5 text-lg font-black uppercase tracking-[0.2em] shadow-2xl shadow-indigo-100">
          View All POC Accounts
        </router-link>
        <router-link to="/register"
          class="button button--secondary button--pill px-10 py-5 text-lg font-black uppercase tracking-[0.2em]">
          Citizen Enrollment
        </router-link>
      </div>

      <footer class="mt-24 grid grid-cols-1 md:grid-cols-3 gap-12 max-w-5xl mx-auto animate-fade-in opacity-60">
        <div class="flex flex-col items-center">
          <i class="bi bi-shield-check text-2xl text-primary mb-3"></i>
          <h3 class="text-xs font-black uppercase tracking-widest text-gray-900 mb-1">Authoritative</h3>
          <p class="text-[10px] text-gray-400 font-bold uppercase">Source of Truth Records</p>
        </div>
        <div class="flex flex-col items-center">
          <i class="bi bi-lightning-charge text-2xl text-premium mb-3"></i>
          <h3 class="text-xs font-black uppercase tracking-widest text-gray-900 mb-1">Automated</h3>
          <p class="text-[10px] text-gray-400 font-bold uppercase">Whole-of-Gov Orchestration</p>
        </div>
        <div class="flex flex-col items-center">
          <i class="bi bi-fingerprint text-2xl text-indigo-600 mb-3"></i>
          <h3 class="text-xs font-black uppercase tracking-widest text-gray-900 mb-1">Secure</h3>
          <p class="text-[10px] text-gray-400 font-bold uppercase">MFA & PKI Integrated</p>
        </div>
      </footer>
    </section>

    <section class="actor-access" aria-labelledby="actor-access-title">
      <header class="actor-access__header">
        <div>
          <span class="actor-access__eyebrow"><i class="bi bi-lightning-charge-fill"></i> Permanent POC access</span>
          <h2 id="actor-access-title">Explore the platform by actor</h2>
          <p>Choose a representative user journey. Each button opens the POC using a seeded demonstration account.</p>
        </div>
        <span class="actor-access__status"><i class="bi bi-check-circle-fill"></i> {{ actorCategories.length }} actor categories</span>
      </header>

      <div class="actor-access__grid">
        <button
          v-for="actor in actorCategories"
          :key="actor.id"
          type="button"
          class="actor-card"
          :class="[`actor-card--${actor.tone}`, { 'actor-card--loading': activeActor === actor.id }]"
          :disabled="Boolean(activeActor)"
          :aria-label="`Enter the POC as ${actor.name}`"
          @click="loginAsActor(actor)"
        >
          <span class="actor-card__icon"><i :class="actor.icon"></i></span>
          <span class="actor-card__body">
            <strong>{{ actor.name }}</strong>
            <small>{{ actor.description }}</small>
            <code>{{ actor.username }}</code>
          </span>
          <span class="actor-card__action">
            <i v-if="activeActor === actor.id" class="bi bi-arrow-repeat actor-card__spinner"></i>
            <i v-else class="bi bi-arrow-right"></i>
          </span>
        </button>
      </div>

      <p v-if="accessError" class="actor-access__error" role="alert">
        <i class="bi bi-exclamation-triangle-fill"></i> {{ accessError }}
      </p>

      <footer class="actor-access__footer">
        <span><i class="bi bi-shield-check"></i> Demonstration data only</span>
        <router-link to="/login">Open the complete seeded account matrix <i class="bi bi-arrow-right"></i></router-link>
      </footer>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const authStore = useAuthStore()
const activeActor = ref('')
const accessError = ref('')

const actorCategories = [
  {
    id: 'citizen',
    name: 'Citizen',
    username: 'citizen1',
    description: 'Discover services, apply and track requests',
    icon: 'bi bi-person-vcard-fill',
    tone: 'citizen'
  },
  {
    id: 'employee',
    name: 'Government Employee',
    username: 'employee1',
    description: 'Access MDA-scoped government services',
    icon: 'bi bi-person-badge-fill',
    tone: 'employee'
  },
  {
    id: 'officer',
    name: 'Service Officer',
    username: 'officer1',
    description: 'Claim and process frontline service tasks',
    icon: 'bi bi-inboxes-fill',
    tone: 'operations'
  },
  {
    id: 'supervisor',
    name: 'Supervisor',
    username: 'supervisor1',
    description: 'Supervise queues, approvals and service levels',
    icon: 'bi bi-clipboard2-check-fill',
    tone: 'oversight'
  },
  {
    id: 'registrar',
    name: 'Registrar',
    username: 'registrar1',
    description: 'Complete formal review and issuance',
    icon: 'bi bi-patch-check-fill',
    tone: 'registrar'
  },
  {
    id: 'hospital',
    name: 'Hospital Staff',
    username: 'nurse.jane',
    description: 'Initiate health-facility notifications',
    icon: 'bi bi-hospital-fill',
    tone: 'health'
  },
  {
    id: 'mda-admin',
    name: 'MDA Administrator',
    username: 'moh.admin',
    description: 'Configure MDA workflows, schemas and forms',
    icon: 'bi bi-buildings-fill',
    tone: 'mda'
  },
  {
    id: 'cross-mda',
    name: 'Cross-MDA Operations',
    username: 'global.officer',
    description: 'Work across government service queues',
    icon: 'bi bi-globe2',
    tone: 'global'
  },
  {
    id: 'platform-admin',
    name: 'Platform Administrator',
    username: 'admin',
    description: 'Inspect architecture and govern the platform',
    icon: 'bi bi-diagram-3-fill',
    tone: 'admin'
  }
]

const loginAsActor = async actor => {
  activeActor.value = actor.id
  accessError.value = ''

  try {
    await authStore.login(actor.username, 'Starten1@')
    await router.push('/dashboard')
  } catch (error) {
    accessError.value = error.response?.status === 401
      ? `The seeded ${actor.name} account is not available. Rerun the POC seed.`
      : 'The POC could not be reached. Confirm that the backend is running.'
  } finally {
    activeActor.value = ''
  }
}
</script>

<style scoped>
.actor-access {
  width: min(1180px, calc(100% - 2rem));
  margin: 0 auto 5rem;
  padding: 2rem;
  border: 1px solid #dce5ea;
  border-radius: 2rem;
  background: linear-gradient(145deg, #ffffff, #f7fafc);
  box-shadow: 0 24px 65px rgba(15, 31, 45, .1);
}

.actor-access__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.actor-access__eyebrow {
  display: flex;
  align-items: center;
  gap: .45rem;
  margin-bottom: .45rem;
  color: #0f766e;
  font-size: .68rem;
  font-weight: 900;
  letter-spacing: .14em;
  text-transform: uppercase;
}

.actor-access__header h2 {
  margin: 0;
  color: #172033;
  font-size: clamp(1.7rem, 3vw, 2.5rem);
  font-weight: 900;
  letter-spacing: -.04em;
}

.actor-access__header p {
  max-width: 680px;
  margin: .45rem 0 0;
  color: #718096;
  font-size: .9rem;
}

.actor-access__status {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  gap: .4rem;
  padding: .55rem .75rem;
  border-radius: 999px;
  color: #047857;
  background: #ecfdf5;
  font-size: .64rem;
  font-weight: 900;
  text-transform: uppercase;
}

.actor-access__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .75rem;
}

.actor-card {
  --actor-color: #4f46e5;
  display: grid;
  grid-template-columns: 2.65rem minmax(0, 1fr) 1.5rem;
  align-items: center;
  gap: .8rem;
  min-width: 0;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  color: #243244;
  background: white;
  text-align: left;
  cursor: pointer;
  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}

.actor-card:hover:not(:disabled),
.actor-card:focus-visible {
  z-index: 1;
  border-color: color-mix(in srgb, var(--actor-color) 55%, white);
  box-shadow: 0 12px 28px color-mix(in srgb, var(--actor-color) 13%, transparent);
  transform: translateY(-3px);
  outline: none;
}

.actor-card:disabled {
  cursor: wait;
  opacity: .65;
}

.actor-card--citizen { --actor-color: #0ea5e9; }
.actor-card--employee { --actor-color: #6366f1; }
.actor-card--operations { --actor-color: #2563eb; }
.actor-card--oversight { --actor-color: #d97706; }
.actor-card--registrar { --actor-color: #7c3aed; }
.actor-card--health { --actor-color: #e11d48; }
.actor-card--mda { --actor-color: #059669; }
.actor-card--global { --actor-color: #0f766e; }
.actor-card--admin { --actor-color: #dc2626; }

.actor-card__icon {
  display: grid;
  width: 2.65rem;
  height: 2.65rem;
  place-items: center;
  border-radius: .8rem;
  color: white;
  background: var(--actor-color);
  box-shadow: 0 7px 16px color-mix(in srgb, var(--actor-color) 22%, transparent);
  font-size: 1rem;
}

.actor-card__body {
  min-width: 0;
}

.actor-card__body strong,
.actor-card__body small,
.actor-card__body code {
  display: block;
}

.actor-card__body strong {
  font-size: .78rem;
  font-weight: 900;
}

.actor-card__body small {
  margin: .15rem 0 .3rem;
  overflow: hidden;
  color: #7b8794;
  font-size: .62rem;
  font-weight: 650;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actor-card__body code {
  color: var(--actor-color);
  font-size: .58rem;
  font-weight: 800;
}

.actor-card__action {
  color: var(--actor-color);
  text-align: center;
}

.actor-card__spinner {
  display: inline-block;
  animation: actor-spin .8s linear infinite;
}

@keyframes actor-spin {
  to { transform: rotate(360deg); }
}

.actor-access__error {
  display: flex;
  align-items: center;
  gap: .5rem;
  margin: 1rem 0 0;
  padding: .75rem 1rem;
  border-radius: .75rem;
  color: #b91c1c;
  background: #fef2f2;
  font-size: .75rem;
  font-weight: 800;
}

.actor-access__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid #e8edf1;
  color: #84909c;
  font-size: .68rem;
  font-weight: 800;
}

.actor-access__footer span,
.actor-access__footer a {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
}

.actor-access__footer a {
  color: #4f46e5;
}

@media (max-width: 900px) {
  .actor-access__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .actor-access {
    padding: 1.2rem;
    border-radius: 1.25rem;
  }

  .actor-access__header,
  .actor-access__footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .actor-access__grid {
    grid-template-columns: 1fr;
  }
}
</style>
