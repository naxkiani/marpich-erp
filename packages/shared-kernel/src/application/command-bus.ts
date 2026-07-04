import { Command } from "./command";
import { Result } from "../domain/result";

export interface ICommandBus {
  dispatch<T extends Command, R = void>(command: T): Promise<Result<R>>;
  register<T extends Command, R = void>(
    commandName: string,
    handler: { execute(command: T): Promise<Result<R>> },
  ): void;
}
