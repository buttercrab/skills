# Verification and release reference lane

Research date: 2026-11-07. Read-only primary-source inspection. Delivered **14 cards**: 11 guides, two tools/comparisons and one standard. Cards contain 36 source links across 33 distinct selected URLs and approximately 3,704 original body words. These are overlapping source bundles, not independent confirmations or a census of the ecosystem.

## Selection and scope

This lane asks how a repository exposes the boundary between editing sources, selecting checks, creating an artifact, coordinating its release and confirming what consumers receive. It deliberately contrasts small and multi-package projects rather than treating a public monorepo's release machinery as a universal quality bar.

All selected primary documents/configuration/implementation sections were read through web or GitHub tools. No upstream repository was cloned, no source/test/build/generation/package command was run, and no package, credential, scan, remote PR, tag, release or protection setting was created. A documented command or configured mechanism is not an executed result. No old dossier content was relabeled as fresh inspection.

## Delivered cards and decision paths

| Card | Decision it supports | Concrete example path |
| --- | --- | --- |
| `quality-python-import-layout` | Src versus flat layout by actual import boundary | Resource declaration → package discovery → installed import/resource lookup; retain fast local feedback. |
| `quality-python-build-metadata` | Build requirements versus installed requirements versus developer tools | Script declaration → callable → runtime dependencies → installed invocation and README. |
| `quality-python-distribution-checks` | Editable tests versus downstream artifact checks | Source test → wheel/sdist selection → isolated command and packaged-template check. |
| `quality-cargo-workspace-selection` | Root defaults versus intended package/feature scope | Member manifest → root inheritance/default-members → focused crate and wider consumer checks. |
| `quality-cargo-package-boundary` | Checkout build versus distributed crate | Authoritative/generated input → archive inclusion/normalized metadata → extracted package build → separate upload reconciliation. |
| `quality-go-module-workspace-boundaries` | Local workspace convenience versus independently consumed modules | Local replacement/workspace test → module-mode declared dependencies → proper independent release boundary. |
| `quality-npm-workspace-scope` | Workspace linking and script-selection limits | Root membership/order → member script → local consumer versus installed package. |
| `quality-npm-artifact-exports` | Tarball contents versus resolvable public API | Source/build output → `files`/ignore rules → exports targets → real consumer import/type check. |
| `quality-generated-source-authority` | Input, tool and output authority | Human input → versioned generator → generated output → focused behavior/drift/publication checks. |
| `quality-reproducible-build-evidence` | Explicit artifact reproducibility envelope | Revision/environment/instructions → specified output → controlled variations → byte comparison. |
| `quality-slsa-provenance-verification` | Authentic build provenance under a consumer policy | Artifact digest → trusted builder/source/parameters → actual verification outcome. |
| `quality-scorecard-diagnostic-limits` | Individual heuristics and access gaps | Score/check input → source/configuration inspection → observed policy or explicit unknown. |
| `quality-versioning-and-human-release-notes` | Compatibility contract and human upgrade communication | Supported invocation/API → intended change/deprecation → checks → user-facing note. |
| `quality-release-planning-workflows` | Change files versus commit-derived release proposals | Human release intent → proposed package/version/notes → review → artifact validation → distinct publication step. |

The example checks above are proposed adaptations, not performed checks.

## Material source findings and conflicts

**Python:** PyPA's layout guide explains the extra installation step for src layout and the root-import shadowing risk. pytest supports both external and included test layouts; therefore neither one test folder nor a source-directory name is universally decisive. PEP 660 explains that editable metadata should resemble regular installation but allows backend differences and identifies changes that require reinstallation. PyPA's packaging flow distinguishes source trees, sdists and wheels. The cards keep developer feedback and distributed-artifact evidence separate.

**Cargo:** Current Cargo docs distinguish workspace/default-member selection from full coverage. Package creation normalizes the manifest, resolves the distributed boundary and verifies an extracted build unless that step is disabled. The VCS metadata file explicitly provides only a best-effort snapshot. Publishing may upload successfully before its later index polling times out; a timeout alone is not evidence that retrying upload is safe. No toolchain-version or runtime behavior was inferred from a README.

**Go:** Modules are independent version/distribution units; packages and repository directories are not automatically separate modules. The reference explicitly warns that committed `go.work` can override a developer's parent workspace or mask versions consumers use, then supplies an exception for modules intentionally developed together. The card preserves that exception instead of banning checked-in workspaces. The current command reference also states generation does not run automatically with build/test. Its viewed page identified go1.27.3 and displayed a not-latest warning; it was not called the latest available Go version.

**npm/Node:** Local workspace links and script selection/order do not establish independent package contents. `--if-present` may intentionally omit missing scripts. Packed-file inclusion and Node exports are different contracts; adding exports can block old subpaths. The npm pages inspected identify CLI 11.21.2 as Legacy, and the Node page identifies v26.13.0. These are recorded version scopes, not a claim that CLI 11 is the current universal recommendation.

