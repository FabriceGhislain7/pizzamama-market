import { httpClient } from "@/services/api/httpClient";
import type { AuthTokens } from "@/types";

interface LoginPayload {
  username: string;
  password: string;
}

interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export const authApi = {
  login: (payload: LoginPayload) =>
    httpClient.post<AuthTokens>("/auth/login/", payload, { skipAuth: true }),

  register: (payload: RegisterPayload) =>
    httpClient.post<{ username: string; email: string }>(
      "/accounts/register/",
      payload,
      { skipAuth: true },
    ),

  refresh: (refreshToken: string) =>
    httpClient.post<{ access: string }>("/auth/refresh/", { refresh: refreshToken }, { skipAuth: true }),

  logout: (refreshToken: string) =>
    httpClient.post<void>("/accounts/logout/", { refresh: refreshToken }),
};
