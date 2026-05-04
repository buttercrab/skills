package frontagent

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"syscall"
	"time"
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
	if err := os.MkdirAll(dir, 0700); err != nil {
		return nil, processLock{}, err
	}
	path := filepath.Join(dir, identity+".json")
	lock := processLock{Identity: identity, PID: os.Getpid(), StartedAt: nowText()}
	if name == "wait-ready" {
		lock.LogPath = waitReadyLogPath(root, identity)
	}
	raw, err := json.MarshalIndent(lock, "", "  ")
	if err != nil {
		return nil, processLock{}, err
	}
	raw = append(raw, '\n')

	for {
		tmp, err := os.CreateTemp(dir, "."+identity+".*.tmp")
		if err != nil {
			return nil, processLock{}, err
		}
		tmpPath := tmp.Name()
		if _, err := tmp.Write(raw); err != nil {
			_ = tmp.Close()
			_ = os.Remove(tmpPath)
			return nil, processLock{}, err
		}
		if err := tmp.Close(); err != nil {
			_ = os.Remove(tmpPath)
			return nil, processLock{}, err
		}
		err = os.Link(tmpPath, path)
		_ = os.Remove(tmpPath)
		if err == nil {
			return func() {
				current, err := readProcessLock(path)
				if err == nil && current.PID == os.Getpid() {
					_ = os.Remove(path)
				}
			}, lock, nil
		}
		if !errors.Is(err, os.ErrExist) {
			return nil, processLock{}, err
		}
		existing, rawExisting, readErr := readProcessLockRaw(path)
		if readErr != nil {
			info, statErr := os.Stat(path)
			if statErr == nil && time.Since(info.ModTime()) < 2*time.Second {
				return nil, processLock{}, fmt.Errorf(liveMessage, identity, 0)
			}
			if rawExisting == nil {
				return nil, processLock{}, readErr
			}
		}
		if readErr == nil && processAlive(existing.PID) {
			return nil, processLock{}, fmt.Errorf(liveMessage, identity, existing.PID)
		}
		removed, removeErr := removeProcessLockIfUnchanged(path, rawExisting)
		if removeErr != nil {
			return nil, processLock{}, removeErr
		}
		if !removed {
			continue
		}
	}
}

func readProcessLock(path string) (processLock, error) {
	lock, _, err := readProcessLockRaw(path)
	return lock, err
}

func readProcessLockRaw(path string) (processLock, []byte, error) {
	raw, err := os.ReadFile(path)
	if err != nil {
		return processLock{}, nil, err
	}
	var lock processLock
	if err := json.Unmarshal(raw, &lock); err != nil {
		return processLock{}, raw, err
	}
	return lock, raw, nil
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
	lock, raw, err := readProcessLockRaw(path)
	if errors.Is(err, os.ErrNotExist) {
		return processLock{}, false, nil
	}
	if err != nil {
		return processLock{}, false, err
	}
	if processAlive(lock.PID) {
		return lock, true, nil
	}
	if _, removeErr := removeProcessLockIfUnchanged(path, raw); removeErr != nil {
		return processLock{}, false, removeErr
	}
	return lock, false, nil
}

func removeProcessLockIfUnchanged(path string, expected []byte) (bool, error) {
	current, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return true, nil
	}
	if err != nil {
		return false, err
	}
	if string(current) != string(expected) {
		return false, nil
	}
	if err := os.Remove(path); err != nil && !errors.Is(err, os.ErrNotExist) {
		return false, err
	}
	return true, nil
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
