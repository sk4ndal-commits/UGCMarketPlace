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
