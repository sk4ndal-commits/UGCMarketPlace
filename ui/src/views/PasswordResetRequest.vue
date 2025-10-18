<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Reset Your Password</h1>
      <p class="subtitle">Enter your email address and we'll send you a password reset link</p>
      
      <form v-if="!success" @submit.prevent="handleSubmit" class="auth-form">
        <!-- Email -->
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="jane@brand.com"
            required
            :disabled="loading"
            autocomplete="email"
          />
        </div>
        
        <!-- Error Messages -->
        <div v-if="error" class="error-message" role="alert">
          {{ error }}
        </div>
        
        <!-- Submit Button -->
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="loading"
        >
          <span v-if="loading">Sending...</span>
          <span v-else>Send Reset Link</span>
        </button>
      </form>
      
      <!-- Success Message -->
      <div v-else class="success-card">
        <div class="success-icon">✓</div>
        <h2>Check Your Email</h2>
        <p>
          We've sent a password reset link to <strong>{{ email }}</strong>.
          Please check your inbox and follow the instructions to reset your password.
        </p>
        <p class="hint">
          Didn't receive the email? Check your spam folder or try again in a few minutes.
        </p>
      </div>
      
      <!-- Back to Login Link -->
      <div class="auth-footer">
        <router-link to="/login">← Back to login</router-link>
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
  max-width: 440px;
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

input[type="email"] {
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input[type="email"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

input:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
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

.success-card {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
  font-weight: bold;
}

.success-card h2 {
  margin: 0 0 16px 0;
  font-size: 22px;
  font-weight: 700;
  color: #1a202c;
}

.success-card p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}

.success-card .hint {
  font-size: 13px;
  color: #718096;
  margin-top: 16px;
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
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
