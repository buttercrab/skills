---
{
  "id": "repo-large-vscode",
  "kind": "repository",
  "title": "VS Code: tooling workspaces and test entrypoints are explicit maintenance boundaries",
  "summary": "The unit-runner workspace migration connects contributor package-manager guidance, root scripts, workspace membership and a private runner manifest.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "workspace-boundaries",
      "test-selection",
      "dependency-management",
      "navigate"
    ],
    "contexts": [
      "desktop-app",
      "monorepo",
      "tooling-workspaces"
    ],
    "languages": [
      "typescript",
      "javascript"
    ],
    "scale": [
      "large-project",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/microsoft/vscode/blob/f405fe233bbd3fd0647968e9356c2816362b2b3d/CONTRIBUTING.md",
      "title": "microsoft/vscode: CONTRIBUTING.md",
      "locator": "Contributing fixes and package-manager contract",
      "revision": "f405fe233bbd3fd0647968e9356c2816362b2b3d"
    },
    {
      "url": "https://github.com/microsoft/vscode/blob/f405fe233bbd3fd0647968e9356c2816362b2b3d/package.json",
      "title": "microsoft/vscode: package.json",
      "locator": "packageManager, test/compile/check scripts, first 110 lines",
      "revision": "f405fe233bbd3fd0647968e9356c2816362b2b3d"
    },
    {
      "url": "https://github.com/microsoft/vscode/blob/f405fe233bbd3fd0647968e9356c2816362b2b3d/test/unit/package.json",
      "title": "microsoft/vscode: test/unit/package.json",
      "locator": "Private runner dependencies",
      "revision": "f405fe233bbd3fd0647968e9356c2816362b2b3d"
    },
    {
      "url": "https://github.com/microsoft/vscode/commit/f405fe233bbd3fd0647968e9356c2816362b2b3d",
      "title": "microsoft/vscode: pinned change",
      "locator": "test/unit workspace member, dependency moves and lockfile importer changes",
      "revision": "f405fe233bbd3fd0647968e9356c2816362b2b3d"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned primary source/configuration/documentation and specified diff portions read. No upstream code, generator, test, build, CI, publication or remote mutation executed."
  },
  "reuse": "Original annotations and source links only. No upstream files or media redistributed; project-specific license statements are evidence, not legal advice.",
  "related": [
    "quality-npm-workspace-scope",
    "repo-small-p-limit"
  ]
}
---

# VS Code: tooling workspaces and test entrypoints are explicit maintenance boundaries

## When to use

Use when a large application keeps build/test tooling in separately managed workspace units, or when an agent assumes the root package's conventional test command represents the whole repository.

## What to inspect

The pinned root manifest declares a package manager and a `test` script that intentionally directs contributors to the repository's test scripts instead of running tests. Separate commands address browser, Node, extensions, smoke, build scripts, type checks and dependency layers. The contributor guide explicitly aligns installation with the manifest's manager.

The inspected commit makes `test/unit` a workspace member, moves runner-specific dependencies into its private manifest, and updates the lockfile importer. These files together establish a dependency-ownership migration; a directory rename alone would not.

## Change path

Trigger: change dependencies or execution needs of the unit-test runner → `test/unit/package.json` → workspace membership in `build/npm/dirs.ts` → corresponding `pnpm-lock.yaml` importer → owning test entrypoint. Root scripts expose several entrypoints, but their complete implementations were not followed or run. A product-source change would require a different path through its owning tests.

## What to borrow and adapt

Keep tooling dependencies at a meaningful ownership boundary when they otherwise inflate unrelated installation or obscure responsibility. Make the expected package manager discoverable in both the contributor entry and machine-readable metadata. Find what the default test script actually does before reporting it as validation.

The migration provides a concrete counterexample to “put every development dependency in the root” as a universal rule, while a single-package project may reasonably retain a single manifest and test command.

## Mismatches and limits

No package installation, Electron/browser launch, test, compilation or performance comparison occurred. A private tooling workspace is not an independently shipped user package. Do not transplant the whole script catalog or release infrastructure, or infer live extension/publishing behavior from the root manifest.

