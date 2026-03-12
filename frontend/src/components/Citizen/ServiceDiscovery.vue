<template>
  <div class="service-discovery space-y-12">
    <div class="header-section">
      <h1 class="title">Citizen <span class="text-highlight">Life Events</span></h1>
      <p class="subtitle">Authoritative G2C services organized around how you live and work</p>
    </div>

    <!-- Empty State -->
    <div v-if="!lifeEvents?.length" class="empty-state">
      <div class="empty-icon shadow-inner">
        <i class="bi bi-cloud-slash"></i>
      </div>
      <h3 class="empty-title">Service Registry Offline</h3>
      <p class="empty-message">The authoritative service catalogue is currently unavailable in your region. Please verify your connection.</p>
    </div>

    <!-- Events Grid -->
    <div v-else class="events-grid">
      <article v-for="event in lifeEvents" :key="event.id" class="event-card" @click="navigateToEvent(event.id)">
        <div class="event-icon-container">
          <div class="event-icon shadow-lg">
            <i :class="getEventIcon(event.name)"></i>
          </div>
          <div class="event-glow"></div>
        </div>
        
        <div class="event-content">
          <h2 class="event-name">{{ event.name }}</h2>
          <p class="event-description">{{ event.description }}</p>
          
          <div class="featured-services mt-6">
            <div v-for="svc in event.services.slice(0, 2)" :key="svc.id" class="service-item">
               <span class="service-dot"></span>
               <span class="service-text">{{ svc.display_name }}</span>
            </div>
            <div v-if="event.services.length > 2" class="more-indicator">
               +{{ event.services.length - 2 }} more protocols
            </div>
          </div>
        </div>
        
        <div class="event-footer">
          <router-link :to="`/life-event/${event.id}`" class="explore-btn" @click.stop>
            <span>Access Registry</span>
            <i class="bi bi-arrow-right-short"></i>
          </router-link>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  lifeEvents: {
    type: Array,
    default: () => []
  }
});

const router = useRouter();

const navigateToEvent = (id) => {
  router.push(`/life-event/${id}`);
};

const getEventIcon = (name) => {
  const icons = {
    'Birth': 'bi-baby',
    'Education': 'bi-book',
    'Employment': 'bi-briefcase',
    'Business': 'bi-building',
    'Health': 'bi-heart-pulse',
    'Marriage': 'bi-people',
    'Death': 'bi-house-heart',
    'Housing': 'bi-house',
    'Transport': 'bi-car-front'
  };
  return icons[name] || 'bi-stars';
};
</script>

<style scoped>
.service-discovery {
  width: 100%;
}

.header-section {
  max-width: 600px;
}

.title {
  font-size: 2.5rem;
  font-weight: 900;
  letter-spacing: -0.05em;
  line-height: 1;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.text-highlight {
  color: #ef4444;
}

.subtitle {
  font-size: 1rem;
  color: #64748b;
  font-weight: 500;
}

/* Events Grid */
.events-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.event-card {
  position: relative;
  background: white;
  border-radius: 2.5rem;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.event-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.1);
  border-color: #ef444433;
}

.event-icon-container {
  position: relative;
  margin-bottom: 2rem;
  align-self: center;
}

.event-icon {
  width: 5rem;
  height: 5rem;
  background: #f8fafc;
  color: #ef4444;
  border-radius: 1.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  z-index: 2;
  position: relative;
  transition: all 0.5s;
}

.event-card:hover .event-icon {
  background: #ef4444;
  color: white;
}

.event-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 7rem;
  height: 7rem;
  background: radial-gradient(circle, rgba(239, 68, 68, 0.15) 0%, transparent 70%);
  z-index: 1;
  opacity: 0;
  transition: opacity 0.5s;
}

.event-card:hover .event-glow {
  opacity: 1;
}

.event-content {
  text-align: center;
  flex: 1;
}

.event-name {
  font-size: 1.5rem;
  font-weight: 900;
  color: #1e293b;
  margin-bottom: 0.75rem;
  letter-spacing: -0.025em;
}

.event-description {
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.service-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  margin-bottom: 0.5rem;
  text-align: left;
}

.service-dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: #cbd5e1;
}

.service-text {
  font-size: 0.7rem;
  font-weight: 800;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.more-indicator {
  font-size: 0.65rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  margin-top: 0.5rem;
}

.event-footer {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f8fafc;
}

.explore-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 900;
  text-transform: uppercase;
  color: #ef4444;
  letter-spacing: 0.1em;
  transition: all 0.3s;
}

.event-card:hover .explore-btn {
  gap: 1rem;
}

/* Empty State */
.empty-state {
  padding: 8rem 2rem;
  text-align: center;
  background: white;
  border-radius: 3.5rem;
  border: 4px solid #f8fafc;
}

.empty-icon {
  width: 6rem;
  height: 6rem;
  background: white;
  border-radius: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #cbd5e1;
  margin: 0 auto 2rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #1e293b;
  margin-bottom: 1rem;
}

.empty-message {
  font-size: 1rem;
  color: #64748b;
  max-width: 25rem;
  margin: 0 auto;
  line-height: 1.6;
}
</style>
