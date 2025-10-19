<template>
  <div class="container mx-auto px-4 py-6 max-w-7xl">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Available Campaigns</h2>
    </div>

    <!-- Filters for Influencers -->
    <div class="bg-white rounded-lg shadow-sm p-5 mb-6">
      <div class="flex justify-between items-center mb-4">
        <h5 class="text-lg font-semibold">
          <span class="mr-2">🔍</span>Filter Campaigns
        </h5>
        <button
          v-if="hasActiveFilters"
          class="px-3 py-1.5 text-sm border border-gray-300 rounded hover:bg-gray-50 transition-colors"
          @click="clearFilters"
        >
          <span class="mr-1">✖</span>Clear Filters
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Budget Range -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Budget Range</label>
          <div class="flex items-center gap-2">
            <div class="flex items-center border border-gray-300 rounded">
              <span class="px-2 text-sm text-gray-600 bg-gray-50">€</span>
              <input
                v-model="filters.budget_min"
                type="number"
                class="w-20 px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r"
                placeholder="Min"
                min="0"
                step="1"
              />
            </div>
            <span class="text-gray-500">-</span>
            <div class="flex items-center border border-gray-300 rounded">
              <span class="px-2 text-sm text-gray-600 bg-gray-50">€</span>
              <input
                v-model="filters.budget_max"
                type="number"
                class="w-20 px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r"
                placeholder="Max"
                min="0"
                step="1"
              />
            </div>
          </div>
        </div>

        <!-- Category -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select v-model="filters.category" class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">All Categories</option>
            <option
              v-for="category in categoryChoices"
              :key="category.value"
              :value="category.value"
            >
              {{ category.label }}
            </option>
          </select>
        </div>

        <!-- Platform/Content Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Platform</label>
          <select v-model="filters.content_type" class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">All Platforms</option>
            <option
              v-for="contentType in contentTypeChoices"
              :key="contentType.value"
              :value="contentType.value"
            >
              {{ contentType.label }}
            </option>
          </select>
        </div>

        <!-- Deadline -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Deadline Before</label>
          <input
            v-model="filters.deadline_before"
            type="date"
            class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div class="mt-4">
        <button
          class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity text-sm"
          @click="applyFilters"
        >
          <span class="mr-1">🔍</span>Apply Filters
        </button>
      </div>
    </div>

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

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <CampaignCard
        v-for="campaign in campaigns"
        :key="campaign.id"
        :campaign="campaign"
        :isBrand="false"
        @view="viewCampaign"
        @edit="editCampaign"
        @delete="confirmDelete"
      />
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
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import campaignService from '../../services/campaignService';
import type { Campaign, CampaignFilters } from '../../models/campaign';
import CampaignCard from '../shared/CampaignCard.vue';

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
const filters = ref<CampaignFilters>({
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
    const filterParams: CampaignFilters = {};
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

const hasActiveFilters = computed(() => {
  return !!(
    filters.value.budget_min ||
    filters.value.budget_max ||
    filters.value.category ||
    filters.value.content_type ||
    filters.value.deadline_before
  );
});

const applyFilters = () => {
  loadCampaigns(true);
};

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

// No-op references to satisfy TypeScript usage checks when template usage isn't picked up
// (template uses these symbols; referencing them here prevents TS6133 errors)
void CampaignCard;
void categoryChoices;
void contentTypeChoices;
void hasActiveFilters;
void applyFilters;
void clearFilters;
void viewCampaign;
void editCampaign;
void confirmDelete;
void deleteCampaign;
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>


*** End Patch