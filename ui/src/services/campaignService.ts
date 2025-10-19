import apiClient from './api';

export interface Campaign {
  id?: number;
  title: string;
  description: string;
  content_type: string;
  content_type_display?: string;
  deliverables: string;
  budget: string | number;
  deadline: string;
  status: string;
  status_display?: string;
  brand?: number;
  brand_email?: string;
  reference_files?: CampaignFile[];
  created_at?: string;
  updated_at?: string;
}

export interface CampaignFile {
  id: number;
  file: string;
  uploaded_at: string;
}

export interface CampaignResponse {
  status: string;
  data: Campaign | Campaign[];
  errors: any[];
}

export interface CampaignFormData {
  title: string;
  description: string;
  content_type: string;
  deliverables: string;
  budget: string | number;
  deadline: string;
  status: string;
  reference_files?: File[];
}

const campaignService = {
  /**
   * Get all campaigns (filtered by user role on backend)
   */
  async getCampaigns(): Promise<CampaignResponse> {
    const response = await apiClient.get('/api/v1/campaigns/');
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
};

export default campaignService;
