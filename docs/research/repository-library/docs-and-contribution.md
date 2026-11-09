# Documentation, contribution and evidence lane

Inspected: 2026-11-07. Delivered **12 cards**: three repository cases, six guides and three studies. The cards contain 32 distinct source locators: 19 pinned repository artifacts, ten official/framework/community guide pages and three original-paper URLs. These counts are resources and reading locations, not independent experimental confirmations. Two study cards received fresh substantive methods/results/limitations inspection; the coverage study preserves explicitly attributed earlier method inspection and a failed fresh follow-up.

The authoritative source links, section locators, revision and evidence scope are in each card's JSON frontmatter. All annotations are original. No upstream code, installer, generator, test, publication workflow or site preview was executed. Source/configuration establishes declared mechanics; it does not establish working commands, live enforcement or delivered releases.

## Pinned documentation repositories

| Card | Revision and freshly followed path | Consequential distinction |
| --- | --- | --- |
| [MDN content](../../../skills/repository-quality/library/entries/docs-mdn-content-contracts.md) | `288e644117c29285df2acf37a2ac97f57546a146`: CONTRIBUTING → package scripts → front-matter schema/validator; document move guidance → move-link repair script and redirect-check workflow. Six artifacts. | Metadata, source-link repair and redirect validity have separate owners/checks. Required-workflow comments are not evidence of live protection. Rari/Fred command routing shows why the entry guide must be followed into implementation. |
| [Rust book](../../../skills/repository-quality/library/entries/docs-rust-book-source-listings.md) | `2771df165f092a4fbb9f46b5b2e7450f19010adb`: README/CONTRIBUTING → chapter 12 includes → listing source → book config/preprocessors → CI, standalone support-crate manifest and reference checker. Eight artifacts. | Prose, executable included listings, terminal-output snapshots, print snapshots and published release trains are different authorities. The broad src-edit instruction does not justify ignoring a chapter's actual include path. |
| [Astro docs](../../../skills/repository-quality/library/entries/docs-astro-localized-contracts.md) | `c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4`: contribution entry/i18n/generated-page and maintainer sections → package scripts → collection schema → slug checker → separate CI jobs. Five artifacts. | The guide says .md in one entry section while implementation handles Markdown and MDX. Matching translated slugs is not translation correctness. Some build collections fetch external data; a local content tree is not the entire build environment. |

Revision resolution used the public GitHub connector's `/commits/main` response, followed by file fetches at that SHA. Root metadata was discovery only; stars were not used as a selection or quality criterion. Additional entry guidance was read to orient the path but not counted as separate evidence when duplicated inside another source.

## Primary guidance

| Card | Fresh inspection and useful transfer | Deliberate boundary |
| --- | --- | --- |
| [Diataxis](../../../skills/repository-quality/library/entries/docs-diataxis-reader-needs.md) | How-to-use/process plus compass: diagnose a reader need and improve a real page iteratively. | Explicitly discourages empty four-section scaffolds; conceptual framework, not an effectiveness experiment. |
| [Google review](../../../skills/repository-quality/library/entries/docs-google-change-review.md) | Looking-for plus standard: design/functionality, meaningful assertions, affected docs, code-health progress and optional polish. | Local engineering culture does not impose its approval or style regime on every project. |
| [GitHub CODEOWNERS](../../../skills/repository-quality/library/entries/docs-github-codeowners.md) | Location/base branch, pattern precedence, access, multiple owners and rule enforcement. | Committed map is routing evidence; hosted rule/permission state must be inspected separately before claiming enforcement. |
| [Contribution entry](../../../skills/repository-quality/library/entries/docs-github-contribution-entry.md) | Contributor-guideline surfaces/precedence and default community files. | Inherited files do not appear in clones/packages; license is not inheritable as a default. Filename absence alone is not missing-guidance proof. |
| [Rust API docs](../../../skills/repository-quality/library/entries/docs-rust-api-contracts.md) | Examples, Errors/Panics/Safety, meaningful links and release notes. | Reasoned example scope; no mechanical example duplication, no current Cargo-metadata specification claim. |
| [Docs as code](../../../skills/repository-quality/library/entries/docs-docs-as-code.md) | Write the Docs overview plus beginner audience/entry guide. | Shared tools do not demonstrate technical truth, writing quality or writer inclusion. Linked talks, books and tools were not inspected. |

## Original empirical evidence

- [Sillito, Murphy and De Volder, FSE 2006](../../../skills/repository-quality/library/entries/docs-study-change-questions.md): freshly read primary PDF §3.1–3.2 setup, §4–5 question/answer categories and §7.1–7.2 limitations. Nine newcomers worked in pairs on assigned Java tasks; sixteen industrial programmers used familiar code/tools and selected involved tasks. Qualitative question relationships justify probing a change path. They do not rank questions, establish an ideal tree or demonstrate task-completion gains.
- [Sadowski et al., ICSE-SEIP 2018](../../../skills/repository-quality/library/entries/docs-study-google-review.md): freshly read primary PDF §3.2–3.4 setting/methods/threats, §5 review mechanism, §7 small-change interpretation/analyzer feedback. Interviews, survey and filtered logs address different questions. Self-selection, company context and heuristics remain explicit. Reviewer count or latency is not a universal target; association is not an intervention result.
- [Inozemtseva and Holmes, ICSE 2014](../../../skills/repository-quality/library/entries/docs-study-coverage-limits.md): retain substantive methods/results evidence from the existing repositories dossier REP-24, including suite-size control, Java-system sampling and mutation proxy limitations. This lane retrieved the opening pages but repeated targeted method/threat reads timed out. The card is historical, openly distinguishes retained versus fresh inspection, and does not assert independent full-paper revalidation. It supports separating coverage from effectiveness, not dropping a project's existing gate.

## Search boundary and access gaps

The lane deliberately sampled documentation repositories with three different authority/publication shapes and followed their maintenance paths, rather than compiling popular README layouts. Guide discovery used directly relevant primary sites and the prior dossier as leads. Empirical discovery followed original author/institution PDFs. This is not a census of docs frameworks, hosting providers, contributor cultures or current research.

No failure occurred for the pinned source files ultimately cited. Initial large batched outputs were narrowed to relevant source sections so important content was inspected rather than inferred from truncated previews. The coverage PDF's fresh method follow-up repeatedly timed out; that gap remains in the card. No inaccessible abstract was promoted into a newly inspected full study. No live branch protection, CI run or actual publication was assessed.

Useful uncovered regions include non-GitHub contribution routing, accessibility/language research about documentation contributor tools, empirical onboarding interventions, and current outcomes from generated-reference maintenance. These remain future investigations, not claimed coverage.

## Local consistency check

All twelve cards parsed and satisfied the owning catalog helper's structural validation at completion. This checks format, source fields and sections; it does not independently prove each underlying claim. Related-resource edges were intentionally left empty for root-level cross-lane reconciliation.
