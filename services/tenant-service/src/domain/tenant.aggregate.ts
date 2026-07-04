import { AggregateRoot } from "@marpich/shared-kernel";
import { UniqueEntityId } from "@marpich/shared-kernel";
import { TenantId } from "@marpich/shared-kernel";
import { Guard } from "@marpich/shared-kernel";
import { TenantProvisionedEvent } from "./events/tenant-provisioned.event";

export type TenantStatus =
  | "provisioning"
  | "active"
  | "suspended"
  | "archived";

export type TenantTier = "starter" | "professional" | "enterprise";

export type IsolationStrategy = "schema" | "row";

export interface TenantProps {
  name: string;
  slug: string;
  industryPack: string;
  tier: TenantTier;
  isolationStrategy: IsolationStrategy;
  status: TenantStatus;
  enabledModules: string[];
  locale: string;
  timezone: string;
  dataRegion: string;
  createdAt: Date;
  updatedAt: Date;
}

export class Tenant extends AggregateRoot<TenantProps> {
  private constructor(props: TenantProps, id?: UniqueEntityId) {
    super(props, id);
  }

  static create(params: {
    name: string;
    slug: string;
    industryPack: string;
    tier?: TenantTier;
    isolationStrategy?: IsolationStrategy;
    locale?: string;
    timezone?: string;
    dataRegion?: string;
    enabledModules: string[];
    correlationId: string;
    id?: UniqueEntityId;
  }): Tenant {
    const nameGuard = Guard.againstEmptyString(params.name, "name");
    const slugGuard = Guard.againstEmptyString(params.slug, "slug");
    const packGuard = Guard.againstEmptyString(
      params.industryPack,
      "industryPack",
    );
    const combined = Guard.combine([nameGuard, slugGuard, packGuard]);
    if (!combined.succeeded) {
      throw new Error(combined.message);
    }

    const now = new Date();
    const tenant = new Tenant(
      {
        name: params.name.trim(),
        slug: params.slug.trim().toLowerCase(),
        industryPack: params.industryPack,
        tier: params.tier ?? "professional",
        isolationStrategy: params.isolationStrategy ?? "row",
        status: "provisioning",
        enabledModules: [...params.enabledModules],
        locale: params.locale ?? "en-US",
        timezone: params.timezone ?? "UTC",
        dataRegion: params.dataRegion ?? "us-east",
        createdAt: now,
        updatedAt: now,
      },
      params.id,
    );

    tenant.addDomainEvent(
      new TenantProvisionedEvent(
        tenant.id,
        TenantId.create(tenant.props.slug),
        {
          correlationId: params.correlationId,
          tenantId: TenantId.create(tenant.props.slug),
          occurredAt: now,
        },
        {
          name: tenant.props.name,
          industryPack: tenant.props.industryPack,
          enabledModules: tenant.props.enabledModules,
        },
      ),
    );

    return tenant;
  }

  static reconstitute(props: TenantProps, id: UniqueEntityId): Tenant {
    return new Tenant(props, id);
  }

  get tenantId(): TenantId {
    return TenantId.create(this.props.slug);
  }

  get name(): string {
    return this.props.name;
  }

  get slug(): string {
    return this.props.slug;
  }

  get industryPack(): string {
    return this.props.industryPack;
  }

  get status(): TenantStatus {
    return this.props.status;
  }

  get enabledModules(): ReadonlyArray<string> {
    return [...this.props.enabledModules];
  }

  activate(): void {
    if (this.props.status === "archived") {
      throw new Error("Cannot activate archived tenant");
    }
    this.props.status = "active";
    this.props.updatedAt = new Date();
  }

  suspend(): void {
    this.props.status = "suspended";
    this.props.updatedAt = new Date();
  }

  enableModule(moduleId: string): void {
    if (!this.props.enabledModules.includes(moduleId)) {
      this.props.enabledModules.push(moduleId);
      this.props.updatedAt = new Date();
    }
  }

  toSnapshot(): Record<string, unknown> {
    return {
      id: this.id.toString(),
      name: this.props.name,
      slug: this.props.slug,
      industryPack: this.props.industryPack,
      tier: this.props.tier,
      isolationStrategy: this.props.isolationStrategy,
      status: this.props.status,
      enabledModules: this.props.enabledModules,
      locale: this.props.locale,
      timezone: this.props.timezone,
      dataRegion: this.props.dataRegion,
      createdAt: this.props.createdAt.toISOString(),
      updatedAt: this.props.updatedAt.toISOString(),
    };
  }
}
