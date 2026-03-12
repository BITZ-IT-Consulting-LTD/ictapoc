<template>
  <div class="action-feed space-y-8">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <div class="feed-badge">
          <i class="bi bi-activity"></i>
        </div>
        <div>
          <h2 class="feed-title">Personalized <span class="text-primary">Action Feed</span></h2>
          <p class="feed-subtitle">Intellectual routing of your government interactions</p>
        </div>
      </div>
      <div v-if="totalCount > 0" class="count-pill">
        {{ totalCount }} ACTIVE
      </div>
    </div>

    <!-- Priority Alerts Section -->
    <div v-if="pendingActions?.length" class="space-y-4">
      <div v-for="alert in pendingActions" :key="alert.id" 
        class="priority-card" :class="alert.type">
        <div class="alert-icon" :class="alert.type">
          <i :class="alert.icon"></i>
        </div>
        <div class="alert-content">
          <div class="alert-meta">
            <span class="alert-time">PRIORITY SIGNAL</span>
          </div>
          <h3 class="alert-title">{{ alert.title }}</h3>
          <p class="alert-message">{{ alert.message }}</p>
        </div>
        <div class="alert-actions">
          <router-link :to="alert.link" class="action-button" :class="alert.type">
            {{ alert.type === 'danger' ? 'Resolve Instantly' : 'Review' }}
            <i class="bi bi-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Ongoing Applications Grid -->
    <div v-if="activeApplications?.length" class="apps-grid">
      <div v-for="app in activeApplications" :key="app.id" class="app-card">
        <div class="app-card__inner">
          <div class="app-header">
            <div class="mda-info">
              <span class="mda-code">{{ app.mda_name }}</span>
              <h3 class="app-name">{{ app.service_name }}</h3>
            </div>
            <div class="step-counter">
              <span class="current">{{ app.current_step_index }}</span>
              <span class="divider">/</span>
              <span class="total">{{ app.total_steps }}</span>
            </div>
          </div>
          
          <div class="app-progress">
            <div class="progress-track">
              <div class="progress-bar" :style="{ width: (app.current_step_index / app.total_steps) * 100 + '%' }">
                <div class="progress-glow"></div>
              </div>
            </div>
            <div class="progress-meta">
              <span class="stage-label">Current Pipeline Node</span>
              <span class="stage-name">{{ app.current_step_name }}</span>
            </div>
          </div>
          
          <div class="app-footer">
            <router-link :to="`/service-request/${app.id}`" class="roadmap-link">
              <span>View Application Roadmap</span>
              <i class="bi bi-map-fill"></i>
            </router-link>
          </div>
        </div>
        
        <!-- Decorative subtle gradient background -->
        <div class="app-card__bg"></div>
      </div>
    </div>

    <!-- Clear State -->
    <div v-if="!pendingActions?.length && !activeApplications?.length" class="clear-state">
      <div class="clear-illustration">
        <i class="bi bi-stars"></i>
        <div class="orbit"></div>
      </div>
      <h3 class="clear-title">System Equilibrium Reached</h3>
      <p class="clear-message">All your authoritative applications are processed. No pending citizen actions detected.</p>
      <button @click="$emit('explore')" class="explore-button">
        Explore New Services
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  pendingActions: {
    type: Array,
    default: () => []
  },
  activeApplications: {
    type: Array,
    default: () => []
  }
});

defineEmits(['explore']);

const totalCount = computed(() => (props.pendingActions?.length || 0) + (props.activeApplications?.length || 0));
</script>

<style scoped>
.action-feed {
  width: 100%;
}

.feed-badge {
  width: 3.5rem;
  height: 3.5rem;
  background: white;
  border-radius: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #4f46e5;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef2ff;
}

.feed-title {
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: -0.025em;
  margin: 0;
  color: #1e293b;
}

.feed-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0.25rem 0 0;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.count-pill {
  background: #4f46e5;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 900;
  letter-spacing: 0.1em;
}

/* Priority Card */
.priority-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.25rem;
  background: white;
  border-radius: 1.5rem;
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.priority-card:hover {
  transform: translateX(4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.priority-card.danger { border-left: 6px solid #ef4444; }
.priority-card.success { border-left: 6px solid #10b981; }

.alert-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.alert-icon.danger { background: #fef2f2; color: #ef4444; }
.alert-icon.success { background: #ecfdf5; color: #10b981; }

.alert-content {
  flex: 1;
}

.alert-meta {
  font-size: 0.6rem;
  font-weight: 900;
  letter-spacing: 0.15em;
  color: #94a3b8;
  margin-bottom: 0.25rem;
}

.alert-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}

.alert-message {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.125rem;
}

.action-button {
  padding: 0.625rem 1.25rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.action-button.danger { background: #ef4444; color: white; }
.action-button.success { background: #10b981; color: white; }

.action-button:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

/* Apps Grid */
.apps-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
}

.app-card {
  position: relative;
  border-radius: 2rem;
  background: white;
  border: 1px solid #f1f5f9;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.app-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  border-color: #4f46e555;
}

.app-card__inner {
  position: relative;
  padding: 2rem;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.mda-code {
  font-size: 0.6rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #94a3b8;
  display: block;
  margin-bottom: 0.25rem;
}

.app-name {
  font-size: 1.125rem;
  font-weight: 900;
  color: #1e293b;
  margin: 0;
  line-height: 1.2;
}

.step-counter {
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 900;
  font-size: 0.75rem;
}

.step-counter .current { color: #4f46e5; }
.step-counter .divider { color: #cbd5e1; }
.step-counter .total { color: #94a3b8; }

.app-progress {
  margin-bottom: 2rem;
}

.progress-track {
  height: 0.75rem;
  background: #f1f5f9;
  border-radius: 9999px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4f46e5 0%, #818cf8 100%);
  border-radius: 9999px;
  position: relative;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
  animation: sweep 2s infinite;
}

@keyframes sweep {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}

.progress-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stage-label {
  font-size: 0.6rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #94a3b8;
}

.stage-name {
  font-size: 0.75rem;
  font-weight: 900;
  color: #4f46e5;
  text-transform: uppercase;
}

.roadmap-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 1rem;
  background: #f1f5f9;
  border-radius: 1.25rem;
  font-size: 0.875rem;
  font-weight: 800;
  color: #475569;
  transition: all 0.2s;
}

.roadmap-link:hover {
  background: #4f46e5;
  color: white;
}

.app-card__bg {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.05) 0%, transparent 70%);
  z-index: 1;
}

/* Clear State */
.clear-state {
  padding: 5rem 2rem;
  text-align: center;
  background: white;
  border-radius: 3rem;
  border: 2px dashed #f1f5f9;
}

.clear-illustration {
  position: relative;
  width: 6rem;
  height: 6rem;
  background: #f0f9ff;
  border-radius: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #0ea5e9;
  margin: 0 auto 2rem;
}

.orbit {
  position: absolute;
  width: 8rem;
  height: 8rem;
  border: 1px dashed #bae6fd;
  border-radius: 50%;
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.clear-title {
  font-size: 1.25rem;
  font-weight: 900;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.clear-message {
  font-size: 0.9rem;
  color: #64748b;
  max-width: 20rem;
  margin: 0 auto 2.5rem;
  line-height: 1.6;
}

.explore-button {
  padding: 0.875rem 2.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 9999px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
}

.explore-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
}
</style>
