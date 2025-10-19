<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12">
        <h2 class="mb-4">
          {{ isBrand ? 'Campaign Applications' : 'My Applications' }}
        </h2>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3">Loading applications...</p>
        </div>

        <!-- Error Message -->
        <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>

        <!-- Empty State -->
        <div v-else-if="applications.length === 0" class="text-center py-5">
          <i class="bi bi-inbox" style="font-size: 4rem; color: #ccc;"></i>
          <h4 class="mt-3">No applications found</h4>
          <p class="text-muted">
            {{ isBrand 
              ? 'Applications to your campaigns will appear here.' 
              : 'You haven\'t applied to any campaigns yet.' 
            }}
          </p>
          <button
            v-if="!isBrand"
            class="btn btn-primary mt-3"
            @click="$router.push('/campaigns')"
          >
            Browse Campaigns
          </button>
        </div>

        <!-- Applications List -->
        <div v-else>
          <div class="row">
            <div
              v-for="application in applications"
              :key="application.id"
              class="col-12 mb-3"
            >
              <div class="card shadow-sm application-card">
                <div class="card-body">
                  <div class="row">
                    <!-- Application Info -->
                    <div class="col-lg-8">
                      <div class="d-flex justify-content-between align-items-start mb-3">
                        <h5 class="card-title mb-0">
                          <i class="bi bi-megaphone me-2 text-primary"></i>
                          {{ application.campaign_title }}
                        </h5>
                        <span
                          class="badge"
                          :class="getStatusBadgeClass(application.status)"
                        >
                          {{ application.status_display }}
                        </span>
                      </div>

                      <div class="mb-3">
                        <h6 class="text-muted mb-2">Pitch</h6>
                        <p class="mb-0">{{ application.pitch }}</p>
                      </div>

                      <div class="row">
                        <div v-if="application.portfolio_link" class="col-md-6 mb-2">
                          <strong>Portfolio:</strong>
                          <a 
                            :href="application.portfolio_link" 
                            target="_blank" 
                            class="ms-2"
                          >
                            <i class="bi bi-link-45deg"></i>
                            View Portfolio
                          </a>
                        </div>
                        <div v-if="application.proposed_price" class="col-md-6 mb-2">
                          <strong>Proposed Price:</strong>
                          <span class="ms-2 text-success">
                            €{{ formatPrice(application.proposed_price) }}
                          </span>
                        </div>
                        <div v-if="isBrand" class="col-md-6 mb-2">
                          <strong>Influencer:</strong>
                          <span class="ms-2">{{ application.influencer_email }}</span>
                        </div>
                        <div class="col-md-6 mb-2">
                          <strong>Submitted:</strong>
                          <span class="ms-2">{{ formatDate(application.created_at!) }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- Actions -->
                    <div class="col-lg-4 d-flex flex-column justify-content-center">
                      <button
                        class="btn btn-outline-primary mb-2"
                        @click="viewCampaign(application.campaign)"
                      >
                        <i class="bi bi-eye me-2"></i>View Campaign
                      </button>
                      
                      <button
                        v-if="!isBrand"
                        class="btn btn-outline-secondary"
                        @click="viewApplication(application.id!)"
                      >
                        <i class="bi bi-file-text me-2"></i>View Details
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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
      return 'bg-warning';
    case 'SHORTLISTED':
      return 'bg-info';
    case 'ACCEPTED':
      return 'bg-success';
    case 'REJECTED':
      return 'bg-danger';
    default:
      return 'bg-secondary';
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

onMounted(() => {
  loadApplications();
});
</script>

<style scoped>
.application-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.application-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
