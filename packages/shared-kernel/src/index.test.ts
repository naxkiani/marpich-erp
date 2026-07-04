import { describe, it, expect } from "vitest";
import { TenantId, Result, Guard } from "./index";

describe("TenantId", () => {
  it("creates valid tenant IDs", () => {
    const id = TenantId.create("acme-hospital");
    expect(id.toString()).toBe("acme-hospital");
  });

  it("rejects invalid format", () => {
    expect(() => TenantId.create("ab")).toThrow();
    expect(() => TenantId.create("a")).toThrow();
    expect(() => TenantId.create("_invalid")).toThrow();
  });
});

describe("Result", () => {
  it("returns value on success", () => {
    const result = Result.ok(42);
    expect(result.succeeded).toBe(true);
    expect(result.getValue()).toBe(42);
  });

  it("returns error on failure", () => {
    const result = Result.fail<number>("error");
    expect(result.succeeded).toBe(false);
    expect(() => result.getValue()).toThrow();
  });
});

describe("Guard", () => {
  it("validates empty strings", () => {
    expect(Guard.againstEmptyString("", "field").succeeded).toBe(false);
    expect(Guard.againstEmptyString("value", "field").succeeded).toBe(true);
  });
});
