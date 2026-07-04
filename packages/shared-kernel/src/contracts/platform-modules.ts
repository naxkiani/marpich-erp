import type { IModuleManifest } from "../infrastructure/module-manifest";

/**
 * Platform module registry — canonical list of all composable modules.
 * Industry packs activate subsets; modules share core platform services.
 */
export const PLATFORM_MODULE_IDS = {
  CORE: "platform.core",
  IDENTITY: "platform.identity",
  TENANT: "platform.tenant",
  FINANCE: "platform.finance",
  HR: "platform.hr",
  CRM: "platform.crm",
  INVENTORY: "platform.inventory",
  DOCUMENTS: "platform.documents",
  WORKFLOW: "platform.workflow",
  NOTIFICATIONS: "platform.notifications",
  REPORTING: "platform.reporting",
  AI_INSIGHTS: "ai.insights",
  AI_FRAUD: "ai.fraud-detection",
  AI_CLINICAL: "ai.clinical-assist",
} as const;

export type PlatformModuleId =
  (typeof PLATFORM_MODULE_IDS)[keyof typeof PLATFORM_MODULE_IDS];

export interface PlatformModuleDefinition {
  moduleId: string;
  layer: "platform" | "domain" | "ai";
  boundedContext: string;
  serviceName: string;
  databaseSchema?: string;
}

export const PLATFORM_MODULES: PlatformModuleDefinition[] = [
  {
    moduleId: PLATFORM_MODULE_IDS.CORE,
    layer: "platform",
    boundedContext: "Platform Core",
    serviceName: "platform-core",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.IDENTITY,
    layer: "platform",
    boundedContext: "Identity & Access",
    serviceName: "identity-service",
    databaseSchema: "identity",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.TENANT,
    layer: "platform",
    boundedContext: "Tenant Management",
    serviceName: "tenant-service",
    databaseSchema: "tenant",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.FINANCE,
    layer: "domain",
    boundedContext: "Finance",
    serviceName: "finance-service",
    databaseSchema: "finance",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.HR,
    layer: "domain",
    boundedContext: "Human Resources",
    serviceName: "hr-service",
    databaseSchema: "hr",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.CRM,
    layer: "domain",
    boundedContext: "Customer Relationship",
    serviceName: "crm-service",
    databaseSchema: "crm",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.INVENTORY,
    layer: "domain",
    boundedContext: "Inventory & Supply",
    serviceName: "inventory-service",
    databaseSchema: "inventory",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.DOCUMENTS,
    layer: "platform",
    boundedContext: "Document Management",
    serviceName: "document-service",
    databaseSchema: "documents",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.WORKFLOW,
    layer: "platform",
    boundedContext: "Workflow Engine",
    serviceName: "workflow-service",
    databaseSchema: "workflow",
  },
  {
    moduleId: PLATFORM_MODULE_IDS.AI_INSIGHTS,
    layer: "ai",
    boundedContext: "AI Insights",
    serviceName: "ai-service",
  },
];

export function findPlatformModule(
  moduleId: string,
): PlatformModuleDefinition | undefined {
  return PLATFORM_MODULES.find((m) => m.moduleId === moduleId);
}

export interface ModuleRegistryEntry {
  manifest: IModuleManifest;
  status: "registered" | "active" | "deprecated";
  registeredAt: string;
}
