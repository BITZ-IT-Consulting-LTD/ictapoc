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
          Access Registry
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
  </main>
</template>
