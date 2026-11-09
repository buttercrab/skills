# Independent foundation-card sample

Date: 2026-11-07. Reviewed only `foundation-cap-model` and `foundation-linearizability-histories`, then independently opened their cited original PDFs. No assessment fixtures, system implementation, running deployment, rendered diagram or test was inspected. No source/card edits, code execution or failure injection occurred.

## Judgment

No demonstrated material defect in either sampled card. Their selected mechanisms and explicit limits are supported by the original definition/model sections. No corrective card edit is requested. This is a bounded textual source check, not a mechanized proof audit or whole-system verification.

## CAP card

Fresh receipt: [Gilbert and Lynch original paper](https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/cap-proof.pdf), §2.1–2.3 (printed pp.52–53), §3.1 (pp.53–54), §4.1–4.3 (pp.55–56). The PDF includes unrelated conference notices before the article; inspection used the named paper sections rather than treating those notices as its publication date.

The card preserves operation-level atomic/linearizable meaning, unbounded eventual-response availability and the arbitrary-loss model. Its partitioned write/read depiction and partial-synchrony qualification fit the selected sections. It does not convert CAP into an ACID definition, database recommendation, latency SLO or observed uptime result. The proposed operation-specific product example is labeled as an application, not an original-paper experiment.

The “waiting/rejection versus stale response” diagram instruction should be read against the modeled operation's legal response: an arbitrary HTTP error is not a proof that the original read/write contract remains available and consistent. The card does not make that erroneous promise, so this is an application caution rather than a requested correction.

## Linearizability card

Fresh receipt: [Herlihy and Wing original coauthor-hosted PDF](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf), §1.2 (printed pp.464–467), §2.1–2.3 (pp.467–470), §3.1 locality statement and selected proof setup (pp.470–471).

The card correctly connects invocation/response histories, legal sequential behavior and real-time precedence. Pending-call uncertainty and overlapping intervals are supported; the application-specific queue API still needs inspection. Locality is not converted into a claim of business-transaction atomicity or durability. Diagram ordering is explicitly interpretation, not an observed implementation instruction.

## Review limits

Both PDFs were accessible through the web text reader during this review. No whole-paper reproduction, graphical figure-view claim, alternative mirror verification or runtime observation is implied. The review checks the cards' central attributions and transfer limits, not every proof step, every architectural use of CAP, or the reliability of this skill. Original formal conclusions remain conditional on their stated models.
