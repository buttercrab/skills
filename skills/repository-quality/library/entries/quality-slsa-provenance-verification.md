---
{
  "id": "quality-slsa-provenance-verification",
  "kind": "standard",
  "title": "SLSA v1.2: provenance must be verified against expectations",
  "summary": "Connect distributed artifacts to trusted build identities and expected source/parameters; do not treat an attestation filename as a quality certificate.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "verify",
      "release",
      "trace"
    ],
    "contexts": [
      "provenance",
      "distribution-trust"
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
      "url": "https://slsa.dev/spec/v1.2/build-track-basics",
      "title": "SLSA v1.2: Build Track Basics",
      "locator": "Build L0–L3; purpose and protection progression",
      "revision": "Approved SLSA v1.2 Build track; read 2026-11-07"
    },
    {
      "url": "https://slsa.dev/spec/v1.2/verifying-artifacts",
      "title": "SLSA v1.2: Build Verifying artifacts",
      "locator": "How to verify; artifact digest/trust root; expected builder/source/buildType/externalParameters",
      "revision": "Approved SLSA v1.2; read 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Primary documentation sections read. No build, package installation, test, generator, publishing command, authentication change or upstream script executed."
  },
  "reuse": "Original annotations and source links only. Upstream source, standards text, binaries and assets are not redistributed; this is not a legal opinion.",
  "related": [
    "quality-reproducible-build-evidence",
    "quality-scorecard-diagnostic-limits"
  ]
}
---

# SLSA v1.2: provenance must be verified against expectations

## When to use

Use when a release pipeline or downstream policy needs to establish where a distributed artifact came from. Start from that threat/consumer need, not a desire to add a badge to every repository.

## What to inspect

Read the declared track/version and its requirements before transferring a level claim. The Build track distinguishes provenance existence, hosted signed provenance and hardened build isolation. Verification also checks that the statement applies to the artifact and matches trusted identities and expected inputs. A file's existence is not the same as accepting its content under an appropriate trust policy.

## What to borrow and adapt

For a downloadable CLI, map source revision → build identity/process → artifact digest → distributed provenance → consumer verification policy. Decide what happens if the source repository, builder or parameters differ from expectation. Keep provenance production and consumer verification separately visible in the repository's release documentation and checks.

Choose proportionate controls for the actual distribution promise. For a local experiment, documenting the build inputs may be sufficient to the current task; do not silently set up credentials or an external release pipeline. For published artifacts relied on by others, identify the concrete authenticity gap before recommending a particular implementation.

## Mismatches and limits

No provenance was generated or verified. These are supply-chain properties, not code-correctness, usability or vulnerability-free certificates. The inspected v1.1 pages are retired and the old v1.2 `/levels` path failed; use the recorded v1.2 read paths. Reproducibility is related but does not replace the trust policy described here.
