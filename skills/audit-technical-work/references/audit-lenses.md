# Audit Lenses

Read only the section needed for the declared audit. These lenses add technical criteria; `audit-technical-work` still owns read-only scope, evidence accounting, and reporting.

## Architecture and ownership

- Identify the invariant and its canonical owner.
- Trace public entry points, state transitions, dependency direction, and data authority.
- Look for duplicated decisions, parallel representations, reverse dependencies, switchboards, or wrappers that conceal rather than remove ownership problems.
- Distinguish structural correction from naming, file movement, or abstraction growth.
- Require behavior-preservation proof and evidence that obsolete paths are removed.

## Security and privacy

- Trace identities, authority, secrets, personal data, logs, storage, serialization, and external boundaries.
- Require both a concrete hostile trigger and an observable unsafe outcome before accepting an exploit claim.
- Treat unknown trust, provenance, or authorization state as unsafe when the contract is fail-closed.
- Check that metadata survives every relevant seam without silent trust restoration.
- Pair each supported finding with a mitigation and a negative or adversarial verification case.
- Do not expose secrets or reproduce sensitive payloads in the report.

## Specification and completion proof

- Inventory every normative requirement, error case, grammar rule, example, and conformance vector.
- Check determinism, implementability, negative cases, executable behavior, and resistance to vacuous success.
- Assign normative facts one owner and inspect downstream implementation, examples, generated artifacts, and status claims for parity.
- Map every current requirement to scope-matched evidence and reject stale, superseded, mock-only, or narrower receipts.
- Report `incomplete` when any required item lacks authoritative proof, even if all available tests pass.
