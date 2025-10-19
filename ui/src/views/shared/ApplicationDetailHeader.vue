<template>
  <div class="mb-6">
    <div class="flex justify-between items-start mb-3">
      <div>
        <h4 class="text-2xl font-bold text-gray-800">{{ application.name }}</h4>
        <p class="text-sm text-gray-500 font-mono mt-1">{{ application.application_id }}</p>
      </div>
      <span class="px-3 py-1 text-sm font-medium rounded" :class="getVisibilityClass(application.visibility)">
        {{ application.visibility }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CreatorApplication } from '../../models/application';
const props = defineProps<{ application: CreatorApplication }>();
const { application } = props;

function getVisibilityClass(visibility: string): string {
  switch (visibility) {
    case 'PUBLIC':
      return 'bg-green-100 text-green-800';
    case 'INTERNAL':
      return 'bg-blue-100 text-blue-800';
    case 'PRIVATE':
      return 'bg-gray-100 text-gray-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}
</script>

<style scoped></style>
