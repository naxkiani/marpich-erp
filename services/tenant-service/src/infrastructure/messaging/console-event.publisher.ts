import { Injectable } from "@nestjs/common";
import { DomainEvent } from "@marpich/shared-kernel";
import { IEventPublisher } from "../../application/ports/event-publisher.port";

/**
 * Kafka-backed publisher in production. Logs events during bootstrap.
 */
@Injectable()
export class ConsoleEventPublisher implements IEventPublisher {
  async publish(event: DomainEvent): Promise<void> {
    const payload = event.toPayload();
    console.log(
      JSON.stringify({
        type: "domain_event",
        service: "tenant-service",
        ...payload,
      }),
    );
  }
}
