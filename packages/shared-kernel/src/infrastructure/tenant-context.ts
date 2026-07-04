import { TenantId } from "../domain/tenant-id";

export interface TenantContextData {
  tenantId: TenantId;
  tenantName: string;
  schemaName: string;
  isolationStrategy: "schema" | "row";
  enabledModules: string[];
  locale: string;
  timezone: string;
  industryPack: string;
}

export interface ITenantContext {
  get(): TenantContextData;
  set(context: TenantContextData): void;
  clear(): void;
  require(): TenantContextData;
}
