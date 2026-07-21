import { httpClient } from "@/services/api/httpClient";
import type { Order } from "@/types";
import type { PaginatedResponse } from "@/types";

export const ordersApi = {
  getMyOrders: () => httpClient.get<PaginatedResponse<Order>>("/orders/"),
  getOrder: (id: string) => httpClient.get<Order>(`/orders/${id}/`),
};
