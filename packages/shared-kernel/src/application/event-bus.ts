import { DomainEvent } from "../domain/domain-event";

export interface IntegrationEvent {
  readonly eventId: string;
  readonly eventName: string;
  readonly eventVersion: number;
  readonly tenantId: string;
  readonly payload: Record<string, unknown>;
  readonly occurredAt: string;
}

export interface IEventBus {
  publish(event: DomainEvent): Promise<void>;
  publishIntegration(event: IntegrationEvent): Promise<void>;
  subscribe(
    eventName: string,
    handler: (event: IntegrationEvent) => Promise<void>,
  ): void;
}
