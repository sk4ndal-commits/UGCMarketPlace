<template>
  <div class="role-container">
    <div class="role-card">
      <h1>Choose Your Role</h1>
      <p class="subtitle">Select how you'd like to use Civana</p>
      
      <!-- Error Messages -->
      <div v-if="error" class="error-message" role="alert">
        {{ error }}
      </div>
      
      <div class="role-options">
        <!-- Brand Option -->
        <div
          class="role-option"
          :class="{ selected: selectedRole === 'BRAND' }"
          @click="selectRole('BRAND')"
        >
          <div class="role-icon">🏢</div>
          <h2>Brand</h2>
          <p>
            Create UGC campaigns, collaborate with creators, and get authentic content for your brand.
          </p>
          <ul class="role-features">
            <li>Post campaign briefs</li>
            <li>Review creator applications</li>
            <li>Manage collaborations</li>
            <li>Receive quality content</li>
          </ul>
        </div>
        
        <!-- Influencer Option -->
        <div
          class="role-option"
          :class="{ selected: selectedRole === 'INFLUENCER' }"
          @click="selectRole('INFLUENCER')"
        >
          <div class="role-icon">✨</div>
          <h2>Creator</h2>
          <p>
            Browse campaigns, apply with proposals, and get paid for creating authentic content.
          </p>
          <ul class="role-features">
            <li>Browse available campaigns</li>
            <li>Submit applications</li>
            <li>Collaborate with brands</li>
            <li>Get paid for your work</li>
          </ul>
        </div>
      </div>
      
      <!-- Confirm Button -->
      <button
        class="btn btn-primary"
        :disabled="!selectedRole || loading"
        @click="handleConfirm"
      >
        <span v-if="loading">Confirming...</span>
        <span v-else>Continue as {{ selectedRole === 'BRAND' ? 'Brand' : 'Creator' }}</span>
      </button>
      
      <!-- Logout Link -->
      <div class="role-footer">
        <button @click="handleLogout" class="logout-link">Log out</button>
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

const selectedRole = ref<'BRAND' | 'INFLUENCER' | null>(null);

const loading = computed(() => authStore.loading);
const error = computed(() => authStore.error);

const selectRole = (role: 'BRAND' | 'INFLUENCER') => {
  selectedRole.value = role;
};

const handleConfirm = async () => {
  if (!selectedRole.value) return;
  
  const success = await authStore.selectRole(selectedRole.value);
  
  if (success) {
    // Redirect to dashboard
    router.push('/dashboard');
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.role-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.role-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 900px;
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

.error-message {
  padding: 12px;
  margin-bottom: 20px;
  background-color: #fed7d7;
  border: 1px solid #fc8181;
  border-radius: 8px;
  color: #c53030;
  font-size: 14px;
  text-align: center;
}

.role-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.role-option {
  padding: 30px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.role-option:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.role-option.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.role-icon {
  font-size: 48px;
  margin-bottom: 16px;
  text-align: center;
}

.role-option h2 {
  margin: 0 0 12px 0;
  font-size: 22px;
  font-weight: 700;
  color: #1a202c;
  text-align: center;
}

.role-option p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  text-align: center;
}

.role-features {
  margin: 0;
  padding: 0;
  list-style: none;
}

.role-features li {
  padding: 8px 0;
  font-size: 13px;
  color: #718096;
  position: relative;
  padding-left: 24px;
}

.role-features li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #667eea;
  font-weight: bold;
}

.btn {
  width: 100%;
  padding: 16px 20px;
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

.role-footer {
  margin-top: 24px;
  text-align: center;
}

.logout-link {
  background: none;
  border: none;
  color: #718096;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
}

.logout-link:hover {
  color: #4a5568;
}
</style>
