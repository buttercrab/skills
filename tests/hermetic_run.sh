#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: hermetic_run.sh --repo PATH --receipt PATH --watch-profile PATH [--run-root PATH] [--watch PATH] [--network deny|loopback] [--seed-cargo-home PATH] [--seed-go-mod-cache PATH] [--seed-go-build-cache PATH] -- COMMAND..." >&2
  exit 64
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO=""
RECEIPT=""
RUN_ROOT_ARG=""
NETWORK_MODE="deny"
WATCHES=()
WATCH_PROFILE=""
SEED_CARGO_HOME=""
SEED_GO_MOD_CACHE=""
SEED_GO_BUILD_CACHE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || usage
      REPO="$2"
      shift 2
      ;;
    --receipt)
      [[ $# -ge 2 ]] || usage
      RECEIPT="$2"
      shift 2
      ;;
    --run-root)
      [[ $# -ge 2 ]] || usage
      RUN_ROOT_ARG="$2"
      shift 2
      ;;
    --watch)
      [[ $# -ge 2 ]] || usage
      WATCHES+=("$2")
      shift 2
      ;;
    --watch-profile)
      [[ $# -ge 2 ]] || usage
      WATCH_PROFILE="$2"
      shift 2
      ;;
    --network)
      [[ $# -ge 2 ]] || usage
      NETWORK_MODE="$2"
      shift 2
      ;;
    --seed-cargo-home)
      [[ $# -ge 2 ]] || usage
      SEED_CARGO_HOME="$2"
      shift 2
      ;;
    --seed-go-mod-cache)
      [[ $# -ge 2 ]] || usage
      SEED_GO_MOD_CACHE="$2"
      shift 2
      ;;
    --seed-go-build-cache)
      [[ $# -ge 2 ]] || usage
      SEED_GO_BUILD_CACHE="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      usage
      ;;
  esac
done

[[ -n "$REPO" && -d "$REPO" && ! -L "$REPO" ]] || usage
[[ -n "$RECEIPT" && -n "$WATCH_PROFILE" && $# -gt 0 ]] || usage
[[ "$NETWORK_MODE" == "deny" || "$NETWORK_MODE" == "loopback" ]] || usage
command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 2; }
command -v sandbox-exec >/dev/null 2>&1 || { echo "technical network/filesystem isolation unavailable: sandbox-exec missing" >&2; exit 2; }

REPO="$(cd "$REPO" && pwd -P)"
RECEIPT="$(python3 -B -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).expanduser().absolute())' "$RECEIPT")"
WATCH_PROFILE="$(python3 -B -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).expanduser().absolute())' "$WATCH_PROFILE")"
[[ -f "$WATCH_PROFILE" && ! -L "$WATCH_PROFILE" ]] || { echo "watch profile must be a regular non-symlink file" >&2; exit 2; }
HOST_HOME="$(python3 -B -c 'from pathlib import Path; import os; print(Path(os.environ["HOME"]).expanduser().absolute())')"
HOST_TMPDIR="$(python3 -B -c 'from pathlib import Path; import os; print(Path(os.environ.get("TMPDIR", "/tmp")).expanduser().absolute())')"
if [[ "$RECEIPT" == "$REPO"/* && "$RECEIPT" != "$REPO/.planning/"* ]]; then
  echo "receipt inside repository must stay under .planning" >&2
  exit 2
fi

if [[ -n "$RUN_ROOT_ARG" ]]; then
  RUN_ROOT="$(python3 -B -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).expanduser().absolute())' "$RUN_ROOT_ARG")"
  [[ ! -e "$RUN_ROOT" && ! -L "$RUN_ROOT" ]] || { echo "--run-root must name an absent path" >&2; exit 2; }
  mkdir -m 700 "$RUN_ROOT"
else
  RUN_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/skills-hermetic.XXXXXX")"
  chmod 700 "$RUN_ROOT"
fi
RUN_ROOT="$(cd "$RUN_ROOT" && pwd -P)"

python3 -B "$SCRIPT_DIR/portfolio_receipts.py" watch-paths \
  --repo "$REPO" \
  --profile "$WATCH_PROFILE" \
  --host-home "$HOST_HOME" \
  --host-tmpdir "$HOST_TMPDIR" >"$RUN_ROOT/watch-paths.txt"
while IFS= read -r item; do
  [[ -n "$item" ]] || continue
  WATCHES+=("$item")
done <"$RUN_ROOT/watch-paths.txt"
[[ ${#WATCHES[@]} -gt 0 ]] || { echo "watch profile resolved to an empty watch set" >&2; exit 2; }
WATCH_PROFILE_DIGEST="$(python3 -B "$SCRIPT_DIR/portfolio_receipts.py" hash "$WATCH_PROFILE" | python3 -B -c 'import json,sys; print(json.load(sys.stdin)["digest"])')"

cleanup() {
  local status=$?
  trap - EXIT INT TERM
  rm -rf "$RUN_ROOT"
  exit "$status"
}
trap cleanup EXIT INT TERM

mkdir -m 700 \
  "$RUN_ROOT/home" \
  "$RUN_ROOT/tmp" \
  "$RUN_ROOT/cargo-home" \
  "$RUN_ROOT/cargo-target" \
  "$RUN_ROOT/go-cache" \
  "$RUN_ROOT/go-mod-cache" \
  "$RUN_ROOT/go-path" \
  "$RUN_ROOT/go-tmp" \
  "$RUN_ROOT/postgres" \
  "$RUN_ROOT/installer"

copy_seed() {
  local source="$1"
  local destination="$2"
  local label="$3"
  [[ -d "$source" && ! -L "$source" ]] || { echo "$label seed is unavailable or unsafe: $source" >&2; exit 2; }
  cp -R "$source/." "$destination/"
  chmod -R u+rwX,go-rwx "$destination"
}

[[ -z "$SEED_CARGO_HOME" ]] || copy_seed "$SEED_CARGO_HOME" "$RUN_ROOT/cargo-home" "Cargo"
[[ -z "$SEED_GO_MOD_CACHE" ]] || copy_seed "$SEED_GO_MOD_CACHE" "$RUN_ROOT/go-mod-cache" "Go module"
[[ -z "$SEED_GO_BUILD_CACHE" ]] || copy_seed "$SEED_GO_BUILD_CACHE" "$RUN_ROOT/go-cache" "Go build"

export RUN_ROOT
export HERMETIC_RUN_ACTIVE=1
export HOME="$RUN_ROOT/home"
export TMPDIR="$RUN_ROOT/tmp"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$RUN_ROOT/python-cache"
export CARGO_HOME="$RUN_ROOT/cargo-home"
export CARGO_TARGET_DIR="$RUN_ROOT/cargo-target"
export CARGO_NET_OFFLINE=true
export GOCACHE="$RUN_ROOT/go-cache"
export GOMODCACHE="$RUN_ROOT/go-mod-cache"
export GOPATH="$RUN_ROOT/go-path"
export GOTMPDIR="$RUN_ROOT/go-tmp"
export GOTOOLCHAIN=local
export GOPROXY=off
export GOSUMDB=off
export FRONT_AGENT_MAIL_BACKEND=memory

SNAPSHOT_ARGS=(state --repo "$REPO")
for item in "${WATCHES[@]}"; do
  SNAPSHOT_ARGS+=(--watch "$item")
done
python3 -B "$SCRIPT_DIR/portfolio_receipts.py" "${SNAPSHOT_ARGS[@]}" >"$RUN_ROOT/pre-state.json"

PROFILE="$RUN_ROOT/sandbox.sb"
{
  printf '%s\n' '(version 1)'
  printf '%s\n' '(allow default)'
  printf '%s\n' '(deny file-write*)'
  printf '(allow file-write* (subpath "%s"))\n' "$RUN_ROOT"
  printf '%s\n' '(allow file-write* (literal "/dev/null"))'
  printf '%s\n' '(allow file-write* (literal "/dev/dtracehelper"))'
  printf '%s\n' '(deny network*)'
  if [[ "$NETWORK_MODE" == "loopback" ]]; then
    printf '%s\n' '(allow network-inbound (local ip "localhost:*"))'
    printf '%s\n' '(allow network-outbound (remote ip "localhost:*"))'
  fi
} >"$PROFILE"

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
sandbox-exec -f "$PROFILE" -- "$@" >"$RUN_ROOT/stdout.log" 2>"$RUN_ROOT/stderr.log"
COMMAND_STATUS=$?
set -e
ENDED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

python3 -B "$SCRIPT_DIR/portfolio_receipts.py" "${SNAPSHOT_ARGS[@]}" >"$RUN_ROOT/post-state.json"

mkdir -p "$(dirname "$RECEIPT")"
python3 -B - \
  "$RUN_ROOT/pre-state.json" \
  "$RUN_ROOT/post-state.json" \
  "$RUN_ROOT/stdout.log" \
  "$RUN_ROOT/stderr.log" \
  "$RECEIPT" \
  "$RUN_ROOT" \
  "$REPO" \
  "$NETWORK_MODE" \
  "$WATCH_PROFILE_DIGEST" \
  "$COMMAND_STATUS" \
  "$STARTED_AT" \
  "$ENDED_AT" \
  "$@" <<'PY'
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

pre_path, post_path, stdout_path, stderr_path, receipt_path, run_root, repo, network, watch_profile_digest, status, started, ended, *command = sys.argv[1:]
pre = json.loads(Path(pre_path).read_text())
post = json.loads(Path(post_path).read_text())
stdout = Path(stdout_path).read_bytes()
stderr = Path(stderr_path).read_bytes()

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def redact(value: str) -> str:
    value = re.sub(r"(?i)(authorization:\s*bearer\s+)[^\s]+", r"\1[REDACTED]", value)
    value = re.sub(r"(?i)((?:token|password|secret)\s*[=:]\s*)[^\s]+", r"\1[REDACTED]", value)
    return value[-4096:]

state_unchanged = pre == post
command_status = int(status)
receipt = {
    "schema_version": "hermetic-run/v1",
    "receipt_id": str(uuid.uuid4()),
    "repository_root": repo,
    "run_root": run_root,
    "network_policy": {"enforcer": "sandbox-exec", "mode": network},
    "watch_profile_digest": watch_profile_digest,
    "command": command,
    "command_exit_code": command_status,
    "started_at": started,
    "ended_at": ended,
    "pre_state": pre,
    "post_state": post,
    "state_unchanged": state_unchanged,
    "stdout_sha256": digest(stdout),
    "stderr_sha256": digest(stderr),
    "failure_summary": redact((stderr + b"\n" + stdout).decode("utf-8", errors="replace")) if command_status else "",
    "verdict": (
        "passed"
        if command_status == 0 and state_unchanged
        else "unsafe"
        if not state_unchanged
        else "incomplete"
        if command_status == 2
        else "failed"
    ),
}
target = Path(receipt_path)
temp = target.parent / f".{target.name}.tmp.{os.getpid()}.{uuid.uuid4()}"
descriptor = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
    json.dump(receipt, handle, indent=2, sort_keys=True)
    handle.write("\n")
    handle.flush()
    os.fsync(handle.fileno())
os.replace(temp, target)
os.chmod(target, 0o600)
directory = os.open(target.parent, os.O_RDONLY)
try:
    os.fsync(directory)
finally:
    os.close(directory)
PY

cat "$RUN_ROOT/stdout.log"
cat "$RUN_ROOT/stderr.log" >&2

if ! cmp -s "$RUN_ROOT/pre-state.json" "$RUN_ROOT/post-state.json"; then
  echo "hermetic state drift detected; see $RECEIPT" >&2
  exit 3
fi
exit "$COMMAND_STATUS"
