# AI-assisted writing: evidence curation receipts

Inspected 2026-11-08. This lane adds ten study cards. It is a purposive primary-source collection, not a systematic review, meta-analysis or exhaustive survey. Sources were read through browser text/PDF extraction; no experiment, detector, scoring package, model, dataset replay or participant study was run. Study claims describe the linked historical versions, not current model capabilities.

## Routing by the question being answered

| Card | Primary source/version | Inspected scope | Boundary that matters |
| --- | --- | --- | --- |
| `evidence-creativity-and-diversity` | [Doshi and Hauser](https://arxiv.org/pdf/2312.00506v3), v3 | Methods, exclusions, rated creativity, embedding similarity, discussion | One draft's rating and variety across drafts are different outcomes. |
| `evidence-cultural-context` | [Agarwal et al.](https://arxiv.org/html/2409.11360v3), v3/CHI 2025 | Assignment, cultural task design, group measures, examples, limits | Nationality is an incomplete cultural proxy; group effects do not reconstruct an individual's counterfactual. |
| `evidence-bounded-productivity` | [Noy and Zhang](https://shakkednoy.com/Noy%20Zhang%20NBER%20SI.pdf), N=453 manuscript | Method, grading, attrition, results, limitations | Bounded generic writing can benefit; precise facts and organization-specific context were outside the central task. |
| `evidence-capability-boundary` | [Dell’Acqua et al.](https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf), WP 24-013 | Experimental conditions, inside/outside task outcomes, recommendation-rating definition | Recommendation Quality is a task measure; correctness is separately measured. |
| `evidence-detector-bias` | [Liang et al.](https://arxiv.org/html/2304.02819v3), v3 | Corpora, detector results, rewriting sensitivity, limitations | Historical, nonmatched corpora cannot establish current rankings or authorship certainty. |
| `evidence-poetry-readers-and-labels` | [Porter and Machery](https://pmc.ncbi.nlm.nih.gov/articles/PMC11564748/), 2024 | Selection, both designs, Study 1 results and reader experience | Partial access; no detailed Study 2 effect estimates promoted from the older dossier. |
| `evidence-claim-verification` | [FActScore](https://aclanthology.org/2023.emnlp-main.741.pdf), EMNLP 2023; [VeriScore](https://arxiv.org/html/2406.19276v1), v1 | Definitions, source scope, extraction/verification human-evaluation setup, results and limits | Precision, coverage, verifiability and quality remain different questions. |
| `evidence-entity-coherence` | [Chiang and Lee](https://aclanthology.org/2024.findings-acl.160.pdf), ACL Findings 2024 | Grouping method, human annotation, Table 3, limitations | Independently supported facts can still describe the wrong combined subject. |
| `evidence-critical-thinking-self-report` | [Lee et al.](https://advait.org/files/lee_2025_ai_critical_thinking_survey.pdf), CHI 2025 | Instruments, cleaning, Table 4, interpretation and limitations | Reported effort is not objective skill loss or a causal longitudinal effect. |
| `evidence-collaboration-and-agency` | [CoAuthor](https://cs.stanford.edu/~minalee/pdf/chi2022-coauthor.pdf), CHI 2022 | Interface, curation, interaction measures, ownership correlations, causal cautions | Collaborative process and ownership are not captured by a final word percentage alone. |

Each card separates reported observations from our proposed editorial applications. Questions, preservation lists, sequential review passes and claim ledgers are recommendations for use, not experimentally validated effects of this skill.

## Conflicts and corrections carried into curation

- Benefits and costs can coexist. The creativity and productivity cards supply counterevidence to a universal claim that AI writing is poor. They do not cancel the cultural, diversity, factual or agency questions, whose measures differ.
- The earlier local research dossier `docs/research/fundamentals-deep/writing.sources.jsonl` and `review-writing.md` were used as discovery leads. Its March 2023 Noy/Zhang lead records N=444. This lane freshly read the author-hosted N=453 manuscript instead. No numerical results were combined across those versions, and identity with publisher PDF bytes was not established.
- Doshi's 293 is the analyzed writer total across arms, not the number treated. Recruitment and exclusions are explicit in Methods. This card cites arXiv v3 rather than silently treating it as a later published revision.
- The consultant study's Recommendation Quality finding is not relabeled as an isolated improvement in prose style. Its task-specific correctness evidence is separately retained.
- The detector paper is evidence of historical failure modes, not a service recommendation, universal rate, evasion recipe or authorship classifier.
- The critical-thinking paper explicitly measures subjective reports. Causal cognitive decline and long-term skill decay are not findings established by that design.
- Factuality papers are split into two distinct decisions, not three near-duplicate metric rankings: what a claim is supported by, and whether combined facts retain the same referent. Neither decision certifies an article's quality.

## Access failures and unresolved leads

| Source | Observed access | Consequence |
| --- | --- | --- |
| Doshi v3 HTML | `https://arxiv.org/html/2312.00506v3` returned 404. | Recovered the versioned PDF; no HTML-dependent claim retained. |
| Porter PMC | Initial reads exposed design and Study 1 results. Later opens returned a three-line recaptcha page. The `?pdf=render` variant was inaccessible. | Card availability is partial. Its empirical claim is restricted to the inspected Study 1 result; detailed framing estimates require recovery. |
| Porter publisher | Nature URL redirected to an inaccessible identity-service endpoint. | Not treated as a successful additional read or an independent source. |
| König et al., nutrition information/source labels | PMC `https://pmc.ncbi.nlm.nih.gov/articles/PMC13641973/` initially exposed bibliographic material; subsequent request returned recaptcha; `?pdf=render` inaccessible. | No card promoted. The earlier local dossier contains a targeted 2026-11-07 read, but this lane did not freshly re-inspect the methods/results. Recover before using its genre contrast or any label-effect claim. |
| Cognitive-burden / Your Brain on ChatGPT lead | Earlier dossier describes a selected-method read of a long mirror, with original-byte identity unresolved. This lane did not re-open it. | Excluded rather than padding the collection with an abstract-only cognition claim. It would need independent methods, sample/crossover, instrument and limitation inspection. |
| Oversized multi-source tool response | One broad call exceeded the available context and was truncated. | Material in the invisible output was not counted as inspected; relevant sections were requested again in smaller reads. |

No current detector comparison, professional long-form author trial, multilingual writing experiment or causal test of this skill's questions was performed. English and short-task evidence dominate this lane. Additional reader-label evidence in informational prose remains a specific coverage gap; poetry results must not stand in for it.

## Maintenance actions

1. Recover the two blocked reader-label texts and inspect design, manipulation awareness, full results and limitations before adding contrasting cards.
2. When new versions change a population, instrument, model or outcome, update that exact card's source revision and scope; retain disagreements rather than silently blending estimates.
3. Broaden beyond English, crowd tasks and brief professional prompts. Preserve negative and null results where they address the same decision and outcome.
4. Review metrics as aids to locating evidence. Any claim of improved articles from the workflow itself requires an appropriate reader/task evaluation, not benchmark transfer by analogy.
