"use client";

import { useAuthContext } from "./AuthProvider";
import type { AuthorizationCheckInput, LoginCredentials } from "./types";

export function useAuth() {
  return useAuthContext();
}

export function usePermission(code: string): boolean {
  const { hasPermission, isLoading } = useAuthContext();
  if (isLoading) return false;
  return hasPermission(code);
}

export function useAuthorization() {
  const { checkAccess, resolvePrincipalPermissions, hasPermission, permissions } = useAuthContext();

  return {
    permissions,
    hasPermission,
    checkAccess: (input: AuthorizationCheckInput) => checkAccess(input),
    resolvePrincipalPermissions,
  };
}

export type UseLoginOptions = {
  defaultTenantId?: string;
  defaultEmail?: string;
  defaultPassword?: string;
  displayName?: string;
  onSuccess?: () => void;
};

export function useLoginForm(options: UseLoginOptions = {}) {
  const { login, isLoading, error } = useAuthContext();
  const {
    defaultTenantId = "marpich-demo",
    defaultEmail = "admin@marpich.dev",
    defaultPassword = "SecurePass123!",
    displayName = "Marpich Admin",
    onSuccess,
  } = options;

  async function submit(
    tenantId: string,
    email: string,
    password: string,
  ): Promise<void> {
    const credentials: LoginCredentials = {
      tenantId,
      email,
      password,
      displayName,
      registerIfMissing: true,
    };
    await login(credentials);
    onSuccess?.();
  }

  return {
    defaultTenantId,
    defaultEmail,
    defaultPassword,
    submit,
    isLoading,
    error,
  };
}
