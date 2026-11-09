---
{
  "id": "flow-discord-community-onboarding",
  "kind": "example",
  "title": "Discord: questions that personalize channels and roles",
  "summary": "A community-joining case where questions have visible consequences and members can revise their answers after entry.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "onboard",
      "choose",
      "personalize",
      "return"
    ],
    "contexts": [
      "community",
      "games",
      "first-use"
    ],
    "platforms": [
      "web",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ",
      "title": "Discord Support: Community Onboarding FAQ",
      "locator": "Here is how it works; Default Channels; Customization Questions; post-join changes",
      "revision": "2023-03-31 support account; live body inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Relevant first-party documented sequence/state account inspected; no authenticated live product workflow exercised."
  },
  "flow_evidence": [
    {
      "url": "https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ",
      "locator": "Here is how it works; Default Channels; Customization Questions; post-join changes",
      "sequence": [
        "Present useful default channels",
        "Ask relevant customization questions",
        "Assign chosen channels/roles",
        "Enter community",
        "Revise answers through Channels & Roles"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-duolingo-guided-path",
    "flow-meetup-waitlist"
  ]
}
---

# Discord: questions that personalize channels and roles

## When to use

Use for a community with several meaningful interests or activities where showing every destination immediately is overwhelming. It is particularly relevant to the question “How will answering this change my experience?”

## What to inspect

Read default channels, answer-to-role/channel mapping and the distinction between before-join and later questions. The source explains that members can revisit their choices. This is an early product feature account, not a measured retention study.

## What to borrow and adapt

Ask only questions that change relevant navigation, participation or support. For a language club, distinguish finding a first event from choosing optional practice interests. Keep a useful default route for people who cannot yet classify themselves and let them revise preferences as they learn. Do not turn every preference into a compulsory entry gate. Show what an answer controls instead of collecting a decorative profile.

## Mismatches and limits

The source account and documented sequence were read; no server, role or permissions were changed, and screenshots were not viewed here. Role assignment can affect access, so mapping interests to authority needs deliberate review. The product’s requirements and administrative setup should not be copied as universal onboarding rules. Compare Duolingo when a prescribed sequence has a stronger domain justification.
