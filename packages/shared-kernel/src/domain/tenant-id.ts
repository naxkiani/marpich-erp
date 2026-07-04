import { ValueObject } from "./value-object";
import { Guard } from "./guard";

interface TenantIdProps {
  value: string;
}

/**
 * Tenant identifier — every aggregate and event is tenant-scoped.
 * Supports schema-per-tenant and row-level isolation strategies.
 */
export class TenantId extends ValueObject<TenantIdProps> {
  private constructor(props: TenantIdProps) {
    super(props);
  }

  static create(value: string): TenantId {
    const guard = Guard.againstNullOrUndefined(value, "tenantId");
    if (!guard.succeeded) {
      throw new Error(guard.message);
    }
    const normalized = value.trim().toLowerCase();
    if (!/^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$/.test(normalized)) {
      throw new Error(`Invalid tenant ID format: ${value}`);
    }
    return new TenantId({ value: normalized });
  }

  override toString(): string {
    return this.props.value;
  }
}
