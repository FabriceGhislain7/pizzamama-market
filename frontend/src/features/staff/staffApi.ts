import { httpClient } from "@/services/api/httpClient";
import type { Order, OrderStatus } from "@/types";
import type { PaginatedResponse } from "@/types";

export const staffApi = {
  getAllOrders: (status?: OrderStatus) => {
    const qs = status ? `?status=${status}` : "";
    return httpClient.get<PaginatedResponse<Order>>(`/orders/${qs}`);
  },

  changeStatus: (orderId: string, newStatus: OrderStatus) =>
    httpClient.post<{ detail: string }>(`/orders/${orderId}/change-status/`, {
      status: newStatus,
    }),
};
