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
    
    <main class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-body p-4 p-md-5 text-center">
              <h2 class="fw-bold mb-3">Welcome to Civana</h2>
              <p class="fs-5 fw-semibold text-dark mb-3">
                {{ user?.first_name }} {{ user?.last_name }}
              </p>
              <span v-if="user?.role" class="badge role-badge rounded-pill px-3 py-2 fs-6 mb-4">
                Role: {{ user.role === 'BRAND' ? 'Brand' : 'Creator' }}
              </span>
              
              <hr class="my-4">
              
              <div class="mt-4">
                <p class="text-muted mb-3">You're successfully logged in!</p>
                <p v-if="!user?.role" class="text-muted">
                  Please select your role to continue.
                  <router-link to="/role-selection" class="text-decoration-none fw-semibold">
                    Go to role selection →
                  </router-link>
                </p>
                <p v-else class="text-muted">
                  Your dashboard is ready.
                  <router-link to="/dashboard" class="text-decoration-none fw-semibold">
                    Go to dashboard →
                  </router-link>
                </p>
              </div>
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
