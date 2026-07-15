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

type workRecord struct {
	CoreSHA256          string `json:"core_sha256"`
	LastSequence        int    `json:"last_sequence"`
	LastEventSHA256     string `json:"last_event_sha256"`
	LastStatus          string `json:"last_status,omitempty"`
	Terminal            bool   `json:"terminal"`
	LastStateGeneration int    `json:"last_state_generation,omitempty"`
	CoordinatorID       string `json:"coordinator_id,omitempty"`
	CoordinatorEpoch    int    `json:"coordinator_epoch,omitempty"`
}

type workLedger struct {
	SchemaVersion string                `json:"schema_version"`
	Works         map[string]workRecord `json:"works"`
}

func prepareWorkEvent(root, identity, body string) (func() error, func(), error) {
	method := bodyScalar(body, "method")
	if method != "work" && method != "update" {
		return func() error { return nil }, func() {}, nil
	}
	release, _, err := acquireProcessLock(root, identity, "work-ledger-locks", "front-agent work lifecycle already updating for identity %s with pid %d")
	if err != nil {
		return nil, nil, err
	}
	fail := func(err error) (func() error, func(), error) {
		release()
		return nil, nil, err
	}
	ledger, err := loadWorkLedger(root, identity)
	if err != nil {
		return fail(err)
	}
	authority, err := parseWorkAuthority(body)
	if err != nil {
		return fail(err)
	}
	eventHash := sha256.Sum256([]byte(body))
	eventSHA := hex.EncodeToString(eventHash[:])
	coreSHA, err := workCoreHash(authority)
	if err != nil {
		return fail(err)
	}
	record, exists := ledger.Works[authority.WorkID]
	if exists && record.LastSequence == authority.Sequence && record.LastEventSHA256 == eventSHA {
		return func() error { return nil }, release, nil
	}
	if method == "work" {
		if exists {
			return fail(fmt.Errorf("work_id %s was reused with different content", authority.WorkID))
		}
		for id, existing := range ledger.Works {
			if !existing.Terminal {
				return fail(fmt.Errorf("work %s is still nonterminal; cannot start %s", id, authority.WorkID))
			}
		}
		if authority.Sequence != 0 {
			return fail(fmt.Errorf("work sequence must start at 0"))
		}
		if authority.PacketBinding != nil && authority.PacketBinding.LifecycleStatus != "approved" {
			return fail(fmt.Errorf("packet work must start from approved status"))
		}
		record = workRecord{CoreSHA256: coreSHA, LastSequence: 0, LastEventSHA256: eventSHA}
		if authority.PacketBinding != nil {
			record.LastStateGeneration = authority.PacketBinding.StateGeneration
			record.CoordinatorID = authority.PacketBinding.CoordinatorID
			record.CoordinatorEpoch = authority.PacketBinding.CoordinatorEpoch
		}
	} else {
		if !exists {
			return fail(fmt.Errorf("update references unknown work_id %s", authority.WorkID))
		}
		if record.Terminal {
			return fail(fmt.Errorf("work_id %s is already terminal with status %s", authority.WorkID, record.LastStatus))
		}
		if record.CoreSHA256 != coreSHA {
			return fail(fmt.Errorf("update changed stable work authority for %s", authority.WorkID))
		}
		if authority.Sequence != record.LastSequence+1 {
			return fail(fmt.Errorf("update sequence %d is stale or reordered; want %d", authority.Sequence, record.LastSequence+1))
		}
		status := bodyScalar(body, "status")
		if record.LastSequence == 0 && status != "accepted" {
			return fail(fmt.Errorf("first update for %s must be accepted", authority.WorkID))
		}
		if record.LastSequence > 0 && status == "accepted" {
			return fail(fmt.Errorf("accepted may appear only as the first update"))
		}
		if authority.PacketBinding != nil {
			packet := authority.PacketBinding
			if packet.StateGeneration < record.LastStateGeneration {
				return fail(fmt.Errorf("update carries stale packet generation"))
			}
			if packet.CoordinatorEpoch < record.CoordinatorEpoch || packet.CoordinatorEpoch > record.CoordinatorEpoch+1 {
				return fail(fmt.Errorf("update carries stale or skipped coordinator epoch"))
			}
			if packet.CoordinatorEpoch == record.CoordinatorEpoch && packet.CoordinatorID != record.CoordinatorID {
				return fail(fmt.Errorf("update changed coordinator without an epoch increment"))
			}
			if !frontStatusAllowsPacket(status, packet.LifecycleStatus) {
				return fail(fmt.Errorf("update status %s cannot bind packet status %s", status, packet.LifecycleStatus))
			}
			record.LastStateGeneration = packet.StateGeneration
			record.CoordinatorID = packet.CoordinatorID
			record.CoordinatorEpoch = packet.CoordinatorEpoch
		}
		record.LastSequence = authority.Sequence
		record.LastEventSHA256 = eventSHA
		record.LastStatus = status
		record.Terminal = status == "complete" || status == "failed" || status == "cancelled"
	}
	ledger.Works[authority.WorkID] = record
	return func() error { return saveWorkLedger(root, identity, ledger) }, release, nil
}

