<template>
  <div class="container mx-auto px-4 py-6">
    <div class="bg-white rounded-lg shadow-sm">
      <div class="bg-gradient-primary text-white p-5 rounded-t-lg">
        <h3 class="text-2xl font-bold">My Campaign Applications</h3>
      </div>

      <div class="p-6">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-700"></div>
          <p class="mt-3 text-gray-600">Loading your applications...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ errorMessage }}
        </div>

        <!-- Empty State -->
        <div v-else-if="applications.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">No applications yet</h3>
          <p class="mt-1 text-sm text-gray-500">
            You haven't applied to any campaigns yet. Browse campaigns to get started!
          </p>
          <div class="mt-6">
            <button
              @click="$router.push('/campaigns')"
              class="px-4 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition"
            >
              Browse Campaigns
            </button>
          </div>
        </div>

        <!-- Applications List -->
        <div v-else>
          <MyApplicationsList :applications="applications" :currentUserId="null" @view="viewCampaign" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import campaignService from '../services/campaignService';
import MyApplicationsList from './shared/MyApplicationsList.vue';
import type { Application } from '../models/campaign';

const router = useRouter();

const loading = ref(false);
const errorMessage = ref('');
const applications = ref<Application[]>([]);

/**
 * Load applications on mount
 */
onMounted(async () => {
  await loadApplications();
});

/**
 * Load all campaign applications for current user
 */
async function loadApplications() {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await campaignService.getApplications();
    if (response.status === 'success' && Array.isArray(response.data)) {
      applications.value = response.data;
    } else {
      errorMessage.value = 'Failed to load applications';
    }
  } catch (error: any) {
    console.error('Failed to load applications:', error);
    errorMessage.value = error.response?.data?.message || 'Failed to load applications';
  } finally {
    loading.value = false;
  }
}

/**
 * View campaign details
 */
function viewCampaign(campaignId: number) {
  router.push(`/campaigns/${campaignId}`);
}

/**
 * Get status badge class
 */
// Helpers moved into ApplicationItem component
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}
</style>
