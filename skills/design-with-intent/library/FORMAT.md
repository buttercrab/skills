# Resource card format

Each `entries/*.md` file is authoritative. The generated `index.md` and `index.json` are browse/search views; edit the card and rebuild them. Stable IDs need not change when a title, classification or recommendation changes.

Cards begin with `---`, a JSON object, and `---` on separate lines. JSON is a YAML-compatible frontmatter subset and lets bundled tooling read the catalog with Python's standard library. The body is original annotated Markdown, not a copied upstream skill or manual.

## Required metadata

| Field | Shape and meaning |
| --- | --- |
| `id` | Unique lowercase letters/digits/hyphens; matches filename stem. |
| `kind` | `skill`, `example`, `system`, `foundation`, or `tool`. |
| `title`, `summary` | Nonempty human-readable identity and short selection-oriented description. |
| `status` | `curated`, `candidate`, `needs-review`, or `retired`; editorial readiness. |
| `availability` | `public`, `partial`, `local-only`, or `unavailable`; access, distinct from quality. |
| `facets` | Object with lists `tasks`, `contexts`, `platforms`, `character`; use lowercase hyphenated labels. Empty character is appropriate when appearance was not inspected or irrelevant. |
| `sources` | Nonempty list of objects with `url`, `title`, `locator`, `revision`; use `not-versioned`/`not-pinned` honestly rather than inventing a revision. Prefer identifiable primary HTTPS URLs. |
| `evidence` | Object with `mode` (nonempty list), `inspected_at` (ISO date or null), `freshness`, and `scope`. |
| `reuse` | Nonempty original-note on linking, observed license scope and any unknown copying rights. This catalog does not redistribute third-party packages/assets by default. |
| `related` | List of existing resource IDs; may begin empty while coordinating new cards. |

Evidence mode values: `source-inspected`, `documented-flow`, `visual-inspected`, `interaction-tested`, `empirical`, `conceptual`, `discovery-only`, `partial`. Multiple modes can apply, with `scope` specifying exactly what was inspected. A source-inspected README is not an executed skill. A screenshot is not a tested interaction.

Freshness values: `versioned`, `live-at-inspection`, `historical`, `unknown`. These describe the evidence snapshot, not the current state of every product. Historical resources can remain curated. Updating a date alone is not revalidation.

Curated entries require an actual inspection date, a substantive evidence mode beyond discovery-only, and specific source locators. Unknown/inaccessible sources can remain candidates or needs-review entries; do not promote their unverified claims.

## Visual and flow receipts

When evidence includes `visual-inspected`, add a nonempty `visual_evidence` list. Each item has `url`, `locator`, `observed`, and `method`: the actual source image/screen viewed, relevant region/state, narrow observation, and viewing method. Describe only what was seen. Original source links are preferred; do not copy or download assets to evade access/reuse restrictions.

When evidence includes `documented-flow` or `interaction-tested`, add a nonempty `flow_evidence` list with `url`, `locator`, `sequence`, and `method`. The sequence may be a string or list of relevant states. Identify whether it came from a detailed source account, source code, or actual interaction. Actual interaction additionally needs an `interaction_evidence` list with `url`, `actions`, `observed`, and `method`.

When multiple actors appear, identify whose sequence is described and keep their states distinct. Merchant configuration, shopper checkout and server review are different flows. A documentation website's URL does not establish that the documented product interaction runs on the web; platform facets describe the actual target context.

Only claim visual matching from actual inspected visual evidence, and flow matching from appropriate sequence/state evidence. Catalog readers still need to inspect the selected material for consequential or fresh claims in their current task.

## Body

Include these sections with useful original annotation:

- `## When to use`: what task/context this resource can help.
- `## What to inspect`: exact sections/files/screens and the purpose of reading them.
- `## What to borrow and adapt`: transferable mechanism and necessary adaptation, with a concrete application where helpful.
- `## Mismatches and limits`: inappropriate uses, conflicts, access/evidence limits and significant counterexamples.

Optional sections can add genuine depth: a short annotated case, related alternatives, capability/dependency details, or maintenance notes. Avoid boilerplate, invented measurements, long quotations and repeating an entire source manual. About 150–350 words of purposeful annotation is often sufficient, but this is not a quality threshold.

## Search and maintenance

The compact index should expose identity, status/access, summary, facets, evidence scope/date and card path. The full card supplies detail. Search labels and text across relevant resource roles before deeply reading candidates; matching should explain both fit and mismatch rather than produce an unexplained universal score.

Use `related` for complementary, alternative or same-family resources and explain the relationship in the body when it is consequential. Related IDs do not imply independent corroboration. Keep discovery notes and source search trails in the repository's research records; operational cards must remain usable after the package is relocated.
