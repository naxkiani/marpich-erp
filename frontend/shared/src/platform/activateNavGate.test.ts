import assert from "node:assert/strict";
import test from "node:test";
import {
  APPLICATION_NAV,
  filterApplicationNav,
  isModuleEnabledForApp,
} from "./applicationRegistry";

/**
 * Activate → nav gate contract: after Modules desk sets enabled_modules,
 * ShellNav / command palette must show only intersection of AuthZ ∩ enabled.
 */
test("activate→nav: enabling platform.crm reveals CRM and hides hospital", () => {
  const can = () => true;
  const before = filterApplicationNav(can, APPLICATION_NAV, []);
  assert.ok(!before.some((a) => a.id === "crm"));

  const after = filterApplicationNav(can, APPLICATION_NAV, ["platform.crm"]);
  assert.ok(after.some((a) => a.id === "crm"));
  assert.ok(after.some((a) => a.id === "dashboard"));
  assert.ok(!after.some((a) => a.id === "hospital"));
});

test("activate→nav: AuthZ deny wins even when module enabled", () => {
  const denyAllCrm = () => false;
  const visible = filterApplicationNav(denyAllCrm, APPLICATION_NAV, ["platform.crm"]);
  assert.ok(!visible.some((a) => a.id === "crm"));
});

test("activate→nav: healthcare modules gate hospital desk", () => {
  const hospital = APPLICATION_NAV.find((a) => a.id === "hospital");
  assert.ok(hospital);
  // undefined enabledModules → Shell skips module filter via filterApplicationNav
  const untilLoaded = filterApplicationNav(() => true, APPLICATION_NAV, undefined);
  assert.ok(untilLoaded.some((a) => a.id === "hospital"));
  assert.equal(isModuleEnabledForApp(hospital, []), false);
  assert.equal(
    isModuleEnabledForApp(hospital, ["healthcare.patient-management"]),
    true,
  );
});
