<template>
  <div class="bg-white rounded-lg shadow-sm card-hover flex flex-col">
    <div class="p-5 flex-1">
      <div class="flex justify-between items-start mb-3">
        <h5 class="text-lg font-semibold flex-1">{{ campaign.title }}</h5>
        <span
          class="ml-2 px-2 py-1 text-xs font-semibold rounded"
          :class="getStatusBadgeClass(campaign.status)"
        >
          {{ campaign.status_display }}
        </span>
      </div>

      <p class="text-gray-500 text-sm mb-4">
        {{ truncateText(campaign.description, 100) }}
      </p>

      <div class="space-y-2">
        <div class="flex items-center text-sm">
          <span class="mr-2">🎥</span>
          <strong class="mr-1">Type:</strong> {{ campaign.content_type_display }}
        </div>
        <div class="flex items-center text-sm">
          <span class="mr-2 text-green-600">💰</span>
          <strong class="mr-1">Budget:</strong> €{{ formatBudget(campaign.budget) }}
        </div>
        <div class="flex items-center text-sm">
          <span class="mr-2 text-yellow-600">📅</span>
          <strong class="mr-1">Deadline:</strong> {{ formatDate(campaign.deadline) }}
        </div>
        <div v-if="!isBrand" class="flex items-center text-sm">
          <span class="mr-2 text-blue-600">🏢</span>
          <strong class="mr-1">Brand:</strong> {{ campaign.brand_email }}
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 p-4 flex justify-between items-center">
      <button
        class="px-3 py-1.5 text-sm border border-blue-500 text-blue-500 rounded hover:bg-blue-50 transition-colors"
        @click="$emit('view', campaign.id)"
      >
        <span class="mr-1">👁</span>View Details
      </button>

      <div v-if="isBrand" class="flex gap-2">
        <button
          class="px-3 py-1.5 text-sm border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors"
          @click="$emit('edit', campaign.id)"
        >
          ✏️
        </button>
        <button
          class="px-3 py-1.5 text-sm border border-red-500 text-red-500 rounded hover:bg-red-50 transition-colors"
          @click="$emit('delete', campaign)"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Campaign } from '../../models/campaign';
const { campaign, isBrand } = defineProps<{ campaign: Campaign; isBrand: boolean }>();

const formatBudget = (budget: string | number): string => {
  const amount = typeof budget === 'string' ? parseFloat(budget) : budget;
  return (amount || 0).toFixed(2);
};

const formatDate = (dateString: string): string => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const truncateText = (text: string, maxLength: number): string => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

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
</script>

<style scoped>
/* small local styles are fine; main layout is tailwind */
</style>
