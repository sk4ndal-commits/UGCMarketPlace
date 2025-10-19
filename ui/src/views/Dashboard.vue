<template>
  <div class="min-h-screen bg-[#f8f9fb]">
    <nav class="bg-white shadow-sm">
      <div class="container mx-auto px-3 md:px-4 py-3 flex items-center justify-between">
        <h1 class="text-2xl font-bold navbar-brand-gradient">Civana</h1>
        <div class="flex items-center gap-3">
          <span class="text-gray-500 text-sm hidden md:inline">{{ user?.email }}</span>
          <button @click="handleLogout" class="px-3 py-1.5 text-sm border border-gray-300 rounded hover:bg-gray-50 transition-colors">Log out</button>
        </div>
      </div>
    </nav>
    
    <main class="container mx-auto px-4 py-6 md:py-8">
      <div class="text-center mb-6 md:mb-8">
        <h2 class="text-3xl font-bold mb-3">Dashboard</h2>
        <span class="role-badge rounded-full px-4 py-2 text-base inline-block">
          {{ user?.role === 'BRAND' ? '🏢 Brand' : '✨ Creator' }}
        </span>
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4 mb-6">
        <!-- Brand Dashboard -->
        <template v-if="user?.role === 'BRAND'">
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">Create Campaign</h3>
              <p class="text-gray-500 text-sm mb-4">Post a new UGC campaign and start receiving applications from creators.</p>
              <button class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg w-full hover:opacity-90 transition-opacity" @click="router.push('/campaigns/create')">Create Campaign</button>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">My Campaigns</h3>
              <p class="text-gray-500 text-sm mb-4">View and manage your active and past campaigns.</p>
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg w-full hover:bg-gray-300 transition-colors" @click="router.push('/campaigns')">View Campaigns</button>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">Applications</h3>
              <p class="text-gray-500 text-sm mb-4">Review applications from creators interested in your campaigns.</p>
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg w-full opacity-50 cursor-not-allowed" disabled>Coming Soon</button>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">Messages</h3>
              <p class="text-gray-500 text-sm mb-4">Communicate with creators and manage collaborations.</p>
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg w-full opacity-50 cursor-not-allowed" disabled>Coming Soon</button>
            </div>
          </div>
        </template>
        
        <!-- Creator Dashboard -->
        <template v-else-if="user?.role === 'INFLUENCER'">
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">Browse Campaigns</h3>
              <p class="text-gray-500 text-sm mb-4">Discover available UGC campaigns and find your next collaboration.</p>
              <button class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg w-full hover:opacity-90 transition-opacity" @click="router.push('/campaigns')">Browse Campaigns</button>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">My Applications</h3>
              <p class="text-gray-500 text-sm mb-4">Track your submitted applications and their status.</p>
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg w-full hover:bg-gray-300 transition-colors" @click="router.push('/applications')">View Applications</button>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">Active Projects</h3>
              <p class="text-gray-500 text-sm mb-4">View your ongoing collaborations and deliverables.</p>
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg w-full opacity-50 cursor-not-allowed" disabled>Coming Soon</button>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm card-hover h-full">
            <div class="p-5">
              <h3 class="text-lg font-bold mb-2">Messages</h3>
              <p class="text-gray-500 text-sm mb-4">Communicate with brands and manage your projects.</p>
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg w-full opacity-50 cursor-not-allowed" disabled>Coming Soon</button>
            </div>
          </div>
        </template>
      </div>
      
      <!-- Creator Feature Banner -->
      <div v-if="user?.role === 'INFLUENCER'" class="bg-white border-2 border-green-500 rounded-lg shadow-sm mb-6">
        <div class="p-6 text-center">
          <h3 class="text-xl font-bold mb-3 text-green-600">🚀 New Features Available!</h3>
          <p class="text-gray-500 mb-4">
            You can now browse campaigns, apply to collaborations, and track your applications!
          </p>
          <div class="flex flex-col md:flex-row gap-3 justify-center">
            <button class="bg-green-600 text-white font-medium py-2 px-4 rounded-lg hover:bg-green-700 transition-colors" @click="router.push('/campaigns')">
              <span class="mr-2">🔍</span>Browse Campaigns
            </button>
            <button class="border-2 border-green-600 text-green-600 font-medium py-2 px-4 rounded-lg hover:bg-green-50 transition-colors" @click="router.push('/applications')">
              <span class="mr-2">✓</span>My Applications
            </button>
          </div>
        </div>
      </div>
      
      <div class="bg-white border-2 border-blue-500 rounded-lg shadow-sm">
        <div class="p-6 md:p-8 text-center">
          <h3 class="text-xl font-bold mb-3">🎉 Welcome to Civana!</h3>
          <p class="text-gray-500 mb-6">
            <template v-if="user?.role === 'BRAND'">
              Create campaigns and connect with talented creators.
            </template>
            <template v-else>
              Start your journey by exploring available campaigns and applying to collaborations.
            </template>
          </p>
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm mx-auto max-w-2xl">
            <div class="p-6 text-left">
              <h4 class="text-base font-bold mb-3">✅ Platform Features:</h4>
              <ul class="space-y-2">
                <li class="text-gray-500 text-sm">• User registration with email/password</li>
                <li class="text-gray-500 text-sm">• Secure login and logout</li>
                <li class="text-gray-500 text-sm">• Password reset flow</li>
                <li class="text-gray-500 text-sm">• Role selection (Brand / Creator)</li>
                <li class="text-gray-500 text-sm">• JWT token authentication</li>
                <li class="text-gray-500 text-sm">• GDPR consent tracking</li>
                <li class="text-gray-500 text-sm">• Protected routes and navigation guards</li>
                <template v-if="user?.role === 'BRAND'">
                  <li class="text-green-600 text-sm font-bold">• Campaign creation & management</li>
                </template>
                <template v-else>
                  <li class="text-green-600 text-sm font-bold">• Campaign browsing with filters</li>
                  <li class="text-green-600 text-sm font-bold">• Application submission</li>
                  <li class="text-green-600 text-sm font-bold">• Application tracking</li>
                </template>
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
