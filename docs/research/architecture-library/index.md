# Architecture library: research, diagrams and coverage

Edition begun: 2026-11-07; completion record: 2026-11-08 (Asia/Seoul). First edition. Deliverable: [system-architecture skill](../../../skills/system-architecture/SKILL.md), [annotated resource library](../../../skills/system-architecture/library/index.md) and [reading paths](../../../skills/system-architecture/library/PATHS.md). Example systems remain research sources, not implementation targets.

## Collection

| Role | Entries | Contribution |
| --- | ---: | --- |
| System cases | 10 | Selected implementation/interface/architecture paths for state, coordination, persistence, process and dependency boundaries. |
| Patterns/decision contrasts | 12 | Decomposition/distribution, ports, messaging, CQRS/history, outbox/saga, overload/retry, caching and migration tradeoffs. |
| Foundations | 12 | Original decomposition/guarantee/model arguments, consistency histories, causality, isolation, objectives, coordination and decisions; one is a partial candidate. |
| Notation | 7 | Purpose-specific logical, runtime, deployment, multi-view, flow, sequence and state representation. |
| Tools | 3 | Model/view, UML-style and syntax-validation capabilities with explicit limits. |

**44 entries: 43 curated and one candidate**, with 100 selected links / 93 distinct source URLs, 88 related-resource edges and approximately 11,000 original body words. [Coverage JSON](coverage.json) gives exact fields. Entries/source locations are not independent experiments or an exhaustive architecture census. One partial FLP discovery lead is deliberately not promoted to proof/model guidance after fresh follow-up failed.

## Source selection and reading

Four parallel lanes used original authors/papers, exact-pinned repository artifacts, official specifications and first-party docs. The prior architecture dossier supplied leads; selected substantive support was read again rather than relabeled as current. Each system card follows a concrete behavior, owner/state/control relationship and failure/guarantee limit, with a separate explanation of the useful diagram view. Pattern/foundation cards preserve assumptions, costs, disagreement and negative transfer.

| Lane | Inventory and findings |
| --- | --- |
| [System cases](systems.md) | Ten cases / 30 links: 22 pinned repository files and eight first-party documentation pages. SQLite commit/WAL checkpoint; PostgreSQL processes; rust-analyzer derived state; Valkey persistence; Kubernetes reconciliation; Raft host integration; NATS delivery; DuckDB pipeline dependencies; Temporal replay/activities; Bazel dependency evaluation. |
| [Patterns](patterns.md) | Twelve cards / 27 selected primary URLs. Explicit counterpositions, bounded work, message/external-effect distinctions, transaction/compensation limits and intermediate migration states. |
| [Foundations](foundations.md) | Twelve cards / 13 URLs, selected original model/definition/limitation sections. Information hiding, end-to-end placement, CAP, linearizability, causality, transaction isolation, overload, SLOs, quality scenarios, Conway and ADRs. FLP remains a candidate because full-model/proof follow-up was inaccessible. |
| [Diagram methods/tools](diagrams.md) | Ten cards / 30 links across 24 official URLs. C4, arc42, Mermaid, Structurizr and PlantUML role distinctions; actual text/code inspection, not source-image viewing or rendering. |

These inventories overlap source families; repeated primary locations are not independent corroboration. A pinned file read is not an executed algorithm/test or a deployed guarantee. Original-author arguments, formal models, implementation contracts and empirical measurements support different claims. No real system, cluster, provider, architecture migration or upstream application/test suite was executed during curation.

## What the comparisons change

- A module, process, transaction, team, trust and deployment boundary can differ. [Information hiding](../../../skills/system-architecture/library/entries/foundation-information-hiding.md), [ports/adapters](../../../skills/system-architecture/library/entries/pattern-ports-and-adapters.md) and [PostgreSQL](../../../skills/system-architecture/library/entries/system-postgresql-process-isolation.md) provide different lenses; directories or service nouns alone are not the decision.
- Delivery/acknowledgment is not a complete business guarantee. [End-to-end placement](../../../skills/system-architecture/library/entries/foundation-end-to-end-guarantees.md), [outbox](../../../skills/system-architecture/library/entries/pattern-transactional-outbox.md), [sagas](../../../skills/system-architecture/library/entries/pattern-saga-compensation.md), [NATS](../../../skills/system-architecture/library/entries/system-nats-delivery-effects.md) and [Temporal](../../../skills/system-architecture/library/entries/system-temporal-replay-activities.md) make their separate assumptions visible.
- Formal shorthand must preserve its model. [CAP](../../../skills/system-architecture/library/entries/foundation-cap-model.md), [linearizability](../../../skills/system-architecture/library/entries/foundation-linearizability-histories.md), [causal order](../../../skills/system-architecture/library/entries/foundation-causal-order.md) and [isolation](../../../skills/system-architecture/library/entries/foundation-transaction-isolation.md) are not interchangeable labels for a whole system's correctness or latency.
- Coarse boundaries and independent delivery have a real [contextual disagreement](../../../skills/system-architecture/library/entries/pattern-coarse-boundaries-before-distribution.md). Source counts do not settle it; workload, domain uncertainty, operating capacity and migration cost matter.
- A [logical container](../../../skills/system-architecture/library/entries/diagram-c4-context-container.md), [runtime scenario](../../../skills/system-architecture/library/entries/diagram-c4-runtime-scenario.md) and [deployment instance](../../../skills/system-architecture/library/entries/diagram-c4-deployment-mapping.md) answer different questions. None requires drawing every view for a small change.

