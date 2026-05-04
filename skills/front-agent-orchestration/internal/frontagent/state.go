package frontagent

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

type state struct {
	Mode         string `json:"mode"`
	Identity     string `json:"identity"`
	PeerIdentity string `json:"peer_identity,omitempty"`
	Role         string `json:"role"`
	StartedAt    string `json:"started_at,omitempty"`
	PairedAt     string `json:"paired_at,omitempty"`
	LastReadyID  string `json:"last_ready_id,omitempty"`
}

func saveState(root string, st state) error {
	if err := validateState(st); err != nil {
		return err
	}
	dir, err := stateRoot(root)
	if err != nil {
		return err
	}
	if err := os.MkdirAll(dir, 0700); err != nil {
		return err
	}
	raw, err := json.MarshalIndent(st, "", "  ")
	if err != nil {
		return err
	}
	path := filepath.Join(dir, st.Identity+".json")
	tmp, err := os.CreateTemp(dir, "."+st.Identity+".*.tmp")
	if err != nil {
		return err
	}
	tmpPath := tmp.Name()
	if _, err := tmp.Write(append(raw, '\n')); err != nil {
		_ = tmp.Close()
		_ = os.Remove(tmpPath)
		return err
	}
	if err := tmp.Sync(); err != nil {
		_ = tmp.Close()
		_ = os.Remove(tmpPath)
		return err
	}
	if err := tmp.Close(); err != nil {
		_ = os.Remove(tmpPath)
		return err
	}
	if err := os.Rename(tmpPath, path); err != nil {
		_ = os.Remove(tmpPath)
		return err
	}
	if dirFile, err := os.Open(dir); err == nil {
		_ = dirFile.Sync()
		_ = dirFile.Close()
	}
	return nil
}

func selectState(root, identity, mode string, requirePaired bool) (state, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return state{}, err
	}
	if identity != "" {
		if err := validateIdentity(identity); err != nil {
			return state{}, err
		}
		return loadState(filepath.Join(dir, identity+".json"), mode, requirePaired)
	}
	entries, err := os.ReadDir(dir)
	if err != nil {
		return state{}, errors.New("front-agent state not found; run main or gateway pairing first")
	}
	var matches []state
	for _, entry := range entries {
		if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".json") {
			continue
		}
		st, err := loadState(filepath.Join(dir, entry.Name()), mode, requirePaired)
		if err == nil {
			matches = append(matches, st)
		}
	}
	sort.Slice(matches, func(i, j int) bool { return matches[i].Identity < matches[j].Identity })
	switch len(matches) {
	case 0:
		if mode == "" {
			return state{}, errors.New("no front-agent state found")
		}
		return state{}, fmt.Errorf("no front-agent %s state found", mode)
	case 1:
		return matches[0], nil
	default:
		return state{}, errors.New("multiple front-agent states found; pass --identity <id>")
	}
}

func loadState(path, mode string, requirePaired bool) (state, error) {
	raw, err := os.ReadFile(path)
	if err != nil {
		return state{}, err
	}
	var st state
	if err := json.Unmarshal(raw, &st); err != nil {
		return state{}, err
	}
	if mode != "" && st.Mode != mode {
		return state{}, fmt.Errorf("state mode is %s, want %s", st.Mode, mode)
	}
	if st.Identity == "" {
		return state{}, errors.New("front-agent state is missing identity")
	}
	if err := validateIdentity(st.Identity); err != nil {
		return state{}, err
	}
	if st.PeerIdentity != "" {
		if err := validateIdentity(st.PeerIdentity); err != nil {
			return state{}, err
		}
	}
	if err := validateModeRole(st); err != nil {
		return state{}, err
	}
	if requirePaired && (st.PeerIdentity == "" || st.PairedAt == "") {
		return state{}, errors.New("front-agent state is not paired")
	}
	return st, nil
}

func validateState(st state) error {
	if err := validateIdentity(st.Identity); err != nil {
		return err
	}
	if st.PeerIdentity != "" {
		if err := validateIdentity(st.PeerIdentity); err != nil {
			return err
		}
	}
	return validateModeRole(st)
}

func validateModeRole(st state) error {
	switch st.Mode {
	case "main":
		if st.Role != mainRole {
			return fmt.Errorf("main state role is %q, want %q", st.Role, mainRole)
		}
	case "gateway":
		if st.Role != gatewayRole {
			return fmt.Errorf("gateway state role is %q, want %q", st.Role, gatewayRole)
		}
	default:
		return fmt.Errorf("invalid front-agent mode %q", st.Mode)
	}
	return nil
}

func validateIdentity(identity string) error {
	if identity == "" {
		return errors.New("front-agent identity is required")
	}
	if strings.ContainsAny(identity, `/\`) || identity == "." || identity == ".." || strings.Contains(identity, "..") {
		return fmt.Errorf("unsafe front-agent identity %q", identity)
	}
	return nil
}
