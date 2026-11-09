---
{
  "id": "principle-navigation-learning",
  "kind": "foundation",
  "title": "Navigation: scent, depth and learned location",
  "summary": "Compare navigation structures using realistic retrieval and repeated-use tasks rather than a fixed item-count rule.",
  "status": "curated",
  "availability": "partial",
  "facets": {
    "tasks": [
      "navigate",
      "information-architecture",
      "retrieve"
    ],
    "contexts": [
      "catalogs",
      "expert-work",
      "novice-users"
    ],
    "platforms": [
      "web",
      "desktop"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/chi98_webdesign.pdf",
      "title": "Web Page Design: Implications of Memory, Structure and Scent for Information Retrieval",
      "locator": "Methods, results and discussion, pp.27–30",
      "revision": "Larson and Czerwinski, CHI 1998"
    },
    {
      "url": "https://www.csse.canterbury.ac.nz/andrew.cockburn/papers/paper191-cockburn.pdf",
      "title": "A Predictive Model of Menu Performance",
      "locator": "Model; calibration pp.630–632; real-design evaluation",
      "revision": "Cockburn, Gutwin and Greenberg, CHI 2007"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Original hierarchy paper refreshed; menu-model methods preserved from same-day inspected research. Current Canterbury endpoint timed out. No modern navigation experiment performed."
  },
  "reuse": "Original annotation and links to original material; no paper, illustrations or third-party software redistributed. Check source-specific terms before substantial reproduction.",
  "related": [
    "principle-choice-context",
    "principle-usability-sampling"
  ]
}
---

# Navigation: scent, depth and learned location

## When to use

Use when deciding between broad menus and deeper hierarchy, changing the location of frequent actions, or reorganizing a large reference catalog.

## What to inspect

Read the hierarchy experiment's category construction and results, then the menu model's treatment of visual search, pointing and learning. The former used a bounded encyclopedia retrieval task; the latter's calibration population was narrow. Keep the study contexts attached to their claims.

## What to borrow and adapt

Treat navigation as finding something under particular knowledge and frequency conditions. Compare known-item retrieval with exploratory browsing. Inspect whether labels provide useful clues, whether grouping matches the task, and whether repeated use benefits from stable locations.

For an expert issue tracker, keeping a learned action location may matter more than moving the most-used command to the first position. A newcomer may instead need explicit categories and examples.

## Mismatches and limits

Neither source yields a universal menu length or maximum depth. Faster performance on an artificial hierarchy does not establish the best structure for a content-rich mobile product. Adding levels to fit a remembered “seven items” slogan can increase work. Changing everything to a flat menu can also remove useful grouping. Source access is currently partial; reopen the menu model before using its exact constants.
