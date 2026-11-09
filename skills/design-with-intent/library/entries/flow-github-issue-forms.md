---
{
  "id": "flow-github-issue-forms",
  "kind": "example",
  "title": "GitHub: structured community issue intake",
  "summary": "An authoring-to-contribution example connecting targeted prompts, required information, preview and a template chooser.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "submit",
      "report",
      "collect-context",
      "preview"
    ],
    "contexts": [
      "community",
      "developer-tools",
      "contributions"
    ],
    "platforms": [
      "desktop-web",
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository",
      "title": "GitHub Docs: Configuring issue templates",
      "locator": "Creating templates; Creating issue forms; Configuring template chooser",
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
      "url": "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository",
      "locator": "Creating templates; Creating issue forms; Configuring template chooser",
      "sequence": [
        "Maintainer defines purpose and fields",
        "Preview/edit configuration",
        "Commit to supported location",
        "Contributor chooses an applicable reporting route"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-linear-triage-decisions",
    "flow-mediawiki-review-publish"
  ]
}
---

# GitHub: structured community issue intake

## When to use

Use for bug reports, support intake or community submissions where people need enough structure to supply useful context. The fit is purposeful information collection and routing, not merely a long mandatory form.

## What to inspect

Read the sample field definitions and required/optional distinctions, then the chooser configuration. The inspected account is primarily the maintainer’s setup path; it does not independently test a contributor’s submission experience.

## What to borrow and adapt

Ask for evidence that changes the receiving team’s decision and mark optional information honestly. For a neighborhood repair request, a description and relevant photo may help while unrelated demographic questions add burden. Provide alternatives for people whose request does not fit a template. Preview the form and test with a realistic reporter before treating a technically valid schema as usable.

## Mismatches and limits

Only documentation/configuration examples were read; no repository or issue was changed. Preview status and supported field types can evolve. Required fields can prevent low-context reports but also exclude people who lack the requested information. Compare Linear Triage for what happens after intake and MediaWiki for review before publication.