## Source and semantic review

Independent cross-lane reviewers sampled six cards against primary sections. A separate reviewer inspected the coordinator's four original diagram examples semantically, and self-rechecked two authored notation claims. This is not a full independent audit of every card.

| Review | Result / correction |
| --- | --- |
| [Foundation source sample](review-foundations.md) | CAP model/theorem/partial-synchrony and original operation-history/locality sections supported the qualified annotations; no material correction requested. |
| [System source sample](review-systems.md) | Raft/Kubernetes central limits supported. Added same-pin README/Ready-comment ordering ambiguity, async response versus forbidden Advance distinction, and request/observation/expiry wording. No integrated host or cluster was tested. |
| [Pattern source sample](review-patterns.md) | Four primary pages support bounded outbox and saga claims; no material defect found at the inspected scope. |
| [Diagram semantic review](review-diagrams.md) | Corrected a file→importer label whose verb read backward, and clarified invocation versus data flow. Other examples keep accepted/committed/unknown/proposed limits. C4/Structurizr primary rechecks are explicitly self-rechecks, not independent-card audit. |
| [Workflow integration](workflow-review.md) | Scope, question handling, query syntax and conditional diagram/evidence obligations are coherent; no universal architecture or diagram suite imposed. |

The catalog's exact `qualities` facet retains distinctions; only the obvious comprehensibility→understandability alias was normalized editorially. Related cards/reading paths are navigation aids, not quality rankings or independent corroboration.

## Original diagram validation

The skill includes four original illustrative diagrams plus three original notation-card sketches. All **seven Mermaid blocks parse with Mermaid 12.3.0** using a temporary JSDOM 31.0.0 environment for the parser's DOM sanitization dependency. They were not rendered. No source-image/figure was viewed or operational behavior tested. Syntax validity, visual readability, semantic agreement and actual architectural correctness remain separate outcomes.

An initial attempt hit DOM setup errors and found a real sequence-label semicolon syntax error. The setup and labels were corrected, then all seven parsed. The [validation record](diagram-validation/examples-results.json), [initial attempt](diagram-validation/first-attempt.json) and original checker/environment manifest under `diagram-validation/` preserve that history. Initial wrapper classification labeled all caught errors “syntax-error”; the DOM dependency failures were environment failures, not source grammar defects. Semantic review independently caught the direction/label issue that parsing could not.

Optional parser dependencies were installed only in a temporary validation directory. The active skill's browse/search/helper runtime remains Python-stdlib-only and needs no Mermaid/JSDOM installation. Upstream source code, assets and source diagrams were not copied into the library.

## Coverage limits and maintenance queue

This edition is strongest on state/coordination boundaries, small-versus-distributed decisions, failure semantics, evolution and diagram purpose. It is weaker on hardware/embedded real-time architectures, specialized regulated domains, heterogeneous physical/network security, ML/data-platform architecture, enterprise topology migration and human comprehension studies of diagrams. System cases show selected paths, not whole-system correctness or current production topology.

Useful next evidence includes actual user decisions on fresh tasks, independently rendered readability checks when visual output is promised, deeper failure/load scenarios where authorized, and primary material for unfamiliar constrained environments. No partial lead should be promoted by an abstract or diagram alone. Update source versions/model assumptions deliberately and preserve earlier snapshots/reviews. No global installation, publishing, automation or real-project changes were performed.

[Assessment results](../../evaluations/architecture-library/results.md) separately review five independently authored fictional source-only cases. They do not establish general effectiveness or live system behavior.

## Post-trial instruction revision

The first frozen assessment cohort exposed six invalid sequence blocks despite useful manual reasoning. The active v1.1 guidance adds the official message-delimiter rule and explicit syntax-verification limits; originals and later punctuation-only corrections remain separate. All 13 corrected assessment blocks parse, without rendering or operational claims. See [assessment results](../../evaluations/architecture-library/results.md); no fresh cohort has tested v1.1 wording.
