---
{
  "id": "pattern-govuk-check-answers",
  "kind": "system",
  "title": "GOV.UK check answers and correction loop",
  "summary": "Review submitted information with specific change links, retained values and a clear return route; adapt review placement to transaction size.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "review",
      "correct",
      "submit"
    ],
    "contexts": [
      "public-service",
      "forms",
      "transactional",
      "occasional-use"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://design-system.service.gov.uk/patterns/check-answers/",
      "title": "Check answers",
      "locator": "When to use; How it works; Let users go back and change their answers; HTML summary-list example",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow",
      "visual-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Pattern explanation and HTML example inspected as text; embedded review screen visually inspected in native Chrome. Correction sequence documented, not executed."
  },
  "reuse": "Link and original annotation only. GOV.UK page footer identifies Open Government Licence v3.0 except where stated; no upstream code, branding or assets redistributed.",
  "related": [
    "system-govuk",
    "principle-choice-context",
    "flow-etsy-custom-request"
  ],
  "flow_evidence": [
    {
      "url": "https://design-system.service.gov.uk/patterns/check-answers/",
      "locator": "Let users go back and change their answers",
      "sequence": [
        "enter answers",
        "review summary",
        "change a specific answer with existing values",
        "return to review",
        "submit"
      ],
      "method": "First-party pattern explanation and HTML inspected; no interaction executed."
    }
  ],
  "visual_evidence": [
    {
      "url": "https://design-system.service.gov.uk/patterns/check-answers/",
      "locator": "Embedded Check your answers review example",
      "observed": "GOV.UK blue header above grouped Personal details and Application details rows; labels, values and Change links align across horizontal dividers.",
      "method": "Public HTTPS example viewed with native Chrome CUA screenshot and accessibility tree. No Change or submit interaction executed."
    }
  ]
}
---

# GOV.UK check answers and correction loop

## When to use

Use when people need a final opportunity to inspect and correct information before sending an application or other meaningful transaction. It is a flow reference for review and recovery, not a reason to add confirmation to every small action.

## What to inspect

Read the transaction-size guidance, the section about returning to edit answers, and the summary-list HTML. The embedded example was also viewed: grouped label/value/change rows make individual correction targets visible. Notice the distinct change targets and added accessible context. Inspect the surrounding application's navigation and data retention separately; the isolated example cannot supply those contracts.

## What to borrow and adapt

Carry the person's existing answers into the edit view, then return them to the review context without repeating unrelated questions. For a workshop application, separate the applicant's details from the requested session and make the change action identify which answer it edits. Choose a single final review or sectional review according to the actual task and information volume.

## Mismatches and limits

A review page can add friction to a repeated expert action or a low-risk reversible preference. Do not reuse official-brand styling or make a local demo's submit button imply an actual application was sent. The card supports a documented correction mechanism; it does not establish keyboard behavior, server persistence, validation correctness or successful submission in a new implementation. Compare error recovery and task-list approaches when the workflow is longer or interrupted.

## Related resource roles

- [principle-choice-context](principle-choice-context.md): Review structure should follow task burden and uncertainty rather than a universal page or choice count.
- [flow-etsy-custom-request](flow-etsy-custom-request.md): Contrast structured correction before submission with open-ended negotiation before a purchasable item exists.
