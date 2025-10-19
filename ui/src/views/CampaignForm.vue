<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">{{ isEdit ? 'Edit Campaign' : 'Create New Campaign' }}</h3>
          </div>
          <div class="card-body">
            <!-- Success Message -->
            <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
              {{ successMessage }}
              <button type="button" class="btn-close" @click="successMessage = ''"></button>
            </div>

            <!-- Error Messages -->
            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = ''"></button>
            </div>

            <form @submit.prevent="handleSubmit">
              <!-- Title -->
              <div class="mb-3">
                <label for="title" class="form-label">Title <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.title }"
                  id="title"
                  v-model="formData.title"
                  required
                  maxlength="200"
                  placeholder="e.g., UGC Reel for Vegan Skincare Product"
                />
                <div v-if="errors.title" class="invalid-feedback">{{ errors.title }}</div>
              </div>

              <!-- Description -->
              <div class="mb-3">
                <label for="description" class="form-label">Description <span class="text-danger">*</span></label>
                <textarea
                  class="form-control"
                  :class="{ 'is-invalid': errors.description }"
                  id="description"
                  v-model="formData.description"
                  rows="4"
                  required
                  placeholder="Provide a detailed description of your campaign requirements..."
                ></textarea>
                <div v-if="errors.description" class="invalid-feedback">{{ errors.description }}</div>
              </div>

              <!-- Content Type -->
              <div class="mb-3">
                <label for="content_type" class="form-label">Content Type <span class="text-danger">*</span></label>
                <select
                  class="form-select"
                  :class="{ 'is-invalid': errors.content_type }"
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
                <div v-if="errors.content_type" class="invalid-feedback">{{ errors.content_type }}</div>
              </div>

              <!-- Deliverables -->
              <div class="mb-3">
                <label for="deliverables" class="form-label">Deliverables <span class="text-danger">*</span></label>
                <textarea
                  class="form-control"
                  :class="{ 'is-invalid': errors.deliverables }"
                  id="deliverables"
                  v-model="formData.deliverables"
                  rows="3"
                  required
                  placeholder="e.g., 1 Instagram Reel (30-60 seconds), 3 story frames"
                ></textarea>
                <div v-if="errors.deliverables" class="invalid-feedback">{{ errors.deliverables }}</div>
              </div>

              <!-- Budget -->
              <div class="mb-3">
                <label for="budget" class="form-label">Budget (EUR) <span class="text-danger">*</span></label>
                <input
                  type="number"
                  class="form-control"
                  :class="{ 'is-invalid': errors.budget }"
                  id="budget"
                  v-model.number="formData.budget"
                  step="0.01"
                  min="0.01"
                  required
                  placeholder="250.00"
                />
                <div v-if="errors.budget" class="invalid-feedback">{{ errors.budget }}</div>
                <small class="form-text text-muted">Budget must be greater than 0</small>
              </div>

              <!-- Deadline -->
              <div class="mb-3">
                <label for="deadline" class="form-label">Deadline <span class="text-danger">*</span></label>
                <input
                  type="date"
                  class="form-control"
                  :class="{ 'is-invalid': errors.deadline }"
                  id="deadline"
                  v-model="formData.deadline"
                  :min="minDate"
                  required
                />
                <div v-if="errors.deadline" class="invalid-feedback">{{ errors.deadline }}</div>
                <small class="form-text text-muted">Deadline must be a future date</small>
              </div>

              <!-- Status -->
              <div class="mb-3">
                <label for="status" class="form-label">Status <span class="text-danger">*</span></label>
                <select
                  class="form-select"
                  :class="{ 'is-invalid': errors.status }"
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
                <div v-if="errors.status" class="invalid-feedback">{{ errors.status }}</div>
                <small class="form-text text-muted">
                  Campaign will only be visible to influencers when status is "Live"
                </small>
              </div>

              <!-- File Upload -->
              <div class="mb-3">
                <label for="files" class="form-label">Reference Materials (Optional)</label>
                <input
                  type="file"
                  class="form-control"
                  :class="{ 'is-invalid': errors.reference_files }"
                  id="files"
                  @change="handleFileChange"
                  multiple
                  accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.mp4,.mov"
                />
                <div v-if="errors.reference_files" class="invalid-feedback">{{ errors.reference_files }}</div>
                <small class="form-text text-muted">
                  Max 10 MB per file. Accepted formats: PDF, JPG, PNG, DOC, DOCX, MP4, MOV
                </small>
                
                <!-- Selected Files List -->
                <div v-if="selectedFiles.length > 0" class="mt-2">
                  <strong>Selected files:</strong>
                  <ul class="list-group mt-1">
                    <li
                      v-for="(file, index) in selectedFiles"
                      :key="index"
                      class="list-group-item d-flex justify-content-between align-items-center"
                    >
                      {{ file.name }} ({{ formatFileSize(file.size) }})
                      <button
                        type="button"
                        class="btn btn-sm btn-danger"
                        @click="removeFile(index)"
                      >
                        Remove
                      </button>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Submit Buttons -->
              <div class="d-flex justify-content-between">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="$router.push('/campaigns')"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="isSubmitting"
                >
                  <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                  {{ isSubmitting ? 'Saving...' : (isEdit ? 'Update Campaign' : 'Create Campaign') }}
                </button>
              </div>
            </form>
          </div>
        </div>
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
.card {
  border-radius: 8px;
}

.card-header {
  border-radius: 8px 8px 0 0;
}

.form-label {
  font-weight: 500;
}

.text-danger {
  color: #dc3545;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
