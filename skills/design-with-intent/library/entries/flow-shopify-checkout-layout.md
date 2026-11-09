---
{
  "id": "flow-shopify-checkout-layout",
  "kind": "example",
  "title": "Shopify: one-page versus three-page checkout",
  "summary": "Compare segmentation while retaining the same information requirements, and distinguish editor preview from the actual checkout surface.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "enter",
      "review",
      "purchase",
      "correct"
    ],
    "contexts": [
      "commerce",
      "consumer",
      "occasional"
    ],
    "platforms": [
      "web",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://help.shopify.com/en/manual/checkout-settings/customize-checkout-configurations/one-page-checkout",
      "title": "Shopify Help: One-page checkout",
      "locator": "Comparing layouts; Change your checkout layout; language customizations",
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
    "scope": "Shopper information grouping and separate merchant configuration instructions read. Native-mobile facet refers only to documented merchant Shopify-app configuration; no shopper native checkout or live workflow tested."
  },
  "flow_evidence": [
    {
      "url": "https://help.shopify.com/en/manual/checkout-settings/customize-checkout-configurations/one-page-checkout",
      "locator": "Introduction; Comparing one-page checkout to three-page checkout",
      "sequence": [
        "Shopper enters and reviews order, shipping and payment information",
        "Layout groups that information on one page or across three pages"
      ],
      "method": "Documented shopper-surface comparison, not a complete ordered purchase journey or interaction test."
    },
    {
      "url": "https://help.shopify.com/en/manual/checkout-settings/customize-checkout-configurations/one-page-checkout",
      "locator": "Change your checkout layout \u2014 Desktop and Mobile instructions; preview caveat",
      "sequence": [
        "Merchant opens checkout configuration in desktop admin or Shopify app",
        "Merchant chooses layout and saves",
        "Merchant inspects storefront checkout because editor preview is not real-time"
      ],
      "method": "Separate merchant configuration sequence from primary instructions. Shopify-app instructions support native-mobile configuration only; shopper purchase is not part of this sequence."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-etsy-custom-request",
    "flow-meetup-waitlist"
  ]
}
---

# Shopify: one-page versus three-page checkout

## When to use

Use for deciding whether to group a transaction or divide it into stages. The useful comparison holds the information requirements steady instead of assuming that fewer pages imply less work.

## What to inspect

Read the shopper information-grouping comparison separately from merchant layout configuration and its preview caveat. The setup instructions and customization list identify surfaces affected by a layout migration, including translated wording. The mobile instructions concern the merchant Shopify app; they do not establish a native shopper checkout. Do not run the merchant steps while researching.

## What to borrow and adapt

Separate field burden, validation, review and navigation from raw page count. In a workshop booking flow, compare complete variants with identical required choices; preserve correction and totals in both. Treat editor configuration, saved configuration and customer-facing rendering as distinct states. A migration checklist should include content and locale behavior as well as layout.

## Mismatches and limits

This is current documentation, not a comparative usability experiment or a tested storefront. It establishes no universal conversion advantage. Payment and shipping complexity differ by product and jurisdiction; no financial or compliance assurance is implied. Etsy custom requests are a better analogy when the user is negotiating a proposal before any purchase.
