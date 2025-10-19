<template>
  <div class="container mx-auto px-4 py-6 max-w-4xl">
    <div class="bg-white rounded-lg shadow-sm">
      <div class="bg-gradient-primary text-white p-5 rounded-t-lg">
        <div class="flex justify-between items-center">
          <h3 class="text-2xl font-bold">Application Details</h3>
          <button
            @click="$router.push('/applications')"
            class="px-4 py-2 bg-white text-purple-700 rounded-lg hover:bg-gray-100 transition font-medium"
          >
            ← Back to List
          </button>
        </div>
      </div>

  <div class="p-6">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-700"></div>
          <p class="mt-3 text-gray-600">Loading application...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ errorMessage }}
        </div>

        <!-- Application Details -->
        <div v-else-if="application">
          <ApplicationDetailHeader :application="application" />
          <ApplicationDetailContent :application="application" :formatDate="formatDate" />

          <!-- Actions (for creators who own the application) -->
          <div v-if="canEdit" class="flex gap-3 mt-6">
            <ApplicationActions @edit="editApplication" @delete="confirmDelete" />
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
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
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import applicationService from '../services/applicationService';
import ApplicationActions from './creator/ApplicationActions.vue';
import ApplicationDetailHeader from './shared/ApplicationDetailHeader.vue';
import ApplicationDetailContent from './shared/ApplicationDetailContent.vue';
import type { CreatorApplication } from '../models/application';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const loading = ref(false);
const errorMessage = ref('');
const application = ref<CreatorApplication | null>(null);
const showDeleteModal = ref(false);

const canEdit = computed(() => {
  return authStore.user?.role === 'CREATOR' && 
         application.value?.creator === authStore.user?.id;
});

/**
 * Load application on mount
 */
onMounted(async () => {
  await loadApplication();
});

/**
 * Load application details
 */
async function loadApplication() {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const id = parseInt(route.params.id as string);
    const response = await applicationService.getApplication(id);
    
    if (response.status === 'success' && !Array.isArray(response.data)) {
      application.value = response.data;
    } else {
      errorMessage.value = 'Failed to load application';
    }
  } catch (error: any) {
    console.error('Failed to load application:', error);
    errorMessage.value = error.response?.data?.message || 'Failed to load application';
  } finally {
    loading.value = false;
  }
}

/**
 * Edit application
 */
function editApplication() {
  router.push(`/applications/${route.params.id}/edit`);
}

/**
 * Show delete confirmation
 */
function confirmDelete() {
  showDeleteModal.value = true;
}

/**
 * Delete application
 */
async function deleteApplication() {
  if (!application.value?.id) return;
  
  try {
    const response = await applicationService.deleteApplication(application.value.id);
    if (response.status === 'success') {
      router.push('/applications');
    } else {
      errorMessage.value = 'Failed to delete application';
      showDeleteModal.value = false;
    }
  } catch (error: any) {
    console.error('Failed to delete application:', error);
    errorMessage.value = error.response?.data?.message || 'Failed to delete application';
    showDeleteModal.value = false;
  }
}

/**
 * Get visibility badge class
 */


/**
 * Format date for display
 */
function formatDate(dateString?: string): string {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
