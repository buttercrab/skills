.PHONY: build test real-test

build:
	cargo build -p agent-mail-server

test:
	cargo test --workspace

real-test:
	./scripts/real_postgres_http_test.sh
