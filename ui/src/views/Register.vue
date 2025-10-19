<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-gradient-primary p-3">
    <div class="card shadow-lg" style="max-width: 480px; width: 100%;">
      <div class="card-body p-4 p-md-5">
        <h1 class="text-center mb-2 fw-bold">Create Your Account</h1>
        <p class="text-center text-muted mb-4">Join Civana and start your collaboration journey</p>
        
        <form @submit.prevent="handleRegister">
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
            />
          </div>
          
          <!-- First Name -->
          <div class="mb-3">
            <label for="firstName" class="form-label fw-semibold">First Name</label>
            <input
              id="firstName"
              v-model="formData.firstName"
              type="text"
              class="form-control"
              placeholder="Jane"
              required
              :disabled="loading"
            />
          </div>
          
          <!-- Last Name -->
          <div class="mb-3">
            <label for="lastName" class="form-label fw-semibold">Last Name</label>
            <input
              id="lastName"
              v-model="formData.lastName"
              type="text"
              class="form-control"
              placeholder="Doe"
              required
              :disabled="loading"
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
              placeholder="Enter a strong password"
              required
              :disabled="loading"
            />
            <small class="form-text text-muted">Minimum 8 characters</small>
          </div>
          
          <!-- Confirm Password -->
          <div class="mb-3">
            <label for="confirmPassword" class="form-label fw-semibold">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              class="form-control"
              placeholder="Re-enter your password"
              required
              :disabled="loading"
            />
          </div>
          
          <!-- GDPR Consent -->
          <div class="mb-3 form-check">
            <input
              v-model="formData.gdprConsent"
              type="checkbox"
              class="form-check-input"
              id="gdprConsent"
              required
              :disabled="loading"
            />
            <label class="form-check-label" for="gdprConsent">
              I consent to the processing of my personal data in accordance with 
              <a href="/privacy" target="_blank">GDPR regulations</a>
            </label>
          </div>
          
          <!-- Error Messages -->
          <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
          </div>
          
          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary w-100 py-2 fw-semibold"
            :disabled="loading || !formData.gdprConsent"
          >
            <span v-if="loading">Creating account...</span>
            <span v-else>Create Account</span>
          </button>
        </form>
        
        <!-- Login Link -->
        <div class="text-center mt-4 text-muted">
          Already have an account?
          <router-link to="/login" class="text-decoration-none fw-semibold">Log in</router-link>
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
/* Bootstrap classes are used, minimal custom styles needed */
</style>
