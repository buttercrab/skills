# Post-freeze syntax correction

This separate copy replaces semicolon punctuation with commas inside sequence-diagram blocks only. It is not a new assessment or an original-run pass; architecture content is unchanged. Original captions below retain the runner’s historical inspection limits. Coordinator parsing of this correction is recorded separately; no rendering or operational check is implied.

# Editable document ingestion diagrams

These Mermaid blocks are source-only models of supplied revision `7f12a6b` and captured inventory, not observed live operation. They were manually reconciled with the evidence, not parsed or rendered. “Captured” identifies supplied release/configuration evidence; “unknown” identifies a missing fact; no proposed system is included. File locators are relative to `snapshot/`.

## Runtime: where does ingestion complete or fail?

Scope: one upload, queue processing and client status observation. Implementation: `intake.ts:2–15`. Captured queue/client contract: `client-and-operations.md:2,4`. Visibility/attempt configuration: `deployment.yaml:13–15`. Browser route mapping is supplied only by the client capture. Diagram source separates the handler from the queue's acknowledgment contract.

```mermaid
sequenceDiagram
    participant C as Browser / caller
    participant I as Intake HTTP handler
    participant O as Document object store
    participant D as Metadata and text DB
    participant Q as Intake task queue
    participant W as Parse-runner handler
    participant P as Parser dependency (location unknown)
    participant F as intake-failed queue
    participant R as Operations
    C->>I: Upload document bytes
    I->>O: Await put(bytes)
    O-->>I: Blob key
    I->>D: Await insert(blobKey, pending)
    D-->>I: Record ID
    I->>Q: Await send(recordId)
    Q-->>I: Send resolves (provider durability unknown)
    I-->>C: Return 202 and record ID, parsing incomplete
    Note over I,Q: Writes are separate, error/timeout can leave partial or unknown enqueue state
    Q->>W: Deliver job (redelivery possible)
    W->>D: Read record
    W->>O: Read bytes by blob key
    W->>P: Await parse(bytes)
    alt Handler completes successfully
        P-->>W: Parsed text
        W->>D: Await update ready and text
        D-->>W: Update resolves
        W-->>Q: Handler success allows acknowledgment
        Note over D,Q: Lost acknowledgment can repeat work, deduplication not established
    else Handler throws at any processing step
        W-->>Q: Error, no failed-status write in supplied handler
        alt Delivery count below four
            Q->>Q: Eligible for redelivery after visibility timeout (120 seconds configured)
        else Four deliveries exhausted
            Q->>F: Move job to intake-failed
            R->>F: Review each weekday, no automatic redrive configured
            Note over D,F: Queue failure is separate from document status, pending can persist
        end
    end
    loop Every three seconds, stops at ready, failed, or two minutes
        C->>I: GET /documents/:id (captured client contract)
        I->>D: status(id) reads record
        D-->>I: Stored record
        I-->>C: Stored status (route wrapper not supplied)
    end
    Note over C,D: At two minutes client offers Check again, no cancellation shown
```

The final polling loop is drawn after processing to keep the branches readable; in the captured client behavior polling can overlap queue processing. The exception branch applies to reads, parse and update, not merely parser rejection. If update took effect before an uncertain return or acknowledgment, stored status can already be `ready` even when delivery later fails. No `failed` transition is drawn because no writer is supplied.

## Deployment: where are the captured executables and stores?

Scope/status: rendered inventory at 2026-11-05 09:00Z, intake application account only, release `7f12a6b` (`deployment.yaml:1–22`); release completion is recorded, not independently observed (`client-and-operations.md:6`). Boxes group placement, not transactions or trust zones. Solid arrows identify implementation calls; dotted arrows identify capture-only relationships or unresolved placement. Locations outside this account, network paths and trust boundaries remain unknown.

```mermaid
flowchart LR
    C["Browser / caller; location unknown"]
    subgraph A["Captured intake application account — Region A — revision 7f12a6b"]
        I["intake workload — 2 replicas — http-server"]
        W["parse-runner workload — 1 replica — queue-consumer"]
        O["documentBlobs: regional-object-store-A"]
        D["metadataAndText: managed-database-A"]
        Q["intake: managed-task-queue-A"]
        F["intake-failed: managed-task-queue-A"]
        I -->|writes original bytes| O
        I -->|inserts pending; reads status| D
        I -->|sends record ID task| Q
        Q -.->|delivers job; contract allows redelivery| W
        W -->|reads blob| O
        W -->|reads record; writes ready and text| D
        Q -.->|moves after four deliveries| F
    end
    P["Parser dependency — execution and placement UNKNOWN"]
    R["Operations — location unknown"]
    U["UNKNOWN: other accounts / regions, global routing, DR and storage replication"]
    C -.->|uploads; captured client polls GET status| I
    W -->|calls parse bytes| P
    R -.->|reviews each weekday; no automatic redrive| F
```

Node evidence: intake/parse-runner names, entrypoints and counts `deployment.yaml:5–12`; stores/queues `deployment.yaml:16–21`; Region A `deployment.yaml:3`; account scope `deployment.yaml:22`. Edge evidence: implementation calls `intake.ts:3–5,8,11–14`; delivery/dead-letter/operations `client-and-operations.md:4`; client `client-and-operations.md:2`. The parser node's placement is deliberately outside the Region A grouping to denote unresolved placement, not evidence that it runs elsewhere. The unattached unknown node records coverage limits and asserts no runtime dependency. No Region B service or active-active topology is established by these inputs.
