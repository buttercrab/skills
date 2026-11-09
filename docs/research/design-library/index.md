# Design resource library: curation and coverage

Date: 2026-11-07. This is the first catalog-backed design edition. Start with the [browsable library](../../../skills/design-with-intent/library/index.md) or the [operating skill](../../../skills/design-with-intent/SKILL.md). The [approved plan](../../plans/awesome-design-library-plan.md) describes the intended workflow; [evaluation results](../../evaluations/design-library/results.md) record what was actually tested.

## Delivered collection

| Resource role | Cards | What they contribute |
| --- | ---: | --- |
| Skills | 16 | Direction, critique, design-system extraction, accessibility/motion repair, implementation, native adaptive layouts and contextual research workflows. |
| Tools | 11 | Sketch/prototype/reference discovery, component inspection, browser/state verification and evidence-scoped accessibility checks. |
| Product/screen/flow examples | 34 | 18 documented workflow cases and 16 viewed visual references with distinct roles and limits. |
| Systems/patterns | 24 | 23 curated system/pattern entries and one partially inspected candidate. |
| Foundations | 22 | Questioning, critique, choice/navigation, measurement, perception/reading, agency, accessibility and localization. |

Total: 107 cards, 106 curated and one candidate. Access labels: 100 public, five partial and two optional local-only resources. The cards contain approximately 23,700 words of original body annotation, in addition to structured metadata. These are selection resources/decision cases, not independent studies or a census of the internet.

Evidence modes overlap: 23 cards contain actual visual inspection receipts, 27 contain documented flow receipts, and two contain narrowly exercised public interactions. The latter are a Radix dialog open/Escape/focus-return check and Toss's public English-to-Korean switch. No counts imply complete product testing or an accessibility/usability acceptance result. [Machine-readable coverage](coverage.json) records exact aggregate fields.

## How the collection was built

Five parallel curation lanes inspected primary material and wrote original task/context/transfer/mismatch annotations. An initial representative batch calibrated the shared format before bulk writing. The builder uses JSON frontmatter in Markdown cards and Python's standard library; canonical cards generate human/agent indexes. A development lookup exposed the need for exact-facet vocabulary and matched-field receipts; see [calibration](calibration.md).

Existing deep research supplied leads and retained evidence where clearly attributed. It was not bulk relabeled as a catalog. Fresh source work broadened product references, public skill discovery and systems/patterns. Dated/pinned skills, historical accounts, live documentation, marketing screens and native-phone representations remain distinguishable.

| Curation lane | Record |
| --- | --- |
| Skills and tools | [Primary sources, capabilities, effects and access limits](skills-tools.md) |
| Systems and patterns | [Guidance, currentness changes, public demo and visual receipts](systems-patterns.md) |
| Product flows | [Workflow source inventory, actor/platform scope and gaps](product-flows.md) |
| Visual references | [Actual viewed surfaces, transfer, partial routes and observed switch](visual-examples.md) |
| Foundations | [Original evidence, standard scope and retained-versus-refreshed inspection](foundations.md) |

No upstream skill packages, scripts, application binaries, fonts or third-party artwork were installed or redistributed to create the collection. Original links and annotations are used. Two ui.sh resources remain optional local references because the installed bundle's exact public origin/version was not established. Their cards do not impose a personal filesystem path on the portable core.

## Priority coverage and remaining limits

| Design job/context | Representative coverage | Remaining limit |
| --- | --- | --- |
| Human creative direction and critique | Mixed initiative, contextual elicitation, comparative prototypes, preference critique and several skill workflows | No real-person creative-satisfaction or longitudinal collaboration study of this library. |
| First visit, joining and community | Meetup waitlist, Discord onboarding, visual Are.na/Duolingo/Finch and correction patterns | Product accounts and observed marketing surfaces do not establish a tested complete first-event journey. |
| Repeated expert/operations work | Figma state visibility, Linear disposition, Notion views, Carbon tables, Raycast/Linear public product previews | Public evidence rather than authenticated operational-product tests; no measured performance comparison. |
| Transactions and creative commerce | Shopify actor-separated configuration/grouping, Etsy custom requests, GOV.UK review/error/task patterns | No purchase or account action executed; requirements and availability must be adapted. |
| Learning and progression | Historical Duolingo path, viewed Brilliant problem framing, learning/choice foundations | Historical flow and current marketing are separate snapshots; no efficacy inference from design. |
| Native/mobile and adaptive work | Apple guidance, Android/SwiftUI skills, documented Maps/Slack/mobile contexts, viewed Things/Gentler phone representations | No current native-device journey or compatibility test performed. |
| Editorial, creative worlds and games | Pudding, Stripe Press, Poolsuite, Monument Valley, creative systems | Game-world marketing is not gameplay/menu/accessibility evidence; direct game interaction remains thin. |
| Accessibility and localization | Versioned WCAG/APG, W3C names/RTL/Hangul, language pattern, observed Toss switch | Standards and a single public switch do not establish complete localized or disabled-user journeys. |

