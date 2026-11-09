---
{
  "id": "quality-versioning-and-human-release-notes",
  "kind": "guide",
  "title": "Versioning and release notes: define the contract and explain the change",
  "summary": "Use an explicit compatibility policy and human-oriented notes together, without treating commit syntax or a version bump as proof of compatibility.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "release",
      "document",
      "review"
    ],
    "contexts": [
      "public-api",
      "change-communication"
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
      "url": "https://semver.org/spec/v2.0.0.html",
      "title": "Semantic Versioning 2.0.0",
      "locator": "Specification items 1–10: public API, immutability, pre-1.0, deprecation and compatibility increments",
      "revision": "SemVer 2.0.0 specification"
    },
    {
      "url": "https://keepachangelog.com/en/1.1.0/",
      "title": "Keep a Changelog 1.1.0",
      "locator": "Guiding principles; types of changes; Unreleased; commit-log and deprecation discussion",
      "revision": "Guide version 1.1.0; inspected 2026-11-07"
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
    "quality-release-planning-workflows",
    "docs-rust-api-contracts"
  ]
}
---

# Versioning and release notes: define the contract and explain the change

## When to use

Use when consumers need to decide whether and how to upgrade, or a repository's automation guesses release significance from commit messages alone.

## What to inspect

Identify the public contract first: imports, command syntax, serialized formats, configuration, documented behavior or other supported surfaces. SemVer ties increments to a declared public API and treats released versions as immutable. Keep a Changelog is a human-oriented convention for notable differences and migration-relevant notes, not a requirement that every commit become an entry.

## What to borrow and adapt

For a CLI option rename, connect the compatibility decision, any deprecation period, tests of supported invocations and a user-facing upgrade note. Explain the effect in terms consumers recognize: what previously worked, what now changes, and which action they need to take. A reviewed note can accompany automated version preparation without outsourcing the underlying compatibility judgment to a prefix.

Choose a policy appropriate to the artifact and its users. A calendar-versioned application or a research dataset may have a different version contract; document that policy instead of forcing SemVer terminology onto an incompatible promise. A concise release page can be sufficient where users can find its history and migration information.

## Mismatches and limits

No compatibility tests or release history were exercised. Version labels do not prove non-breaking behavior, and a missing inspected changelog does not prove users lack release communication elsewhere. Keep a Changelog includes historical views about hosting interfaces; this card borrows its note-writing mechanism, not those mutable interface claims.
