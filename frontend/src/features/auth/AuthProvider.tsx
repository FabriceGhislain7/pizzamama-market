import { useState, useCallback, type ReactNode } from "react";
import { AuthContext, type AuthUser } from "./authContext";
import { authApi } from "./authApi";
import { authStorage } from "./authStorage";

function getUserFromStorage(): AuthUser | null {
  const token = authStorage.getAccess();
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return { username: payload.username ?? payload.user_id ?? "utente" };
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(getUserFromStorage);

  const login = useCallback(async (username: string, password: string) => {
    const tokens = await authApi.login({ username, password });
    authStorage.save(tokens.access, tokens.refresh);
    setUser(getUserFromStorage());
  }, []);

  const logout = useCallback(async () => {
    const refresh = authStorage.getRefresh();
    if (refresh) {
      try {
        await authApi.logout(refresh);
      } catch {
        // blacklist best-effort
      }
    }
    authStorage.clear();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: user !== null, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
