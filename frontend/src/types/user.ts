export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Address {
  id: string;
  label: string;
  street_address: string;
  city: string;
  postal_code: string;
  province: string;
  country: string;
  is_default: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}
