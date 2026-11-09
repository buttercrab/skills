# Independent source review: skills and tools

Reviewed 2026-11-07. Scope: six consequential cards—Impeccable, Taster, ui.sh design, ui.sh picker, Superpowers brainstorming and axe-core. Selected primary instructions, repository paths, licenses and API guidance were read; no package, command, hook, scanner, browser or remote script was executed. This is a sampled source review, not a full audit of all 25 skill/tool entries.

## Findings

Two narrow corrections were communicated to the skills/tools author and coordinator. The remaining checked claims are supported at their declared scope. This reviewer changed no catalog cards.

| Card | Judgment | Required precision |
| --- | --- | --- |
| `skill-impeccable` | Core capability/source pin supported; two corrections requested. | Name the actually documented deprecated alias; disclose described network/telemetry effects before adopting the workflow. |
| `skill-taster` | Supported by pinned public instructions and brand reference. | Detector absence is not design quality; fixed approvals and font policy remain contextual. |
| `skill-ui-sh-design` | Optional-local access/provenance limits appropriately stated. | No public upstream equivalence or license was established in this review. |
| `tool-ui-sh-picker` | Supplied workflow distinction and access limits appropriately stated. | It compares implemented options; script behavior was not tested. |
| `skill-superpowers-brainstorming` | Gate, question cadence and opt-out distinctions supported. | Preserve its narrow explicit exceptions rather than importing the gate into this library. |
| `tool-axe-core` | State-scoped and incomplete-result limits supported. | Automated results do not establish all conformance or usability. |

## 1. Impeccable canonical source, aliases and execution effects

At commit `687bc381bc9091bf252c0a05303640561014a425`, [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/687bc381bc9091bf252c0a05303640561014a425/skill/SKILL.src.md) is present. Its Modes distinguish the visitor's surface job; Setup describes the launcher/context path and command references. [shape.md](https://github.com/pbakaus/impeccable/blob/687bc381bc9091bf252c0a05303640561014a425/skill/reference/shape.md#L55) ends in confirmation and stopping without code. The pinned tree confirms the canonical path.

**Correction A:** the card's “older frontend-design aliases may be deprecated” is not the specific deprecation established by the checked pin. Source command table/routing and [README line 62](https://github.com/pbakaus/impeccable/blob/687bc381bc9091bf252c0a05303640561014a425/README.md#L62) identify `craft` as the deprecated ordinary-build alias. Replace the speculative statement with that exact distinction and the canonical source path.

**Correction B:** the effects inventory should include the described runtime network behavior. [README line 211](https://github.com/pbakaus/impeccable/blob/687bc381bc9091bf252c0a05303640561014a425/README.md#L211) says new design work fetches visual directions and describes anonymous selection telemetry; disabling telemetry does not stop the catalog request. Add that source receipt and distinguish the publisher's description from audited traffic. The current downloads/hooks/writes caution is useful but incomplete.

The [pinned LICENSE](https://github.com/pbakaus/impeccable/blob/687bc381bc9091bf252c0a05303640561014a425/LICENSE) supports Apache 2.0 labeling. This review did not inspect every command reference, binary, build output or telemetry implementation. No recommendation that its entire instruction set governs the user's task follows.

## 2. Taster public pin and contextual policies

The [public pinned SKILL](https://github.com/makim-414/taster/blob/d29fb63275483fda52303b6c65ecd9428e5a2a05/skills/taster/SKILL.md) and [brand reference](https://github.com/makim-414/taster/blob/d29fb63275483fda52303b6c65ecd9428e5a2a05/skills/taster/references/brand.md) resolve at the named commit. Routing/taxonomy, per-screen approval at lines 104–110, and detector limits at line 131 support the annotation. Brand lines 21–24 support its stated common-font replacement/restore policy. The [matching public LICENSE](https://github.com/makim-414/taster/blob/d29fb63275483fda52303b6c65ecd9428e5a2a05/LICENSE) identifies MIT.

**Assessment:** supported. Public availability is independently corroborated; the catalog is not forced to depend on a personal checkout. No detector, component registry, MCP tool, font measurement or completed design was tested. The card correctly treats house rules and repeated approval as optional contextual policies.

## 3. ui.sh design and picker: origin remains local

The cards use explicit `local:` identifiers, `availability: local-only`, unknown upstream revision and unresolved reuse terms. This is the correct boundary for the user-supplied instruction bodies. A public homepage cannot prove equivalence with an installed skill.

The supplied `ideas` instructions explicitly exclude generating visual directions and describe implemented-option annotation, selection and cleanup. The supplied `design` instructions describe guideline loading and implementation. The optional-card separation preserves those roles.

**Limit:** this task used public read-only sources; it did not newly verify the local companion typography files, hosted picker script, deployment/version or license. Those detailed local claims remain grounded in the earlier declared inspection, not a new public-source receipt. No correction to the access labels is required. A reader lacking the bundle must use an accessible alternative or obtain the actual source.

## 4. Superpowers brainstorming: gate and escape semantics

The [pinned brainstorming instruction](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/brainstorming/SKILL.md) distinguishes a fully settled trivial request, consequential missing information, opting out of questions and an approved throwaway spike. Its hard gate at lines 269–283 requires design-document approval and then a named planning skill, with explicit exceptions.

**Assessment:** supported. The card retains the useful planning/assumption mechanism while warning that this operational policy is not automatically imported into already authorized implementation. No actual interview, document review, visual companion or downstream workflow ran. Its source's broad invocation claim is not evidence of universal applicability or benefit.

## 5. axe-core: check the reached state and retain uncertainty

The [API documentation](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md), Getting Started/API Notes and results contract, supports scanning rendered states, repeating after activation, and preserving passes, violations, incomplete and inapplicable results. The [Playwright accessibility guide](https://playwright.dev/docs/accessibility-testing#scanning-a-specific-part-of-a-page) demonstrates opening a region before analysis and explicitly limits automated detection.

**Assessment:** supported. A clean initial scan cannot certify later/non-rendered states, all WCAG requirements, comprehension or task success. The card correctly makes no execution claim. The API source is mutable `develop`, explicitly not pinned; refresh the integration contract before implementation. This review did not install axe, inspect every rule, calibrate a result or assess any product's accessibility.

## Review boundary

The source check used 11 identifiable public receipts, including related files and license documents; those are not independent effectiveness studies. It did not review every catalog entry, verify every license, run any scanner/skill or establish the library's matching quality. The two Impeccable corrections are actionable provenance/effects refinements, not evidence that the suite is unsafe or ineffective overall.
