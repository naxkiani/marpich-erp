import { describe, it, expect } from "vitest";
import { PermissionEvaluator } from "@marpich/platform-core";
import { User } from "../../src/domain/user.aggregate";
import { TotpMfaService } from "../../src/infrastructure/security/totp-mfa.service";

describe("PermissionEvaluator", () => {
  const evaluator = new PermissionEvaluator();

  it("grants wildcard admin permission", () => {
    expect(
      evaluator.hasPermission(
        { tenantId: "t1", userId: "u1", permissions: ["*"], roles: ["admin"], attributes: {} },
        "identity.users.write",
      ),
    ).toBe(true);
  });

  it("denies missing permission", () => {
    expect(
      evaluator.hasPermission(
        { tenantId: "t1", userId: "u1", permissions: ["identity.users.read"], roles: [], attributes: {} },
        "identity.users.write",
      ),
    ).toBe(false);
  });
});

describe("User aggregate", () => {
  it("locks account after failed attempts", () => {
    const user = User.register({
      tenantId: "acme",
      email: "a@b.com",
      passwordHash: "hash",
      displayName: "Test",
      correlationId: "c1",
    });

    for (let i = 0; i < 5; i++) user.recordFailedLogin();
    expect(user.isLocked()).toBe(true);
  });
});

describe("TotpMfaService", () => {
  it("generates and verifies TOTP", () => {
    const mfa = new TotpMfaService();
    const secret = mfa.generateSecret();
    const token = require("otplib").authenticator.generate(secret);
    expect(mfa.verifyToken(secret, token)).toBe(true);
  });
});
