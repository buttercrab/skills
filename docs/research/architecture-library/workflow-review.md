# Read-only architecture workflow integration review

Date: 2026-11-07. Reviewed the active `system-architecture/SKILL.md`, all five references, `library/FORMAT.md`, `library/VOCABULARY.md` and the relevant helper validation/search interface. No assessment fixtures, private evaluation notes, prior assessment conclusions, current product code or upstream source was inspected. No active package files were edited or examples executed. This is a consistency review, not behavioral or architectural validation.

## Result

No actionable material inconsistency found in the inspected workflow/interface. The guidance preserves a bounded architecture deliverable, resolves consequential human intent, exposes source/diagram/runtime evidence differences, and does not force a universal architecture or diagram suite.

## Checked relationships

| Surface / exact section | Supported integration observation |
| --- | --- |
| `SKILL.md` introduction; “Decide and verify at the requested scope” | A skill/library example remains subordinate to the parent deliverable; assessment/diagram scope does not silently become implementation or infrastructure work. Existing authorization is preserved rather than replaced with repeated approval prompts. |
| `SKILL.md` “Establish the decision…”; `context-and-tradeoffs.md` | Questions are tied to invariant/workload/operator/compatibility decisions. Technical facts should be discovered; full briefs, narrow tasks and delegation can proceed. Delayed answers retire dependent provisional choices; viewing a reference is not endorsement. The reference explicitly says its table is not a mandatory questionnaire. |
| `SKILL.md` “Compare mechanisms…”; `boundaries-and-failure.md` | Simpler/no-change and in-process alternatives remain available. Team/module/process/deployment/transaction/trust boundaries are distinguished. Distribution, event sourcing, cache or clean-layer choices need contextual justification; no vendor or microservice default is imposed. |
| `SKILL.md` “Draw the model…”; `diagram-contract.md` | Views answer distinct questions and do not require every C4/UML level. Important relation semantics, status, scope, evidence and unknowns must be explicit; a logical container is not a Docker container. Source/deployment/current/proposed states are separated. |
| `diagram-contract.md` original examples | Text review shows consistent illustrative/proposed labeling. The asynchronous sequence separates durable local acceptance from external effect and leaves provider retry policy unresolved. The state view keeps unknown outcome distinct from confirmed failure/success. The deployment view does not invent instance counts, zones or database location. These examples were **not parsed or rendered by this review**, and no runtime invariant is proven. |
| `verification-and-evolution.md` evidence table and decision lifecycle | Parsing, rendering, semantic/source correspondence, workload measurements and deployed observation remain separate. A source-only assessment can finish with a model/check plan. Superseded/intermediate views and rollback/state-effect limits are retained without requiring ADR bureaucracy for every edit. |
| `library-usage.md`; `VOCABULARY.md`; `catalog.py::parser/select/searchable_fields` | Commands and flags agree: kinds system/pattern/foundation/notation/tool; exact task/context/quality/scale facets; all text terms and repeated facet values AND; alternatives within kind/status/availability OR. `--root` precedes subcommands, `show` uses a resource ID, source/evidence/body match fields are exposed, and no quality ranking is implied. |
| `FORMAT.md`; `catalog.py::parse_card` | Four common sections are required. Systems additionally require Architecture trace and Diagram implications; notation requires Diagram implications. Ordinary source-inspected mode requires no executed-flow receipt. Optional visual mode requires visual receipt; documented-flow and interaction-tested require flow sequence; interaction-tested also requires URL/actions/observed/method interaction receipt. Documentation matches helper behavior. |

## Limits

This pass did not verify the truth of curated cards, source versions, actual diagram layout, user usefulness or test-run outcomes. A required body section is an annotation obligation, not semantic proof. The coordinator should retain normal package/link/index validation and distinguish any actual Mermaid parser/rendering result from architecture correctness. No new tests based on wording/heading matches were added for this review.
