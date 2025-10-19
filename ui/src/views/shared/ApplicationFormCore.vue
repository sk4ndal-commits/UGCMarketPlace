<template>
  <div>
    <!-- Name -->
    <div class="mb-4">
      <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
        Application Name <span class="text-red-600">*</span>
      </label>
      <input
        id="name"
        type="text"
        class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="errors.name ? 'border-red-500' : 'border-gray-300'"
        v-model="formData.name"
        required
        maxlength="200"
        placeholder="e.g., Customer Portal"
      />
      <div v-if="errors.name" class="text-red-600 text-sm mt-1">{{ errors.name }}</div>
    </div>

    <!-- Description -->
    <div class="mb-4">
      <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
        Description <span class="text-red-600">*</span>
      </label>
      <textarea
        id="description"
        class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="errors.description ? 'border-red-500' : 'border-gray-300'"
        v-model="formData.description"
        rows="4"
        required
        placeholder="Provide a detailed description of your application..."
      ></textarea>
      <div v-if="errors.description" class="text-red-600 text-sm mt-1">{{ errors.description }}</div>
    </div>

    <!-- Owner -->
    <div class="mb-4">
      <label for="owner" class="block text-sm font-medium text-gray-700 mb-1">
        Owner <span class="text-red-600">*</span>
      </label>
      <input
        id="owner"
        type="text"
        class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="errors.owner ? 'border-red-500' : 'border-gray-300'"
        v-model="formData.owner"
        required
        maxlength="200"
        placeholder="e.g., team-customer"
      />
      <div v-if="errors.owner" class="text-red-600 text-sm mt-1">{{ errors.owner }}</div>
    </div>

    <!-- Visibility -->
    <div class="mb-4">
      <label for="visibility" class="block text-sm font-medium text-gray-700 mb-1">
        Visibility <span class="text-red-600">*</span>
      </label>
      <select
        id="visibility"
        class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="errors.visibility ? 'border-red-500' : 'border-gray-300'"
        v-model="formData.visibility"
        required
      >
        <option value="">Select visibility...</option>
        <option v-for="option in visibilityChoices" :key="option.value" :value="option.value">{{ option.label }}</option>
      </select>
      <div v-if="errors.visibility" class="text-red-600 text-sm mt-1">{{ errors.visibility }}</div>
    </div>

    <!-- Template Selection -->
    <div class="mb-4">
      <label for="template_id" class="block text-sm font-medium text-gray-700 mb-1">
        Template (Optional)
      </label>
      <select
        id="template_id"
        class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="errors.template_id ? 'border-red-500' : 'border-gray-300'"
        v-model="formData.template_id"
        @change="$emit('template-change')"
      >
        <option value="">No template (free configuration)</option>
        <option v-for="template in templates" :key="template.id" :value="template.template_id">
          {{ template.name }} ({{ template.template_id }})
        </option>
      </select>
      <div v-if="errors.template_id" class="text-red-600 text-sm mt-1">{{ errors.template_id }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Template, CreatorApplicationFormData } from '../../models/application';

const { formData, errors, templates, visibilityChoices } = defineProps<{
  formData: CreatorApplicationFormData;
  errors: Record<string, string>;
  templates: Template[];
  visibilityChoices: { value: string; label: string }[];
}>();

const emits = defineEmits<['template-change']>();
</script>

<style scoped></style>
