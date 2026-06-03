export type { Category, Allergen, Ingredient, PizzaSize, Pizza } from "./product";
export type { OrderStatus, OrderType, OrderItem, Order, CartItem } from "./order";
export type { User, Address, AuthTokens } from "./user";

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
