---
{
  "id": "repo-small-uv",
  "kind": "repository",
  "title": "uv: source-authoritative CLI reference and build-time regeneration",
  "summary": "A multi-crate Rust/Python tool distinguishes authoring CLI declarations, generating reference pages, checking selected outputs and publishing rebuilt documentation.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "generated-files",
      "document",
      "test",
      "release"
    ],
    "contexts": [
      "cli",
      "workspace",
      "generated-reference",
      "documentation-site"
    ],
    "languages": [
      "rust",
      "python",
      "shell"
    ],
    "scale": [
      "multi-package",
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/CONTRIBUTING.md",
      "title": "astral-sh/uv: CONTRIBUTING.md",
      "locator": "snapshot testing and Documentation section",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
    },
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.cargo/config.toml",
      "title": "astral-sh/uv: .cargo/config.toml",
      "locator": "cargo dev alias",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
    },
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/crates/uv-cli/src/lib.rs",
      "title": "astral-sh/uv: crates/uv-cli/src/lib.rs",
      "locator": "Cli, TopLevelArgs and command argument declarations",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
    },
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/crates/uv-dev/src/generate_cli_reference.rs",
      "title": "astral-sh/uv: crates/uv-dev/src/generate_cli_reference.rs",
      "locator": "Mode handling, Clap build and reference rendering",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
    },
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/check-generated-files.yml",
      "title": "astral-sh/uv: .github/workflows/check-generated-files.yml",
      "locator": "DryRun versus selected Check calls",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
    },
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/check-docs.yml",
      "title": "astral-sh/uv: .github/workflows/check-docs.yml",
      "locator": "reference regeneration followed by strict docs build",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
    },
    {
      "url": "https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/publish-docs.yml",
      "title": "astral-sh/uv: .github/workflows/publish-docs.yml",
      "locator": "release documentation generation and publication inputs",
      "revision": "5ce34500b8a3d16d24bc7576bd8ac64879091cea"
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
    "quality-generated-source-authority",
    "quality-cargo-workspace-selection"
  ]
}
---

# uv: source-authoritative CLI reference and build-time regeneration

## When to use

Use for command-line systems with generated user documentation, especially where a large repository makes it unclear whether a checked-in page or a source declaration is authoritative. It is useful when a stale-looking generated file tempts an assessor to declare missing enforcement after reading only one workflow.

## What to inspect

The cargo dev alias targets uv-dev. CLI arguments live in uv-cli, while the reference generator constructs the Clap command, builds it before inspection so propagated options exist, and writes docs/reference/cli.md. Its DryRun, Check and Write modes have different effects. The broad generated-files job uses DryRun and selected explicit comparisons; documentation checking and publication separately regenerate reference material before their build/publication paths. Contributor documentation describes focused snapshot review and documentation regeneration.

## Change path

Trigger: change a command option or its help text. Start at the owning declaration in crates/uv-cli/src/lib.rs, follow uv-dev’s generate_cli_reference into its built Clap model and rendered reference output, then inspect check-docs and publish-docs as separate consumers. The generator’s selected Check mode compares the existing page; DryRun prints generated content; Write updates it. The configured documentation workflow regenerates CLI/options/environment/preview references before a strict MkDocs build. This path separates source intent, checked-in freshness and built/published freshness.

## What to borrow and adapt

State source authority next to generated artifacts and make each validation mode’s effects explicit. Follow the complete path before calling a missing drift comparison a defect: generating correct publication input at build time is different from enforcing checked-in equality. A smaller CLI could use one generator command and one clear check without copying uv’s multi-crate layout, snapshot infrastructure or release automation.

## Mismatches and limits

No generator, docs server, test, release or publication ran during this research. Workflow configuration does not prove its live execution, credential access or deployed-page freshness. A guessed .github/workflows/docs.yml path returned 404; the inspected owning workflows are check-docs.yml and publish-docs.yml. This is an evidence-path correction, not evidence that documentation automation was absent.

