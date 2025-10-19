import apiClient from './api';
import type {
  CampaignResponse,
  CampaignFormData,
  CampaignFilters,
  ApplicationFormData,
  ApplicationResponse,
} from '../models/campaign';

const campaignService = {
  /**
   * Get all campaigns (filtered by user role on backend)
   * @param filters - Optional filters for campaigns (for influencers)
   */
  async getCampaigns(filters?: CampaignFilters): Promise<CampaignResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      if (filters.budget_min !== undefined) {
        params.append('budget_min', filters.budget_min.toString());
      }
      if (filters.budget_max !== undefined) {
        params.append('budget_max', filters.budget_max.toString());
      }
      if (filters.category) {
        params.append('category', filters.category);
      }
      if (filters.content_type) {
        params.append('content_type', filters.content_type);
      }
      if (filters.deadline_before) {
        params.append('deadline_before', filters.deadline_before);
      }
    }
    
    const url = params.toString() ? `/api/v1/campaigns/?${params.toString()}` : '/api/v1/campaigns/';
    const response = await apiClient.get(url);
    return response.data;
  },

  /**
   * Get a single campaign by ID
   */
  async getCampaign(id: number): Promise<CampaignResponse> {
    const response = await apiClient.get(`/api/v1/campaigns/${id}/`);
    return response.data;
  },

  /**
   * Create a new campaign
   */
  async createCampaign(campaignData: CampaignFormData): Promise<CampaignResponse> {
    // If there are files, use FormData
    if (campaignData.reference_files && campaignData.reference_files.length > 0) {
      const formData = new FormData();
      
      // Add all campaign fields
      formData.append('title', campaignData.title);
      formData.append('description', campaignData.description);
      formData.append('content_type', campaignData.content_type);
      formData.append('category', campaignData.category);
      formData.append('deliverables', campaignData.deliverables);
      formData.append('budget', campaignData.budget.toString());
      formData.append('deadline', campaignData.deadline);
      formData.append('status', campaignData.status);
      
      // Add files
      campaignData.reference_files.forEach((file) => {
        formData.append('reference_files', file);
      });
      
      const response = await apiClient.post('/api/v1/campaigns/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } else {
      // No files, send as JSON
      const response = await apiClient.post('/api/v1/campaigns/', {
        title: campaignData.title,
        description: campaignData.description,
        content_type: campaignData.content_type,
        category: campaignData.category,
        deliverables: campaignData.deliverables,
        budget: campaignData.budget,
        deadline: campaignData.deadline,
        status: campaignData.status,
      });
      return response.data;
    }
  },

  /**
   * Update an existing campaign
   */
  async updateCampaign(id: number, campaignData: Partial<CampaignFormData>): Promise<CampaignResponse> {
    // If there are files, use FormData
    if (campaignData.reference_files && campaignData.reference_files.length > 0) {
      const formData = new FormData();
      
      // Add all campaign fields that are present
      if (campaignData.title) formData.append('title', campaignData.title);
      if (campaignData.description) formData.append('description', campaignData.description);
      if (campaignData.content_type) formData.append('content_type', campaignData.content_type);
      if (campaignData.category) formData.append('category', campaignData.category);
      if (campaignData.deliverables) formData.append('deliverables', campaignData.deliverables);
      if (campaignData.budget) formData.append('budget', campaignData.budget.toString());
      if (campaignData.deadline) formData.append('deadline', campaignData.deadline);
      if (campaignData.status) formData.append('status', campaignData.status);
      
      // Add files
      campaignData.reference_files.forEach((file) => {
        formData.append('reference_files', file);
      });
      
      const response = await apiClient.patch(`/api/v1/campaigns/${id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } else {
      // No files, send as JSON
      const updateData: any = {};
      if (campaignData.title !== undefined) updateData.title = campaignData.title;
      if (campaignData.description !== undefined) updateData.description = campaignData.description;
      if (campaignData.content_type !== undefined) updateData.content_type = campaignData.content_type;
      if (campaignData.category !== undefined) updateData.category = campaignData.category;
      if (campaignData.deliverables !== undefined) updateData.deliverables = campaignData.deliverables;
      if (campaignData.budget !== undefined) updateData.budget = campaignData.budget;
      if (campaignData.deadline !== undefined) updateData.deadline = campaignData.deadline;
      if (campaignData.status !== undefined) updateData.status = campaignData.status;
      
      const response = await apiClient.patch(`/api/v1/campaigns/${id}/`, updateData);
      return response.data;
    }
  },

  /**
   * Delete a campaign
   */
  async deleteCampaign(id: number): Promise<CampaignResponse> {
    const response = await apiClient.delete(`/api/v1/campaigns/${id}/`);
    return response.data;
  },

  /**
   * Upload additional file to existing campaign
   */
  async uploadFile(campaignId: number, file: File): Promise<CampaignResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post(
      `/api/v1/campaigns/${campaignId}/upload_file/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  /**
   * Get content type choices for form
   */
  getContentTypeChoices() {
    return [
      { value: 'INSTAGRAM_REEL', label: 'Instagram Reel' },
      { value: 'INSTAGRAM_POST', label: 'Instagram Post' },
      { value: 'INSTAGRAM_STORY', label: 'Instagram Story' },
      { value: 'TIKTOK_VIDEO', label: 'TikTok Video' },
      { value: 'YOUTUBE_VIDEO', label: 'YouTube Video' },
      { value: 'YOUTUBE_SHORT', label: 'YouTube Short' },
    ];
  },

  /**
   * Get status choices for form
   */
  getStatusChoices() {
    return [
      { value: 'DRAFT', label: 'Draft' },
      { value: 'LIVE', label: 'Live' },
      { value: 'CLOSED', label: 'Closed' },
    ];
  },

  /**
   * Get category choices for form
   */
  getCategoryChoices() {
    return [
      { value: 'BEAUTY', label: 'Beauty' },
      { value: 'FASHION', label: 'Fashion' },
      { value: 'FITNESS', label: 'Fitness' },
      { value: 'FOOD', label: 'Food' },
      { value: 'TECH', label: 'Tech' },
      { value: 'TRAVEL', label: 'Travel' },
      { value: 'LIFESTYLE', label: 'Lifestyle' },
      { value: 'GAMING', label: 'Gaming' },
      { value: 'OTHER', label: 'Other' },
    ];
  },

  /**
   * Get all applications (filtered by user role on backend)
   */
  async getApplications(): Promise<ApplicationResponse> {
    const response = await apiClient.get('/api/v1/campaign-applications/');
    return response.data;
  },

  /**
   * Get a single application by ID
   */
  async getApplication(id: number): Promise<ApplicationResponse> {
    const response = await apiClient.get(`/api/v1/campaign-applications/${id}/`);
    return response.data;
  },

  /**
   * Create a new application
   */
  async createApplication(applicationData: ApplicationFormData): Promise<ApplicationResponse> {
    const response = await apiClient.post('/api/v1/campaign-applications/', {
      campaign: applicationData.campaign,
      pitch: applicationData.pitch,
      portfolio_link: applicationData.portfolio_link || null,
      proposed_price: applicationData.proposed_price || null,
    });
    return response.data;
  },

  /**
   * Update application status (shortlist, accept, reject)
   * Only brands can call this for their campaign applications
   */
  async updateApplicationStatus(id: number, status: string): Promise<ApplicationResponse> {
    const response = await apiClient.patch(`/api/v1/campaign-applications/${id}/update_status/`, {
      status,
    });
    return response.data;
  },
};

export default campaignService;