## Independent review and corrections

Separate curators sampled one another's cards against underlying sources; this is not a full audit of every entry. The coordinator additionally reviewed the workflow/tool interface and one public visual sample.

| Review | Consequential result |
| --- | --- |
| [Workflow integration](workflow-review.md) | Added actual facet vocabulary and explicit literal/exact-filter semantics; normalized obvious task aliases without fuzzy quality scoring. |
| [Skills/tools](review-skills-tools.md) | Corrected the precise Impeccable deprecated alias and documented catalog-network/telemetry effects; preserved local-version and execution limits. |
| [Systems/patterns](review-systems-patterns.md) | Sampled current guidance/migrations and candidate scope; did not equate documentation with replayed interactions. |
| [Product flows](review-product-flows.md) | Separated Shopify merchant configuration from shopper grouping; removed unsupported Signal web-client scope and clarified actors. |
| [Visual examples](review-visual-examples.md) | Confirmed several actual screens and the narrow language switch; retained Monument Valley deep-link fragility while confirming the inspected root entry. |
| [Foundations](review-foundations.md) | Added precise APG read path and WCAG scope clarity; retained unsuccessful fresh-paper retrievals instead of claiming independent revalidation. |

Task labels use a small [editorial vocabulary note](../../../skills/design-with-intent/library/VOCABULARY.md). Explicit cross-family relationships connect visual examples to flow cases, patterns to foundation/verification, and skills to contextual alternatives. They are reading paths, not automatic activation or claims of independent corroboration.

## Discovery and maintenance queue

This queue identifies further work, not already inspected recommendations:

| Gap | Next useful investigation | Promotion requirement |
| --- | --- | --- |
| Current native end-to-end journeys | Permitted first-party screen sequences or authorized device observation | Actual state/actor/platform receipts; do not treat a phone mockup as a tested app. |
| Gameplay and accessible game interaction | Original game-interface/accessibility accounts and inspectable state examples | Relevant interaction or documented sequence beyond a promotional world image. |
| Broader multilingual/cultural visual work | Regional product examples and original layout/reading studies | Viewed local-script samples and explicit audience/script limits. |
| Disability-led and longitudinal evidence | Original studies of complete relevant tasks | Inspect methods/outcomes and preserve their population/context. |
| Pointing/steering and direct manipulation | Original papers and meaningful application contrasts | Contextual transfer, not a universal target or timing constant. |
| Trial-discovered contextual leads | Repair Café/Age UK newcomer framing, Meta voice-message preview, ODK offline/conflict handling and session-timeout guidance | Separate claim-specific primary inspection and contextual annotation before promotion; do not alter the frozen catalog to fit evaluation cases. |
| Optional local ui.sh provenance | Identify the exact publicly distributable bundle and version | Verify source identity and reuse scope before changing access labels. |
| Partial or fragile sources | Gestalt candidate, historical endpoints, deep-link/access changes | Substantive inspection, updated locators and honest version/access state. |

New discoveries should enter as leads until their claims are inspected. A selected resource that has changed can become needs-review or receive a revised annotation. Preserve stable IDs and relevant supersession; regenerate and validate the indexes. No scheduled automation or external publication was created.

## Use and validation scope

The package is self-contained for normal card reading and optional local search. The current library uses no database, mandatory server, embedding service or dependency installation. Tooling validates declared structure and consistency; it cannot prove the truth of a source observation.

Matching evaluation must distinguish reading a card from opening an original source, viewing a sample, documenting a flow and actually testing an interaction. Source/selection outlines cannot establish rendered UI quality. The earlier [execution pilot](../../evaluations/design-pilot/results.md), including browser-policy invalidations, remains unchanged and separate.
