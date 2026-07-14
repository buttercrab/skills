#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOKEN="mcp-test-token"
CREDENTIAL_ADMIN_TOKEN="mcp-test-credential-admin-token"
CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$ROOT/target}"
TEST_PASSED=0
if [[ -z "${POSTGRES_BIN:-}" ]]; then
  if command -v pg_config >/dev/null 2>&1; then
    POSTGRES_BIN="$(pg_config --bindir)"
  elif command -v initdb >/dev/null 2>&1; then
    POSTGRES_BIN="$(dirname "$(command -v initdb)")"
  else
    echo "PostgreSQL tools not found; set POSTGRES_BIN or install PostgreSQL" >&2
    exit 2
  fi
fi
for tool in initdb pg_ctl pg_isready createdb; do
  [[ -x "$POSTGRES_BIN/$tool" ]] || { echo "missing PostgreSQL tool: $POSTGRES_BIN/$tool" >&2; exit 2; }
done
TMPDIR="$(mktemp -d /tmp/agent-mail-mcp-test-XXXXXX)"
PGDATA="$TMPDIR/pgdata"
PGLOG="$TMPDIR/postgres.log"
SERVERLOG="$TMPDIR/server.log"

cleanup() {
  local status=$?
  trap - EXIT
  if [[ $status -eq 0 && $TEST_PASSED -ne 1 ]]; then
    status=1
  fi
  if [[ -n "${SSE_PID:-}" ]]; then
    kill "$SSE_PID" 2>/dev/null || true
    wait "$SSE_PID" 2>/dev/null || true
  fi
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  if [[ -n "${POSTGRES_PID:-}" ]]; then
    "$POSTGRES_BIN/pg_ctl" -D "$PGDATA" -m fast stop >/dev/null 2>&1 || true
  fi
  if [[ $status -ne 0 ]]; then
    echo "tmpdir: $TMPDIR" >&2
    echo "postgres log: $PGLOG" >&2
    echo "server log: $SERVERLOG" >&2
    [[ -f "$TMPDIR/sse.log" ]] && cat "$TMPDIR/sse.log" >&2
  else
    rm -rf "$TMPDIR"
  fi
  exit "$status"
}
trap cleanup EXIT

free_port() {
  python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
}

json_get() {
  python3 -c 'import json, sys; print(json.load(sys.stdin)[sys.argv[1]])' "$1"
}

assert_json() {
  python3 -c 'import json, sys
data = json.load(sys.stdin)
expr = sys.argv[1]
if not eval(expr, {"json": json}, {"data": data}):
    raise SystemExit(f"assertion failed: {expr}\n{json.dumps(data, indent=2)}")' "$1"
}

mcp_request() {
  python3 -c 'import json, sys
method = sys.argv[1]
request = {"jsonrpc": "2.0", "method": method}
if sys.argv[2]:
    request["id"] = int(sys.argv[2])
if sys.argv[3]:
    request["params"] = json.loads(sys.argv[3])
print(json.dumps(request))' "$@"
}

wait_for_sse_uri() {
  local uri="$1"
  for _ in {1..100}; do
    if python3 - "$TMPDIR/sse.log" "$uri" <<'PY'
import json
import sys

path, expected = sys.argv[1], sys.argv[2]
try:
    lines = open(path, encoding="utf-8").read().splitlines()
except FileNotFoundError:
    raise SystemExit(1)

for line in lines:
    line = line.lstrip("\x00")
    if not line.startswith("data:"):
        continue
    payload = line.removeprefix("data:").strip()
    if not payload:
        continue
    try:
        message = json.loads(payload)
    except json.JSONDecodeError:
        continue
    if (
        message.get("method") == "notifications/resources/updated"
        and message.get("params", {}).get("uri") == expected
    ):
        raise SystemExit(0)
raise SystemExit(1)
PY
    then
      return 0
    fi
    sleep 0.05
  done
  echo "missing SSE resource update for $uri" >&2
  return 1
}

