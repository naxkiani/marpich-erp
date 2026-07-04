import { v4 as uuidv4, validate as uuidValidate } from "uuid";
import { ValueObject } from "./value-object";

interface UniqueEntityIdProps {
  value: string;
}

export class UniqueEntityId extends ValueObject<UniqueEntityIdProps> {
  private constructor(props: UniqueEntityIdProps) {
    super(props);
  }

  static create(id?: string): UniqueEntityId {
    const value = id ?? uuidv4();
    if (!uuidValidate(value)) {
      throw new Error(`Invalid UUID: ${value}`);
    }
    return new UniqueEntityId({ value });
  }

  override toString(): string {
    return this.props.value;
  }
}
