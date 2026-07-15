#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOKEN="real-test-token"
CREDENTIAL_ADMIN_TOKEN="real-test-credential-admin-token"
if [[ "${HERMETIC_RUN_ACTIVE:-}" != "1" || -z "${RUN_ROOT:-}" ]]; then
  echo "real PostgreSQL tests require tests/hermetic_run.sh and its RUN_ROOT" >&2
  exit 2
fi
[[ -d "$RUN_ROOT" && ! -L "$RUN_ROOT" ]] || { echo "unsafe RUN_ROOT: $RUN_ROOT" >&2; exit 2; }
RUN_ROOT="$(cd "$RUN_ROOT" && pwd -P)"
CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$RUN_ROOT/cargo-target}"
[[ "$CARGO_TARGET_DIR" == "$RUN_ROOT/"* ]] || { echo "CARGO_TARGET_DIR escaped RUN_ROOT" >&2; exit 2; }
TEST_ROOT="$(mktemp -d "$RUN_ROOT/agent-mail-http.XXXXXX")"
mkdir -m 700 "$TEST_ROOT/tmp"
export TMPDIR="$TEST_ROOT/tmp"
TEST_PASSED=0
if [[ "${AGENT_MAIL_TEST_FAIL_AT:-}" == "before-postgres" ]]; then
  echo "injected failure before PostgreSQL startup: $TEST_ROOT" >&2
  exit 97
fi
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
for tool in initdb pg_ctl pg_isready createdb psql; do
  [[ -x "$POSTGRES_BIN/$tool" ]] || { echo "missing PostgreSQL tool: $POSTGRES_BIN/$tool" >&2; exit 2; }
done
PGDATA="$TEST_ROOT/pgdata"
PGLOG="$TEST_ROOT/postgres.log"
SERVERLOG="$TEST_ROOT/server.log"

cleanup() {
  local status=$?
  trap - EXIT
  if [[ $status -eq 0 && $TEST_PASSED -ne 1 ]]; then
    status=1
  fi
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  if [[ -n "${POSTGRES_PID:-}" ]]; then
    "$POSTGRES_BIN/pg_ctl" -D "$PGDATA" -m fast stop >/dev/null 2>&1 || true
  fi
  if [[ $status -ne 0 ]]; then
    echo "test root: $TEST_ROOT" >&2
    echo "postgres log: $PGLOG" >&2
    echo "server log: $SERVERLOG" >&2
    [[ -f "$PGLOG" ]] && tail -n 80 "$PGLOG" >&2
    [[ -f "$SERVERLOG" ]] && tail -n 80 "$SERVERLOG" >&2
  fi
  exit "$status"
}
trap cleanup EXIT

free_port() {
  python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()'
}

json_get() {
  python3 -c 'import json, sys; print(json.load(sys.stdin)[sys.argv[1]])' "$1"
}

assert_json() {
  python3 -c 'import json, sys
data = json.load(sys.stdin)
expr = sys.argv[1]
if not eval(expr, {}, {"data": data}):
    raise SystemExit(f"assertion failed: {expr}\n{json.dumps(data, indent=2)}")' "$1"
}

request() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  if [[ -n "$body" ]]; then
    curl -fsS \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -X "$method" \
      --data "$body" \
      "http://127.0.0.1:$HTTP_PORT$path"
  else
    curl -fsS \
      -H "Authorization: Bearer $TOKEN" \
      -X "$method" \
      "http://127.0.0.1:$HTTP_PORT$path"
  fi
}

participant_request() {
  local token="$1"
  local method="$2"
  local path="$3"
  local body="${4:-}"
  local args=(-fsS -H "Authorization: Bearer $token" -X "$method")
  if [[ -n "$body" ]]; then
    args+=(-H "Content-Type: application/json" --data "$body")
  fi
  curl "${args[@]}" "http://127.0.0.1:$HTTP_PORT$path"
}

credential_admin_request() {
  local identity="$1"
  curl -fsS \
    -H "Authorization: Bearer $CREDENTIAL_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -X POST \
    "http://127.0.0.1:$HTTP_PORT/v1/participants/$identity/credential"
}

PG_PORT="$(free_port)"
HTTP_PORT="$(free_port)"

