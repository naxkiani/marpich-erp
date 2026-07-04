/** Marpich Plugin SDK — types and manifest validator */

export type PluginType =
  | "module"
  | "widget"
  | "report"
  | "dashboard"
  | "theme"
  | "ai_skill"
  | "integration"
  | "workflow_extension";

export type TrustLevel = "community" | "verified" | "enterprise";

export type SandboxNetwork = "deny" | "allowlist";
export type SandboxFilesystem = "read_only" | "read_write_temp";

export interface PluginPublisher {
  id: string;
  name: string;
  website?: string;
}

export interface PluginSandbox {
  network: SandboxNetwork;
  allowedHosts?: string[];
  filesystem: SandboxFilesystem;
  maxMemoryMb: number;
}

export interface PluginSignature {
  algorithm: "ed25519" | "rsa-pss-sha256";
  publicKeyFingerprint: string;
  packageChecksum: string;
  signedAt?: string;
}

export interface PluginManifest {
  pluginId: string;
  pluginVersion: string;
  pluginType: PluginType;
  displayName: string;
  description?: string;
  publisher: PluginPublisher;
  permissions: string[];
  extensionPoints: string[];
  industryPacks?: string[];
  dependencies?: string[];
  sandbox: PluginSandbox;
  signature: PluginSignature;
  configSchema?: Record<string, unknown>;
  entrypoint?: string;
}

const PLUGIN_ID_RE = /^[a-z][a-z0-9.-]*\.[a-z][a-z0-9.-]*\.[a-z][a-z0-9.-]*$/;
const SEMVER_RE = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$/;

export function validateManifest(manifest: PluginManifest): string[] {
  const errors: string[] = [];
  if (!PLUGIN_ID_RE.test(manifest.pluginId)) {
    errors.push("pluginId must be reverse-DNS (com.publisher.name)");
  }
  if (!SEMVER_RE.test(manifest.pluginVersion)) {
    errors.push("pluginVersion must be semver");
  }
  if (!manifest.extensionPoints.length) {
    errors.push("extensionPoints must not be empty");
  }
  if (!manifest.signature.packageChecksum.startsWith("sha256:")) {
    errors.push("signature.packageChecksum must start with sha256:");
  }
  if (!manifest.signature.publicKeyFingerprint) {
    errors.push("signature.publicKeyFingerprint is required");
  }
  if (manifest.sandbox.maxMemoryMb < 16 || manifest.sandbox.maxMemoryMb > 2048) {
    errors.push("sandbox.maxMemoryMb must be between 16 and 2048");
  }
  return errors;
}

export const EXTENSION_POINTS: Record<PluginType, string> = {
  module: "platform.module.register",
  widget: "ui.dashboard.widget",
  report: "analytics.report.template",
  dashboard: "analytics.dashboard.layout",
  theme: "ui.theme.override",
  ai_skill: "ai.skill.register",
  integration: "integration.connector.register",
  workflow_extension: "workflow.hook.register",
};

export const SANDBOX_PROFILES: Record<PluginType, string> = {
  widget: "strict",
  theme: "strict",
  report: "standard",
  dashboard: "standard",
  ai_skill: "standard",
  workflow_extension: "standard",
  integration: "integration",
  module: "module",
};
