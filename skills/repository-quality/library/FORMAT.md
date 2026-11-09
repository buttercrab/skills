# Repository reference card format

Canonical cards are `library/entries/<id>.md`. Use UTF-8 Markdown with JSON frontmatter between two `---` lines. The generated Markdown/JSON index is a browse/search view, never the authoritative annotation. No remote code is executed to build or search it.

Required fields:

- `id`: lowercase hyphenated filename stem.
- `kind`: `repository`, `guide`, `standard`, `study`, or `tool`.
- `title`, `summary`: substantive strings; describe a transferable mechanism, not a quality ranking.
- `status`: `curated`, `candidate`, `needs-review`, or `retired`.
- `availability`: `public`, `partial`, `local-only`, or `unavailable`.
- `facets`: lists for `tasks`, `contexts`, `languages`, `scale`. Labels are lowercase hyphenated slugs. Use `language-agnostic` for appropriate general guidance. Scale describes applicability, not prestige; useful labels include `small-project`, `single-package`, `multi-package`, `large-project`, `cross-scale`.
- `sources`: nonempty list of objects with `url`, `title`, `locator`, `revision`. Prefer exact commit URLs for repository claims and precise paths/sections. A default-branch link is mutable; state its access date rather than implying a frozen version.
- `evidence`: `mode` (list), `inspected_at` (ISO date), `freshness`, `scope`. Modes: `source-inspected`, `documented-flow`, `empirical`, `conceptual`, `discovery-only`, `partial`, `visual-inspected`, `interaction-tested`. Freshness: `versioned`, `live-at-inspection`, `historical`, `unknown`. Use only modes actually supported. Read source/configuration establishes intended mechanics, not an executed command, passing CI, repository protections, release or installed package.
- `reuse`: original annotation/link scope; do not redistribute upstream files or give a legal opinion.
- `related`: list of existing IDs; empty while lanes curate independently. Root will connect relevant cards after reconciliation.

Required body sections: `## When to use`, `## What to inspect`, `## What to borrow and adapt`, `## Mismatches and limits`. Repository cases also include `## Change path`: a concrete trigger → authoritative input → source/tests/docs/configuration touched → relevant validation/distribution. Identify what was actually followed and what remains unknown. Root tree listings alone do not establish this path. Guides/standards/studies should give a concrete application contrast rather than a universal checklist.

Each repository card should inspect multiple substantive artifacts (normally a contributor/entry document, an authoritative source/manifest/build input, and a test/CI/documentation/release boundary). Use enough evidence for the claimed mechanism; do not pad counts. Keep sources exact and narrow. Explain context mismatch: a mature monorepo may illustrate source authority while imposing unsuitable governance cost on a two-person library.

Candidate discovery and curated support are different statuses. A failed lookup is not evidence of nonexistence. If a source or requested artifact is unavailable, preserve the access gap and narrow the claim. Direct evidence may contradict a popular README account; reconcile the difference. Do not interpret missing inspected proof as a demonstrated defect.

Use `source-inspected` for read-only repository/configuration tracing; the `Change path` body section can describe intended mechanics without claiming a flow was exercised. If using `documented-flow`, also include `flow_evidence`: list of objects with `url`, `locator`, `sequence` (nonempty string or string list) and `method`. Optional `visual-inspected` similarly needs `visual_evidence` (`url`, `locator`, `observed`, `method`); `interaction-tested` needs `interaction_evidence` (`url`, `actions`, `observed`, `method`). An `interaction-tested` card also needs the `flow_evidence` sequence receipt. These support claim-specific receipts; none is required simply because a repository has CI or contributor docs.
