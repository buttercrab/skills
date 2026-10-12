package frontagent

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"
)

type processLock struct {
	Identity  string `json:"identity"`
	PID       int    `json:"pid"`
	StartedAt string `json:"started_at"`
	LogPath   string `json:"log_path,omitempty"`
}

func acquireProcessLock(root, identity, name, liveMessage string) (func(), processLock, error) {
	if err := validateIdentity(identity); err != nil {
		return nil, processLock{}, err
	}
	dir, err := processLockDir(root, name)
	if err != nil {
		return nil, processLock{}, err
	}
	stateDir, err := stateRoot(root)
	if err != nil {
		return nil, processLock{}, err
	}
	if err := ensurePrivateDir(stateDir); err != nil {
		return nil, processLock{}, err
	}
	if err := ensurePrivateDir(dir); err != nil {
		return nil, processLock{}, err
	}
	path := filepath.Join(dir, identity+".json")
	lock := processLock{Identity: identity, PID: os.Getpid(), StartedAt: nowText()}
	if name == "wait-ready" {
		lock.LogPath = waitReadyLogPath(root, identity)
	}
	file, err := openPrivateFile(path, os.O_CREATE|os.O_RDWR)
	if err != nil {
		return nil, processLock{}, err
	}
	if err := syscall.Flock(int(file.Fd()), syscall.LOCK_EX|syscall.LOCK_NB); err != nil {
		existing, _ := readProcessLockFile(file)
		_ = file.Close()
		if errors.Is(err, syscall.EWOULDBLOCK) || errors.Is(err, syscall.EAGAIN) {
			return nil, processLock{}, fmt.Errorf(liveMessage, identity, existing.PID)
		}
		return nil, processLock{}, err
	}
	if err := writeProcessLockFile(file, lock); err != nil {
		_ = syscall.Flock(int(file.Fd()), syscall.LOCK_UN)
		_ = file.Close()
		return nil, processLock{}, err
	}
	return func() {
		_ = syscall.Flock(int(file.Fd()), syscall.LOCK_UN)
		_ = file.Close()
	}, lock, nil
}

func readProcessLock(path string) (processLock, error) {
	file, err := openPrivateFile(path, os.O_RDONLY)
	if err != nil {
		return processLock{}, err
	}
	defer file.Close()
	return readProcessLockFile(file)
}

func readProcessLockFile(file *os.File) (processLock, error) {
	if _, err := file.Seek(0, io.SeekStart); err != nil {
		return processLock{}, err
	}
	raw, err := io.ReadAll(file)
	if err != nil {
		return processLock{}, err
	}
	var lock processLock
	if err := json.Unmarshal(raw, &lock); err != nil {
		return processLock{}, err
	}
	return lock, nil
}

func writeProcessLockFile(file *os.File, lock processLock) error {
	raw, err := json.MarshalIndent(lock, "", "  ")
	if err != nil {
		return err
	}
	if err := file.Truncate(0); err != nil {
		return err
	}
	if _, err := file.Seek(0, io.SeekStart); err != nil {
		return err
	}
	if _, err := file.Write(append(raw, '\n')); err != nil {
		return err
	}
	return file.Sync()
}

func liveProcessLock(root, identity, name string) (processLock, bool, error) {
	if err := validateIdentity(identity); err != nil {
		return processLock{}, false, err
	}
	dir, err := processLockDir(root, name)
	if err != nil {
		return processLock{}, false, err
	}
	path := filepath.Join(dir, identity+".json")
	file, err := openPrivateFile(path, os.O_RDONLY)
	if errors.Is(err, os.ErrNotExist) {
		return processLock{}, false, nil
	}
	if err != nil {
		return processLock{}, false, err
	}
	defer file.Close()
	if err := syscall.Flock(int(file.Fd()), syscall.LOCK_EX|syscall.LOCK_NB); err != nil {
		if errors.Is(err, syscall.EWOULDBLOCK) || errors.Is(err, syscall.EAGAIN) {
			lock, readErr := readProcessLockFile(file)
			if readErr != nil {
				return processLock{}, false, readErr
			}
			return lock, true, nil
		}
		return processLock{}, false, err
	}
	defer syscall.Flock(int(file.Fd()), syscall.LOCK_UN)
	lock, readErr := readProcessLockFile(file)
	if readErr != nil {
		return processLock{}, false, nil
	}
	return lock, false, nil
}

func processLockDir(root, name string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, name), nil
}

func processAlive(pid int) bool {
	if pid <= 0 {
		return false
	}
	err := syscall.Kill(pid, 0)
	if err == nil {
		return true
	}
	return errors.Is(err, syscall.EPERM)
}

func frontAgentStateDir(root string) string {
	dir, err := stateRoot(root)
	if err != nil {
		return ".front-agent"
	}
	return dir
}

func waitReadyLogPath(root, identity string) string {
	return filepath.Join(frontAgentStateDir(root), identity+".wait-ready.log")
}
