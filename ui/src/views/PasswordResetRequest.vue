<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-primary p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
      <div class="p-6 md:p-8">
        <h1 class="text-center text-2xl font-bold mb-2">Reset Your Password</h1>
        <p class="text-center text-gray-500 mb-6">Enter your email address and we'll send you a password reset link</p>
        
        <form v-if="!success" @submit.prevent="handleSubmit">
          <!-- Email -->
          <div class="mb-4">
            <label for="email" class="block text-sm font-semibold text-gray-700 mb-1">Email Address</label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="jane@brand.com"
              required
              :disabled="loading"
              autocomplete="email"
            />
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
            <span v-if="loading">Sending...</span>
            <span v-else>Send Reset Link</span>
          </button>
        </form>
        
        <!-- Success Message -->
        <div v-else class="text-center py-4">
          <div class="text-6xl mb-4">✅</div>
          <h2 class="text-xl font-bold mb-3">Check Your Email</h2>
          <p class="text-gray-600 mb-2">
            We've sent a password reset link to <strong>{{ email }}</strong>.
            Please check your inbox and follow the instructions to reset your password.
          </p>
          <p class="text-gray-500 text-sm mt-4">
            Didn't receive the email? Check your spam folder or try again in a few minutes.
          </p>
        </div>
        
        <!-- Back to Login Link -->
        <div class="text-center mt-6">
          <router-link to="/login" class="text-blue-600 hover:text-blue-800 font-semibold no-underline">← Back to login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();

const email = ref('');
const success = ref(false);

const loading = computed(() => authStore.loading);
const error = computed(() => authStore.error);

const handleSubmit = async () => {
  const result = await authStore.requestPasswordReset(email.value);
  if (result) {
    success.value = true;
  }
};
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
