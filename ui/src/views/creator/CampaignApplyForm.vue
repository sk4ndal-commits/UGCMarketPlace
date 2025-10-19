<template>
  <div class="bg-white rounded-lg shadow-sm p-6 sticky top-5">
    <h4 class="text-xl font-bold mb-4">Apply to Campaign</h4>

    <div v-if="applicationSuccess" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
      <p class="mb-2">Application submitted successfully!</p>
      <button @click="$router.push('/my-applications')" class="text-green-800 underline">View My Applications →</button>
    </div>

    <div v-else-if="alreadyApplied" class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-4">
      <p class="mb-2">You have already applied to this campaign.</p>
      <button @click="$router.push('/my-applications')" class="text-blue-800 underline">View My Applications →</button>
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
import type { ApplicationFormData } from '../../models/campaign';
import campaignService from '../../services/campaignService';

const props = defineProps<{ campaignId: number }>();

const form = ref<ApplicationFormData>({ campaign: props.campaignId, pitch: '', portfolio_link: '', proposed_price: undefined });
const submitting = ref(false);
const applicationSuccess = ref(false);
const alreadyApplied = ref(false);
const applicationError = ref('');

const submitApplication = async () => {
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
</script>

<style scoped></style>
