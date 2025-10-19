<template>
  <div class="min-vh-100" style="background-color: #f8f9fb;">
    <nav class="navbar navbar-expand navbar-light bg-white shadow-sm">
      <div class="container-fluid px-3 px-md-4">
        <h1 class="navbar-brand mb-0 h1 navbar-brand-gradient">Civana</h1>
        <div class="d-flex align-items-center gap-3">
          <span class="text-muted small d-none d-md-inline">{{ user?.email }}</span>
          <button @click="handleLogout" class="btn btn-outline-secondary btn-sm">Log out</button>
        </div>
      </div>
    </nav>
    
    <main class="container py-4 py-md-5">
      <div class="text-center mb-4 mb-md-5">
        <h2 class="fw-bold mb-3">Dashboard</h2>
        <span class="badge role-badge rounded-pill px-3 py-2 fs-6">
          {{ user?.role === 'BRAND' ? '🏢 Brand' : '✨ Creator' }}
        </span>
      </div>
      
      <div class="row g-3 g-md-4 mb-4">
        <!-- Brand Dashboard -->
        <template v-if="user?.role === 'BRAND'">
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">Create Campaign</h3>
                <p class="card-text text-muted small">Post a new UGC campaign and start receiving applications from creators.</p>
                <button class="btn btn-primary btn-sm w-100" @click="router.push('/campaigns/create')">Create Campaign</button>
              </div>
            </div>
          </div>
          
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">My Campaigns</h3>
                <p class="card-text text-muted small">View and manage your active and past campaigns.</p>
                <button class="btn btn-secondary btn-sm w-100" @click="router.push('/campaigns')">View Campaigns</button>
              </div>
            </div>
          </div>
          
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">Applications</h3>
                <p class="card-text text-muted small">Review applications from creators interested in your campaigns.</p>
                <button class="btn btn-secondary btn-sm w-100" disabled>Coming Soon</button>
              </div>
            </div>
          </div>
          
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">Messages</h3>
                <p class="card-text text-muted small">Communicate with creators and manage collaborations.</p>
                <button class="btn btn-secondary btn-sm w-100" disabled>Coming Soon</button>
              </div>
            </div>
          </div>
        </template>
        
        <!-- Creator Dashboard -->
        <template v-else-if="user?.role === 'INFLUENCER'">
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">Browse Campaigns</h3>
                <p class="card-text text-muted small">Discover available UGC campaigns and find your next collaboration.</p>
                <button class="btn btn-primary btn-sm w-100" disabled>Coming Soon</button>
              </div>
            </div>
          </div>
          
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">My Applications</h3>
                <p class="card-text text-muted small">Track your submitted applications and their status.</p>
                <button class="btn btn-secondary btn-sm w-100" disabled>Coming Soon</button>
              </div>
            </div>
          </div>
          
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">Active Projects</h3>
                <p class="card-text text-muted small">View your ongoing collaborations and deliverables.</p>
                <button class="btn btn-secondary btn-sm w-100" disabled>Coming Soon</button>
              </div>
            </div>
          </div>
          
          <div class="col-sm-6 col-lg-3">
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <h3 class="card-title h5 fw-bold">Messages</h3>
                <p class="card-text text-muted small">Communicate with brands and manage your projects.</p>
                <button class="btn btn-secondary btn-sm w-100" disabled>Coming Soon</button>
              </div>
            </div>
          </div>
        </template>
      </div>
      
      <div class="card border-primary shadow-sm">
        <div class="card-body p-4 p-md-5 text-center">
          <h3 class="fw-bold mb-3">🎉 Welcome to Civana!</h3>
          <p class="text-muted mb-4">
            Your authentication is complete. The dashboard features are currently under development.
            This is the MVP authentication implementation.
          </p>
          <div class="card bg-white border-0 shadow-sm mx-auto" style="max-width: 600px;">
            <div class="card-body text-start">
              <h4 class="h6 fw-bold mb-3">✅ Completed Features:</h4>
              <ul class="list-unstyled mb-0">
                <li class="mb-2 text-muted">• User registration with email/password</li>
                <li class="mb-2 text-muted">• Secure login and logout</li>
                <li class="mb-2 text-muted">• Password reset flow</li>
                <li class="mb-2 text-muted">• Role selection (Brand / Creator)</li>
                <li class="mb-2 text-muted">• JWT token authentication</li>
                <li class="mb-2 text-muted">• GDPR consent tracking</li>
                <li class="mb-2 text-muted">• Protected routes and navigation guards</li>
              </ul>
            </div>
          </div>
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
/* Bootstrap classes are used, minimal custom styles needed */
</style>
