# Catalog tooling implementation

Implemented 2026-11-07. Scope: local catalog parsing, integrity, generated views, and transparent retrieval. This tooling validates metadata declarations and portable read paths; it does not prove source truth, visual inspection, current web availability, design quality, or skill efficacy.

## Entry authoring and views

`skills/design-with-intent/library/entries/*.md` are authoritative cards. Their frontmatter is strict JSON between `---` lines. Duplicate JSON keys are rejected rather than overwritten. The developer and runtime helper use Python's standard library only; no package installation, network, database or server is required.

The builder produces `library/index.md` (human browse by resource kind with applicability, source and evidence/access) and `library/index.json` (compact agent metadata, relative card paths and full-card SHA256). Full annotations remain in cards. A changed annotation, metadata field or generated output causes drift validation to fail. The generated views contain no build timestamp, so identical inputs produce identical output.

Historical evidence is valid when accurately classified. Editorial status, access availability, evidence modes and freshness are independent. A discovery-only or partial-only record cannot be promoted to curated. Visual/flow/interaction modes require their respective receipt fields, but those declarations still need editorial source review.

## Commands

From the package root:

```sh
python3 scripts/catalog.py build
python3 scripts/catalog.py validate
python3 scripts/catalog.py list --kind example --status curated
python3 scripts/catalog.py facets --status curated
python3 scripts/catalog.py find "correction" --platform web
python3 scripts/catalog.py find "community" --json
python3 scripts/catalog.py show RESOURCE-ID
```

From another directory, the script derives its package root from its own path. An explicit override goes before the subcommand:

```sh
python3 /path/to/package/scripts/catalog.py --root /path/to/copied-package validate
```

`build` validates all cards/relations and writes the two derived views. `validate` performs the same integrity checks and checks that views are present/current. `list`, `find` and `facets` read current canonical cards, not an independently editable cache. `facets` summarizes actual filter labels and occurrence counts, optionally within filters, so readers need not guess vocabulary. Counts are catalog occurrences, not evidence strength. `show` accepts an exact resource ID, never a file path.

## Retrieval semantics

Find terms are whitespace-separated, case-insensitive literal substrings; **all terms must occur** somewhere in the record's identity, summary, facets, status/access, source metadata, evidence or annotation. They need not all occur in one field. Results expose which fields matched each term, preserving deterministic ID order. There is no popularity or quality score, synonym expansion, semantic model, or claim of relevance beyond these literal matches. Broaden/refine vocabulary and inspect candidate cards.

Different supplied filters are combined with AND. Repeated facet filters require every requested facet value. Repeated `--kind`, `--status` and `--availability` values are alternatives within that field. For example, `--task compare --task recover` requires both tasks; `--kind example --kind system` permits either kind. Defaults include all editorial/access states, which are displayed explicitly; use `--status curated` for an inspected recommendation pool. A candidate match is a discovery lead, not a recommendation.

## Integrity and portability

Validation checks required metadata/types, ID/filename agreement, evidence mode/date/scope, conditional receipts, body sections, related-ID existence, no self-relations, internal Markdown resource links, generated drift, and package containment. Explicit `local:` source identifiers require `availability: local-only` and are never resolved or executed. Network source URLs reject embedded credentials and control characters. A source URL is syntactically validated, not fetched.

Card symlinks and generated output symlinks are rejected; internal links must resolve inside the package. Known derived index links may bootstrap during a clean build. A copied package works without the original research directory. Unknown optional metadata is preserved in cards but not automatically exposed in the compact view; deliberate future schema extensions can add useful fields.

## Tests run

`python3 -B -m unittest discover -s tests -p test_design_library.py`: **18 passed** at implementation time. Tests cover malformed/duplicate/nonfinite JSON and unsupported file-URL links, status/evidence promotion, receipt requirements, related IDs, filename identity, path escape and symlink destinations, local-only source labeling, credential/control-character source URLs, deterministic drift including annotation hashes, literal/filter match semantics and match-field receipts, clean-view bootstrapping, relocated-package execution and invalid show paths.

A live calibration build parsed the first available cards successfully. Final catalog build/validation must be repeated after curation stabilizes. Existing installer/package tests remain the coordinator's final integration checks; no global installation or external-source execution was performed in this lane.
