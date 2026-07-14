# Cross-Skill and Repository Audit

## Ownership contract

| Request shape | Owner |
| --- | --- |
| Ephemeral workers inside one current task | Built-in collaboration |
| Durable cross-session or cross-project mail | `agent-mail` |
| Human-facing gateway paired with a separate main session | `front-agent-orchestration` |
| Explicit persistent goal or repeated quality loop | `execute-goal-loop` |
| Fixed supplied resources reconciled across providers | `brief-linked-evidence` |
| Open-ended ecosystem discovery and canonicalization | `map-technical-landscapes` |
| Historical execution lineage or root-intent recurrence | `mine-history-tool-landscapes` |
| Skill structure, metadata, and mechanics | `skill-creator` |

## Repository findings and fixes

- P1: bundled commands assumed the user's current working directory. Skill docs now require resolving the installed skill directory before invoking resources.
- P1: generic validation included a production-mutating public smoke. It is now guarded and documented separately.
- P2: the installer linked skills before proving Front Agent could build. It now requires Go and builds before changing either HOME skill directory.
- P2: root docs listed only three of the six planned skills. Root inventory now reflects all seven currently discoverable skills; deterministic audit commands cover the six in scope, while the user-excluded `align-work` command remains documented for repository users only.
- P2: Front Agent's UI prompt duplicated implementation policy. It was reduced to protocol ownership.
- P2: trigger precedence was ambiguous. Frontmatter now carries the material exclusions and handoffs.
- P2: bundled references were undiscoverable. Canonical skills now link required references with read conditions.
- P2: Python bytecode could be staged with untracked skills. `.gitignore` now excludes caches and generated caches were removed.

## Verification

The planning inventory contains six audited skills. End discovery contains those six plus late-discovered `align-work`, which the user explicitly excluded from audit. Canonical package validation passes for the six audited skills only. The isolated installer produces seven links in each destination with Go and fails before touching HOME without Go.

The trigger matrix in `trigger-matrix.tsv` records one positive, negative, ambiguous-overlap, and misuse prompt for each audited skill, with expected routing, static observation, result, and false-positive/false-negative risk. All 24 cases reconcile with the final frontmatter and ownership table. This is a deterministic contract review, not a fresh-agent behavioral claim.
