import type { CreatorApplication } from './CreatorApplication';

export interface ApplicationResponse {
  status: string;
  data: CreatorApplication | CreatorApplication[];
  errors: any[];
}
