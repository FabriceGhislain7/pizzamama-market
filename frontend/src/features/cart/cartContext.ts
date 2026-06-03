import { createContext } from "react";
import type { Pizza, PizzaSize, CartItem } from "@/types";

export interface CartContextValue {
  items: CartItem[];
  totalItems: number;
  totalPrice: number;
  addItem: (pizza: Pizza, size: PizzaSize, quantity?: number) => void;
  removeItem: (pizzaId: number, sizeId: number) => void;
  updateQuantity: (pizzaId: number, sizeId: number, quantity: number) => void;
  clearItems: () => void;
}

export const CartContext = createContext<CartContextValue | null>(null);
