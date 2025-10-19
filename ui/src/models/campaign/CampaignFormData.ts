export interface CampaignFormData {
  title: string;
  description: string;
  content_type: string;
  category: string;
  deliverables: string;
  budget: string | number;
  deadline: string;
  status: string;
  reference_files?: File[];
}
