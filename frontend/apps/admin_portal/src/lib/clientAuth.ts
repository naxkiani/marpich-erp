import {
  type AuthSession as ApiSession,
  apiDelete,
  apiGet,
  apiPost,
  apiPut,
  loadSession,
  loginSession,
  saveSession,
} from "@marpich/auth-provider";

export type { ApiSession };
export { apiDelete, apiGet, apiPost, apiPut, loadSession, saveSession };

export function createClientLogin(displayName: string) {
  return (tenantId: string, email: string, password: string): Promise<ApiSession> =>
    loginSession({ tenantId, email, password, displayName, registerIfMissing: true });
}
