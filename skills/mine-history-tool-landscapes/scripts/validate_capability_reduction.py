#!/usr/bin/env python3
"""Validate capability-reduction/v3 inside its fully reopened v4 authority chain.

This compatibility filename is a successor entrypoint, not a v2 shim.  It has
the same arguments and authoritative behavior as validate_history_v4.py and
deliberately offers no skip-raw success mode.
"""

from __future__ import annotations

import validate_history_v4


if __name__ == "__main__":
    raise SystemExit(validate_history_v4.main())
