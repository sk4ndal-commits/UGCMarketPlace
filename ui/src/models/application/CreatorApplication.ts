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
  // Use canonical fields only. Views should use template_details?.name and creator (id)
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