"$POSTGRES_BIN/initdb" -D "$PGDATA" -A trust -U postgres >/dev/null
"$POSTGRES_BIN/pg_ctl" -D "$PGDATA" -o "-h 127.0.0.1 -p $PG_PORT -c unix_socket_directories=''" -l "$PGLOG" start >/dev/null
POSTGRES_PID=1
if [[ "${AGENT_MAIL_TEST_FAIL_AT:-}" == "after-postgres" ]]; then
  echo "injected failure after PostgreSQL startup: $TEST_ROOT" >&2
  exit 98
fi
for _ in {1..100}; do
  if "$POSTGRES_BIN/pg_isready" -h 127.0.0.1 -p "$PG_PORT" -U postgres >/dev/null 2>&1; then
    break
  fi
  sleep 0.05
done
"$POSTGRES_BIN/createdb" -h 127.0.0.1 -p "$PG_PORT" -U postgres agent_mail_real_test
DATABASE_URL="postgres://postgres@127.0.0.1:$PG_PORT/agent_mail_real_test"
SCHEMA_SQL="$TEST_ROOT/schema.sql"
printf '%s\n' \
  "CREATE TABLE participants (" \
  "  identity TEXT PRIMARY KEY," \
  "  role TEXT NOT NULL," \
  "  created_at TEXT NOT NULL," \
  "  updated_at TEXT NOT NULL" \
  ");" \
  "CREATE TABLE projects (" \
  "  alias TEXT PRIMARY KEY," \
  "  root TEXT NOT NULL DEFAULT ''," \
  "  created_at TEXT NOT NULL" \
  ");" \
  "CREATE TABLE messages (" \
  "  id TEXT PRIMARY KEY," \
  "  project_alias TEXT NOT NULL REFERENCES projects(alias) ON DELETE CASCADE," \
  "  sender_identity TEXT NOT NULL REFERENCES participants(identity)," \
  "  sender_role TEXT NOT NULL," \
  "  recipient_kind TEXT NOT NULL CHECK (recipient_kind IN ('identity', 'role', 'broadcast'))," \
  "  recipient TEXT NOT NULL," \
  "  subject TEXT NOT NULL," \
  "  body TEXT NOT NULL," \
  "  created_at TEXT NOT NULL," \
  "  created_at_ns BIGINT NOT NULL" \
  ");" \
  "CREATE TABLE receipts (" \
  "  message_id TEXT NOT NULL REFERENCES messages(id) ON DELETE CASCADE," \
  "  identity TEXT NOT NULL REFERENCES participants(identity) ON DELETE CASCADE," \
  "  read_at TEXT NOT NULL," \
  "  PRIMARY KEY(message_id, identity)" \
  ");" \
  "INSERT INTO participants(identity, role, created_at, updated_at) VALUES" \
  "  ('legacy-sender', 'legacy-sender', '2026-01-01T00:00:00.000000000Z', '2026-01-01T00:00:00.000000000Z')," \
  "  ('legacy-001', 'legacy', '2026-01-01T00:00:00.000000000Z', '2026-01-01T00:00:00.000000000Z');" \
  "INSERT INTO projects(alias, root, created_at) VALUES" \
  "  ('legacy', '/srv/legacy', '2026-01-01T00:00:00.000000000Z');" \
  "INSERT INTO messages(id, project_alias, sender_identity, sender_role, recipient_kind, recipient, subject, body, created_at, created_at_ns) VALUES" \
  "  ('mail-legacy-001', 'legacy', 'legacy-sender', 'legacy-sender', 'identity', 'legacy-001', 'Legacy mail', 'legacy body', '2026-01-01T00:00:00.000000000Z', 1);" \
  >"$SCHEMA_SQL"
"$POSTGRES_BIN/psql" "$DATABASE_URL" -v ON_ERROR_STOP=1 -q -f "$SCHEMA_SQL"

CARGO_TARGET_DIR="$CARGO_TARGET_DIR" cargo build --manifest-path "$ROOT/Cargo.toml" -p agent-mail-server >/dev/null
if "$CARGO_TARGET_DIR/debug/agent-mail-server" \
  --database-url "postgres://127.0.0.1:1/unused" \
  --token "same-secret" \
  --credential-admin-token "same-secret" >"$TMPDIR/equal-token.log" 2>&1; then
  echo "server accepted equal service and credential-administration tokens" >&2
  exit 1