func frontStatusAllowsPacket(status, packetStatus string) bool {
	allowed := map[string]map[string]bool{
		"accepted":  {"approved": true},
		"progress":  {"executing": true, "verifying": true},
		"blocked":   {"executing": true, "verifying": true, "blocked": true},
		"failed":    {"executing": true, "verifying": true, "blocked": true, "needs_reapproval": true},
		"cancelled": {"cancelled": true},
		"complete":  {"verifying": true},
	}
	return allowed[status][packetStatus]
}

func workCoreHash(authority workAuthority) (string, error) {
	type packetCore struct {
		PacketID         string   `json:"packet_id"`
		TaskID           string   `json:"task_id"`
		PacketPath       string   `json:"packet_path"`
		PacketRevision   int      `json:"packet_revision"`
		ProtectedDigest  string   `json:"protected_digest"`
		ApprovalID       string   `json:"approval_id"`
		AuthorityClasses []string `json:"authority_classes"`
	}
	type core struct {
		SchemaVersion         string      `json:"schema_version"`
		WorkID                string      `json:"work_id"`
		OriginalRequestSHA256 string      `json:"original_request_sha256"`
		AlignmentMode         string      `json:"alignment_mode"`
		GatewayClassification string      `json:"gateway_classification"`
		RepositoryRoot        string      `json:"repository_root"`
		Packet                *packetCore `json:"packet_binding"`
	}
	value := core{
		SchemaVersion:         authority.SchemaVersion,
		WorkID:                authority.WorkID,
		OriginalRequestSHA256: authority.OriginalRequestSHA256,
		AlignmentMode:         authority.AlignmentMode,
		GatewayClassification: authority.GatewayClassification,
		RepositoryRoot:        authority.RepositoryRoot,
	}
	if authority.PacketBinding != nil {
		packet := authority.PacketBinding
		value.Packet = &packetCore{
			PacketID: packet.PacketID, TaskID: packet.TaskID, PacketPath: packet.PacketPath,
			PacketRevision: packet.PacketRevision, ProtectedDigest: packet.ProtectedDigest,
			ApprovalID: packet.ApprovalID, AuthorityClasses: packet.AuthorityClasses,
		}
	}
	raw, err := json.Marshal(value)
	if err != nil {
		return "", err
	}
	sum := sha256.Sum256(append([]byte("work-authority-core/v1\x00"), raw...))
	return hex.EncodeToString(sum[:]), nil
}

func loadWorkLedger(root, identity string) (workLedger, error) {
	ledger := workLedger{SchemaVersion: "front-work-ledger/v1", Works: map[string]workRecord{}}
	dir, err := workLedgerDir(root)
	if err != nil {
		return workLedger{}, err
	}
	file, err := openPrivateRegularFileForRead(filepath.Join(dir, identity+".json"))
	if errors.Is(err, os.ErrNotExist) {
		return ledger, nil
	}
	if err != nil {
		return workLedger{}, err
	}
	defer file.Close()
	decoder := json.NewDecoder(io.LimitReader(file, 2<<20))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&ledger); err != nil {
		return workLedger{}, err
	}
	if ledger.SchemaVersion != "front-work-ledger/v1" || ledger.Works == nil {
		return workLedger{}, fmt.Errorf("front-agent work ledger schema is invalid")
	}
	return ledger, nil
}

func saveWorkLedger(root, identity string, ledger workLedger) error {
	dir, err := workLedgerDir(root)
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

func workLedgerDir(root string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "work-ledgers"), nil
}
