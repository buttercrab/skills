---
{
  "id": "docs-mdn-content-contracts",
  "kind": "repository",
  "title": "MDN content: page contracts and URL-preserving moves",
  "summary": "Follow authored Markdown, front-matter schema, move-link repair and redirect validation as separate parts of a documentation change.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "verify",
      "navigate"
    ],
    "contexts": [
      "documentation-site",
      "community-contributions",
      "url-compatibility"
    ],
    "languages": [
      "markdown",
      "javascript"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/mdn/content/blob/288e644117c29285df2acf37a2ac97f57546a146/CONTRIBUTING.md",
      "title": "mdn/content: CONTRIBUTING.md",
      "locator": "Documentation conventions; Front matter; Moving documents; Redirecting a document",
      "revision": "288e644117c29285df2acf37a2ac97f57546a146"
    },
    {
      "url": "https://github.com/mdn/content/blob/288e644117c29285df2acf37a2ac97f57546a146/package.json",
      "title": "mdn/content: package.json",
      "locator": "scripts content, lint:fm, start, build",
      "revision": "288e644117c29285df2acf37a2ac97f57546a146"
    },
    {
      "url": "https://github.com/mdn/content/blob/288e644117c29285df2acf37a2ac97f57546a146/front-matter-config.json",
      "title": "mdn/content: front-matter-config.json",
      "locator": "schema.required, additionalProperties and slug/page-type cases",
      "revision": "288e644117c29285df2acf37a2ac97f57546a146"
    },
    {
      "url": "https://github.com/mdn/content/blob/288e644117c29285df2acf37a2ac97f57546a146/scripts/front-matter_utils.js",
      "title": "mdn/content: scripts/front-matter_utils.js",
      "locator": "getAjvValidator and checkFrontMatter",
      "revision": "288e644117c29285df2acf37a2ac97f57546a146"
    },
    {
      "url": "https://github.com/mdn/content/blob/288e644117c29285df2acf37a2ac97f57546a146/scripts/update-moved-file-links.js",
      "title": "mdn/content: scripts/update-moved-file-links.js",
      "locator": "--check; Git rename detection; link replacements",
      "revision": "288e644117c29285df2acf37a2ac97f57546a146"
    },
    {
      "url": "https://github.com/mdn/content/blob/288e644117c29285df2acf37a2ac97f57546a146/.github/workflows/pr-check_redirects.yml",
      "title": "mdn/content: .github/workflows/pr-check_redirects.yml",
      "locator": "internal path filter and validate-redirects step",
      "revision": "288e644117c29285df2acf37a2ac97f57546a146"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Six pinned source artifacts freshly read; current branch SHA resolved through GitHub. No install, generator, linter, CI, preview or published redirect tested."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "docs-astro-localized-contracts",
    "docs-diataxis-reader-needs"
  ]
}
---

# MDN content: page contracts and URL-preserving moves

## When to use

Use when pages move, metadata drives navigation, or outside contributors need a reproducible content-edit path. A content repository can have contracts as consequential as a package API.

## What to inspect

Follow contribution instructions into the actual npm scripts and validator. Required title/slug/page-type and restricted properties are schema obligations; useful prose and technical truth remain review tasks. Inspect the move-link script's Git-status input and its check-versus-write behavior.

## Change path

Trigger: relocate an existing topic. The documented content-move command updates placement/redirect data; the separate script repairs references to renamed files; redirect CI validates its own boundary. Metadata edits pass through the schema-backed linter. The guide names a command, while package.json reveals the current Rari/Fred split behind content/build versus local preview. No command was executed here, and external CLI internals were not traced.

## What to borrow and adapt

Map a documentation move to old URL, new URL, links, metadata and validation. Tell a contributor which input owns each output. For a small manual, a redirect table plus a focused link check may suffice; MDN's full dependency set is unnecessary.

## Mismatches and limits

Workflow comments describe a required-check rationale; source inspection does not verify live branch protection, CI success, public redirects or deployment timing. The link-repair script depends on recognized working-tree renames and replacement patterns; it is not a universal crawler. Do not turn metadata validity into an editorial quality score.