fi
grep -q "must differ from AGENT_MAIL_TOKEN" "$TMPDIR/equal-token.log"
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

unauth_status="$(
  curl -sS -o /dev/null -w "%{http_code}" "http://127.0.0.1:$HTTP_PORT/v1/projects"
)"
[[ "$unauth_status" == "401" ]]

sender_start="$(request POST /v1/participants/start '{"identity":"sender-001","role":"sender"}')"
sender_token="$(printf '%s' "$sender_start" | json_get participant_token)"
printf '%s' "$sender_start" | assert_json 'data["identity"] == "sender-001" and data["role"] == "sender" and data["participant_token"].startswith("amp_")'
reviewer_start="$(request POST /v1/participants/start '{"identity":"reviewer-001","role":"reviewer"}')"
reviewer_token="$(printf '%s' "$reviewer_start" | json_get participant_token)"
printf '%s' "$reviewer_start" | assert_json 'data["identity"] == "reviewer-001" and data["role"] == "reviewer" and data["participant_token"].startswith("amp_")'
duplicate_identity_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -X POST --data '{"identity":"reviewer-001","role":"reviewer"}' "http://127.0.0.1:$HTTP_PORT/v1/participants/start")"
[[ "$duplicate_identity_status" == "409" ]]
request POST /v1/projects '{"alias":"alpha","root":"/srv/alpha"}' | assert_json 'data["alias"] == "alpha"'
request POST /v1/projects '{"alias":"beta","root":"/srv/beta"}' | assert_json 'data["alias"] == "beta"'
request POST /v1/projects '{"alias":"paged","root":"/srv/paged"}' | assert_json 'data["alias"] == "paged"'

legacy_credential="$(credential_admin_request legacy-001)"
legacy_token="$(printf '%s' "$legacy_credential" | json_get participant_token)"
participant_request "$legacy_token" GET /v1/projects/legacy/participants/legacy-001/inbox | assert_json 'data["identity"] == "legacy-001" and data["unread_count"] == 1 and data["messages"][0]["id"] == "mail-legacy-001"'
rotated_credential="$(credential_admin_request legacy-001)"
rotated_token="$(printf '%s' "$rotated_credential" | json_get participant_token)"
[[ "$rotated_token" != "$legacy_token" ]]
revoked_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $legacy_token" "http://127.0.0.1:$HTTP_PORT/v1/projects/legacy/participants/legacy-001/inbox")"
[[ "$revoked_status" == "401" ]]
participant_request "$rotated_token" GET /v1/projects/legacy/participants/legacy-001/inbox | assert_json 'data["identity"] == "legacy-001" and "body" not in data["messages"][0]'

alpha_message="$(
  participant_request "$sender_token" POST /v1/messages '{"project":"alpha","to_kind":"role","to":"reviewer","subject":"Alpha review","body":"alpha body","idempotency_key":"answer:alpha-001"}'
)"
alpha_id="$(printf '%s' "$alpha_message" | json_get id)"
alpha_retry="$(participant_request "$sender_token" POST /v1/messages '{"project":"alpha","to_kind":"role","to":"reviewer","subject":"Alpha review","body":"alpha body","idempotency_key":"answer:alpha-001"}')"
[[ "$(printf '%s' "$alpha_retry" | json_get id)" == "$alpha_id" ]]
idempotency_conflict_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $sender_token" -H "Content-Type: application/json" -X POST --data '{"project":"alpha","to_kind":"role","to":"reviewer","subject":"Changed","body":"alpha body","idempotency_key":"answer:alpha-001"}' "http://127.0.0.1:$HTTP_PORT/v1/messages")"
[[ "$idempotency_conflict_status" == "409" ]]
participant_request "$sender_token" POST /v1/messages '{"project":"beta","to_kind":"role","to":"reviewer","subject":"Beta review","body":"beta body","idempotency_key":"answer:alpha-001"}' >/dev/null

for page_number in 1 2 3 4 5; do
  participant_request "$sender_token" POST /v1/messages "{\"project\":\"paged\",\"to_kind\":\"identity\",\"to\":\"reviewer-001\",\"subject\":\"Page $page_number\",\"body\":\"page body $page_number\",\"idempotency_key\":\"page:$page_number\"}" >/dev/null
