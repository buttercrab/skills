---
{
  "id": "diagram-c4-deployment-mapping",
  "kind": "notation",
  "title": "C4 deployment: map instances to an explicit environment",
  "summary": "Separate logical application/store roles from their runtime instances, infrastructure nodes and environment-specific placement.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "diagram",
      "trace",
      "document"
    ],
    "contexts": [
      "deployment-topology",
      "environment-boundaries"
    ],
    "qualities": [
      "availability",
      "operability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://c4model.com/diagrams/deployment",
      "title": "C4 Deployment diagram",
      "locator": "Environment scope, deployment nodes, instances and infrastructure",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.arc42.org/section-7/",
      "title": "arc42 Deployment view",
      "locator": "Infrastructure mapping, relevant environments, motivation and mapping table",
      "revision": "Mutable official documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh official documentation text and selected source examples inspected. No source diagram image was visually viewed, and no parser, renderer, installed tool, generated output or system interaction was executed in this curation."
  },
  "reuse": "Original annotations and source links only. No upstream images, manuals, implementations or packages redistributed; source-specific asset reuse rights must be checked before copying.",
  "related": [
    "system-raft-host-integration",
    "diagram-c4-context-container"
  ]
}
---

# C4 deployment: map instances to an explicit environment

## When to use

Use for questions about placement, failure domains or who operates an infrastructure boundary. It helps when a logical worker or database icon has been mistaken for a complete production topology.

## What to inspect

C4 deployment documentation maps software-system/container instances onto potentially nested execution nodes in one environment. Supporting infrastructure can include routing or name-resolution elements. arc42 pairs infrastructure with explicit software mapping and reasons for the deployment, permitting diagrams and tables.

## Diagram implications

Name the environment and observation date/revision. Distinguish an application role from its instance count and deployment node; avoid implying a replica or standby from an unlabeled extra icon. Show only network, storage or isolation boundaries needed for the question. Label uncertain placement, proposed topology and external ownership. Keep development and production facts separate even when they share component names.

## What to borrow and adapt

For a service with one worker and two independently managed data stores, use a small mapping table alongside the view to explain owners and evidence sources. If the question is recovery, follow the relevant failure domain through routing and state rather than drawing every cloud product. A single-process desktop app can often use a much smaller host/dependency view.

## Mismatches and limits

A deployment view is an authored model, not discovery or a health check. Two replicas do not alone establish failover, quorum, independent power or an availability target. These recommendations do not authorize infrastructure changes or require cloud deployment. No actual environment, diagram image, deployment tool or failover interaction was inspected.
