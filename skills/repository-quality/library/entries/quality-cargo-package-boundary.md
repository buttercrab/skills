---
{
  "id": "quality-cargo-package-boundary",
  "kind": "guide",
  "title": "Cargo: inspect the crate that users will build",
  "summary": "Treat package inclusion and normalized dependency metadata as a separate boundary from a successful workspace checkout build.",
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
      "path-dependencies"
    ],
    "languages": [
      "rust"
    ],
    "scale": [
      "single-package",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://doc.rust-lang.org/cargo/commands/cargo-package.html",
      "title": "Cargo Book: cargo package",
      "locator": "Archive creation; normalized manifest; path dependencies; extracted build verification; --list; VCS information",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://doc.rust-lang.org/cargo/commands/cargo-publish.html",
      "title": "Cargo Book: cargo publish",
      "locator": "Description; --dry-run; --no-verify; post-upload polling timeout",
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
    "quality-cargo-workspace-selection",
    "repo-small-ripgrep"
  ]
}
---

# Cargo: inspect the crate that users will build

## When to use

Use when a crate builds with neighboring paths but fails after packaging, or when release preparation must establish exactly what leaves the repository.

## What to inspect

Read include/exclude rules, build-script inputs, resource paths and manifest dependency declarations. Cargo's package description distinguishes creating the archive from building its extracted contents. It rewrites the distributed manifest and handles path dependencies differently from local resolution. The VCS metadata file is explicitly a best-effort snapshot, not verified provenance.

## What to borrow and adapt

For a library using a code-generated lookup table, trace the generator input and whether the archive contains what the downstream build needs. Review the proposed archive file list, then choose an authorized package verification path appropriate to the toolchain and supported consumers. A path-only local dependency should not be treated as an externally resolvable version merely because the workspace compiled.

Document release preparation separately from upload. An upload command's timeout may occur after the registry received the crate, so retry policy must first reconcile the published version. A dry run can check preparation without authorizing publication; it is still executable build tooling and may need dependencies or network access.

## Mismatches and limits

No archive, dry run, build or registry request was executed here. The inspected current documentation includes options whose availability depends on Cargo version. A checked-in lockfile or VCS hash alone establishes neither reproducibility nor authentic source-to-artifact correspondence. Private internal crates may intentionally have no publication path.
