import { Query } from "./query";
import { Result } from "../domain/result";

export interface QueryHandler<TQuery extends Query<TResult>, TResult> {
  readonly queryName: string;
  execute(query: TQuery): Promise<Result<TResult>>;
}
