export type AuthSession = {
  tenantId: string;
  /** Never persisted in sessionStorage. Browser traffic uses the HttpOnly BFF cookie. */
  accessToken?: string;
  /** Never persisted in sessionStorage. Refresh uses the HttpOnly BFF cookie. */
  refreshToken?: string;
  expiresAt?: number;
  userId?: string;
};

/** @deprecated Use AuthSession */
export type ApiSession = AuthSession;

export type AuthUser = {
  id: string;
  email: string;
  display_name?: string;
  permissions: string[];
  roles: string[];
  [key: string]: unknown;
};

export type LoginCredentials = {
  tenantId: string;
  email: string;
  password: string;
  displayName?: string;
  registerIfMissing?: boolean;
};

export type AuthorizationCheckInput = {
  resource?: string;
  action?: string;
  permissionCode?: string;
  principalId?: string;
  context?: Record<string, unknown>;
};

export type AuthorizationCheckResult = {
  allowed: boolean;
  reason?: string;
  decision_id?: string;
  [key: string]: unknown;
};

export type PrincipalPermissions = {
  principal_id: string;
  permissions: string[];
  roles?: string[];
  [key: string]: unknown;
};
