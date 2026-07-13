export { AuthProvider, useAuthContext } from "./AuthProvider";
export { useAuth, useAuthorization, useLoginForm, usePermission } from "./hooks";
export { LoginGate } from "./LoginGate";
export type { LoginGateProps } from "./LoginGate";
export { PasskeyLoginButton } from "./PasskeyLoginButton";
export type { PasskeyLoginButtonProps } from "./PasskeyLoginButton";

export { loginWithPasskey, isWebAuthnSupported, beginPasskeyLogin, completePasskeyLogin } from "./webauthn";
export type { AuthenticationCredentialJSON, PublicKeyCredentialRequestOptionsJSON } from "./webauthn";

export { apiDelete, apiGet, apiPost, apiPut } from "./api-client";
export {
  fetchCurrentUser,
  getStoredSession,
  loginSession,
  logoutSession,
  refreshSession,
  registerUser,
} from "./auth-service";
export { checkAuthorization, fetchPrincipalPermissions } from "./authorization-service";
export {
  API_URL,
  SESSION_COOKIE_NAME,
  SESSION_COOKIE_VALUE,
  SESSION_STORAGE_KEY,
} from "./config";
export { clearSessionCookie, setSessionCookie } from "./cookie";
export {
  authHeaders,
  clearSession,
  isSessionExpired,
  loadSession,
  saveSession,
  tenantHeaders,
} from "./session";

export type {
  ApiSession,
  AuthSession,
  AuthUser,
  AuthorizationCheckInput,
  AuthorizationCheckResult,
  LoginCredentials,
  PrincipalPermissions,
} from "./types";
