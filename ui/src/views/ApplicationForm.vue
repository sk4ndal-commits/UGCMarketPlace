<template>
  <div class="container mx-auto px-4 py-6 max-w-4xl">
    <div class="bg-white rounded-lg shadow-sm">
      <div class="bg-gradient-primary text-white p-5 rounded-t-lg">
        <h3 class="text-2xl font-bold">{{ isEdit ? 'Edit Application' : 'Create New Application' }}</h3>
      </div>
      <div class="p-6">
        <!-- Success Message -->
        <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4 flex justify-between items-center">
          {{ successMessage }}
          <button type="button" class="text-green-700 hover:text-green-900 font-bold text-xl" @click="successMessage = ''">&times;</button>
        </div>

        <!-- Error Messages -->
        <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 flex justify-between items-center">
          {{ errorMessage }}
          <button type="button" class="text-red-700 hover:text-red-900 font-bold text-xl" @click="errorMessage = ''">&times;</button>
        </div>

        <form @submit.prevent="handleSubmit">
          <!-- Name -->
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
              Application Name <span class="text-red-600">*</span>
            </label>
            <input
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.name ? 'border-red-500' : 'border-gray-300'"
              id="name"
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
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.description ? 'border-red-500' : 'border-gray-300'"
              id="description"
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
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.owner ? 'border-red-500' : 'border-gray-300'"
              id="owner"
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
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.visibility ? 'border-red-500' : 'border-gray-300'"
              id="visibility"
              v-model="formData.visibility"
              required
            >
              <option value="">Select visibility...</option>
              <option
                v-for="option in visibilityChoices"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <div v-if="errors.visibility" class="text-red-600 text-sm mt-1">{{ errors.visibility }}</div>
          </div>

          <!-- Template Selection -->
          <div class="mb-4">
            <label for="template_id" class="block text-sm font-medium text-gray-700 mb-1">
              Template (Optional)
            </label>
            <select
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.template_id ? 'border-red-500' : 'border-gray-300'"
              id="template_id"
              v-model="formData.template_id"
              @change="onTemplateChange"
            >
              <option value="">No template (free configuration)</option>
              <option
                v-for="template in templates"
                :key="template.id"
                :value="template.template_id"
              >
                {{ template.name }} ({{ template.template_id }})
              </option>
            </select>
            <div v-if="errors.template_id" class="text-red-600 text-sm mt-1">{{ errors.template_id }}</div>
          </div>

          <!-- Parameters (JSON) -->
          <div class="mb-4">
            <label for="parameters" class="block text-sm font-medium text-gray-700 mb-1">
              Parameters (JSON format)
            </label>
            <textarea
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              :class="errors.parameters ? 'border-red-500' : 'border-gray-300'"
              id="parameters"
              v-model="parametersJson"
              rows="4"
              placeholder='{"key": "value"}'
            ></textarea>
            <div v-if="errors.parameters" class="text-red-600 text-sm mt-1">{{ errors.parameters }}</div>
            <p class="text-xs text-gray-500 mt-1">Leave empty for no parameters or enter valid JSON</p>
          </div>

          <!-- Git Integration Section -->
          <div class="mb-4">
            <div class="flex items-center mb-2">
              <input
                type="checkbox"
                id="enable_git"
                v-model="enableGit"
                class="mr-2"
              />
              <label for="enable_git" class="text-sm font-medium text-gray-700">
                Enable Git Integration
              </label>
            </div>

            <div v-if="enableGit" class="pl-6 space-y-3">
              <div>
                <label for="git_repo" class="block text-xs font-medium text-gray-600 mb-1">
                  Repository URL <span class="text-red-600">*</span>
                </label>
                <input
                  type="url"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  id="git_repo"
                  v-model="gitIntegration.repository_url"
                  placeholder="https://github.com/org/repo.git"
                />
              </div>
              <div>
                <label for="git_branch" class="block text-xs font-medium text-gray-600 mb-1">
                  Branch (Optional)
                </label>
                <input
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  id="git_branch"
                  v-model="gitIntegration.branch"
                  placeholder="main"
                />
              </div>
            </div>
          </div>

          <!-- OIDC Integration Section -->
          <div class="mb-4">
            <div class="flex items-center mb-2">
              <input
                type="checkbox"
                id="enable_oidc"
                v-model="enableOidc"
                class="mr-2"
              />
              <label for="enable_oidc" class="text-sm font-medium text-gray-700">
                Enable OIDC Integration
              </label>
            </div>

            <div v-if="enableOidc" class="pl-6 space-y-3">
              <div>
                <label for="oidc_provider" class="block text-xs font-medium text-gray-600 mb-1">
                  Provider <span class="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  id="oidc_provider"
                  v-model="oidcIntegration.provider"
                  placeholder="e.g., auth0, okta"
                />
              </div>
              <div>
                <label for="oidc_client_id" class="block text-xs font-medium text-gray-600 mb-1">
                  Client ID <span class="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  id="oidc_client_id"
                  v-model="oidcIntegration.client_id"
                  placeholder="client_id"
                />
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 mt-6">
            <button
              type="submit"
              class="px-6 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition disabled:opacity-50"
              :disabled="loading"
            >
              {{ loading ? 'Saving...' : (isEdit ? 'Update Application' : 'Create Application') }}
            </button>
            <button
              type="button"
              class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition"
              @click="$router.push('/applications')"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import applicationService, { type Template, type CreatorApplicationFormData } from '../services/applicationService';

