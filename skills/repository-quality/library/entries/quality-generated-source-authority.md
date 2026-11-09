---
{
  "id": "quality-generated-source-authority",
  "kind": "guide",
  "title": "Generated source: review the authority and regeneration boundary",
  "summary": "Trace source inputs, generator version, outputs and drift enforcement instead of editing generated files or assuming ordinary tests regenerate them.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "generate",
      "verify"
    ],
    "contexts": [
      "generated-files",
      "source-authority"
    ],
    "languages": [
      "go",
      "language-agnostic"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://pkg.go.dev/cmd/go#hdr-Generate_Go_files_by_processing_source",
      "title": "Go command: Generate Go files by processing source",
      "locator": "Generate directive semantics; explicit execution; generated-code marker; ordering",
      "revision": "Page identifies go1.27.3; read 2026-11-07, not claimed latest toolchain"
    },
    {
      "url": "https://go.dev/blog/generate",
      "title": "Go Blog: Generating code",
      "locator": "2014 motivation and explicit author-versus-consumer generation workflow",
      "revision": "Rob Pike, 2014-12-22; historical account read 2026-11-07"
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
    "repo-small-uv",
    "repo-small-testify",
    "repo-large-sqlite"
  ]
}
---

# Generated source: review the authority and regeneration boundary

## When to use

Use when generated API clients, parsers, tables or reference pages are committed, regenerated during a build, or published from different inputs than contributors edit.

## What to inspect

Identify the authoritative input and exact generator/tool version, then follow its invocation and output consumer. The Go command documentation explicitly separates generation from build/test and explains the generated-source marker. The older Go account supplies motivation, but its historical installation examples should not be treated as current setup advice.

## What to borrow and adapt

For an enum-to-string table, the change path is enum declaration → pinned generator → generated file → focused behavior tests → any drift check. Ask whether the repository commits the output for downstream users or generates it during their build. If it commits the file, investigate how CI detects stale output; if it generates during build, investigate availability of the required tools and inputs in the distributed artifact.

Review both the human-edited input and meaningful output difference. Do not hand-edit the output merely because that makes the immediate test pass. A successful generator exit, a no-diff check and a regenerated published reference are different results; report the one actually obtained.

## Mismatches and limits

Go provides an illustrative mechanism, not a universal generator command for other ecosystems. No generator was executed. Generated files are not automatically undesirable, nor does an absent inspected regeneration job establish a defect: another build/publication boundary may provide the needed derivation. Running generation can execute arbitrary upstream commands.
