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
          <ApplicationItem
            v-for="app in applications"
            :key="app.id"
            :app="app"
            :isCreator="isCreator"
            :currentUserId="currentUserId"
            @view="viewApplication"
            @edit="editApplication"
            @deleted="onDeleted"
          />
        </div>
      </div>
    </div>

    <!-- item-level confirmation modals moved into ApplicationItem -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import applicationService from '../services/applicationService';
import type { CreatorApplication } from '../models/application';
import ApplicationItem from './shared/ApplicationItem.vue';

const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const errorMessage = ref('');
const applications = ref<CreatorApplication[]>([]);
// deletion is handled by ApplicationItem via emitted 'deleted' event

const isCreator = computed(() => authStore.user?.role === 'CREATOR');
const currentUserId = computed(() => authStore.user?.id);

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
function onDeleted(id: number) {
  applications.value = applications.value.filter(a => a.id !== id);
}

/**
 * Get visibility badge class
 */
// visibility and date formatting are handled inside ApplicationItem now
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
