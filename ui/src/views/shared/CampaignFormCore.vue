<template>
  <div>
    <!-- Title -->
    <div class="mb-4">
      <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title <span class="text-red-600">*</span></label>
      <input id="title" type="text" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.title ? 'border-red-500' : 'border-gray-300'" v-model="formData.title" required maxlength="200" placeholder="e.g., UGC Reel for Vegan Skincare Product" />
      <div v-if="errors.title" class="text-red-600 text-sm mt-1">{{ errors.title }}</div>
    </div>

    <!-- Description -->
    <div class="mb-4">
      <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description <span class="text-red-600">*</span></label>
      <textarea id="description" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.description ? 'border-red-500' : 'border-gray-300'" v-model="formData.description" rows="4" required placeholder="Provide a detailed description of your campaign requirements..."></textarea>
      <div v-if="errors.description" class="text-red-600 text-sm mt-1">{{ errors.description }}</div>
    </div>

    <!-- Deliverables -->
    <div class="mb-4">
      <label for="deliverables" class="block text-sm font-medium text-gray-700 mb-1">Deliverables <span class="text-red-600">*</span></label>
      <textarea id="deliverables" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.deliverables ? 'border-red-500' : 'border-gray-300'" v-model="formData.deliverables" rows="3" required placeholder="e.g., 1 Instagram Reel (30-60 seconds), 3 story frames"></textarea>
      <div v-if="errors.deliverables" class="text-red-600 text-sm mt-1">{{ errors.deliverables }}</div>
    </div>

    <!-- Budget -->
    <div class="mb-4">
      <label for="budget" class="block text-sm font-medium text-gray-700 mb-1">Budget (EUR) <span class="text-red-600">*</span></label>
      <input id="budget" type="number" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.budget ? 'border-red-500' : 'border-gray-300'" v-model.number="formData.budget" step="0.01" min="0.01" required placeholder="250.00" />
      <div v-if="errors.budget" class="text-red-600 text-sm mt-1">{{ errors.budget }}</div>
      <small class="text-gray-500 text-sm">Budget must be greater than 0</small>
    </div>

    <!-- Deadline -->
    <div class="mb-4">
      <label for="deadline" class="block text-sm font-medium text-gray-700 mb-1">Deadline <span class="text-red-600">*</span></label>
      <input id="deadline" type="date" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" :class="errors.deadline ? 'border-red-500' : 'border-gray-300'" v-model="formData.deadline" :min="minDate" required />
      <div v-if="errors.deadline" class="text-red-600 text-sm mt-1">{{ errors.deadline }}</div>
      <small class="text-gray-500 text-sm">Deadline must be a future date</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CampaignFormData } from '../../models/campaign';
const { formData, errors, minDate } = defineProps<{ formData: CampaignFormData; errors: Record<string,string>; minDate?: string }>();
</script>

<style scoped></style>
