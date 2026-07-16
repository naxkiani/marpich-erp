import { apiGet, apiPost } from "./api-client";
import type {
  AuthorizationCheckInput,
  AuthorizationCheckResult,
  AuthSession,
  PrincipalPermissions,
} from "./types";

export async function checkAuthorization(
  session: AuthSession,
  input: AuthorizationCheckInput,
): Promise<AuthorizationCheckResult> {
  return apiPost<AuthorizationCheckResult>("/api/v1/authorization/check", session, {
    principal_id: input.principalId,
    resource: input.resource ?? "",
    action: input.action ?? "",
    permission_code: input.permissionCode,
    context: input.context ?? {},
  });
}

export async function fetchPrincipalPermissions(
  session: AuthSession,
  principalId: string,
): Promise<PrincipalPermissions> {
  return apiGet<PrincipalPermissions>(`/api/v1/permissions/principals/${principalId}/permissions`, session);
}
