.PHONY: build test real-test mcp-test public-mcp-smoke

build:
	cargo build -p agent-mail-server

test:
	cargo test --workspace

real-test:
	./scripts/real_postgres_http_test.sh
	./scripts/real_postgres_mcp_test.sh

mcp-test:
	./scripts/real_postgres_mcp_test.sh

public-mcp-smoke:
	./scripts/public_mcp_smoke.sh