**Reproducibility and provenance:** Bit-identical specified outputs, a repeatable environment, an attestation file and a verified source/build identity are separate properties. Reproducible Builds defines the artifact/environment envelope; SOURCE_DATE_EPOCH addresses one input class. SLSA Build verification requires expectations/trust as well as the artifact/statement relationship. These sources do not establish functionality or absence of vulnerabilities.

**SLSA freshness:** Initial v1.1 pages explicitly label themselves Retired and link v1.2. The guessed v1.2 `/levels` URL returned 404. Following the official v1.2 navigation reached `build-track-basics`; its approved page notes the Source Track reintroduction in v1.2. The curated card uses v1.2 Build Track/verification read paths, not the retired overview.

**Scorecard:** README at `b753b11c3523c5db8b4880c138858e7e7b8c614a` explicitly says heuristic checks have false positives and negatives and cautions about aggregate-score information loss. The check docs explain visibility differences for branch protection, including administrative and provider-specific unknowns. Those notes prevent interpreting unreadable controls or a filename-detection result as full assurance. No scan or live target protection query occurred.

**Release tools:** Release Please at `ea20bc261acd75149f0be90890bb9c90e681eea7` explicitly excludes package-manager publication. Selected `src/manifest.ts` methods distinguish building PR candidates, creating/updating PRs, building release candidates and creating GitHub releases; this was read, not executed. Changesets' pinned README at `2f6995d5bbd3b1572d7a6cd897d2229bfc1ce8c1` calls main v3 development, and `docs/intro-to-using-changesets.md` marks itself outdated. Following its link reached docs identifying v3.0.3 with footer commit 2f6995d. These labels are both preserved; neither independently establishes an npm publication. The linked current CLI documents version/publish separation, private-package accidental-publish risk and commands unavailable in older versions. Choosing a tool requires matching the actual installed version and release-intent workflow.

**SemVer/changelogs:** SemVer is about a declared public contract; a bump is not proof a change respects it. Keep a Changelog's guidance is a human communication convention. Its historical comments about GitHub UI were not promoted into current interface claims. Neither source mandates that every private script use SemVer or that every commit deserve a release note.

## Primary-source inventory

The exact URL, read locator and version for every selected source are embedded in the cards. Distinct selected reading regions:

- PyPA layout, writing-pyproject and packaging-flow guides; pytest integration test layouts/import modes; PEP 517 hook/build-environment sections and PEP 660 editable goals/metadata.
- Cargo workspaces, cargo-package and cargo-publish references, including selection, normalized archive and verification/upload boundaries.
- Go managing-source, module reference/workspaces, release workflow; current cmd/go generation documentation and 2014 Go generation account (historical motivation only).
- npm CLI 11 workspaces, package.json inclusion/exports and npm-pack; Node v26.13.0 package entry points.
- Reproducible Builds definitions and SOURCE_DATE_EPOCH; approved SLSA v1.2 Build Track Basics and verifying artifacts.
- Scorecard pinned README and check docs (especially Branch-Protection, CI-Tests, Token-Permissions and Signed-Releases).
- SemVer 2.0.0 and Keep a Changelog 1.1.0's human-oriented principles, Unreleased, deprecation and commit-log discussions.
- Release Please pinned README, manifest-releaser guide and selected manifest implementation methods; Changesets pinned README/outdated-intro notice and linked getting-started, versioning/publishing and CLI pages.

Metadata/identity reads of GitHub repo/default branches and commits were used to resolve paths and pin three repository source bundles. Their star counts or reported commit tests are not evidence used to rank repository quality. Full GitHub result bodies are not redistributed.

## Access gaps and retrieval corrections

- SLSA v1.2 `/levels`: ordinary 404; official navigation supplied the current read path. Retired v1.1 pages remain historical discovery evidence only.
- Direct guessed Changesets `/guide/adding-a-changeset` and `/reference/cli` routes were inaccessible through the web tool. Official getting-started links supplied `/guide/cli` and `/guide/versioning-and-publishing`; these were substantively read. No policy denial was bypassed.
- An initial web click addressed by URL rather than the returned reference identifier failed argument resolution; corrected to the observed reference/link ID.
- A lexical search for "committed" initially found no Go reference text; opening the actual Workspaces section exposed the explicit guidance. Search misses are not absence claims.
- GitHub branch search returned branch names without head SHAs; commit lookup resolved main to exact SHAs before source file inspection. No branch mutation occurred.

## Coverage boundary

This lane does not audit actual release credentials, package-manager availability, downstream installations, branch rules or production systems. It does not cover a full native-wheel matrix, JVM/Maven or .NET packaging, container image publication, database migration deployment or every package-manager orchestration tool. It supplies carefully scoped mechanisms for assessment and future research rather than mandatory release ceremony. Cross-family relationships are left for coordinator reconciliation.