wait_for_sse_method() {
  local method="$1"
  for _ in {1..100}; do
    if python3 - "$TMPDIR/sse.log" "$method" <<'PY'
import json
import sys

path, expected = sys.argv[1], sys.argv[2]
try:
    lines = open(path, encoding="utf-8").read().splitlines()
except FileNotFoundError:
    raise SystemExit(1)

for line in lines:
    line = line.lstrip("\x00")
    if not line.startswith("data:"):
        continue
    payload = line.removeprefix("data:").strip()
    if not payload:
        continue
    try:
        message = json.loads(payload)
    except json.JSONDecodeError:
        continue
    if message.get("method") == expected:
        raise SystemExit(0)
raise SystemExit(1)
PY
    then
      return 0
    fi
    sleep 0.05
  done
  echo "missing SSE method $method" >&2
  return 1
}

mcp_post() {
  local session="$1"
  local body="$2"
  local request_id
  request_id="$(python3 -c 'import secrets; print(secrets.token_hex(8))')"
  local out="$TMPDIR/body-$request_id.json"
  local headers="$TMPDIR/headers-$request_id.txt"
  local extra_headers=(
    -H "Authorization: Bearer $TOKEN"
    -H "Content-Type: application/json"
    -H "Accept: application/json, text/event-stream"
    -H "Origin: http://localhost:$HTTP_PORT"
  )
  if [[ -n "$session" ]]; then
    extra_headers+=(
      -H "MCP-Session-Id: $session"
      -H "MCP-Protocol-Version: 2025-11-25"
    )
  fi
  curl -fsS -D "$headers" -o "$out" -X POST "${extra_headers[@]}" --data "$body" "http://127.0.0.1:$HTTP_PORT/mcp"
  cat "$out"
}

mcp_init() {
  local version="${1:-2025-11-25}"
  local out="$TMPDIR/init-body.json"
  local headers="$TMPDIR/init-headers.txt"
  curl -fsS -D "$headers" -o "$out" -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "Origin: http://localhost:$HTTP_PORT" \
    --data "$(python3 -c 'import json, sys; print(json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":sys.argv[1],"capabilities":{},"clientInfo":{"name":"mcp-smoke","version":"0"}}}))' "$version")" \
    "http://127.0.0.1:$HTTP_PORT/mcp" >/dev/null
  assert_json 'data["result"]["protocolVersion"] == "'"$version"'" and data["result"]["capabilities"]["resources"]["subscribe"] is True and data["result"]["capabilities"]["resources"]["listChanged"] is True and "tools" in data["result"]["capabilities"]' <"$out"
  awk 'tolower($1)=="mcp-session-id:" {gsub("\r","",$2); print $2}' "$headers"
}

tool_call() {
  local session="$1"
  local id="$2"
  local name="$3"
  local args="$4"
  mcp_post "$session" "$(python3 -c 'import json, sys
print(json.dumps({"jsonrpc":"2.0","id":int(sys.argv[1]),"method":"tools/call","params":{"name":sys.argv[2],"arguments":json.loads(sys.argv[3])}}))' "$id" "$name" "$args")"
}

admin_http() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local args=(-fsS -H "Authorization: Bearer $TOKEN" -X "$method")
  if [[ -n "$body" ]]; then
    args+=(-H "Content-Type: application/json" --data "$body")
  fi
  curl "${args[@]}" "http://127.0.0.1:$HTTP_PORT$path"
}

participant_http() {
  local participant_token="$1"
  local method="$2"
  local path="$3"
  local body="${4:-}"
  local args=(-fsS -H "Authorization: Bearer $participant_token" -X "$method")
  if [[ -n "$body" ]]; then
    args+=(-H "Content-Type: application/json" --data "$body")
  fi
  curl "${args[@]}" "http://127.0.0.1:$HTTP_PORT$path"
}

PG_PORT="$(free_port)"
HTTP_PORT="$(free_port)"

