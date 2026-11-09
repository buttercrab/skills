---
{
  "id": "quality-scorecard-diagnostic-limits",
  "kind": "tool",
  "title": "OpenSSF Scorecard: inspect checks, access and unknowns",
  "summary": "Use individual security heuristics as investigative leads, preserving false positives, false negatives and permission-dependent visibility.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "assess",
      "verify",
      "prioritize"
    ],
    "contexts": [
      "repository-security-signals",
      "evidence-limits"
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
      "url": "https://github.com/ossf/scorecard/blob/b753b11c3523c5db8b4880c138858e7e7b8c614a/README.md",
      "title": "OpenSSF Scorecard README",
      "locator": "Scorecard checks; structured results/probes; false positives/negatives and aggregate-score limits",
      "revision": "b753b11c3523c5db8b4880c138858e7e7b8c614a"
    },
    {
      "url": "https://github.com/ossf/scorecard/blob/b753b11c3523c5db8b4880c138858e7e7b8c614a/docs/checks.md",
      "title": "Scorecard check documentation",
      "locator": "Branch-Protection permission notes; CI-Tests; Token-Permissions; Signed-Releases",
      "revision": "b753b11c3523c5db8b4880c138858e7e7b8c614a"
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
    "docs-github-codeowners",
    "quality-slsa-provenance-verification"
  ]
}
---

# OpenSSF Scorecard: inspect checks, access and unknowns

## When to use

Use when a repository assessment includes security-maintenance signals or a dependency decision needs a closer look at a particular practice. It is not a substitute for tracing the changed code or determining whether a project serves its users.

## What to inspect

Read the exact check's inputs, criteria, supported host and access conditions, not only the aggregate score. The README explicitly describes heuristics with false positives and false negatives. The pinned branch-protection documentation explains which queried settings need administrative visibility, alternative rule information and provider-specific unknowns. A caller's inability to read a control cannot be promoted into proof that the control is absent.

## What to borrow and adapt

For a low CI-related result, locate the named workflow, triggers and actual required checks before proposing changes. For protection findings, distinguish observable configured policy, evaluator permissions, unsupported settings and confirmed missing controls. Record the repository revision/tool configuration so the same numeric result is not mistaken for a timeless property.

Prefer a specific remediation tied to a relevant threat over chasing every point. A source-only educational repository and a privileged package-release pipeline have different consequential risks. The tool's own structured check/probe reasoning can guide which evidence to inspect next; it does not justify a universal pass threshold.

## Mismatches and limits

No scan, authentication setup or live repository-protection query was run. Pinned docs describe intended detection, not verified results for any sampled project. Even a release asset recognized as a provenance file is not evidence that a consumer validated its digest, signer and expectations. Scores can change when heuristics change without the repository changing.
