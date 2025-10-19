<template>
  <div>
    <!-- Git Integration Section -->
    <div class="mb-4">
      <div class="flex items-center mb-2">
        <input type="checkbox" id="enable_git" v-model="enableGitLocal" class="mr-2" />
        <label for="enable_git" class="text-sm font-medium text-gray-700">Enable Git Integration</label>
      </div>

      <div v-if="enableGitLocal" class="pl-6 space-y-3">
        <div>
          <label for="git_repo" class="block text-xs font-medium text-gray-600 mb-1">Repository URL <span class="text-red-600">*</span></label>
          <input id="git_repo" type="url" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" v-model="gitIntegrationLocal.repository_url" placeholder="https://github.com/org/repo.git" />
        </div>
        <div>
          <label for="git_branch" class="block text-xs font-medium text-gray-600 mb-1">Branch (Optional)</label>
          <input id="git_branch" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" v-model="gitIntegrationLocal.branch" placeholder="main" />
        </div>
      </div>
    </div>

    <!-- OIDC Integration Section -->
    <div class="mb-4">
      <div class="flex items-center mb-2">
        <input type="checkbox" id="enable_oidc" v-model="enableOidcLocal" class="mr-2" />
        <label for="enable_oidc" class="text-sm font-medium text-gray-700">Enable OIDC Integration</label>
      </div>

      <div v-if="enableOidcLocal" class="pl-6 space-y-3">
        <div>
          <label for="oidc_provider" class="block text-xs font-medium text-gray-600 mb-1">Provider <span class="text-red-600">*</span></label>
          <input id="oidc_provider" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" v-model="oidcIntegrationLocal.provider" placeholder="e.g., auth0, okta" />
        </div>
        <div>
          <label for="oidc_client_id" class="block text-xs font-medium text-gray-600 mb-1">Client ID <span class="text-red-600">*</span></label>
          <input id="oidc_client_id" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" v-model="oidcIntegrationLocal.client_id" placeholder="client_id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toRefs, watch } from 'vue';
const props = defineProps<{
  enableGit: boolean;
  enableOidc: boolean;
  gitIntegration: { repository_url?: string; branch?: string };
  oidcIntegration: { provider?: string; client_id?: string };
}>();

const emits = defineEmits<{ (e: 'update:enableGit', v: boolean): void; (e: 'update:enableOidc', v: boolean): void; (e: 'update:gitIntegration', v: any): void; (e: 'update:oidcIntegration', v: any): void }>();

// Local copies to avoid mutating props directly
const enableGitLocal = toRefs(props).enableGit as any;
const enableOidcLocal = toRefs(props).enableOidc as any;
const gitIntegrationLocal = { ...(props.gitIntegration || {}) };
const oidcIntegrationLocal = { ...(props.oidcIntegration || {}) };

watch(() => enableGitLocal.value, (v) => emits('update:enableGit', v));
watch(() => enableOidcLocal.value, (v) => emits('update:enableOidc', v));
watch(gitIntegrationLocal, (v) => emits('update:gitIntegration', v), { deep: true });
watch(oidcIntegrationLocal, (v) => emits('update:oidcIntegration', v), { deep: true });
</script>

<style scoped></style>
