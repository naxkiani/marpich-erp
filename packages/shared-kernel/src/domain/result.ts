export class Result<T> {
  readonly succeeded: boolean;
  readonly value?: T | undefined;
  readonly error?: string | undefined;

  private constructor(succeeded: boolean, value?: T, error?: string) {
    this.succeeded = succeeded;
    this.value = value;
    this.error = error;
  }

  static ok<U>(value: U): Result<U> {
    return new Result<U>(true, value);
  }

  static fail<U>(error: string): Result<U> {
    return new Result<U>(false, undefined, error);
  }

  getValue(): T {
    if (!this.succeeded || this.value === undefined) {
      throw new Error(this.error ?? "Result has no value");
    }
    return this.value;
  }
}
