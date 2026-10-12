---
name: refactor-by-invariant
description: Plan, execute, or review structural refactors that simplify ownership and dependencies while preserving observable behavior. Use for deduplication, modularization, or source-of-truth consolidation rather than mechanical renames or ordinary feature changes.
---

# Refactor by Invariant

A substantive refactor changes who owns a responsibility. Moving files or introducing wrappers can be useful steps, but cannot by themselves demonstrate simpler ownership.

## Identify what must stay true

State the behavior to preserve, including relevant error semantics, ordering, side effects, persistence, and public compatibility. Use the user's scope and existing authorization; ask only when an unresolved behavior or compatibility choice changes the outcome.

Trace the current owners, callers, state representations, and dependencies. Identify the specific duplicated decision, split authority, or dependency problem. Choose the intended owner by what information and lifecycle it needs, rather than by a preference for a particular directory or abstraction.

Separate production duplication from independent verification. Fixed vectors, differential comparisons, and independently derived expected results can detect a broken canonical owner. Replacing all expected results with calls to the new owner can make the tests self-confirming.

## Change responsibility, then remove duplication

- Define what the chosen owner decides and what neighboring layers supply or consume.
- Find the smallest coherent migration that removes the actual duplication. Avoid opportunistic cleanup outside that slice.
- Capture useful behavioral evidence before changing structure. If a baseline already fails, record that failure so it is not attributed to the refactor or silently hidden.
- Move decisions and state authority to the owner; update callers and dependency direction. Remove obsolete paths once callers no longer need them.
- Keep an adapter when it serves a real boundary, lifecycle, or compatibility requirement. Remove forwarding layers that merely preserve competing ownership. Do not break required compatibility just to reduce code.
- Replace obsolete structural assertions with behavioral coverage where needed. Preserve unrelated dirty work.

For analysis or review requests, produce the ownership design or assessment without making product changes. For implementation requests, proceed under the existing authority.

## Prove both outcomes

Verify behavior through relevant existing tests, independent examples, or representative integration paths. Include negative cases when the moved responsibility rejects input or controls side effects. Use structural inspection to show where the decision now lives, how callers reach it, and which old paths disappeared; passing behavior tests alone does not prove ownership simplification.

Report the behavior preserved, responsibility moved, duplication removed, and checks performed. Identify retained compatibility layers and unverified paths. If the result only reorganizes files, describe it as organization rather than claiming a source-of-truth consolidation.
