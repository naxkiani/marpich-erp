import {
  type ApiSession,
  apiGet,
  apiPost,
} from "./clientAuth";

export type { ApiSession };

export type IdentityMe = {
  id: string;
  email: string;
  display_name?: string;
  mfa_enabled: boolean;
  password_must_change?: boolean;
  password_changed_at?: string | null;
  permissions?: string[];
  roles?: string[];
};

export type MfaSetupResult = {
  secret: string;
  provisioning_uri: string;
};

export type MfaVerifyResult = {
  mfa_enabled: boolean;
  backup_codes: string[];
};

export type ChangePasswordResult = {
  password_changed: boolean;
  password_must_change: boolean;
  password_changed_at?: string | null;
  other_sessions_revoked: boolean;
};

export async function fetchIdentityMe(session: ApiSession): Promise<IdentityMe> {
  return apiGet("/api/v1/users/me", session);
}

export async function setupMfa(session: ApiSession): Promise<MfaSetupResult> {
  return apiPost("/api/v1/users/me/mfa/setup", session, {});
}

export async function verifyMfaSetup(
  session: ApiSession,
  code: string,
): Promise<MfaVerifyResult> {
  return apiPost("/api/v1/users/me/mfa/verify", session, { code });
}

export async function changePassword(
  session: ApiSession,
  input: {
    current_password: string;
    new_password: string;
    revoke_other_sessions?: boolean;
  },
): Promise<ChangePasswordResult> {
  return apiPost("/api/v1/users/me/password", session, {
    current_password: input.current_password,
    new_password: input.new_password,
    revoke_other_sessions: input.revoke_other_sessions ?? true,
  });
}
