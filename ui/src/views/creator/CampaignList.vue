<template>
  <div class="container mx-auto px-4 py-6 max-w-7xl">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Available Campaigns</h2>
    </div>

    <CampaignFilters :filters="filters" :categoryChoices="categoryChoices" :contentTypeChoices="contentTypeChoices" :isBrand="false" @apply="loadCampaigns" @clear="clearFilters" />

    <!-- Loading/Error/Empty/Results handled like brand view but with isBrand=false -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-600">Loading campaigns...</p>
    </div>

    <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ errorMessage }}
    </div>

    <div v-else-if="campaigns.length === 0" class="text-center py-12">
      <div class="text-6xl text-gray-300 mb-4">📭</div>
      <h4 class="text-xl font-semibold mb-2">No campaigns found</h4>
      <p class="text-gray-500 mb-4">Check back later for new opportunities.</p>
    </div>

    <div v-else>
      <CampaignCardsGrid :campaigns="campaigns" :isBrand="false" @view="viewCampaign" @edit="editCampaign" @delete="confirmDelete" />
    </div>

    <!-- Delete modal same as brand -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4">
        <div class="flex justify-between items-center p-5 border-b">
          <h5 class="text-lg font-semibold">Confirm Delete</h5>
          <button
            type="button"
            class="text-gray-400 hover:text-gray-600 text-2xl leading-none"
            @click="showDeleteModal = false"
          >
            &times;
          </button>
        </div>
        <div class="p-5">
          <p class="mb-3">Are you sure you want to delete the campaign "{{ campaignToDelete?.title }}"?</p>
          <p class="text-red-600 font-semibold">This action cannot be undone.</p>
        </div>
        <div class="flex justify-end gap-3 p-5 border-t">
          <button
            type="button"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
            @click="showDeleteModal = false"
          >
            Cancel
          </button>
          <button
            type="button"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors disabled:opacity-50"
            @click="deleteCampaign"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
            {{ isDeleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import campaignService from '../../services/campaignService';
import type { Campaign, CampaignFilters as CampaignFiltersType } from '../../models/campaign';
import CampaignFilters from '../shared/CampaignFilters.vue';
import CampaignCardsGrid from '../shared/CampaignCardsGrid.vue';

const router = useRouter();
// authStore intentionally not used directly in script; kept for future role checks
// const authStore = useAuthStore();

const campaigns = ref<Campaign[]>([]);
const loading = ref(true);
const errorMessage = ref('');
const showDeleteModal = ref(false);
const campaignToDelete = ref<Campaign | null>(null);
const isDeleting = ref(false);

// Filter state
const filters = ref<CampaignFiltersType>({
  budget_min: undefined,
  budget_max: undefined,
  category: '',
  content_type: '',
  deadline_before: '',
});

const categoryChoices = campaignService.getCategoryChoices();
const contentTypeChoices = campaignService.getContentTypeChoices();

const loadCampaigns = async (applyFilters = false) => {
  loading.value = true;
  errorMessage.value = '';
  try {
  const filterParams: CampaignFiltersType = {};
    if (applyFilters) {
      if (filters.value.budget_min) filterParams.budget_min = Number(filters.value.budget_min);
      if (filters.value.budget_max) filterParams.budget_max = Number(filters.value.budget_max);
      if (filters.value.category) filterParams.category = filters.value.category;
      if (filters.value.content_type) filterParams.content_type = filters.value.content_type;
      if (filters.value.deadline_before) filterParams.deadline_before = filters.value.deadline_before;
    }
    const response = await campaignService.getCampaigns(applyFilters ? filterParams : undefined);
    campaigns.value = Array.isArray(response.data) ? response.data : [response.data];
  } catch (error: any) {
    console.error('Error loading campaigns:', error);
    errorMessage.value = 'Failed to load campaigns. Please try again later.';
  } finally {
    loading.value = false;
  }
};

// hasActiveFilters and applyFilters are handled inside CampaignFilters component now

const clearFilters = () => {
  filters.value = {
    budget_min: undefined,
    budget_max: undefined,
    category: '',
    content_type: '',
    deadline_before: '',
  };
  loadCampaigns(false);
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

onMounted(() => {
  loadCampaigns();
});

void categoryChoices;
void contentTypeChoices;
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>


*** End Patch