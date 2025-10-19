import type { Template } from './Template';

export interface CreatorApplication {
  id?: number;
  application_id?: string;
  name: string;
  description: string;
  owner: string;
  visibility: string;
  template?: number;
  template_details?: Template;
  // Some views expect a derived template_name and creator_email fields
  template_name?: string;
  creator_email?: string;
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
