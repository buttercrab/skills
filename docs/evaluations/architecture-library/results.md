# System architecture library: delivery and development assessment

Edition begun: 2026-11-07; completion record: 2026-11-08 (Asia/Seoul). Delivered the [system-architecture skill](../../../skills/system-architecture/SKILL.md), [44-resource library](../../../skills/system-architecture/library/index.md), [reading paths](../../../skills/system-architecture/library/PATHS.md) and [original diagram examples](../../../skills/system-architecture/references/diagram-contract.md). The deliverable is reusable guidance and evidence, not changes to example systems.

## Delivered resources and operating behavior

Ten system cases, twelve pattern contrasts, twelve foundation entries, seven notation resources and three tools: **43 curated, one partial candidate**. Cards contain 100 selected links / 93 distinct source URLs and approximately 11,000 original body words. These are resources/locations, not independent studies or exhaustive coverage. [Research inventory and source reviews](../../research/architecture-library/index.md) preserve primary sections, pinned revisions, conditions, disagreements and access gaps.

The skill asks consequential context questions, traces behavior/state/ownership/failure, compares mechanisms and simpler alternatives, and selects diagrams for their question. It separates current, proposed, inferred and unknown claims; logical/deployment/transaction boundaries; source inspection and operational evidence. No default microservice architecture or mandatory full diagram suite is imposed. A bounded example in skill development must return findings to the parent deliverable.

The portable package has canonical Markdown/JSON cards, deterministic browse/agent indexes and a stdlib-only local search helper. No database, hosted service or Mermaid installation is required to read/search it. Existing design/repository libraries and Taster work were not modified in this task.

## Development assessment method

An independent fixture author wrote five fictional source snapshots, prompts, evidence keys and checksums without seeing the new package/cards or prior evaluations. The workflow author wrote and froze 57 package files before reading case contents. Five fresh non-forked agents received the same frozen guide, exact absolute input paths, file inventories and read-only/effect limits; inherited model/effort with no overrides. No baseline or instruction-effect comparison exists.

Tasks cover a small offline ledger, refunds with external uncertainty, incident-documentation reconciliation, compatible authorization migration and a hard one-way transfer constraint. No fixture or upstream code, tests, builds, installs, external services, registries, production queries or real-system edits were requested. Ordinary scoped reads and the local catalog's read/search functions were allowed. Mandatory host guidance remains applicable and recorded. No child agents were requested.

Two consequential policy questions received only their exact scripted answers: refund hold/manual reconciliation after provider retention, and pilot abort thresholds for migration. Other private optional facts were not volunteered. No question-count or diagram-count target was used. Outputs were frozen before independent review and posthoc corrections. [Protocol](protocol.md), [fixtures](fixtures.md) and [archive](runs/2026-11-07/README.md) retain inputs, scopes, relays and hashes.

## Actual diagram failure and correction

Root separately parsed the frozen Mermaid blocks using **Mermaid12.3.0 + JSDOM31.0.0**: **7 of 13 passed; 6 sequence blocks failed**, affecting every original assessment's diagram deliverable. All failures involved unescaped semicolons in message/sequence text, which Mermaid treats as statement separators. Original runners honestly reported manual review rather than parsing; that limit does not make invalid editable source complete.

The [original syntax results](runs/2026-11-07/diagram-syntax-original.json) are preserved. Separate [correction copies](corrections/manifest.json) replace semicolon punctuation with commas inside sequence blocks only, plus an explicit provenance header. **All 13 corrected blocks parse.** These are post-freeze corrections, not new original passes or evidence of the skill's general effectiveness. No diagram was rendered or operationally tested; parsing establishes grammar only.

The active skill is now **v1.1**, with a narrower completion rule and the official sequence-label escape/rephrasing guidance. [Revision snapshot](revisions/v1.1/manifest.json) records the four changed files, including the generated card-hash JSON view. A three-example parser regression check confirms unescaped message failure, documented `#59;` encoding and rephrased-message success. No fresh assessment cohort tests the revised wording; it must not inherit the first cohort's judgments.

