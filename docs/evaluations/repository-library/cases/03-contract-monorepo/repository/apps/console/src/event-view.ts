type GatewayEvent = { id: string; occurred_at: string; source: string };
export const label = (event: GatewayEvent) => `${event.source.toUpperCase()}: ${event.id}`;
