import assert from "node:assert/strict";
import test from "node:test";
import {
  APPLICATION_NAV,
  activatableModulesForPack,
  filterApplicationNav,
  isModuleEnabledForApp,
  isPackComingSoon,
  launchHrefForModule,
  launchHrefForPack,
} from "./applicationRegistry";

test("pack launch map covers healthcare and marks scaffolds coming soon", () => {
  assert.equal(launchHrefForPack("hospital"), "/healthcare/hospital");
  assert.equal(launchHrefForPack("accounting_firm"), "/accounting");
  assert.equal(isPackComingSoon("warehouse"), true);
});

test("module launch map unlocks Wave 02 apps", () => {
  assert.equal(launchHrefForModule("platform.crm"), "/crm");
  assert.equal(launchHrefForModule("platform.hr"), "/hr");
  assert.equal(launchHrefForModule("finance.tax"), "/tax");
});

test("nav filter requires enabled module when gated", () => {
  const crm = APPLICATION_NAV.find((a) => a.id === "crm");
  assert.ok(crm);
  assert.equal(isModuleEnabledForApp(crm!, ["platform.crm"]), true);
  assert.equal(isModuleEnabledForApp(crm!, []), false);
  const visible = filterApplicationNav(() => true, APPLICATION_NAV, ["platform.crm"]);
  assert.ok(visible.some((a) => a.id === "crm"));
  assert.ok(visible.some((a) => a.id === "dashboard"));
  assert.ok(!visible.some((a) => a.id === "hospital"));
});

test("activatable modules exclude already enabled", () => {
  const next = activatableModulesForPack(
    { required_modules: ["platform.core"], optional_modules: ["platform.crm", "healthcare.pharmacy"] },
    ["platform.core", "platform.crm"],
  );
  assert.deepEqual(next, ["healthcare.pharmacy"]);
});
