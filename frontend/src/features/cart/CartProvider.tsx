import { useReducer, useEffect } from "react";
import type { CartItem, Pizza, PizzaSize } from "@/types";
import { CartContext } from "./cartContext";
import { loadCart, saveCart, clearCart } from "./cartStorage";

type CartAction =
  | { type: "ADD"; payload: CartItem }
  | { type: "REMOVE"; pizzaId: number; sizeId: number }
  | { type: "UPDATE_QTY"; pizzaId: number; sizeId: number; quantity: number }
  | { type: "CLEAR" };

function cartReducer(state: CartItem[], action: CartAction): CartItem[] {
  switch (action.type) {
    case "ADD": {
      const exists = state.find(
        (i) => i.pizza.id === action.payload.pizza.id && i.size.id === action.payload.size.id,
      );
      if (exists) {
        return state.map((i) =>
          i.pizza.id === action.payload.pizza.id && i.size.id === action.payload.size.id
            ? { ...i, quantity: i.quantity + action.payload.quantity }
            : i,
        );
      }
      return [...state, action.payload];
    }
    case "REMOVE":
      return state.filter(
        (i) => !(i.pizza.id === action.pizzaId && i.size.id === action.sizeId),
      );
    case "UPDATE_QTY":
      return state.map((i) =>
        i.pizza.id === action.pizzaId && i.size.id === action.sizeId
          ? { ...i, quantity: action.quantity }
          : i,
      );
    case "CLEAR":
      return [];
    default:
      return state;
  }
}

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, dispatch] = useReducer(cartReducer, loadCart());

  useEffect(() => {
    saveCart(items);
  }, [items]);

  const totalItems = items.reduce((sum, i) => sum + i.quantity, 0);
  const totalPrice = items.reduce(
    (sum, i) => sum + (i.unitPrice + i.extraCost) * i.quantity,
    0,
  );

  const addItem = (pizza: Pizza, size: PizzaSize, quantity = 1) => {
    const unitPrice = parseFloat(pizza.base_price) * parseFloat(size.price_multiplier);
    dispatch({ type: "ADD", payload: { pizza, size, quantity, unitPrice, extraCost: 0 } });
  };

  const removeItem = (pizzaId: number, sizeId: number) =>
    dispatch({ type: "REMOVE", pizzaId, sizeId });

  const updateQuantity = (pizzaId: number, sizeId: number, quantity: number) =>
    dispatch({ type: "UPDATE_QTY", pizzaId, sizeId, quantity });

  const clearItems = () => {
    dispatch({ type: "CLEAR" });
    clearCart();
  };

  return (
    <CartContext.Provider
      value={{ items, totalItems, totalPrice, addItem, removeItem, updateQuantity, clearItems }}
    >
      {children}
    </CartContext.Provider>
  );
}
