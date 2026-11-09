# Architecture facets and local discovery

Use the labels actually present in the current cards. Editorial suggestions below are not a closed taxonomy, automatic matching rule or architecture quality score.

```sh
python3 scripts/catalog.py facets --status curated
python3 scripts/catalog.py facets --kind system --json
python3 scripts/catalog.py find "retry" --status curated
python3 scripts/catalog.py list --quality durability --status curated
python3 scripts/catalog.py show exact-card-id
```

Run from the skill root, use an absolute script path, or put `--root /path/to/relocated-skill` before the subcommand. Python standard library only; normal catalog reading/search does not use a service, upstream executable, installation, database or network request.

## Search and filter semantics

- Text search splits on whitespace and matches case-insensitive literal substrings in metadata, source locators and body annotations. **Every term must match**; terms can match different fields. A hit in a mismatch paragraph is a discovery lead, not a recommendation. Results identify matched fields.
- `--task`, `--context`, `--quality` and `--scale` use exact labels. Repeating a facet requires **all** values. For example, `--quality durability --quality consistency` selects cards annotated with both, not either. A broad label such as `cross-scale` is not a wildcard.
- Repeated `--kind`, `--status` and `--availability` permit alternatives within that filter. Different filters combine with AND. A `system` or `pattern` filter plus a quality still requires that quality.
- Results use deterministic ID order, not popularity, semantic affinity, architectural goodness or evidence strength. All statuses are visible unless filtered; select `--status curated` for ready annotations and inspect candidates deliberately.
- No match means no card matched this literal query/filter combination. Try alternate words, inspect facets and browse related roles before asserting a coverage gap. The library is not an internet census.

## Editorial hints

| Facet | What it describes | Useful distinctions |
| --- | --- | --- |
| `tasks` | Decision or action the resource can help with | Decompose, trace, compare, document, diagram, migrate, verify, model failure. Preserve meaningful distinctions and normalize only obvious aliases. |
| `contexts` | Relevant system/problem assumptions | Embedded storage, control loops, replicated state, interactive tooling, asynchronous processing, deployment or migration. A project can span several contexts. |
| `qualities` | Constraints and tradeoffs discussed | Consistency, durability, availability, latency, operability, evolvability and security. A quality label does not prove a guarantee, metric value or universal priority. |
| `scale` | Applicable operational/process setting | Single process, one deployment, several deployments, distributed systems and cross-scale reasoning. These are overlapping contexts, not workload thresholds or maturity rankings. |

Cards of kind `system` include an Architecture trace and Diagram implications. `notation` cards include Diagram implications; the presence of either section records an annotation, not successful rendering or operational validation. Source reads, documented sequences, diagram viewing/rendering and runtime observations retain distinct evidence boundaries.

Related-card IDs are suggested reading paths, not corroboration or automatic activation of upstream instructions. Regenerate and validate indexes after canonical cards change; do not hand-edit a generated view.

The first edition editorially normalizes `comprehensibility` to `understandability`; this is a canonical annotation change, not runtime fuzzy matching. Other quality distinctions (including consistency, durability, availability, reliability, maintainability and evolvability) remain explicit. A related candidate such as the partial FLP lead is still a candidate, not ready evidence merely because a curated card links to it.
