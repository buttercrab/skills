# Review the Plan

Read this reference when deciding whether a plan needs adversarial review and when reconciling reviewer evidence.

## Review threshold

Prefer fresh review for broad, architectural, security-sensitive, production-facing, irreversible, costly, ambiguous, or multi-owner plans. A simple, low-risk, single-path plan with deterministic checks may skip review only with a recorded reason.

## Reviewer setup

- Use direct reviewers only. Begin every reviewer assignment with: `You are a direct child. Do not spawn or delegate to any other agent.`
- Assign distinct attack angles such as architecture/trigger ownership, packet/approval safety, verification validity, security, or UX.
- Give raw artifacts and minimum task-local context. Do not provide the intended verdict, suspected bug, or desired fix.
- Prefer read-only isolation or copies. Otherwise hash canonical packet files before and after the child run and invalidate any result that mutated them.
- Require inspected scope, uninspected scope, evidence versus inference, severity, concrete correction, missing proof, and an explicit verdict.
- Keep each assignment narrowly bounded and prohibit product execution, generated-cache cleanup, or unrelated repository work. Set a concrete time/poll budget. If a reviewer does not finish, stop or interrupt it when supported, preserve the partial trace, record the review as failed/blocked, and do not claim review completion or seal the plan.

## Reconciliation

The active coordinator independently verifies findings. Accept supported corrections, reject overreach with reasons, update facts and decisions before the plan, and rerun affected review gates. A review verdict does not replace deterministic evidence.
