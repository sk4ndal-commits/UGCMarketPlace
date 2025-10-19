<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-gradient-primary p-3">
    <div class="card shadow-lg" style="max-width: 900px; width: 100%;">
      <div class="card-body p-4 p-md-5">
        <h1 class="text-center mb-2 fw-bold">Choose Your Role</h1>
        <p class="text-center text-muted mb-4">Select how you'd like to use Civana</p>
        
        <!-- Error Messages -->
        <div v-if="error" class="alert alert-danger text-center" role="alert">
          {{ error }}
        </div>
        
        <div class="row g-3 mb-4">
          <!-- Brand Option -->
          <div class="col-md-6">
            <div
              class="card h-100 cursor-pointer card-hover"
              :class="{ 'border-primary border-2 bg-light': selectedRole === 'BRAND' }"
              @click="selectRole('BRAND')"
            >
              <div class="card-body p-4">
                <div class="text-center fs-1 mb-3">🏢</div>
                <h2 class="text-center fs-5 fw-bold mb-3">Brand</h2>
                <p class="text-center text-muted mb-3">
                  Create UGC campaigns, collaborate with creators, and get authentic content for your brand.
                </p>
                <ul class="list-unstyled">
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Post campaign briefs</li>
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Review creator applications</li>
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Manage collaborations</li>
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Receive quality content</li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Influencer Option -->
          <div class="col-md-6">
            <div
              class="card h-100 cursor-pointer card-hover"
              :class="{ 'border-primary border-2 bg-light': selectedRole === 'INFLUENCER' }"
              @click="selectRole('INFLUENCER')"
            >
              <div class="card-body p-4">
                <div class="text-center fs-1 mb-3">✨</div>
                <h2 class="text-center fs-5 fw-bold mb-3">Creator</h2>
                <p class="text-center text-muted mb-3">
                  Browse campaigns, apply with proposals, and get paid for creating authentic content.
                </p>
                <ul class="list-unstyled">
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Browse available campaigns</li>
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Submit applications</li>
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Collaborate with brands</li>
                  <li class="mb-2 text-muted"><i class="text-primary">✓</i> Get paid for your work</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Confirm Button -->
        <button
          class="btn btn-primary w-100 py-2 fw-semibold"
          :disabled="!selectedRole || loading"
          @click="handleConfirm"
        >
          <span v-if="loading">Confirming...</span>
          <span v-else>Continue as {{ selectedRole === 'BRAND' ? 'Brand' : 'Creator' }}</span>
        </button>
        
        <!-- Logout Link -->
        <div class="text-center mt-4">
          <button @click="handleLogout" class="btn btn-link text-muted text-decoration-underline">Log out</button>
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
/* Bootstrap classes are used, minimal custom styles needed */
.cursor-pointer {
  cursor: pointer;
}
</style>
