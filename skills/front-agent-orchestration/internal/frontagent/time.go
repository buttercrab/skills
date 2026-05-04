package frontagent

import (
	"fmt"
	"time"
)

func nowText() string {
	return time.Now().UTC().Format(time.RFC3339)
}

func validateNotStale(meta map[string]string, startedAt string) error {
	if startedAt == "" {
		return fmt.Errorf("state is missing freshness timestamp")
	}
	if meta["created_at"] == "" {
		return fmt.Errorf("message %s is missing created_at", meta["id"])
	}
	created, err := time.Parse(time.RFC3339Nano, meta["created_at"])
	if err != nil {
		return fmt.Errorf("message %s has invalid created_at: %w", meta["id"], err)
	}
	started, err := time.Parse(time.RFC3339Nano, startedAt)
	if err != nil {
		return fmt.Errorf("state has invalid freshness timestamp: %w", err)
	}
	if created.Before(started) {
		return fmt.Errorf("message %s was created before current pairing started", meta["id"])
	}
	return nil
}
