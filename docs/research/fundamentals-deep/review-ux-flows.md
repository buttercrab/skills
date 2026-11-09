# Independent cross-review of UX research

Reviewed 2026-11-07. Scope: six consequential claim groups in `ux-flows.md` and its ledger. The reviewer independently reopened eight underlying papers/pages, reading the relevant methods, results, correction, or first-party account. No experiments or external mutations performed. Only this review file is owned by the reviewer.

## Verdict

The reviewed substantive conclusions are supported at the report's stated scope. One source locator needs correction; one assistance qualifier would make an otherwise accurate example harder to misread. The report appropriately distinguishes observations, practitioner accounts, and candidate instructions. This review does not validate every source or the proposed skill's effectiveness.

## Findings

| Claim group | Assessment | Underlying evidence and implication |
| --- | --- | --- |
| Faulkner and the five-user assumption | Supported | [Original paper](https://link.springer.com/content/pdf/10.3758/BF03195514.pdf), printed pp.380–382, Method, Results, Table 2: 60 people, one specified timesheet task, three experience groups, random subsets compared with the finite observed problem set. The report correctly avoids turning the observed minimum into a population guarantee or a universal replacement sample size. |
| Choice-overload disagreement | Supported | [2010 original](https://scheibehenne.de/ScheibehenneGreifenederTodd2010.pdf), Method and Discussion; [2015 full author-uploaded paper](https://www.researchgate.net/profile/Ulf-Bockenholt/publication/265170803_Choice_Overload_A_Conceptual_Review_and_Meta-Analysis/links/59f1e791a6fdcc1dc7bb07f5/Choice-Overload-A-Conceptual-Review-and-Meta-Analysis.pdf?origin=publication_detail), pp.339–340 and 352–353: source inclusion, observations, moderators, and hierarchical analysis differ. Their conclusions cannot be collapsed into an option-count law. The report's qualification is appropriate. |
| Choice-overload corrigendum | Supported | [Published correction](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2015.07.001), corrections to p.348: separates coefficients from t statistics in three comparisons. It is neither a new experiment nor evidence that the entire conditional conclusion was reversed. The report does not make either overclaim. |
| Figma UI3 reversals | Supported, preserve iteration distinction | [October 2024 first-party account](https://www.figma.com/blog/our-approach-to-designing-ui3/), Docked panels, Blend modes, Properties panel: directly describes fixed-panel restoration, hidden blend-state inspection cost, and returning clip content to a checkbox. Blend-mode icon treatment is described as an early pass, while clip content dropdown was public beta. The account supplies reasoning and reported feedback, not public effect-size evidence. |
| Duolingo path and learning outcomes | Supported; minor locator correction | [Original report](https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_language_read_listen_write_speak_2024.pdf), §1.1, §2.1, §3.1.1, §4.1: content/practice/sequence changed together, selection follows completion, and historical tests differ. The research report correctly rejects layout-only causality. Its evidence-map/ledger locator should identify **§3.1.1 for proficiency comparisons**, rather than §3.2, which covers usage/time. |
| Low-literacy graphical versus voice interfaces | Supported; assistance deserves explicit wording | [2011 original](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ToCHI2711_Medhi.pdf), §4.3–4.4, Table III and footnote: prompting was allowed, results differ for completion versus speed among completers, and speech recognition was Wizard-of-Oz. Case8 mentions assistance, but adding “with experimenter prompting” next to the completion result prevents unassisted-success interpretation. |

The earlier [Medhi ICTD manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/medhi_ictd2006.pdf), §VII, explicitly says its small quantitative results do not achieve statistical significance and presents qualitative hypotheses. The UX report accurately preserves that distinction and does not merge it with the later mobile experiment.

## Details to preserve during synthesis

Faulkner's percentages use the problems observed by the complete sample as their denominator. They cannot describe unknown defects in a new product. The review did not independently execute the sampling or audit raw data, and the paper does not fully specify a modern bootstrap implementation.

For the 2010 choice analysis, seven experiments with unavailable detailed results and only approximate negligible-effect indices were assigned zero. For the 2015 analysis, peer-reviewed-only inclusion and nesting differ. Those are interpretive constraints, not proof that either team manipulated results. No reanalysis or publication-bias correction was performed here.

Duolingo's Table1 counts test takers who completed at least one skill; Table 2's per-skill and overall denominators differ. “257 selected learners” is accurate, but avoid rewriting it as “257 complete four-skill assessments.” Its abstract's stronger rhetoric should not replace the report's explicit comparison caveats.

The Medhi example is useful precisely because speed among successful users and inclusive completion can disagree. It does not establish modern production voice-recognition performance, a universal preference for graphical interfaces, or unassisted success for all lower-literacy populations.

## Unknowns and follow-through

- Original raw datasets, analysis scripts, and independent replications were not audited in this cross-review.
- Figma's internal measurements and Duolingo's unobserved attrition remain unavailable; both are acknowledged limits, not demonstrated false claims.
- The source-locator correction and assistance clarification were sent to the UX author and coordinator. The UX author reports both amendments completed under coordinator authorization; this reviewer did not edit those files.
- Candidate instructions and evaluations remain proposals. Source-supported reasoning does not demonstrate that injecting those instructions improves an agent's decisions.
