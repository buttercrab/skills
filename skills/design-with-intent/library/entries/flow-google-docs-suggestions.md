---
{
  "id": "flow-google-docs-suggestions",
  "kind": "example",
  "title": "Google Docs: propose, preview and accept changes",
  "summary": "A collaboration flow separating a proposed edit from authoritative document content and allowing individual or bulk review.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "propose",
      "review",
      "accept",
      "reject"
    ],
    "contexts": [
      "collaboration",
      "writing",
      "human-review"
    ],
    "platforms": [
      "desktop-web",
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://support.google.com/docs/answer/6033474",
      "title": "Google Docs Help: Suggest edits",
      "locator": "Suggest changes; Accept/reject one; Review suggested edits; permissions",
      "revision": "not-versioned; documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Relevant first-party documented sequence/state account inspected; no authenticated live product workflow exercised."
  },
  "flow_evidence": [
    {
      "url": "https://support.google.com/docs/answer/6033474",
      "locator": "Suggest changes; Accept/reject one; Review suggested edits; permissions",
      "sequence": [
        "Enter suggestion mode",
        "Make proposed change with context",
        "Owner reviews individual or combined result",
        "Accept or reject",
        "Return to document with chosen content"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-mediawiki-review-publish",
    "flow-etsy-custom-request"
  ]
}
---

# Google Docs: propose, preview and accept changes

## When to use

Use for collaborative writing or generated proposals where someone retains editorial authority. It helps distinguish an agent offering an option from silently applying it as the final result.

## What to inspect

Read suggesting mode, required access, single decisions and previewing the combined document. The source also describes cross-format tracked changes, but this card does not verify conversion fidelity.

## What to borrow and adapt

Represent proposals as changes to a shared object with a clear decision-maker. Let the reviewer understand the local edit and the resulting whole. For a design brief, show which assumptions or copy revisions are proposed and retain a route to reject them without losing the original. Bulk acceptance can help repetitive low-risk review, but should not conceal interactions between changes.

## Mismatches and limits

No document was opened or edited in an account. Product documentation supports the workflow, not the effectiveness of every review interface. A commenter’s ability to propose is not equivalent to publication authority. Compare MediaWiki’s author-driven publish/review loop and Etsy’s negotiation before a separate commitment.
