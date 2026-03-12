<template>
  <main class="page life-event-page">
    <div v-if="lifeEvent" class="animate-fade-in u-flex u-flex-col u-gap-12">
      <!-- Premium Event Header -->
      <header
        class="page__header page__header--premium u-p-12 u-rounded-[3rem] u-shadow-2xl u-relative u-overflow-hidden u-bg-white u-border u-border-slate-100">
        <!-- Abstract Background Shape -->
        <div class="u-absolute u-top-0 u-right-0 u-w-96 u-h-96 u-bg-primary/5 u-rounded-full -u-translate-y-1/2 u-translate-x-1/2 u-blur-3xl"></div>
        
        <div class="u-flex u-items-center u-gap-8 u-relative u-z-10">
          <div class="u-w-24 u-h-24 u-rounded-3xl u-bg-primary u-text-white u-flex u-items-center u-justify-center u-shadow-2xl shadow-primary/20" style="font-size: 3rem;">
            <i :class="getEventIcon(lifeEvent.name)"></i>
          </div>
          <div class="u-flex-1">
            <div class="u-flex u-items-center u-gap-3 u-mb-2">
              <router-link to="/dashboard" class="u-text-[10px] u-font-black u-text-primary u-uppercase u-tracking-widest hover:u-underline">
                <i class="bi bi-arrow-left"></i> Dashboard
              </router-link>
              <span class="u-text-slate-300">/</span>
              <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Life Event</span>
            </div>
            <h1 class="u-text-4xl u-font-black u-text-main u-tracking-tight u-mb-2">{{ lifeEvent.name }}</h1>
            <p class="u-text-lg u-text-muted u-max-w-2xl u-leading-relaxed">{{ lifeEvent.description }}</p>
          </div>
        </div>
      </header>

      <!-- Services Grid -->
      <section class="u-flex u-flex-col u-gap-8">
        <div class="u-flex u-items-center u-justify-between">
          <h2 class="u-text-xl u-font-black u-text-main u-uppercase u-tracking-widest">Available Registry Services</h2>
          <span class="badge badge--primary">{{ lifeEvent.services.length }} Available</span>
        </div>

        <div v-if="lifeEvent.services.length === 0" class="u-p-20 u-bg-white u-rounded-3xl u-border-2 u-border-dashed u-border-slate-200 u-flex u-flex-col u-items-center u-justify-center text-center">
            <i class="bi bi-inbox u-text-5xl u-mb-4 u-text-slate-300"></i>
            <h3 class="u-text-lg u-font-bold u-text-main">No services found</h3>
            <p class="u-text-sm u-text-muted u-max-w-xs u-mt-2">There are currently no services linked to the "{{ lifeEvent.name }}" event in the official registry.</p>
        </div>

        <div v-else class="u-grid u-gap-6 md:u-grid-cols-2 lg:u-grid-cols-3">
          <div v-for="service in lifeEvent.services" :key="service.id" 
            class="card u-p-8 u-flex u-flex-col u-rounded-[2rem] hover:u-shadow-2xl transition-all border border-slate-100 hover:border-primary/20 group">
            <div class="u-flex u-items-center u-justify-between u-mb-6">
              <div class="u-w-12 u-h-12 u-rounded-2xl u-bg-slate-50 u-flex u-items-center u-justify-center u-text-primary group-hover:u-bg-primary group-hover:u-text-white transition-colors" style="font-size: 1.25rem;">
                <i class="bi bi-shield-lock-fill"></i>
              </div>
              <span class="badge badge--info u-text-[10px] u-font-black u-uppercase">{{ getMdaName(service.mda) }}</span>
            </div>
            <h3 class="u-text-lg u-font-black u-text-main u-mb-2 group-hover:u-text-primary transition-colors">{{ service.display_name }}</h3>
            <p class="u-text-xs u-text-muted u-mb-8 u-leading-relaxed">Access authoritative information and apply for {{ service.display_name.toLowerCase() }} through the secure national portal.</p>
            
            <div class="u-mt-auto">
              <router-link :to="`/apply/${service.id}`" class="button button--primary button--pill u-w-full u-text-xs u-font-black u-uppercase u-tracking-widest py-4">
                Begin Application
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- Support Footer -->
      <footer class="u-p-10 u-bg-slate-50 u-rounded-[3rem] u-flex u-flex-col md:u-flex-row u-items-center u-justify-between u-gap-8 u-border u-border-slate-200/50">
        <div class="u-flex u-items-center u-gap-6 text-center md:u-text-left">
          <div class="u-w-14 u-h-14 u-rounded-full u-bg-white u-shadow-md u-flex u-items-center u-justify-center u-text-success text-2xl">
            <i class="bi bi-headset"></i>
          </div>
          <div>
            <h4 class="u-text-lg u-font-black u-text-main">Need assistance?</h4>
            <p class="u-text-sm u-text-muted">Our support officers are available 24/7 via the Huduma Bridge.</p>
          </div>
        </div>
        <div class="u-flex u-gap-4">
          <button class="button button--secondary button--pill px-8 u-font-black u-text-[10px] u-uppercase">Contact Support</button>
          <button class="button button--primary button--pill px-8 u-font-black u-text-[10px] u-uppercase">View FAQs</button>
        </div>
      </footer>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="u-flex u-flex-col u-items-center u-justify-center u-py-40">
      <div class="u-w-16 u-h-16 u-border-4 u-border-slate-100 u-border-t-primary u-rounded-full u-animate-spin u-mb-6"></div>
      <p class="u-text-xs u-font-black u-uppercase u-tracking-[0.4em] u-text-primary u-animate-pulse">Loading National Service Registry...</p>
    </div>

    <!-- Not Found State -->
    <div v-else class="u-flex u-flex-col u-items-center u-justify-center u-py-40 text-center">
        <i class="bi bi-search u-text-5xl u-mb-4 u-text-slate-300"></i>
        <h2 class="u-text-2xl u-font-black u-text-main u-mb-2">Life Event Not Found</h2>
        <p class="u-text-muted u-max-w-md u-mb-8">The life event you are looking for does not exist in our authoritative registry or has been moved.</p>
        <router-link to="/dashboard" class="button button--primary button--pill px-10">Return to Dashboard</router-link>
    </div>
  </main>
