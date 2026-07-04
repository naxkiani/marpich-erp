import { DomainEvent } from "@marpich/shared-kernel";

export interface IEventPublisher {
  publish(event: DomainEvent): Promise<void>;
}

export const EVENT_PUBLISHER = Symbol("EVENT_PUBLISHER");
