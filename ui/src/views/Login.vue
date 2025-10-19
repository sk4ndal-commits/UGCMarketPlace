<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-primary p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
      <div class="p-6 md:p-8">
        <h1 class="text-center text-2xl font-bold mb-2">Welcome Back</h1>
        <p class="text-center text-gray-500 mb-6">Log in to continue your collaboration journey</p>
        
        <form @submit.prevent="handleLogin">
          <!-- Email -->
          <div class="mb-4">
            <label for="email" class="block text-sm font-semibold text-gray-700 mb-1">Email Address</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="jane@brand.com"
              required
              :disabled="loading"
              autocomplete="email"
            />
          </div>
          
          <!-- Password -->
          <div class="mb-4">
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-1">Password</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your password"
              required
              :disabled="loading"
              autocomplete="current-password"
            />
          </div>
          
          <!-- Forgot Password Link -->
          <div class="text-right mb-4">
            <router-link to="/password-reset" class="text-sm text-blue-600 hover:text-blue-800">Forgot password?</router-link>
          </div>
          
          <!-- Error Messages -->
          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {{ error }}
          </div>
          
          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full bg-gradient-primary text-white font-semibold py-2 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
            :disabled="loading"
          >
            <span v-if="loading">Logging in...</span>
            <span v-else>Log In</span>
          </button>
        </form>
        
        <!-- Register Link -->
        <div class="text-center mt-6 text-gray-500">
          Don't have an account?
          <router-link to="/register" class="text-blue-600 hover:text-blue-800 font-semibold">Create account</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const formData = ref({
  email: '',
  password: '',
});

const loading = computed(() => authStore.loading);
const error = computed(() => authStore.error);

const handleLogin = async () => {
  const success = await authStore.login({
    email: formData.value.email,
    password: formData.value.password
  });
  
  if (success) {
    // Redirect based on whether user has a role
    if (authStore.hasRole) {
      router.push('/dashboard');
    } else {
      router.push('/role-selection');
    }
  }
};
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
