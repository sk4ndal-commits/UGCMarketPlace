<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-primary p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
      <div class="p-6 md:p-8">
        <h1 class="text-center text-2xl font-bold mb-2">Set New Password</h1>
        <p class="text-center text-gray-500 mb-6">Enter your new password below</p>
        
        <form v-if="!success" @submit.prevent="handleSubmit">
          <!-- New Password -->
          <div class="mb-4">
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-1">New Password</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter a strong password"
              required
              :disabled="loading"
              autocomplete="new-password"
            />
            <small class="text-gray-500 text-sm">Minimum 8 characters</small>
          </div>
          
          <!-- Confirm Password -->
          <div class="mb-4">
            <label for="confirmPassword" class="block text-sm font-semibold text-gray-700 mb-1">Confirm New Password</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Re-enter your password"
              required
              :disabled="loading"
              autocomplete="new-password"
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
            <span v-if="loading">Resetting...</span>
            <span v-else>Reset Password</span>
          </button>
        </form>
        
        <!-- Success Message -->
        <div v-else class="text-center py-4">
          <div class="text-6xl mb-4">✅</div>
          <h2 class="text-xl font-bold mb-3">Password Reset Successful</h2>
          <p class="text-gray-600 mb-6">
            Your password has been successfully reset. You can now log in with your new password.
          </p>
          <router-link to="/login" class="block w-full bg-gradient-primary text-white font-semibold py-2 rounded-lg hover:opacity-90 transition-opacity text-center no-underline">
            Go to Login
          </router-link>
        </div>
        
        <!-- Back to Login Link -->
        <div v-if="!success" class="text-center mt-6">
          <router-link to="/login" class="text-blue-600 hover:text-blue-800 font-semibold no-underline">← Back to login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const route = useRoute();
const authStore = useAuthStore();

const formData = ref({
  password: '',
  confirmPassword: '',
});

const success = ref(false);

const loading = computed(() => authStore.loading);
const error = computed(() => authStore.error);

const handleSubmit = async () => {
  // Validation
  if (formData.value.password !== formData.value.confirmPassword) {
    authStore.error = 'Passwords do not match';
    return;
  }
  
  if (formData.value.password.length < 8) {
    authStore.error = 'Password must be at least 8 characters long';
    return;
  }
  
  // Get uid and token from route params
  const uid = route.params.uid as string;
  const token = route.params.token as string;
  
  if (!uid || !token) {
    authStore.error = 'Invalid password reset link';
    return;
  }
  
  // Reset password
  const result = await authStore.confirmPasswordReset(
    uid,
    token,
    formData.value.password
  );
  
  if (result) {
    success.value = true;
  }
};
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
