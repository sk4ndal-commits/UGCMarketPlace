<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-gradient-primary p-3">
    <div class="card shadow-lg" style="max-width: 440px; width: 100%;">
      <div class="card-body p-4 p-md-5">
        <h1 class="text-center mb-2 fw-bold">Welcome Back</h1>
        <p class="text-center text-muted mb-4">Log in to continue your collaboration journey</p>
        
        <form @submit.prevent="handleLogin">
          <!-- Email -->
          <div class="mb-3">
            <label for="email" class="form-label fw-semibold">Email Address</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="form-control"
              placeholder="jane@brand.com"
              required
              :disabled="loading"
              autocomplete="email"
            />
          </div>
          
          <!-- Password -->
          <div class="mb-3">
            <label for="password" class="form-label fw-semibold">Password</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="form-control"
              placeholder="Enter your password"
              required
              :disabled="loading"
              autocomplete="current-password"
            />
          </div>
          
          <!-- Forgot Password Link -->
          <div class="text-end mb-3">
            <router-link to="/password-reset" class="text-decoration-none small">Forgot password?</router-link>
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
            <span v-if="loading">Logging in...</span>
            <span v-else>Log In</span>
          </button>
        </form>
        
        <!-- Register Link -->
        <div class="text-center mt-4 text-muted">
          Don't have an account?
          <router-link to="/register" class="text-decoration-none fw-semibold">Create account</router-link>
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
/* Bootstrap classes are used, minimal custom styles needed */
</style>
