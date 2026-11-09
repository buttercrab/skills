---
{
  "id": "repo-small-p-limit",
  "kind": "repository",
  "title": "p-limit: a flat tree with runtime, declaration and distribution boundaries",
  "summary": "A tiny JavaScript library keeps public runtime/type exports, behavioral tests and published-file intent discoverable without introducing package layers.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "organize",
      "test",
      "package",
      "navigate"
    ],
    "contexts": [
      "library",
      "public-api",
      "flat-layout"
    ],
    "languages": [
      "javascript",
      "typescript"
    ],
    "scale": [
      "small-project",
      "single-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/package.json",
      "title": "sindresorhus/p-limit: package.json",
      "locator": "exports, scripts.test, files and engines",
      "revision": "a8a6fbec4e0e866d6d779b10889bb4f5567e70eb"
    },
    {
      "url": "https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/index.js",
      "title": "sindresorhus/p-limit: index.js",
      "locator": "clearQueue and map error handling",
      "revision": "a8a6fbec4e0e866d6d779b10889bb4f5567e70eb"
    },
    {
      "url": "https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/index.d.ts",
      "title": "sindresorhus/p-limit: index.d.ts",
      "locator": "public API declarations",
      "revision": "a8a6fbec4e0e866d6d779b10889bb4f5567e70eb"
    },
    {
      "url": "https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/test.js",
      "title": "sindresorhus/p-limit: test.js",
      "locator": "clearQueue, iterable-error and concurrency scenarios",
      "revision": "a8a6fbec4e0e866d6d779b10889bb4f5567e70eb"
    },
    {
      "url": "https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/readme.md",
      "title": "sindresorhus/p-limit: readme.md",
      "locator": "API: rejectOnClear, map, clearQueue",
      "revision": "a8a6fbec4e0e866d6d779b10889bb4f5567e70eb"
    },
    {
      "url": "https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/.github/workflows/main.yml",
      "title": "sindresorhus/p-limit: .github/workflows/main.yml",
      "locator": "Node matrix and npm test",
      "revision": "a8a6fbec4e0e866d6d779b10889bb4f5567e70eb"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh primary repository metadata and selected substantive source/configuration/test/documentation sections inspected at the pinned commit. No upstream code, command, CI, build or release was executed."
  },
  "reuse": "Original annotations and primary-source links only; no upstream implementation, images or packages redistributed. License declarations are source facts, not legal advice.",
  "related": [
    "quality-npm-artifact-exports",
    "repo-large-vscode"
  ]
}
---

# p-limit: a flat tree with runtime, declaration and distribution boundaries

## When to use

Use as a counterexample when a small published library is being reorganized into layers merely because its root looks sparse. It is useful for assessing whether implementation, declarations, tests and package entry points are easy to find, while preserving a public API that is more subtle than the file count suggests.

## What to inspect

The manifest exports index.js alongside index.d.ts, runs lint, runtime tests and declaration tests in its aggregate test command, and limits its declared distribution file set. Read the queue-clearing and iterable-error branches, then the corresponding test names. The README distinguishes clearing queued work from behavior of promises already returned. CI calls the aggregate command on a Node-version matrix; that is configuration evidence, not a passing run.

## Change path

Trigger: change whether clearing the queue rejects pending promises. Follow package.json exports to index.js clearQueue, the declaration surface in index.d.ts, API explanation in readme.md and clearQueue tests in test.js. For iterable-mapping changes, follow map’s catch path and tests that ensure already-scheduled rejections are observed. The configured verification path is npm test → xo, ava and tsd; CI selects Node versions. The rejection-specific clearQueue scenarios are conditionally skipped on Node 20 for a documented AVA/DOMException issue, so the matrix does not imply uniform scenario coverage or a Node 20 implementation failure. Published npm contents were not inspected, so the manifest file list is intended packaging, not an observed tarball.

## What to borrow and adapt

Make the whole public maintenance surface visible at the project’s scale. A small library can use a small tree while still distinguishing runtime behavior, static declarations and distributed artifacts. Select regression scenarios around the invariant being changed rather than judging the repository by its number of directories. Adapt the combined check command to the language and consumers; do not add TypeScript declaration testing when no such surface exists.

## Mismatches and limits

This is a single narrow library, not an application with several independent deployments or a large contributor governance problem. A flat layout does not prove low coupling or good performance, and it should not override a real need for separate packages. Source, declaration and test excerpts were read at the pinned revision; no test, benchmark, package build or release was executed.

