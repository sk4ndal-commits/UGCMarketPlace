<template>
  <div class="border border-gray-200 rounded-lg p-5 hover:shadow-md transition cursor-pointer" @click="onView">
    <!-- Application Header -->
    <div class="flex justify-between items-start mb-3">
      <h4 class="text-lg font-semibold text-gray-800 flex-1">{{ app.name }}</h4>
      <span
        class="px-2 py-1 text-xs font-medium rounded"
        :class="getVisibilityClass(app.visibility)"
      >
        {{ app.visibility }}
      </span>
    </div>

    <!-- Application ID -->
    <p class="text-xs text-gray-500 mb-2 font-mono">{{ app.application_id }}</p>

    <!-- Description -->
    <p class="text-sm text-gray-600 mb-3 line-clamp-2">{{ app.description }}</p>

    <!-- Metadata -->
    <div class="space-y-1 text-xs text-gray-500">
      <div class="flex items-center">
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>Owner: {{ app.owner }}</span>
      </div>
      <div v-if="app.template_details" class="flex items-center">
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
        </svg>
        <span>Template: {{ app.template_details?.name }}</span>
      </div>
      <div class="flex items-center">
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>Created: {{ formatDate(app.created_at) }}</span>
      </div>
    </div>

    <!-- Actions (for creators) -->
    <div v-if="isCreator && app.creator === currentUserId" class="mt-4 flex gap-2">
      <button
        @click.stop="onEdit"
        class="flex-1 px-3 py-1.5 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition"
      >
        Edit
      </button>
      <button
        @click.stop="showDeleteModal = true"
        class="flex-1 px-3 py-1.5 text-sm bg-red-500 text-white rounded hover:bg-red-600 transition"
      >
        Delete
      </button>
    </div>

    <!-- Delete Confirmation Modal (local to item) -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-3">Delete Application</h3>
        <p class="text-gray-600 mb-6">
          Are you sure you want to delete this application? This action cannot be undone.
        </p>
        <div class="flex gap-3 justify-end">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition"
          >
            Cancel
          </button>
          <button
            @click="deleteApplication"
            class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import applicationService from '../../services/applicationService';
import type { CreatorApplication } from '../../models/application';

const props = defineProps<{
  app: CreatorApplication;
  isCreator: boolean;
  currentUserId?: number | null;
}>();

const emits = defineEmits<{
  (e: 'view', id: number): void;
  (e: 'edit', id: number): void;
  (e: 'deleted', id: number): void;
}>();

const showDeleteModal = ref(false);
const isDeleting = ref(false);
const deletionError = ref('');

function onView() {
  emits('view', props.app.id!);
}

function onEdit() {
  emits('edit', props.app.id!);
}

async function deleteApplication() {
  if (!props.app.id) return;
  isDeleting.value = true;
  deletionError.value = '';
  try {
    const resp = await applicationService.deleteApplication(props.app.id);
    if (resp.status === 'success') {
      emits('deleted', props.app.id);
    } else {
      deletionError.value = 'Failed to delete application';
    }
  } catch (err: any) {
    deletionError.value = err.response?.data?.message || 'Failed to delete application';
  } finally {
    isDeleting.value = false;
    showDeleteModal.value = false;
  }
}

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

function formatDate(dateString?: string): string {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* standard property for newer browsers */
  line-clamp: 2;
}
</style>
