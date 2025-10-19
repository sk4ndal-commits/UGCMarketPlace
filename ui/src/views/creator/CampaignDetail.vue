<template>
  <div class="container mx-auto px-4 py-6 max-w-7xl">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-600">Loading campaign details...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ errorMessage }}
      <button class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity mt-3" @click="$router.push('/campaigns')">
        Back to Campaigns
      </button>
    </div>

    <!-- Campaign Details -->
    <div v-else-if="campaign">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Campaign Info Column -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div class="flex justify-between items-start mb-6">
              <h2 class="text-2xl font-bold">{{ campaign.title }}</h2>
              <span
                class="ml-4 px-3 py-1 text-sm font-semibold rounded"
                :class="getStatusBadgeClass(campaign.status)"
              >
                {{ campaign.status_display }}
              </span>
            </div>

            <div class="mb-6">
              <h5 class="text-lg font-semibold text-gray-600 mb-2">Description</h5>
              <p class="text-lg text-gray-700">{{ campaign.description }}</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div class="bg-gray-50 p-4 rounded border border-gray-200">
                <div class="flex items-center mb-2">
                  <span class="mr-2">🎥</span>
                  <strong>Content Type:</strong>
                </div>
                <div class="mt-1 text-gray-700">{{ campaign.content_type_display }}</div>
              </div>
              <div class="bg-gray-50 p-4 rounded border border-gray-200">
                <div class="flex items-center mb-2">
                  <span class="mr-2 text-blue-600">🏷️</span>
                  <strong>Category:</strong>
                </div>
                <div class="mt-1 text-gray-700">{{ campaign.category_display }}</div>
              </div>
              <div class="bg-gray-50 p-4 rounded border border-gray-200">
                <div class="flex items-center mb-2">
                  <span class="mr-2 text-green-600">💰</span>
                  <strong>Budget:</strong>
                </div>
                <div class="mt-1 text-gray-700">€{{ formatBudget(campaign.budget) }}</div>
              </div>
              <div class="bg-gray-50 p-4 rounded border border-gray-200">
                <div class="flex items-center mb-2">
                  <span class="mr-2 text-yellow-600">📅</span>
                  <strong>Deadline:</strong>
                </div>
                <div class="mt-1 text-gray-700">{{ formatDate(campaign.deadline) }}</div>
              </div>
            </div>

            <div class="mb-6">
              <h5 class="text-lg font-semibold text-gray-600 mb-2">Deliverables</h5>
              <p class="whitespace-pre-line text-gray-700">{{ campaign.deliverables }}</p>
            </div>

            <div class="mb-6">
              <h5 class="text-lg font-semibold text-gray-600 mb-2">Brand</h5>
              <p class="flex items-center">
                <span class="mr-2">🏢</span>{{ campaign.brand_email }}
              </p>
            </div>

            <!-- Reference Files -->
            <div v-if="campaign.reference_files && campaign.reference_files.length > 0" class="mb-6">
              <h5 class="text-lg font-semibold text-gray-600 mb-2">Reference Materials</h5>
              <div class="space-y-2">
                <a
                  v-for="file in campaign.reference_files"
                  :key="file.id"
                  :href="file.file"
                  target="_blank"
                  class="flex items-center justify-between p-3 bg-white border border-gray-200 rounded hover:bg-gray-50 transition-colors"
                >
                  <span class="flex items-center">
                    <span class="mr-2">📄</span>
                    {{ getFileName(file.file) }}
                  </span>
                  <span class="text-blue-600">⬇</span>
                </a>
              </div>
            </div>

            <div class="mt-6">
              <button class="bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors" @click="$router.push('/campaigns')">
                <span class="mr-2">←</span>Back to Campaigns
              </button>
            </div>
          </div>
        </div>

        <!-- Application Form Column (for creators/influencers) -->
        <div class="lg:col-span-1">
          <CampaignApplyForm :campaignId="campaign?.id || 0" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import campaignService from '../../services/campaignService';
import CampaignApplyForm from './CampaignApplyForm.vue';
import type { Campaign } from '../../models/campaign';

const route = useRoute();
// router and authStore not needed in creator detail currently
// const router = useRouter();
// const authStore = useAuthStore();

const campaign = ref<Campaign | null>(null);
const loading = ref(true);
const errorMessage = ref('');

const loadCampaign = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const campaignId = parseInt(route.params.id as string);
    const response = await campaignService.getCampaign(campaignId);
    campaign.value = response.data as Campaign;
  } catch (error: any) {
    console.error('Error loading campaign:', error);
    errorMessage.value = 'Failed to load campaign details. Please try again later.';
  } finally {
    loading.value = false;
  }
};

const formatBudget = (budget: string | number): string => {
  const amount = typeof budget === 'string' ? parseFloat(budget) : budget;
  return amount.toFixed(2);
};

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const getStatusBadgeClass = (status: string): string => {
  switch (status) {
    case 'LIVE':
      return 'bg-green-500 text-white';
    case 'DRAFT':
      return 'bg-gray-500 text-white';
    case 'CLOSED':
      return 'bg-red-500 text-white';
    default:
      return 'bg-gray-500 text-white';
  }
};

const getFileName = (filePath: string): string => {
  return filePath.split('/').pop() || filePath;
};

onMounted(() => {
  loadCampaign();
});

// no-op to avoid unused-variable TS errors if tools are stricter
void getStatusBadgeClass;
void getFileName;
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>

*** End Patch