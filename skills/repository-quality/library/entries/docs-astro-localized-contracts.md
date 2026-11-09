---
{
  "id": "docs-astro-localized-contracts",
  "kind": "repository",
  "title": "Astro docs: localized content contracts and separate validation jobs",
  "summary": "Trace contribution routing, authored/generated page authority, content schemas and slug/link checks without treating translation tracking as translation correctness.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "localization",
      "verify",
      "generated-authority"
    ],
    "contexts": [
      "documentation-site",
      "community-contributions",
      "localized-content"
    ],
    "languages": [
      "typescript",
      "mdx",
      "markdown"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/CONTRIBUTING.md",
      "title": "withastro/docs: CONTRIBUTING.md",
      "locator": "Types of Contributions; i18n; Pages generated from outside sources; maintainer release process",
      "revision": "c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4"
    },
    {
      "url": "https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/package.json",
      "title": "withastro/docs: package.json",
      "locator": "check, docgen, lint:linkcheck and lint:slugcheck scripts",
      "revision": "c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4"
    },
    {
      "url": "https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/src/content.config.ts",
      "title": "withastro/docs: src/content.config.ts",
      "locator": "docsCollectionSchema, docs collection and external loaders",
      "revision": "c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4"
    },
    {
      "url": "https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/scripts/lint-slugcheck.mjs",
      "title": "withastro/docs: scripts/lint-slugcheck.mjs",
      "locator": "English counterpart discovery and failure exit",
      "revision": "c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4"
    },
    {
      "url": "https://github.com/withastro/docs/blob/c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4/.github/workflows/ci.yml",
      "title": "withastro/docs: .github/workflows/ci.yml",
      "locator": "astrocheck, eslint, slugcheck and linkcheck jobs",
      "revision": "c73a3bea5a635c1afce0f0516ff22ecb34a3d7d4"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Five pinned repository artifacts freshly read. Contributor entry and maintainer sections inspected, schema and slug checker followed into configured CI; no build or translation/deployment interaction."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "docs-mdn-content-contracts",
    "quality-generated-source-authority"
  ]
}
---

# Astro docs: localized content contracts and separate validation jobs

## When to use

Use when content types have structured metadata, translations share routes, or some references originate outside the docs repository. It also shows why contributors need different routes for obvious typos and substantial new material.

## What to inspect

The contributor manual routes larger proposals through issues/discussions, marks English-only exceptions to translation tracking, and explains generated pages' githubURL authority. Its prose mentions .md while the inspected slug checker explicitly matches both Markdown and MDX. The collection configuration delegates docs loading to Starlight; that loader implementation was not inspected. Inspect configuration before treating a filename convention in a guide as the complete rule.

## Change path

Trigger: change a reference page that has translated counterparts. First determine whether it is authored locally or derived elsewhere; then inspect its content-type schema and English/translated slug relationship. package.json maps focused commands to the CI's separate type, code, slug and built-link checks. The slug checker finds non-English files without corresponding English paths; it does not assess translation completeness or correctness.

## What to borrow and adapt

Make source authority and contributor routing visible close to the edit link. Validate structural contracts separately from content review. For a bilingual small project, a few named checks and translation ownership may be preferable to copying this site's full release-label automation.

## Mismatches and limits

The generated-source workflow and translation/release rules are documented, not replayed. Schema validity, a matching slug and a green build would still not prove language equivalence or reader comprehension. Some collection loaders fetch external data at build time; a local content tree is not a complete reproducible build environment.
