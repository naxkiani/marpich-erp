import { Query } from "./query";
import { Result } from "../domain/result";

export interface IQueryBus {
  dispatch<TQuery extends Query<TResult>, TResult>(
    query: TQuery,
  ): Promise<Result<TResult>>;
  register<TQuery extends Query<TResult>, TResult>(
    queryName: string,
    handler: { execute(query: TQuery): Promise<Result<TResult>> },
  ): void;
}
