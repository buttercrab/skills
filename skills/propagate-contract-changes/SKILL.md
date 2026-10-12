---
name: propagate-contract-changes
description: Carry a requested API, schema, protocol, event, configuration, or serialization change through its authoritative definition, producers, boundaries, and consumers. Use for cross-surface contract changes or confirmed contract drift.
---

# Propagate Contract Changes

Treat the contract as a path through a system, not merely a type declaration. A value can compile correctly and still be dropped by a serializer, rejected by an older reader, or interpreted differently after storage.

## Locate authority and affected paths

Identify the exact old and requested new semantics and the authoritative definition. Determine authority from generation and consumption paths; a generated type or schema is not automatically the source of truth.

Trace actual producers to consumers through applicable validation, encoding, transport, persistence, loading, and generated code. Check normative documentation, fixtures, and examples for promised behavior. Include hashes, caches, replay, or deduplication only when the change affects their inputs or interpretation. Track affected surfaces in a form proportional to the change; a short list can suffice.

Search for alternate encodings, copied definitions, old names, and older consumers. A text search starts the inventory but does not prove it complete: inspect dynamic construction, generation commands, and deployed version relationships when relevant.

## Choose compatibility and order

Use existing user decisions and repository conventions. Clarify only an unresolved material choice, such as whether old persisted records must still load or a public field may disappear. Do not silently turn an internal edit into a breaking migration.

Distinguish an atomic local edit from a rollout across independently updated components. For a rolling change, readers may need to tolerate both forms before writers emit the new form; removal can follow after migration. For an atomic change, update all affected surfaces coherently. Document defaults, absence, invalid values, versioning, and rollback only as applicable.

A request to change code does not itself authorize deploying components or migrating production data. Provide required rollout steps when those operations are outside the authorized scope.

## Propagate and verify

Change the canonical source and regenerate derived artifacts with the repository's tooling. Do not fix drift solely by hand-editing generated output. Update callers, serializers, readers, examples, and fixtures that actually depend on the semantics; remove stale duplicate definitions without unrelated restructuring.

Select checks that exercise the changed boundaries:

- A representative producer-to-consumer path carrying the new value.
- Rejection and error behavior for invalid input.
- Missing, nullable, optional, or defaulted values when supported.
- Old data and mixed-version readers/writers when compatibility is required.
- Encoding or persistence round trips where the representation crosses those boundaries.
- Repeatable regeneration and relevant cache, identity, or replay behavior.

An updated mock or generated type is not evidence that a real reader accepts the value. Inspect raw boundary representations when a field can disappear or change meaning.

Report the canonical change, compatibility decision, affected paths, regeneration and verification performed, and any pending migration or unverified consumer. Distinguish locally complete code from a completed rollout.