"$POSTGRES_BIN/initdb" -D "$PGDATA" -A trust -U postgres >/dev/null
"$POSTGRES_BIN/pg_ctl" -D "$PGDATA" -o "-h 127.0.0.1 -p $PG_PORT" -l "$PGLOG" start >/dev/null
POSTGRES_PID=1
for _ in {1..100}; do
  if "$POSTGRES_BIN/pg_isready" -h 127.0.0.1 -p "$PG_PORT" -U postgres >/dev/null 2>&1; then
    break
  fi
  sleep 0.05
done
"$POSTGRES_BIN/createdb" -h 127.0.0.1 -p "$PG_PORT" -U postgres agent_mail_mcp_test

CARGO_TARGET_DIR="$CARGO_TARGET_DIR" cargo build --manifest-path "$ROOT/Cargo.toml" -p agent-mail-server >/dev/null
DATABASE_URL="postgres://postgres@127.0.0.1:$PG_PORT/agent_mail_mcp_test"
RUST_LOG=warn "$CARGO_TARGET_DIR/debug/agent-mail-server" \
  --database-url "$DATABASE_URL" \
  --bind "127.0.0.1:$HTTP_PORT" \
  --token "$TOKEN" \
  --credential-admin-token "$CREDENTIAL_ADMIN_TOKEN" >"$SERVERLOG" 2>&1 &
SERVER_PID=$!

for _ in {1..100}; do
  if curl -fsS "http://127.0.0.1:$HTTP_PORT/health" >/dev/null 2>&1; then
    break
  fi
  sleep 0.05
done

unauth_status="$(curl -sS -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$unauth_status" == "401" ]]
wrong_token_status="$(curl -sS -o /dev/null -w "%{http_code}" -X POST -H "Authorization: Bearer wrong" -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$wrong_token_status" == "401" ]]
bad_origin_status="$(curl -sS -o /dev/null -w "%{http_code}" -X POST -H "Authorization: Bearer $TOKEN" -H "Origin: https://evil.example" -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$bad_origin_status" == "403" ]]
curl -fsS -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data '{' "http://127.0.0.1:$HTTP_PORT/mcp" | assert_json 'data["error"]["code"] == -32700'
curl -fsS -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1}' "http://127.0.0.1:$HTTP_PORT/mcp" | assert_json 'data["error"]["code"] == -32600'

receiver_session="$(mcp_init)"
sender_session="$(mcp_init)"
[[ -n "$receiver_session" && -n "$sender_session" && "$receiver_session" != "$sender_session" ]]
legacy_session="$(mcp_init "2025-03-26")"
[[ -n "$legacy_session" ]]

unauth_sse_status="$(curl -m 2 -sS -o /dev/null -w "%{http_code}" -H "Accept: text/event-stream" -H "MCP-Session-Id: $receiver_session" "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$unauth_sse_status" == "401" ]]
wrong_token_sse_status="$(curl -m 2 -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer wrong" -H "Accept: text/event-stream" -H "MCP-Session-Id: $receiver_session" "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$wrong_token_sse_status" == "401" ]]
stale_session_status="$(curl -sS -o /dev/null -w "%{http_code}" -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -H "MCP-Session-Id: mcp-stale" -H "MCP-Protocol-Version: 2025-11-25" --data '{"jsonrpc":"2.0","id":99,"method":"ping"}' "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$stale_session_status" == "404" ]]
notification_status="$(curl -sS -D "$TMPDIR/notification-headers.txt" -o "$TMPDIR/notification-body.txt" -w "%{http_code}" -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -H "MCP-Session-Id: $receiver_session" -H "MCP-Protocol-Version: 2025-11-25" --data '{"jsonrpc":"2.0","method":"ping"}' "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$notification_status" == "202" ]]
[[ ! -s "$TMPDIR/notification-body.txt" ]]

mcp_post "$receiver_session" '{"jsonrpc":"2.0","method":"notifications/initialized"}' >/dev/null
mcp_post "$sender_session" '{"jsonrpc":"2.0","method":"notifications/initialized"}' >/dev/null

