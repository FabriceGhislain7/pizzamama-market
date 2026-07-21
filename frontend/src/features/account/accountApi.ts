import { httpClient } from "@/services/api/httpClient";
import type { Address } from "@/types";
import type { PaginatedResponse } from "@/types";

interface ExportData {
  user: { id: string; username: string; email: string; date_joined: string | null };
  addresses: Record<string, unknown>[];
  orders: Record<string, unknown>[];
}

export const accountApi = {
  getAddresses: () =>
    httpClient.get<PaginatedResponse<Address>>("/accounts/addresses/"),

  exportData: () =>
    httpClient.get<ExportData>("/accounts/me/export/"),
};
