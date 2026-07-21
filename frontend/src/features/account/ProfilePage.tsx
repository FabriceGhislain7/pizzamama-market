import { useAuth } from "@/features/auth";
import { useAsync } from "@/hooks/useAsync";
import { accountApi } from "./accountApi";
import { LoadingState, ErrorState } from "@/components/state";

export function ProfilePage() {
  const { user } = useAuth();
  const { state: addrState } = useAsync(() => accountApi.getAddresses(), []);

  return (
    <div style={{ maxWidth: 680, margin: "var(--space-8) auto", padding: "0 var(--space-4)" }}>
      <h1 style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-5)" }}>
        Il mio profilo
      </h1>

      <div style={{ background: "#fff", border: "1px solid var(--color-border)", borderRadius: "var(--radius-md)", padding: "var(--space-5)", marginBottom: "var(--space-4)" }}>
        <p style={{ fontWeight: 600, marginBottom: "var(--space-2)" }}>Account</p>
        <p style={{ margin: 0 }}>Username: <strong>{user?.username}</strong></p>
      </div>

      <div style={{ background: "#fff", border: "1px solid var(--color-border)", borderRadius: "var(--radius-md)", padding: "var(--space-5)" }}>
        <p style={{ fontWeight: 600, marginBottom: "var(--space-3)" }}>Indirizzi di consegna</p>

        {addrState.status === "loading" && <LoadingState message="Caricamento indirizzi..." />}
        {addrState.status === "error" && <ErrorState message={addrState.message} />}
        {addrState.status === "success" && (
          addrState.data.results.length === 0 ? (
            <p style={{ color: "var(--color-text-muted)", fontSize: "var(--font-size-sm)" }}>
              Nessun indirizzo salvato.
            </p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
              {addrState.data.results.map((addr) => (
                <div key={addr.id} style={{ fontSize: "var(--font-size-sm)", padding: "var(--space-2) 0", borderBottom: "1px solid var(--color-border)" }}>
                  {addr.label && <strong>{addr.label} — </strong>}
                  {addr.street_address}, {addr.city}
                  {addr.is_default && <span style={{ marginLeft: 8, color: "var(--color-primary)", fontSize: "var(--font-size-xs)" }}>Predefinito</span>}
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </div>
  );
}
