<template>
  <div class="container mx-auto px-4 py-6">
    <div class="bg-white rounded-lg shadow-sm">
      <div class="bg-gradient-primary text-white p-5 rounded-t-lg flex justify-between items-center">
        <h3 class="text-2xl font-bold">Application Catalog</h3>
        <button
          v-if="isCreator"
          @click="$router.push('/applications/new')"
          class="px-4 py-2 bg-white text-purple-700 rounded-lg hover:bg-gray-100 transition font-medium"
        >
          + Create Application
        </button>
      </div>

      <div class="p-6">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-700"></div>
          <p class="mt-3 text-gray-600">Loading applications...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ errorMessage }}
        </div>

        <!-- Empty State -->
        <div v-else-if="applications.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">No applications found</h3>
          <p class="mt-1 text-sm text-gray-500">
            {{ isCreator ? 'Get started by creating your first application.' : 'No applications are currently available in the catalog.' }}
          </p>
          <div v-if="isCreator" class="mt-6">
            <button
              @click="$router.push('/applications/new')"
              class="px-4 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition"
            >
              Create Application
            </button>
          </div>
        </div>

        <!-- Applications Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="app in applications"
            :key="app.id"
            class="border border-gray-200 rounded-lg p-5 hover:shadow-md transition cursor-pointer"
            @click="viewApplication(app.id!)"
          >
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
              <div v-if="app.template_name" class="flex items-center">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
                <span>Template: {{ app.template_name }}</span>
              </div>
              <div class="flex items-center">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Created: {{ formatDate(app.created_at) }}</span>
              </div>
            </div>

            <!-- Actions (for creators) -->
            <div v-if="isCreator && app.creator_email === currentUserEmail" class="mt-4 flex gap-2">
              <button
                @click.stop="editApplication(app.id!)"
                class="flex-1 px-3 py-1.5 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition"
              >
                Edit
              </button>
              <button
                @click.stop="confirmDelete(app.id!)"
                class="flex-1 px-3 py-1.5 text-sm bg-red-500 text-white rounded hover:bg-red-600 transition"
              >
                Delete
              </button>
            </div>
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
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import applicationService from '../services/applicationService';
import type { CreatorApplication } from '../models/application';

const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const errorMessage = ref('');
const applications = ref<CreatorApplication[]>([]);
const showDeleteModal = ref(false);
const applicationToDelete = ref<number | null>(null);

const isCreator = computed(() => authStore.user?.role === 'CREATOR');
const currentUserEmail = computed(() => authStore.user?.email);

/**
 * Load applications on mount
 */
onMounted(async () => {
  await loadApplications();
});

/**
 * Load all applications
 */
async function loadApplications() {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await applicationService.getApplications();
    if (response.status === 'success' && Array.isArray(response.data)) {
      applications.value = response.data;
    } else {
      errorMessage.value = 'Failed to load applications';
    }
  } catch (error: any) {
    console.error('Failed to load applications:', error);
    errorMessage.value = error.response?.data?.message || 'Failed to load applications';
  } finally {
    loading.value = false;
  }
}

/**
 * View application details
 */
function viewApplication(id: number) {
  router.push(`/applications/${id}`);
}

/**
 * Edit application
 */
function editApplication(id: number) {
  router.push(`/applications/${id}/edit`);
}

/**
 * Show delete confirmation
 */
function confirmDelete(id: number) {
  applicationToDelete.value = id;
  showDeleteModal.value = true;
}

/**
 * Delete application
 */
async function deleteApplication() {
  if (!applicationToDelete.value) return;
  
  try {
    const response = await applicationService.deleteApplication(applicationToDelete.value);
    if (response.status === 'success') {
      // Remove from list
      applications.value = applications.value.filter(app => app.id !== applicationToDelete.value);
      showDeleteModal.value = false;
      applicationToDelete.value = null;
    } else {
      errorMessage.value = 'Failed to delete application';
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
    month: 'short',
    day: 'numeric',
  });
}
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
