<template>
  <div class="dashboard-container">
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
      <div class="dashboard-header">
        <h2>Dashboard</h2>
        <p class="role-badge">
          {{ user?.role === 'BRAND' ? '🏢 Brand' : '✨ Creator' }}
        </p>
      </div>
      
      <div class="dashboard-grid">
        <!-- Brand Dashboard -->
        <template v-if="user?.role === 'BRAND'">
          <div class="dashboard-card">
            <h3>Create Campaign</h3>
            <p>Post a new UGC campaign and start receiving applications from creators.</p>
            <button class="btn btn-primary" disabled>Coming Soon</button>
          </div>
          
          <div class="dashboard-card">
            <h3>My Campaigns</h3>
            <p>View and manage your active and past campaigns.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
          
          <div class="dashboard-card">
            <h3>Applications</h3>
            <p>Review applications from creators interested in your campaigns.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
          
          <div class="dashboard-card">
            <h3>Messages</h3>
            <p>Communicate with creators and manage collaborations.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
        </template>
        
        <!-- Creator Dashboard -->
        <template v-else-if="user?.role === 'INFLUENCER'">
          <div class="dashboard-card">
            <h3>Browse Campaigns</h3>
            <p>Discover available UGC campaigns and find your next collaboration.</p>
            <button class="btn btn-primary" disabled>Coming Soon</button>
          </div>
          
          <div class="dashboard-card">
            <h3>My Applications</h3>
            <p>Track your submitted applications and their status.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
          
          <div class="dashboard-card">
            <h3>Active Projects</h3>
            <p>View your ongoing collaborations and deliverables.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
          
          <div class="dashboard-card">
            <h3>Messages</h3>
            <p>Communicate with brands and manage your projects.</p>
            <button class="btn btn-secondary" disabled>Coming Soon</button>
          </div>
        </template>
      </div>
      
      <div class="info-card">
        <h3>🎉 Welcome to Civana!</h3>
        <p>
          Your authentication is complete. The dashboard features are currently under development.
          This is the MVP authentication implementation.
        </p>
        <div class="feature-list">
          <h4>✅ Completed Features:</h4>
          <ul>
            <li>User registration with email/password</li>
            <li>Secure login and logout</li>
            <li>Password reset flow</li>
            <li>Role selection (Brand / Creator)</li>
            <li>JWT token authentication</li>
            <li>GDPR consent tracking</li>
            <li>Protected routes and navigation guards</li>
          </ul>
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
.dashboard-container {
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.dashboard-header {
  margin-bottom: 40px;
  text-align: center;
}

.dashboard-header h2 {
  margin: 0 0 12px 0;
  font-size: 32px;
  font-weight: 700;
  color: #1a202c;
}

.role-badge {
  display: inline-block;
  padding: 8px 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 1px solid #667eea;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.dashboard-card h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1a202c;
}

.dashboard-card p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #718096;
  line-height: 1.6;
}

.btn {
  width: 100%;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
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

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-secondary:hover:not(:disabled) {
  background: #cbd5e0;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.info-card {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: 1px solid #667eea;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
}

.info-card h3 {
  margin: 0 0 16px 0;
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
}

.info-card p {
  margin: 0 0 24px 0;
  font-size: 16px;
  color: #4a5568;
  line-height: 1.6;
}

.feature-list {
  background: white;
  border-radius: 8px;
  padding: 24px;
  text-align: left;
  max-width: 600px;
  margin: 0 auto;
}

.feature-list h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 700;
  color: #1a202c;
}

.feature-list ul {
  margin: 0;
  padding-left: 20px;
}

.feature-list li {
  margin: 8px 0;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}
</style>
