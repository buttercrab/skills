---
{
  "id": "quality-release-planning-workflows",
  "kind": "tool",
  "title": "Release planning: contributor change files versus commit-derived proposals",
  "summary": "Compare Changesets and Release Please by how human release intent enters the repository, and keep preparation, GitHub releases and registry publication distinct.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "release",
      "review",
      "document"
    ],
    "contexts": [
      "release-orchestration",
      "monorepo-publication"
    ],
    "languages": [
      "javascript",
      "typescript",
      "language-agnostic"
    ],
    "scale": [
      "single-package",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/googleapis/release-please/blob/ea20bc261acd75149f0be90890bb9c90e681eea7/README.md",
      "title": "Release Please README",
      "locator": "Release pull requests; Conventional Commits; scope excludes package-manager publication",
      "revision": "ea20bc261acd75149f0be90890bb9c90e681eea7"
    },
    {
      "url": "https://github.com/googleapis/release-please/blob/ea20bc261acd75149f0be90890bb9c90e681eea7/docs/manifest-releaser.md",
      "title": "Release Please manifest releaser",
      "locator": "Per-package configuration; released-version manifest; bootstrap/version behavior",
      "revision": "ea20bc261acd75149f0be90890bb9c90e681eea7"
    },
    {
      "url": "https://github.com/googleapis/release-please/blob/ea20bc261acd75149f0be90890bb9c90e681eea7/src/manifest.ts",
      "title": "Release Please manifest implementation",
      "locator": "buildPullRequests/createPullRequests; buildReleases/createReleases",
      "revision": "ea20bc261acd75149f0be90890bb9c90e681eea7"
    },
    {
      "url": "https://changesets.dev/guide/getting-started",
      "title": "Changesets: Getting Started",
      "locator": "Changeset files; contributor release intent; not every change needs a changeset",
      "revision": "Site identifies v3.0.3; footer links 2f6995d; read 2026-11-07"
    },
    {
      "url": "https://changesets.dev/guide/versioning-and-publishing",
      "title": "Changesets: Versioning and Publishing",
      "locator": "Reviewable versioning step separated from publication; tags",
      "revision": "Site identifies v3.0.3; read 2026-11-07"
    },
    {
      "url": "https://changesets.dev/guide/cli",
      "title": "Changesets: CLI",
      "locator": "version/publish/pack/publish-plan; private-package warning",
      "revision": "Site identifies v3.0.3; read 2026-11-07"
    },
    {
      "url": "https://github.com/changesets/changesets/blob/2f6995d5bbd3b1572d7a6cd897d2229bfc1ce8c1/README.md",
      "title": "Changesets README",
      "locator": "Development-branch notice and purpose",
      "revision": "2f6995d5bbd3b1572d7a6cd897d2229bfc1ce8c1"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned Release Please README/manifest guide and selected implementation methods read; pinned Changesets README/obsolete-doc notice and linked current guide/CLI pages read. Source/configuration and documented commands only; no release behavior executed."
  },
  "reuse": "Original annotations and source links only. Upstream source, standards text, binaries and assets are not redistributed; this is not a legal opinion.",
  "related": [
    "quality-versioning-and-human-release-notes",
    "quality-npm-workspace-scope"
  ]
}
---

# Release planning: contributor change files versus commit-derived proposals

## When to use

Use when a repository already has meaningful release coordination costs: several independently versioned packages, repeated hand-edited metadata, or release intent that is lost between contribution and publication. First ask who decides compatibility and which artifacts are actually distributed.

## What to inspect

Release Please reads Conventional Commit history to prepare reviewable release pull requests; its manifest maps package paths and known versions. The pinned implementation distinguishes building proposals, creating PRs and creating GitHub releases. Its README explicitly excludes package-manager publication. Changesets instead records contributor-written package bump intentions and summaries, then separates version preparation/review from publishing. Their input contracts differ; they are not interchangeable badges for a healthy monorepo.

## What to borrow and adapt

For two related packages, compare where a contributor can accurately state the intended impact. If that belongs with the change, a reviewable change file may be useful. If commit history reliably carries the policy, a generated release proposal may reduce repetition. In either case, inspect dependent-version handling, private packages, authoritative metadata, artifacts to validate, and the handoff to actual publication. A generated PR is a proposal, not proof of a shipped package.

Keep human-readable notes and version review possible. For a small tool released rarely, a short explicit release procedure may serve better than either orchestrator.

## Mismatches and limits

No tool was installed or run, PR opened, tag created or package published. Changesets main's pinned README calls itself v3 development; its old checked-in intro is marked outdated while the linked site identifies v3.0.3. These observed labels do not independently prove registry publication. Match documentation to the project's installed version before borrowing commands or automation assumptions.
