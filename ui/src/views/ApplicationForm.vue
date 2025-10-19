<template>
  <div class="container mx-auto px-4 py-6 max-w-4xl">
    <FormHeader :title="isEdit ? 'Edit Application' : 'Create New Application'" />
    <div class="p-6 bg-white rounded-b-lg shadow-sm">
      <FormMessages :successMessage="successMessage" :errorMessage="errorMessage" @clear-success="successMessage = ''" @clear-error="errorMessage = ''" />

      <form @submit.prevent="handleSubmit">
          <ApplicationFormCore
            :formData="formData"
            :errors="errors"
            :templates="templates"
            :visibilityChoices="visibilityChoices"
            @template-change="onTemplateChange"
          />

          <ParametersEditor :parametersJson="parametersJson" :errors="errors" @update:parametersJson="updateParameters" />

          <ApplicationFormIntegrations
            :enableGit="enableGit"
            :enableOidc="enableOidc"
            :gitIntegration="gitIntegration"
            :oidcIntegration="oidcIntegration"
            @update:enableGit="updateEnableGit"
            @update:enableOidc="updateEnableOidc"
            @update:gitIntegration="updateGitIntegration"
            @update:oidcIntegration="updateOidcIntegration"
          />

          <FormActions>
            <template #left>
              <button
                type="button"
                class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition"
                @click="$router.push('/applications')"
              >
                Cancel
              </button>
            </template>
            <template #right>
              <button
                type="submit"
                class="px-6 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition disabled:opacity-50"
                :disabled="loading"
              >
                {{ loading ? 'Saving...' : (isEdit ? 'Update Application' : 'Create Application') }}
              </button>
            </template>
          </FormActions>
        </form>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import applicationService from '../services/applicationService';
import type { Template, CreatorApplicationFormData } from '../models/application';
import FormHeader from './shared/FormHeader.vue';
import FormMessages from './shared/FormMessages.vue';
import FormActions from './shared/FormActions.vue';
import { parseParametersJson, normalizeGitIntegration, normalizeOidcIntegration } from '../composables/useApplicationValidation';

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
    // Parse parameters JSON using composable
    const parsed = parseParametersJson(parametersJson.value);
    if (!parsed.ok) {
      errors.parameters = parsed.error as string;
      loading.value = false;
      return;
    }
    formData.parameters = parsed.value;

    // Normalize integrations using composable helpers
    formData.git_integration = normalizeGitIntegration(enableGit.value, gitIntegration);
    formData.oidc_integration = normalizeOidcIntegration(enableOidc.value, oidcIntegration);
    
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

// Event handlers wired to child components (avoid inline arrow handlers to keep types explicit)
function updateParameters(v: string) {
  parametersJson.value = v;
}

function updateEnableGit(v: boolean) {
  enableGit.value = v;
}

function updateEnableOidc(v: boolean) {
  enableOidc.value = v;
}

function updateGitIntegration(v: any) {
  Object.assign(gitIntegration, v);
}

function updateOidcIntegration(v: any) {
  Object.assign(oidcIntegration, v);
}
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
