<template>
  <div class="container mx-auto px-4 py-6 max-w-7xl">
    <h2 class="text-2xl font-bold mb-6">
      {{ isBrand ? 'Campaign Applications' : 'My Applications' }}
    </h2>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-600">Loading applications...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ errorMessage }}
    </div>

    <!-- Empty State -->
    <div v-else-if="applications.length === 0" class="text-center py-12">
      <div class="text-6xl text-gray-300 mb-4">📭</div>
      <h4 class="text-xl font-semibold mb-2">No applications found</h4>
      <p class="text-gray-500 mb-4">
        {{ isBrand 
          ? 'Applications to your campaigns will appear here.' 
          : 'You haven\'t applied to any campaigns yet.' 
        }}
      </p>
      <button
        v-if="!isBrand"
        class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity"
        @click="$router.push('/campaigns')"
      >
        Browse Campaigns
      </button>
    </div>

    <!-- Applications List -->
    <div v-else class="space-y-4">
      <div
        v-for="application in applications"
        :key="application.id"
        class="bg-white rounded-lg shadow-sm card-hover"
      >
        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Application Info -->
            <div class="lg:col-span-2">
              <div class="flex justify-between items-start mb-4">
                <h5 class="text-lg font-semibold flex items-center">
                  <span class="mr-2 text-blue-600">📢</span>
                  {{ application.campaign_title }}
                </h5>
                <span
                  class="ml-4 px-3 py-1 text-xs font-semibold rounded"
                  :class="getStatusBadgeClass(application.status)"
                >
                  {{ application.status_display }}
                </span>
              </div>

              <div class="mb-4">
                <h6 class="text-sm font-semibold text-gray-600 mb-2">Pitch</h6>
                <p class="text-gray-700">{{ application.pitch }}</p>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                <div v-if="isBrand" class="flex items-center">
                  <strong class="mr-2">Influencer:</strong>
                  <span class="text-gray-700">{{ application.influencer_email }}</span>
                </div>
                <div v-if="isBrand && application.influencer_platform" class="flex items-center">
                  <strong class="mr-2">Platform:</strong>
                  <span class="text-gray-700">{{ application.influencer_platform }}</span>
                </div>
                <div v-if="isBrand && application.influencer_followers" class="flex items-center">
                  <strong class="mr-2">Followers:</strong>
                  <span class="text-gray-700">{{ formatNumber(application.influencer_followers) }}</span>
                </div>
                <div v-if="isBrand && application.influencer_engagement_rate" class="flex items-center">
                  <strong class="mr-2">Engagement:</strong>
                  <span class="text-gray-700">{{ formatEngagement(application.influencer_engagement_rate) }}%</span>
                </div>
                <div v-if="application.portfolio_link" class="flex items-center">
                  <strong class="mr-2">Portfolio:</strong>
                  <a 
                    :href="application.portfolio_link" 
                    target="_blank" 
                    class="text-blue-600 hover:text-blue-800 flex items-center"
                  >
                    <span class="mr-1">🔗</span>
                    View Portfolio
                  </a>
                </div>
                <div v-if="application.proposed_price" class="flex items-center">
                  <strong class="mr-2">Proposed Price:</strong>
                  <span class="text-green-600 font-semibold">
                    €{{ formatPrice(application.proposed_price) }}
                  </span>
                </div>
                <div class="flex items-center">
                  <strong class="mr-2">Submitted:</strong>
                  <span class="text-gray-700">{{ formatDate(application.created_at!) }}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="lg:col-span-1 flex flex-col justify-center gap-3">
              <button
                class="px-4 py-2 border border-blue-500 text-blue-500 rounded-lg hover:bg-blue-50 transition-colors font-medium"
                @click="viewCampaign(application.campaign)"
              >
                <span class="mr-2">👁</span>View Campaign
              </button>
              
              <!-- Brand Actions -->
              <template v-if="isBrand">
                <button
                  v-if="application.status === 'PENDING'"
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
                  @click="updateStatus(application.id!, 'SHORTLISTED')"
                >
                  <span class="mr-2">⭐</span>Shortlist
                </button>
                
                <button
                  v-if="application.status === 'PENDING' || application.status === 'SHORTLISTED'"
                  class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
                  @click="confirmAction(application.id!, 'ACCEPTED', application.campaign_title!)"
                >
                  <span class="mr-2">✓</span>Accept
                </button>
                
                <button
                  v-if="application.status === 'PENDING' || application.status === 'SHORTLISTED'"
                  class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium"
                  @click="confirmAction(application.id!, 'REJECTED', application.campaign_title!)"
                >
                  <span class="mr-2">✗</span>Reject
                </button>
              </template>
              
              <!-- Influencer Actions -->
              <button
                v-if="!isBrand"
                class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
                @click="viewApplication(application.id!)"
              >
                <span class="mr-2">📄</span>View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Confirmation Dialog -->
  <div
    v-if="showConfirmDialog"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="cancelConfirmation"
  >
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-xl">
      <h3 class="text-xl font-bold mb-4">
        {{ confirmDialogTitle }}
      </h3>
      <p class="text-gray-700 mb-6">
        {{ confirmDialogMessage }}
      </p>
      <div class="flex justify-end gap-3">
        <button
          class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
          @click="cancelConfirmation"
        >
          Cancel
        </button>
        <button
          class="px-4 py-2 rounded-lg font-medium transition-colors text-white"
          :class="confirmDialogAction === 'ACCEPTED' ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'"
          @click="executeAction"
          :disabled="actionInProgress"
        >
          {{ actionInProgress ? 'Processing...' : 'Confirm' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import campaignService, { type Application } from '../services/campaignService';

const router = useRouter();
const authStore = useAuthStore();

const applications = ref<Application[]>([]);
const loading = ref(true);
const errorMessage = ref('');
const showConfirmDialog = ref(false);
const confirmDialogTitle = ref('');
const confirmDialogMessage = ref('');
const confirmDialogAction = ref('');
const confirmApplicationId = ref<number | null>(null);
const actionInProgress = ref(false);

const isBrand = computed(() => authStore.user?.role === 'BRAND');

const loadApplications = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await campaignService.getApplications();
    applications.value = Array.isArray(response.data) ? response.data : [response.data];
  } catch (error: any) {
    console.error('Error loading applications:', error);
    errorMessage.value = 'Failed to load applications. Please try again later.';
  } finally {
    loading.value = false;
  }
};

