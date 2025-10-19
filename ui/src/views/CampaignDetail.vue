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
          <CampaignSummary :campaign="campaign" :isInfluencer="isInfluencer" />
        </div>

        <!-- Application Form Column (for Influencers) -->
        <div v-if="isInfluencer" class="lg:col-span-1">
          <CampaignApplyForm :campaignId="campaign?.id || 0" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import campaignService from '../services/campaignService';
import CampaignApplyForm from './creator/CampaignApplyForm.vue';
import CampaignSummary from './shared/CampaignSummary.vue';
import type { Campaign } from '../models/campaign';

const route = useRoute();
const authStore = useAuthStore();

const campaign = ref<Campaign | null>(null);
const loading = ref(true);
const errorMessage = ref('');

const isInfluencer = computed(() => authStore.user?.role === 'INFLUENCER');

const loadCampaign = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
  const campaignId = parseInt(route.params.id as string);
  const response = await campaignService.getCampaign(campaignId);
  campaign.value = response.data as Campaign;
    
    // Creator/applicant interactions are handled by the CampaignApplyForm component
  } catch (error: any) {
    console.error('Error loading campaign:', error);
    errorMessage.value = 'Failed to load campaign details. Please try again later.';
  } finally {
    loading.value = false;
  }
};

// application interactions moved into CampaignApplyForm component

// helper logic moved to shared/CampaignSummary.vue

onMounted(() => {
  loadCampaign();
});
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
