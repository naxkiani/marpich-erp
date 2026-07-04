#!/usr/bin/env node
/** Marpich Plugin CLI — pack, sign, validate, publish stubs */
import { readFileSync } from "node:fs";
import { validateManifest, type PluginManifest } from "./index.js";

const [,, command, ...args] = process.argv;

function loadManifest(): PluginManifest {
  const raw = readFileSync("marpich.plugin.json", "utf8");
  return JSON.parse(raw) as PluginManifest;
}

switch (command) {
  case "validate": {
    const manifest = loadManifest();
    const errors = validateManifest(manifest);
    if (errors.length) {
      console.error("Manifest validation failed:");
      errors.forEach((e) => console.error(`  - ${e}`));
      process.exit(1);
    }
    console.log(`✓ ${manifest.pluginId}@${manifest.pluginVersion} valid`);
    break;
  }
  case "pack":
    console.log("Packaging plugin → dist/plugin.marpich (stub)");
    break;
  case "sign":
    console.log(`Signing with key ${args[1] ?? "(default)"} (stub)`);
    break;
  case "publish":
    console.log(`Publishing to ${args[1] ?? "marketplace"} (stub)`);
    break;
  case "init":
    console.log(`Scaffold plugin ${args[0]} type=${args[1] ?? "widget"} (stub)`);
    break;
  default:
    console.log("marpich-plugin <validate|pack|sign|publish|init>");
}
