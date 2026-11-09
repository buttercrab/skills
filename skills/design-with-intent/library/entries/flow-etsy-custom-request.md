---
{
  "id": "flow-etsy-custom-request",
  "kind": "example",
  "title": "Etsy: negotiate a custom request before purchase",
  "summary": "A creative-commerce case separating configurable personalization from an open-ended proposal and later purchasable item.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "request",
      "customize",
      "discuss",
      "purchase"
    ],
    "contexts": [
      "commerce",
      "creative-services",
      "consumer"
    ],
    "platforms": [
      "web",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://help.etsy.com/hc/en-us/articles/115015440167-How-to-Request-a-Personalized-or-Custom-Item",
      "title": "Etsy Help: Request a Personalized or Custom Item",
      "locator": "Personalize an item; Request custom item; After you send a request",
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
      "url": "https://help.etsy.com/hc/en-us/articles/115015440167-How-to-Request-a-Personalized-or-Custom-Item",
      "locator": "Personalize an item; Request custom item; After you send a request",
      "sequence": [
        "Choose listing personalization or custom request",
        "Describe needs/reference/deadline",
        "Discuss feasibility and terms",
        "Seller may create private listing",
        "Buyer separately chooses whether to purchase"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-shopify-checkout-layout",
    "flow-google-docs-suggestions"
  ]
}
---

# Etsy: negotiate a custom request before purchase

## When to use

Use when the person cannot specify a finished product from predefined options: commissions, tailored services or custom fabrication. The distinction between a request and a confirmed purchase is central.

## What to inspect

Read the two entry paths and the post-request state. The help account describes request messages, progress updates and a possible private listing; it is not a universal contract for every seller.

## What to borrow and adapt

Offer structured prompts for relevant constraints and references while retaining room for discussion. In a community workshop commission, ask about intended use, deadline and what matters in an example. Make clear whether submitting starts a conversation, reserves capacity or commits money. Keep feasibility and purchase as explicit later decisions; preserve the person’s evolving idea without pretending every request can be priced instantly.

## Mismatches and limits

No seller was contacted, image uploaded or purchase made. The documentation does not prove response quality or fulfillment. Personalization is more bounded than an open commission, so do not force both into the same control. Compare Shopify when the product is already defined and only transaction details remain.