receiver_start="$(tool_call "$receiver_session" 2 agent_mail_start '{"role":"reviewer"}')"
receiver_identity="$(printf '%s' "$receiver_start" | python3 -c 'import json, sys; print(json.loads(json.load(sys.stdin)["result"]["content"][0]["text"])["identity"])')"
receiver_retry="$(tool_call "$receiver_session" 22 agent_mail_start '{"role":"reviewer"}')"
receiver_retry_identity="$(printf '%s' "$receiver_retry" | python3 -c 'import json, sys; print(json.loads(json.load(sys.stdin)["result"]["content"][0]["text"])["identity"])')"
[[ "$receiver_retry_identity" == "$receiver_identity" ]]
receiver_whitespace_retry="$(tool_call "$receiver_session" 24 agent_mail_start '{"role":" reviewer "}')"
receiver_whitespace_identity="$(printf '%s' "$receiver_whitespace_retry" | python3 -c 'import json, sys; print(json.loads(json.load(sys.stdin)["result"]["content"][0]["text"])["identity"])')"
[[ "$receiver_whitespace_identity" == "$receiver_identity" ]]
tool_call "$receiver_session" 23 agent_mail_start '{"role":"different-role"}' | assert_json 'data["error"]["message"].startswith("MCP session already started")'
sender_start="$(tool_call "$sender_session" 3 agent_mail_start '{"role":"sender"}')"
printf '%s' "$sender_start" | assert_json 'json.loads(data["result"]["content"][0]["text"])["role"] == "sender"'

concurrent_session="$(mcp_init)"
mcp_post "$concurrent_session" '{"jsonrpc":"2.0","method":"notifications/initialized"}' >/dev/null
tool_call "$concurrent_session" 60 agent_mail_start '{"role":"concurrent"}' >"$TMPDIR/concurrent-a.json" &
concurrent_a_pid=$!
tool_call "$concurrent_session" 61 agent_mail_start '{"role":"concurrent"}' >"$TMPDIR/concurrent-b.json" &
concurrent_b_pid=$!
wait "$concurrent_a_pid" "$concurrent_b_pid"
concurrent_a_identity="$(python3 -c 'import json, sys; print(json.loads(json.load(open(sys.argv[1]))["result"]["content"][0]["text"])["identity"])' "$TMPDIR/concurrent-a.json")"
concurrent_b_identity="$(python3 -c 'import json, sys; print(json.loads(json.load(open(sys.argv[1]))["result"]["content"][0]["text"])["identity"])' "$TMPDIR/concurrent-b.json")"
[[ "$concurrent_a_identity" == "$concurrent_b_identity" ]]
admin_http GET /v1/participants | assert_json 'sum(item["role"] == "concurrent" for item in data["participants"]) == 1'

curl -fsS -N \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: text/event-stream" \
  -H "MCP-Session-Id: $receiver_session" \
  -H "MCP-Protocol-Version: 2025-11-25" \
  -H "Origin: http://localhost:$HTTP_PORT" \
  "http://127.0.0.1:$HTTP_PORT/mcp" >"$TMPDIR/sse.log" &
SSE_PID=$!
sleep 0.2

admin_http POST /v1/projects '{"alias":"mcp-smoke","root":"/tmp/mcp-smoke"}' >/dev/null
wait_for_sse_method "notifications/resources/list_changed"

inbox_uri="agent-mail://projects/mcp-smoke/inbox?identity=$receiver_identity"
mcp_post "$receiver_session" "$(mcp_request resources/list 40 '{}')" | assert_json 'any(item["uri"] == "agent-mail://projects" for item in data["result"]["resources"]) and any(item["uri"] == "'"$inbox_uri"'" for item in data["result"]["resources"])'
mcp_post "$receiver_session" "$(mcp_request resources/templates/list 41 '{}')" | assert_json 'any(item["name"] == "project-inbox" for item in data["result"]["resourceTemplates"]) and any(item["name"] == "project-message" for item in data["result"]["resourceTemplates"])'
mcp_post "$receiver_session" "$(python3 -c 'import json, sys; print(json.dumps({"jsonrpc":"2.0","id":5,"method":"resources/subscribe","params":{"uri":sys.argv[1]}}))' "$inbox_uri")" | assert_json 'data["result"] == {}'

