# Independent source check: architecture research

Reviewed 2026-11-07. Scope: six consequential claims in `architecture.md`, with underlying pinned implementation/tests or original papers re-opened independently. No code, tests, failure injection, or production checks were run. The review does not establish current-version correctness.

## Result

The selected claims are supported at their stated research scope. No demonstrated runtime defect or material contradiction was found. Two precision additions would make future skill guidance safer: distinguish a conditional VFS sync call from an observed filesystem syscall, and distinguish expectation expiry from a scheduled wakeup. A diagram-label refinement is also useful.

## 1. SQLite TRUNCATE prose versus selected implementation

**Checked claim:** the retrieved atomic-commit article's unqualified TRUNCATE prose differs from a conditional synchronization branch at the pinned 3.46.1 implementation.

The [article §7.6](https://sqlite.org/atomiccommit.html#_persistent_rollback_journals) says TRUNCATE is not followed by a synchronization syscall. At [pager.c L2060–2079](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L2060), the open rollback-journal path checks TRUNCATE; `journalOff==0` skips work; otherwise successful truncation plus `fullSync` invokes `sqlite3OsSync`. This supports the scoped representation discrepancy.

**Required interpretation:** this is a conditional code path, not an observed syscall or power-loss result. The original report already avoids claiming a present runtime defect. Keep that restriction when distilling it into examples.

**Suggested narrow wording:** “At this historical revision, a nonempty TRUNCATE journal invokes VFS synchronization after successful truncation when the pager's full-synchronization condition holds. That conditional behavior is absent from the retrieved prose.”

## 2. SQLite flags and durability-model omissions

Additional owning source inspection strengthens the scope qualification:

- [pager.c L3605–3620](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L3605) makes temporary files unsynchronized; otherwise `fullSync` is set by a synchronous safety level at least `PAGER_SYNCHRONOUS_FULL`. The separate `PAGER_FULLFSYNC` flag selects a sync flavor. These similarly named concepts should not be conflated.
- [os.c L99–101](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/os.c#L99) dispatches to `xSync` only for nonzero flags.
- [os_unix.c L3638–3703](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/os_unix.c#L3638) includes a no-sync build branch and platform-dependent synchronization choices; [L3771–3794](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/os_unix.c#L3771) delegates from the Unix VFS.

The report correctly labels its diagram a simplified rollback-mode ordering and excludes WAL, atomic-write optimizations, noSync, and exclusive fast paths. [Phase-one comments L6430–6440](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L6430) also say an explicit noSync caller must synchronize before phase two. [Phase two L6689–6711](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L6689) contains the stated unchanged exclusive/PERSIST early return.

**Recommendation:** label the teaching model “successful normal rollback-mode commit path, under declared sync/VFS assumptions.” A box called “Database durability” is an intended property, not a hardware guarantee established by source inspection. This is a clarification to preserve the report's own limitations, not a discovered SQLite bug.

## 3. Kubernetes expectations, expiration, and retries

**Checked claim:** the selected ReplicaSet controller permits progress on fulfilled or expired expectations, adjusts failed/skipped creation counts, and rate-limits failed work items without establishing exactly-once creation.

Receipts at commit `9edcffcde5595e8a5b1a35f88c421764e575afce`:

- [controller_utils.go L186–217](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/controller_utils.go#L186) returns true for fulfilled or expired expectations, as well as missing/error cases. Expiration compares real-clock elapsed time to [the five-minute constant at L70](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/controller_utils.go#L70).
- [replica_set.go L587–619](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set.go#L587) sets expectations and lowers counts for unsuccessful/skipped creations.
- [L547–563](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set.go#L547) forgets successful queue items and calls `AddRateLimited` for errors.

**Precision addition:** expiration is evaluated when this function runs. These branches do not themselves schedule a five-minute wakeup. “Liveness mechanism” is reasonable as a component description; do not convert it into a guarantee of progress at exactly five minutes. Further scheduling/event assumptions would need separate inspection.

## 4. Kubernetes observation order, status, and test evidence

The [sync implementation L696–740](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set.go#L696) evaluates expectations before listing cached Pods. The mutation call is gated by both that result and absence of a deletion timestamp; status calculation/update follows even when that mutation gate is false, subject to earlier error returns.

Selected test bodies independently support the reported intent: [dormancy L307–385](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set_test.go#L307), [ordering L1103–1133](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set_test.go#L1103), and [slow-start L1776–1843](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set_test.go#L1776). These are assertions read in fixtures, not passing-test receipts.

**Diagram refinement:** rename the initial diamond “Compute expectations-satisfied flag (including expiry)” and label the later mutation decision with that flag. This makes clear that an unsatisfied flag does not skip cached observation or status handling. The report's prose already states the correct distinction.

## 5. CAP model and clocks

The [original Gilbert/Lynch paper §§2–3](https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/cap-proof.pdf) supports the report's definitions: linearizability, eventual response at non-failing nodes, and arbitrary message loss. Availability here is not a finite latency SLO or permission to return an arbitrary error value.

One useful extension is [§4.2, Theorem 2](https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/cap-proof.pdf): arbitrary message loss still prevents the stated guarantees in the paper's partially synchronous model. Thus adding clocks does not in itself resolve the partition tradeoff. The report makes no contrary claim; this would strengthen its comparison with Spanner.

## 6. Helland assumptions versus Spanner's mechanism

[Helland's introduction](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf), printed p.132, explicitly assumes no large-scale distributed transactions and sets aside availability to discuss scalability. Its messaging sections distinguish durable remembered acceptance from natural idempotence. Treating it as a theorem forbidding distributed transactions would change its evidence class.

[Spanner's original paper](https://www.usenix.org/system/files/conference/osdi12/osdi12-final-16.pdf), §§2.1,3,4.1.2,4.2.1, supports the contrasting reported design: replicated transaction state, multi-group two-phase commit, TrueTime uncertainty bounds, and commit wait. Its measurements are conditional experiments. Neither existence of that design nor bounded clocks implies availability in every partition.

The report preserves these assumptions and does not overclaim present product support or universal cost. No correction needed.

## Review boundary

Only these claims were rechecked; the rest of the architecture bibliography is not independently audited by this review. Repository content was fetched through the GitHub connector at exact commits and selected lines inspected. Papers and SQLite prose were read through web tools. No Git operation, compiler invocation, test run, storage experiment, live controller, or production observation contributed evidence.

The additional SQLite wrapper/VFS sources should be retained as supplemental receipts if the final example names system calls. The five-minute expectation condition should remain a permission-to-proceed condition rather than a promised timer. Both are examples of the library's central challenge: simplification must preserve the assumptions that make a statement true.
