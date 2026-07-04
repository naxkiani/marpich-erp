import { Injectable } from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import { createHash, randomUUID } from "node:crypto";
import type { ITokenService, TokenPayload } from "../../domain/ports/identity.ports";

@Injectable()
export class JwtTokenService implements ITokenService {
  constructor(private readonly jwt: JwtService) {}

  signAccess(payload: TokenPayload): string {
    return this.jwt.sign(payload, {
      expiresIn: Number(process.env.JWT_ACCESS_TTL ?? 900),
    });
  }

  signRefresh(payload: TokenPayload): string {
    return this.jwt.sign(
      { ...payload, type: "refresh", jti: randomUUID() },
      {
        expiresIn: Number(process.env.JWT_REFRESH_TTL ?? 604800),
      },
    );
  }

  verifyAccess(token: string): TokenPayload {
    const decoded = this.jwt.verify<TokenPayload & { type?: string }>(token);
    if (decoded.type === "refresh") throw new Error("Invalid token type");
    return decoded;
  }

  verifyRefresh(token: string): TokenPayload {
    const decoded = this.jwt.verify<TokenPayload & { type?: string }>(token);
    if (decoded.type !== "refresh") throw new Error("Invalid token type");
    return decoded;
  }

  hashRefreshToken(token: string): string {
    return createHash("sha256").update(token).digest("hex");
  }
}