Separately, all seven original diagram examples bundled in the skill/notation cards parse. Initial DOM-environment failures and a genuine example-label error were corrected before the first package freeze. Semantic review also corrected an arrow label/direction mismatch that parsing could not detect. Those results are recorded in the [research validation directory](../../research/architecture-library/diagram-validation/examples-results.json).

## Independent content review

The [frozen original review](review.md) and [detailed judgments](review.json) found the substantive reasoning supported in all five supplied contexts, with honest source/proposal/unknown distinctions. Every original delivery remains **qualified/incomplete** because at least one delivered sequence view fails parsing. No original diagram failure was upgraded to a pass.

| Case | Supported reasoning | Original delivery limit |
| --- | --- | --- |
| Offline ledger | Retains local app/storage for measured constraints; distinguishes approval, commit observation, backup freshness and disk-loss recovery. | Two runtime/recovery sequence views fail syntax; proposal is longer than the requested short brief. |
| Refund queue | Durable intent and stable identity, concurrency/external uncertainty, retention-window recovery, distinct acknowledgment and supplied finance policy. | Sequence fails syntax; state view parses. Provider semantics and actual capacity remain unverified. |
| Incident system mapping | Reconciles old README with source and captured deployment, polling, partial writes and dead-letter behavior without inventing a failed-status update. | Runtime sequence fails syntax; deployment view parses. Captured inventory is not current liveness/global topology proof. |
| Compatible rollout | Preserves old-client interface, fail-closed enforcement, revocation-aware rollback/security floor and supplied pilot abort policy. | Request sequence fails syntax; migration state view parses. Policy-version/freshness and broad-cutover evidence remain unresolved. |
| One-way archive | Respects one-way transport and approved paper recovery; separates source knowledge/archive effects, retention, replay/integrity and unestablished trust enrollment. | Transfer sequence fails syntax; two local state views parse. Authenticity/durability/capacity guarantees remain conditional. |

No reported disqualifying scope breach was found. That is bounded review of records, not a full native-trace audit. The reviewer checked fixture checksums/input copies and relevant frozen card portions; upstream source assertions were not independently reverified by this assessment reviewer.

After freezing original judgments, the [separate correction review](correction-review.md) verified hashes and exact punctuation-only sequence transformations plus provenance headers. No intended architectural semantic change was found; corrected syntax results were supplied by root, not independently rerun by that reviewer. Corrected source remains unrendered and does not establish operational correctness or general skill improvement. The active v1.1 wording has no fresh behavioral cohort.

## Structural and scope validation

**49 checks passed**: 23 helper tests, four package tests and 22 isolated installer tests. Metadata validation and generated-view validation passed. The real 57-file first package was copied outside the repository and validated/searched without the research tree or external dependencies. Installer discovery includes twelve skills; no global installation was performed. Later v1.1 metadata/index validation passed; helper/installer code is unchanged.

Original guide/input and frozen assessment hashes matched their manifests. The raw v1 guide remains separate from active v1.1 and correction files. Full native tool traces are not archived; receipts/logs are runner reports plus recorded coordinator relays. Scope/integrity and semantic judgments must be read at that evidence level, not as a certificate of every action.

## Limits

The curation emphasizes state/coordination, small-versus-distributed tradeoffs, failure/evolution reasoning and meaningful views. Formal results retain model assumptions; first-party docs and selected code paths are not whole-system proofs or current deployment observations. The FLP lead remains partial/candidate rather than model guidance. No benchmarks, real failure injections, upstream runtime tests, rendered-diagram readability studies or human architecture-decision outcomes were performed.

The development cases are now exposed material. Future comparison needs fresh tasks/contexts, appropriate controls and separately authorized operational or visual validation if those outcomes matter. No real product, migration, infrastructure, commit, push or deployment was changed.
