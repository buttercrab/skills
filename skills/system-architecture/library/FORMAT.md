# Architecture resource card format

Canonical entries are UTF-8 Markdown in `library/entries/<id>.md`, with a strict JSON object between `---` lines. Generated indexes are views of these original annotations. No upstream source body or artwork is redistributed.

Required metadata:

- `id`: lowercase hyphenated filename stem; `kind`: `system`, `pattern`, `foundation`, `notation`, or `tool`.
- `title`, `summary`: concrete transferable mechanism, not a quality ranking.
- `status`: `curated`, `candidate`, `needs-review`, or `retired`.
- `availability`: `public`, `partial`, `local-only`, or `unavailable`.
- `facets`: unique slug lists for `tasks`, `contexts`, `qualities`, `scale`. Useful tasks: `decompose`, `trace`, `compare`, `document`, `diagram`, `migrate`, `verify`, `model-failure`. Qualities describe relevant constraints (e.g. consistency, availability, durability, latency, operability, evolvability), not quality scores. Scale is applicability such as `single-process`, `single-deployment`, `multi-deployment`, `distributed`, `cross-scale`; no arbitrary workload threshold.
- `sources`: nonempty objects with `url`, `title`, `locator`, `revision`. Prefer immutable commit URLs for inspected code and version/section IDs for standards/papers. Mutable documentation needs an explicit access/version boundary.
- `evidence`: mode list, `inspected_at` ISO date, `freshness` (`versioned`, `live-at-inspection`, `historical`, `unknown`), and `scope`. Modes: `source-inspected`, `documented-flow`, `empirical`, `conceptual`, `discovery-only`, `partial`, `visual-inspected`, `interaction-tested`. Reading implementation/config/tests is not execution, deployed topology or current operational guarantees.
- `reuse`: original annotations and links, copying/asset limits; `related`: existing card IDs (empty until coordinator reconciliation).

Required body sections for all cards: `## When to use`, `## What to inspect`, `## What to borrow and adapt`, `## Mismatches and limits`.

System cards also require `## Architecture trace`: a concrete behavior/change → owning boundary/state → selected implementation/config/test or first-party specification → claimed guarantee/failure limit. Inspect normally at least three substantive source locations; a README architecture picture alone is insufficient for implementation claims. Papers/docs-only cases are valid if clearly labeled with their actual evidence scope.

System and notation cards require `## Diagram implications`: what question/view is useful, which boundaries/arrows/state/failure points it must expose and what cannot be inferred. Diagram source inspection differs from actual visual viewing/rendering; do not claim the latter from an image URL or Mermaid text. Never require all C4/UML levels for a small problem.

Ordinary read-only tracing can use `source-inspected` without flow receipts. If `documented-flow` is used, include `flow_evidence` objects with URL, locator, sequence (nonempty string or list) and method. `visual-inspected` requires `visual_evidence` URL/locator/observed/method. `interaction-tested` additionally requires flow_evidence and `interaction_evidence` URL/actions/observed/method. No executions are required for curation.

Explain when a mechanism should not transfer: workload, failure assumptions, team capability, operations budget, state/transaction ownership, deployment constraints or evidence limitations. A source count or famous system does not establish superiority. Formal results retain their exact model; published measurements remain authors' reports unless reproduced. Historical inspection can be retained only with attribution and honest freshness/access scope.
