"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { checkAuthorization, fetchPrincipalPermissions } from "./authorization-service";
import {
  fetchCurrentUser,
  getStoredSession,
  loginSession,
  logoutSession,
  refreshSession,
} from "./auth-service";
import { isSessionExpired } from "./session";
import type {
  AuthorizationCheckInput,
  AuthorizationCheckResult,
  AuthSession,
  AuthUser,
  LoginCredentials,
  PrincipalPermissions,
} from "./types";

type AuthContextValue = {
  session: AuthSession | null;
  user: AuthUser | null;
  permissions: string[];
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<AuthSession>;
  logout: () => Promise<void>;
  refresh: () => Promise<AuthSession | null>;
  reloadUser: () => Promise<AuthUser | null>;
  hasPermission: (code: string) => boolean;
  checkAccess: (input: AuthorizationCheckInput) => Promise<AuthorizationCheckResult>;
  resolvePrincipalPermissions: (principalId: string) => Promise<PrincipalPermissions>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

type AuthProviderProps = {
  children: ReactNode;
  autoRefresh?: boolean;
};

export function AuthProvider({ children, autoRefresh = true }: AuthProviderProps) {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const permissions = user?.permissions ?? [];

  const reloadUser = useCallback(async (active: AuthSession): Promise<AuthUser | null> => {
    try {
      const me = await fetchCurrentUser(active);
      const nextSession: AuthSession = { ...active, userId: me.id };
      setSession(nextSession);
      setUser(me);
      setError(null);
      return me;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load user profile");
      return null;
    }
  }, []);

  const refresh = useCallback(async (): Promise<AuthSession | null> => {
    const current = session ?? getStoredSession();
    if (!current) return null;
    try {
      const next = autoRefresh && isSessionExpired(current) ? await refreshSession(current) : current;
      setSession(next);
      await reloadUser(next);
      setError(null);
      return next;
    } catch (err) {
      setSession(null);
      setUser(null);
      setError(err instanceof Error ? err.message : "Session refresh failed");
      return null;
    }
  }, [autoRefresh, reloadUser, session]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const stored = getStoredSession();
      if (!stored) {
        if (!cancelled) setIsLoading(false);
        return;
      }
      try {
        const active =
          autoRefresh && isSessionExpired(stored) ? await refreshSession(stored) : stored;
        if (cancelled) return;
        setSession(active);
        await reloadUser(active);
      } catch (err) {
        if (!cancelled) {
          setSession(null);
          setUser(null);
          setError(err instanceof Error ? err.message : "Failed to restore session");
        }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [autoRefresh, reloadUser]);

  const login = useCallback(
    async (credentials: LoginCredentials): Promise<AuthSession> => {
      setIsLoading(true);
      setError(null);
      try {
        const next = await loginSession(credentials);
        setSession(next);
        await reloadUser(next);
        return next;
      } catch (err) {
        const message = err instanceof Error ? err.message : "Login failed";
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [reloadUser],
  );

  const logout = useCallback(async (): Promise<void> => {
    const current = session ?? getStoredSession();
    if (current) await logoutSession(current);
    setSession(null);
    setUser(null);
    setError(null);
  }, [session]);

  const hasPermission = useCallback(
    (code: string) => permissions.includes(code),
    [permissions],
  );

  const checkAccess = useCallback(
    async (input: AuthorizationCheckInput): Promise<AuthorizationCheckResult> => {
      const active = session ?? getStoredSession();
      if (!active) throw new Error("Not authenticated");
      return checkAuthorization(active, {
        ...input,
        principalId: input.principalId ?? active.userId ?? user?.id,
      });
    },
    [session, user?.id],
  );

  const resolvePrincipalPermissions = useCallback(
    async (principalId: string): Promise<PrincipalPermissions> => {
      const active = session ?? getStoredSession();
      if (!active) throw new Error("Not authenticated");
      return fetchPrincipalPermissions(active, principalId);
    },
    [session],
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      session,
      user,
      permissions,
      isAuthenticated: Boolean(session?.accessToken),
      isLoading,
      error,
      login,
      logout,
      refresh,
      reloadUser: async () => {
        const active = session ?? getStoredSession();
        return active ? reloadUser(active) : null;
      },
      hasPermission,
      checkAccess,
      resolvePrincipalPermissions,
    }),
    [
      session,
      user,
      permissions,
      isLoading,
      error,
      login,
      logout,
      refresh,
      reloadUser,
      hasPermission,
      checkAccess,
      resolvePrincipalPermissions,
    ],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
