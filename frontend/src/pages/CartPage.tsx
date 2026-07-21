import { useNavigate } from "react-router-dom";
import { useCart } from "@/features/cart";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/state";

export function CartPage() {
  const { items, totalPrice, totalItems, removeItem, updateQuantity } = useCart();
  const navigate = useNavigate();

  if (items.length === 0) {
    return (
      <div style={{ padding: "var(--space-8) var(--space-4)", maxWidth: 680, margin: "0 auto" }}>
        <EmptyState title="Carrello vuoto" description="Sfoglia il menu e aggiungi le tue pizze preferite." />
      </div>
    );
  }

  return (
    <div style={{ padding: "var(--space-6) var(--space-4)", maxWidth: 680, margin: "0 auto" }}>
      <h1 style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-5)" }}>
        Carrello ({totalItems} {totalItems === 1 ? "articolo" : "articoli"})
      </h1>

      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
        {items.map((item) => (
          <div
            key={`${item.pizza.id}-${item.size.id}`}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "var(--space-4)",
              background: "#fff",
              border: "1px solid var(--color-border)",
              borderRadius: "var(--radius-md)",
              gap: "var(--space-3)",
            }}
          >
            <div style={{ flex: 1 }}>
              <p style={{ fontWeight: 600, margin: 0 }}>{item.pizza.name}</p>
              <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-muted)", margin: 0 }}>
                {item.size.name}
              </p>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
              <button
                onClick={() => item.quantity > 1
                  ? updateQuantity(item.pizza.id, item.size.id, item.quantity - 1)
                  : removeItem(item.pizza.id, item.size.id)
                }
                style={{ width: 28, height: 28, borderRadius: "var(--radius-sm)", border: "1px solid var(--color-border)", background: "#fff", cursor: "pointer", fontWeight: 700 }}
              >-</button>
              <span style={{ minWidth: 20, textAlign: "center" }}>{item.quantity}</span>
              <button
                onClick={() => updateQuantity(item.pizza.id, item.size.id, item.quantity + 1)}
                style={{ width: 28, height: 28, borderRadius: "var(--radius-sm)", border: "1px solid var(--color-border)", background: "#fff", cursor: "pointer", fontWeight: 700 }}
              >+</button>
            </div>

            <span style={{ fontWeight: 700, color: "var(--color-primary)", minWidth: 60, textAlign: "right" }}>
              €{((item.unitPrice + item.extraCost) * item.quantity).toFixed(2)}
            </span>

            <button
              onClick={() => removeItem(item.pizza.id, item.size.id)}
              style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text-muted)", fontSize: "var(--font-size-lg)" }}
            >×</button>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "var(--space-5)", padding: "var(--space-4) 0", borderTop: "2px solid var(--color-border)" }}>
        <span style={{ fontSize: "var(--font-size-xl)", fontWeight: 700 }}>
          Totale: €{totalPrice.toFixed(2)}
        </span>
        <Button variant="primary" onClick={() => navigate("/checkout")}>
          Procedi al checkout →
        </Button>
      </div>
    </div>
  );
}
