<template>
  <div class="container mx-auto px-4 py-6 max-w-4xl">
    <FormHeader :title="isEdit ? 'Edit Campaign' : 'Create New Campaign'" />
    <div class="p-6 bg-white rounded-b-lg shadow-sm">
      <FormMessages :successMessage="successMessage" :errorMessage="errorMessage" @clear-success="successMessage = ''" @clear-error="errorMessage = ''" />

      <form @submit.prevent="handleSubmit">
          <!-- Core form fields (title, description, deliverables, budget, deadline) -->
          <CampaignFormCore :formData="formData" :errors="errors" :minDate="minDate" />

          <!-- Meta fields (content type, category, status) -->
          <CampaignFormMeta
            :formData="formData"
            :errors="errors"
            :contentTypeChoices="contentTypeChoices"
            :categoryChoices="categoryChoices"
            :statusChoices="statusChoices"
          />

          <!-- File Upload (shared) -->
          <CampaignFileUploader :selectedFiles="selectedFiles" :errors="errors" @update:selectedFiles="updateSelectedFiles" />

          <FormActions>
            <template #left>
              <button
                type="button"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                @click="$router.push('/campaigns')"
              >
                Cancel
              </button>
            </template>
            <template #right>
              <button
                type="submit"
                class="px-4 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
                :disabled="isSubmitting"
              >
                <span v-if="isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                {{ isSubmitting ? 'Saving...' : (isEdit ? 'Update Campaign' : 'Create Campaign') }}
              </button>
            </template>
          </FormActions>
        </form>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import campaignService from '../services/campaignService';
import CampaignFileUploader from './shared/CampaignFileUploader.vue';
import CampaignFormCore from './shared/CampaignFormCore.vue';
import CampaignFormMeta from './shared/CampaignFormMeta.vue';
import FormHeader from './shared/FormHeader.vue';
import FormMessages from './shared/FormMessages.vue';
import FormActions from './shared/FormActions.vue';
import type { CampaignFormData } from '../models/campaign';

const router = useRouter();
const route = useRoute();

const isEdit = computed(() => !!route.params.id);
const campaignId = computed(() => route.params.id ? Number(route.params.id) : null);

const formData = ref<CampaignFormData>({
  title: '',
  description: '',
  content_type: '',
  category: '',
  deliverables: '',
  budget: '',
  deadline: '',
  status: 'DRAFT',
});

const selectedFiles = ref<File[]>([]);
const errors = ref<Record<string, string>>({});
const errorMessage = ref('');
const successMessage = ref('');
const isSubmitting = ref(false);

const contentTypeChoices = campaignService.getContentTypeChoices();
const categoryChoices = campaignService.getCategoryChoices();
const statusChoices = campaignService.getStatusChoices();

const minDate = computed(() => {
  const today = new Date();
  today.setDate(today.getDate() + 1);
  return today.toISOString().split('T')[0];
});

function updateSelectedFiles(val: File[]) {
  selectedFiles.value = val;
  if (selectedFiles.value.length === 0) {
    delete errors.value.reference_files;
  } else {
    errors.value.reference_files = '';
  }
}

const validateForm = (): boolean => {
  errors.value = {};
  
  if (!formData.value.title.trim()) {
    errors.value.title = 'Title is required';
  }
  
  if (!formData.value.description.trim()) {
    errors.value.description = 'Description is required';
  }
  
  if (!formData.value.content_type) {
    errors.value.content_type = 'Content type is required';
  }
  
  if (!formData.value.category) {
    errors.value.category = 'Category is required';
  }
  
  if (!formData.value.deliverables.trim()) {
    errors.value.deliverables = 'Deliverables are required';
  }
  
  if (!formData.value.budget || Number(formData.value.budget) <= 0) {
    errors.value.budget = 'Budget must be greater than 0';
  }
  
  if (!formData.value.deadline) {
    errors.value.deadline = 'Deadline is required';
  } else {
    const deadlineDate = new Date(formData.value.deadline);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (deadlineDate <= today) {
      errors.value.deadline = 'Deadline must be a future date';
    }
  }
  
  if (!formData.value.status) {
    errors.value.status = 'Status is required';
  }
  
  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }
  
  isSubmitting.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  
  try {
    const submitData: CampaignFormData = {
      ...formData.value,
      reference_files: selectedFiles.value.length > 0 ? selectedFiles.value : undefined,
    };
    
    if (isEdit.value && campaignId.value) {
      await campaignService.updateCampaign(campaignId.value, submitData);
      successMessage.value = 'Campaign updated successfully!';
    } else {
      await campaignService.createCampaign(submitData);
      successMessage.value = 'Campaign created successfully!';
    }
    
    // Redirect to campaigns list after a short delay
    setTimeout(() => {
      router.push('/campaigns');
    }, 1500);
  } catch (error: any) {
    console.error('Error submitting campaign:', error);
    
    if (error.response?.data?.errors) {
      const apiErrors = error.response.data.errors;
      
      if (typeof apiErrors === 'object') {
        Object.keys(apiErrors).forEach(key => {
          errors.value[key] = Array.isArray(apiErrors[key]) 
            ? apiErrors[key].join(', ') 
            : apiErrors[key];
        });
      }
      
      errorMessage.value = 'Please correct the errors below and try again.';
    } else {
      errorMessage.value = error.response?.data?.message || 'Failed to save campaign. Please try again.';
    }
  } finally {
    isSubmitting.value = false;
  }
};

const loadCampaign = async () => {
  if (isEdit.value && campaignId.value) {
    try {
      const response = await campaignService.getCampaign(campaignId.value);
      const campaign = response.data as any;
      
      formData.value = {
        title: campaign.title,
        description: campaign.description,
        content_type: campaign.content_type,
        category: campaign.category,
        deliverables: campaign.deliverables,
        budget: campaign.budget,
        deadline: campaign.deadline,
        status: campaign.status,
      };
    } catch (error: any) {
      console.error('Error loading campaign:', error);
      errorMessage.value = 'Failed to load campaign data.';
    }
  }
};

onMounted(() => {
  loadCampaign();
});
</script>

<style scoped>
/* All styles now handled by Tailwind CSS */
</style>
