import { UniqueEntityId } from "./unique-entity-id";

export abstract class Entity<TProps> {
  protected readonly _id: UniqueEntityId;
  protected readonly props: TProps;

  constructor(props: TProps, id?: UniqueEntityId) {
    this._id = id ?? UniqueEntityId.create();
    this.props = props;
  }

  get id(): UniqueEntityId {
    return this._id;
  }

  equals(entity?: Entity<TProps>): boolean {
    if (!entity) return false;
    if (this === entity) return true;
    return this._id.equals(entity._id);
  }
}
