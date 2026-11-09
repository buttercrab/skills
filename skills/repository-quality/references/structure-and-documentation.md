# Structure and documentation as maintenance paths

Use this for organization, ownership, generated authority and reader navigation. Apply language/tool semantics from inspected primary material; the examples below are decision frames, not a universal scaffold.

## Different boundaries answer different questions

| Boundary | Question to resolve | Common mistaken inference |
| --- | --- | --- |
| Repository/directory | Where are related artifacts discovered and reviewed? | One folder must equal one deployable service or architectural layer. |
| Dependency/import | What may use what, and which public contract is stable? | Moving files alone fixes coupling. |
| Build/generation | What is edited and what is derived? | A generated file's convenient location makes it authoritative. |
| Ownership/review | Who understands and reviews the affected change? | An ownership file proves enforced review or maintenance activity. |
| Publication | What is versioned, packaged and consumed together? | A monorepo necessarily has one version, or separate packages require separate repositories. |

Inspect the actual manifests, workspace links, generator inputs and CI/release configuration. Preserve differences between documented intentions and configured behavior. A source tree can contain authoritative copies that are later split or generated into distributed artifacts; importing or editing the distributed copy can send work to the wrong place.

Before a move, identify consumers, import/export paths, tests, generated references, package include rules, documentation links and release tooling that depend on the current location. Prefer a small repair when the problem is a stale command or missing navigation link. Make a broader move only when its maintenance benefit justifies migration and review cost.

## Choose layout for actual semantics

Flat and source-subdirectory layouts can both be deliberate. Inspect how the language discovers imports, tests and packages, whether checkout paths can shadow the installed artifact, and what files enter distribution. A tiny exported implementation does not need service/repository layers for visual symmetry. A framework with independently reviewed backends may need stronger ownership and test-routing boundaries.

A workspace can simplify joint development while hiding missing dependency/version declarations that an external consumer will encounter. Compare the workspace build with the actual package contract when publication matters. Do not recommend independent versioning merely because subdirectories exist, or one version merely because tooling supports it.

Tool, dependency and architecture changes are separate decisions. Keep project conventions unless a demonstrated problem or explicit user direction warrants changing them. Detailed system architecture and production infrastructure are separate deliverables, not automatic extensions of repository assessment.

## Document the reader's next task

Identify the reader and occasion: try the project, complete a specific task, look up a precise contract, understand a design choice, contribute a change, or prepare a release. Documentation frameworks can expose missing reader support without requiring a fixed physical four-folder layout or every document type in every project.

Check the journey across links and commands. A README's installation example should match the supported artifact. A contribution entry should lead to the actual prerequisites and focused checks. Reference information should identify its owning source or generator when generated. An explanation should clarify a consequential tradeoff rather than repeat a directory listing.

Distinguish source authority from navigation. Linking a canonical guide from the README is often better than copying prerequisites into several surfaces. Generated reference and authored tutorials can coexist; determine which is derived, when regeneration occurs and whether validation checks checked-in freshness, build-time generation or published output. Those checks are not interchangeable.

## Proportional contribution conventions

Find the actual contribution route, ownership and support channel before judging whether another file is needed. A small team can use concise inline guidance; a public project with distinct contributor groups may need separate paths. Samples from established projects describe their own norms, not binding requirements for another repository.

Read the actual behavior of automated ownership/review tooling. Do not infer private settings from public files or mistake a file's absence for proof of no process. License declarations, contribution agreements and signing expectations are legal/governance evidence; an ordinary quality improvement does not authorize changing them.

When recommendations depend on current source semantics, open the matching [library cards](../library/index.md) and their precise upstream paths instead of applying a generic “good repository” template.
