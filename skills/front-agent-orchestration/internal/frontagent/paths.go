package frontagent

import (
	"os"
	"path/filepath"
	"strings"
)

func projectRoot(root string) (string, error) {
	if strings.TrimSpace(root) != "" {
		return filepath.Abs(root)
	}
	current, err := filepath.Abs(".")
	if err != nil {
		return "", err
	}
	for {
		if exists(filepath.Join(current, ".front-agent")) || exists(filepath.Join(current, ".git")) {
			return current, nil
		}
		parent := filepath.Dir(current)
		if parent == current {
			return filepath.Abs(".")
		}
		current = parent
	}
}

func stateRoot(root string) (string, error) {
	project, err := projectRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(project, ".front-agent"), nil
}

func exists(path string) bool {
	_, err := os.Lstat(path)
	return err == nil
}
