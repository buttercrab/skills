---
{
  "id": "quality-cargo-workspace-selection",
  "kind": "guide",
  "title": "Cargo: workspace convenience and selected validation scope",
  "summary": "Identify workspace membership, default members and inherited configuration before interpreting a root command as repository-wide validation.",
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
      "shared-configuration"
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
      "url": "https://doc.rust-lang.org/cargo/reference/workspaces.html",
      "title": "Cargo Book: Workspaces",
      "locator": "Root/virtual workspaces; members/exclude/default-members; package selection and inheritance",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://doc.rust-lang.org/cargo/commands/cargo-publish.html",
      "title": "Cargo Book: cargo publish",
      "locator": "Package selection; default-members; workspace selection; dry-run versus upload",
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
    "repo-small-uv",
    "repo-large-rust"
  ]
}
---

# Cargo: workspace convenience and selected validation scope

## When to use

Use when several Rust crates share a repository, a root command leaves some packages unchecked, or a contributor needs to know whether configuration belongs in a member or workspace root.

## What to inspect

Read workspace membership and exclusions, the root package versus virtual manifest, and `default-members`. Cargo shares a lockfile/output area and permits shared metadata, but package selection remains meaningful. Root-only patch/profile settings and inherited fields are not equivalent to independent values in every member. The publish documentation also exposes selection controls; repository membership is not a promise that every crate should be published.

## What to borrow and adapt

For a CLI plus reusable library, map the affected crate and its dependants before choosing checks. A fast package-specific test may be appropriate for a local edit, followed by workspace checks when a shared interface changes. Document which root command contributors should use and what it leaves out. Keep private helper crates and distributed crates distinguishable in manifests and release instructions.

A flat `crates/` convention can make membership easy to scan, but it should follow actual package boundaries. Do not split one small cohesive crate solely to resemble a large workspace; added crates introduce manifest, feature and publication obligations.

## Mismatches and limits

The command/reference docs describe intended behavior, not the target repository's supported Cargo version, enabled features or successful CI runs. Default members, feature selection and targets can each narrow validation. Running a root command is not automatically equivalent to testing every package, every feature combination or downstream crates.
