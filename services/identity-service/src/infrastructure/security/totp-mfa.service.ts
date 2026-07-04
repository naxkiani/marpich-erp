import { Injectable } from "@nestjs/common";
import { authenticator } from "otplib";
import { randomBytes } from "node:crypto";
import type { IMfaService } from "../../domain/ports/identity.ports";

@Injectable()
export class TotpMfaService implements IMfaService {
  generateSecret(): string {
    return authenticator.generateSecret();
  }

  generateUri(email: string, secret: string, issuer = "Marpich ERP"): string {
    return authenticator.keyuri(email, issuer, secret);
  }

  verifyToken(secret: string, token: string): boolean {
    return authenticator.verify({ token, secret });
  }

  generateBackupCodes(count = 8): string[] {
    return Array.from({ length: count }, () =>
      randomBytes(4).toString("hex").toUpperCase(),
    );
  }
}
