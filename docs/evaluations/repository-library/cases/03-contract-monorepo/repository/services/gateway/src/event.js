export function serializeEvent(input) {
  return { id: input.id, occurred_at: input.occurred_at, source: input.source ?? "gateway" };
}
