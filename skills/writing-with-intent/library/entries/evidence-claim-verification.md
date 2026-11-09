---
{
  "id": "evidence-claim-verification",
  "kind": "study",
  "title": "Verify claims against evidence while preserving their context",
  "summary": "FActScore and VeriScore clarify claim-level support without making a metric into an editor.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "verify",
      "report",
      "evaluate"
    ],
    "genres": [
      "research-summary",
      "article",
      "explanation"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "factual-verification",
      "source-coverage",
      "metric-limitations"
    ]
  },
  "sources": [
    {
      "url": "https://aclanthology.org/2023.emnlp-main.741.pdf",
      "title": "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation — Min and colleagues",
      "locator": "§§3.1–3.4; §4.3.2; Limitations",
      "revision": "EMNLP 2023 proceedings, pp. 12076–12100"
    },
    {
      "url": "https://arxiv.org/html/2406.19276v1",
      "title": "VeriScore: Evaluating the factuality of verifiable claims in long-form text generation — Song and colleagues",
      "locator": "§§2.1–2.4, 3.1–3.3; Limitations",
      "revision": "arXiv:2406.19276v1, 2024; claim-extraction evaluation April 2024"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Fresh reading of FActScore definition, biography/Wikipedia scope and result/limit sections; VeriScore extraction comparison, human-verification setup and limitations. No metric was executed."
  },
  "reuse": "Original annotations and links only; no upstream prose, poems, datasets or study materials redistributed.",
  "related": [
    "evidence-entity-coherence",
    "practice-ori-attribution"
  ]
}
---

## When to use

Use for factual articles, explanations and research summaries. Ask what needs external support and what is an attributed opinion, inference, personal experience or fictional premise.

## What to inspect

FActScore measures supported atomic facts against a specified knowledge source; its main studies concern biographies and Wikipedia, not universal truth or completeness. VeriScore addresses mixed factual and nonfactual writing using context-aware extraction. Its claim-extraction comparison used three raters and eight domains; complex claims and search coverage remain limitations.

## What to borrow and adapt

Our application: record the exact claim, source passage, date and support status. Check whether the evidence supports the stated scope and causal strength. Preserve qualifications during decomposition. An unresolved claim needs further evidence, narrower wording or explicit uncertainty; a genuine value judgment needs an argument rather than a fabricated citation.

## Mismatches and limits

FActScore measures precision, not recall: saying less can improve a score without helping the reader. Neither metric is a comprehensive truth oracle or a validated prose-quality measure. Search failure is not proof of falsity. Benchmark agreement does not demonstrate that a particular editorial workflow improves articles. Model standings in these papers are historical.

