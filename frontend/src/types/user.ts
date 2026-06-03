export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Address {
  id: number;
  street: string;
  city: string;
  zip_code: string;
  country: string;
  is_default: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}
