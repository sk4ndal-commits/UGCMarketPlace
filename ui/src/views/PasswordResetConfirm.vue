<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Set New Password</h1>
      <p class="subtitle">Enter your new password below</p>
      
      <form v-if="!success" @submit.prevent="handleSubmit" class="auth-form">
        <!-- New Password -->
        <div class="form-group">
          <label for="password">New Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="Enter a strong password"
            required
            :disabled="loading"
            autocomplete="new-password"
          />
          <small class="hint">Minimum 8 characters</small>
        </div>
        
        <!-- Confirm Password -->
        <div class="form-group">
          <label for="confirmPassword">Confirm New Password</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="Re-enter your password"
            required
            :disabled="loading"
            autocomplete="new-password"
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
          <span v-if="loading">Resetting...</span>
          <span v-else>Reset Password</span>
        </button>
      </form>
      
      <!-- Success Message -->
      <div v-else class="success-card">
        <div class="success-icon">✓</div>
        <h2>Password Reset Successful</h2>
        <p>
          Your password has been successfully reset. You can now log in with your new password.
        </p>
        <router-link to="/login" class="btn btn-primary">Go to Login</router-link>
      </div>
      
      <!-- Back to Login Link -->
      <div v-if="!success" class="auth-footer">
        <router-link to="/login">← Back to login</router-link>
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

input[type="password"] {
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

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
  text-decoration: none;
  display: inline-block;
  text-align: center;
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
  margin: 0 0 24px 0;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
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
