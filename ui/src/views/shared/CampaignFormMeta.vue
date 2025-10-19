<template>
  <div>
    <!-- Content Type -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-1">Content Type <span class="text-red-600">*</span></label>
      <select class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.content_type ? 'border-red-500' : 'border-gray-300'" v-model="formData.content_type" required>
        <option value="">Select content type...</option>
        <option v-for="option in contentTypeChoices" :key="option.value" :value="option.value">{{ option.label }}</option>
      </select>
      <div v-if="errors.content_type" class="text-red-600 text-sm mt-1">{{ errors.content_type }}</div>
    </div>

    <!-- Category -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-1">Category <span class="text-red-600">*</span></label>
      <select class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.category ? 'border-red-500' : 'border-gray-300'" v-model="formData.category" required>
        <option value="">Select category...</option>
        <option v-for="option in categoryChoices" :key="option.value" :value="option.value">{{ option.label }}</option>
      </select>
      <div v-if="errors.category" class="text-red-600 text-sm mt-1">{{ errors.category }}</div>
    </div>

    <!-- Status -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-1">Status <span class="text-red-600">*</span></label>
      <select class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.status ? 'border-red-500' : 'border-gray-300'" v-model="formData.status" required>
        <option v-for="option in statusChoices" :key="option.value" :value="option.value">{{ option.label }}</option>
      </select>
      <div v-if="errors.status" class="text-red-600 text-sm mt-1">{{ errors.status }}</div>
      <small class="text-gray-500 text-sm">Campaign will only be visible to influencers when status is "Live"</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CampaignFormData } from '../../models/campaign';
const { formData, errors, contentTypeChoices, categoryChoices, statusChoices } = defineProps<{ formData: CampaignFormData; errors: Record<string,string>; contentTypeChoices: any[]; categoryChoices: any[]; statusChoices: any[] }>();
</script>

<style scoped></style>
