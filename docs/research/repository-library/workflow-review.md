# Repository-quality workflow integration review

Date: 2026-11-07. Read-only review of `SKILL.md`, all five `references/*.md` files, `library/FORMAT.md`, `library/VOCABULARY.md` and the catalog interface/validation code. The reviewer authored the helper but not the operating workflow or curators' source annotations. Assessment fixture prompts, keys and cases were not read. No active package files were edited by this review; the coordinator owns reconciliations.

## Actionable finding and reconciliation

**Receipt schema documentation differed from the executable contract — resolved.** The final receipt paragraph in `library/FORMAT.md` initially described interaction receipt fields as `url`, `locator`, `actions`, `result`, `method`, whereas `scripts/catalog.py` validates `url`, `actions`, `observed`, `method`. In addition, catalog.py's evidence-mode branch requires a `flow_evidence` sequence receipt whenever `interaction-tested` is declared; the format initially documented this requirement only for `documented-flow`. A curator following the initial prose could therefore produce an interaction-tested card rejected by the helper.

The coordinator changed the format paragraph. A follow-up source read confirmed it now states `url`, `actions`, `observed`, `method` and explicitly requires `flow_evidence` as well for `interaction-tested`. This agrees with catalog.py's `parse_card` evidence branches (lines 182–187 at inspection). Source-inspected repository/configuration tracing still requires no executed-flow claim or receipt; its nonempty `Change path` body remains the applicable repository-case requirement.

No other actionable integration contradiction was found in the inspected material.

## Other checked boundaries

- **Scope:** the entrypoint names assessment, plan, implementation and reusable skill/library as separate deliverables. Trial findings return to the parent skill; assessment is not silent permission to restructure, publish or alter licensing/access. Existing authorization is preserved rather than adding a recurring approval sequence.
- **Questions:** the entrypoint and questions reference ask for consequential unknown intent after discovering technical facts, preserve delegation/detailed briefs and retire superseded questions. There is no required question count, universal interview or arbitrary quality score.
- **Reference selection:** comparisons use transferable mechanisms and meaningful contextual contrasts, with a small/no-change alternative. The library is not a demand to imitate famous root trees or load all cards.
- **Queries:** all documented examples use actual helper subcommands/flags. `show RESOURCE_ID` is explicitly a placeholder to replace, not an underscored valid ID. Whitespace-separated literal terms AND across fields; repeated task/context/language/scale values AND; repeated kind/status/availability alternatives OR. Vocabulary correctly notes that `language-agnostic` is an exact explicit label, not an automatic Python-match wildcard.
- **Evidence layers:** source/configuration inspection, configured jobs, executed checks, packaged contents, consumer exercises and observed release are separately scoped. Unknown permissions or uninspected artifacts are not automatically defects. Catalog operations perform local annotation search/validation, not upstream execution.
- **Proportional verification:** installed-artifact checks depend on actual consumer distribution, release/security mechanisms remain conditional, and blocked checks are not relabeled passes. The guidance does not force a monorepo, four documentation directories, numeric coverage gate or release platform on a small internal script.
- **Portability:** active references point within the package or to explicit public sources. Normal helper use derives its root from the script; explicit `--root` precedes the subcommand. The optional helper has no dependency on the repository research tree.

## Validation limits

This is an instruction/interface consistency review, not behavioral effectiveness evidence or a source audit of all curator cards. No repository build, package install, upstream command, release or live protection was exercised. The existing 22 helper tests were not rerun for the documentation-only correction because no new executable concern required it. The coordinator will build final indexes and validate the completed corpus after reconciliation.
