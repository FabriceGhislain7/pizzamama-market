import { Navigate } from "react-router-dom";
import { useAuth } from "@/features/auth";

declare module "@/features/auth/authContext" {
  interface AuthUser {
    groups?: string[];
  }
}

// Per ora controlla solo isAuthenticated — il controllo ruolo richiede
// un endpoint /me/ che restituisce i gruppi (non ancora implementato).
// La protezione vera avviene sul backend (403 se non Manager/IT_Admin).
export function StaffRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}
