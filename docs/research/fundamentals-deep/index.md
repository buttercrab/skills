# Fundamentals skill library: deep research index

Research date: 2026-11-07 (Asia/Seoul).

Subsequent work: [focused research on eliciting creative direction](../design-pilot/questioning-research.md), the [design pilot](../../../skills/design-with-intent/SKILL.md), and [trial results](../../evaluations/design-pilot/results.md). Counts below describe the original deep-research snapshot; the focused follow-up has its own ledger.

Start with the [cross-domain synthesis](synthesis.md). It explains what changed, what the evidence supports, and how the findings could become skills. The [initial survey](../2026-11-07-fundamentals-skill-library.md) is retained as an earlier snapshot.

## What was produced

Seven subagents and the coordinator developed nine domain dossiers, followed sources into methods and implementation, and performed eight targeted source reviews. The code/contracts dossier and article-revision work were added after the first deep round exposed gaps.

The registries contain **270 source records: 242 inspected, 12 partial, 13 inaccessible, and three discovery-only**. These are evidence units, not 270 independent studies. Some records bundle several source/configuration/test files; other records inspect related chapters or different versions of one work. Mirrors and institutional families are not independent corroboration. “Inspected” means substantive relevant content was examined, not that every page or code path was read.

The [search and evidence method](research-method.md) defines inclusion, statuses, evidence types, limitations, and follow-up. The [source index CSV](sources-index.csv) provides a filterable catalog; claim-specific detail lives in each JSONL ledger. [Coverage metadata](coverage.json) records the generated counts and validation scope.

## Domain dossiers

| Dossier | Inspected records | Other records | Concrete depth |
| --- | ---: | ---: | --- |
| [UX and flows](ux-flows.md) · [ledger](ux-flows.sources.jsonl) | 29 | 4 | Nine decision cases; original sampling/choice/menu methods; Figma reversals; Duolingo confounding; literacy/permission/cultural-data cases. |
| [Visual design](visual-design.md) · [ledger](visual-design.sources.jsonl) | 38 | 4 | Seven comparative cases; typography methods; exact WCAG scope; localization; system migrations and retrospectives; six skill/rubric samples. |
| [Repository maintainability](repositories.md) · [ledger](repositories.sources.jsonl) | 29 | 4 | Six commit-pinned change paths: p-limit, uv, Django, CPython, Kubernetes and MDN; original review/complexity/coverage research. |
| [Architecture and diagrams](architecture.md) · [ledger](architecture.sources.jsonl) | 30 | 1 | Six system cases; original modularity/end-to-end/consistency arguments; four historical code snapshots; failure and reconciliation traces. |
| [Code and contracts](code-and-contracts.md) · [ledger](code-and-contracts.sources.jsonl) | 18 | 0 | Three pinned contract/implementation/test cases in Rust, Go and protobuf-Go; caller obligations, errors, partial effects and compatibility. |
| [Writing](writing.md) · [ledger](writing.sources.jsonl) | 33 | 6 | Five annotated craft cases; three actual Distill revision diffs; Korean/Japanese guidance; original composition and AI-writing studies. |
| [Verification](verification.md) · [ledger](verification.sources.jsonl) | 27 | 5 | Six detailed cases; oracles/generators/mutation/flakiness; incident causal chains; performance-method counterevidence; scoped security guidance. |
| [Skills and evaluation](skills-evaluation.md) · [ledger](skills-evaluation.sources.jsonl) | 26 | 0 | Seven direct skill studies, judge-method research, actual skill libraries, public result records, verifiers and scorer implementations. |
| [Knowledge synthesis](knowledge-synthesis.md) · [ledger](knowledge-synthesis.sources.jsonl) | 12 | 4 | Human analogy/transfer limits, model example/order/context studies, evidence appraisal and original research-to-instruction proposals. |

All dossiers distinguish sourced findings from proposed instructions and teaching exercises. The latter have not been forward-tested.

## Follow-through that changed or strengthened the findings

| Investigation | Result |
| --- | --- |
| uv generation workflow → command semantics → docs validation → publication configuration | Resolved a suspicious-looking DryRun step: generation, checked-in freshness and build-time derived documentation are different claims. No defect asserted. |
| SQLite commit article → historical pager → VFS wrappers | Confirmed a conditional representation discrepancy while distinguishing an xSync request from observed syscall/durability. |
| Skill-evaluation paper → scorer contract → implemented judge and wrapper | Separated outcome quality from skill-naming reward and found a README/formula discrepancy at a pinned path. Published aggregates were not rescored. |
| Writing-study methods and version records | Corrected treatment/sample wording, kept Noy manuscript versions separate, and distinguished Recommendation Quality from prose-only quality. |
| Performance paper → later experiment → compiler/platform settings | Preserved smaller variation alongside significant shifts and changed setup; avoided attributing the contrast solely to workload size. |
| Published explanation → actual revision commits | Replaced inferred author process with inspectable changes to ordering, questions, explanation and assumptions. |

## Targeted source reviews

Each review sampled consequential claims against underlying sources. None is a full audit of every registry entry or an experimental reproduction.

| Reviewed area | Review artifact | Refinements incorporated |
| --- | --- | --- |
| Repositories | [review](review-repositories.md) | Complexity thresholds and ambiguous severity-scale interpretation; publication boundary. |
| Architecture | [review](review-architecture.md) | VFS versus syscall evidence, synchronization flags, expectation expiry versus scheduling, theorem/model scope. |
| Skills evaluation | [review](review-skills-evaluation.md) | Outcome scorer implementation; up-to-five available dimensions; paper cleanup claim versus narrower inspected code. |
| UX | [review](review-ux-flows.md) | Historical proficiency locator and experimenter-assisted completion. |
| Visual design | [review](review-visual-design.md) | Reflow orientation, actual five-font assignment, separate search/recall sample sizes. |
| Writing | [review](review-writing.md) | Treatment denominator, manuscript version, rating construct and pagination. |
| Verification | [review](review-verification.md) | Performance comparison conditions/locator and Cloudflare's permitted rollout procedure. |
| Code/contracts | [coordinator check](review-code-and-contracts.md) | Destination preservation versus source consumption; narrow branch versus whole-system guarantee. |

## What is ready, and what remains unproved

Ready: source-linked domain knowledge, case analyses, disagreements, application conditions, counterexamples, candidate instructions, and realistic evaluation scenarios. The synthesis contains a provisional capability map that preserves existing audit/refactor/contract-propagation ownership.

Unproved: whether the proposed instruction sets improve actual agent outcomes, intended-user usability, visual judgment or authorial voice. No new skills were installed or executed; no external source builds, test suites, benchmark reruns, deployment checks or product usability experiments were performed. Static code/test inspection and reported study/incident outcomes are labeled accordingly.

Coverage remains weaker for games, native mobile/embedded/data pipelines, private teams, long-form professional literary work, disabled-user complete journeys, multilingual/cross-cultural empirical work and longitudinal effects. The original question remains open to reframing; the current taxonomy is a research result to test, not a permanent catalog.
