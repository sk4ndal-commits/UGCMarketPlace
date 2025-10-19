<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-primary p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-lg">
      <div class="p-6 md:p-8">
        <h1 class="text-center text-2xl font-bold mb-2">Create Your Account</h1>
        <p class="text-center text-gray-500 mb-6">Join Civana and start your collaboration journey</p>
        
        <form @submit.prevent="handleRegister">
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
            />
          </div>
          
          <!-- First Name -->
          <div class="mb-4">
            <label for="firstName" class="block text-sm font-semibold text-gray-700 mb-1">First Name</label>
            <input
              id="firstName"
              v-model="formData.firstName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Jane"
              required
              :disabled="loading"
            />
          </div>
          
          <!-- Last Name -->
          <div class="mb-4">
            <label for="lastName" class="block text-sm font-semibold text-gray-700 mb-1">Last Name</label>
            <input
              id="lastName"
              v-model="formData.lastName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Doe"
              required
              :disabled="loading"
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
              placeholder="Enter a strong password"
              required
              :disabled="loading"
            />
            <p class="mt-1 text-sm text-gray-500">Minimum 8 characters</p>
          </div>
          
          <!-- Confirm Password -->
          <div class="mb-4">
            <label for="confirmPassword" class="block text-sm font-semibold text-gray-700 mb-1">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Re-enter your password"
              required
              :disabled="loading"
            />
          </div>
          
          <!-- GDPR Consent -->
          <div class="mb-4 flex items-start">
            <input
              v-model="formData.gdprConsent"
              type="checkbox"
              class="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              id="gdprConsent"
              required
              :disabled="loading"
            />
            <label class="ml-2 text-sm text-gray-700" for="gdprConsent">
              I consent to the processing of my personal data in accordance with 
              <a href="/privacy" target="_blank" class="text-blue-600 hover:text-blue-800">GDPR regulations</a>
            </label>
          </div>
          
          <!-- Error Messages -->
          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {{ error }}
          </div>
          
          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full bg-gradient-primary text-white font-semibold py-2 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
            :disabled="loading || !formData.gdprConsent"
          >
            <span v-if="loading">Creating account...</span>
            <span v-else>Create Account</span>
          </button>
        </form>
        
        <!-- Login Link -->
        <div class="text-center mt-6 text-gray-500">
          Already have an account?
          <router-link to="/login" class="text-blue-600 hover:text-blue-800 font-semibold">Log in</router-link>
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
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: '',
  gdprConsent: false,
});

const loading = computed(() => authStore.loading);
const error = computed(() => authStore.error);

const handleRegister = async () => {
  // Validation
  if (formData.value.password !== formData.value.confirmPassword) {
    authStore.error = 'Passwords do not match';
    return;
  }
  
  if (formData.value.password.length < 8) {
    authStore.error = 'Password must be at least 8 characters long';
    return;
  }
  
  if (!formData.value.gdprConsent) {
    authStore.error = 'You must consent to GDPR data processing';
    return;
  }
  
  // Register
  const success = await authStore.register({
    email: formData.value.email,
    first_name: formData.value.firstName,
    last_name: formData.value.lastName,
    password: formData.value.password,
    password_confirm: formData.value.confirmPassword,
    gdpr_consent: formData.value.gdprConsent,
  });
  
  if (success) {
    // Redirect to role selection
    router.push('/role-selection');
  }
};
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
