# Independent sample review of product-flow references

Reviewed 2026-11-07. Six varied cards were compared with their linked first-party documentation: community, commerce, native offline use, privacy, operational intake and learning. This is a documentary sample review, not a full catalog audit, current product acceptance test or independent visual inspection. No account, signup, native app, payment, submission or settings change was exercised. Source images embedded in documentation were not independently viewed for this review; the Duolingo author's separate visual receipt is outside this review's evidence.

## Corrections requested

### `flow-shopify-checkout-layout`: separate merchant setup from shopper experience

Source: [Shopify — One-page checkout](https://help.shopify.com/en/manual/checkout-settings/customize-checkout-configurations/one-page-checkout), “Comparing layouts” and “Change your checkout layout,” including Desktop and Shopify-app tabs.

The comparison supports holding information requirements steady across layouts. The setup steps belong to a merchant: open configuration, choose layout, save, then inspect storefront checkout because the editor preview is not real time. The card's receipt instead begins with shopper information entry before switching to merchant configuration. Although the prose correctly distinguishes these surfaces, the metadata reads as one actor's ordered journey.

**Requested correction:** separate two receipts or explicitly label actors and present these as related workflows rather than one sequence. Clarify that `native-mobile` is supported by merchant configuration through the Shopify app; this source does not establish a native shopper checkout flow. Preserve the preview limitation and absence of a comparative usability/conversion result.

### `flow-signal-usernames`: platform and actor precision

Source: [Signal — Phone Number Privacy and Usernames](https://support.signal.org/hc/en-us/articles/6712070553754-Phone-Number-Privacy-and-Usernames), “Where do I see my phone number in Signal?”, “Start a chat by username,” “Receiving a message request via username,” and “What happens if I message someone by phone number and by username?”

The source documents Android, iOS and Desktop app settings. A shareable URL is an initiation artifact; it does not substantiate a web client. The `web` platform tag therefore overstates the documented surface. The sequence's “Recipient initiates request” also leaves unclear whether recipient means recipient of the shared username or recipient of the eventual message request.

**Requested correction:** use native-mobile and the catalog's desktop-app platform term, and name the username owner, person receiving the identifier/initiating contact, and person accepting the message request. Preserve the distinction between identity visibility and discoverability, existing-chat merging and phone-number settings. Accepting a request reveals profile identity under the documented conditions; it is not a general anonymity guarantee.

Both corrections were sent to the flow author and root. This review does not edit the cards or assert that corrections have already landed.

## Scoped support and minor clarifications

### `flow-discord-community-onboarding`

Source: [Discord — Community Onboarding FAQ](https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ), “Here is how it works,” “1. Add Default Channels,” “2. Create Customization Questions,” and before-join/post-join question guidance. The page identifies its March 2023 account; the card correctly labels historical freshness.

The source supports answer-driven channels/roles and later revision through Channels & Roles. The card's borrowed community example is clearly an adaptation rather than an observed Discord screen sequence. Minor clarification: label defaults/question mapping as administrator configuration and answering/revising as member actions. Do not imply that all questions occur before entry or that launch-era publishing requirements are universal onboarding principles. Current mobile parity was not established by this documentary check.

### `flow-google-maps-offline`

Source: [Google Maps — Download areas and navigate offline](https://support.google.com/maps/answer/6291838?hl=en), Android guidance: “Select your own map,” “Use offline maps,” and “Update offline maps.”

The card correctly bounds itself to Android instructions and distinguishes prepared coverage, unavailable offline capabilities and refresh. The source requires the route within downloaded coverage and constrains offline transport modes/live information. Preparation also depends on connectivity and sign-in, and availability varies by region. The current card's platform warning and limits avoid claiming cross-platform equivalence or tested navigation. No correction required for its narrow design analogy; include sign-in/connectivity prerequisites if turning the card into an executable checklist.

### `flow-linear-triage-decisions`

Source: [Linear — Triage](https://linear.app/docs/triage), “Create issues,” “Take actions,” and automation sections.

The documented action model supports acceptance to a team default, cancellation on decline/duplicate resolution, and snooze returning on time or earlier activity. Template overrides qualify how items enter triage. The card retains these distinctions and explicitly excludes paid automation/AI suggestions; it does not suggest that those features are required for the analogy. Its operational adaptation is a teaching proposal, not a claim that Linear has volunteer-application screens. No correction required within this scope.

### `flow-duolingo-guided-path`

Source: [Duolingo — Introducing the new Duolingo learning path](https://blog.duolingo.com/new-duolingo-home-screen-design/), “Quick overview,” completed-level review FAQ, guidebooks/practice explanation, return-to-current-position answer and progress-transfer FAQ.

The article supports a guided next step alongside review/orientation and describes a 2022 migration. The card correctly calls this historical product-team rationale rather than a current app specification or isolated causal result. Guidebook availability is course-dependent and Practice Hub is described as a Super feature; these should remain explicit if a later adaptation expands the short “Use guidebooks/practice” receipt into feature-level requirements. No lesson was opened here and no current entitlement claim was independently tested. No blocking correction required for the present historical analogy.

## Review limits and follow-up

- Six cards sampled from eighteen product-flow cards. Other cards were not audited.
- Primary source bodies were opened through the web tool. No browser policy denial occurred in this review; no alternate surface or download workaround was used.
- No live workflow, accessibility, responsive layout, retention, safety, performance or conversion result is established by this review.
- Recheck revised Shopify and Signal metadata, then regenerate/validate the catalog through its owner. Preserve actor and platform boundaries in future flow receipts rather than treating a documentation page as one continuous journey.
