#!/usr/bin/env node
/** Marpich Plugin CLI — validate and init are real; pack/sign/publish are NOT_IMPLEMENTED. */
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { buildScaffoldManifest, SCAFFOLDABLE_TYPES, validateManifest } from "./index.js";

const [, , command, ...args] = process.argv;

function loadManifest(path = "marpich.plugin.json") {
  const raw = readFileSync(path, "utf8");
  return JSON.parse(raw);
}

function notImplemented(name) {
  console.error(
    `NOT_IMPLEMENTED: marpich-plugin ${name} is a stub. It does not produce a signed, certified, or publishable artifact.`,
  );
  process.exit(2);
}

switch (command) {
  case "validate": {
    const path = args[0] ?? "marpich.plugin.json";
    const manifest = loadManifest(path);
    const errors = validateManifest(manifest);
    if (errors.length) {
      console.error("Manifest validation failed:");
      errors.forEach((e) => console.error(`  - ${e}`));
      process.exit(1);
    }
    console.log(`${manifest.pluginId}@${manifest.pluginVersion} valid (manifest only — not CERTIFIED)`);
    break;
  }
  case "init": {
    const pluginId = args[0];
    const pluginType = args[1] ?? "widget";
    if (!pluginId) {
      console.error("usage: marpich-plugin init <pluginId> [widget|report]");
      process.exit(1);
    }
    if (!SCAFFOLDABLE_TYPES.has(pluginType)) {
      console.error(
        `init supports widget|report (types with MEOS seed evidence). Catalog type ${pluginType} has no scaffold.`,
      );
      process.exit(1);
    }
    const out = "marpich.plugin.json";
    if (existsSync(out) && args[2] !== "--force") {
      console.error(`${out} exists; pass --force to overwrite`);
      process.exit(1);
    }
    const manifest = buildScaffoldManifest(pluginId, pluginType);
    const errors = validateManifest(manifest);
    if (errors.length) {
      console.error(errors.join("\n"));
      process.exit(1);
    }
    writeFileSync(out, `${JSON.stringify(manifest, null, 2)}\n`);
    console.log(`Wrote ${out} for ${pluginId} (${pluginType}). DEMO scaffold — not CERTIFIED.`);
    break;
  }
  case "pack":
  case "sign":
  case "publish":
  case "test":
  case "deploy":
    notImplemented(command);
    break;
  default:
    console.log("marpich-plugin <validate|init>");
    console.log("  validate [path]     Validate marpich.plugin.json (manifest only)");
    console.log("  init <id> [type]    Scaffold widget|report manifest");
    console.log("pack|sign|publish|test|deploy: NOT_IMPLEMENTED (fail closed)");
    process.exit(command ? 1 : 0);
}
