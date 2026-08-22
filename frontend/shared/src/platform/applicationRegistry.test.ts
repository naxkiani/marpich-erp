import assert from "node:assert/strict";
import test from "node:test";
import {
  APPLICATION_NAV,
  NAV_GROUP_ORDER,
  activatableModulesForPack,
  filterApplicationNav,
  isModuleEnabledForApp,
  isPackComingSoon,
  launchHrefForModule,
  launchHrefForPack,
  registryApplicationId,
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

test("shell nav ids are unique and alias to registry applications", () => {
  const ids = APPLICATION_NAV.map((item) => item.id);
  assert.equal(new Set(ids).size, ids.length);
  assert.equal(registryApplicationId(APPLICATION_NAV.find((a) => a.id === "dashboard")!), "core_platform");
  assert.equal(registryApplicationId(APPLICATION_NAV.find((a) => a.id === "modules")!), "core_platform");
  assert.equal(registryApplicationId(APPLICATION_NAV.find((a) => a.id === "federation")!), "identity_federation");
  assert.equal(registryApplicationId(APPLICATION_NAV.find((a) => a.id === "security")!), "identity");
  assert.equal(registryApplicationId(APPLICATION_NAV.find((a) => a.id === "policy")!), "policy");
  for (const item of APPLICATION_NAV) {
    assert.ok(NAV_GROUP_ORDER.includes(item.group));
  }
});

test("activatable modules exclude already enabled", () => {
  const next = activatableModulesForPack(
    { required_modules: ["platform.core"], optional_modules: ["platform.crm", "healthcare.pharmacy"] },
    ["platform.core", "platform.crm"],
  );
  assert.deepEqual(next, ["healthcare.pharmacy"]);
});
