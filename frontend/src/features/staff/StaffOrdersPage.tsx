import { useReducer, useEffect } from "react";
import { staffApi } from "./staffApi";
import { toUserMessage } from "@/services/api/apiErrors";
import { LoadingState, ErrorState, EmptyState } from "@/components/state";
import type { Order, OrderStatus } from "@/types";

const NEXT_STATUS: Partial<Record<OrderStatus, OrderStatus>> = {
  pending: "confirmed",
  confirmed: "preparing",
  preparing: "ready",
  ready: "out_for_delivery",
  out_for_delivery: "delivered",
};

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

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; orders: Order[] };

type Action =
  | { type: "LOAD_START" }
  | { type: "LOAD_DONE"; orders: Order[] }
  | { type: "LOAD_ERROR"; message: string }
  | { type: "UPDATE_ORDER"; order: Order };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "LOAD_START": return { status: "loading" };
    case "LOAD_DONE": return { status: "ready", orders: action.orders };
    case "LOAD_ERROR": return { status: "error", message: action.message };
    case "UPDATE_ORDER":
      if (state.status !== "ready") return state;
      return {
        ...state,
        orders: state.orders.map((o) => o.id === action.order.id ? action.order : o),
      };
    default: return state;
  }
}

export function StaffOrdersPage() {
  const [state, dispatch] = useReducer(reducer, { status: "loading" });

  useEffect(() => {
    dispatch({ type: "LOAD_START" });
    staffApi.getAllOrders()
      .then((data) => dispatch({ type: "LOAD_DONE", orders: data.results }))
      .catch((err: unknown) => dispatch({ type: "LOAD_ERROR", message: toUserMessage(err) }));
  }, []);

  async function handleAdvance(order: Order) {
    const next = NEXT_STATUS[order.status];
    if (!next) return;
    try {
      await staffApi.changeStatus(order.id, next);
      dispatch({ type: "UPDATE_ORDER", order: { ...order, status: next } });
    } catch {
      alert("Impossibile aggiornare lo stato.");
    }
  }

  if (state.status === "loading") return <LoadingState message="Caricamento ordini..." />;
  if (state.status === "error") return <ErrorState message={state.message} />;

  return (
    <div style={{ maxWidth: 900, margin: "var(--space-8) auto", padding: "0 var(--space-4)" }}>
      <h1 style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-5)" }}>
        Gestione ordini — Staff
      </h1>

      {state.orders.length === 0 ? (
        <EmptyState title="Nessun ordine attivo" />
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
          {state.orders.map((order) => (
            <div key={order.id} style={{
              background: "#fff",
              border: "1px solid var(--color-border)",
              borderRadius: "var(--radius-md)",
              padding: "var(--space-4)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: "var(--space-3)",
            }}>
              <div>
                <p style={{ fontWeight: 700, margin: "0 0 4px" }}>{order.order_number}</p>
                <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-muted)", margin: 0 }}>
                  {STATUS_LABEL[order.status]} · €{order.total_amount}
                </p>
              </div>
              {NEXT_STATUS[order.status] && (
                <button
                  onClick={() => void handleAdvance(order)}
                  style={{
                    padding: "var(--space-2) var(--space-3)",
                    background: "var(--color-primary)",
                    color: "#fff",
                    border: "none",
                    borderRadius: "var(--radius-sm)",
                    cursor: "pointer",
                    fontSize: "var(--font-size-sm)",
                    fontWeight: 600,
                  }}
                >
                  → {STATUS_LABEL[NEXT_STATUS[order.status]!]}
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
