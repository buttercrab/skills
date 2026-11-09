---
{
  "id": "repo-small-testify",
  "kind": "repository",
  "title": "Testify: assertions as source, fatal wrappers as generated consumers",
  "summary": "A Go testing module connects authored assertion semantics and templates to generated require wrappers, with CI explicitly checking generation drift before race-enabled tests.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "generated-files",
      "test",
      "maintain-api",
      "navigate"
    ],
    "contexts": [
      "library",
      "testing-tools",
      "code-generation",
      "public-api"
    ],
    "languages": [
      "go",
      "shell"
    ],
    "scale": [
      "multi-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/CONTRIBUTING.md",
      "title": "stretchr/testify: CONTRIBUTING.md",
      "locator": "API usefulness, maintenance expectations and review context",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/go.mod",
      "title": "stretchr/testify: go.mod",
      "locator": "module identity and supported-version comment",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/assert/assertions.go",
      "title": "stretchr/testify: assert/assertions.go",
      "locator": "Equal behavior and argument validation",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/assert/assertions_test.go",
      "title": "stretchr/testify: assert/assertions_test.go",
      "locator": "TestEqual table of semantic cases",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/require/requirements.go",
      "title": "stretchr/testify: require/requirements.go",
      "locator": "go:generate directive",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/require/require.go.tmpl",
      "title": "stretchr/testify: require/require.go.tmpl",
      "locator": "fatal wrapper template",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/require/require.go",
      "title": "stretchr/testify: require/require.go",
      "locator": "generated header and Equal forwarding",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/_codegen/main.go",
      "title": "stretchr/testify: _codegen/main.go",
      "locator": "source parsing and generation entrypoint",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/.ci.gogenerate.sh",
      "title": "stretchr/testify: .ci.gogenerate.sh",
      "locator": "generation and git-diff failure condition",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
    },
    {
      "url": "https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/.github/workflows/main.yml",
      "title": "stretchr/testify: .github/workflows/main.yml",
      "locator": "generation, format, vet and race-test routes",
      "revision": "87a7b9d57689f6579db2da795ab8deeab29cb724"
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
    "quality-generated-source-authority",
    "quality-go-module-workspace-boundaries"
  ]
}
---

# Testify: assertions as source, fatal wrappers as generated consumers

## When to use

Use when a public API has several mechanically related façades and a tempting quick fix would edit a generated wrapper. It also helps distinguish an authored function’s semantic tests from the checks needed to keep its generated consumers synchronized.

## What to inspect

The contribution guide asks whether proposed API expansion serves concrete users and preserves predictable behavior. assert.Equal owns the comparison result; require.Equal is generated and delegates to assert.Equal before failing the test immediately on false. A directive in require/requirements.go calls the code generator with require.go.tmpl. The generator parses source and renders functions; .ci.gogenerate.sh runs generation then fails on a resulting diff, and the primary CI job invokes that script before other checks.

## Change path

Trigger: change an assertion signature or failure behavior exposed through both assert and require. Start at assert/assertions.go and its TestEqual scenarios. Follow require/requirements.go’s directive through _codegen/main.go and require/require.go.tmpl to require/require.go rather than hand-editing the derived file. Run the owning project’s appropriate generation/semantic checks only when executing a real change is authorized; here their wiring was inspected. The workflow separates the main generation/format/vet/race route from tests on older Go versions.

## What to borrow and adapt

Draw an authority map that includes authored source, templates and generated façades. A short wrapper can still be an important consumer of a changed public contract. Make generation drift detectable as a distinct failure rather than letting a runtime-test pass imply generated files are synchronized. If a small project has no repeated façade surface, hand-written code may be simpler; generation should repay its extra tool/module/validation boundary.

## Mismatches and limits

This is a multi-package testing module, not a deployed service architecture or proof that every assertion library needs code generation. The generator and CI script were read, not run; no working-tree drift, generated output equality or CI result was observed. Local Go-version comments and workflow matrices were inspected without certifying every environment. Upstream review/maintainer rules are not imported as instructions.

