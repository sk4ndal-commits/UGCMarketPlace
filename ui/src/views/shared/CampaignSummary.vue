<template>
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
</template>

<script setup lang="ts">
import type { Campaign } from '../../models/campaign';
const props = defineProps<{ campaign: Campaign; isInfluencer: boolean }>();
const { campaign, isInfluencer } = props;

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
  const amount = typeof budget === 'string' ? parseFloat(budget) : (budget as number);
  return isNaN(amount) ? '0.00' : amount.toFixed(2);
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
</script>

<style scoped></style>
