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

            <div v-if="!isInfluencer" class="mb-6">
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

        <!-- Application Form Column (for Influencers) -->
        <div v-if="isInfluencer" class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm p-6 sticky top-5">
            <h4 class="text-xl font-bold mb-4">Apply to Campaign</h4>

            <!-- Success Message -->
            <div v-if="applicationSuccess" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              <p class="mb-2">
                <span class="mr-2">✓</span>
                Application submitted successfully! You will receive a confirmation email shortly.
              </p>
              <button
                @click="$router.push('/my-applications')"
                class="text-green-800 underline hover:text-green-900 font-medium"
              >
                View My Applications →
              </button>
            </div>

            <!-- Already Applied Message -->
            <div v-else-if="alreadyApplied" class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-4">
              <p class="mb-2">
                <span class="mr-2">!</span>
                You have already applied to this campaign.
              </p>
              <button
                @click="$router.push('/my-applications')"
                class="text-blue-800 underline hover:text-blue-900 font-medium"
              >
                View My Applications →
              </button>
            </div>

            <!-- Application Form -->
            <form v-else @submit.prevent="submitApplication">
              <div class="mb-4">
                <label for="pitch" class="block text-sm font-medium text-gray-700 mb-1">
                  Your Pitch <span class="text-red-600">*</span>
                </label>
                <textarea
                  id="pitch"
                  v-model="applicationForm.pitch"
                  class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="5"
                  placeholder="Tell the brand why you're perfect for this campaign..."
                  required
                  :disabled="submitting"
                ></textarea>
                <p class="mt-1 text-sm text-gray-500">
                  Describe your content style, audience, and why you're a great fit.
                </p>
              </div>

              <div class="mb-4">
                <label for="portfolio_link" class="block text-sm font-medium text-gray-700 mb-1">
                  Portfolio Link (Optional)
                </label>
                <input
                  id="portfolio_link"
                  v-model="applicationForm.portfolio_link"
                  type="url"
                  class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="https://instagram.com/yourprofile"
                  :disabled="submitting"
                />
                <p class="mt-1 text-sm text-gray-500">
                  Link to your social media profile or portfolio.
                </p>
              </div>

              <div class="mb-4">
                <label for="proposed_price" class="block text-sm font-medium text-gray-700 mb-1">
                  Proposed Price (Optional)
                </label>
                <div class="flex items-center border border-gray-300 rounded">
                  <span class="px-3 text-gray-600 bg-gray-50">€</span>
                  <input
                    id="proposed_price"
                    v-model="applicationForm.proposed_price"
                    type="number"
                    step="0.01"
                    min="0.01"
                    class="flex-1 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r"
                    placeholder="220.00"
                    :disabled="submitting"
                  />
                </div>
                <p class="mt-1 text-sm text-gray-500">
                  Suggest your price if the budget is negotiable.
                </p>
              </div>

              <!-- Error Message -->
              <div v-if="applicationError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {{ applicationError }}
              </div>

              <button
                type="submit"
                class="w-full bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
                :disabled="submitting || !applicationForm.pitch.trim()"
              >
                <span v-if="submitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                {{ submitting ? 'Submitting...' : 'Submit Application' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import campaignService, { type Campaign, type ApplicationFormData } from '../services/campaignService';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const campaign = ref<Campaign | null>(null);
const loading = ref(true);
const errorMessage = ref('');
const submitting = ref(false);
const applicationSuccess = ref(false);
const applicationError = ref('');
const alreadyApplied = ref(false);

const applicationForm = ref<ApplicationFormData>({
  campaign: 0,
  pitch: '',
  portfolio_link: '',
  proposed_price: undefined,
});

const isInfluencer = computed(() => authStore.user?.role === 'INFLUENCER');

const loadCampaign = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const campaignId = parseInt(route.params.id as string);
    const response = await campaignService.getCampaign(campaignId);
    campaign.value = response.data as Campaign;
    applicationForm.value.campaign = campaignId;
    
    // Check if user already applied to this campaign
    if (isInfluencer.value) {
      await checkIfAlreadyApplied(campaignId);
    }
  } catch (error: any) {
    console.error('Error loading campaign:', error);
    errorMessage.value = 'Failed to load campaign details. Please try again later.';
  } finally {
    loading.value = false;
  }
};

const checkIfAlreadyApplied = async (campaignId: number) => {
  try {
    const response = await campaignService.getApplications();
    if (response.status === 'success' && Array.isArray(response.data)) {
      // Check if any application is for this campaign
      const existingApplication = response.data.find(
        (app: any) => app.campaign === campaignId
      );
      if (existingApplication) {
        alreadyApplied.value = true;
      }
    }
  } catch (error: any) {
    console.error('Error checking existing applications:', error);
    // Don't show error to user, just log it
  }
};

const submitApplication = async () => {
  if (!applicationForm.value.pitch.trim()) {
    applicationError.value = 'Please provide a pitch.';
    return;
  }

  submitting.value = true;
  applicationError.value = '';

  try {
    // Prepare data - remove empty optional fields
    const data: ApplicationFormData = {
      campaign: applicationForm.value.campaign,
      pitch: applicationForm.value.pitch,
    };

    if (applicationForm.value.portfolio_link?.trim()) {
      data.portfolio_link = applicationForm.value.portfolio_link;
    }

    if (applicationForm.value.proposed_price && parseFloat(applicationForm.value.proposed_price.toString()) > 0) {
      data.proposed_price = applicationForm.value.proposed_price;
    }

    await campaignService.createApplication(data);
    applicationSuccess.value = true;
    
    // Reset form
    applicationForm.value.pitch = '';
    applicationForm.value.portfolio_link = '';
    applicationForm.value.proposed_price = undefined;
  } catch (error: any) {
    console.error('Error submitting application:', error);
    
    // Handle specific error messages
    if (error.response?.data?.errors) {
      const errors = error.response.data.errors;
      if (typeof errors === 'string') {
        applicationError.value = errors;
      } else if (errors.campaign) {
        if (Array.isArray(errors.campaign)) {
          applicationError.value = errors.campaign[0];
        } else {
          applicationError.value = errors.campaign;
        }
        // Check if already applied
        if (applicationError.value.includes('already applied')) {
          alreadyApplied.value = true;
        }
      } else if (errors.non_field_errors) {
        applicationError.value = Array.isArray(errors.non_field_errors)
          ? errors.non_field_errors[0]
          : errors.non_field_errors;
      } else {
        applicationError.value = 'Failed to submit application. Please check your input and try again.';
      }
    } else {
      applicationError.value = 'Failed to submit application. Please try again later.';
    }
  } finally {
    submitting.value = false;
  }
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

const getFileName = (filePath: string): string => {
  return filePath.split('/').pop() || filePath;
};

onMounted(() => {
  loadCampaign();
});
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
