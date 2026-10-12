# Isolated validation

`hermetic_run.sh` runs a command with macOS `sandbox-exec`. It permits writes only
inside a private temporary run directory and denies networking, or permits only
loopback with `--network loopback`. It refuses to run without technical isolation.
No deployed service or external account is needed.

```sh
tools/validation/hermetic_run.sh \
  --repo "$PWD" --receipt /tmp/validation-result.json \
  --watch-profile tools/validation/ambient-watches-v1.json \
  -- python3 -B -m unittest discover -s tests
```

Repository and watched state is hashed before and after the command. The receipt
records exit status, state drift, output hashes, and a bounded failure summary.
The private run directory is removed on exit. Build-cache seeds are copied into
that directory; commands never write to the originals. PostgreSQL test scripts in
`integrations/agent-mail` require this runner and its `RUN_ROOT`.

`state_manifest.py` provides strict JSON loading, content manifests, tree hashes,
and watch-profile expansion. Existing manifest version identifiers remain stable
for legacy preservation-journal recovery. `ambient_baseline.py` optionally checks
installed skill links and Python cache drift; it discovers skills from `SKILL.md`
files and does not depend on a routing catalog. It expects a complete installation
at both supplied roots; use installer migration tests for partial installations.

The runner restricts writes and networking, but does not restrict reads. Receipts
include command arguments, so do not pass credentials in arguments. Redaction of
failure summaries is best effort. Ordinary skill tests need no sandbox runner;
use it for integration checks that must demonstrate isolation.
