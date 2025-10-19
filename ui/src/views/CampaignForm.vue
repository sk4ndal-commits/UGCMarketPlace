<template>
  <div class="container mx-auto px-4 py-6 max-w-4xl">
    <div class="bg-white rounded-lg shadow-sm">
      <div class="bg-gradient-primary text-white p-5 rounded-t-lg">
        <h3 class="text-2xl font-bold">{{ isEdit ? 'Edit Campaign' : 'Create New Campaign' }}</h3>
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
          <!-- Title -->
          <div class="mb-4">
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
              Title <span class="text-red-600">*</span>
            </label>
            <input
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.title ? 'border-red-500' : 'border-gray-300'"
              id="title"
              v-model="formData.title"
              required
              maxlength="200"
              placeholder="e.g., UGC Reel for Vegan Skincare Product"
            />
            <div v-if="errors.title" class="text-red-600 text-sm mt-1">{{ errors.title }}</div>
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
              placeholder="Provide a detailed description of your campaign requirements..."
            ></textarea>
            <div v-if="errors.description" class="text-red-600 text-sm mt-1">{{ errors.description }}</div>
          </div>

          <!-- Content Type -->
          <div class="mb-4">
            <label for="content_type" class="block text-sm font-medium text-gray-700 mb-1">
              Content Type <span class="text-red-600">*</span>
            </label>
            <select
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.content_type ? 'border-red-500' : 'border-gray-300'"
              id="content_type"
              v-model="formData.content_type"
              required
            >
              <option value="">Select content type...</option>
              <option
                v-for="option in contentTypeChoices"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <div v-if="errors.content_type" class="text-red-600 text-sm mt-1">{{ errors.content_type }}</div>
          </div>

          <!-- Category -->
          <div class="mb-4">
            <label for="category" class="block text-sm font-medium text-gray-700 mb-1">
              Category <span class="text-red-600">*</span>
            </label>
            <select
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.category ? 'border-red-500' : 'border-gray-300'"
              id="category"
              v-model="formData.category"
              required
            >
              <option value="">Select category...</option>
              <option
                v-for="option in categoryChoices"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <div v-if="errors.category" class="text-red-600 text-sm mt-1">{{ errors.category }}</div>
          </div>

          <!-- Deliverables -->
          <div class="mb-4">
            <label for="deliverables" class="block text-sm font-medium text-gray-700 mb-1">
              Deliverables <span class="text-red-600">*</span>
            </label>
            <textarea
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.deliverables ? 'border-red-500' : 'border-gray-300'"
              id="deliverables"
              v-model="formData.deliverables"
              rows="3"
              required
              placeholder="e.g., 1 Instagram Reel (30-60 seconds), 3 story frames"
            ></textarea>
            <div v-if="errors.deliverables" class="text-red-600 text-sm mt-1">{{ errors.deliverables }}</div>
          </div>

          <!-- Budget -->
          <div class="mb-4">
            <label for="budget" class="block text-sm font-medium text-gray-700 mb-1">
              Budget (EUR) <span class="text-red-600">*</span>
            </label>
            <input
              type="number"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.budget ? 'border-red-500' : 'border-gray-300'"
              id="budget"
              v-model.number="formData.budget"
              step="0.01"
              min="0.01"
              required
              placeholder="250.00"
            />
            <div v-if="errors.budget" class="text-red-600 text-sm mt-1">{{ errors.budget }}</div>
            <small class="text-gray-500 text-sm">Budget must be greater than 0</small>
          </div>

          <!-- Deadline -->
          <div class="mb-4">
            <label for="deadline" class="block text-sm font-medium text-gray-700 mb-1">
              Deadline <span class="text-red-600">*</span>
            </label>
            <input
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.deadline ? 'border-red-500' : 'border-gray-300'"
              id="deadline"
              v-model="formData.deadline"
              :min="minDate"
              required
            />
            <div v-if="errors.deadline" class="text-red-600 text-sm mt-1">{{ errors.deadline }}</div>
            <small class="text-gray-500 text-sm">Deadline must be a future date</small>
          </div>

          <!-- Status -->
          <div class="mb-4">
            <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
              Status <span class="text-red-600">*</span>
            </label>
            <select
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.status ? 'border-red-500' : 'border-gray-300'"
              id="status"
              v-model="formData.status"
              required
            >
              <option
                v-for="option in statusChoices"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <div v-if="errors.status" class="text-red-600 text-sm mt-1">{{ errors.status }}</div>
            <small class="text-gray-500 text-sm">
              Campaign will only be visible to influencers when status is "Live"
            </small>
          </div>

          <!-- File Upload -->
          <div class="mb-4">
            <label for="files" class="block text-sm font-medium text-gray-700 mb-1">Reference Materials (Optional)</label>
            <input
              type="file"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="errors.reference_files ? 'border-red-500' : 'border-gray-300'"
              id="files"
              @change="handleFileChange"
              multiple
              accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.mp4,.mov"
            />
            <div v-if="errors.reference_files" class="text-red-600 text-sm mt-1">{{ errors.reference_files }}</div>
            <small class="text-gray-500 text-sm block mt-1">
              Max 10 MB per file. Accepted formats: PDF, JPG, PNG, DOC, DOCX, MP4, MOV
            </small>
            
            <!-- Selected Files List -->
            <div v-if="selectedFiles.length > 0" class="mt-3">
              <strong class="text-sm">Selected files:</strong>
              <ul class="mt-2 space-y-2">
                <li
                  v-for="(file, index) in selectedFiles"
                  :key="index"
                  class="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded"
                >
                  <span class="text-sm">{{ file.name }} ({{ formatFileSize(file.size) }})</span>
                  <button
                    type="button"
                    class="px-2 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                    @click="removeFile(index)"
                  >
                    Remove
                  </button>
                </li>
              </ul>
            </div>
          </div>

          <!-- Submit Buttons -->
          <div class="flex justify-between pt-4">
            <button
              type="button"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              @click="$router.push('/campaigns')"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
              {{ isSubmitting ? 'Saving...' : (isEdit ? 'Update Campaign' : 'Create Campaign') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import campaignService, { type CampaignFormData } from '../services/campaignService';

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

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    const files = Array.from(target.files);
    const maxSize = 10 * 1024 * 1024; // 10 MB
    
    const invalidFiles = files.filter(file => file.size > maxSize);
    if (invalidFiles.length > 0) {
      errors.value.reference_files = `Some files exceed 10 MB limit: ${invalidFiles.map(f => f.name).join(', ')}`;
      return;
    }
    
    errors.value.reference_files = '';
    selectedFiles.value = [...selectedFiles.value, ...files];
  }
};

const removeFile = (index: number) => {
  selectedFiles.value.splice(index, 1);
};

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

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
