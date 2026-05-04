package main

import (
	"os"

	"front-agent-orchestration/internal/frontagent"
)

func main() {
	os.Exit(frontagent.Main(os.Args[1:], os.Stdin, os.Stdout, os.Stderr))
}
