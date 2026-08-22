/** Marpich Plugin SDK — types and manifest validator (plain ESM, no tsc required). */

const PLUGIN_ID_RE = /^[a-z][a-z0-9.-]*\.[a-z][a-z0-9.-]*\.[a-z][a-z0-9.-]*$/;
const SEMVER_RE = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$/;

const PLUGIN_TYPES = new Set([
  "module",
  "widget",
  "report",
  "dashboard",
  "theme",
  "ai_skill",
  "integration",
  "workflow_extension",
]);

export const EXTENSION_POINTS = {
  module: "platform.module.register",
  widget: "ui.dashboard.widget",
  report: "analytics.report.template",
  dashboard: "analytics.dashboard.layout",
  theme: "ui.theme.override",
  ai_skill: "ai.skill.register",
  integration: "integration.connector.register",
  workflow_extension: "workflow.hook.register",
};

export const SANDBOX_PROFILES = {
  widget: "strict",
  theme: "strict",
  report: "standard",
  dashboard: "standard",
  ai_skill: "standard",
  workflow_extension: "standard",
  integration: "integration",
  module: "module",
};

/** Types with seed evidence in Plugin Platform. Others exist as catalog types only. */
export const SCAFFOLDABLE_TYPES = new Set(["widget", "report"]);

export function validateManifest(manifest) {
  const errors = [];
  if (!manifest || typeof manifest !== "object") {
    return ["manifest must be an object"];
  }
  if (!manifest.pluginId || !PLUGIN_ID_RE.test(manifest.pluginId)) {
    errors.push("pluginId must be reverse-DNS (com.publisher.name)");
  }
  if (!manifest.pluginVersion || !SEMVER_RE.test(manifest.pluginVersion)) {
    errors.push("pluginVersion must be semver");
  }
  if (!manifest.pluginType || !PLUGIN_TYPES.has(manifest.pluginType)) {
    errors.push("pluginType must be a catalog type");
  }
  if (!manifest.displayName || !String(manifest.displayName).trim()) {
    errors.push("displayName is required");
  }
  if (!manifest.publisher?.id || !manifest.publisher?.name) {
    errors.push("publisher.id and publisher.name are required");
  }
  if (!Array.isArray(manifest.extensionPoints) || manifest.extensionPoints.length === 0) {
    errors.push("extensionPoints must not be empty");
  } else if (manifest.pluginType && PLUGIN_TYPES.has(manifest.pluginType)) {
    const expected = EXTENSION_POINTS[manifest.pluginType];
    if (!manifest.extensionPoints.includes(expected)) {
      errors.push(`extensionPoints must include canonical point ${expected}`);
    }
  }
  if (!Array.isArray(manifest.permissions)) {
    errors.push("permissions must be an array");
  } else {
    for (const perm of manifest.permissions) {
      if (typeof perm !== "string" || !perm.includes(".")) {
        errors.push(`permission must be dotted (module.resource.action): ${String(perm)}`);
      }
    }
  }
  if (!manifest.sandbox) {
    errors.push("sandbox is required");
  } else {
    if (manifest.sandbox.network !== "deny" && manifest.sandbox.network !== "allowlist") {
      errors.push("sandbox.network must be deny or allowlist");
    }
    if (manifest.sandbox.filesystem !== "read_only" && manifest.sandbox.filesystem !== "read_write_temp") {
      errors.push("sandbox.filesystem must be read_only or read_write_temp");
    }
    const mem = manifest.sandbox.maxMemoryMb;
    if (typeof mem !== "number" || mem < 16 || mem > 2048) {
      errors.push("sandbox.maxMemoryMb must be between 16 and 2048");
    }
  }
  if (!manifest.signature) {
    errors.push("signature is required");
  } else {
    if (manifest.signature.algorithm !== "ed25519" && manifest.signature.algorithm !== "rsa-pss-sha256") {
      errors.push("signature.algorithm must be ed25519 or rsa-pss-sha256");
    }
    if (!manifest.signature.packageChecksum?.startsWith("sha256:")) {
      errors.push("signature.packageChecksum must start with sha256:");
    }
    if (!manifest.signature.publicKeyFingerprint) {
      errors.push("signature.publicKeyFingerprint is required");
    }
  }
  return errors;
}

export function buildScaffoldManifest(pluginId, pluginType) {
  const point = EXTENSION_POINTS[pluginType];
  const strict = pluginType === "widget" || pluginType === "theme";
  return {
    pluginId,
    pluginVersion: "0.1.0",
    pluginType,
    displayName: pluginId,
    description: "MEOS extension scaffold — DEMO, not CERTIFIED",
    publisher: { id: "com.marpich", name: "Marpich Labs" },
    permissions: pluginType === "report" ? ["finance.reports.read"] : ["analytics.read"],
    extensionPoints: [point],
    sandbox: {
      network: "deny",
      filesystem: "read_only",
      maxMemoryMb: strict ? 64 : 256,
    },
    signature: {
      algorithm: "ed25519",
      publicKeyFingerprint: "sha256:demo-publisher-key-unverified",
      packageChecksum: "sha256:demo-scaffold-checksum-unverified",
    },
  };
}
