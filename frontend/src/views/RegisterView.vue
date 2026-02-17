<template>
  <main class="page page--centered login-page">
    <!-- Decorative Background Elements (Shared with Login) -->
    <div class="login-page__background">
      <div class="login-page__blob login-page__blob--indigo"></div>
      <div class="login-page__blob login-page__blob--emerald"></div>
    </div>

    <div class="card login-card" style="max-width: 500px; width: 100%;">
      <div class="card__body p-0">
        <div class="p-10">
          <header class="text-center mb-10">
            <div
              class="w-16 h-16 bg-primary text-white rounded-2xl flex items-center justify-center text-3xl mx-auto mb-6 shadow-xl shadow-indigo-100">
              <i class="bi bi-person-plus-fill"></i>
            </div>
            <h1 class="text-2xl font-black text-gray-900 mb-2">Establish Digital Identity</h1>
            <p class="text-xs font-black uppercase tracking-[0.2em] text-gray-400">Registry Enrollment Portal</p>
          </header>

          <form class="form space-y-6" @submit.prevent="handleRegister">
            <div class="form__group">
              <label for="username" class="form__label">Authorized Username</label>
              <div class="relative">
                <i class="bi bi-person absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                <input id="username" v-model="form.username" name="username" type="text" autocomplete="username"
                  required class="form__input ps-11" placeholder="Desired registry alias">
              </div>
            </div>

            <div class="form__group">
              <label for="email" class="form__label">Official Email Address</label>
              <div class="relative">
                <i class="bi bi-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                <input id="email" v-model="form.email" name="email" type="email" autocomplete="email" required
                  class="form__input ps-11" placeholder="official@email.go.ke">
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="form__group">
                <label for="password" class="form__label">Cryptographic Password</label>
                <input id="password" v-model="form.password" name="password" type="password" required
                  class="form__input" placeholder="••••••••">
              </div>

              <div class="form__group">
                <label for="confirmPassword" class="form__label">Retype Security Credential</label>
                <input id="confirmPassword" v-model="form.confirmPassword" name="confirmPassword" type="password"
                  required class="form__input" placeholder="••••••••">
              </div>
            </div>

            <div v-if="error" class="alert alert--danger mt-6">
              <i class="bi bi-exclamation-triangle-fill"></i>
              <span class="text-xs font-bold uppercase tracking-tight">{{ error }}</span>
            </div>

            <div class="pt-4">
              <button type="submit"
                class="button button--primary button--pill w-full py-4 text-sm tracking-widest font-black uppercase shadow-xl shadow-indigo-100">
                Initiate Enrollment
              </button>
            </div>
          </form>

          <footer class="mt-10 pt-8 border-t border-gray-100 text-center">
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest">
              Already have an authoritative account?
              <router-link to="/login" class="text-primary font-black ms-2 hover:underline">
                Authenticate Now
              </router-link>
            </p>
          </footer>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '../services/api';

  const router = useRouter();
  const form = ref({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const error = ref('');

  const handleRegister = async () => {
    error.value = '';
    if (form.value.password !== form.value.confirmPassword) {
      error.value = "Passwords do not match.";
      return;
    }

    try {
      await api.post('/users/register/', {
        username: form.value.username,
        email: form.value.email,
        password: form.value.password
      });
      alert("Registration successful! Please login.");
      router.push('/login');
    } catch (e) {
      console.error(e);
      if (e.response && e.response.data && e.response.data.error) {
        error.value = e.response.data.error;
      } else {
        error.value = "Registration failed. Please try again.";
      }
    }
  };
</script>
