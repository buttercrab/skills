# Writing resource card format

Canonical cards are UTF-8 Markdown at `library/entries/<id>.md`, with a strict JSON object between `---` lines. Generated indexes are browse/search views, not authoritative annotations. Original articles, drafts, screenshots and upstream source bodies are not redistributed.

Required metadata:

- `id`: lowercase hyphenated filename stem; `kind`: `example`, `guide`, `foundation`, `study`, or `tool`.
- `title`, `summary`: concrete craft/decision mechanism, not a quality ranking or authorship detector.
- `status`: `curated`, `candidate`, `needs-review`, `retired`.
- `availability`: `public`, `partial`, `local-only`, `unavailable`.
- `facets`: unique slug lists `tasks`, `genres`, `languages`, `contexts`. Tasks may include `frame`, `structure`, `explain`, `argue`, `report`, `revise`, `verify`, `preserve-voice`, `evaluate`. Genres describe applicability (e.g. article, essay, explanation, tutorial, argument, reported-feature, personal-essay, research-summary). Contexts describe actual readers/conditions/evidence, not good/bad authorship labels.
- `sources`: nonempty objects with `url`, `title`, `locator`, `revision`. Precise original sections/passages/version/diffs; mutable sources need inspection date and scoped claims. No invented author/editing history or inaccessible-article summary from a snippet.
- `evidence`: `mode` list, `inspected_at` ISO date, `freshness` (`versioned`, `live-at-inspection`, `historical`, `unknown`), `scope`. Modes: source-inspected, documented-flow, empirical, conceptual, discovery-only, partial, visual-inspected, interaction-tested. Craft reading is not reader testing, causal improvement or proof of human/AI origin. Empirical studies need actual method/result/limit inspection, not abstract-only promotion.
- `reuse`: original analysis and links; no substantial quotations/full-article paraphrase or style-cloning instructions. `related`: existing IDs (empty until coordinator reconciliation).

Required body sections: `## When to use`, `## What to inspect`, `## What to borrow and adapt`, `## Mismatches and limits`.

Example cards also need `## Craft trace` and `## Revision implications`. Follow reader question/angle → particular opening/middle/ending or precisely scoped passage → evidence/craft choice → transferable decision. Inspect the whole piece before claims about whole-piece structure; otherwise narrow the card to inspected sections and access limits. Revision implications are our proposed transfer, not evidence of the author's actual drafts. Actual revision claims require inspected before/after artifacts or diffs with exact locators, not commit-message inference.

Keep source-derived summary within source word limits. Prefer original decision analysis and short locators; avoid direct article quotations. For protected third-party readings not supplied by the user, keep verbatim quotation within the applicable source limit (normally at most 25 non-lyrical words per source across curation artifacts). Prefer minimal quotations as a curation house practice even where broader reuse is permitted; this does not restrict editing a user-supplied draft or imply that public-domain material has the same copyright limit. No copying passages to imitate a living author's distinctive voice. Describe general craft mechanisms and preserve the user's own voice.

Ordinary reading uses source-inspected. If documented-flow is used, include flow_evidence URL/locator/sequence/method. Visual-inspected needs visual_evidence URL/locator/observed/method; interaction-tested needs both flow_evidence and interaction_evidence URL/actions/observed/method. These modes are optional, not required to make a writing resource useful. Examples, conceptual guidance, empirical studies and automated tool flags have distinct limits.
