<template>
  <div class="container mx-auto px-4 py-6 max-w-7xl">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-600">Loading campaign details...</p>
    </div>

    <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ errorMessage }}
      <button class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity mt-3" @click="$router.push('/campaigns')">
        Back to Campaigns
      </button>
    </div>

    <div v-else-if="campaign">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
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
          </div>
        </div>

        <!-- Brand actions / applicant list -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
            <h5 class="text-lg font-semibold mb-3">Applications</h5>
            <p class="text-sm text-gray-500 mb-3">View and manage applications submitted for this campaign.</p>
            <!-- Placeholder: real implementation should fetch and list applications for this campaign -->
            <div v-if="applicationsLoading" class="text-center py-6">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-700"></div>
            </div>
            <ul v-else class="space-y-2">
              <li v-for="app in applications" :key="app.id" class="p-2 border rounded">
                <div class="flex justify-between items-center">
                  <div>
                    <div class="font-medium">{{ app.influencer_email || ('influencer:' + (app.influencer || 'n/a')) }}</div>
                    <div class="text-xs text-gray-500">Price: €{{ app.proposed_price ?? '—' }} · Status: {{ app.status }}</div>
                  </div>
                  <div class="flex gap-2">
                    <button @click="() => viewApplication(app.id)" class="px-2 py-1 text-sm bg-blue-500 text-white rounded">View</button>
                    <button class="px-2 py-1 text-sm bg-green-500 text-white rounded">Accept</button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import campaignService from '../../services/campaignService';
import type { Campaign, Application as CampaignApplication } from '../../models/campaign';

const route = useRoute();

const campaign = ref<Campaign | null>(null);
const loading = ref(true);
const errorMessage = ref('');

// applications placeholder
const applications = ref<CampaignApplication[]>([]);
const applicationsLoading = ref(true);

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

const loadApplications = async () => {
  applicationsLoading.value = true;
  try {
    const response = await campaignService.getApplications();
    applications.value = Array.isArray(response.data) ? response.data : [response.data];
  } catch (error: any) {
    console.error('Error loading applications:', error);
  } finally {
    applicationsLoading.value = false;
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
  loadApplications();
});

const viewApplication = (id?: number) => {
  if (!id) return;
  // route to application detail
  window.location.href = `/applications/${id}`;
};

// no-op references to avoid TS6133 warnings
void formatBudget;
void formatDate;
void getFileName;
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>

*** End Patch