import { useAsync } from "@/hooks/useAsync";
import { dashboardApi } from "./dashboardApi";
import { LoadingState, ErrorState } from "@/components/state";

function KpiCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={{
      background: "#fff",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-md)",
      padding: "var(--space-5)",
      textAlign: "center",
    }}>
      <p style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, margin: "0 0 4px", color: "var(--color-primary)" }}>
        {value}
      </p>
      <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-muted)", margin: 0 }}>{label}</p>
    </div>
  );
}

export function DashboardPage() {
  const { state } = useAsync(() => dashboardApi.getDashboard(), []);

  if (state.status === "loading") return <LoadingState message="Caricamento dashboard..." />;
  if (state.status === "error") return <ErrorState message={state.message} />;
  if (state.status !== "success") return null;

  const { today, top_products } = state.data;

  return (
    <div style={{ maxWidth: 900, margin: "var(--space-8) auto", padding: "0 var(--space-4)" }}>
      <h1 style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-6)" }}>
        Dashboard Manager
      </h1>

      <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)" }}>Oggi</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "var(--space-4)", marginBottom: "var(--space-6)" }}>
        <KpiCard label="Ricavi" value={`€${today.total_revenue ?? "0"}`} />
        <KpiCard label="Ordini" value={today.total_orders ?? 0} />
        <KpiCard label="Valore medio" value={`€${today.avg_order_value ?? "0"}`} />
      </div>

      {top_products.length > 0 && (
        <>
          <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)" }}>
            Top prodotti
          </h2>
          <div style={{ background: "#fff", border: "1px solid var(--color-border)", borderRadius: "var(--radius-md)", overflow: "hidden" }}>
            {top_products.map((p, i) => (
              <div key={p.pizza__name} style={{
                display: "flex",
                justifyContent: "space-between",
                padding: "var(--space-3) var(--space-4)",
                borderBottom: i < top_products.length - 1 ? "1px solid var(--color-border)" : "none",
                fontSize: "var(--font-size-sm)",
              }}>
                <span>{i + 1}. {p.pizza__name}</span>
                <strong>{p.total_sold} vendute</strong>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
