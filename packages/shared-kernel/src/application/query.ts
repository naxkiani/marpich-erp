import { TenantId } from "../domain/tenant-id";

export abstract class Query<TResult> {
  readonly correlationId: string;
  readonly tenantId: TenantId;
  readonly userId?: string | undefined;

  protected constructor(params: {
    correlationId: string;
    tenantId: TenantId;
    userId?: string | undefined;
  }) {
    this.correlationId = params.correlationId;
    this.tenantId = params.tenantId;
    this.userId = params.userId;
  }
}
