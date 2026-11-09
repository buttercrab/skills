# Editorial notes

Delivered a finished internal explanation for application engineers familiar with HTTP but new to caching. The brief supplied sufficient intent; no human-owned choice required clarification.

## Consequential editorial decisions

- Replaced the colleague’s causal and energy headline with “What Cedar’s Cache Trial Shows.” The opening preserves the interesting 40% observation while identifying its denominator, scope and limits.
- Explained hits and misses before interpreting the combined latency distribution. Defined median and p95 where readers need them, rather than assuming knowledge of caching or distribution summaries.
- Made arithmetic inspectable: (200 − 120) / 200 = 40%; (900 − 840) / 900 ≈ 6.7%; (12,000 − 10,000) / 10,000 = 20%. The last percentage describes successful request counts, not capacity.
- Kept missing input data, excluded failures, lack of randomization/pairing and absent interval estimates attached to the conclusions they limit. The seventh paragraph is the brief uncertainty paragraph.
- Kept Birch’s disk-cache, different-renderer benchmark attached to Birch. Explicitly rejected transferring its 50% reduction to Cedar.
- Treated energy as unmeasured, rather than inferring it from elapsed time. Ended with one bounded measurement direction and the supported finding; no rollout recommendation or promises.

## Craft references and limits

Surveyed the frozen guide’s library index, including relevant and neighboring explanatory entries. Read three local cards in full:

1. `example-life-expectancy-definition-before-causes`: selected the card’s mechanism of defining a metric before readers interpret a population difference. Fit: median can be mistaken for an individual request change. Mismatch: the original concerns population health, not HTTP latency. Adaptation: define median and p95 beside Cedar’s actual comparisons.
2. `example-inside-git-inspectable-objects`: considered its bounded inventory and comparable objects. Fit: concrete hit/miss paths help novice readers. Mismatch: a directory tour would fragment this short evidence explanation. Adaptation: one compact mechanism paragraph, rather than an inventory-led article.
3. `evidence-entity-coherence`: applied the card’s proposed editorial referent check to Cedar/Birch. Its underlying study concerns ambiguous biographies; transfer to service benchmarks is an editorial analogy, not a tested intervention.

These are local card readings and craft interpretations. No upstream source body was freshly inspected, and no empirical claim about writing improvement is made. The article cites only the two supplied factual files.

## Revision and verification

Reviewed paragraph progression: observed result → cache mechanism → hit/miss limits → median arithmetic → p95 → counts and failures → uncertainty → Birch boundary → energy boundary → next measurement. Each paragraph adds a distinct reason or distinction.

A sentence-level pass retained units and baselines, qualified causal language, and removed any need for invented implementation details. Rechecked the article against both supplied source bodies, including the difference between review comments and measurements. `wc -w piece.md` returned 764 words, within the requested 650–850 words even when title and source references are included.

Material limits: only the frozen synthetic snapshot and comments support trial facts. No raw data, benchmark execution, external technical verification, reader testing, detector, service call, publication or real-project edit occurred. Missing measurements remain missing.
