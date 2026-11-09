# Independent primary-source review: two AI evidence cards

Reviewed 2026-11-08. Scope is `evidence-bounded-productivity` and `evidence-detector-bias` only. Fresh primary reading; no upstream code, detector submissions, experiments or assessment fixtures. Card files were not edited.

## Bounded productivity

Primary: [author-hosted NBER SI manuscript](https://shakkednoy.com/Noy%20Zhang%20NBER%20SI.pdf). Inspected PDF pp. 1–7 (abstract, Method, Results, Discussion, Limitations), p. 12/Fig. 1 caption and p. 18/Table 1 (PDF page numbers). Exact text locators: Method lines 58–98; takeup/productivity 100–140; interactions 152–173; limitations 220–256; Fig. 1 caption 408–421; Table 1 562–617 in the browser extraction.

Verdict: central percentages, model/date, task boundaries and distinction between observational editing and causal evidence are supported. One denominator qualification should be added: Fig. 1 restricts to the linear/convex incentive groups, approximately 80% of the sample; the fixed-time arm is separate. Therefore the headline effect must not be read as one pooled estimate across every participant/incentive condition.

Recommended insertion: “Headline results concern the variable-time incentive arms; randomized access also had imperfect takeup and control use.” This improves the card’s decision boundary without changing its central claim. Preserve “ratings” rather than treating the percentage as an absolute measure of quality or factual correctness. Do not infer that minimally edited generation is optimal: editing was not randomized.

Access limits: source text and captions read, not figure images, supplementary materials, registry or analysis data. Supplementary robustness is an author-reported claim here, not independently reproduced. The author URL is mutable; the manuscript is identified by its sample/model/content, not an immutable archive hash. No versions were merged. No present-day model or workplace extrapolation was validated.

## Detector bias

Primary: [Liang and colleagues, arXiv:2304.02819v3](https://arxiv.org/html/2304.02819v3), dated 10 July 2023. Inspected Results (lines 33–49), Discussion/limits (51–65), figure captions (114–121), detector list/access date (127–158), generation/filtering protocol (171–216), corpus provenance/statistical method (217–229).

Verdict: no demonstrated material defect. The card correctly identifies the two nonmatched essay corpora and refuses causal language-proficiency inference. It keeps detector outcomes distinct from reader quality and authorship proof. Its historical qualifier is essential: the methods specify March 2023 detector access. Generated-essay filtering and the particular generation model bound the separate rewriting demonstration; the card appropriately avoids universal evasion rates.

Optional locator improvement: include Materials and Methods in source metadata. Keep the rewrite model unspecified unless needed: the source’s Results/Methods and Discussion use inconsistent model labels for the human-essay intervention. This uncertainty does not undermine the card’s deliberately non-model-specific instability claim.

Access limits: paper methods/results read, not archived detector implementations, underlying essays, data/code, current vendor behavior or separate validation of author language status. A detector label supplies no direct measurement of clarity, truth, usefulness or individual provenance. The recommendation to inspect concrete writing defects is the library’s application, not an experimentally tested intervention from this study.
