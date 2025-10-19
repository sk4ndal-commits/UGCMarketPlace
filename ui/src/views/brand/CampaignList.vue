<template>
  <div class="container mx-auto px-4 py-6 max-w-7xl">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">My Campaigns</h2>
      <button
        class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity"
        @click="$router.push('/campaigns/create')"
      >
        <span class="mr-2">➕</span>Create Campaign
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-600">Loading campaigns...</p>
    </div>

    <!-- Error Message -->
    <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ errorMessage }}
    </div>

    <!-- Empty State -->
    <div v-else-if="campaigns.length === 0" class="text-center py-12">
      <div class="text-6xl text-gray-300 mb-4">📭</div>
      <h4 class="text-xl font-semibold mb-2">No campaigns found</h4>
      <p class="text-gray-500 mb-4">Create your first campaign to get started!</p>
      <button
        class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity"
        @click="$router.push('/campaigns/create')"
      >
        Create Campaign
      </button>
    </div>

    <!-- Campaigns List -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <CampaignCard
        v-for="campaign in campaigns"
        :key="campaign.id"
        :campaign="campaign"
        :isBrand="true"
        @view="viewCampaign"
        @edit="editCampaign"
        @delete="confirmDelete"
      />
    </div>

    <!-- Delete Confirmation Modal -->
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
import type { Campaign } from '../../models/campaign';
import CampaignCard from '../shared/CampaignCard.vue';

const router = useRouter();

const campaigns = ref<Campaign[]>([]);
const loading = ref(true);
const errorMessage = ref('');
const showDeleteModal = ref(false);
const campaignToDelete = ref<Campaign | null>(null);
const isDeleting = ref(false);

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

onMounted(() => {
  loadCampaigns();
});
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>

*** End Patch