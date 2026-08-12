import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadSecuritySession,
  saveSession as saveSecuritySession,
} from "./clientAuth";

export type { ApiSession };

export const loginSecuritySession = createClientLogin("Integration Security Admin");
export { loadSecuritySession, saveSecuritySession };
export type SecurityCatalog = {
  capabilities: Array<{ capability: string; label: string }>;
  policy_keys: string[];
  oauth2: boolean;
  openid_connect: boolean;
  jwt: boolean;
  mtls: boolean;
  waf: boolean;
};

export type SecurityDashboard = {
  summary: {
    capabilities: number;
    oauth_clients: number;
    active_oauth_clients: number;
    api_keys: number;
    active_api_keys: number;
    certificates: number;
    active_certificates: number;
    secrets: number;
    rate_limit_policies: number;
    ip_filter_rules: number;
    waf_rules: number;
    active_waf_rules: number;
    audit_events: number;
    threat_block_rate_pct: number;
    oauth2_enabled: boolean;
    mtls_enabled: boolean;
    encryption_enabled: boolean;
  };
  profile: Record<string, unknown> | null;
  audit_by_outcome: Record<string, number>;
  audit_by_auth_method: Record<string, number>;
  recent_audit: Array<Record<string, unknown>>;
  active_rate_limits: Array<Record<string, unknown>>;
  active_ip_filters: Array<Record<string, unknown>>;
  active_waf_rules: Array<Record<string, unknown>>;
  credential_summary: Record<string, number>;
};



export const fetchSecurityCatalog = (s: ApiSession) =>
  apiGet<SecurityCatalog>("/api/v1/enterprise-integration-security/catalog", s);
export const fetchSecurityDashboard = (s: ApiSession) =>
  apiGet<SecurityDashboard>("/api/v1/enterprise-integration-security/dashboard", s);
export const fetchOAuthClients = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/oauth-clients", s);
export const fetchApiKeys = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/api-keys", s);
export const fetchCertificates = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/certificates", s);
export const fetchSecrets = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/secrets", s);
export const fetchRateLimits = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/rate-limits", s);
export const fetchIpFilters = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/ip-filters", s);
export const fetchWafRules = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/waf-rules", s);
export const fetchSecurityAudit = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-integration-security/audit", s);
export const seedSecurity = (s: ApiSession) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-integration-security/seed", s);
export const issueApiKey = (s: ApiSession, name: string) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-integration-security/api-keys", s, { name, scopes: ["read", "write"] });
export const validateSecurityRequest = (
  s: ApiSession,
  authMethod: string,
  clientIp: string,
  resource: string,
  payload = "",
  opts: { has_jwt?: boolean; has_api_key?: boolean; has_mtls?: boolean } = {},
) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-integration-security/validate", s, {
    auth_method: authMethod,
    client_ip: clientIp,
    resource,
    payload,
    has_jwt: opts.has_jwt ?? false,
    has_api_key: opts.has_api_key ?? false,
    has_mtls: opts.has_mtls ?? false,
  });