const viewCampaign = (campaignId: number) => {
  router.push(`/campaigns/${campaignId}`);
};

const viewApplication = (applicationId: number) => {
  router.push(`/applications/${applicationId}`);
};

const getStatusBadgeClass = (status?: string): string => {
  switch (status) {
    case 'PENDING':
      return 'bg-yellow-500 text-white';
    case 'SHORTLISTED':
      return 'bg-blue-500 text-white';
    case 'ACCEPTED':
      return 'bg-green-500 text-white';
    case 'REJECTED':
      return 'bg-red-500 text-white';
    default:
      return 'bg-gray-500 text-white';
  }
};

const formatPrice = (price: string | number): string => {
  const amount = typeof price === 'string' ? parseFloat(price) : price;
  return amount.toFixed(2);
};

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

const formatEngagement = (rate: string | number): string => {
  const rateNum = typeof rate === 'string' ? parseFloat(rate) : rate;
  return rateNum.toFixed(2);
};

const confirmAction = (applicationId: number, action: string, campaignTitle: string) => {
  confirmApplicationId.value = applicationId;
  confirmDialogAction.value = action;
  
  if (action === 'ACCEPTED') {
    confirmDialogTitle.value = 'Accept Application';
    confirmDialogMessage.value = `Are you sure you want to accept this application for "${campaignTitle}"? This will trigger a payment request and the selection will be irreversible after payment initiation.`;
  } else if (action === 'REJECTED') {
    confirmDialogTitle.value = 'Reject Application';
    confirmDialogMessage.value = `Are you sure you want to reject this application for "${campaignTitle}"? The influencer will receive an automated notification.`;
  }
  
  showConfirmDialog.value = true;
};

const updateStatus = async (applicationId: number, status: string) => {
  // Shortlist doesn't need confirmation
  actionInProgress.value = true;
  errorMessage.value = '';
  
  try {
    await campaignService.updateApplicationStatus(applicationId, status);
    // Reload applications to reflect changes
    await loadApplications();
  } catch (error: any) {
    console.error('Error updating application status:', error);
    errorMessage.value = error.response?.data?.errors?.[0] || 'Failed to update application status. Please try again.';
  } finally {
    actionInProgress.value = false;
  }
};

const executeAction = async () => {
  if (!confirmApplicationId.value || !confirmDialogAction.value) return;
  
  actionInProgress.value = true;
  errorMessage.value = '';
  
  try {
    await campaignService.updateApplicationStatus(confirmApplicationId.value, confirmDialogAction.value);
    showConfirmDialog.value = false;
    // Reload applications to reflect changes
    await loadApplications();
  } catch (error: any) {
    console.error('Error updating application status:', error);
    errorMessage.value = error.response?.data?.errors?.[0] || 'Failed to update application status. Please try again.';
    showConfirmDialog.value = false;
  } finally {
    actionInProgress.value = false;
    confirmApplicationId.value = null;
    confirmDialogAction.value = '';
  }
};

const cancelConfirmation = () => {
  showConfirmDialog.value = false;
  confirmApplicationId.value = null;
  confirmDialogAction.value = '';
  confirmDialogTitle.value = '';
  confirmDialogMessage.value = '';
};

onMounted(() => {
  loadApplications();
});
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
