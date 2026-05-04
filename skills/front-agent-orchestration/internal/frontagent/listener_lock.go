package frontagent

import "path/filepath"

type listenerLock = processLock

func acquireListenerLock(root, identity string) (func(), error) {
	release, _, err := acquireProcessLock(root, identity, "listeners", "front-agent listen already running for identity %s with pid %d")
	if err != nil {
		return nil, err
	}
	return release, nil
}

func readListenerLock(path string) (listenerLock, error) {
	return readProcessLock(path)
}

func listenerLockDir(root string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "listeners"), nil
}
