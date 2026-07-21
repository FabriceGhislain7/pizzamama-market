import { render, screen, act } from "@testing-library/react";
import { CartProvider } from "./CartProvider";
import { useCart } from "./useCart";
import type { Pizza, PizzaSize } from "@/types";

const mockPizza: Pizza = {
  id: 1,
  name: "Margherita",
  slug: "margherita",
  description: "Classica",
  short_description: "Classica",
  base_price: "8.00",
  category: { id: 1, name: "Classiche", slug: "classiche", description: "" },
  image: null,
  is_active: true,
  is_featured: false,
};

const mockSize: PizzaSize = {
  id: 1,
  name: "Media",
  diameter_cm: 28,
  price_multiplier: "1.00",
};

function TestConsumer() {
  const { items, totalItems, totalPrice, addItem, removeItem, clearItems } = useCart();
  return (
    <div>
      <span data-testid="count">{totalItems}</span>
      <span data-testid="price">{totalPrice.toFixed(2)}</span>
      <span data-testid="items">{items.length}</span>
      <button onClick={() => addItem(mockPizza, mockSize)}>Aggiungi</button>
      <button onClick={() => removeItem(1, 1)}>Rimuovi</button>
      <button onClick={() => clearItems()}>Svuota</button>
    </div>
  );
}

describe("CartProvider", () => {
  beforeEach(() => localStorage.clear());

  it("starts empty", () => {
    render(<CartProvider><TestConsumer /></CartProvider>);
    expect(screen.getByTestId("count").textContent).toBe("0");
  });

  it("adds item and updates totals", async () => {
    render(<CartProvider><TestConsumer /></CartProvider>);
    await act(async () => screen.getByText("Aggiungi").click());
    expect(screen.getByTestId("count").textContent).toBe("1");
    expect(screen.getByTestId("price").textContent).toBe("8.00");
  });

  it("removes item", async () => {
    render(<CartProvider><TestConsumer /></CartProvider>);
    await act(async () => screen.getByText("Aggiungi").click());
    await act(async () => screen.getByText("Rimuovi").click());
    expect(screen.getByTestId("count").textContent).toBe("0");
  });

  it("clears all items", async () => {
    render(<CartProvider><TestConsumer /></CartProvider>);
    await act(async () => screen.getByText("Aggiungi").click());
    await act(async () => screen.getByText("Svuota").click());
    expect(screen.getByTestId("items").textContent).toBe("0");
  });
});
