<template>
  <div class="min-h-screen bg-[#f8f9fb]">
    <nav class="bg-white shadow-sm">
      <div class="container mx-auto px-3 md:px-4 py-3 flex items-center justify-between">
        <h1 class="text-2xl font-bold navbar-brand-gradient">Civana</h1>
        <div class="flex items-center gap-3">
          <span class="text-gray-500 text-sm hidden md:inline">{{ user?.email }}</span>
          <button @click="handleLogout" class="px-3 py-1.5 text-sm border border-gray-300 rounded hover:bg-gray-50 transition-colors">Log out</button>
        </div>
      </div>
    </nav>
    
    <main class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-lg shadow-sm">
          <div class="p-6 md:p-8 text-center">
            <h2 class="text-3xl font-bold mb-3">Welcome to Civana</h2>
            <p class="text-xl font-semibold text-gray-900 mb-3">
              {{ user?.first_name }} {{ user?.last_name }}
            </p>
            <span v-if="user?.role" class="role-badge rounded-full px-4 py-2 text-base inline-block mb-4">
              Role: {{ user.role === 'BRAND' ? 'Brand' : 'Creator' }}
            </span>
            
            <hr class="my-6 border-gray-200">
            
            <div class="mt-4">
              <p class="text-gray-500 mb-3">You're successfully logged in!</p>
              <p v-if="!user?.role" class="text-gray-500">
                Please select your role to continue.
                <router-link to="/role-selection" class="text-blue-600 hover:text-blue-800 font-semibold no-underline">
                  Go to role selection →
                </router-link>
              </p>
              <p v-else class="text-gray-500">
                Your dashboard is ready.
                <router-link to="/dashboard" class="text-blue-600 hover:text-blue-800 font-semibold no-underline">
                  Go to dashboard →
                </router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const user = computed(() => authStore.user);

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
