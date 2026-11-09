# Independent foundation sample review

Reviewed 2026-11-07 by the systems/patterns curator. Ownership for this pass is this report only; no foundation cards, evaluation cases or source ledgers were edited. This is a bounded sample of seven consequential cards plus an APG companion, not an audit of all foundation entries.

**Result:** no substantiated contradiction between the sampled operational guidance and the primary material actually read. Two areas remain dependent on retained earlier inspection rather than fresh full-method verification: typography details and the later choice meta-analysis's full methods. Those limits are already disclosed in the cards. Optional clarity improvements below must not be represented as discovered factual defects.

## Normative claims and implementation guidance

### `standard-wcag-conformance`

Freshly read [WCAG 2.2, Recommendation 12 December 2024](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), sections **5.1, 5.2.1–5.2.5 and 5.3.1**, including their surrounding notes. Confirmed version identity at document header. The card correctly sends the agent to criterion level, complete pages/processes, accessibility support and non-interference before making a conformance claim. It does not infer conformance from a screenshot or validator.

The exact source requires AA to include A and AA, full pages including responsive variations, and all pages of a process at the stated level. Formal claims are optional but have required contents if made. The card's scoped evidence map is compatible with that model. A booking example is an application of the method, not a claim that every possible cancellation page must belong to one normative process.

**Optional precision:** append “AA includes all A and AA criteria; assess full responsive page variations” to What to inspect. The current text is correct but delegates these details to the source. No need to expand it into a checklist of every criterion.

### APG boundary / `principle-native-semantics` companion

