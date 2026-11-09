# Catalog vocabulary

The catalog uses descriptive facets, not a universal design taxonomy. Inspect current labels/counts with `python3 scripts/catalog.py facets --status curated`. Filter values are exact; ordinary text search is case-insensitive literal substring matching. The helper does not secretly expand synonyms or rank aesthetic quality.

## Editorial task aliases

Obvious noun/verb duplicates are stored under a common action label. The table is a query aid; it is not a second source of resource metadata or a claim that every related concept is interchangeable.

| Alternate wording | Stored task label |
| --- | --- |
| clarification | `clarify` |
| collaboration | `collaborate` |
| comparison | `compare` |
| composition | `compose` |
| correction | `correct` |
| discovery | `discover` |
| evaluation | `evaluate` |
| framing | `frame` |
| grouping | `group` |
| implementation | `implement` |
| localization | `localize` |
| measurement | `measure` |
| navigation | `navigate` |
| onboarding | `onboard` |
| reading | `read` |
| recovery | `recover` |
| retrieval | `retrieve` |

Do not collapse meaningful distinctions such as evaluation versus verification, first-use versus repeated expert work, visual character versus interaction structure, or privacy visibility versus discoverability. New useful labels can be added as curation reveals a genuine need.

## Platform scope

Where justified, cards include `web` alongside `desktop-web` or `mobile-web`, and `native-mobile` alongside specific `ios`/`android` tags. Exact filters do not imply a hierarchy: broadening must be explicit in the card. A platform-neutral research principle may remain `cross-platform`; a browser-rendered marketing page is not evidence about a native app.

Use platform facets to understand the resource's target context, then inspect the actual evidence scope. A native-phone mockup and a tested native workflow can share a platform while supporting different claims.
