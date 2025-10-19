<template>
  <div class="container mt-5">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading campaign details...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
      <button class="btn btn-primary mt-3" @click="$router.push('/campaigns')">
        Back to Campaigns
      </button>
    </div>

    <!-- Campaign Details -->
    <div v-else-if="campaign">
      <div class="row">
        <!-- Campaign Info Column -->
        <div class="col-lg-8">
          <div class="card shadow-sm mb-4">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h2 class="card-title">{{ campaign.title }}</h2>
                <span
                  class="badge"
                  :class="getStatusBadgeClass(campaign.status)"
                >
                  {{ campaign.status_display }}
                </span>
              </div>

              <div class="mb-4">
                <h5 class="text-muted">Description</h5>
                <p class="lead">{{ campaign.description }}</p>
              </div>

              <div class="row mb-4">
                <div class="col-md-6">
                  <div class="detail-box p-3 mb-3 border rounded">
                    <i class="bi bi-camera-video text-primary me-2"></i>
                    <strong>Content Type:</strong>
                    <div class="mt-1">{{ campaign.content_type_display }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-box p-3 mb-3 border rounded">
                    <i class="bi bi-tag text-info me-2"></i>
                    <strong>Category:</strong>
                    <div class="mt-1">{{ campaign.category_display }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-box p-3 mb-3 border rounded">
                    <i class="bi bi-currency-euro text-success me-2"></i>
                    <strong>Budget:</strong>
                    <div class="mt-1">€{{ formatBudget(campaign.budget) }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-box p-3 mb-3 border rounded">
                    <i class="bi bi-calendar-event text-warning me-2"></i>
                    <strong>Deadline:</strong>
                    <div class="mt-1">{{ formatDate(campaign.deadline) }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-4">
                <h5 class="text-muted">Deliverables</h5>
                <p class="white-space-pre-line">{{ campaign.deliverables }}</p>
              </div>

              <div v-if="!isInfluencer" class="mb-3">
                <h5 class="text-muted">Brand</h5>
                <p><i class="bi bi-building me-2"></i>{{ campaign.brand_email }}</p>
              </div>

              <!-- Reference Files -->
              <div v-if="campaign.reference_files && campaign.reference_files.length > 0" class="mb-4">
                <h5 class="text-muted">Reference Materials</h5>
                <div class="list-group">
                  <a
                    v-for="file in campaign.reference_files"
                    :key="file.id"
                    :href="file.file"
                    target="_blank"
                    class="list-group-item list-group-item-action"
                  >
                    <i class="bi bi-file-earmark me-2"></i>
                    {{ getFileName(file.file) }}
                    <i class="bi bi-download float-end"></i>
                  </a>
                </div>
              </div>

              <div class="mt-4">
                <button class="btn btn-secondary" @click="$router.push('/campaigns')">
                  <i class="bi bi-arrow-left me-2"></i>Back to Campaigns
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Application Form Column (for Influencers) -->
        <div v-if="isInfluencer" class="col-lg-4">
          <div class="card shadow-sm sticky-top" style="top: 20px;">
            <div class="card-body">
              <h4 class="card-title mb-4">Apply to Campaign</h4>

              <!-- Success Message -->
              <div v-if="applicationSuccess" class="alert alert-success" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                Application submitted successfully! You will receive a confirmation email shortly.
              </div>

              <!-- Already Applied Message -->
              <div v-else-if="alreadyApplied" class="alert alert-info" role="alert">
                <i class="bi bi-info-circle me-2"></i>
                You have already applied to this campaign.
              </div>

              <!-- Application Form -->
              <form v-else @submit.prevent="submitApplication">
                <div class="mb-3">
                  <label for="pitch" class="form-label">
                    Your Pitch <span class="text-danger">*</span>
                  </label>
                  <textarea
                    id="pitch"
                    v-model="applicationForm.pitch"
                    class="form-control"
                    rows="5"
                    placeholder="Tell the brand why you're perfect for this campaign..."
                    required
                    :disabled="submitting"
                  ></textarea>
                  <div class="form-text">
                    Describe your content style, audience, and why you're a great fit.
                  </div>
                </div>

                <div class="mb-3">
                  <label for="portfolio_link" class="form-label">
                    Portfolio Link (Optional)
                  </label>
                  <input
                    id="portfolio_link"
                    v-model="applicationForm.portfolio_link"
                    type="url"
                    class="form-control"
                    placeholder="https://instagram.com/yourprofile"
                    :disabled="submitting"
                  />
                  <div class="form-text">
                    Link to your social media profile or portfolio.
                  </div>
                </div>

                <div class="mb-3">
                  <label for="proposed_price" class="form-label">
                    Proposed Price (Optional)
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">€</span>
                    <input
                      id="proposed_price"
                      v-model="applicationForm.proposed_price"
                      type="number"
                      step="0.01"
                      min="0.01"
                      class="form-control"
                      placeholder="220.00"
                      :disabled="submitting"
                    />
                  </div>
                  <div class="form-text">
                    Suggest your price if the budget is negotiable.
                  </div>
                </div>

                <!-- Error Message -->
                <div v-if="applicationError" class="alert alert-danger" role="alert">
                  {{ applicationError }}
                </div>

                <button
                  type="submit"
                  class="btn btn-primary w-100"
                  :disabled="submitting || !applicationForm.pitch.trim()"
                >
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                  {{ submitting ? 'Submitting...' : 'Submit Application' }}
                </button>
              </form>
            </div>
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
  } catch (error: any) {
    console.error('Error loading campaign:', error);
    errorMessage.value = 'Failed to load campaign details. Please try again later.';
  } finally {
    loading.value = false;
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
      return 'bg-success';
    case 'DRAFT':
      return 'bg-secondary';
    case 'CLOSED':
      return 'bg-danger';
    default:
      return 'bg-secondary';
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
.detail-box {
  background-color: #f8f9fa;
}

.sticky-top {
  position: sticky;
}

.white-space-pre-line {
  white-space: pre-line;
}
</style>
