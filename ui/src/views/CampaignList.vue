<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>{{ isBrand ? 'My Campaigns' : 'Available Campaigns' }}</h2>
          <button
            v-if="isBrand"
            class="btn btn-primary"
            @click="$router.push('/campaigns/create')"
          >
            <i class="bi bi-plus-circle me-2"></i>Create Campaign
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3">Loading campaigns...</p>
        </div>

        <!-- Error Message -->
        <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>

        <!-- Empty State -->
        <div v-else-if="campaigns.length === 0" class="text-center py-5">
          <i class="bi bi-inbox" style="font-size: 4rem; color: #ccc;"></i>
          <h4 class="mt-3">No campaigns found</h4>
          <p class="text-muted">
            {{ isBrand ? 'Create your first campaign to get started!' : 'Check back later for new opportunities.' }}
          </p>
          <button
            v-if="isBrand"
            class="btn btn-primary mt-3"
            @click="$router.push('/campaigns/create')"
          >
            Create Campaign
          </button>
        </div>

        <!-- Campaigns List -->
        <div v-else class="row">
          <div
            v-for="campaign in campaigns"
            :key="campaign.id"
            class="col-md-6 col-lg-4 mb-4"
          >
            <div class="card h-100 shadow-sm campaign-card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <h5 class="card-title mb-0">{{ campaign.title }}</h5>
                  <span
                    class="badge"
                    :class="getStatusBadgeClass(campaign.status)"
                  >
                    {{ campaign.status_display }}
                  </span>
                </div>
                
                <p class="card-text text-muted small mb-3">
                  {{ truncateText(campaign.description, 100) }}
                </p>

                <div class="campaign-details">
                  <div class="detail-item mb-2">
                    <i class="bi bi-camera-video me-2 text-primary"></i>
                    <strong>Type:</strong> {{ campaign.content_type_display }}
                  </div>
                  <div class="detail-item mb-2">
                    <i class="bi bi-currency-euro me-2 text-success"></i>
                    <strong>Budget:</strong> €{{ formatBudget(campaign.budget) }}
                  </div>
                  <div class="detail-item mb-2">
                    <i class="bi bi-calendar-event me-2 text-warning"></i>
                    <strong>Deadline:</strong> {{ formatDate(campaign.deadline) }}
                  </div>
                  <div v-if="!isBrand" class="detail-item mb-2">
                    <i class="bi bi-building me-2 text-info"></i>
                    <strong>Brand:</strong> {{ campaign.brand_email }}
                  </div>
                </div>
              </div>

              <div class="card-footer bg-transparent">
                <div class="d-flex justify-content-between">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="viewCampaign(campaign.id!)"
                  >
                    <i class="bi bi-eye me-1"></i>View Details
                  </button>
                  
                  <div v-if="isBrand" class="btn-group">
                    <button
                      class="btn btn-sm btn-outline-secondary"
                      @click="editCampaign(campaign.id!)"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button
                      class="btn btn-sm btn-outline-danger"
                      @click="confirmDelete(campaign)"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background-color: rgba(0,0,0,0.5);"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button
              type="button"
              class="btn-close"
              @click="showDeleteModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete the campaign "{{ campaignToDelete?.title }}"?</p>
            <p class="text-danger mb-0">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showDeleteModal = false"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              @click="deleteCampaign"
              :disabled="isDeleting"
            >
              <span v-if="isDeleting" class="spinner-border spinner-border-sm me-2"></span>
              {{ isDeleting ? 'Deleting...' : 'Delete' }}
            </button>
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
import campaignService, { type Campaign } from '../services/campaignService';

const router = useRouter();
const authStore = useAuthStore();

const campaigns = ref<Campaign[]>([]);
const loading = ref(true);
const errorMessage = ref('');
const showDeleteModal = ref(false);
const campaignToDelete = ref<Campaign | null>(null);
const isDeleting = ref(false);

const isBrand = computed(() => authStore.user?.role === 'BRAND');

const loadCampaigns = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await campaignService.getCampaigns();
    campaigns.value = Array.isArray(response.data) ? response.data : [response.data];
  } catch (error: any) {
    console.error('Error loading campaigns:', error);
    errorMessage.value = 'Failed to load campaigns. Please try again later.';
  } finally {
    loading.value = false;
  }
};

const viewCampaign = (id: number) => {
  router.push(`/campaigns/${id}`);
};

const editCampaign = (id: number) => {
  router.push(`/campaigns/${id}/edit`);
};

const confirmDelete = (campaign: Campaign) => {
  campaignToDelete.value = campaign;
  showDeleteModal.value = true;
};

const deleteCampaign = async () => {
  if (!campaignToDelete.value?.id) return;
  
  isDeleting.value = true;
  
  try {
    await campaignService.deleteCampaign(campaignToDelete.value.id);
    campaigns.value = campaigns.value.filter(c => c.id !== campaignToDelete.value?.id);
    showDeleteModal.value = false;
    campaignToDelete.value = null;
  } catch (error: any) {
    console.error('Error deleting campaign:', error);
    errorMessage.value = 'Failed to delete campaign. Please try again.';
  } finally {
    isDeleting.value = false;
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
    month: 'short',
    day: 'numeric',
  });
};

const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

onMounted(() => {
  loadCampaigns();
});
</script>

<style scoped>
.campaign-card {
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 8px;
}

.campaign-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.card-title {
  color: #333;
  font-weight: 600;
}

.detail-item {
  font-size: 0.9rem;
  color: #555;
}

.detail-item i {
  width: 20px;
}

.modal.show {
  display: block;
}

.btn-group .btn {
  padding: 0.25rem 0.5rem;
}
</style>
