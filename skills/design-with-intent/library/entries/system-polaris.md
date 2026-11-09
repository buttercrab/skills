---
{
  "id": "system-polaris",
  "kind": "system",
  "title": "Shopify Polaris: current app-surface routing",
  "summary": "Choose the correct Shopify surface and current web-component documentation before borrowing admin patterns.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "operate",
      "configure",
      "manage"
    ],
    "contexts": [
      "commerce",
      "embedded-app",
      "merchant-tools"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://shopify.dev/docs/api/polaris",
      "title": "Polaris",
      "locator": "Overview; app surfaces; App Home/Admin/Checkout/Customer/POS routes",
      "revision": "polaris.shopify.com redirected here at inspection"
    },
    {
      "url": "https://shopify.dev/docs/api/app-home/latest/web-components",
      "title": "App Home web components",
      "locator": "Component categories; current version selector",
      "revision": "v2.0 latest shown at inspection; latest URL is mutable"
    },
    {
      "url": "https://shopify.dev/docs/api/app-home/latest",
      "title": "App Home",
      "locator": "App Bridge; web components; page-pattern routes; release channels",
      "revision": "v2.0 latest at inspection"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-carbon",
    "pattern-carbon-data-table",
    "flow-shopify-checkout-layout"
  ]
}
---

# Shopify Polaris: current app-surface routing

## When to use

Use when building a merchant-facing Shopify app or studying a mature commerce admin vocabulary. Ask which Shopify surface hosts the experience, what APIs it permits and which documentation version matches the project.

## What to inspect

The old Polaris address redirected to Shopify developer documentation. Inspect the surface selector, version and App Home web-component routes before reading a component. App Home, checkout, customer accounts and POS are different environments; a pattern name does not establish interchangeability.

## What to borrow and adapt

Borrow the habit of composing task-oriented merchant pages from consistent status, action, form and layout conventions. For an inventory import app, map setup, data review, empty results and error recovery before selecting components. In an actual Shopify app, align the embedded host and supported bridge behavior with the documented surface; elsewhere, adapt the workflow idea to the local stack.

## Mismatches and limits

Polaris is not a general customer storefront template. No web component or App Bridge integration was run, and documentation installation or deployment instructions were not executed. Currentness matters: historical React examples may not match the inspected v2.0 web-component route. A release candidate is not equivalent to a production-supported release. This card establishes navigation and scope, not visual or accessibility acceptance of a merchant application.

## Related resource roles

- [flow-shopify-checkout-layout](flow-shopify-checkout-layout.md): Contrast merchant tooling with checkout configuration and shopper progression; shared product branding does not make the actors interchangeable.
