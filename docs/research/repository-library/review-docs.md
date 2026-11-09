# Independent docs-card review

Date: 2026-11-07. Scope: `docs-astro-localized-contracts` and `docs-github-codeowners` only. Reviewer did not author these cards and did not inspect assessment fixtures. Read five exact Astro artifacts and current official GitHub feature documentation. No upstream scripts, builds, PRs, repository settings or translation/deployment workflows executed. Cards and example repositories were not edited.

## Judgment

The two cards' central conclusions are supported at their declared source-inspection scope. No material contradiction or false enforcement claim found. There is one optional precision improvement in the Astro description: the inspected slug checker explicitly matches `.md` and `.mdx`, while `content.config.ts` delegates content loading to Starlight's `docsLoader()`. The delegated loader implementation was not inspected in this review, so “actual collection and slug-check code handle both” is broader than the directly visible extension handling. Wording that attributes the extension glob specifically to the slug checker would reduce inference without changing the conclusion.

## Astro documentation contracts

All files read at `c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4`:

| Primary artifact | Supported claim / boundary |
| --- | --- |
| [CONTRIBUTING.md](https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/CONTRIBUTING.md), Types of Contributions / Internationalization / Pages generated from outside sources | Guide distinguishes direct typo/link fixes from larger issue/discussion proposals, describes English-only translation exceptions and routes generated-page edits through edit URLs/githubURL. These are documented workflow claims, not verified tracker behavior. |
| [package.json](https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/package.json), scripts | `check`, `docgen`, slug checking and link checking are distinct commands. Link checking first invokes a build. A root manifest's script existence does not establish every job ran successfully. |
| [src/content.config.ts](https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/src/content.config.ts), base/type-specific schemas and collections | Schema variants and optional githubURL are explicit; docs loading is delegated. Package/contributor collections use fetch-based loaders. Thus the checked-out content files alone do not pin all build-time external inputs. No fetched data was inspected. |
| [scripts/lint-slugcheck.mjs](https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/scripts/lint-slugcheck.mjs), file glob and English counterpart set | Glob explicitly includes Markdown and MDX, excludes 404.mdx, compares non-English paths against English paths and exits with failure for unmatched slugs. It does not compare translated meaning or ensure every English page has every translation. |
| [.github/workflows/ci.yml](https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/.github/workflows/ci.yml), astrocheck/eslint/slugcheck/linkcheck | Separate jobs invoke the corresponding scripts on configured events. This is configured validation, not evidence of live branch requirements, green runs or deployed page freshness. |

The contributor prose's `.md` instruction and its own later `.mdx` generated-page examples are a useful navigation warning. The card correctly advises checking actual configuration rather than treating one prose filename convention as exhaustive. The review did not follow nightly generation, translation tracker implementation, shared install action or Starlight loader source; no broader enforcement claim is supported.

## GitHub ownership mapping

Fresh official [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) sections read: Who can use, file location, forks/base branch, syntax, branch protection/rulesets. They support the card's distinctions: host-selected file location and base branch affect routing; later matching rules take precedence; eligible owners need appropriate access; required owner approval is separately configured; one eligible owner's approval can satisfy a multi-owner rule. The card makes no claim to have inspected actual repository protection or response capacity.

Optional future refinement: when a real PR is the subject of assessment, include its draft/ready status because the docs distinguish automatic review requests for draft PRs. The current card does not promise that all PR states trigger requests, so this omission is not a defect at its present scope.

## Limits

This is a bounded two-card primary-source check, not an audit of the docs lane or an executed repository assessment. The precise page/file locators above support the described mechanisms only. No framework behavior, translation quality, hosted enforcement or release outcome was independently tested.