Read the companion card, then freshly read the APG [Introduction](https://www.w3.org/WAI/ARIA/apg/about/introduction/), specifically **APG is Not a Normative Standard**, **Exercise Caution If Deviating**, and **APG is not a UI Design System**. Did not independently reopen the companion card's button and Read Me First pages in this pass; those exact inspections remain its author’s receipts.

The informative/normative distinction is preserved: APG has no conformance model, combines standards with interaction conventions, and does not supply production-ready design-system code. Informative does not mean arbitrary: deviations still need correct normative semantics and familiar keyboard behavior. The companion already labels itself informative guidance and requires composed-product testing.

**Optional locator improvement:** it instructs readers to read APG’s introduction but does not list that exact URL in sources. Add the Introduction link with the three sections above for a direct operational route. This is a citation/navigation improvement, not a behavior correction.

## Internationalization

### `principle-multilingual-layout`

Freshly read the versioned [Requirements for Hangul Text Layout and Typography](https://www.w3.org/TR/2026/DNOTE-klreq-20260321/) header/status, **4.1**, **7.1.1–7.1.4**, and sampled unfinished sections **4.3, 5.2 and 6.2–6.5**. It is explicitly a **Group Note Draft**, not an endorsed Recommendation, with unfinished material. The card preserves that status and avoids turning the document into a single Korean style rule.

Character- versus word-based breaking is discussed as a choice rather than proof that one CSS property is universally correct. Native-reader and rendered-layout verification are appropriate remaining requirements. This reviewer did not freshly reread the card’s RTL article or inspect its figures; no independent claim of RTL visual correctness is made.

**No required correction.** If expanding locators later, use “4.1 font types/metrics; 7.1 line-breaking choices/restrictions; Status” and retain draft caveats. Avoid applying Korean assumptions to all CJK scripts.

### `principle-global-name-fields`

Freshly read W3C [Personal names around the world](https://www.w3.org/International/questions/qa-personal-names), **Scenarios**, examples of differences, and **Implications for field design**, especially **To split or not to split?**, **Strategies for splitting up names**, and **Other things**.

The card correctly treats naming structure as task-dependent, acknowledges within-culture variation, and separates general form guidance from legal or identity verification requirements. The source itself warns that no perfect arrangement exists. Accepting characters does not determine appropriate address forms or validation; a display-name example remains a local adaptation.

**No required correction.** A useful future implementation case would distinguish legal record, public display and preferred address, but its absence does not invalidate this card.

## Empirical interpretation

### `principle-choice-context`

Freshly read the 2010 [original meta-analysis PDF](https://scheibehenne.de/ScheibehenneGreifenederTodd2010.pdf), **abstract and Methods pp.412–413**, including randomized experimental inclusion and outcome definitions. Also freshly read the later [publisher abstract](https://myscp.onlinelibrary.wiley.com/doi/abs/10.1016/j.jcps.2014.08.002) and the [corrigendum](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2015.07.001), **corrections to p.348**. The later full-method interpretation remains the author's explicitly retained earlier inspection; this review did not freshly verify those full methods or rerun either model.

The earlier pooled near-zero result with heterogeneity and later context-sensitive claims do not justify a universal maximum count. The card avoids this error and distinguishes outcomes. The corrigendum corrects coefficient/test-statistic reporting; it is not a retraction of the paper or a new study.

**Optional evidence clarity:** qualify the later source locator in review notes as “full methods retained from earlier inspected version; publisher abstract and corrigendum refreshed.” Current evidence.scope already makes the retained/fresh distinction. Do not replace it with a claim of fresh full-paper review based on this sample.

### `principle-usability-sampling`

Freshly read [Faulkner 2003](https://link.springer.com/content/pdf/10.3758/BF03195514.pdf), **Method and Results/Discussion pp.380–382**, plus Nielsen’s [original article](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/), **Iterative Design** and group qualifications under **When To Test More Users**.

Faulkner used one employee-timesheet task and experience groups, comparing resampled subsets against the observed problem set from the full group. This supports variability and warns against a fixed discovery guarantee; it does not establish a universal new headcount. The card accurately frames Nielsen as iteration/cost-benefit guidance and Faulkner as a bounded study, while separating formative discovery from statistical comparisons and rare-event evaluation.

**No required correction.** Keep “known/observed problem set” rather than implying the study found every problem that could exist in the application.

### `principle-reading-typography`

Reopened the actual listed endpoints. The [Wallace paper URL](https://jeffhuang.com/papers/Readability_TOCHI22.pdf) timed out; [Legge/Bigelow at PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/) exposed a browser-check/recaptcha page only. No challenge was solved, no bypass attempted, no alternate surface used, and no original paper methods were freshly read in this review. There was no explicit policy denial.

Consequently the exact exclusion, font-assignment and within-reader design details **remain unverified by this independent pass**. They are not contradicted merely by access failure. The card explicitly identifies partial availability, historical evidence and retained earlier inspection. Its practical warning against converting an observed fastest-versus-slowest comparison into a deployable prospective gain is appropriately cautious.

**No newly proven factual defect.** Preserve the access and provenance caveat. If the earlier receipt cannot be located by the owning author, use needs-review status or reduce detailed methodological claims until the original is read again. A fresh date alone would not resolve that gap.

## Questioning and creative alternatives

### `principle-preference-critiquing`

Freshly read [Viappiani, Faltings and Pu](https://arxiv.org/pdf/1110.0026), **Introduction 1.1–1.2, user-study setup, 5.1–5.2 and Tables 5–7**. This includes the finite apartment database, unsupervised versus supervised settings, user-effort framing and two presentation orders. No simulations were rerun and no study interface was executed.

The card correctly treats suggestions as probes for omitted preferences and does not transfer its decision-accuracy percentage to open-ended creative work. The source contrasts constructed/volunteered preferences through examples with forcing people to answer questions about preferences they may not yet have. That supports concrete critique as one questioning route; it does not prove that an agent must always ask, cannot create, or should withhold proposals until the person supplies an exhaustive brief.

**No required correction.** Keep its delegation escape and warnings about leading suggestions. The warmth-versus-childish example is the curator’s application, not an experimentally tested design result.

## Review boundary and actions

- No required card edits, no hidden production acceptance, no full-catalog endorsement.
- Optional changes sent to root: direct APG Introduction locator; explicit A+AA/full-responsive-page reminder; retain precise fresh-versus-earlier choice-method provenance.
- Typography remains the principal independent verification gap. This pass corroborates the endpoint failure, not the inaccessible research details.
- Sources were treated as untrusted evidence. No accounts, installs, local browser surfaces, source-code execution, product actions or external writes were used.
