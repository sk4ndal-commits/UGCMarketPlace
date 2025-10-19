<template>
  <div class="bg-white rounded-lg shadow-sm p-6 sticky top-5">
    <h4 class="text-xl font-bold mb-4">Apply to Campaign</h4>

    <div v-if="applicationSuccess" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
      <p class="mb-2">Application submitted successfully!</p>
      <button @click="$router.push('/my-applications')" class="text-green-800 underline">View My Applications →</button>
    </div>

    <div v-else-if="alreadyApplied" class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-4">
      <p class="mb-2">You have already applied to this campaign.</p>
      <div class="flex items-center gap-3">
        <button v-if="existingApplicationId" @click="$router.push(`/applications/${existingApplicationId}`)" class="text-blue-800 underline">View your application →</button>
        <button v-else @click="$router.push('/my-applications')" class="text-blue-800 underline">View My Applications →</button>
      </div>
    </div>

    <div v-else-if="isBrandOwner" class="bg-yellow-50 border border-yellow-300 text-yellow-800 px-4 py-3 rounded mb-4">
      <p class="mb-2">You are the owner of this campaign and cannot apply as a creator.</p>
      <button @click="$router.push(`/campaigns/${props.campaignId}/edit`)" class="text-yellow-800 underline">Edit Campaign →</button>
    </div>

    <form v-else @submit.prevent="submitApplication">
      <div class="mb-4">
        <label for="pitch" class="block text-sm font-medium text-gray-700 mb-1">Your Pitch <span class="text-red-600">*</span></label>
        <textarea id="pitch" v-model="form.pitch" rows="5" class="w-full px-3 py-2 border rounded" required></textarea>
      </div>

      <div class="mb-4">
        <label for="portfolio_link" class="block text-sm font-medium text-gray-700 mb-1">Portfolio Link (Optional)</label>
        <input id="portfolio_link" v-model="form.portfolio_link" type="url" class="w-full px-3 py-2 border rounded" />
      </div>

      <div class="mb-4">
        <label for="proposed_price" class="block text-sm font-medium text-gray-700 mb-1">Proposed Price (Optional)</label>
        <div class="flex items-center border rounded">
          <span class="px-3 text-gray-600 bg-gray-50">€</span>
          <input id="proposed_price" v-model="form.proposed_price" type="number" step="0.01" class="flex-1 px-3 py-2" />
        </div>
      </div>

      <div v-if="applicationError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{{ applicationError }}</div>

      <button type="submit" class="w-full bg-gradient-primary text-white py-2 rounded" :disabled="submitting">
        {{ submitting ? 'Submitting...' : 'Submit Application' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { onMounted } from 'vue';
import type { ApplicationFormData } from '../../models/campaign';
import campaignService from '../../services/campaignService';
import { useAuthStore } from '../../stores/authStore';

const props = defineProps<{ campaignId: number }>();

const authStore = useAuthStore();

const form = ref<ApplicationFormData>({ campaign: props.campaignId, pitch: '', portfolio_link: '', proposed_price: undefined });
const submitting = ref(false);
const applicationSuccess = ref(false);
const alreadyApplied = ref(false);
const existingApplicationId = ref<number | null>(null);
const isBrandOwner = ref(false);
const applicationError = ref('');

const submitApplication = async () => {
  // Prevent submission if brand owner or already applied
  if (isBrandOwner.value) {
    applicationError.value = 'Brand owners cannot apply to their own campaign.';
    return;
  }

  if (alreadyApplied.value) {
    applicationError.value = 'You have already applied to this campaign.';
    return;
  }

  submitting.value = true;
  applicationError.value = '';
  try {
    await campaignService.createApplication(form.value);
    applicationSuccess.value = true;
  } catch (err: any) {
    applicationError.value = err.response?.data?.message || 'Failed to submit application';
  } finally {
    submitting.value = false;
  }
};

onMounted(async () => {
  // Fetch campaign to check owner/brand
  try {
    const resp = await campaignService.getCampaign(props.campaignId);
    const campaign = resp.data as any;
    // campaign may have a `brand` or `owner` field; try common names
    const ownerId = (campaign.brand ?? campaign.owner ?? campaign.created_by ?? null) as number | null;
    if (ownerId && authStore.user?.id === ownerId) {
      isBrandOwner.value = true;
      return; // brand owners shouldn't apply, no need to check further
    }
  } catch (err) {
    // ignore — we will still try to fetch applications
    console.warn('Failed to load campaign for apply-form checks', err);
  }

  // Fetch user's applications to see if already applied
  try {
    const appsResp = await campaignService.getApplications();
    const apps = Array.isArray(appsResp.data) ? appsResp.data : [appsResp.data];
    const existing = apps.find((a: any) => a.campaign === props.campaignId && a.creator === authStore.user?.id);
    if (existing) {
      alreadyApplied.value = true;
      existingApplicationId.value = existing.id ?? null;
    }
  } catch (err) {
    console.warn('Failed to load applications for apply-form checks', err);
  }
});
</script>

<style scoped></style>
