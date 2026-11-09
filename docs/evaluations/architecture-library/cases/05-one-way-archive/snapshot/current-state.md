# Existing prototype observations
The prototype writes one CSV per day with a timestamp filename, submits it once, then deletes the local copy after seven days. A imports every received CSV and prints “Imported” with its row count. It does not compute content digests or track record versions. These are source inspection observations, not a measured delivery/reliability report.

Approved business fields available to the exporter: stable record ID, immutable version ID, payload bytes, export-approval decision ID. Local identity and access control for the S exporter and A archive already exist. The custodian's manual entry UI does not exist yet.
