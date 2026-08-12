/** Node built-in test — AuthZ nav filter contract (no TS loader required). */
import assert from "node:assert/strict";
import { describe, it } from "node:test";

function matchesPermission(userPermissions, required) {
  if (userPermissions.includes("*")) return true;
  return userPermissions.includes(required);
}

function matchesAnyPermission(userPermissions, required) {
  if (!required) return true;
  const codes = typeof required === "string" ? [required] : required;
  if (codes.length === 0) return true;
  return codes.some((code) => matchesPermission(userPermissions, code));
}

const SAMPLE_NAV = [
  { id: "dashboard", permission: undefined },
  { id: "hospital", permission: "hospital.patients.read" },
  { id: "audit", permission: "audit.entries.read" },
  {
    id: "workflow",
    permission: ["workflow.instances.read", "workflow.definitions.read", "workflow.tasks.complete"],
  },
];

function filterNav(perms) {
  return SAMPLE_NAV.filter((item) => matchesAnyPermission(perms, item.permission));
}

describe("matchesPermission", () => {
  it("honors wildcard admin", () => {
    assert.equal(matchesPermission(["*"], "hospital.patients.read"), true);
  });
  it("requires exact code otherwise", () => {
    assert.equal(matchesPermission(["audit.entries.read"], "hospital.patients.read"), false);
    assert.equal(matchesPermission(["audit.entries.read"], "audit.entries.read"), true);
  });
});

describe("filterApplicationNav contract", () => {
  it("keeps home items without permission", () => {
    const visible = filterNav([]);
    assert.ok(visible.some((i) => i.id === "dashboard"));
    assert.ok(!visible.some((i) => i.id === "hospital"));
  });

  it("shows hospital when granted", () => {
    assert.ok(filterNav(["hospital.patients.read"]).some((i) => i.id === "hospital"));
  });

  it("workflow any-of", () => {
    assert.ok(filterNav(["workflow.tasks.complete"]).some((i) => i.id === "workflow"));
    assert.ok(!filterNav(["documents.read"]).some((i) => i.id === "workflow"));
  });
});
