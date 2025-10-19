import type { CampaignFile } from './CampaignFile';

export interface Campaign {
  id?: number;
  title: string;
  description: string;
  content_type: string;
  content_type_display?: string;
  category: string;
  category_display?: string;
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

