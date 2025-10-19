import type { User } from './User';

export interface AuthResponse {
  status: string;
  data: {
    user: User;
    tokens: {
      access: string;
      refresh: string;
    };
  };
  errors: any[];
}
