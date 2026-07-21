import { useAsync } from "@/hooks/useAsync";
import { ordersApi } from "./ordersApi";
import { LoadingState, ErrorState, EmptyState } from "@/components/state";
import type { Order, OrderStatus } from "@/types";

const STATUS_LABEL: Record<OrderStatus, string> = {
  pending: "In attesa",
  confirmed: "Confermato",
  preparing: "In preparazione",
  ready: "Pronto",
  out_for_delivery: "In consegna",
  delivered: "Consegnato",
  cancelled: "Annullato",
  refunded: "Rimborsato",
};

const STATUS_COLOR: Record<OrderStatus, string> = {
  pending: "#f59e0b",
  confirmed: "#3b82f6",
  preparing: "#8b5cf6",
  ready: "#10b981",
  out_for_delivery: "#6366f1",
  delivered: "#22c55e",
  cancelled: "#ef4444",
  refunded: "#6b7280",
};

function OrderCard({ order }: { order: Order }) {
  return (
    <div style={{
      background: "#fff",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-md)",
      padding: "var(--space-4)",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "var(--space-2)" }}>
        <div>
          <p style={{ fontWeight: 700, margin: 0 }}>{order.order_number}</p>
          <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-muted)", margin: 0 }}>
            {new Date(order.created_at).toLocaleDateString("it-IT", { day: "2-digit", month: "short", year: "numeric" })}
          </p>
        </div>
        <span style={{
          fontSize: "var(--font-size-xs)",
          fontWeight: 600,
          padding: "3px 10px",
          borderRadius: "var(--radius-sm)",
          background: STATUS_COLOR[order.status] + "20",
          color: STATUS_COLOR[order.status],
        }}>
          {STATUS_LABEL[order.status]}
        </span>
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "var(--font-size-sm)" }}>
        <span style={{ color: "var(--color-text-muted)" }}>
          {order.order_type === "delivery" ? "🛵 Consegna" : order.order_type === "pickup" ? "🏪 Ritiro" : "🍽️ In sede"}
        </span>
        <span style={{ fontWeight: 700, color: "var(--color-primary)" }}>€{order.total_amount}</span>
      </div>
    </div>
  );
}

export function OrdersPage() {
  const { state } = useAsync(() => ordersApi.getMyOrders(), []);

  if (state.status === "loading") return <LoadingState message="Caricamento ordini..." />;
  if (state.status === "error") return <ErrorState message={state.message} />;
  if (state.status !== "success") return null;

  const orders = state.data.results;

  return (
    <div style={{ maxWidth: 680, margin: "var(--space-8) auto", padding: "0 var(--space-4)" }}>
      <h1 style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-5)" }}>
        I miei ordini
      </h1>
      {orders.length === 0 ? (
        <EmptyState title="Nessun ordine" description="Non hai ancora effettuato ordini." />
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
          {orders.map((order) => <OrderCard key={order.id} order={order} />)}
        </div>
      )}
    </div>
  );
}
