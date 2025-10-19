import type { Application } from './Application';

export interface ApplicationResponse {
  status: string;
  data: Application | Application[];
  errors: any[];
}
