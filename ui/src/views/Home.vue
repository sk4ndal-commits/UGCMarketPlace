<template>
  <div class="home-container">
    <nav class="navbar">
      <div class="nav-content">
        <h1 class="logo">Civana</h1>
        <div class="nav-actions">
          <span class="user-email">{{ user?.email }}</span>
          <button @click="handleLogout" class="btn-logout">Log out</button>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <div class="welcome-card">
        <h2>Welcome to Civana</h2>
        <p>
          <strong>{{ user?.first_name }} {{ user?.last_name }}</strong>
        </p>
        <p class="role-badge" v-if="user?.role">
          Role: {{ user.role === 'BRAND' ? 'Brand' : 'Creator' }}
        </p>
        
        <div class="info-section">
          <p>You're successfully logged in!</p>
          <p v-if="!user?.role" class="hint">
            Please select your role to continue.
            <router-link to="/role-selection">Go to role selection →</router-link>
          </p>
          <p v-else class="hint">
            Your dashboard is ready.
            <router-link to="/dashboard">Go to dashboard →</router-link>
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const user = computed(() => authStore.user);

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: #f8f9fb;
}

.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 16px 0;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-email {
  font-size: 14px;
  color: #4a5568;
}

.btn-logout {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  border-color: #cbd5e0;
  background: #f7fafc;
}

.main-content {
  max-width: 800px;
  margin: 60px auto;
  padding: 0 20px;
}

.welcome-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.welcome-card h2 {
  margin: 0 0 16px 0;
  font-size: 28px;
  font-weight: 700;
  color: #1a202c;
}

.welcome-card p {
  margin: 8px 0;
  font-size: 16px;
  color: #4a5568;
}

.role-badge {
  display: inline-block;
  margin: 16px 0;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 1px solid #667eea;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
}

.info-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.hint {
  font-size: 14px;
  color: #718096;
  margin-top: 12px;
}

.hint a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}

.hint a:hover {
  text-decoration: underline;
}
</style>
