---
{
  "id": "flow-signal-usernames",
  "kind": "example",
  "title": "Signal: identity visibility versus discoverability",
  "summary": "A privacy-settings example separating what others can see, how they can initiate contact, and an optional shared identifier.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "configure",
      "connect",
      "share-identity",
      "recover"
    ],
    "contexts": [
      "messaging",
      "privacy",
      "consumer"
    ],
    "platforms": [
      "native-mobile",
      "desktop"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://support.signal.org/hc/en-us/articles/6712070553754-Phone-Number-Privacy-and-Usernames",
      "title": "Signal Support: Phone Number Privacy and Usernames",
      "locator": "Phone-number settings and Android/iOS/Desktop paths; Share username; Start a chat by username; Receiving a message request via username",
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
    "scope": "First-party Android/iOS/Desktop settings and actor-specific contact account read; support website and shared URL are not evidence of a web client. No account settings or messaging exercised."
  },
  "flow_evidence": [
    {
      "url": "https://support.signal.org/hc/en-us/articles/6712070553754-Phone-Number-Privacy-and-Usernames",
      "locator": "How do I manage Phone Number Privacy Settings?; Share username",
      "sequence": [
        "Username owner chooses phone-number visibility and discoverability in Signal settings",
        "Owner optionally creates and shares an identifier"
      ],
      "method": "Owner-side documented settings/sharing states; source distinguishes Android, iOS and Desktop paths. No web-client or interaction evidence."
    },
    {
      "url": "https://support.signal.org/hc/en-us/articles/6712070553754-Phone-Number-Privacy-and-Usernames",
      "locator": "Start a chat by username; Receiving a message request via username",
      "sequence": [
        "Contact initiator uses the owner\u2019s exact username to open a new chat and send a request",
        "Username owner receives request and may accept",
        "Acceptance shares the owner\u2019s profile name/image with the initiator; existing chats may merge"
      ],
      "method": "Actor-labeled summary of documented contact states. Username owner is the receiving/accepting party; contact initiator sends the request. Not interaction-tested."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-steam-family-roles",
    "flow-discord-community-onboarding"
  ]
}
---

# Signal: identity visibility versus discoverability

## When to use

Use when settings with similar names change different relationships: visible identity, search/discovery and connection requests. It also helps explain why a privacy choice can reduce discoverability.

## What to inspect

Read both number settings and username purpose together, including existing contacts/chats and changed identifiers. Distinguish the username owner, contact initiator and request recipient: the owner receives and may accept a request initiated by another person. Do not reduce the source to one reassuring “private” toggle.

## What to borrow and adapt

Explain what each setting changes for specific people. In a member directory, hiding a phone field and preventing number-based search are different promises. Provide an intentional alternate connection route and explain what happens to a shared link after changes. Keep profile name, login identifier and contact address conceptually separate when their lifecycles differ. Use examples grounded in actual relationships rather than broad security adjectives.

## Mismatches and limits

The documentation describes Android, iOS and Desktop paths; its support-site address and shared contact URL do not establish a web client. Accounts and privacy controls were not operated. It does not independently establish cryptographic guarantees, anonymity or protection against all recipients. Existing knowledge cannot be made unknown by hiding a field. Compare Steam for authority roles and Discord for personalization that changes navigation rather than identity exposure.
