import { TenantId } from "../domain/tenant-id";

export abstract class Command {
  readonly correlationId: string;
  readonly tenantId: TenantId;
  readonly userId?: string | undefined;
  readonly issuedAt: Date;

  protected constructor(params: {
    correlationId: string;
    tenantId: TenantId;
    userId?: string | undefined;
    issuedAt?: Date;
  }) {
    this.correlationId = params.correlationId;
    this.tenantId = params.tenantId;
    this.userId = params.userId;
    this.issuedAt = params.issuedAt ?? new Date();
  }
}
