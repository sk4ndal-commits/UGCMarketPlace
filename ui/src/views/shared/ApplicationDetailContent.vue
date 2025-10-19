<template>
  <div>
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
  </div>
</template>

<script setup lang="ts">
import type { CreatorApplication } from '../../models/application';
const props = defineProps<{ application: CreatorApplication; formatDate: (d?: string) => string }>();
const { application, formatDate } = props;
</script>

<style scoped></style>
