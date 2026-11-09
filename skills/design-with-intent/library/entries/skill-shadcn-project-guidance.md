---
{
  "id": "skill-shadcn-project-guidance",
  "kind": "skill",
  "title": "shadcn/ui project and component guidance",
  "summary": "Project-aware component composition, registry search and design-system implementation instructions for an actual shadcn/ui codebase.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "implement",
      "compose",
      "maintain"
    ],
    "contexts": [
      "components",
      "design-system",
      "chat",
      "forms"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/shadcn-ui/ui/blob/42f3bb63b46a69e52a24bd005cdc9ec15ba7a7b9/skills/shadcn/SKILL.md",
      "title": "skills/shadcn/SKILL.md",
      "locator": "Project context; principles; rules; CLI; references",
      "revision": "42f3bb63b46a69e52a24bd005cdc9ec15ba7a7b9"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned skill instructions and root license inspected; no CLI commands or project modifications executed."
  },
  "reuse": "Root LICENSE.md inspected as MIT. Only original annotation and source links provided; preserve applicable terms when copying components.",
  "related": [
    "tool-storybook",
    "skill-fixing-accessibility"
  ]
}
---

# shadcn/ui project and component guidance

## When to use

Select this when the project already uses shadcn/ui or the user explicitly requests that ecosystem. It is an implementation/capability match: existing components, presets and base primitives constrain how to build the selected design coherently.

## What to inspect

Read the project-context section, composition/form rules and the references relevant to the installed base. The file distinguishes Radix/Base/React Aria variants and supplies registry inspection and dry-run/diff commands. Confirm versions and local component modifications before transferring examples.

## What to borrow and adapt

Borrow source-aware component reuse, semantic roles and reviewing upstream differences before replacement. A dialog or input group should preserve the appropriate component contract rather than imitate its screenshot with unrelated markup. A design-system page can demonstrate actual states and edge cases instead of being merely a gallery of default components.

## Mismatches and limits

The CLI adds source files and presets can alter a project; catalog selection does not authorize those actions or overwriting local work. Its card, spacing and component rules are ecosystem conventions, not general design laws. This resource does not decide whether a familiar shadcn layout fits the user’s desired visual direction. No CLI invocation, installation or generated UI was performed here.
