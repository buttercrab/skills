# Static review of design-with-intent

Reviewed: 2026-11-07. Scope: SKILL.md, agents/openai.yaml, and four references under skills/design-with-intent. No trial cases, private answers, generated artifacts, or experimental conditions were inspected. No skill files were changed. This is an instruction/source review, not evidence of actual agent behavior.

## Finding

### Low priority: make the viewport check conditional in the entrypoint

Location: [SKILL.md:54](/Users/jaeyong/skills/skills/design-with-intent/SKILL.md:54).

The entrypoint tells all rendered work to inspect a desktop layout, while [verification.md:22](/Users/jaeyong/skills/skills/design-with-intent/references/verification.md:22) correctly qualifies desktop/narrow checks by whether the requested interface spans them. The unconditional entrypoint can add an irrelevant requirement for a mobile-only native interface.

Counterexample: implementing an iPhone-only appointment flow should verify supported device sizes and orientation/content behavior; it need not invent or inspect a desktop interface.

Suggested narrow change: qualify the entrypoint's viewport check the same way as the reference, or say to inspect the relevant supported layouts. No new universal breakpoint or device count is needed.

Resolution: applied in package revision v1.1. The frozen v1 trial package retains the original wording; boundary/development probes use v1.1. This correction came from the static review, not from a trial's preferred answer.

## Checked and supported

- **Missing direction versus over-questioning:** [SKILL.md:20](/Users/jaeyong/skills/skills/design-with-intent/SKILL.md:20) ties questions to consequential human-owned choices. Lines 26–28 preserve independent work, resolved briefs, explicit delegation, and provisional drafts. This matches the conditional approach supported by [Horvitz's principles 5–11](https://erichorvitz.com/chi99horvitz.pdf). No fixed interview length or question count is imposed.
- **Human expression and leading alternatives:** entrypoint lines 22–24 and [eliciting-direction.md:19](/Users/jaeyong/skills/skills/design-with-intent/references/eliciting-direction.md:19) allow alternatives outside the offered framing and discourage unequal praise. Reference line 21 acknowledges anchoring and avoids requiring multiple complete interfaces. This preserves the distinction between helping expression and claiming neutral preference measurement.
- **Execution after answers:** entrypoint lines 34–38 and 52 require actual design commitments and working implementation when requested. They do not stop at a brief, rationale, or selection question. Reference lines 25–33 retain partial answers, accept delegation, and do not treat elapsed time as an answer.
- **Answer fidelity and scope:** entrypoint lines 16 and 36 preserve prior decisions and avoid approval for every screen. Reference line 31 limits new feedback to the affected decision. No instruction silently converts an owner's taste into proof of end-user usability.
- **Source limits:** [evidence-and-maintenance.md:7](/Users/jaeyong/skills/skills/design-with-intent/references/evidence-and-maintenance.md:7) through line 18 correctly distinguishes principles, bounded experiments, oracle-based NLP clarification, documented patterns, and standards. The [Tohidi paper](https://www.billbuxton.com/rightDesign.pdf) did not establish increased substantial suggestions; the reference preserves that negative result. The [Zhang/Choi benchmark](https://aclanthology.org/2025.findings-naacl.306.pdf) is not represented as a real creative-user effort study.
- **Proportion and duplication:** the entrypoint contains the core route; references add contextual examples, state distinctions, verification cases, and provenance. Some overlap reinforces invariants without introducing contradictory interviews, taste bans, or formal-document requirements. No deletion is warranted solely to reduce repeated wording.

## Conclusion and limits

No blocking static issue found in questioning, delegation, answer fidelity, or evidence attribution. The viewport qualifier is a small scope correction. The draft's actual tendency to ask, interpret, execute, preserve direction, or stop unnecessarily must be assessed through the separate behavioral trials; this review did not inspect or prejudge them.

