#!/usr/bin/env python3
"""Emit one descriptor-bound v2 Claude Code adapter projection."""

from __future__ import annotations

import normalize_codex_history as common


def main() -> int:
    args = common.parser().parse_args()
    args.platform = "claude-code"
    return common.main_for_args(args)


if __name__ == "__main__":
    raise SystemExit(main())
