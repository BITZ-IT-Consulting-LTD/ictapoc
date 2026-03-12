<template>
  <div class="authoritative-wallet overflow-hidden relative">
    <div class="wallet-background">
      <div class="abstract-shape shape-1"></div>
      <div class="abstract-shape shape-2"></div>
      <i class="bi bi-wallet2 decorative-icon"></i>
    </div>
    
    <div class="wallet-content flex flex-col md:flex-row items-center justify-between gap-10">
      <div class="flex-1 text-center md:text-left z-10">
        <div class="status-badge">
          <i class="bi bi-shield-check"></i>
          <span>Identity Verified & Cryptographically Locked</span>
        </div>
        
        <h2 class="wallet-title">
          Authoritative <span class="text-highlight">Wallet</span>
        </h2>
        
        <p class="wallet-description">
          Secure cloud access to your <strong>{{ documents?.length || 0 }}</strong> official government credentials.
          All documents are cryptographically signed by the National Registry.
        </p>
        
        <div class="wallet-actions flex flex-wrap gap-4 justify-center md:justify-start">
          <router-link to="/profile" class="wallet-button primary">
            <i class="bi bi-wallet2"></i> Open Secure Vault
          </router-link>
          <button class="wallet-button secondary">
             <i class="bi bi-qr-code-scan"></i> Show ID QR
          </button>
        </div>
      </div>
      
      <!-- Visual Card Stack -->
      <div class="card-stack hidden lg:block perspective" aria-hidden="true">
        <div v-for="(doc, i) in displayedDocuments" :key="i"
          class="stack-card"
          :style="{
            transform: `translateY(${i * 16}px) scale(${1 - (i * 0.08)})`,
            zIndex: 10 - i,
            opacity: 1 - (i * 0.15)
          }">
          <div class="card-header">
            <div class="card-icon" :class="doc.type">
              <i :class="getDocIcon(doc.type)"></i>
            </div>
            <div class="card-titles">
              <div class="line-bold"></div>
              <div class="line-slim"></div>
            </div>
            <div class="chip"></div>
          </div>
          <div class="card-body">
            <div class="line-ghost"></div>
            <div class="line-ghost short"></div>
          </div>
          <div class="card-footer">
             <div class="text-[8px] font-black opacity-30 tracking-widest uppercase">Government of Kenya</div>
          </div>
        </div>
        
        <!-- Empty state / Placeholder card if no documents -->
        <div v-if="!documents?.length" class="stack-card empty">
           <div class="flex flex-col items-center justify-center h-full text-slate-300 gap-3">
              <i class="bi bi-plus-circle text-4xl"></i>
              <span class="text-[10px] font-black uppercase tracking-widest">No Documents Issued</span>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  documents: {
    type: Array,
    default: () => []
  }
});

const displayedDocuments = computed(() => {
  if (!props.documents || props.documents.length === 0) return [];
  return props.documents.slice(0, 3);
});

const getDocIcon = (type) => {
  if (type === 'AUTHORITATIVE_OUTPUT') return 'bi-patch-check-fill';
  if (type === 'INDENTITY_CARD') return 'bi-person-badge-fill';
  return 'bi-file-earmark-text-fill';
};
</script>

<style scoped>
.authoritative-wallet {
  background: var(--grad-premium, linear-gradient(135deg, #0f172a 0%, #1e293b 100%));
  color: white;
  border-radius: 2rem;
  min-height: 280px;
  padding: 3rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.wallet-background {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
}

.abstract-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: rgba(99, 102, 241, 0.15);
  top: -100px;
  right: -50px;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: rgba(239, 68, 68, 0.1);
  bottom: -50px;
  left: 50px;
}

.decorative-icon {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 18rem;
  color: white;
  opacity: 0.05;
  transform: translate(20%, -20%);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 2rem;
}

.status-badge i {
  color: #10b981;
}

.wallet-title {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: -0.05em;
  line-height: 1;
  margin-bottom: 1rem;
}

.text-highlight {
  color: #ef4444; /* ICTA Red */
}

.wallet-description {
  color: #94a3b8;
  font-size: 1rem;
  line-height: 1.6;
  max-width: 500px;
  margin-bottom: 2.5rem;
}

.wallet-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 2rem;
  border-radius: 9999px;
  font-weight: 800;
  font-size: 0.875rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  border: none;
}

.wallet-button.primary {
  background: #ef4444;
  color: white;
}

.wallet-button.primary:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(239, 68, 68, 0.3);
}

.wallet-button.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.wallet-button.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* Card Stack */
.card-stack {
  position: relative;
  width: 320px;
  height: 200px;
}

.stack-card {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 1.25rem;
  padding: 1.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(226, 232, 240, 0.8);
  display: flex;
  flex-col: column;
  transition: all 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.stack-card.empty {
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1rem;
}

.card-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  background: #f8fafc;
  color: #475569;
}

.card-icon.AUTHORITATIVE_OUTPUT {
  background: #ecfdf5;
  color: #10b981;
}

.card-titles {
  flex: 1;
}

.line-bold {
  height: 0.75rem;
  background: #1e293b;
  border-radius: 0.25rem;
  width: 70%;
  margin-bottom: 0.5rem;
}

.line-slim {
  height: 0.5rem;
  background: #e2e8f0;
  border-radius: 0.2rem;
  width: 40%;
}

.chip {
  width: 2.5rem;
  height: 1.75rem;
  background: #fbbf24;
  border-radius: 0.375rem;
  opacity: 0.8;
  position: relative;
}

.chip::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: 60%;
  border: 1px solid rgba(0,0,0,0.1);
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.line-ghost {
  height: 0.5rem;
  background: #f1f5f9;
  border-radius: 9999px;
  width: 100%;
}

.line-ghost.short {
  width: 60%;
}

.card-footer {
  margin-top: auto;
  text-align: right;
}
</style>
