package frontagent

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

type answerLedger struct {
	Answers map[string]string `json:"answers"`
}

func acquireAnswerLock(root, identity, questionID string) (func(), error) {
	if err := validateIdentity(identity); err != nil {
		return nil, err
	}
	if err := validateMailID(questionID); err != nil {
		return nil, err
	}
	sum := sha256.Sum256([]byte(identity + "\x00" + questionID))
	key := "answer-" + hex.EncodeToString(sum[:12])
	release, _, err := acquireProcessLock(root, key, "answer-locks", "front-agent answer send already running for question %s with pid %d")
	return release, err
}

func recordedAnswer(root, identity, questionID string) (string, error) {
	ledger, err := loadAnswerLedger(root, identity)
	if err != nil {
		return "", err
	}
	return ledger.Answers[questionID], nil
}

func recordAnswer(root, identity, questionID, answerID string) error {
	if err := validateMailID(questionID); err != nil {
		return err
	}
	if err := validateMailID(answerID); err != nil {
		return err
	}
	ledger, err := loadAnswerLedger(root, identity)
	if err != nil {
		return err
	}
	if previous := ledger.Answers[questionID]; previous != "" && previous != answerID {
		return fmt.Errorf("question %s already has answer %s", questionID, previous)
	}
	ledger.Answers[questionID] = answerID
	return saveAnswerLedger(root, identity, ledger)
}

func loadAnswerLedger(root, identity string) (answerLedger, error) {
	if err := validateIdentity(identity); err != nil {
		return answerLedger{}, err
	}
	ledger := answerLedger{Answers: map[string]string{}}
	dir, err := answerLedgerDir(root)
	if err != nil {
		return answerLedger{}, err
	}
	file, err := openPrivateFile(filepath.Join(dir, identity+".json"), os.O_RDONLY)
	if errors.Is(err, os.ErrNotExist) {
		return ledger, nil
	}
	if err != nil {
		return answerLedger{}, err
	}
	defer file.Close()
	raw, err := io.ReadAll(io.LimitReader(file, 2<<20))
	if err != nil {
		return answerLedger{}, err
	}
	if err := json.Unmarshal(raw, &ledger); err != nil {
		return answerLedger{}, err
	}
	if ledger.Answers == nil {
		ledger.Answers = map[string]string{}
	}
	return ledger, nil
}

func saveAnswerLedger(root, identity string, ledger answerLedger) error {
	dir, err := answerLedgerDir(root)
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
	raw, err := json.MarshalIndent(ledger, "", "  ")
	if err != nil {
		return err
	}
	tmp, err := os.CreateTemp(dir, "."+identity+".*.tmp")
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
	return os.Rename(tmpPath, filepath.Join(dir, identity+".json"))
}

func answerLedgerDir(root string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "answers"), nil
}
