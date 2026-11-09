---
{
  "id": "foundation-information-hiding",
  "kind": "foundation",
  "title": "Information hiding: own a changeable decision",
  "summary": "Choose module boundaries around protected decisions rather than processing stages or directory names.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "compare"
    ],
    "contexts": [
      "module-boundaries",
      "change-scenarios"
    ],
    "qualities": [
      "evolvability",
      "understandability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf",
      "title": "Parnas: On the Criteria To Be Used in Decomposing Systems into Modules",
      "locator": "pp.1054–1057: responsibility assignment, KWIC alternatives, The Criteria, Efficiency and Implementation",
      "revision": "CACM 15(12), 1972"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh selected original-paper model, alternatives and overhead sections read as text. No implementation, experiment or visual figure inspection."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "pattern-ports-and-adapters",
    "system-rust-analyzer-derived-state"
  ]
}
---

# Information hiding: own a changeable decision

## When to use

Use when a proposed extraction adds layers without identifying the change each boundary contains.

## What to inspect

Read the two KWIC decompositions, responsibility definition, change comparisons and implementation-overhead discussion. This is an illustrative design argument, not a controlled comparison across products.

## What to borrow and adapt

Our application: a report exporter may own delimiter/encoding choices behind one interface while keeping its caller in the same process. Compare changing that representation with changing processing order; ask which callers must change. A separate service is not implied.

## Diagram implications

Show responsibility and allowed dependencies separately from runtime sequence. Label the decision hidden by a boundary; a phase arrow is not evidence of information hiding.

## Mismatches and limits

Do not abstract every speculative future variation. Indirection has implementation and navigation cost. The paper discusses efficiency explicitly; it does not prescribe a contemporary framework or prove that its example wins for this workload.
