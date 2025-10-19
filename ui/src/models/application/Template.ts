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
