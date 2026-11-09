---
{
  "id": "quality-npm-artifact-exports",
  "kind": "guide",
  "title": "npm and Node: file contents and public entry points are separate contracts",
  "summary": "Review the packed files and exports map together so local imports do not hide missing output or accidental API breakage.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "package",
      "verify",
      "release"
    ],
    "contexts": [
      "published-artifacts",
      "public-api"
    ],
    "languages": [
      "javascript",
      "typescript"
    ],
    "scale": [
      "single-package",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://docs.npmjs.com/cli/v11/configuring-npm/package-json/",
      "title": "npm CLI 11: package.json",
      "locator": "files/.npmignore inclusion; always included/excluded files; exports/main/private",
      "revision": "CLI 11.21.2 documentation; live read 2026-11-07"
    },
    {
      "url": "https://docs.npmjs.com/cli/v11/commands/npm-pack/",
      "title": "npm CLI 11: npm pack",
      "locator": "dry-run/json/ignore-scripts; description and file-list behavior",
      "revision": "CLI 11.21.2 documentation; live read 2026-11-07"
    },
    {
      "url": "https://nodejs.org/api/packages.html#package-entry-points",
      "title": "Node.js: Packages",
      "locator": "Package entry points; introducing exports; subpath encapsulation",
      "revision": "Node.js v26.13.0 page inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Primary documentation sections read. No build, package installation, test, generator, publishing command, authentication change or upstream script executed."
  },
  "reuse": "Original annotations and source links only. Upstream source, standards text, binaries and assets are not redistributed; this is not a legal opinion.",
  "related": [
    "repo-small-p-limit",
    "quality-npm-workspace-scope"
  ]
}
---

# npm and Node: file contents and public entry points are separate contracts

## When to use

Use when TypeScript source works locally but a package omits its compiled file/declarations, or a cleanup proposes restricting previously usable import paths.

## What to inspect

Read `files`, ignore rules, entry points and the build outputs those entries name. npm's inclusion rules determine tarball contents; Node's exports rules determine which package paths consumers may resolve. One does not substitute for the other. Introducing exports can block previously accessible subpaths, so an apparently tidy metadata change may affect compatibility.

## What to borrow and adapt

For a package promising both JavaScript runtime and TypeScript types, trace each declared public entry to an actual distributed file. Plan a consumer-shaped import/type check against the artifact, using the supported environments rather than the repository's source alias configuration. Preserve supported deep imports or document an intentional compatibility change instead of silently sealing them.

Separate local package inspection from publication. Inspect lifecycle scripts before running pack or dry-run tooling, especially if preparing outputs is part of the process. Mark private members appropriately when the repository has packages that must never be published; do not infer that privacy from a folder name.

## Mismatches and limits

No tarball or consumer test was produced here. A file list does not prove runtime behavior, and a passing workspace build does not prove the list is correct. Exact inclusion/exports behavior is version-dependent. This card is not permission to upload a package or a guarantee that a package is safe to execute.
