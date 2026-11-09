---
{
  "id": "docs-rust-book-source-listings",
  "kind": "repository",
  "title": "Rust book: prose, included listings and publication snapshots",
  "summary": "Locate the true input for an included code example and distinguish source, print snapshots, doctests and release-train publication.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "generated-authority",
      "verify"
    ],
    "contexts": [
      "documentation-site",
      "executable-examples",
      "release-trains"
    ],
    "languages": [
      "rust",
      "markdown",
      "shell"
    ],
    "scale": [
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/README.md",
      "title": "rust-lang/book: README.md",
      "locator": "Building; tests; contribution/release-train expectations",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/CONTRIBUTING.md",
      "title": "rust-lang/book: CONTRIBUTING.md",
      "locator": "Where to Edit; Checking for Fixes; Expectations",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/src/ch12-01-accepting-command-line-arguments.md",
      "title": "rust-lang/book: src/ch12-01-accepting-command-line-arguments.md",
      "locator": "Listings 12-1/12-2 rustdoc_include and included output",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/listings/ch12-an-io-project/listing-12-01/src/main.rs",
      "title": "rust-lang/book: listings/ch12-an-io-project/listing-12-01/src/main.rs",
      "locator": "executable listing source",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/book.toml",
      "title": "rust-lang/book: book.toml",
      "locator": "preprocessors, HTML redirects and nostarch sync comment",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/.github/workflows/main.yml",
      "title": "rust-lang/book: .github/workflows/main.yml",
      "locator": "trpl build before mdbook test; package_tests; lint",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/packages/trpl/Cargo.toml",
      "title": "rust-lang/book: packages/trpl/Cargo.toml",
      "locator": "standalone support crate workspace boundary",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    },
    {
      "url": "https://github.com/rust-lang/book/blob/2771df165f092a4fbb9f46b5b2e7450f19010adb/ci/validate.sh",
      "title": "rust-lang/book: ci/validate.sh",
      "locator": "link2print references loop",
      "revision": "2771df165f092a4fbb9f46b5b2e7450f19010adb"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Eight pinned repository artifacts freshly read; source includes and CI path followed. No Rust/mdBook/tool download, executable example, package test or release run."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "quality-generated-source-authority",
    "docs-diataxis-reader-needs"
  ]
}
---

# Rust book: prose, included listings and publication snapshots

## When to use

Use for tutorials with compiled examples, print/web variants or content shipped with a language release. It contrasts authored narrative with included executable material and publication snapshots.

## What to inspect

The contributor guide directs prose work to src and warns against editing nostarch print snapshots. Follow an actual chapter: its code block includes a file under listings, and terminal output is also included. A blanket instruction to edit only Markdown would miss those inputs. book.toml additionally identifies selected synchronization and renderer-only exceptions.

## Change path

Trigger: revise the argument-reading example in chapter 12. Trace the prose include to listing-12-01/src/main.rs, then inspect mdBook preprocessing and CI. CI builds the trpl support crate before passing its dependency path to mdbook test, and separates package tests, spelling and reference/link checks. The support crate declares a separate workspace boundary. These commands and relationships were read, not run.

## What to borrow and adapt

Keep examples executable where that guards a real user promise; make included/generated authority discoverable. Separate an upstream source fix from its arrival in stable documentation. A modest README may need one verified example instead of a publishing workspace.

## Mismatches and limits

The print/edition policy belongs to this book and can make non-error revisions slow; it is unsuitable as a default contribution rule. An include's existence does not prove every rendered listing is tested or its output current. No release, build, published book or compatibility result was verified.
