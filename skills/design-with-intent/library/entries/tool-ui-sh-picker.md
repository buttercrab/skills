---
{
  "id": "tool-ui-sh-picker",
  "kind": "tool",
  "title": "ui.sh ideas picker (optional local workflow)",
  "summary": "An implemented-option comparison and cleanup mechanism whose local skill excludes generating visual directions.",
  "status": "curated",
  "availability": "local-only",
  "facets": {
    "tasks": [
      "compare",
      "prototype",
      "select"
    ],
    "contexts": [
      "components",
      "collaboration",
      "visual-variants"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "local:ui-sh/ideas/SKILL.md",
      "title": "User-supplied ui.sh ideas skill",
      "locator": "Activation; picker attributes; framework injection; selection; cleanup",
      "revision": "installed/user-supplied snapshot 2026-11-07; upstream version unknown"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "unknown",
    "scope": "User-supplied/installed ideas instructions inspected locally. Exact upstream/license, hosted script and picker behavior unverified."
  },
  "reuse": "Local provenance/license unresolved. Original annotation and optional local identifier only; no skill or hosted script copied.",
  "related": [
    "skill-ui-sh-design",
    "tool-penpot"
  ]
}
---

# ui.sh ideas picker (optional local workflow)

## When to use

Select this only when the local ideas skill is available and the human needs to compare actual implemented variants in a browser. It is a mechanism for a specific decision point after alternatives have been designed, not a source of the alternatives or design principles.

## What to inspect

Read its activation exclusions, wrapper/option attributes, framework-specific injection and final cleanup lifecycle. Inspect the project’s existing comparison artifacts first. Its external picker script and browser availability are dependencies whose current behavior was not tested here.

## What to borrow and adapt

Borrow named decision points, one visible option at a time, and preserving the current design as an explicit alternative. Make option labels match the conversation, allow a different answer, and remove rejected code and scaffolding after selection. Compare equivalent content/fidelity so an artificially polished option does not determine the person’s preference.

## Mismatches and limits

The exact installed source and license are local/unversioned; this card is optional and ships no copy of that skill or script. Selecting it does not authorize injecting an external dependency or circumventing browser/CSP restrictions. If permitted preview cannot run, clearly labeled descriptions or allowed artifacts can support discussion at their narrower evidence scope. No picker, browser script or comparison was executed during curation.
