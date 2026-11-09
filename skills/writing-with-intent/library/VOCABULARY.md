# Writing facets and local discovery

Use labels actually present in the cards. These editorial hints are not a closed writing taxonomy, hidden similarity system, quality score or human/AI authorship test.

```sh
python3 scripts/catalog.py facets --status curated
python3 scripts/catalog.py facets --kind example --json
python3 scripts/catalog.py find "reader" --status curated
python3 scripts/catalog.py list --genre explanation --status curated
python3 scripts/catalog.py list --language korean --status curated
python3 scripts/catalog.py show exact-card-id
```

Run from this skill's directory or use the helper's absolute path. An explicit `--root /path/to/relocated-skill` precedes the subcommand. The helper uses only Python's standard library. Reading/searching does not call a network service, install dependencies, run upstream code or publish anything.

## Search semantics

- Text terms are whitespace-separated, case-insensitive literal substrings across metadata, source locators and original body annotations. Every term must match, possibly in different fields. A word in a mismatch paragraph is a discovery hit, not a recommendation. Results identify matched fields.
- `--task`, `--genre`, `--language` and `--context` use exact labels. Repeating a facet flag requires all supplied values. `--genre article --genre explanation` means both; a broad or language-neutral label does not automatically match a specific language.
- Repeated `--kind`, `--status` and `--availability` values are alternatives within that filter. Distinct filters combine with AND. Unless filtered, candidates and review-needed/retired records remain visible; use `--status curated` for ready annotations.
- Results retain deterministic ID ordering. There is no automatic style, author, popularity or quality ranking. No match means no card matched this literal query/filter combination, not that no useful reference exists. Inspect facets, try alternate vocabulary and browse neighboring roles.

## Editorial hints

| Facet | What it describes | Useful distinctions |
| --- | --- | --- |
| `tasks` | Editorial decision or action | Frame, structure, explain, argue, report, revise, verify, preserve voice or evaluate. Preserve meaningful differences rather than merge every revision into “polish.” |
| `genres` | Forms where transfer may apply | Article, essay, explanation, tutorial, argument, reported feature, personal essay or research summary. An argument technique need not impose a thesis template on every genre. |
| `languages` | Language applicability actually supported | English, Korean or an explicit language-agnostic label where appropriate. A translation or English-only example does not establish equivalent effects in every language. |
| `contexts` | Readers, conditions or evidence needs | Newcomers/expert readers, author voice, source synthesis, multilingual work, uncertainty or technical explanation. These are context labels, not evidence of authorship or reader outcomes. |

Example cards require Craft trace and Revision implications. Those sections explain inspected craft and a proposed transfer; they do not prove the author's revision history or improved readership. Keep article analysis, conceptual advice, study results, local checker flags and human editorial decisions distinct.

Related-card IDs are reading paths, not independent corroboration or automatically governing instructions. Normalize only obvious aliases editorially, preserve stable IDs, and regenerate/check the views when canonical cards change.

First-edition metadata normalizes `en`/`ko` to `english`/`korean`, `novice-readers` to `beginner-readers`, and `nonexpert-readers` to `non-specialist-readers`. This is editorial metadata reconciliation, not runtime fuzzy matching or evidence that study populations are equivalent. Source-specific participants/readers and genre limits stay in each annotation. General readers and beginners are not automatically the same audience.
