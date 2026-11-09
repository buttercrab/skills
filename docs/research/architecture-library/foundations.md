# Architecture foundations: source curation record

Research date: 2026-11-07. Own lane: `foundation-*` cards. Twelve original annotations: **11 curated resources and one partial candidate**. Thirteen selected source URLs appear in card metadata; they are not independent experimental confirmations. Additional failed lookup variants are recorded below rather than counted as successful inspection.

## Scope and method

Used the earlier architecture dossier only to identify leads. All substantive support claimed by these cards was freshly read through the web tool in this lane; no old method inspection was silently relabeled as fresh. Primary originals, author/institution-hosted copies and official versioned/method documentation were preferred. Search results located the original Herlihy/Wing, Lamport and FLP papers; search snippets did not supply model/proof evidence.

This is selected-section reading, not a declaration that every page/proof/linked standard was reviewed. No upstream installation, source execution, benchmark, simulation, fault injection, database transaction, deployment or actual organizational intervention occurred. PDF text was inspected; diagram/image URLs or extracted figure text were not treated as visual observations. Every card's Diagram implications section is explicit application reasoning about a useful view, not evidence that a graphic was rendered or an implementation satisfies the property.

## Selected inspection inventory

Exact URLs and revisions are canonical in each card. This table records successful reading locations, not additional sources.

| Card | Source / substantive sections read | Evidence boundary |
| --- | --- | --- |
| `foundation-information-hiding` | Parnas1972 original university copy: responsibility assignment and KWIC alternatives, change comparison, The Criteria, Efficiency and Implementation, pp.1054–1057 | Illustrative decomposition/design argument; contemporary framework or universal overhead benefit not established. |
| `foundation-end-to-end-guarantees` | Saltzer/Reed/Clark1984 original MIT PDF: application knowledge, careful file transfer/performance discussion, duplicate suppression and sequencing, PDF pp.2–7 | Function-placement argument; no current broker/transport implementation or guarantee inspected. |
| `foundation-cap-model` | Gilbert/Lynch2002 original paper university copy: §2 definitions, §3.1 partitioned write/read proof, selected §4.2–4.3 partial-synchrony passages | Formal result under a stated model, not an operational availability percentage or database choice. |
| `foundation-linearizability-histories` | Herlihy/Wing1990 coauthor-hosted Brown PDF: §1.2 examples, §2.1–2.3 histories/definition/pending calls, §3.1 locality statement and opening proof | Selected formal/model sections; no entire-proof audit, implementation verification or runtime trace. |
| `foundation-transaction-isolation` | PostgreSQL18 official manual: Table13.1, §§13.2.1–13.2.3, retry and concurrent sum/insertion example | Versioned product contract, not the ISO SQL standard text, every database or an executed transaction. |
| `foundation-causal-order` | Lamport1978 original author-publication PDF on Microsoft Research: partial ordering/event granularity and Clock Condition/non-converse, pp.558–560 | Selected formal/model reasoning; no physical clock/tracing deployment verified. |
| `foundation-overload-capacity` | Google SRE book chapter21: QPS pitfalls/resource-cost capacity; chapter22: resource exhaustion, Queue Management, load shedding/degradation | First-party practitioner reasoning/reported experience, not reproduced capacity measurements or a universal numeric queue rule. |
| `foundation-slo-measurement` | SRE Workbook chapter2: stakeholder policy, good/total ratios, SLI specification versus implementation, coverage/cost examples | Service-practice method, not a measured target/user-happiness result or safety/correctness tolerance. |
| `foundation-quality-scenarios` | arc42 section10: overview and optional detailed usage/change scenarios, short and long forms | Method-author guidance; no ISO25010 text or empirical sufficiency study read. |
| `foundation-conway-coordination` | Original author-hosted1968 PDF: delegation, graph relationship, examples, management/conclusion pp.28–31 | Conceptual/anecdotal argument; no deterministic org-to-quality prediction. |
| `foundation-decision-records` | Nygard2011 original article: context, decision, status, consequences/supersession and early experience report | Original practice proposal and short experience report, not an efficacy comparison. |
| `foundation-flp-model-lead` | Original institution-hosted JACM1985 PDF opening/abstract only | **Candidate/partial:** exact model/proof unavailable in fresh follow-ups; no model-dependent recommendation promoted. |

The conceptual evidence mode on curated foundations distinguishes reasoning/practice from empirical intervention. CAP, linearizability and logical-clock cards explicitly name their formal/model scope in prose; the schema has no separate formal-proof mode. They are not labeled empirical. No card claims a theorem chooses an architecture outside its assumptions.

## Access gaps and reconciliations

- Parnas, end-to-end, CAP and Lamport selected deeper sections were successfully retrieved as text.
- Herlihy/Wing's CMU original PDF opening loaded, but deeper histories/definition requests repeatedly timed out. The coauthor-hosted Brown copy then supplied substantive histories/model/definition/locality passages; its URL is the card's canonical source. These are copies of one paper, not independent corroboration.
- Conway's author HTML opening loaded but deeper section requests timed out. The linked original PDF supplied the graph argument, examples and conclusion. The paper is one source family; no independent modern empirical validation is implied.
- FLP's JACM original opening loaded, but repeated deeper model/proof requests timed out. The MIT technical-report variant also timed out. The card remains a partial candidate; its schema and diagram advice do not smuggle in an uninspected exact model. Future promotion requires substantive original model/proof inspection.
- PostgreSQL18 is an explicitly versioned manual. The page's current-site navigation/release banner does not change which version's contract was inspected or establish the current behavior of an installed server.
- SRE and arc42 online pages are mutable method/practice texts. The card revisions record the online inspection date. Book examples and thresholds are not copied into recommendations as universal constants.

## Context contrasts preserved

The collection separates responsibility/dependency decisions from runtime sequence, logical order from physical time, object histories from multi-object transactions, formal partition availability from latency objectives, and desired service outcomes from actual measurement coverage. These are distinct questions, not several independent votes for one architecture.

Each card gives an original application question/scenario and negative applicability. Their diagram implications require the relevant boundary, event or measurement relationship and state what the view cannot prove. The examples are proposals, not inspected systems. No star count, cloud provider, microservice count, abstract template or numeric target is used as an architectural quality score.

## Local checks and remaining work

Cards were written only under the assigned foundation filenames; related IDs are empty for coordinator reconciliation. Required metadata/body sections and JSON structure are checked locally. Coordinator will build indexes and validate cross-card relations after all lanes settle. No assessment fixture or private key was read.

Potential later research: full FLP model/proof access; original queueing-law derivations with stable-workload assumptions; contemporary intervention studies about architecture decisions/coordination; measurements of actual decision records or quality-scenario use. These are gaps, not implied additional coverage.
