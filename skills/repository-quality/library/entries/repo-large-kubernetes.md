---
{
  "id": "repo-large-kubernetes",
  "kind": "repository",
  "title": "Kubernetes: one authoritative staging tree, several publication units",
  "summary": "The staging guide, generated workspace and import-verification inputs make source authority and published module boundaries explicit rather than equating repositories with ownership.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "source-authority",
      "module-boundaries",
      "generated-files",
      "distribution"
    ],
    "contexts": [
      "monorepo",
      "multi-module",
      "published-libraries"
    ],
    "languages": [
      "go",
      "shell"
    ],
    "scale": [
      "large-project",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/staging/README.md",
      "title": "kubernetes/kubernetes: staging/README.md",
      "locator": "Authoritative copy, workspace use and repository creation workflow",
      "revision": "ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8"
    },
    {
      "url": "https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/go.work",
      "title": "kubernetes/kubernetes: go.work",
      "locator": "Generated workspace and staged module use entries",
      "revision": "ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8"
    },
    {
      "url": "https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/staging/publishing/import-restrictions.yaml",
      "title": "kubernetes/kubernetes: staging/publishing/import-restrictions.yaml",
      "locator": "Allowed imports and exclusions, first 100 lines",
      "revision": "ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8"
    },
    {
      "url": "https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/hack/verify-imports.sh",
      "title": "kubernetes/kubernetes: hack/verify-imports.sh",
      "locator": "Import-verifier invocation and policy input",
      "revision": "ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned primary source/configuration/documentation and specified diff portions read. No upstream code, generator, test, build, CI, publication or remote mutation executed."
  },
  "reuse": "Original annotations and source links only. No upstream files or media redistributed; project-specific license statements are evidence, not legal advice.",
  "related": [
    "quality-go-module-workspace-boundaries",
    "quality-generated-source-authority"
  ]
}
---

# Kubernetes: one authoritative staging tree, several publication units

## When to use

Use when a monorepo exposes separately distributed libraries or mirrored repositories and contributors might edit the wrong copy. It also helps assess whether module boundaries are represented by executable dependency rules rather than only directory names.

## What to inspect

The staging README says the monorepo staging copy is authoritative and describes published repositories as downstream outputs. It explains local Go workspace and replacement resolution. The inspected `go.work` is marked generated. Import restrictions list allowed dependencies and some test/subtree exceptions; the verification script installs/runs the owning import verifier against that policy file.

The setup workflow also names organizational approvals and published-repository access settings. Those are documentation of the process, not evidence that a specific live repository has current protections.

## Change path

Trigger: change a staged client library or its dependency boundary → owning `staging/src/k8s.io/...` source/module → local workspace resolution → import policy and verifier when the dependency surface changes → separately maintained publishing rules/bot for distribution. The first four relationships were read directly. The publishing-bot implementation, publication job and distributed package were not exercised or fully followed here.

## What to borrow and adapt

Make the authoritative source and output copies obvious to contributors. For generated workspace/module metadata, identify the project's update route before hand-editing it. Dependency allowlists can expose intended boundaries, but exclusions and temporary exceptions are part of the actual policy; do not flatten them into a slogan that all cross-module imports are forbidden.

A smaller multi-package project may need only a workspace manifest, clear release units and a focused import check. Separate repositories are neither inherently more modular nor a requirement for independently published packages.

## Mismatches and limits

No verifier, vendor update, Go test, publishing bot, remote protection inspection or package publication occurred. The workflow's governance and automation cost should not be transplanted into a two-person library. A missing locally inspected publication step is an evidence gap, not proof that staged modules are untested or unsafely published.

