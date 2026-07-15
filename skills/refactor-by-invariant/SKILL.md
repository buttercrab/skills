---
name: refactor-by-invariant
description: Analyze, plan, or execute structural refactors by identifying the invariant, canonical owner, duplicated responsibility, and dependency direction, then proving behavior preservation and actual ownership simplification. Use for explicit modularization, deduplication, architecture cleanup, source-of-truth consolidation, or technical review of whether a refactor is substantive. This skill owns refactor mechanics only. align-work owns unresolved decisions and approval, audit-technical-work owns a requested read-only audit envelope, and mutation still requires existing authorization. Do not use for mechanical renames or file moves, ordinary feature work, formatting cleanup, performance-only optimization, or contract propagation whose primary objective is cross-surface consistency.
---

# Refactor by Invariant

Change structural ownership rather than merely moving code. Keep alignment, approval, and iteration with their outer workflows; this skill owns the refactor mechanics.

## Establish the baseline

1. State the behavior that must remain observable and the checks that prove it.
2. Name the invariant, the current sources that represent it, and the layer that should canonically own it.
3. Map callers, state transitions, dependency direction, duplicate representations, and compatibility constraints.
4. Distinguish the structural defect from symptoms such as long files, repeated branches, forwarding wrappers, or awkward names.
5. Separate duplicated production decisions from independent test oracles. Fixed vectors and independently derived expected results may remain when they detect a broken canonical owner; test helpers must not reimplement the production acceptance decision.

## Design the ownership change

1. Select one canonical owner and define what every neighboring layer may know or do.
2. Identify obsolete paths, duplicated decisions, reverse dependencies, switchboards, and adapters that must disappear.
3. Compare the proposed structure with a cosmetic alternative. Reject file motion, renaming, indirection, or abstraction growth that leaves authority duplicated.
4. Define the smallest honest proving slice, its allowed surfaces, its migration order, and rollback behavior.
5. Make any compatibility-versus-breaking decision explicit. Never preserve compatibility scaffolding by default when the approved objective allows removal.

## Implement and prove

Proceed only with existing mutation authority.

1. Capture the relevant behavior baseline before changing structure.
2. Move decision-making to the canonical owner before deleting old paths.
3. Update dependencies toward the owner; do not leave new forwarding switchboards behind.
4. Remove obsolete representations, adapters, branches, and tests that assert the discarded structure. Preserve or replace their behavioral coverage; deleting a structural assertion must not erase a regression oracle.
5. Run behavior-preservation gates and structural checks proving one owner, intended dependency direction, no hidden duplicate path, and no unrelated change.

Report the invariant, old and new ownership maps, removed paths, behavior receipts, structural receipts, and any remaining compatibility debt. If ownership did not materially simplify, report that the refactor is cosmetic rather than claiming success.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "refactor-by-invariant"
- `routing_role`: "mechanics"
- `portfolio_position`: "Domain mechanics for structural ownership simplification."
- `positive_request_classes`: ["explicit modularization","deduplication","source-of-truth consolidation","dependency-direction cleanup","substantive refactor review"]
- `triggers`: ["The primary objective is to simplify structural ownership around an invariant."]
- `exclusions`: ["mechanical rename or move","ordinary feature work","formatting cleanup","performance-only optimization","contract propagation without ownership change"]
- `state_owner`: "Owns invariant, canonical-owner, dependency-direction, and behavior-preservation proof; not user authority."
- `precedence`: ["Compose Propagate only where a distinct contract crosses surfaces."]
- `legal_compositions`: [{"route":"propagate-contract-changes","relation":"mechanics"}]
- `fallbacks`: [{"condition":"The primary objective is structured cross-surface consistency.","route":"propagate-contract-changes","result":"Use contract propagation mechanics."},{"condition":"The change is cosmetic or mechanical.","route":"native-codex","result":"Use bounded native implementation."}]
- `forbidden_actions`: ["change behavior silently","claim success without ownership reduction","decide approval policy"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
