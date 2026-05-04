#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$DIR/../../.." && pwd)"
ROOT="$(mktemp -d)"
BIN="$ROOT/front-agent"

if [[ -z "${AGENT_MAIL_TOKEN:-}" ]]; then
  shopt -s nullglob
  env_files=("$REPO_DIR"/.env/agent-mail/*.env)
  shopt -u nullglob
  if [[ "${#env_files[@]}" -gt 0 ]]; then
    set -a
    # shellcheck disable=SC1090
    source "${env_files[0]}"
    set +a
  fi
fi

if [[ -z "${AGENT_MAIL_TOKEN:-}" ]]; then
  echo "front-agent smoke skipped: AGENT_MAIL_TOKEN is not set"
  exit 0
fi

cleanup() {
  rm -rf "$ROOT"
}
trap cleanup EXIT

go build -o "$BIN" "$DIR/../cmd/front-agent"

main_log="$ROOT/main.log"
gateway_log="$ROOT/gateway.log"

"$BIN" main --root "$ROOT" >"$main_log" 2>&1
main_id="$(awk '/Main identity:/ {print $3}' "$main_log")"
if [[ -z "$main_id" ]]; then
  echo "main identity not found" >&2
  cat "$main_log" >&2
  exit 1
fi

wait_lock="$ROOT/.front-agent/wait-ready/$main_id.json"
for _ in {1..100}; do
  [[ -f "$wait_lock" ]] && break
  sleep 0.01
done
if [[ ! -f "$wait_lock" ]]; then
  echo "detached wait-ready lock was not created" >&2
  cat "$main_log" >&2
  exit 1
fi

"$BIN" gateway "$main_id" --root "$ROOT" --timeout 10s >"$gateway_log" 2>&1
gateway_id="$(awk '/Gateway identity:/ {print $3}' "$gateway_log")"
if [[ -z "$gateway_id" ]]; then
  echo "gateway identity not found" >&2
  cat "$gateway_log" >&2
  exit 1
fi

question_id="$(cat <<'YAML' | "$BIN" send "Need direction" --root "$ROOT" --identity "$main_id"
```yaml
method: question
from_role: main
to_role: gateway
summary: Choose direction.
question: Prototype or production?
```
YAML
)"

gateway_listen="$("$BIN" listen --root "$ROOT" --identity "$gateway_id" --timeout 0)"
if [[ "$gateway_listen" != *"$question_id"* || "$gateway_listen" != *"method: question"* ]]; then
  echo "gateway listen did not include main question" >&2
  echo "$gateway_listen" >&2
  exit 1
fi

answer_id="$(cat <<'YAML' | "$BIN" send "Direction confirmed" --root "$ROOT" --identity "$gateway_id" --responds-to "$question_id"
```yaml
method: answer
from_role: gateway
to_role: main
summary: Direction confirmed.
human_confirmed: true
answer: Production.
```
YAML
)"

main_listen="$("$BIN" listen --root "$ROOT" --identity "$main_id" --timeout 0)"
if [[ "$main_listen" != *"$answer_id"* || "$main_listen" != *"answer: Production."* ]]; then
  echo "main listen did not include gateway answer" >&2
  echo "$main_listen" >&2
  exit 1
fi

listener_log="$ROOT/listener.log"
"$BIN" listen --root "$ROOT" --identity "$main_id" --timeout 1s >"$listener_log" 2>&1 &
listener_pid=$!
listener_lock="$ROOT/.front-agent/listeners/$main_id.json"
for _ in {1..100}; do
  [[ -f "$listener_lock" ]] && break
  sleep 0.01
done
if [[ ! -f "$listener_lock" ]]; then
  echo "listener lock was not created" >&2
  cat "$listener_log" >&2 || true
  exit 1
fi
if "$BIN" listen --root "$ROOT" --identity "$main_id" --timeout 0 >"$ROOT/duplicate-listener.out" 2>"$ROOT/duplicate-listener.err"; then
  echo "duplicate listener unexpectedly succeeded" >&2
  exit 1
fi
if ! grep -q "already running" "$ROOT/duplicate-listener.err"; then
  echo "duplicate listener did not explain existing listener" >&2
  cat "$ROOT/duplicate-listener.err" >&2
  exit 1
fi
wait "$listener_pid"

echo "front-agent smoke passed"
