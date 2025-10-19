export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'BRAND' | 'INFLUENCER' | 'CREATOR' | null;
  is_email_verified: boolean;
  gdpr_consent: boolean;
  created_at: string;
  updated_at: string;
}
