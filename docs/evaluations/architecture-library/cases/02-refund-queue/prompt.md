# Refund processing assessment

Review the supplied refund operation and propose a reliable processing architecture. Explain the business commit point, queue acknowledgment point, duplicate deliveries, and the uncertainty after a payment-provider timeout. Include editable sequence and/or state diagram source useful to the on-call maintainer; show a failure and recovery path rather than only the happy path.

Separate current behavior, proposed behavior, inferred risks, and true unknowns. Cite snapshot paths/lines. You may ask a focused policy question only if its answer changes a business action. Supply a safe no-answer fallback. Do not modify or run fixture code, execute tests, call a payment provider, or provision anything. This is an assessment and design artifact task.
