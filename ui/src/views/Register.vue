<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Create Your Account</h1>
      <p class="subtitle">Join Civana and start your collaboration journey</p>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <!-- Email -->
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="jane@brand.com"
            required
            :disabled="loading"
          />
        </div>
        
        <!-- First Name -->
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input
            id="firstName"
            v-model="formData.firstName"
            type="text"
            placeholder="Jane"
            required
            :disabled="loading"
          />
        </div>
        
        <!-- Last Name -->
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input
            id="lastName"
            v-model="formData.lastName"
            type="text"
            placeholder="Doe"
            required
            :disabled="loading"
          />
        </div>
        
        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="Enter a strong password"
            required
            :disabled="loading"
          />
          <small class="hint">Minimum 8 characters</small>
        </div>
        
        <!-- Confirm Password -->
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="Re-enter your password"
            required
            :disabled="loading"
          />
        </div>
        
        <!-- GDPR Consent -->
        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input
              v-model="formData.gdprConsent"
              type="checkbox"
              required
              :disabled="loading"
            />
            <span>
              I consent to the processing of my personal data in accordance with 
              <a href="/privacy" target="_blank">GDPR regulations</a>
            </span>
          </label>
        </div>
        
        <!-- Error Messages -->
        <div v-if="error" class="error-message" role="alert">
          {{ error }}
        </div>
        
        <!-- Submit Button -->
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="loading || !formData.gdprConsent"
        >
          <span v-if="loading">Creating account...</span>
          <span v-else>Create Account</span>
        </button>
      </form>
      
      <!-- Login Link -->
      <div class="auth-footer">
        Already have an account?
        <router-link to="/login">Log in</router-link>
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
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 700;
  color: #1a202c;
  text-align: center;
}

.subtitle {
  margin: 0 0 30px 0;
  font-size: 14px;
  color: #718096;
  text-align: center;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
}

input[type="email"],
input[type="text"],
input[type="password"] {
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input[type="email"]:focus,
input[type="text"]:focus,
input[type="password"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

input:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
}

.hint {
  font-size: 12px;
  color: #718096;
}

.checkbox-group {
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: #4a5568;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  margin-top: 2px;
  cursor: pointer;
}

.checkbox-label a {
  color: #667eea;
  text-decoration: underline;
}

.error-message {
  padding: 12px;
  background-color: #fed7d7;
  border: 1px solid #fc8181;
  border-radius: 8px;
  color: #c53030;
  font-size: 14px;
}

.btn {
  padding: 14px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: #718096;
}

.auth-footer a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
