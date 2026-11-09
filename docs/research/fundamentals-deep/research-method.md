# Deep research method and boundaries

Started 2026-11-07, Asia/Seoul. The user explicitly requested substantially deeper research after the initial survey. This directory contains research, not installed skills or a claim of validated skill effectiveness.

## Questions

1. Which principles change good decisions across contexts, and which are house styles or situational defaults?
2. What do original studies, real artifacts, and first-party failures actually establish?
3. Which competing approaches remain reasonable under different constraints?
4. What specific instructions, worked examples, and checks could improve an agent's work?
5. How should the eventual library evolve without accumulating contradictory or irrelevant rules?

## Independent research lanes

| Lane | Investigation |
| --- | --- |
| UX and flows | Journeys, information architecture, interaction models, research methods, state and recovery, varied users/tasks. |
| Visual design | Composition, typography, color, motion, density, accessibility, responsiveness, contrasting design systems and actual skills. |
| Repositories | Maintenance boundaries, contributor routes, executable conventions, documentation, review, contrasting commit-pinned repositories. |
| Architecture | Original principles, tradeoffs, failure semantics, useful diagrams, code-backed architectural case studies. |
| Writing | Argument, explanation, narrative, editing, reader purpose, authorial voice, empirical AI-writing evidence. |
| Verification | Oracles, debugging, testing, performance, security/reliability, first-party incident chains. |
| Skills and evaluation | Actual skill libraries, public empirical skill studies, activation/composition, behavioral and artifact evaluation. |
| Knowledge synthesis | Learning from examples, transfer limits, evidence appraisal, research-to-instruction decisions, maintenance. |

The first seven lanes use separate subagents. The coordinator owns cross-lane synthesis and knowledge-synthesis research. File ownership is disjoint; existing skills remain untouched.

## Search and selection

Each lane records query families, citation trails, included/excluded source types, and consequential access failures. Prefer original papers, normative standards, first-party documentation and incidents, actual source/configuration files, and original authors' practice. A well-known title or large star count is a discovery lead, not evidence of effectiveness.

Go beyond a single publisher, aesthetic, ecosystem, or project size. Investigate competing advice and the original methods behind memorable slogans. Read consequential methods/results/limitations or implementation branches; opening an abstract alone does not qualify as inspecting the underlying study. Several sources should support detailed decision cases, not just one-line principles.

This investigation uses iterative, purposive sampling and citation following. It is not a registered systematic review, complete search of scholarly databases, or census of the internet. Broad coverage and diminishing returns do not establish exhaustiveness.

## Evidence records

Each lane writes a report and a JSONL source registry. Records identify the work, inspected URL, access date, source family, evidence type, locator, narrow claim, applicable context, limitations, and revision when known. Status distinguishes `inspected`, `partial`, `inaccessible`, and `discovery-only`. `Inspected` means substantive relevant content was examined; it does not mean every page of a book or every source file was read. Reports should identify selected-section boundaries.

Source IDs are lane-specific (UX, VIS, REP, ARC, WRI, VER, SKI, KNO). Duplicate URLs and aliases are reconciled in the combined index, but multiple records may inspect different parts of one work. Counts must distinguish records, distinct URLs, underlying works, source families, and access status. A mirror, paper abstract, HTML full text, and PDF may represent one work.

Keep source-derived wording concise and original; do not republish manuals, essays, proprietary assets, or full papers. Track license and attribution where future reuse of code, assets, or substantial adapted content is contemplated. A publicly accessible file is not automatically permission to redistribute it.

## Claim discipline

- A standard establishes a requirement within its scope and conformance level; explanatory guidance is not identical to normative text.
- A design-system rule establishes that system's convention, not a universal aesthetic law.
- An experiment establishes results for its sampled people/models/tasks and procedures; statistical significance is not practical importance or proof of generality.
- Source inspection corroborates specific structure or branches; it does not prove runtime behavior, production health, or all code paths.
- A first-party incident report provides an investigated account; distinguish that account from independent reproduction.
- A practitioner's argument or authorial process can teach useful judgment without becoming controlled evidence.
- Cross-domain application, packaging, and proposed instructions are coordinator/researcher inferences and must be labeled as such.

Preserve contradictory results and investigate differing populations, tasks, revisions, definitions, and measures before treating them as disagreement. Do not manufacture equal evidential weight for all positions.

## Depth check and follow-up

The coordinator reviews interim findings, then assigns targeted follow-ups on weak generalizations, version conflicts, hard case branches, and neglected contexts. The stopping condition is a defensible investigation with meaningful case analyses, not reaching an arbitrary source count. Unmet areas remain explicit.

The result should contain candidate instructions with application conditions, examples and counterexamples, observable evaluation criteria, and a maintainable evidence trail. Research alone does not establish that a skill works. Actual paired agent trials, usability sessions, deployments, or benchmark reproduction are outside this research pass unless subsequently carried out and reported.
