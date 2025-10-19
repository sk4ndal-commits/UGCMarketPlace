export interface Application {
  id?: number;
  campaign: number;
  campaign_title?: string;
  influencer?: number;
  influencer_email?: string;
  influencer_followers?: number;
  influencer_engagement_rate?: string | number;
  influencer_platform?: string;
  pitch: string;
  portfolio_link?: string;
  proposed_price?: string | number;
  status?: string;
  status_display?: string;
  created_at?: string;
  updated_at?: string;
}