mcp_post "$sender_session" "$(mcp_request resources/read 50 "$(python3 -c 'import json, sys; print(json.dumps({"uri":sys.argv[1]}))' "$inbox_uri")")" | assert_json 'data["error"]["message"] == "forbidden"'
mcp_post "$sender_session" "$(mcp_request resources/subscribe 51 "$(python3 -c 'import json, sys; print(json.dumps({"uri":sys.argv[1]}))' "$inbox_uri")")" | assert_json 'data["error"]["message"] == "forbidden"'

http_sender="$(admin_http POST /v1/participants/start '{"identity":"http-sender","role":"http-sender"}')"
http_sender_token="$(printf '%s' "$http_sender" | json_get participant_token)"
: >"$TMPDIR/sse.log"
participant_http "$http_sender_token" POST /v1/messages '{"project":"mcp-smoke","to":"reviewer","subject":"MCP smoke","body":"real mcp body"}' >/dev/null
wait_for_sse_uri "$inbox_uri"

inbox_json="$(mcp_post "$receiver_session" "$(python3 -c 'import json, sys; print(json.dumps({"jsonrpc":"2.0","id":7,"method":"resources/read","params":{"uri":sys.argv[1]}}))' "$inbox_uri")")"
printf '%s' "$inbox_json" | assert_json 'json.loads(data["result"]["contents"][0]["text"])["unread_count"] == 1'
mail_id="$(printf '%s' "$inbox_json" | python3 -c 'import json, sys; data=json.loads(json.load(sys.stdin)["result"]["contents"][0]["text"]); print(data["messages"][0]["id"])')"

message_uri="agent-mail://projects/mcp-smoke/messages/$mail_id?identity=$receiver_identity"
mcp_post "$receiver_session" "$(python3 -c 'import json, sys; print(json.dumps({"jsonrpc":"2.0","id":42,"method":"resources/subscribe","params":{"uri":sys.argv[1]}}))' "$message_uri")" | assert_json 'data["result"] == {}'
mcp_post "$receiver_session" "$(python3 -c 'import json, sys; print(json.dumps({"jsonrpc":"2.0","id":8,"method":"resources/read","params":{"uri":sys.argv[1]}}))' "$message_uri")" | assert_json 'json.loads(data["result"]["contents"][0]["text"])["body"] == "real mcp body"'

tool_call "$receiver_session" 9 agent_mail_mark_read "$(python3 -c 'import json, sys; print(json.dumps({"project":"mcp-smoke","mail_id":sys.argv[1]}))' "$mail_id")" >/dev/null
wait_for_sse_uri "$message_uri"
mcp_post "$receiver_session" "$(python3 -c 'import json, sys; print(json.dumps({"jsonrpc":"2.0","id":10,"method":"resources/read","params":{"uri":sys.argv[1]}}))' "$inbox_uri")" | assert_json 'json.loads(data["result"]["contents"][0]["text"])["unread_count"] == 0'

delete_status="$(curl -sS -o /dev/null -w "%{http_code}" -X DELETE -H "Authorization: Bearer $TOKEN" -H "MCP-Session-Id: $sender_session" "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$delete_status" == "204" ]]
deleted_session_status="$(curl -sS -o /dev/null -w "%{http_code}" -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "MCP-Session-Id: $sender_session" --data '{"jsonrpc":"2.0","id":99,"method":"ping"}' "http://127.0.0.1:$HTTP_PORT/mcp")"
[[ "$deleted_session_status" == "404" ]]

TEST_PASSED=1
echo "real postgres/mcp test passed"
