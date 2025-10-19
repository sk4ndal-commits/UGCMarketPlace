<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-gradient-primary p-3">
    <div class="card shadow-lg" style="max-width: 440px; width: 100%;">
      <div class="card-body p-4 p-md-5">
        <h1 class="text-center mb-2 fw-bold">Reset Your Password</h1>
        <p class="text-center text-muted mb-4">Enter your email address and we'll send you a password reset link</p>
        
        <form v-if="!success" @submit.prevent="handleSubmit">
          <!-- Email -->
          <div class="mb-3">
            <label for="email" class="form-label fw-semibold">Email Address</label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="form-control"
              placeholder="jane@brand.com"
              required
              :disabled="loading"
              autocomplete="email"
            />
          </div>
          
          <!-- Error Messages -->
          <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
          </div>
          
          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary w-100 py-2 fw-semibold"
            :disabled="loading"
          >
            <span v-if="loading">Sending...</span>
            <span v-else>Send Reset Link</span>
          </button>
        </form>
        
        <!-- Success Message -->
        <div v-else class="text-center py-3">
          <div class="success-icon mx-auto mb-3"></div>
          <h2 class="h5 fw-bold mb-3">Check Your Email</h2>
          <p class="text-muted mb-2">
            We've sent a password reset link to <strong>{{ email }}</strong>.
            Please check your inbox and follow the instructions to reset your password.
          </p>
          <p class="text-muted small mt-3">
            Didn't receive the email? Check your spam folder or try again in a few minutes.
          </p>
        </div>
        
        <!-- Back to Login Link -->
        <div class="text-center mt-4">
          <router-link to="/login" class="text-decoration-none fw-semibold">← Back to login</router-link>
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
/* Bootstrap classes are used, minimal custom styles needed */
</style>
