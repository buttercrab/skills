---
{
  "id": "quality-reproducible-build-evidence",
  "kind": "guide",
  "title": "Reproducible builds: define artifacts and controlled variation",
  "summary": "Distinguish a repeatable setup from a bit-identical artifact claim, then investigate the specific sources of variation relevant to distribution.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "build",
      "verify",
      "release"
    ],
    "contexts": [
      "reproducibility",
      "artifact-boundaries"
    ],
    "languages": [
      "language-agnostic"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://reproducible-builds.org/docs/definition/",
      "title": "Reproducible Builds: Definitions",
      "locator": "Same source/environment/instructions; specified artifacts; bitwise comparison",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://reproducible-builds.org/docs/source-date-epoch/",
      "title": "Reproducible Builds: SOURCE_DATE_EPOCH",
      "locator": "Purpose; tool support and standardized-variable guidance",
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
    "quality-slsa-provenance-verification",
    "repo-large-sqlite"
  ]
}
---

# Reproducible builds: define artifacts and controlled variation

## When to use

Use when a project distributes binaries/archives, claims reproducible releases, or sees unexplained differences between equivalent builds. A local development command that succeeds twice answers a weaker question.

## What to inspect

Read which artifacts are covered and what source revision, environment and instructions define the claim. The Reproducible Builds definition requires matching output bytes for specified artifacts. Its SOURCE_DATE_EPOCH guidance addresses a common timestamp input but does not make every build deterministic merely by setting one variable.

## What to borrow and adapt

For a CLI archive, identify the expected binary/archive, compiler and dependency inputs, packaging order and metadata. Choose relevant variations such as build path, locale or timestamp, then compare outputs and explain differences. If the difference is in a ZIP timestamp rather than the executable, state that distinction instead of calling the entire application nondeterministic.

Document the narrow reproducibility envelope and preserve useful diagnostics. A two-person tool may begin with one important supported artifact and a clear build recipe; it need not claim independent multi-party reproduction of every platform to gain a useful debugging check. Conversely, downstream verifiers need more than a lockfile to reconstruct an artifact.

## Mismatches and limits

No builds or hash comparisons were performed here. Reproducibility does not establish absence of vulnerabilities, appropriate functionality or a trustworthy compiler. A signature/provenance statement and bit-identical rebuild are separate evidence. Avoid applying binary-release ceremony to an unpublished exploratory script without a distribution need.
