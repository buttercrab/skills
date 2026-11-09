# Repository-quality library: research and coverage

Date: 2026-11-07. First edition. Deliverable: the reusable [repository-quality skill](../../../skills/repository-quality/SKILL.md) and [annotated library](../../../skills/repository-quality/library/index.md), not changes to the repositories used as evidence. Start with [reading paths by maintenance problem](../../../skills/repository-quality/library/PATHS.md) when a whole index is too broad.

## Collection and evidence

| Resource role | Cards | Inspected contribution |
| --- | ---: | --- |
| Repository cases | 25 | Concrete source/manifests/tests/docs/build or release paths, with pinned revisions and contextual limits. |
| Guides | 17 | Reader/contributor needs, review, API documentation, language packaging/workspaces, generation, reproducibility and release tradeoffs. |
| Studies | 3 | Program-comprehension questions, review practice and coverage limitations, with methods/populations and transfer boundaries. |
| Tools/comparisons | 2 | Scorecard diagnostic limits and release-planning mechanisms, not mandated services. |
| Standard | 1 | SLSA provenance and verification scope at the inspected version. |

Total: **48 curated cards**, 182 selected source links / 179 distinct URLs, 97 related-resource edges and approximately 13,400 original body words. [Exact coverage fields](coverage.json) are machine-readable. These are reference resources/source locations, not 48 independent studies, 179 independent confirmations, or an exhaustive census.

All entries link to public sources. Access gaps and historical versions remain in their annotations; public availability does not mean every follow-up fetch succeeded. All cards use source-inspected evidence; three also carry empirical evidence and one conceptual evidence. Two studies received fresh substantive method/result/limitation inspection; the coverage study openly retains earlier inspection and records failed fresh method retrieval. No upstream repository, build, generator, test, package install, contribution action or release was executed for curation. A configured command establishes intended mechanics, not a successful run.

## How the research was conducted

Four parallel primary-source lanes sampled contrasts rather than star rankings. Small/public-library/CLI cases span JavaScript/TypeScript, Python, Rust and Go; large/native/compiler/framework cases add C/C++, Tcl and generated/compiler artifacts. Three docs repositories expose content, localization, included code and publishing boundaries. Guides/standards/studies add decision criteria and counterevidence.

Existing deep-research dossiers supplied leads. Repository cases were followed again at exact inspected snapshots, through substantive entry/contribution, source/manifest/generator and test/docs/configuration/distribution boundaries. The older coverage study's retained evidence is attributed rather than relabeled as fresh full-paper inspection. Whole source files and upstream assets are not redistributed; cards contain original annotations and precise links/sections.

| Lane | Reading inventory and material findings |
| --- | --- |
| [Small/library/CLI cases](small-repositories.md) | 12 cases / 70 selected pinned file sources. Flat exports versus packaging, default versus stress/optional tests, parser versus binary tests, embedded assets, generated references and assertion façades. Lane prefixes are not universal size labels. |
| [Large/native/multi-package cases](large-repositories.md) | 10 cases / 44 selected pinned file/diff receipts. Bootstrap stages, generated authority, conditional renderer coverage, staging publication, workspace-specific test entry and linker registration. |
| [Documentation/contribution/research](docs-and-contribution.md) | 3 pinned docs repos, 6 primary guides and 3 studies; 32 selected locators. Reader journeys, review/configuration limits, source/include/translation boundaries and empirical methods. |
| [Verification/distribution/releases](verification-and-release.md) | 14 cards / 36 selected links. Language-specific artifact boundaries, optional workspace behavior, generation, reproducibility, provenance and release planning. Version/path changes are retained. |

The source inventories are purposive, not a measure of popularity, ecosystem prevalence or causality. No claim that these repositories are uniformly good follows from using one well-documented mechanism.

## Decisions supported by contrasts