done
page_one="$(participant_request "$reviewer_token" GET '/v1/projects/paged/participants/reviewer-001/inbox?limit=2')"
printf '%s' "$page_one" | assert_json 'data["unread_count"] == 5 and len(data["messages"]) == 2 and [item["subject"] for item in data["messages"]] == ["Page 1", "Page 2"] and "next_cursor" in data'
page_one_cursor="$(printf '%s' "$page_one" | json_get next_cursor)"
page_two="$(participant_request "$reviewer_token" GET "/v1/projects/paged/participants/reviewer-001/inbox?limit=2&cursor=$page_one_cursor")"
printf '%s' "$page_two" | assert_json 'data["unread_count"] == 5 and len(data["messages"]) == 2 and [item["subject"] for item in data["messages"]] == ["Page 3", "Page 4"] and "next_cursor" in data'
page_two_cursor="$(printf '%s' "$page_two" | json_get next_cursor)"
page_three="$(participant_request "$reviewer_token" GET "/v1/projects/paged/participants/reviewer-001/inbox?limit=2&cursor=$page_two_cursor")"
printf '%s' "$page_three" | assert_json 'data["unread_count"] == 5 and len(data["messages"]) == 1 and data["messages"][0]["subject"] == "Page 5" and "next_cursor" not in data'
participant_request "$reviewer_token" GET /v1/projects/paged/participants/reviewer-001/inbox | assert_json 'data["unread_count"] == 5 and len(data["messages"]) == 5 and "next_cursor" not in data'
for invalid_query in 'limit=0' 'limit=201' 'cursor=not-hex'; do
  invalid_page_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $reviewer_token" "http://127.0.0.1:$HTTP_PORT/v1/projects/paged/participants/reviewer-001/inbox?$invalid_query")"
  [[ "$invalid_page_status" == "400" ]]
done

participant_request "$reviewer_token" GET /v1/projects/alpha/participants/reviewer-001/inbox | assert_json 'data["unread_count"] == 1 and data["messages"][0]["project"] == "alpha"'
participant_request "$reviewer_token" GET /v1/projects/beta/participants/reviewer-001/inbox | assert_json 'data["unread_count"] == 1 and data["messages"][0]["project"] == "beta"'
participant_request "$reviewer_token" GET "/v1/projects/alpha/messages/$alpha_id?identity=reviewer-001" | assert_json 'data["body"] == "alpha body"'
participant_request "$reviewer_token" POST "/v1/projects/alpha/messages/$alpha_id/read" '{"identity":"reviewer-001"}' | assert_json 'data["marked_read"]'
participant_request "$reviewer_token" GET /v1/projects/alpha/participants/reviewer-001/inbox | assert_json 'data["unread_count"] == 0'
participant_request "$reviewer_token" GET /v1/projects/beta/participants/reviewer-001/inbox | assert_json 'data["unread_count"] == 1'

forbidden_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $sender_token" "http://127.0.0.1:$HTTP_PORT/v1/projects/beta/participants/reviewer-001/inbox")"
[[ "$forbidden_status" == "403" ]]
admin_read_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "http://127.0.0.1:$HTTP_PORT/v1/projects/beta/participants/reviewer-001/inbox")"
[[ "$admin_read_status" == "401" ]]
impersonation_status="$(curl -sS -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $sender_token" -H "Content-Type: application/json" -X POST --data '{"sender_identity":"reviewer-001","project":"beta","to":"sender","subject":"forged","body":"forged"}' "http://127.0.0.1:$HTTP_PORT/v1/messages")"
[[ "$impersonation_status" == "403" ]]

[[ "$(curl -sS -o /dev/null -w "%{http_code}" "http://127.0.0.1:$HTTP_PORT/live")" == "200" ]]
[[ "$(curl -sS -o /dev/null -w "%{http_code}" "http://127.0.0.1:$HTTP_PORT/ready")" == "200" ]]
"$POSTGRES_BIN/pg_ctl" -D "$PGDATA" -m fast stop >/dev/null
POSTGRES_PID=""
[[ "$(curl -m 5 -sS -o /dev/null -w "%{http_code}" "http://127.0.0.1:$HTTP_PORT/live")" == "200" ]]
[[ "$(curl -m 5 -sS -o /dev/null -w "%{http_code}" "http://127.0.0.1:$HTTP_PORT/ready")" == "503" ]]

TEST_PASSED=1
echo "real postgres/http test passed"
