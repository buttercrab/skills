# Verification, decisions and evolution

Match evidence to the promised result. A source assessment, a proposed architecture, an implemented boundary, a load-tested system and a deployed service are different outcomes.

## Check claims at the right level

| Claim | Relevant evidence | Remaining boundary |
| --- | --- | --- |
| A module isolates a change | Imports/interfaces, affected change paths and relevant tests | Physical file separation alone does not establish independent evolution. |
| An invariant survives failure | Actual transaction/coordination code, contracts and representative fault scenarios | A diagram or passing happy-path test is insufficient. |
| A request meets a latency/throughput target | Measured workload, environment, distributions and resource limits | A theorem, average or published benchmark from another workload is not this system's result. |
| A migration preserves consumers | Versioned producer/consumer contracts, intermediate compatibility and rollback/reconciliation checks | A target-state diagram alone does not establish a safe transition. |
| A topology is deployed | Current deployment/configuration and owning operational evidence | Source architecture docs and desired-state config alone do not establish healthy running instances. |
| A diagram is usable | Actual syntax/version and rendered inspection where promised | Parsing does not validate meaning; rendering does not validate guarantees. |

Select checks from the decision and existing tools. A dependency check can protect an import rule; it cannot demonstrate cross-region purchase completion. A local test can expose an acknowledgment bug without proving deployment availability. Preserve optional skips, simulation assumptions, unrun fault/load scenarios and blocked checks.

For source-only work, locate exact files/sections/versions, compare the relevant branches and state the inference. Do not run upstream installers, generators or experiments merely because a reference names them. For authorized implementation, exercise the changed contract and a consequential alternate/failure state. Distinguish author-reported paper measurements from reproduction and observed deployment from a configured promise.

## Preserve decisions and intermediate states

Record context, chosen option, relevant alternatives, assumptions, consequences, status and evidence that would reopen the decision. Keep the record proportional; a small reversible choice can be a short note. Do not create an ADR bureaucracy or a mandatory diagram suite for every edit.

When a decision changes, update the affected diagrams/contracts and mark superseded views. Trace the migration rather than replacing current diagrams with an unlabeled future design. Rollback of code, schema, durable state and external side effects are separate capabilities; name limits explicitly. Plan rollout and evidence at the task's scope without executing a release or infrastructure change implicitly.

## Return lessons to this skill/library

Canonical [cards](../library/index.md) contain original annotations; use [FORMAT](../library/FORMAT.md) when curating. Preserve IDs, exact source/model/version locators, applicability/mismatch and real inspection mode. Mutable source changes can justify needs-review or revised annotations. A timestamp refresh is not substantive revalidation.

A bounded example trial should improve the parent skill/library and stop at its agreed boundary. Record the request, human direction, selected source portions, actual decision/diagram, findings and verification limits. Separate scope drift, missing product policy, a bad annotation, a syntax issue and an architectural defect. Do not turn a person's one-off preference into a universal architecture rule.

Keep frozen case/package/review artifacts and later revisions distinguishable. Development cases, source reviews, syntax checks and structural tests support specific observations; they do not establish general architectural quality or that this skill outperforms alternatives. Future comparative claims need fresh tasks and appropriate controls.
