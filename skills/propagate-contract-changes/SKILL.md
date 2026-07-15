---
name: propagate-contract-changes
description: Analyze, plan, or execute a requested structured API, schema, protocol, configuration, event, tool, serialization, or generated-artifact contract change through its canonical source, producers, boundaries, consumers, documentation, and tests. Use when the requested task is to change a contract across two or more surfaces or to repair confirmed drift between them. This skill owns propagation mechanics only. align-work owns unresolved compatibility or approval decisions, audit-technical-work owns read-only drift assessment, and mutation still requires existing authorization. Do not use for internal-only refactors without contract drift, documentation-only rewrites, generic multi-file features, or open-ended architecture review.
---

# Propagate Contract Changes

Treat one structured contract as a graph of producers and consumers. Preserve one canonical definition and verify every affected boundary instead of patching the first visible failure.

## Define the contract change

1. Identify the canonical owner from repository authority, generation, and consumption paths rather than assuming that a schema or generated type is authoritative. Write the exact old and requested new contract.
2. Decide compatibility, versioning, defaulting, absence, migration, and rollback behavior before mutation. Return unresolved material choices to the outer alignment workflow.
3. Inventory the propagation graph:
   - models and producers;
   - validation and serialization;
   - transport, persistence, and generated artifacts;
   - loaders, APIs, tools, events, and consumers;
   - identity, hash, cache, deduplication, and replay implications;
   - normative documentation, examples, fixtures, and tests.
4. Mark each surface as authoritative, generated, derived, consuming, test-only, or unaffected with a reason.

## Propagate from the owner

Proceed only with existing mutation authority.

1. Change the canonical source first within one coherent migration. If that ordering makes intermediate state invalid, use an atomic change set or an explicitly approved compatibility window; do not land a knowingly broken intermediate contract.
2. Regenerate derived artifacts through canonical tooling. Never leave a hand-edited generated artifact as the solution.
3. Update producers before consumers when the migration requires the new value to exist; otherwise use the explicitly approved compatibility order.
4. Preserve the contract through serialization, persistence, transport, and identity boundaries without silent dropping or reinterpretation.
5. Remove stale duplicate definitions and update documentation or examples to point to the owner.

## Verify every boundary

Test applicable cases through real boundaries:

- valid new value;
- invalid value and error behavior;
- absent, defaulted, nullable, or optional value;
- old-version and new-version compatibility;
- serialization and persistence round trip;
- generated artifact regeneration and clean diff;
- identity, cache, hash, replay, or deduplication behavior;
- representative producer-to-consumer integration.

Return the canonical contract, compatibility decision, propagation inventory, changed surfaces, regeneration command, gate receipts, and any surface that remains unknown or unverified. Do not claim completion while a required producer, boundary, consumer, or proof surface is unaccounted for.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "propagate-contract-changes"
- `routing_role`: "mechanics"
- `portfolio_position`: "Domain mechanics for structured multi-surface contract migration."
- `positive_request_classes`: ["structured API, schema, protocol, configuration, event, tool, serialization, or generated-artifact change across two or more surfaces","repair confirmed contract drift"]
- `triggers`: ["A structured contract must propagate through at least two surfaces.","Confirmed drift exists between a canonical contract and consumers."]
- `exclusions`: ["one-surface ordinary edit","internal-only refactor without contract drift","documentation-only rewrite","generic multi-file feature"]
- `state_owner`: "Owns canonical-source and propagation-graph mechanics, not approval or user authority."
- `precedence`: ["Compatibility and approval decisions stay with Align or the user.","Compose Refactor only for a separately named invariant slice."]
- `legal_compositions`: [{"route":"refactor-by-invariant","relation":"mechanics"}]
- `fallbacks`: [{"condition":"The work is a one-surface ordinary edit.","route":"native-codex","result":"Use bounded native implementation."},{"condition":"The primary objective is ownership simplification.","route":"refactor-by-invariant","result":"Use refactor mechanics unless a distinct contract slice is named."}]
- `forbidden_actions`: ["decide compatibility policy without authority","become outer authority","opportunistically refactor unrelated structure"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
