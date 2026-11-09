# Repository library tooling

Date: 2026-11-07. Implemented by adapting the portable design catalog helper into a self-contained repository-quality package. The design helper/package was not edited. Canonical cards are Markdown with strict JSON frontmatter; root will generate final indexes after the curation lanes settle.

## Interface and guarantees

`skills/repository-quality/scripts/catalog.py` supports `build`, `validate`, `list`, `find`, `facets`, and `show`. Python standard library only. `--root` precedes the subcommand; normal use discovers the package relative to the script. New kinds are repository/guide/standard/study/tool; exact facets are tasks/contexts/languages/scale, with `--task`, `--context`, `--language` and `--scale` flags.

The helper validates required metadata, IDs/filenames, source/evidence declarations, nonempty body sections, related IDs and local links. Repository cases additionally require a substantive `Change path` section; ordinary `source-inspected` cases do not imply or require an executed-flow receipt. Optional visual/documented-flow/interaction modes retain their explicit receipt obligations; do not add such modes casually.

Generated JSON and Markdown views are deterministic; each compact record includes the canonical card's SHA-256. Validation detects both metadata and annotation drift. Symlink/path containment guards apply to canonical cards, internal links and both generated outputs before reading/writing. Duplicate JSON keys, NaN/infinities, embedded URL credentials and unsupported file URL links are rejected. These structural checks cannot prove the annotation true or its cited command executed.

Search uses literal substrings, all text terms AND; repeated facet values AND; kind/status/availability alternatives OR within their respective filters. Matched fields are exposed and IDs remain deterministic, without similarity/popularity/quality scoring. `facets` exposes actual vocabulary. See portable `library/VOCABULARY.md`; it intentionally does not claim the suggested editorial terms exhaust the final cards.

## Validation performed

`python3 -B -m unittest discover -s tests -p test_repository_library.py`: **22 tests passed** (0.246s on the initial successful run). Tests use temporary synthetic card packages, not assumptions about final curator counts. They cover deterministic generation and hash/drift detection, source/evidence modes, relations, malformed metadata, strict JSON, source URL safety, identity, local links/symlinks, generated-output containment in build and check modes, source/evidence search receipts, AND/OR filtering, exact language/scale CLI filters, repository-only Change path requirements, facet discovery and relocated/no-dependency operation. The final rename of one descriptive test method did not alter its behavior.

No final indexes were built while curators wrote cards. No upstream repository, source script, build, test or release command was executed by the helper. No third-party dependency was installed for the tool or tests.
