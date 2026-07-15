#!/usr/bin/env python3
"""Validate history-evidence/v1 and publication/v3 under full raw reopening.

This compatibility filename is a successor entrypoint, not an evidence-v2
shim.  Non-authoritative inspection can only emit E_RAW_REOPEN_REQUIRED and
cannot be consumed as evidence, hydration, synthesis, or publication success.
"""

from __future__ import annotations

import validate_history_v4


if __name__ == "__main__":
    raise SystemExit(validate_history_v4.main())
