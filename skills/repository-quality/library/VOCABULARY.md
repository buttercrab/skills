# Facets and local discovery

The catalog accepts explicit lowercase hyphenated labels; it does not normalize words, infer similarity or rank repository quality. Treat the vocabulary below as editorial guidance, not a closed set or a framework-selection rule. Use the labels present in the current cards:

```sh
python3 scripts/catalog.py facets --status curated
python3 scripts/catalog.py facets --kind repository --json
python3 scripts/catalog.py find "generated" --status curated
python3 scripts/catalog.py list --language python --scale single-package --status curated
python3 scripts/catalog.py show exact-card-id
```

Run these from the skill root, or use the script's absolute path. `--root /path/to/relocated-skill` precedes the subcommand when an explicit package root is needed. Python's standard library is sufficient; no service, package installation, repository checkout, network request or upstream command is used for catalog operations.

## Interpret results

- Text search splits the query on whitespace and matches case-insensitive literal substrings across metadata, source locators and original body annotations. **Every query term must match**, but terms may match different fields. A term in a mismatch paragraph is a discovery hit, not a recommendation. Results identify the matched fields.
- `--task`, `--context`, `--language` and `--scale` require exact labels. Repeating a facet flag requires **all** supplied values: `--language python --language rust` finds cards applicable to both languages, not a union. `language-agnostic` is an explicit label, not a wildcard that automatically matches Python.
- Repeated `--kind`, `--status` and `--availability` are alternatives within each filter. Different filters still combine with AND. For example, two kinds plus a language means either kind with that language.
- Results keep deterministic ID order rather than a popularity, quality or similarity score. All statuses are visible unless filtered; use `--status curated` for ready annotations and inspect candidates deliberately.
- A zero result means no card matched that literal query/filter combination. Inspect facets, try neighboring vocabulary or browse kinds before inferring a coverage gap. The catalog is not an internet census.

## Editorial hints

| Facet | What it describes | Useful distinctions |
| --- | --- | --- |
| `tasks` | Maintenance decision or action | Locate authoritative inputs, test a package, review a change, update generated reference, publish an artifact, onboard contributors. Prefer the same label for obvious verb/noun aliases. |
| `contexts` | Project/artifact/contribution situation | CLI, library, framework, monorepo, documentation repository, native build, multi-maintainer/community work. Several can apply; they are not mandatory architecture layers. |
| `languages` | Language relevance | Common labels include `python`, `javascript`, `typescript`, `rust`, `go`, `c`, `cpp`, `shell`, and `language-agnostic`. Read the actual card before assuming portability between ecosystems. |
| `scale` | Applicability of maintenance overhead | `small-project`, `single-package`, `multi-package`, `large-project`, `cross-scale`. These are overlapping contexts, not numerical maturity ratings or prescribed team-size thresholds. |

When normalizing labels, preserve a meaningful distinction rather than merging merely similar strings. Regenerate and validate the views after a canonical card changes. Keep repository/guide/study evidence and configured/executed/published states separate even when their discovery labels overlap.

## Editorial aliases in the first edition

The cards normalize `documentation` → `document`, `navigation`/`change-navigation` → `navigate`, `validation` → `verify`, `code-review` → `review`, `contribution`/`contribution-routing` → `contribute`, and `structure` → `organize`. These are canonical metadata edits, not runtime fuzzy matching. More specific distinctions such as test selection, generated authority and publication remain explicit. Use context to distinguish documentation navigation from source navigation. The `repo-small-` and `repo-large-` ID prefixes identify curation lanes; actual scale applicability is in each card and need not match the prefix.
