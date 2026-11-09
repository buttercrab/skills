---
{
  "id": "pattern-govuk-error-summary",
  "kind": "system",
  "title": "GOV.UK: validation recovery",
  "summary": "Connect page-level error navigation with precise errors beside affected fields.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "correct",
      "enter",
      "recover"
    ],
    "contexts": [
      "public-service",
      "transactional",
      "forms"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://design-system.service.gov.uk/components/error-summary/",
      "title": "Error summary",
      "locator": "When to use; How it works; accessibility and focus guidance",
      "revision": "live documentation; not pinned to a source commit"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-govuk",
    "pattern-govuk-check-answers"
  ],
  "flow_evidence": [
    {
      "url": "https://design-system.service.gov.uk/components/error-summary/",
      "locator": "How it works",
      "sequence": [
        "Submit form with invalid answers",
        "Show focused summary and matching inline errors",
        "Follow error link to affected input",
        "Correct and resubmit"
      ],
      "method": "Maintainer documentation sequence read as text; not executed."
    }
  ]
}
---

# GOV.UK: validation recovery

## When to use

Use this when submitting a form can leave several fields needing correction, especially on a long or unfamiliar service page. Ask what failures users can resolve, whether the server preserves valid answers, and where focus lands after rejection.

## What to inspect

Read summary-to-field linking and the relationship with inline errors. The documentation asks for a summary even for a single validation error, focus on the summary, and matching wording beside each field. Inspect the local form architecture before adopting that complete contract.

## What to borrow and adapt

Borrow a navigable map of unresolved problems. For an event application, link each error to its field, keep already valid answers, and explain a concrete correction in language the applicant understands. Write a recovery sequence covering submission, announcement, link activation, correction and successful resubmission; then test it with keyboard and assistive technology.

## Mismatches and limits

This card records guidance, not a tested application. A network outage, expired session or pending asynchronous check needs its own recovery model; treating every failure as an invalid input would blame the user. GOV.UK wording and placement are system conventions. Adopt them coherently or document the alternative rather than combining incompatible focus behaviors.
