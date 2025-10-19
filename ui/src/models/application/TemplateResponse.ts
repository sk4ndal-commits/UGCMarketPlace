import type { Template } from './Template';

export interface TemplateResponse {
  status: string;
  data: Template | Template[];
  errors: any[];
}
