<template>
  <div v-if="!isBrand" class="bg-white rounded-lg shadow-sm p-5 mb-6">
    <div class="flex justify-between items-center mb-4">
      <h5 class="text-lg font-semibold">
        <span class="mr-2">🔍</span>Filter Campaigns
      </h5>
      <button v-if="hasActiveFilters" class="px-3 py-1.5 text-sm border border-gray-300 rounded hover:bg-gray-50 transition-colors" @click="$emit('clear')">
        <span class="mr-1">✖</span>Clear Filters
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Budget Range</label>
        <div class="flex items-center gap-2">
          <div class="flex items-center border border-gray-300 rounded">
            <span class="px-2 text-sm text-gray-600 bg-gray-50">€</span>
            <input v-model="localFilters.budget_min" type="number" class="w-20 px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r" placeholder="Min" min="0" step="1" />
          </div>
          <span class="text-gray-500">-</span>
          <div class="flex items-center border border-gray-300 rounded">
            <span class="px-2 text-sm text-gray-600 bg-gray-50">€</span>
            <input v-model="localFilters.budget_max" type="number" class="w-20 px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r" placeholder="Max" min="0" step="1" />
          </div>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
        <select v-model="localFilters.category" class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">All Categories</option>
          <option v-for="category in categoryChoices" :key="category.value" :value="category.value">{{ category.label }}</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Platform</label>
        <select v-model="localFilters.content_type" class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">All Platforms</option>
          <option v-for="ct in contentTypeChoices" :key="ct.value" :value="ct.value">{{ ct.label }}</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Deadline Before</label>
        <input v-model="localFilters.deadline_before" type="date" class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
    </div>

    <div class="mt-4">
      <button class="bg-gradient-primary text-white font-medium py-2 px-4 rounded-lg hover:opacity-90 transition-opacity text-sm" @click="$emit('apply', localFilters)">
        <span class="mr-1">🔍</span>Apply Filters
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue';
import type { CampaignFilters } from '../../models/campaign';
const props = defineProps<{ filters: CampaignFilters; categoryChoices: any[]; contentTypeChoices: any[]; isBrand: boolean }>();
const emits = defineEmits(['apply', 'clear']);

const localFilters = reactive({ ...(props.filters || {}) });

const hasActiveFilters = computed(() => {
  return !!(localFilters.budget_min || localFilters.budget_max || localFilters.category || localFilters.content_type || localFilters.deadline_before);
});

watch(() => props.filters, (v) => {
  Object.assign(localFilters, v || {});
});
</script>

<style scoped></style>
