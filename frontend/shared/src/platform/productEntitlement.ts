/** Product entitlement client. Server-side POST /api/v1/feature-flags/entitlements/evaluate is authoritative. */
export const PRODUCT_ENTITLEMENT_PATH = "/api/v1/feature-flags/entitlements/evaluate";

export type EntitlementStatus =
  | "ENABLED"
  | "DISABLED"
  | "TRIAL"
  | "EXPIRED"
  | "SUSPENDED"
  | "NOT_ENTITLED"
  | "BLOCKED";

export function clientEntitlementIsNotAuthoritative(): true {
  return true;
}
