import { httpClient } from "@/services/api/httpClient";
import type { Order, OrderType } from "@/types";

export interface CreateOrderPayload {
  order_type: OrderType;
  subtotal: string;
  delivery_fee: string;
  tax_amount: string;
  discount_amount: string;
  total_amount: string;
  delivery_address?: number;
}

export const checkoutApi = {
  createOrder: (payload: CreateOrderPayload) =>
    httpClient.post<Order>("/orders/", payload),
};
