import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "@/features/cart";
import { checkoutApi } from "./checkoutApi";
import { toUserMessage } from "@/services/api/apiErrors";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/state";
import type { OrderType } from "@/types";
import styles from "./CheckoutPage.module.css";

const DELIVERY_FEE = 2.5;

export function CheckoutPage() {
  const { items, totalPrice, clearItems } = useCart();
  const navigate = useNavigate();
  const [orderType, setOrderType] = useState<OrderType>("delivery");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (items.length === 0) {
    return (
      <div className={styles.page}>
        <EmptyState title="Carrello vuoto" description="Aggiungi delle pizze dal menu prima di procedere." />
      </div>
    );
  }

  const fee = orderType === "delivery" ? DELIVERY_FEE : 0;
  const total = totalPrice + fee;

  async function handleOrder() {
    setError(null);
    setLoading(true);
    try {
      await checkoutApi.createOrder({
        order_type: orderType,
        subtotal: totalPrice.toFixed(2),
        delivery_fee: fee.toFixed(2),
        tax_amount: "0.00",
        discount_amount: "0.00",
        total_amount: total.toFixed(2),
      });
      clearItems();
      navigate("/orders");
    } catch (err) {
      setError(toUserMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Checkout</h1>

      <div className={styles.section}>
        <p className={styles.sectionTitle}>Tipo ordine</p>
        <div className={styles.typeRow}>
          {(["delivery", "pickup", "dine_in"] as OrderType[]).map((t) => (
            <button
              key={t}
              className={`${styles.typeBtn} ${orderType === t ? styles.selected : ""}`}
              onClick={() => setOrderType(t)}
            >
              {t === "delivery" ? "🛵 Consegna" : t === "pickup" ? "🏪 Ritiro" : "🍽️ In sede"}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.section}>
        <p className={styles.sectionTitle}>Riepilogo</p>
        {items.map((item) => (
          <div key={`${item.pizza.id}-${item.size.id}`} className={styles.cartLine}>
            <span>{item.pizza.name} × {item.quantity}</span>
            <span>€{((item.unitPrice + item.extraCost) * item.quantity).toFixed(2)}</span>
          </div>
        ))}
        {fee > 0 && (
          <div className={styles.cartLine}>
            <span>Consegna</span>
            <span>€{fee.toFixed(2)}</span>
          </div>
        )}
        <div className={styles.totalRow}>
          <span>Totale</span>
          <span>€{total.toFixed(2)}</span>
        </div>
      </div>

      {error && <p className={styles.error}>{error}</p>}

      <div className={styles.actions}>
        <Button variant="primary" loading={loading} onClick={() => void handleOrder()}>
          Conferma ordine
        </Button>
      </div>
    </div>
  );
}
