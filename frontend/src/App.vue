<template>
  <div class="layout">
    <header class="layout__header">
      <nav class="layout__container navbar">
        <div class="navbar__brand-wrapper">
          <router-link to="/" class="navbar__brand">
            <span>ICT</span> AUTHORITY
          </router-link>
        </div>
        <div class="navbar__menu">
          <router-link to="/public-repository" class="navbar__link" active-class="navbar__link--active">
            <i class="bi bi-bank2"></i> Repository
          </router-link>
          <router-link to="/login" class="navbar__link" active-class="navbar__link--active">
            <i class="bi bi-shield-lock-fill"></i> Portal Access
          </router-link>
          <router-link to="/dashboard" class="navbar__link navbar__link--button">
            Dashboard <i class="bi bi-arrow-right-short ms-1"></i>
          </router-link>
          
          <button @click="toggleTheme" class="theme-toggle" :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
            <i :class="isDark ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill'"></i>
          </button>
        </div>
      </nav>
    </header>

    <main class="layout__main">
      <div :class="{ 'layout__container': !isDashboard }">
        <router-view />
      </div>
    </main>

    <footer class="layout__footer">
      <div class="layout__container">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-16 pb-16">
          <section class="footer-block">
            <h2 class="text-primary font-black text-xl mb-6 uppercase tracking-tighter">ICT AUTHORITY</h2>
            <p class="text-sm text-white/50 leading-relaxed font-medium">
              The Authority for information and communications technology, fostering an ICT-enabled society through
              digital excellence and authoritative governance.
            </p>
          </section>

          <nav class="footer-block">
            <h3 class="font-black text-xs uppercase tracking-[0.2em] mb-8 text-white">Official Gateway</h3>
            <ul class="space-y-4 list-none p-0">
              <li><a href="#" class="text-sm text-white/40 hover:text-primary transition-colors font-bold">National
                  eCitizen Portal</a></li>
              <li><a href="#" class="text-sm text-white/40 hover:text-primary transition-colors font-bold">Public
                  Service Commission</a></li>
              <li><a href="#" class="text-sm text-white/40 hover:text-primary transition-colors font-bold">Ministry of
                  ICT & Digital Economy</a></li>
            </ul>
          </nav>

          <section class="footer-block">
            <h3 class="font-black text-xs uppercase tracking-[0.2em] mb-8 text-white">National Headquarters</h3>
            <p class="text-sm text-white/40 font-bold leading-relaxed mb-4">
              Telposta Towers, 12th Floor<br>
              Kenyatta Avenue, Nairobi<br>
              Republic of Kenya
            </p>
            <div class="flex gap-4">
              <i class="bi bi-facebook text-white/20 hover:text-white cursor-pointer transition-colors"></i>
              <i class="bi bi-twitter-x text-white/20 hover:text-white cursor-pointer transition-colors"></i>
              <i class="bi bi-linkedin text-white/20 hover:text-white cursor-pointer transition-colors"></i>
            </div>
          </section>
        </div>

        <div class="pt-8 border-t border-white/5 flex flex-col md:row items-center justify-between gap-4">
          <p class="text-[10px] font-black uppercase tracking-[0.5em] text-white/20">
            &copy; 2026 ICT Authority. National GOK Enterprise Platform.
          </p>
          <div class="flex gap-6">
            <span class="text-[10px] font-black uppercase text-white/10 tracking-widest">Digital Trust</span>
            <span class="text-[10px] font-black uppercase text-white/10 tracking-widest">ISO 27001</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
  .theme-toggle {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-hover);
    color: var(--icta-dark);
    transition: all 0.2s ease;
    border: 1px solid var(--icta-border);
  }

  .theme-toggle:hover {
    transform: rotate(15deg) scale(1.1);
    background: var(--primary-soft);
    color: var(--primary);
  }

  .dark .theme-toggle {
    background: #1e293b;
    border-color: #334155;
    color: #fbbf24;
  }
</style>

<script setup>
  import { computed, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { useTheme } from './composables/useTheme';

  const route = useRoute();
  const isDashboard = computed(() => route.path === '/dashboard');
  
  const { isDark, toggleTheme, initTheme } = useTheme();
  
  onMounted(() => {
    initTheme();
  });
</script>
