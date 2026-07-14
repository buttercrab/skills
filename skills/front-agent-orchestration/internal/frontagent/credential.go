package frontagent

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"syscall"
)

type participantCredential struct {
	Identity string `json:"identity"`
	Token    string `json:"participant_token"`
}

func saveParticipantCredential(root string, session mailSession) error {
	if err := validateIdentity(session.Identity); err != nil {
		return err
	}
	if strings.TrimSpace(session.ParticipantToken) == "" {
		return fmt.Errorf("Agent Mail did not return a participant credential")
	}
	dir, err := credentialDir(root)
	if err != nil {
		return err
	}
	stateDir, err := stateRoot(root)
	if err != nil {
		return err
	}
	if err := ensurePrivateDir(stateDir); err != nil {
		return err
	}
	if err := ensurePrivateDir(dir); err != nil {
		return err
	}
	raw, err := json.MarshalIndent(participantCredential{Identity: session.Identity, Token: session.ParticipantToken}, "", "  ")
	if err != nil {
		return err
	}
	tmp, err := os.CreateTemp(dir, "."+session.Identity+".*.tmp")
	if err != nil {
		return err
	}
	tmpPath := tmp.Name()
	defer os.Remove(tmpPath)
	if err := tmp.Chmod(0600); err != nil {
		_ = tmp.Close()
		return err
	}
	if _, err := tmp.Write(append(raw, '\n')); err != nil {
		_ = tmp.Close()
		return err
	}
	if err := tmp.Sync(); err != nil {
		_ = tmp.Close()
		return err
	}
	if err := tmp.Close(); err != nil {
		return err
	}
	return os.Rename(tmpPath, filepath.Join(dir, session.Identity+".json"))
}

func loadParticipantToken(root, identity string) (string, error) {
	if err := validateIdentity(identity); err != nil {
		return "", err
	}
	dir, err := credentialDir(root)
	if err != nil {
		return "", err
	}
	path := filepath.Join(dir, identity+".json")
	file, err := openPrivateFile(path, os.O_RDONLY)
	if err != nil {
		return "", fmt.Errorf("participant credential for %s is unavailable: %w", identity, err)
	}
	defer file.Close()
	info, err := file.Stat()
	if err != nil {
		return "", err
	}
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok || int(stat.Uid) != os.Getuid() || info.Mode().Perm()&0077 != 0 {
		return "", fmt.Errorf("participant credential for %s has unsafe ownership or permissions", identity)
	}
	raw, err := io.ReadAll(io.LimitReader(file, 64<<10))
	if err != nil {
		return "", err
	}
	var credential participantCredential
	if err := json.Unmarshal(raw, &credential); err != nil {
		return "", fmt.Errorf("participant credential for %s is invalid", identity)
	}
	if credential.Identity != identity || strings.TrimSpace(credential.Token) == "" {
		return "", fmt.Errorf("participant credential for %s does not match identity", identity)
	}
	return credential.Token, nil
}

func credentialDir(root string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "credentials"), nil
}