- A small public library can have a complete maintenance surface without architectural layers. Compare [p-limit](../../../skills/repository-quality/library/entries/repo-small-p-limit.md) with [npm artifact guidance](../../../skills/repository-quality/library/entries/quality-npm-artifact-exports.md), not a folder-count score.
- Source authority, repository location and publication units can differ. [Kubernetes](../../../skills/repository-quality/library/entries/repo-large-kubernetes.md), [SQLite's mirror](../../../skills/repository-quality/library/entries/repo-large-sqlite.md), [uv](../../../skills/repository-quality/library/entries/repo-small-uv.md) and [generation guidance](../../../skills/repository-quality/library/entries/quality-generated-source-authority.md) expose distinct cases; none requires adopting their entire build/governance system.
- A source-tree pass can bypass distribution or an optional environment. [Python installed-artifact guidance](../../../skills/repository-quality/library/entries/quality-python-distribution-checks.md), [Django](../../../skills/repository-quality/library/entries/repo-large-django.md) and [Click](../../../skills/repository-quality/library/entries/repo-small-click.md) explain why verification scope matters.
- Documentation architecture should follow reader tasks and actual authority. [Diataxis](../../../skills/repository-quality/library/entries/docs-diataxis-reader-needs.md), [MDN](../../../skills/repository-quality/library/entries/docs-mdn-content-contracts.md), [Rust book](../../../skills/repository-quality/library/entries/docs-rust-book-source-listings.md) and [Astro](../../../skills/repository-quality/library/entries/docs-astro-localized-contracts.md) are contrasts, not a mandatory four-folder scaffold.
- [Coverage evidence](../../../skills/repository-quality/library/entries/docs-study-coverage-limits.md), [CODEOWNERS](../../../skills/repository-quality/library/entries/docs-github-codeowners.md), [Scorecard](../../../skills/repository-quality/library/entries/quality-scorecard-diagnostic-limits.md) and [SLSA](../../../skills/repository-quality/library/entries/quality-slsa-provenance-verification.md) answer different questions. A numeric signal, committed map or provenance record does not prove runtime correctness or effective hosted enforcement.

## Source sampling and corrections

Independent cross-lane reviewers inspected eight selected cards against their owning primary artifacts/sections; this is sampling, not a full truth audit of all 48 entries. The workflow/helper integration was reviewed separately.

| Review | Result |
| --- | --- |
| [Small cases](review-small.md) | All 11 cited pinned artifacts fetched. Added p-limit's Node20 scenario exclusion and corrected Click's temporary-directory plus absolute-path combination. Neither issue proves a failing runtime. |
| [Large cases](review-large.md) | Eight pinned Kubernetes/SQLite files checked; source/publication distinction supported. SQLite canonical Fossil reconciliation remains an explicit access/version limit. |
| [Documentation cases](review-docs.md) | Astro and GitHub ownership conclusions supported. Narrowed Markdown/MDX extension evidence to the actual slug checker, separately from the delegated docs loader. |
| [Verification/release cases](review-release.md) | SLSA current/retired version and verifier-scope caveats confirmed; Go workspace warning and committed-workspace exception retained. |
| [Workflow/tool integration](workflow-review.md) | No material target/scope/query contradiction found; corrected optional interaction-receipt schema documentation to match the helper. |

Root normalized eight obvious task aliases in card metadata, preserving more specific distinctions. Related IDs and reading paths connect mechanisms across resource types/scale; they are reading aids, not independent corroboration. Exact literal/exact-facet semantics remain visible in [vocabulary](../../../skills/repository-quality/library/VOCABULARY.md) and [tooling notes](tooling.md).

## Limits and maintenance queue

This edition is strongest on GitHub-hosted libraries/CLIs/frameworks/native projects and language packaging. It is weaker on self-hosted/non-GitHub contribution workflows, private enterprise repository constraints, research/data repositories, embedded firmware, JVM/.NET/Ruby/PHP/Swift ecosystems, and measured outcomes of onboarding interventions. No public metadata supports conclusions about private branch rules, actual contributor capacity or shipped artifact quality here.

Further useful work: inspect contrasting application/data/firmware paths; add non-GitHub/canonical-authority cases; refresh standards/tool versions when relevant; investigate real task completion under repository guidance. Promote a new resource only after inspecting the claimed mechanism. Preserve inaccessible or historical evidence limits. No recurring automation or global installation is implied.

The [assessment evaluation](../../evaluations/repository-library/results.md) tests the first package on five fictional snapshots. It is separate from primary-source research and tooling validation, and cannot establish general effectiveness or exhaustive recall. Examples remain read-only; Taster work was not resumed.
