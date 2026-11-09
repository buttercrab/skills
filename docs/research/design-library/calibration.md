# Library calibration

Date: 2026-11-07. Implementation-stage development record, not an independent evaluation or completeness claim.

## Card contract checked before broad curation

Reviewed representative skill, tool, system, correction pattern, product workflow, actual visual example, conceptual foundation and normative-standard cards. The initial ten cards parsed under the standard-library tooling without a schema change. The cards preserve evidence mode, access and freshness separately.

Specific distinctions checked:

- Anthropic instruction inspection is not measured skill efficacy or a viewed generated interface.
- axe API documentation is not an executed accessibility scan.
- GOV.UK's correction sequence is documented; it is not automatically a tested downstream service.
- Figma's historical state-visibility account can inform repeated work without establishing current product behavior or a visual match.
- Duolingo/Finch visual cards identify the public marketing surface actually viewed, not unobserved app workflows.
- Mixed-initiative theory and WCAG conformance have different evidence roles.

The coordinator independently viewed Duolingo's public HTTPS welcome screen in native Chrome: character collage on white, rounded headline, green primary start action, outlined returning-user action. This corroborates that card's narrow composition observation only. No signup or lesson was entered. A later navigation was aborted before dispatch; no additional source observation is claimed from that coordinator browser session. Curators maintain their separate visual receipts.

## Development discovery walkthrough

With the initial growing collection, ran:

```sh
python3 skills/design-with-intent/scripts/catalog.py list --context learning
python3 skills/design-with-intent/scripts/catalog.py find correction
python3 skills/design-with-intent/scripts/catalog.py find state --kind example
```

The learning filter found the viewed Duolingo example; correction search exposed the review/correction pattern along with foundations and annotations that merely discuss correction; state-example search found Figma and Linear cases with different task structures. This demonstrates searchable distinctions, not automatic semantic relevance. Some terms appear in a mismatch paragraph or source locator, so matched-field receipts and deeper reading matter.

A zero result in this partial development collection would not establish absence. The expanded curation phase continues across resource kinds and contexts. The independent evaluation cases were authored without reading the target or catalog and are not used as card-writing answer keys.

## Packaging decision

Markdown cards use JSON frontmatter, a YAML-compatible subset, so the bundled builder/searcher requires only Python 3 standard library. The card is authoritative; generated Markdown/JSON views avoid manual duplication. Existing package checks already use YAML for skill metadata, but ordinary library reading/filtering introduces no dependency installation.

Related IDs can be completed after parallel curation. Local-only references use explicit `local:` identifiers and access labels rather than required personal paths. Public source links form the portable core. No third-party skill, script, asset or tool was installed or executed to create these cards.
