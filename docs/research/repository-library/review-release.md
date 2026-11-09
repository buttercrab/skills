# Independent source sample: SLSA provenance and Go module/workspace cards

Review date: 2026-11-07. Scope: only `quality-slsa-provenance-verification.md` and `quality-go-module-workspace-boundaries.md`, compared with the precise primary-source sections they cite. No assessment fixtures, card/example edits, installations, builds, generators, tests, artifact verification or upstream mutations were performed.

## Judgment

**No demonstrated material defect in either sampled card.** Both preserve the difference between documentation/configuration and actual execution. SLSA's track/version status and Go's workspace exception are supported by the current primary pages. This is a bounded source-attribution review, not certification of a release pipeline or a full library audit.

## SLSA v1.2 card

Inspected [Build: Track Basics](https://slsa.dev/spec/v1.2/build-track-basics), including its Approved status, level summary and L1–L3 requirements. The card accurately distinguishes provenance existence, platform-generated authenticated provenance and a hardened platform. Its summary is intentionally shorter than the full level requirements; no specific repository or builder is declared compliant.

Inspected [Build: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts), How to verify, Step 1 and Step 2, and Forming Expectations. The attribution is supported: the verifier relates the artifact digest to the statement, uses a configured trust root for builder identity/level, and checks expected source/build parameters. The page's normative strength is generally SHOULD for these recommendations; the card does not represent a universal MUST checklist. Its title is editorial guidance, not a quoted normative requirement.

The same page's trust assumption matters: verification cannot make an untrusted or compromised build platform trustworthy merely because an envelope has a signature. The card's emphasis on trusted identity and expectations is consistent with that boundary. The card also correctly avoids treating provenance as evidence of functional correctness or freedom from vulnerabilities.

Freshly checked the older [v1.1 levels](https://slsa.dev/spec/v1.1/levels) and [v1.1 artifact-verification](https://slsa.dev/spec/v1.1/verifying-artifacts) pages: both explicitly identify v1.2 as current and show Retired status. This supports the card's version/currentness caveat. The historical failed v1.2 `/levels` lookup was not repeated; its recorded failure should remain an access-attempt note, not be strengthened into a permanent nonexistence claim.

No correction required. If this annotation later grows into an executable compliance checklist, preserve the actual normative keywords, applicable track/level and trust assumptions instead of turning the short level descriptions into complete requirements.

## Go module/workspace card

Inspected [Managing module source](https://go.dev/doc/modules/managing-source), Choosing repository scope and its one-module/multiple-module subsections. It ties module boundaries to independent versioning and describes a single root module as a simpler option while allowing multiple modules. The card conveys that distinction without equating every directory or repository with a release unit.

Inspected [Go Modules Reference](https://go.dev/ref/mod#workspaces), Workspaces and go.work files. It describes joint main-module selection, GOWORK lookup including parent directories, the general caution about committing a workspace, the CI dependency-selection risk and the explicit committed-workspace exception. The card retains the exception rather than inventing a blanket ban. Its recommendation to distinguish local convenience from downstream module behavior is supported.

Inspected [Module release and versioning workflow](https://go.dev/doc/modules/release-workflow), the common workflow and Coding against an unpublished module. It describes local filesystem replacement before publication. The card correctly keeps a locally available unpublished API separate from a published version's availability.

No correction required. Optional implementation detail for a later task: the Modules Reference describes `GOWORK=off` as single-module mode and `go env GOWORK` as an observation of the selected workspace. Those commands were not run here and are not required additions to this conceptual card.

The Go references are live documentation, not pinned implementation revisions or a declared toolchain-specific compatibility result. The card already labels them accordingly; exact command behavior should be checked against the task's toolchain when executed.

## Evidence boundary

All five cited current source pages were accessible and substantive sections were read; the two historical SLSA pages were additionally checked for status. No relevant current-source access gap remains in this sample. No source code or actual build/provenance/module outcome was verified. There is no demonstrated reason from this sample to change either card or to infer an effectiveness advantage for the operating skill.
