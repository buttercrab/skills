# Scope approved by product/security
- Two engineers, six weeks, maximum one engineer-week of new operations burden over the quarter.
- Existing app fleet, relational database, and private object storage are supported. No new always-on datastore is budgeted.
- Gateway may be exercised in shadow mode with decision comparison; shadow deny must not alter current production responses.
- Enforcement cutover can be gradual by stable account cohort, with a recorded version of policy and switch state per decision.
- Once a cohort is enforcing, gateway unavailable returns 503; it must not fall back to ownership-only authorization.
- A rollback may disable a newly added sharing feature for an enforcing cohort, but must not restore access revoked by the new policy.
- Ownership records and current endpoint cannot be removed before 2027-04-01.
- Current runtime emits request counts, latency, and status metrics; it does not record policy version or authorization decision source.
- No cutover error/latency threshold has yet been approved by the on-call owner.
