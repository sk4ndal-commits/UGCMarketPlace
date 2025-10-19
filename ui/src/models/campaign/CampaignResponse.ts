import type { Campaign } from './Campaign';

export interface CampaignResponse {
  status: string;
  data: Campaign | Campaign[];
  errors: any[];
}
