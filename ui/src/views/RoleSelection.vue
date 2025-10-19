<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-primary p-4">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-4xl">
      <div class="p-6 md:p-8">
        <h1 class="text-center text-3xl font-bold mb-2">Choose Your Role</h1>
        <p class="text-center text-gray-500 mb-6">Select how you'd like to use Civana</p>
        
        <!-- Error Messages -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-center">
          {{ error }}
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <!-- Brand Option -->
          <div
            class="bg-white border-2 rounded-lg p-6 cursor-pointer card-hover transition-all"
            :class="selectedRole === 'BRAND' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
            @click="selectRole('BRAND')"
          >
            <div class="text-center text-5xl mb-4">🏢</div>
            <h2 class="text-center text-xl font-bold mb-3">Brand</h2>
            <p class="text-center text-gray-500 mb-4">
              Create UGC campaigns, collaborate with creators, and get authentic content for your brand.
            </p>
            <ul class="space-y-2">
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Post campaign briefs</li>
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Review creator applications</li>
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Manage collaborations</li>
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Receive quality content</li>
            </ul>
          </div>
          
          <!-- Influencer Option -->
          <div
            class="bg-white border-2 rounded-lg p-6 cursor-pointer card-hover transition-all"
            :class="selectedRole === 'INFLUENCER' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
            @click="selectRole('INFLUENCER')"
          >
            <div class="text-center text-5xl mb-4">✨</div>
            <h2 class="text-center text-xl font-bold mb-3">Creator</h2>
            <p class="text-center text-gray-500 mb-4">
              Browse campaigns, apply with proposals, and get paid for creating authentic content.
            </p>
            <ul class="space-y-2">
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Browse available campaigns</li>
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Submit applications</li>
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Collaborate with brands</li>
              <li class="text-gray-600"><span class="text-blue-600 mr-2">✓</span>Get paid for your work</li>
            </ul>
          </div>
        </div>
        
        <!-- Confirm Button -->
        <button
          class="w-full bg-gradient-primary text-white font-semibold py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
          :disabled="!selectedRole || loading"
          @click="handleConfirm"
        >
          <span v-if="loading">Confirming...</span>
          <span v-else>Continue as {{ selectedRole === 'BRAND' ? 'Brand' : 'Creator' }}</span>
        </button>
        
        <!-- Logout Link -->
        <div class="text-center mt-6">
          <button @click="handleLogout" class="text-gray-500 hover:text-gray-700 underline">Log out</button>
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
/* All styles now handled by Tailwind CSS */
</style>