</template>

<script setup>
  import { ref, onMounted, computed, watch } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useCitizenStore } from '../store/citizen';
  import { useMdaStore } from '../store/mda';
  import { useAuthStore } from '../store/auth';

  const route = useRoute();
  const router = useRouter();
  const citizenStore = useCitizenStore();
  const mdaStore = useMdaStore();
  const authStore = useAuthStore();

  const eventId = computed(() => route.params.id);
  const lifeEvent = ref(null);
  const loading = ref(true);

  const mdas = computed(() => mdaStore.mdas);

  const getMdaName = (mdaId) => {
    if (!mdaId) return 'All Agencies';
    if (mdaId && typeof mdaId === 'object') return mdaId.name;
    const mda = mdas.value.find(m => String(m.id) === String(mdaId));
    return mda ? mda.name : (mdaId.name || `Agency #${mdaId}`);
  };

  const getEventIcon = (eventName) => {
    const icons = {
      'Getting Married': 'bi-heart-fill',
      'Starting a Business': 'bi-briefcase-fill',
      'Buying Property': 'bi-house-fill',
      'Having a Child': 'bi-baby-carriage',
      'Birth': 'bi-baby-carriage',
      'Education': 'bi-mortarboard-fill',
      'Employment': 'bi-person-workspace',
      'Retirement': 'bi-sun-fill',
      'Death & Cemetery': 'bi-flower1',
      'Death': 'bi-flower1',
      'Legal Matters': 'bi-scales',
      'Health & Wellness': 'bi-heart-pulse-fill',
      'Health': 'bi-heart-pulse-fill',
      'Transport': 'bi-truck',
      'Travel': 'bi-airplane-fill',
      'Family': 'bi-people-fill',
      'Financial': 'bi-bank2',
      'Governance': 'bi-building-fill',
      'Identity': 'bi-person-badge-fill',
      'Property': 'bi-house-fill'
    };
    return icons[eventName] || 'bi-stars';
  };

  const findEvent = () => {
    const groups = {};
    citizenStore.availableServices.forEach(svc => {
      const gName = svc.life_event_group || 'General Services';
      const id = gName.toLowerCase().replace(/\s+/g, '-');
      if (!groups[id]) {
        groups[id] = {
          id,
          name: gName,
          description: `Authoritative G2C services linked to your ${gName.toLowerCase()} journey. Securely managed via the national registry.`,
          services: []
        };
      }
      groups[id].services.push({
        id: svc.service_code,
        display_name: svc.service_name,
        mda: svc.mda
      });
    });
    
    lifeEvent.value = groups[eventId.value] || null;
    loading.value = false;
  };

  onMounted(async () => {
    loading.value = true;
    if (mdaStore.mdas.length === 0) {
        await mdaStore.fetchMdas();
    }
    if (citizenStore.availableServices.length === 0) {
      await citizenStore.fetchAvailableServices();
    }
    findEvent();
  });

  watch(eventId, () => {
    findEvent();
  });
</script>

<style scoped>
  .life-event-page {
    padding: 3rem;
    max-width: 1400px;
    margin: 0 auto;
    min-height: 80vh;
  }

  .page__header--premium {
    background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
  }

  @media (max-width: 768px) {
    .life-event-page {
      padding: 1.5rem;
    }
    .page__header--premium {
      padding: 2rem;
      border-radius: 2rem;
    }
  }
</style>
