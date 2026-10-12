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
	"strconv"
	"strings"
)

type idempotencyRecord struct {
	Key         string `json:"key"`
	PayloadHash string `json:"payload_hash"`
	Status      string `json:"status"`
	Generation  int    `json:"generation,omitempty"`
}

type idempotencyLedger struct {
	Records map[string]idempotencyRecord `json:"records"`
}

func prepareIdempotentSend(root, identity, to, subject string, env envelope) (string, func(), error) {
	locator, payloadHash, key, err := idempotentSendIdentity(to, subject, env)
	if err != nil {
		return "", nil, err
	}
	lockSum := sha256.Sum256([]byte(identity + "\x00" + locator))
	lockID := "send-" + hex.EncodeToString(lockSum[:12])
	release, _, err := acquireProcessLock(root, lockID, "send-locks", "front-agent send already running for operation %s with pid %d")
	if err != nil {
		return "", nil, err
	}
	ledger, err := loadIdempotencyLedger(root, identity)
	if err != nil {
		release()
		return "", nil, err
	}
	if existing, ok := ledger.Records[locator]; ok {
		if existing.PayloadHash != payloadHash {
			release()
			return "", nil, fmt.Errorf("idempotent send %s was already prepared with different payload", locator)
		}
		if env.RespondsTo == "" && existing.Status == "complete" {
			existing.Generation++
			existing.Status = "prepared"
			existing.Key = "message:" + payloadHash[:24] + ":" + strconv.Itoa(existing.Generation)
			ledger.Records[locator] = existing
			if err := saveIdempotencyLedger(root, identity, ledger); err != nil {
				release()
				return "", nil, err
			}
		}
		return ledger.Records[locator].Key, release, nil
	}
	ledger.Records[locator] = idempotencyRecord{Key: key, PayloadHash: payloadHash, Status: "prepared"}
	if err := saveIdempotencyLedger(root, identity, ledger); err != nil {
		release()
		return "", nil, err
	}
	return key, release, nil
}

func completeIdempotentSend(root, identity, to, subject string, env envelope) error {
	locator, payloadHash, _, err := idempotentSendIdentity(to, subject, env)
	if err != nil {
		return err
	}
	lockSum := sha256.Sum256([]byte(identity + "\x00" + locator))
	lockID := "send-" + hex.EncodeToString(lockSum[:12])
	release, _, err := acquireProcessLock(root, lockID, "send-locks", "front-agent send already running for operation %s with pid %d")
	if err != nil {
		return err
	}
	defer release()
	ledger, err := loadIdempotencyLedger(root, identity)
	if err != nil {
		return err
	}
	record, ok := ledger.Records[locator]
	if !ok {
		return nil
	}
	if record.PayloadHash != payloadHash {
		return fmt.Errorf("idempotent send %s completion payload does not match", locator)
	}
	record.Status = "complete"
	ledger.Records[locator] = record
	return saveIdempotencyLedger(root, identity, ledger)
}

func idempotentSendIdentity(to, subject string, env envelope) (string, string, string, error) {
	payloadSum := sha256.Sum256([]byte(strings.Join([]string{to, strings.TrimSpace(subject), encodeEnvelope(env)}, "\x00")))
	payloadHash := hex.EncodeToString(payloadSum[:])
	locator := "payload:" + payloadHash
	key := "message:" + payloadHash[:32]
	if env.RespondsTo == "" {
		return locator, payloadHash, key, nil
	}
	if err := validateMailID(env.RespondsTo); err != nil {
		return "", "", "", err
	}
	prefix := "response"
	if env.Contract == contractMessage && bodyScalar(env.Body, "method") == "answer" {
		prefix = "answer"
	} else if env.Contract == contractReady {
		prefix = "ready"
	}
	locator = prefix + ":" + env.RespondsTo
	return locator, payloadHash, locator, nil
}

func loadIdempotencyLedger(root, identity string) (idempotencyLedger, error) {
	if err := validateIdentity(identity); err != nil {
		return idempotencyLedger{}, err
	}
	ledger := idempotencyLedger{Records: map[string]idempotencyRecord{}}
	dir, err := idempotencyDir(root)
	if err != nil {
		return ledger, err
	}
	file, err := openPrivateFile(filepath.Join(dir, identity+".json"), os.O_RDONLY)
	if errors.Is(err, os.ErrNotExist) {
		return ledger, nil
	}
	if err != nil {
		return ledger, err
	}
	defer file.Close()
	raw, err := io.ReadAll(io.LimitReader(file, 2<<20))
	if err != nil {
		return ledger, err
	}
	if err := json.Unmarshal(raw, &ledger); err != nil {
		return ledger, err
	}
	if ledger.Records == nil {
		ledger.Records = map[string]idempotencyRecord{}
	}
	return ledger, nil
}

func saveIdempotencyLedger(root, identity string, ledger idempotencyLedger) error {
	dir, err := idempotencyDir(root)
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

func idempotencyDir(root string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "idempotency"), nil
}
