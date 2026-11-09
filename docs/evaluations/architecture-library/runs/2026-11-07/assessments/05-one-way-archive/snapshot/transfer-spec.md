# Supplied device integration specification, revision 3
An installed one-way transport accepts files from S and emits files into A's landing directory. A submitted file may be lost, duplicated, delayed up to 36 hours, or arrive out of order. Filename uniqueness is not guaranteed. Individual file bytes may be corrupted in transit. The maximum accepted file is 300 MB. The transport provides no delivery receipt usable by S. No other delivery semantics are established by this specification.

A can validate file bytes and write its local archive. On A the application may atomically commit an archive record and its receipt record in one local database transaction. No transaction spans S, device, and A. S and A have independent clocks which can differ by 20 minutes.

The supplied specification does not establish cryptographic authenticity of received files, key provisioning, or physical tamper resistance. A signed export manifest format can be designed, but no approved trust root or verification-key enrollment procedure is supplied. Assess that gap explicitly; do not infer authenticity from a digest or the transport's directionality.
