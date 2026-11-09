---
{
  "id": "quality-npm-workspace-scope",
  "kind": "guide",
  "title": "npm: linked workspaces are not independent package evidence",
  "summary": "Use workspace membership and script selection deliberately; local linking can conceal distribution and command-order assumptions.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "organize",
      "configure",
      "test"
    ],
    "contexts": [
      "workspace-scope",
      "local-linking"
    ],
    "languages": [
      "javascript",
      "typescript"
    ],
    "scale": [
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://docs.npmjs.com/cli/v11/using-npm/workspaces/",
      "title": "npm CLI 11: Workspaces",
      "locator": "Defining/linking workspaces; commands; ordering; --if-present",
      "revision": "CLI 11.21.2 documentation identifies itself Legacy; read 2026-11-07"
    },
    {
      "url": "https://docs.npmjs.com/cli/v11/commands/npm-pack/",
      "title": "npm CLI 11: npm pack",
      "locator": "workspace/workspaces/include-workspace-root options",
      "revision": "CLI 11.21.2 documentation; live read 2026-11-07"
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
    "repo-large-vscode",
    "quality-release-planning-workflows"
  ]
}
---

# npm: linked workspaces are not independent package evidence

## When to use

Use when multiple JavaScript or TypeScript packages share installation and commands, or when a root test result is being described as coverage of every package.

## What to inspect

Read the root workspaces declaration, member manifests and the exact command's selection options. npm documents automatic local package linking, explicit workspace execution and ordering. Missing scripts can be ignored with `--if-present`; a convenient aggregate command may therefore skip members intentionally. Packaging also has its own root/member inclusion options.

## What to borrow and adapt

For a parser and CLI that depend on each other, distinguish testing against the linked local package from testing what a downstream install receives. Make package-specific fast checks easy to find, and document the intended wider check when a shared contract changes. If a script relies on build order, inspect whether the root's declared order is sufficient rather than assuming a dependency scheduler.

A private application with internal packages might reasonably share a root workflow without publishing any member. A public utility suite needs a visible per-package consumer boundary. The same directory shape can serve either intent; ask about release ownership before importing a release orchestrator.

## Mismatches and limits

These are version-11 docs, explicitly labeled legacy at inspection; recheck the actual CLI version before prescribing exact flags. No install, test or pack command was run. A workspace-wide test script is not proof of package contents, independent installation, all scripts existing, or every member's published compatibility.
