<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-gradient-primary p-3">
    <div class="card shadow-lg" style="max-width: 440px; width: 100%;">
      <div class="card-body p-4 p-md-5">
        <h1 class="text-center mb-2 fw-bold">Set New Password</h1>
        <p class="text-center text-muted mb-4">Enter your new password below</p>
        
        <form v-if="!success" @submit.prevent="handleSubmit">
          <!-- New Password -->
          <div class="mb-3">
            <label for="password" class="form-label fw-semibold">New Password</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="form-control"
              placeholder="Enter a strong password"
              required
              :disabled="loading"
              autocomplete="new-password"
            />
            <small class="form-text text-muted">Minimum 8 characters</small>
          </div>
          
          <!-- Confirm Password -->
          <div class="mb-3">
            <label for="confirmPassword" class="form-label fw-semibold">Confirm New Password</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              class="form-control"
              placeholder="Re-enter your password"
              required
              :disabled="loading"
              autocomplete="new-password"
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
            <span v-if="loading">Resetting...</span>
            <span v-else>Reset Password</span>
          </button>
        </form>
        
        <!-- Success Message -->
        <div v-else class="text-center py-3">
          <div class="success-icon mx-auto mb-3"></div>
          <h2 class="h5 fw-bold mb-3">Password Reset Successful</h2>
          <p class="text-muted mb-4">
            Your password has been successfully reset. You can now log in with your new password.
          </p>
          <router-link to="/login" class="btn btn-primary w-100 py-2 fw-semibold text-decoration-none">
            Go to Login
          </router-link>
        </div>
        
        <!-- Back to Login Link -->
        <div v-if="!success" class="text-center mt-4">
          <router-link to="/login" class="text-decoration-none fw-semibold">← Back to login</router-link>
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
/* Bootstrap classes are used, minimal custom styles needed */
</style>
