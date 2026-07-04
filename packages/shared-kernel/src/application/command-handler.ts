import { Command } from "./command";
import { Result } from "../domain/result";

export interface CommandHandler<TCommand extends Command, TResult = void> {
  readonly commandName: string;
  execute(command: TCommand): Promise<Result<TResult>>;
}
