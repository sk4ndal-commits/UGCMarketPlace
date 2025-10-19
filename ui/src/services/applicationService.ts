import apiClient from './api';

export interface Template {
  id: number;
  template_id: string;
  name: string;
  description: string;
  is_available: boolean;
  default_parameters: Record<string, any>;
  required_parameters: string[];
  created_at: string;
  updated_at: string;
}

export interface CreatorApplication {
  id?: number;
  application_id?: string;
  name: string;
  description: string;
  owner: string;
  visibility: string;
  template?: number;
  template_details?: Template;
  parameters?: Record<string, any>;
  git_integration?: {
    repository_url?: string;
    branch?: string;
    [key: string]: any;
  };
  oidc_integration?: {
    provider?: string;
    client_id?: string;
    [key: string]: any;
  };
  creator?: number;
  created_at?: string;
  updated_at?: string;
}

export interface CreatorApplicationFormData {
  name: string;
  description: string;
  owner: string;
  visibility: string;
  template_id?: string;
  parameters?: Record<string, any>;
  git_integration?: Record<string, any>;
  oidc_integration?: Record<string, any>;
}

export interface TemplateResponse {
  status: string;
  data: Template | Template[];
  errors: any[];
}

export interface ApplicationResponse {
  status: string;
  data: CreatorApplication | CreatorApplication[];
  errors: any[];
}

const applicationService = {
  /**
   * Get all available templates
   */
  async getTemplates(): Promise<TemplateResponse> {
    const response = await apiClient.get('/api/v1/templates/');
    return response.data;
  },

  /**
   * Get a single template by ID
   */
  async getTemplate(id: number): Promise<TemplateResponse> {
    const response = await apiClient.get(`/api/v1/templates/${id}/`);
    return response.data;
  },

  /**
   * Get all creator applications
   */
  async getApplications(): Promise<ApplicationResponse> {
    const response = await apiClient.get('/api/v1/applications/');
    return response.data;
  },

  /**
   * Get a single application by ID
   */
  async getApplication(id: number): Promise<ApplicationResponse> {
    const response = await apiClient.get(`/api/v1/applications/${id}/`);
    return response.data;
  },

  /**
   * Create a new creator application
   */
  async createApplication(applicationData: CreatorApplicationFormData): Promise<ApplicationResponse> {
    const payload: any = {
      name: applicationData.name,
      description: applicationData.description,
      owner: applicationData.owner,
      visibility: applicationData.visibility,
    };

    // Add optional fields if provided
    if (applicationData.template_id) {
      payload.template_id = applicationData.template_id;
    }

    if (applicationData.parameters && Object.keys(applicationData.parameters).length > 0) {
      payload.parameters = applicationData.parameters;
    }

    if (applicationData.git_integration && Object.keys(applicationData.git_integration).length > 0) {
      payload.git_integration = applicationData.git_integration;
    }

    if (applicationData.oidc_integration && Object.keys(applicationData.oidc_integration).length > 0) {
      payload.oidc_integration = applicationData.oidc_integration;
    }

    const response = await apiClient.post('/api/v1/applications/', payload);
    return response.data;
  },

  /**
   * Update an existing application
   */
  async updateApplication(id: number, applicationData: Partial<CreatorApplicationFormData>): Promise<ApplicationResponse> {
    const payload: any = {};

    if (applicationData.name !== undefined) payload.name = applicationData.name;
    if (applicationData.description !== undefined) payload.description = applicationData.description;
    if (applicationData.owner !== undefined) payload.owner = applicationData.owner;
    if (applicationData.visibility !== undefined) payload.visibility = applicationData.visibility;
    if (applicationData.template_id !== undefined) payload.template_id = applicationData.template_id;
    if (applicationData.parameters !== undefined) payload.parameters = applicationData.parameters;
    if (applicationData.git_integration !== undefined) payload.git_integration = applicationData.git_integration;
    if (applicationData.oidc_integration !== undefined) payload.oidc_integration = applicationData.oidc_integration;

    const response = await apiClient.patch(`/api/v1/applications/${id}/`, payload);
    return response.data;
  },

  /**
   * Delete an application
   */
  async deleteApplication(id: number): Promise<ApplicationResponse> {
    const response = await apiClient.delete(`/api/v1/applications/${id}/`);
    return response.data;
  },

  /**
   * Get application for catalog view
   */
  async getCatalogView(id: number): Promise<ApplicationResponse> {
    const response = await apiClient.get(`/api/v1/applications/${id}/catalog_view/`);
    return response.data;
  },

  /**
   * Get visibility choices for form
   */
  getVisibilityChoices() {
    return [
      { value: 'PUBLIC', label: 'Public' },
      { value: 'INTERNAL', label: 'Internal' },
      { value: 'PRIVATE', label: 'Private' },
    ];
  },
};

export default applicationService;
