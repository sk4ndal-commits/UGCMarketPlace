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
        <div v-else class="space-y-4">
          <div
            v-for="app in applications"
            :key="app.id"
            class="border border-gray-200 rounded-lg p-5 hover:shadow-md transition cursor-pointer"
            @click="viewCampaign(app.campaign)"
          >
            <!-- Application Header -->
            <div class="flex justify-between items-start mb-3">
              <div class="flex-1">
                <h4 class="text-lg font-semibold text-gray-800">{{ app.campaign_title }}</h4>
                <p class="text-sm text-gray-500 mt-1">Applied on {{ formatDate(app.created_at) }}</p>
              </div>
              <span
                class="px-3 py-1 text-sm font-medium rounded ml-4"
                :class="getStatusClass(app.status)"
              >
                {{ app.status_display }}
              </span>
            </div>

            <!-- Campaign Details -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3 text-sm">
              <div class="flex items-center text-gray-600">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>{{ app.influencer_followers || 'N/A' }} followers</span>
              </div>
              <div v-if="app.influencer_platform" class="flex items-center text-gray-600">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <span>{{ app.influencer_platform }}</span>
              </div>
              <div v-if="app.proposed_price" class="flex items-center text-gray-600">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>€{{ formatPrice(app.proposed_price) }}</span>
              </div>
            </div>

            <!-- Pitch Preview -->
            <div class="bg-gray-50 rounded p-3 mb-3">
              <p class="text-sm text-gray-700 line-clamp-2">{{ app.pitch }}</p>
            </div>

            <!-- Portfolio Link -->
            <div v-if="app.portfolio_link" class="text-sm">
              <a 
                :href="app.portfolio_link" 
                target="_blank"
                class="text-blue-600 hover:text-blue-800 flex items-center"
                @click.stop
              >
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                View Portfolio
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import campaignService, { type Application } from '../services/campaignService';

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
function getStatusClass(status?: string): string {
  switch (status) {
    case 'PENDING':
      return 'bg-yellow-100 text-yellow-800';
    case 'SHORTLISTED':
      return 'bg-blue-100 text-blue-800';
    case 'ACCEPTED':
      return 'bg-green-100 text-green-800';
    case 'REJECTED':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}

/**
 * Format date for display
 */
function formatDate(dateString?: string): string {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format price for display
 */
function formatPrice(price?: string | number): string {
  if (!price) return '0.00';
  const amount = typeof price === 'string' ? parseFloat(price) : price;
  return amount.toFixed(2);
}
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
}
</style>
