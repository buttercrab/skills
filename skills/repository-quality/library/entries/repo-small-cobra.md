---
{
  "id": "repo-small-cobra",
  "kind": "repository",
  "title": "Cobra: co-located Go tests and commands that do more than their names suggest",
  "summary": "A Go CLI framework makes command/help behavior and regression scenarios easy to pair, while its Make targets reveal dependency-fetch side effects and CI-specific flags.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "navigate",
      "test",
      "maintain-api",
      "check-compatibility"
    ],
    "contexts": [
      "library",
      "cli",
      "co-located-tests",
      "developer-commands"
    ],
    "languages": [
      "go",
      "make"
    ],
    "scale": [
      "single-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/CONTRIBUTING.md",
      "title": "spf13/cobra: CONTRIBUTING.md",
      "locator": "reproduction context and documented test commands",
      "revision": "adbc8813901bba65827259daa8e22ff94ec1f30e"
    },
    {
      "url": "https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/go.mod",
      "title": "spf13/cobra: go.mod",
      "locator": "module/dependency and Go directive",
      "revision": "adbc8813901bba65827259daa8e22ff94ec1f30e"
    },
    {
      "url": "https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/command.go",
      "title": "spf13/cobra: command.go",
      "locator": "ExecuteC and InitDefaultHelpCmd",
      "revision": "adbc8813901bba65827259daa8e22ff94ec1f30e"
    },
    {
      "url": "https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/command_test.go",
      "title": "spf13/cobra: command_test.go",
      "locator": "help command, shadowed flags and unknown-command scenarios",
      "revision": "adbc8813901bba65827259daa8e22ff94ec1f30e"
    },
    {
      "url": "https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/Makefile",
      "title": "spf13/cobra: Makefile",
      "locator": "test/richtest and install_deps",
      "revision": "adbc8813901bba65827259daa8e22ff94ec1f30e"
    },
    {
      "url": "https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/.github/workflows/test.yml",
      "title": "spf13/cobra: .github/workflows/test.yml",
      "locator": "test platforms/toolchains and macOS linker flags",
      "revision": "adbc8813901bba65827259daa8e22ff94ec1f30e"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh primary repository metadata and selected substantive source/configuration/test/documentation sections inspected at the pinned commit. No upstream code, command, CI, build or release was executed."
  },
  "reuse": "Original annotations and primary-source links only; no upstream implementation, images or packages redistributed. License declarations are source facts, not legal advice.",
  "related": [
    "quality-go-module-workspace-boundaries",
    "repo-small-click"
  ]
}
---

# Cobra: co-located Go tests and commands that do more than their names suggest

## When to use

Use for a Go library that serves many independently owned command trees, or when repository cleanup proposes moving tests away from their subject without a maintenance reason. The Make targets also provide a useful check against assuming a command named test is only local validation.

## What to inspect

Command implementation and command_test.go are co-located. ExecuteC initializes default help at execution time, permitting user customization; nearby tests cover root/child help and flag shadowing rather than a single happy path. CONTRIBUTING documents go test and make test. The actual Makefile makes test/richtest depend on install_deps, which calls go get; CI uses richtest and injects platform-sensitive test flags. The module Go directive, lint toolchain and tested interpreter matrix describe different scopes.

## Change path

Trigger: change inherited help flags or help-command initialization. Follow command.go InitDefaultHelpCmd and ExecuteC into command_test.go’s parent/child help and shadowing cases. Inspect Makefile targets before choosing the validation route: test and richtest fetch dependencies first, while CI also installs tools and supplies GO_TEST_FLAGS for selected macOS/Go combinations. A local direct go test and the whole CI job therefore make different environment promises. None was run for this card.

## What to borrow and adapt

Prefer navigable ownership and scenario adjacency over a universal tests-directory rule. Read developer command definitions, including prerequisite targets and environment flags, before describing what they validate or mutate. Documentation can expose an easy entry route while configuration supplies the exact path; report any difference with scope rather than calling either name inherently wrong. Apply only the compatibility dimensions your actual consumers need.

## Mismatches and limits

The old Go directive does not by itself prove that every package dependency or CI job supports that version. A command tree framework’s compatibility cases are not a required template for a one-command program. Governance and contribution terms remain local. No dependencies were fetched, test command executed, CLI interaction tried, CI run observed or release built; these are inspected intended mechanics.

