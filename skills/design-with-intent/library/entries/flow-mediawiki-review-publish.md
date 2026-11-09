---
{
  "id": "flow-mediawiki-review-publish",
  "kind": "example",
  "title": "MediaWiki VisualEditor: draft, review and publish",
  "summary": "A public-contribution flow where editing, reviewing the diff and committing an externally visible change remain separate stages.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "edit",
      "preview",
      "review",
      "publish"
    ],
    "contexts": [
      "community",
      "editorial",
      "contributions"
    ],
    "platforms": [
      "desktop-web",
      "mobile-web",
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.mediawiki.org/wiki/Help:VisualEditor/User_guide/en",
      "title": "MediaWiki Help: VisualEditor User guide",
      "locator": "Publishing changes; Resume editing; switching editor; local-wiki differences",
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
      "url": "https://www.mediawiki.org/wiki/Help:VisualEditor/User_guide/en",
      "locator": "Publishing changes; Resume editing; switching editor; local-wiki differences",
      "sequence": [
        "Edit local draft",
        "Open publish dialog",
        "Describe change and optionally review",
        "Resume editing or commit the whole change"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-google-docs-suggestions",
    "flow-github-issue-forms"
  ]
}
---

# MediaWiki VisualEditor: draft, review and publish

## When to use

Use for contribution tools, CMS editors or public forms where a draft should remain revisable until a deliberate commit. It is especially relevant when an edit is easy but its publication consequences are less obvious.

## What to inspect

Read Publishing changes and the return-to-edit behavior. The help documentation describes a disabled action when nothing changed and an intermediate dialog; do not infer that every wiki exposes exactly the same tools.

## What to borrow and adapt

Give the person a clear boundary between preparation and publication. A venue listing editor could preserve a draft, summarize meaningful changes, let the person inspect them and return to correction. Make commit scope explicit: updating one subcomponent may still publish the entire object. Preserve context when switching modes and avoid implying that a preview is already saved externally.

## Mismatches and limits

Only the guide was read; no live article was edited or published, and its screenshots were not visually inspected here. This is not permission to perform a public contribution. Review does not guarantee factual accuracy. Google Docs offers a contrasting model where a different collaborator accepts proposed changes.
