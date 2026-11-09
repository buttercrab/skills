# Coordinator source check: code and contracts

Reviewed 2026-11-07. Scope: three implementation-backed case groups in the code/contracts investigation. This check independently fetched selected pinned source through the GitHub connector. No code or tests ran. It is not a review of every API guideline, test body, generated fast path, or compatibility claim in the dossier.

## 1. Rust destination contents and source progress are distinct contracts

At historical Rust commit `eeb90cda1969383f56a2637cbd3037bdf598841c`, [Read::read_exact rustdoc and default dispatch](https://github.com/rust-lang/rust/blob/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/io/mod.rs#L912) explicitly leave destination contents and read progress unspecified after relevant errors, subject to its documented read bound.

The [slice specialization](https://github.com/rust-lang/rust/blob/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/io/impls.rs#L288) checks length before copying. On insufficient input it leaves the destination unchanged but advances the source slice to its end before returning an error.

**Assessment:** the distinction between one implementation's behavior and the trait's promise is supported. Preserve the extra nuance: unchanged destination does not mean the entire operation is failure-atomic. A caller cannot safely generalize either destination preservation or unchanged source state to every reader. The author was notified of this precision point.

## 2. Go's inspection helper and traversal are different operations

At historical Go commit `6885bad7dd86880be6929c02085e5c7a67ff2887`, [errors/wrap.go lines17–77](https://github.com/golang/go/blob/6885bad7dd86880be6929c02085e5c7a67ff2887/src/errors/wrap.go#L17) shows unary `Unwrap` separately from `Is`, whose internal search handles unary and multi-error interfaces and custom matching.

**Assessment:** supported. Treating `Unwrap` as a generic iterator over all wrapped errors would miss branches. This source check corroborates that helper distinction; it does not independently reproduce formatted-error behavior, custom user types, or every public call site.

## 3. Protobuf unknown data differs by representation and option

At historical protobuf-Go commit `c33baa8f3a0d35fd5a39e43c22a50a050f707d34`, the [binary decoder branch](https://github.com/protocolbuffers/protobuf-go/blob/c33baa8f3a0d35fd5a39e43c22a50a050f707d34/proto/decode.go#L175) appends unknown bytes unless its discard option is set. The [ProtoJSON decoder branch](https://github.com/protocolbuffers/protobuf-go/blob/c33baa8f3a0d35fd5a39e43c22a50a050f707d34/encoding/protojson/decode.go#L201) either skips an unknown value when configured or returns an unknown-field error.

**Assessment:** supported for the selected paths. Skipping a field is not preserving it for a later relay. These branches do not establish semantic round-trip compatibility, all generated binary fast paths, or a deployed mixed-version system's behavior. Presence and public API compatibility require their own evidence.

## Result

The three case groups support the dossier's narrow implementation observations. The Rust source-state precision is an important qualifier, not a runtime defect. Historical commits are evidence snapshots rather than current-version recommendations. No general superiority of typed wrappers, wrapping errors, binary encoding, or strict parsing follows from these checks alone.
