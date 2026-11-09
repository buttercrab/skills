# Static review: catalog-backed design workflow

Reviewed 2026-11-07. Scope: current `SKILL.md`, discovery/selection and evidence/maintenance references, UI metadata, browse/index interface, and actual local CLI semantics. No evaluation cases, private keys, trial outputs or expected selections were inspected. No skill/catalog files were edited. This is a static integration review, not evidence of discovery effectiveness or UI quality.

## Verdict

The workflow now addresses the approved library plan. No blocking omission found in broad discovery, contextual matching, human refinement/delegation, scoped source inspection, selected-resource application, portability or third-party instruction boundaries. Two small retrieval improvements are recommended below.

## Actionable refinements

### 1. Expose exact facet vocabulary and filter semantics beside the examples

Location: `references/discovery-and-selection.md:19–27`; implemented behavior in `scripts/catalog.py:342–381`.

The examples are executable and current, but the guide omits the available `facets` command. Filters use exact labels, repeated facet values are ANDed, and text query terms are ANDed as literal case-insensitive substrings. A reader who assumes a semantic search or OR between repeated task filters can miss plausible candidates. General `--help` does not explain every conjunction rule.

Suggested narrow addition: show `python3 scripts/catalog.py facets --status curated`, plus one sentence explaining literal/all-term search, exact facet labels, AND across/repeated facet filters, and OR among repeated kinds/statuses/access values. Keep `--status curated` visible when choosing an inspected recommendation pool, while allowing deliberate browsing of leads. No new retrieval service is needed.

### 2. Normalize obvious grammatical task aliases after curation settles

The current read-only facet summary shows pairs such as `compare/comparison`, `correct/correction`, `collaborate/collaboration`, `compose/composition`, `discover/discovery`, `frame/framing`, `implement/implementation`, `navigate/navigation`, `onboard/onboarding`, `read/reading`, and `recover/recovery`.

Recommend a small editorial canonical-label pass, with an explicit alias glossary, rather than silently adding fuzzy ranking. Existing IDs, source claims and meanings should remain stable; rebuild generated views after changing metadata. The helper's `facets` command can expose the actual vocabulary during this transition.

Do not collapse substantively different concepts merely because they look related: expert use and repeated use are different conditions; a visual direction differs from general choosing; platforms can have parent/subtype relationships. For instance, a `desktop-web` resource is relevant to some broad web searches, while `--platform web` currently requires the exact `web` tag. Where appropriate, explicitly add a broader platform facet in the card rather than make the CLI infer an unstated hierarchy. More involved aliases should be justified by observed missed matches.

## Checked and supported

- **Discovery loop:** entrypoint lines 32–46 require a relevant/neighbouring-family survey, deep card/upstream inspection, fit/mismatch/adaptation, human rejection/mixing and broader external discovery. Reference lines 7–13 make this revisable and end exploration-only requests without product edits. It is not a compulsory all-catalog tour for narrow tasks.
- **Human direction:** the existing consequential-question policy retains supplied answers, detailed briefs, explicit delegation and quick provisional drafts. Reference lines 53–61 allow a person to reject the framing and change the search rather than merely choose a preselected style.
- **Evidence scope:** entrypoint lines 38–42 distinguish viewed visuals, documented sequences and tested flows. Reference lines 65–69 preserve historical/access limits and forbid alternate-route retries after policy denial. A card description is not treated as evidence that the current agent viewed the source.
- **Application:** entrypoint lines 50–52 connects chosen resources to concrete flow, visual, content, implementation or verification decisions. Citation or file opening alone is explicitly insufficient.
- **Third-party authority:** entrypoint line 44 and reference line 69 treat upstream skills as selected source material. They do not authorize installs, scripts, copying, publication or new approval loops.
- **Portability and progressive loading:** all operational read paths are inside the skill; external references are sources rather than mandatory repository-local dependencies. Optional Python tooling derives its root from its installed location, uses the standard library and leaves direct file reading available. No database/server or embedding service is required.
- **Maintenance:** current evidence/maintenance guidance distinguishes card authority from generated views, identities/versions, editorial status, availability, evidence mode and freshness. It allows review, narrowing and retirement; a timestamp alone is not called revalidation.
- **Metadata:** the description and default prompt now route design-reference research as well as implementation. They do not force questioning for every request or create a second competing catalog entrypoint.

## Limits

This review did not inspect every card's underlying source or attest final coverage. Curation was still in progress, so a snapshot count is not a release verdict. It did not test external discovery, real-human usefulness, selected-resource fidelity, natural skill activation, browser authorization or final artifact behavior. Those require the separate frozen evaluation and final integrity checks.
