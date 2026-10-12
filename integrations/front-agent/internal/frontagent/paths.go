package frontagent

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"syscall"
)

func projectRoot(root string) (string, error) {
	if strings.TrimSpace(root) != "" {
		return canonicalDirectory(root)
	}
	current, err := canonicalDirectory(".")
	if err != nil {
		return "", err
	}
	for {
		statePath := filepath.Join(current, ".front-agent")
		if exists(statePath) {
			if err := validatePrivateDirectory(statePath, false); err != nil {
				return "", err
			}
			return current, nil
		}
		if exists(filepath.Join(current, ".git")) {
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
	dir := filepath.Join(project, ".front-agent")
	if exists(dir) {
		if err := validatePrivateDirectory(dir, true); err != nil {
			return "", err
		}
	}
	return dir, nil
}

func exists(path string) bool {
	_, err := os.Lstat(path)
	return err == nil
}

func canonicalDirectory(path string) (string, error) {
	abs, err := filepath.Abs(path)
	if err != nil {
		return "", err
	}
	resolved, err := filepath.EvalSymlinks(abs)
	if err != nil {
		return "", err
	}
	info, err := os.Stat(resolved)
	if err != nil {
		return "", err
	}
	if !info.IsDir() {
		return "", fmt.Errorf("project root is not a directory: %s", resolved)
	}
	return resolved, nil
}

func ensurePrivateDir(path string) error {
	if err := os.Mkdir(path, 0700); err != nil && !errors.Is(err, os.ErrExist) {
		return err
	}
	if err := validatePrivateDirectory(path, true); err != nil {
		return err
	}
	if err := os.Chmod(path, 0700); err != nil {
		return err
	}
	if filepath.Base(path) == ".front-agent" {
		ignore, err := openPrivateFile(filepath.Join(path, ".gitignore"), os.O_CREATE|os.O_WRONLY|os.O_TRUNC)
		if err != nil {
			return err
		}
		if _, err := ignore.WriteString("*\n!.gitignore\n"); err != nil {
			_ = ignore.Close()
			return err
		}
		if err := ignore.Close(); err != nil {
			return err
		}
	}
	return nil
}

func validatePrivateDirectory(path string, requireOwner bool) error {
	info, err := os.Lstat(path)
	if err != nil {
		return err
	}
	if info.Mode()&os.ModeSymlink != 0 {
		return fmt.Errorf("front-agent refuses symlinked runtime directory %s", path)
	}
	if !info.IsDir() {
		return fmt.Errorf("front-agent runtime path is not a directory: %s", path)
	}
	if requireOwner {
		stat, ok := info.Sys().(*syscall.Stat_t)
		if !ok || int(stat.Uid) != os.Getuid() {
			return fmt.Errorf("front-agent runtime directory is not owned by the current user: %s", path)
		}
		if info.Mode().Perm()&0077 != 0 {
			return fmt.Errorf("front-agent runtime directory has unsafe permissions: %s", path)
		}
	}
	return nil
}

func openPrivateFile(path string, flags int) (*os.File, error) {
	fd, err := syscall.Open(path, flags|syscall.O_NOFOLLOW, 0600)
	if err != nil {
		return nil, err
	}
	file := os.NewFile(uintptr(fd), path)
	if file == nil {
		_ = syscall.Close(fd)
		return nil, fmt.Errorf("failed to open %s", path)
	}
	if err := file.Chmod(0600); err != nil {
		_ = file.Close()
		return nil, err
	}
	return file, nil
}

func openPrivateRegularFileForRead(path string) (*os.File, error) {
	fd, err := syscall.Open(path, syscall.O_RDONLY|syscall.O_NONBLOCK|syscall.O_NOFOLLOW, 0)
	if err != nil {
		return nil, err
	}
	file := os.NewFile(uintptr(fd), path)
	if file == nil {
		_ = syscall.Close(fd)
		return nil, fmt.Errorf("failed to open %s", path)
	}
	info, err := file.Stat()
	if err != nil {
		_ = file.Close()
		return nil, err
	}
	if !info.Mode().IsRegular() {
		_ = file.Close()
		return nil, fmt.Errorf("front-agent runtime file is not regular: %s", path)
	}
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok || int(stat.Uid) != os.Getuid() {
		_ = file.Close()
		return nil, fmt.Errorf("front-agent runtime file is not owned by the current user: %s", path)
	}
	if info.Mode().Perm()&0077 != 0 {
		_ = file.Close()
		return nil, fmt.Errorf("front-agent runtime file has unsafe permissions: %s", path)
	}
	return file, nil
}
