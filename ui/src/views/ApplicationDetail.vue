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
          <!-- Application Header -->
          <div class="mb-6">
            <div class="flex justify-between items-start mb-3">
              <div>
                <h4 class="text-2xl font-bold text-gray-800">{{ application.name }}</h4>
                <p class="text-sm text-gray-500 font-mono mt-1">{{ application.application_id }}</p>
              </div>
              <span
                class="px-3 py-1 text-sm font-medium rounded"
                :class="getVisibilityClass(application.visibility)"
              >
                {{ application.visibility }}
              </span>
            </div>
          </div>

          <!-- Description -->
          <div class="mb-6">
            <h5 class="text-lg font-semibold text-gray-700 mb-2">Description</h5>
            <p class="text-gray-600">{{ application.description }}</p>
          </div>

          <!-- Basic Information -->
          <div class="mb-6">
            <h5 class="text-lg font-semibold text-gray-700 mb-3">Basic Information</h5>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">Owner</label>
                <p class="text-gray-800">{{ application.owner }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Visibility</label>
                <p class="text-gray-800">{{ application.visibility }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Created</label>
                <p class="text-gray-800">{{ formatDate(application.created_at) }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Last Updated</label>
                <p class="text-gray-800">{{ formatDate(application.updated_at) }}</p>
              </div>
            </div>
          </div>

          <!-- Template Information -->
          <div v-if="application.template_details" class="mb-6">
            <h5 class="text-lg font-semibold text-gray-700 mb-3">Template</h5>
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="font-medium text-gray-800">{{ application.template_details.name }}</p>
              <p class="text-sm text-gray-600 mt-1">{{ application.template_details.description }}</p>
              <p class="text-xs text-gray-500 font-mono mt-2">{{ application.template_details.template_id }}</p>
            </div>
          </div>

          <!-- Parameters -->
          <div v-if="application.parameters && Object.keys(application.parameters).length > 0" class="mb-6">
            <h5 class="text-lg font-semibold text-gray-700 mb-3">Parameters</h5>
            <pre class="bg-gray-50 rounded-lg p-4 overflow-x-auto text-sm">{{ JSON.stringify(application.parameters, null, 2) }}</pre>
          </div>

          <!-- Git Integration -->
          <div v-if="application.git_integration && Object.keys(application.git_integration).length > 0" class="mb-6">
            <h5 class="text-lg font-semibold text-gray-700 mb-3">Git Integration</h5>
            <div class="bg-gray-50 rounded-lg p-4">
              <div v-if="application.git_integration.repository_url" class="mb-2">
                <label class="text-sm font-medium text-gray-500">Repository URL</label>
                <p class="text-gray-800 font-mono text-sm break-all">{{ application.git_integration.repository_url }}</p>
              </div>
              <div v-if="application.git_integration.branch">
                <label class="text-sm font-medium text-gray-500">Branch</label>
                <p class="text-gray-800 font-mono text-sm">{{ application.git_integration.branch }}</p>
              </div>
            </div>
          </div>

          <!-- OIDC Integration -->
          <div v-if="application.oidc_integration && Object.keys(application.oidc_integration).length > 0" class="mb-6">
            <h5 class="text-lg font-semibold text-gray-700 mb-3">OIDC Integration</h5>
            <div class="bg-gray-50 rounded-lg p-4">
              <div v-if="application.oidc_integration.provider" class="mb-2">
                <label class="text-sm font-medium text-gray-500">Provider</label>
                <p class="text-gray-800">{{ application.oidc_integration.provider }}</p>
              </div>
              <div v-if="application.oidc_integration.client_id">
                <label class="text-sm font-medium text-gray-500">Client ID</label>
                <p class="text-gray-800 font-mono text-sm">{{ application.oidc_integration.client_id }}</p>
              </div>
            </div>
          </div>

          <!-- Actions (for creators who own the application) -->
          <div v-if="canEdit" class="flex gap-3 mt-6">
            <button
              @click="editApplication"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            >
              Edit Application
            </button>
            <button
              @click="confirmDelete"
              class="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
            >
              Delete Application
            </button>
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
