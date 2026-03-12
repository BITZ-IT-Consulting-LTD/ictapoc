<template>
  <div class="premium-card" :class="[variantClass, { 'is-hoverable': hoverable, 'is-glass': glass }]">
    <div v-if="$slots.header || title" class="premium-card__header">
      <slot name="header">
        <div class="flex items-center gap-3">
          <div v-if="icon" class="premium-card__icon-wrapper" :class="iconVariantClass">
            <i :class="icon"></i>
          </div>
          <div>
            <h3 class="premium-card__title">{{ title }}</h3>
            <p v-if="subtitle" class="premium-card__subtitle">{{ subtitle }}</p>
          </div>
        </div>
      </slot>
      <div v-if="$slots.actions" class="premium-card__actions">
        <slot name="actions" />
      </div>
    </div>
    
    <div class="premium-card__body" :class="bodyClass">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="premium-card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  title: String,
  subtitle: String,
  icon: String,
  variant: {
    type: String,
    default: 'default' // default, primary, danger, success, warning, info
  },
  hoverable: Boolean,
  glass: {
    type: Boolean,
    default: true
  },
  bodyClass: String
});

const variantClass = computed(() => `premium-card--${props.variant}`);
const iconVariantClass = computed(() => `icon-wrapper--${props.variant}`);
</script>

<style scoped>
.premium-card {
  --pc-radius: 1.5rem;
  --pc-padding: 1.5rem;
  --pc-bg: #ffffff;
  --pc-border: #e2e8f0;
  --pc-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  
  background: var(--pc-bg);
  border: 1px solid var(--pc-border);
  border-radius: var(--pc-radius);
  box-shadow: var(--pc-shadow);
  overflow: hidden;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.premium-card.is-glass {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.4);
}

.premium-card.is-hoverable:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  border-color: rgba(var(--primary-rgb, 99, 102, 241), 0.3);
}

.premium-card__header {
  padding: var(--pc-padding);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.premium-card__body {
  padding: var(--pc-padding);
}

.premium-card__footer {
  padding: var(--pc-padding);
  background: rgba(0, 0, 0, 0.02);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.premium-card__title {
  font-size: 1.125rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.025em;
}

.premium-card__subtitle {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  margin: 0.25rem 0 0;
}

.premium-card__icon-wrapper {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

/* Variants */
.icon-wrapper--default { background: #f1f5f9; color: #475569; }
.icon-wrapper--primary { background: #eef2ff; color: #4f46e5; }
.icon-wrapper--success { background: #ecfdf5; color: #10b981; }
.icon-wrapper--danger  { background: #fef2f2; color: #ef4444; }
.icon-wrapper--warning { background: #fffbeb; color: #f59e0b; }
.icon-wrapper--info    { background: #f0f9ff; color: #0ea5e9; }

.premium-card--primary { border-left: 4px solid #4f46e5; }
.premium-card--success { border-left: 4px solid #10b981; }
.premium-card--danger  { border-left: 4px solid #ef4444; }
.premium-card--warning { border-left: 4px solid #f59e0b; }
.premium-card--info    { border-left: 4px solid #0ea5e9; }
</style>
