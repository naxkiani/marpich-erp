import { Injectable } from "@nestjs/common";
import * as bcrypt from "bcrypt";
import type { IPasswordHasher } from "../../domain/ports/identity.ports";

@Injectable()
export class BcryptPasswordHasher implements IPasswordHasher {
  private readonly rounds = 12;

  async hash(plain: string): Promise<string> {
    return bcrypt.hash(plain, this.rounds);
  }

  async verify(plain: string, hash: string): Promise<boolean> {
    return bcrypt.compare(plain, hash);
  }
}
