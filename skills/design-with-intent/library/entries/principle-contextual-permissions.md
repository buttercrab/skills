---
{
  "id": "principle-contextual-permissions",
  "kind": "foundation",
  "title": "Request access at the relevant task boundary",
  "summary": "Combine Android's permission workflow with contextual-integrity evidence to explain why access is needed, respect refusal and preserve useful paths after denial.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "permissions",
      "onboard",
      "recover"
    ],
    "contexts": [
      "privacy",
      "consent",
      "mobile",
      "graceful-degradation"
    ],
    "platforms": [
      "native-mobile",
      "android"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://developer.android.com/training/permissions/requesting",
      "title": "Request runtime permissions",
      "locator": "Basic principles; workflow; handle permission denial",
      "revision": "Live platform documentation inspected 2026-11-07"
    },
    {
      "url": "https://arxiv.org/pdf/1504.03747",
      "title": "Android Permissions Remystified: A Field Study on Contextual Integrity",
      "locator": "Section 3 methodology/exit survey; sections 5.1–5.2 expectations and blocking",
      "revision": "Wijesekera et al., arXiv 1504.03747v1, 2015"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Current official guidance and original historical field-study PDF inspected. Platform behavior is version-dependent; no current device test or consent-effectiveness measurement."
  },
  "reuse": "Original decision annotation and source links only; no original paper, figures, data or third-party assets redistributed. Consult the source's terms for substantial reuse.",
  "related": [
    "principle-human-ai-control",
    "principle-informed-choice"
  ]
}
---

# Request access at the relevant task boundary

## When to use

Use when designing camera, location, notification or other protected-resource requests, especially if onboarding currently asks for every permission before the task is understood.

## What to inspect

Read platform-specific request/denial paths and whether the permission is actually necessary. In the field study, distinguish instrumented access events from sampled retrospective user judgments; a large event log is not an equally large participant sample.

## What to borrow and adapt

Connect a request to the action requiring it, explain the consequence, permit cancellation and preserve unrelated functions. Design denial/revocation as real states. Prefer a supported lower-access alternative when it satisfies the person's task.

For a photo attachment, the permission boundary belongs with selecting or capturing an image, not with a compulsory launch funnel. A refusal should leave the surrounding draft recoverable.

## Mismatches and limits

Android permission families, OS versions and special permissions differ; do not infer current behavior from the 2015 platform. Retrospective preferences are not observed response to a modern prompt. Contextual explanation must not become repeated persuasion until acceptance. This resource does not determine every jurisdiction's consent rules or justify access beyond the requested feature.
