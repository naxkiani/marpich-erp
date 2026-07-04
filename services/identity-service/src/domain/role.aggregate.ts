import { AggregateRoot, Guard, UniqueEntityId } from "@marpich/shared-kernel";

export interface RoleProps {
  tenantId: string;
  code: string;
  name: string;
  description?: string | undefined;
  isSystem: boolean;
  permissionIds: string[];
  createdAt: Date;
  updatedAt: Date;
}

export class Role extends AggregateRoot<RoleProps> {
  private constructor(props: RoleProps, id?: UniqueEntityId) {
    super(props, id);
  }

  static create(params: {
    tenantId: string;
    code: string;
    name: string;
    description?: string | undefined;
    permissionIds?: string[] | undefined;
    isSystem?: boolean | undefined;
  }): Role {
    const codeGuard = Guard.againstEmptyString(params.code, "code");
    const nameGuard = Guard.againstEmptyString(params.name, "name");
    const combined = Guard.combine([codeGuard, nameGuard]);
    if (!combined.succeeded) throw new Error(combined.message);

    const now = new Date();
    return new Role({
      tenantId: params.tenantId,
      code: params.code.trim().toLowerCase(),
      name: params.name.trim(),
      description: params.description,
      isSystem: params.isSystem ?? false,
      permissionIds: params.permissionIds ?? [],
      createdAt: now,
      updatedAt: now,
    });
  }

  static reconstitute(props: RoleProps, id: UniqueEntityId): Role {
    return new Role(props, id);
  }

  get tenantId(): string {
    return this.props.tenantId;
  }

  get code(): string {
    return this.props.code;
  }

  get name(): string {
    return this.props.name;
  }

  get permissionIds(): ReadonlyArray<string> {
    return [...this.props.permissionIds];
  }

  grantPermission(permissionId: string): void {
    if (!this.props.permissionIds.includes(permissionId)) {
      this.props.permissionIds.push(permissionId);
      this.props.updatedAt = new Date();
    }
  }

  toSnapshot(): Record<string, unknown> {
    return {
      id: this.id.toString(),
      tenantId: this.props.tenantId,
      code: this.props.code,
      name: this.props.name,
      description: this.props.description,
      isSystem: this.props.isSystem,
      permissionIds: this.props.permissionIds,
      createdAt: this.props.createdAt.toISOString(),
      updatedAt: this.props.updatedAt.toISOString(),
    };
  }
}