const router = useRouter();
const route = useRoute();

const isEdit = computed(() => !!route.params.id);
const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const templates = ref<Template[]>([]);
const enableGit = ref(false);
const enableOidc = ref(false);

const formData = reactive<CreatorApplicationFormData>({
  name: '',
  description: '',
  owner: '',
  visibility: 'INTERNAL',
  template_id: '',
  parameters: {},
  git_integration: {},
  oidc_integration: {},
});

const parametersJson = ref('');
const gitIntegration = reactive({
  repository_url: '',
  branch: '',
});
const oidcIntegration = reactive({
  provider: '',
  client_id: '',
});

const errors = reactive<Record<string, string>>({});
const visibilityChoices = applicationService.getVisibilityChoices();

/**
 * Load templates on mount
 */
onMounted(async () => {
  await loadTemplates();
  
  // If editing, load application data
  if (isEdit.value) {
    await loadApplication();
  }
});

/**
 * Load available templates
 */
async function loadTemplates() {
  try {
    const response = await applicationService.getTemplates();
    if (response.status === 'success' && Array.isArray(response.data)) {
      templates.value = response.data;
    }
  } catch (error: any) {
    console.error('Failed to load templates:', error);
  }
}

/**
 * Load application data for editing
 */
async function loadApplication() {
  try {
    const id = parseInt(route.params.id as string);
    const response = await applicationService.getApplication(id);
    
    if (response.status === 'success' && !Array.isArray(response.data)) {
      const app = response.data;
      formData.name = app.name;
      formData.description = app.description;
      formData.owner = app.owner;
      formData.visibility = app.visibility;
      
      if (app.template_details) {
        formData.template_id = app.template_details.template_id;
      }
      
      if (app.parameters && Object.keys(app.parameters).length > 0) {
        parametersJson.value = JSON.stringify(app.parameters, null, 2);
      }
      
      if (app.git_integration && Object.keys(app.git_integration).length > 0) {
        enableGit.value = true;
        gitIntegration.repository_url = app.git_integration.repository_url || '';
        gitIntegration.branch = app.git_integration.branch || '';
      }
      
      if (app.oidc_integration && Object.keys(app.oidc_integration).length > 0) {
        enableOidc.value = true;
        oidcIntegration.provider = app.oidc_integration.provider || '';
        oidcIntegration.client_id = app.oidc_integration.client_id || '';
      }
    }
  } catch (error: any) {
    errorMessage.value = 'Failed to load application data';
    console.error('Failed to load application:', error);
  }
}

/**
 * Handle template change
 */
function onTemplateChange() {
  // Could load template defaults here
  console.log('Template changed to:', formData.template_id);
}

/**
 * Handle form submission
 */
async function handleSubmit() {
  // Clear previous messages and errors
  successMessage.value = '';
  errorMessage.value = '';
  Object.keys(errors).forEach(key => delete errors[key]);
  
  loading.value = true;
  
  try {
    // Parse parameters JSON
    if (parametersJson.value.trim()) {
      try {
        formData.parameters = JSON.parse(parametersJson.value);
      } catch (e) {
        errors.parameters = 'Invalid JSON format';
        loading.value = false;
        return;
      }
    } else {
      formData.parameters = {};
    }
    
    // Set Git integration if enabled
    if (enableGit.value && gitIntegration.repository_url) {
      formData.git_integration = {
        repository_url: gitIntegration.repository_url,
        ...(gitIntegration.branch && { branch: gitIntegration.branch }),
      };
    } else {
      formData.git_integration = {};
    }
    
    // Set OIDC integration if enabled
    if (enableOidc.value && oidcIntegration.provider && oidcIntegration.client_id) {
      formData.oidc_integration = {
        provider: oidcIntegration.provider,
        client_id: oidcIntegration.client_id,
      };
    } else {
      formData.oidc_integration = {};
    }
    
    let response;
    if (isEdit.value) {
      const id = parseInt(route.params.id as string);
      response = await applicationService.updateApplication(id, formData);
    } else {
      response = await applicationService.createApplication(formData);
    }
    
    if (response.status === 'success') {
      successMessage.value = isEdit.value 
        ? 'Application updated successfully!' 
        : 'Application created successfully!';
      
      // Redirect after short delay
      setTimeout(() => {
        router.push('/applications');
      }, 1500);
    } else {
      errorMessage.value = response.errors?.join(', ') || 'Failed to save application';
    }
  } catch (error: any) {
    console.error('Form submission error:', error);
    
    // Handle validation errors
    if (error.response?.data?.errors) {
      const apiErrors = error.response.data.errors;
      if (Array.isArray(apiErrors)) {
        errorMessage.value = apiErrors.join(', ');
      } else if (typeof apiErrors === 'object') {
        Object.keys(apiErrors).forEach(key => {
          errors[key] = Array.isArray(apiErrors[key]) ? apiErrors[key][0] : apiErrors[key];
        });
      }
    } else {
      errorMessage.value = error.response?.data?.message || 'An error occurred while saving the application';
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
