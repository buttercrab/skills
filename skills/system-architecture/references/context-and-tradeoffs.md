# Context, consequential questions and architectural tradeoffs

Use this when a design request lacks its operating conditions or when multiple plausible architectures solve different problems. Do not turn the table into a mandatory questionnaire.

| Decision input | Inspect first | Ask only what remains consequential |
| --- | --- | --- |
| Behavior and invariant | Contracts, operation paths, known incidents and data ownership | What outcome must never happen, and what degraded result is acceptable? |
| Workload | Available measurements, data sizes, concurrency and growth records | Which scenario matters and what growth/latency assumptions should guide a proposal? |
| Deployment and operations | Current configuration/topology, permitted dependencies, ownership | Who will operate added components and what operating cost can the team sustain? |
| State and compatibility | Authoritative stores, transaction boundaries, consumers, API/event versions | Which stale/duplicate/partial observations are acceptable, and what must remain compatible? |
| Evolution | Actual change pressure, migration options and constraints | Which capability must change independently, and how much transition risk is acceptable? |

Separate a business rule from its current implementation. A user can know the cost of duplicate fulfillment without choosing a queue technology. A source tree can reveal current calls but not whether a latency target is negotiable. Do not ask people to invent an answer to a discoverable technical fact.

Make quality requirements operational: a named stimulus, environment, affected operation/state, required response and measure if supplied. “Reliable,” “scalable” and “clean” alone do not select a design. If measurements or a policy are absent, use an explicit conditional recommendation or a labeled provisional model; do not add precise invented targets.

## Compare under the same constraints

For each serious option, identify the invariant it can enforce, state/coordination ownership, normal/failure path, operational burden, compatibility/migration cost and unresolved evidence. Retain meaningful alternatives without building every one. Existing in-process boundaries or a single deployment are valid candidates. Distribution can support independent deployment or fault/resource isolation while adding partial failures, consistency and operations work.

A directory/module can hide a change-prone decision without being a service. A semantic/domain boundary can be useful without a process boundary. Conversely, a single deployment does not guarantee that internal modules remain independent. Compare actual interfaces and coordination needs rather than declaring either form inherently superior.

Read original arguments with their stated uncertainty. A conceptual design argument, a formal impossibility proof, an author's system report and a controlled experiment support different claims. Preserve disagreement about assumptions instead of selecting whichever slogan supports a preferred pattern. Use the [library](../library/index.md) to find the relevant primary portions and contrasting cases.

## Compact decision record

A useful record can be a few paragraphs: context/decision question, chosen mechanism, alternatives and decisive reason, consequences/assumptions, status and evidence that would reopen it. Keep accepted, proposed, superseded and historical decisions distinguishable. A decision record is not proof the design was deployed or remains current.

When feedback arrives, revise the affected choice and corresponding diagrams. If an unknown-field policy, offline requirement or operating budget invalidates a provisional architecture, retire that branch rather than asking the person to choose between obsolete technology options. A full brief or explicit delegation does not need another style vote.
