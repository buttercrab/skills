# Independent source sample: systems and patterns

Reviewed 2026-11-07 by the skills/tools curator, independently of the systems author. Read seven current cards and underlying public primary material. This is a consequential-claim sample, **not an audit of all 24 systems/pattern cards**, their full dependencies or applications built from them. No other author's card or evaluation fixture was changed.

## Results

No required source correction found in this sample. These conclusions concern documentation support and calibrated scope. They do not independently reproduce the original curator's screenshots or interactions.

| Card | Independent evidence and conclusion |
| --- | --- |
| `pattern-material-navigation-bar` | [Material overview](https://m3.material.io/components/navigation-bar/overview), native Chrome accessibility text: compact/medium use, 3–5 equal peer destinations, consistency across screens, May 2025 flexible-bar update, older baseline deprecation and Web/Web Expressive unavailability are explicit. Card appropriately separates target implementation from platform inspiration. Mobile-web tagging does not establish an official web package; the body preserves that caveat. |
| `system-polaris` | [App Home](https://shopify.dev/docs/api/app-home/latest), primary text: current v2.0, iframe web components, App Bridge, UI-extension alternative and release-candidate limitations support its routing claim. [Polaris 2 update guide](https://shopify.dev/docs/apps/build/app-home/polaris2) also exists. No claim that historical React samples universally migrate unchanged is made. This is documentation scope, not integration proof. |
| `pattern-radix-dialog` | [Dialog](https://www.radix-ui.com/primitives/docs/components/dialog), features/API/keyboard sections: modal/nonmodal, controlled/uncontrolled and Escape-to-trigger behavior support the composition advice. Version 1.2.0 is displayed. The card explicitly limits its original interaction receipt to opening/Escape and excludes Save, persistence, trap auditing and screen-reader acceptance. This review read source; it did not replay that receipt. |
| `pattern-apple-onboarding` | [Apple HIG onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding), native Chrome accessibility text: safe interactive teaching, contextual tips, optional rediscoverable tutorials, postponed nonessential setup and contextual permissions support the synthesis. June 2024/June 2023 changelog entries match. Its flow receipt openly identifies a synthesis of documented options, rather than a single native journey tested. |
| `pattern-carbon-data-table` | [Guidelines](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines), sizing/variants/batch sections: five row sizes, dedicated destinations for cramped detail, selection-triggered batch bar and disabled row actions in batch mode support the operational guidance. Stable/React/Sep 30, 2026 labels match. Card correctly declines spreadsheet equivalence or runtime performance/keyboard acceptance. |
| `pattern-carbon-empty-states` | [Empty states](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states), cause table/anatomy/smaller regions: no-data, user-action and error-management distinctions, optional images/actions and less content in small spaces support the advice. Aug 11, 2026 label matches. No illustration or conversion efficacy was inferred. |
| `system-gestalt` | [Landing](https://gestalt.pinterest.systems/) exposes system purpose and foundations/components routes. [Foundations overview](https://gestalt.pinterest.systems/v1/foundations/overview) again exposed little substantive material in text retrieval. Candidate/partial classification and the explicit absence of component, visual and behavioral claims remain appropriate. A `v1` path is not treated as version proof. |

## Review surface and limits

Web text retrieval was sufficient for Shopify, Radix, Carbon and Gestalt. Material yielded a JavaScript shell; Apple yielded a shell and its linked Markdown route failed with unsupported content type. A single agent-created native Chrome public HTTPS tab then read the Material and Apple pages through the accessibility tree. No policy denial occurred, no local page/server was opened and no form, login, permissions prompt, tutorial or live component interaction was performed. Reading a rendered documentation page is not native-app verification.

The original author's visual and interaction receipts were checked for internal scope and consistency with documentation, not independently re-enacted. This review adds no screenshot/interaction modes to their cards. Static content may drift; latest/version selector labels need refresh at use time. Original annotation only; no third-party assets or code reproduced.

## Adjacent correction applied in owned lane

The foundations reviewer identified two precise improvements to `skill-impeccable`. Its own author applied them before this review: replace speculative frontend-design alias language with the documented deprecated `craft` alias, and add the pinned README receipt describing catalog network requests, anonymous direction-selection telemetry and hooks outside model approval. The card marks these as source-described, unexecuted and unaudited behavior.
