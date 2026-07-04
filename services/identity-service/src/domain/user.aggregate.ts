import { AggregateRoot, Guard, UniqueEntityId } from "@marpich/shared-kernel";
import { UserCreatedEvent, UserLoggedInEvent, MfaEnabledEvent } from "./events/identity.events";
import { TenantId } from "@marpich/shared-kernel";

export type UserStatus = "active" | "inactive" | "locked" | "pending_mfa";

export interface UserProps {
  tenantId: string;
  email: string;
  passwordHash: string;
  displayName: string;
  status: UserStatus;
  locale: string;
  attributes: Record<string, unknown>;
  mfaEnabled: boolean;
  mfaSecret?: string | undefined;
  backupCodes: string[];
  roleIds: string[];
  failedLoginAttempts: number;
  lockedUntil?: Date | undefined;
  lastLoginAt?: Date | undefined;
  createdAt: Date;
  updatedAt: Date;
}

export class User extends AggregateRoot<UserProps> {
  private constructor(props: UserProps, id?: UniqueEntityId) {
    super(props, id);
  }

  static register(params: {
    tenantId: string;
    email: string;
    passwordHash: string;
    displayName: string;
    locale?: string | undefined;
    roleIds?: string[] | undefined;
    correlationId: string;
    actorId?: string | undefined;
  }): User {
    const emailGuard = Guard.againstEmptyString(params.email, "email");
    const nameGuard = Guard.againstEmptyString(params.displayName, "displayName");
    const combined = Guard.combine([emailGuard, nameGuard]);
    if (!combined.succeeded) throw new Error(combined.message);

    const now = new Date();
    const user = new User({
      tenantId: params.tenantId,
      email: params.email.trim().toLowerCase(),
      passwordHash: params.passwordHash,
      displayName: params.displayName.trim(),
      status: "active",
      locale: params.locale ?? "en-US",
      attributes: {},
      mfaEnabled: false,
      backupCodes: [],
      roleIds: params.roleIds ?? [],
      failedLoginAttempts: 0,
      createdAt: now,
      updatedAt: now,
    });

    user.addDomainEvent(
      new UserCreatedEvent(user.id, params.tenantId, {
        correlationId: params.correlationId,
        tenantId: TenantId.create(params.tenantId),
        occurredAt: now,
        ...(params.actorId !== undefined ? { userId: params.actorId } : {}),
      }, {
        email: user.props.email,
        displayName: user.props.displayName,
      }),
    );

    return user;
  }

  static reconstitute(props: UserProps, id: UniqueEntityId): User {
    return new User(props, id);
  }

  get tenantId(): string {
    return this.props.tenantId;
  }

  get email(): string {
    return this.props.email;
  }

  get displayName(): string {
    return this.props.displayName;
  }

  get status(): UserStatus {
    return this.props.status;
  }

  get mfaEnabled(): boolean {
    return this.props.mfaEnabled;
  }

  get roleIds(): ReadonlyArray<string> {
    return [...this.props.roleIds];
  }

  get passwordHash(): string {
    return this.props.passwordHash;
  }

  get mfaSecret(): string | undefined {
    return this.props.mfaSecret;
  }

  get backupCodes(): ReadonlyArray<string> {
    return [...this.props.backupCodes];
  }

  get failedLoginAttempts(): number {
    return this.props.failedLoginAttempts;
  }

  get lockedUntil(): Date | undefined {
    return this.props.lockedUntil;
  }

  get locale(): string {
    return this.props.locale;
  }

  get attributes(): Record<string, unknown> {
    return { ...this.props.attributes };
  }

  isLocked(): boolean {
    if (this.props.status === "locked" && this.props.lockedUntil) {
      return this.props.lockedUntil > new Date();
    }
    return this.props.status === "locked";
  }

  recordFailedLogin(): void {
    this.props.failedLoginAttempts += 1;
    if (this.props.failedLoginAttempts >= 5) {
      this.props.status = "locked";
      this.props.lockedUntil = new Date(Date.now() + 15 * 60 * 1000);
    }
    this.props.updatedAt = new Date();
  }

  recordSuccessfulLogin(correlationId: string, ipAddress?: string): void {
    this.props.failedLoginAttempts = 0;
    this.props.lockedUntil = undefined;
    this.props.status = this.props.mfaEnabled ? this.props.status : "active";
    this.props.lastLoginAt = new Date();
    this.props.updatedAt = new Date();

    this.addDomainEvent(
      new UserLoggedInEvent(this.id, this.props.tenantId, {
        correlationId,
        tenantId: TenantId.create(this.props.tenantId),
        occurredAt: new Date(),
        userId: this.id.toString(),
      }, { ipAddress }),
    );
  }

  enableMfa(secret: string, backupCodes: string[], correlationId: string): void {
    this.props.mfaSecret = secret;
    this.props.backupCodes = backupCodes;
    this.props.mfaEnabled = true;
    this.props.updatedAt = new Date();

    this.addDomainEvent(
      new MfaEnabledEvent(this.id, this.props.tenantId, {
        correlationId,
        tenantId: TenantId.create(this.props.tenantId),
        occurredAt: new Date(),
        userId: this.id.toString(),
      }),
    );
  }

  disableMfa(): void {
    this.props.mfaEnabled = false;
    this.props.mfaSecret = undefined;
    this.props.backupCodes = [];
    this.props.updatedAt = new Date();
  }

  assignRole(roleId: string): void {
    if (!this.props.roleIds.includes(roleId)) {
      this.props.roleIds.push(roleId);
      this.props.updatedAt = new Date();
    }
  }

  consumeBackupCode(code: string): boolean {
    const idx = this.props.backupCodes.indexOf(code);
    if (idx === -1) return false;
    this.props.backupCodes.splice(idx, 1);
    this.props.updatedAt = new Date();
    return true;
  }

  toSnapshot(): Record<string, unknown> {
    return {
      id: this.id.toString(),
      tenantId: this.props.tenantId,
      email: this.props.email,
      displayName: this.props.displayName,
      status: this.props.status,
      locale: this.props.locale,
      attributes: this.props.attributes,
      mfaEnabled: this.props.mfaEnabled,
      roleIds: this.props.roleIds,
      lastLoginAt: this.props.lastLoginAt?.toISOString(),
      createdAt: this.props.createdAt.toISOString(),
      updatedAt: this.props.updatedAt.toISOString(),
    };
  }
}
