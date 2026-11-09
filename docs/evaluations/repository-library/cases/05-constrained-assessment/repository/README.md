# signal-window
Python >=3.11. `signal-window input.txt` prints TSV columns `label` and `value`, skipping blank lines. Every nonblank input line must be `label=value`; labels are nonempty and values are decimal integers. Parse errors should report a line number and exit 2 without a traceback.

Library API: `parse_lines(lines: Iterable[str]) -> list[tuple[str, int]]` raises ValueError on invalid input.
Install: `pip install signal-window`. Release 0.6.2 is planned; no upload has happened according to the maintainer note. No release artifacts are present.
