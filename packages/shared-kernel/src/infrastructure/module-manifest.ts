/**
 * Module manifest contract — every industry capability registers through this.
 * Modules are composable; never duplicate domain logic across industries.
 */
export interface ModulePermission {
  code: string;
  description: string;
  resource: string;
  action: string;
}

export interface ModuleEntity {
  name: string;
  tableName: string;
  description: string;
}

export interface ModuleApiRoute {
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  path: string;
  handler: string;
  permissions: string[];
}

export interface IModuleManifest {
  readonly moduleId: string;
  readonly moduleVersion: string;
  readonly displayName: string;
  readonly description: string;
  readonly category: ModuleCategory;
  readonly industryPacks: string[];
  readonly dependencies: string[];
  readonly permissions: ModulePermission[];
  readonly entities: ModuleEntity[];
  readonly apiRoutes: ModuleApiRoute[];
  readonly eventSubscriptions: string[];
  readonly eventPublications: string[];
}

export type ModuleCategory =
  | "platform"
  | "finance"
  | "hr"
  | "crm"
  | "scm"
  | "manufacturing"
  | "healthcare"
  | "education"
  | "hospitality"
  | "real-estate"
  | "government"
  | "logistics"
  | "retail"
  | "ai"
  | "compliance";
