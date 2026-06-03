import type { Pizza, PizzaSize } from "./product";

export type OrderStatus =
  | "pending"
  | "confirmed"
  | "preparing"
  | "ready"
  | "out_for_delivery"
  | "delivered"
  | "cancelled"
  | "refunded";

export type OrderType = "delivery" | "pickup" | "dine_in";

export interface OrderItem {
  id: number;
  pizza: Pizza;
  size: PizzaSize;
  quantity: number;
  unit_price: string;
  extra_cost: string;
}

export interface Order {
  id: string;
  order_number: string;
  order_type: OrderType;
  status: OrderStatus;
  subtotal: string;
  delivery_fee: string;
  tax_amount: string;
  discount_amount: string;
  total_amount: string;
  items: OrderItem[];
  confirmed_at: string | null;
  delivered_at: string | null;
  created_at: string;
}

// Carrello locale (pre-ordine)
export interface CartItem {
  pizza: Pizza;
  size: PizzaSize;
  quantity: number;
  unitPrice: number;
  extraCost: number;
}
