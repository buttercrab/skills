---
{
  "id": "quality-go-module-workspace-boundaries",
  "kind": "guide",
  "title": "Go: module release units versus local workspaces",
  "summary": "Keep each module independently consumable where promised, even when go.work makes joint local development convenient.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "organize",
      "test",
      "release"
    ],
    "contexts": [
      "module-boundaries",
      "workspace-scope"
    ],
    "languages": [
      "go"
    ],
    "scale": [
      "single-package",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://go.dev/doc/modules/managing-source",
      "title": "Go: Managing module source",
      "locator": "Choosing repository scope; independent versioning; single/multiple modules",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://go.dev/ref/mod#workspaces",
      "title": "Go Modules Reference",
      "locator": "Workspaces; go.work use/replacement behavior; CI warning and committed-workspace exceptions",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://go.dev/doc/modules/release-workflow",
      "title": "Go: Module release and versioning workflow",
      "locator": "Local unpublished client development; release/version progression",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
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
    "repo-large-kubernetes",
    "repo-small-go-cmp"
  ]
}
---

# Go: module release units versus local workspaces

## When to use

Use when deciding whether Go code needs another module, when a monorepo consumer sees dependencies unlike local CI, or when a checked-in workspace changes what the project actually tests.

## What to inspect

Identify module paths and version boundaries before counting directories. Go's source guide ties modules to independent versioning. Its reference explains that workspace modules participate together in dependency selection and warns that a checked-in workspace can mask consumer behavior; it also describes cases where committed joint workspaces make sense. A repository can hold several modules, but local convenience does not settle their external contracts.

## What to borrow and adapt

For an SDK and separate command module, validate the intended local combination during development and also consider the released-version dependency path consumers use. Record whether CI uses workspace mode or an individual module, and why. If a local replacement makes an unpublished API available, avoid claiming that the declared published dependency already contains it.

Split a module when its version/support ownership warrants that boundary, not simply because a directory grows. For a single tool with cohesive packages, one module can keep the release path clearer. Make any checked-in workspace policy explicit in contributor commands so an ancestor workspace does not silently change conclusions.

## Mismatches and limits

The guidance was read, not executed against Go modules. No universal ban on committing go.work follows: the documented exception matters. Local tests, module-mode tests and tag/proxy availability are distinct evidence. This card does not establish a consumer compatibility matrix or authorize release tags.
