import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div style={{ textAlign: "center", padding: "4rem 0" }}>
      <h1>404 — Pagina non trovata</h1>
      <p>La pagina che cerchi non esiste.</p>
      <Link to="/">Torna alla home</Link>
    </div>
  );
}
