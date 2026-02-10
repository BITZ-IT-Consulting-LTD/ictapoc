<template>
  <div id="app" class="bg-gray-100 min-h-screen">
    <header class="bg-white shadow">
      <nav class="container mx-auto px-6 py-3">
        <div class="flex justify-between items-center">
          <router-link to="/" class="text-xl font-semibold text-gray-700">GovServices</router-link>
          <div>
            <router-link to="/login" class="px-3 py-2 rounded text-gray-700 hover:bg-gray-200">Login</router-link>
            <router-link to="/dashboard" class="px-3 py-2 rounded text-gray-700 hover:bg-gray-200">Dashboard</router-link>
          </div>
        </div>
      </nav>
    </header>
    <main class="container mx-auto px-6 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>
