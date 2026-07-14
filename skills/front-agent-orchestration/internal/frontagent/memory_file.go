package frontagent

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"syscall"
	"time"
)

type sharedMemoryStore struct {
	Seq          int                        `json:"seq"`
	Participants map[string]string          `json:"participants"`
	Messages     []mailMessage              `json:"messages"`
	Read         map[string]map[string]bool `json:"read"`
}

func sharedMemoryRunMail(stdin string, args []string) (string, error) {
	root := argValue(args, "--root")
	switch args[0] {
	case "start":
		role := argValue(args, "--role")
		if role == "" {
			return "", errors.New("start requires --role")
		}
		var identity string
		err := withSharedMemoryStore(root, true, func(store *sharedMemoryStore) error {
			store.Seq++
			identity = fmt.Sprintf("test-%s-%04d", strings.ReplaceAll(role, "/", "-"), store.Seq)
			store.Participants[identity] = role
			return nil
		})
		if err != nil {
			return "", err
		}
		return fmt.Sprintf("identity: %s\nrole: %s\n", identity, role), nil
	case "send":
		return sharedMemorySend(stdin, root, args)
	case "inbox":
		return sharedMemoryInbox(root, args)
	case "read":
		if len(args) < 2 {
			return "", errors.New("read requires message id")
		}
		return sharedMemoryRead(root, args[1], args)
	default:
		return "", fmt.Errorf("unsupported mail command %q", args[0])
	}
}

func sharedMemorySend(stdin, root string, args []string) (string, error) {
	project, err := projectAlias(root)
	if err != nil {
		return "", err
	}
	sender := argValue(args, "--identity")
	recipient := argValue(args, "--to")
	subject := argValue(args, "--subject")
	if sender == "" || recipient == "" || subject == "" {
		return "", errors.New("send requires --identity, --to, and --subject")
	}
	if strings.ContainsAny(subject, "\r\n") {
		return "", errors.New("subject must not contain newlines")
	}
	var msg mailMessage
	err = withSharedMemoryStore(root, true, func(store *sharedMemoryStore) error {
		role, ok := store.Participants[sender]
		if !ok {
			return fmt.Errorf("unknown sender identity %s", sender)
		}
		store.Seq++
		now := time.Now().UTC()
		msg = mailMessage{
			ID:             fmt.Sprintf("mail-%s-%08x", now.Format("20060102-150405"), store.Seq),
			Project:        project,
			SenderIdentity: sender,
			SenderRole:     role,
			RecipientKind:  "identity",
			Recipient:      recipient,
			Subject:        subject,
			Body: encodeEnvelope(envelope{
				Type:       argValue(args, "--type"),
				Contract:   argValue(args, "--contract"),
				RespondsTo: argValue(args, "--responds-to"),
				Body:       stdin,
			}),
			CreatedAt:   now.Format(time.RFC3339Nano),
			CreatedAtNS: now.UnixNano(),
		}
		store.Messages = append(store.Messages, msg)
		return nil
	})
	if err != nil {
		return "", err
	}
	if err := cacheMail(root, msg); err != nil {
		return "", err
	}
	return fmt.Sprintf("id: %s\n%s\n", msg.ID, msg.ID), nil
}

func sharedMemoryInbox(root string, args []string) (string, error) {
	timeout := parseTimeout(args)
	deadline := time.Now().Add(timeout)
	for {
		var output string
		var found bool
		err := withSharedMemoryStore(root, false, func(store *sharedMemoryStore) error {
			var err error
			output, found, err = sharedMemoryFilteredInbox(store, root, args)
			return err
		})
		if err != nil {
			return "", err
		}
		if found || !hasArg(args, "--wait") {
			return output, nil
		}
		if timeout <= 0 || !time.Now().Before(deadline) {
			return "", errors.New("timed out waiting for matching mail")
		}
		sleep := 20 * time.Millisecond
		if remaining := time.Until(deadline); remaining < sleep {
			sleep = remaining
		}
		if sleep <= 0 {
			return "", errors.New("timed out waiting for matching mail")
		}
		time.Sleep(sleep)
	}
}

func sharedMemoryFilteredInbox(store *sharedMemoryStore, root string, args []string) (string, bool, error) {
	project, err := projectAlias(root)
	if err != nil {
		return "", false, err
	}
	identity := argValue(args, "--identity")
	if identity == "" {
		return "", false, errors.New("inbox requires --identity")
	}
	if _, ok := store.Participants[identity]; !ok {
		return "", false, fmt.Errorf("unknown inbox identity %s", identity)
	}
	var matches []mailMessage
	for _, msg := range store.Messages {
		if msg.Project != project || msg.Recipient != identity || store.Read[msg.ID][identity] {
			continue
		}
		if matchesFilters(messageMeta(msg), args) {
			matches = append(matches, msg)
		}
	}
	sort.Slice(matches, func(i, j int) bool {
		if matches[i].CreatedAtNS == matches[j].CreatedAtNS {
			return matches[i].ID < matches[j].ID
		}
		return matches[i].CreatedAtNS < matches[j].CreatedAtNS
	})
	var output strings.Builder
	for _, msg := range matches {
		fmt.Fprintf(&output, "%s\t%s\n", msg.ID, msg.SenderIdentity)
	}
	return output.String(), len(matches) > 0, nil
}

func sharedMemoryRead(root, id string, args []string) (string, error) {
	if err := validateMailID(id); err != nil {
		return "", err
	}
	project, err := projectAlias(root)
	if err != nil {
		return "", err
	}
	identity := argValue(args, "--identity")
	var found mailMessage
	err = withSharedMemoryStore(root, !hasArg(args, "--no-mark-read"), func(store *sharedMemoryStore) error {
		if _, ok := store.Participants[identity]; !ok {
			return fmt.Errorf("unknown reader identity %s", identity)
		}
		for _, msg := range store.Messages {
			if msg.ID != id || msg.Project != project {
				continue
			}
			if msg.Recipient != identity && msg.SenderIdentity != identity && !hasArg(args, "--force") {
				return fmt.Errorf("message %s is not delivered to %s", id, identity)
			}
			found = msg
			if !hasArg(args, "--no-mark-read") {
				if store.Read[id] == nil {
					store.Read[id] = map[string]bool{}
				}
				store.Read[id][identity] = true
			}
			return nil
		}
		return os.ErrNotExist
	})
	if errors.Is(err, os.ErrNotExist) && hasArg(args, "--force") {
		found, err = readCachedMail(root, id)
	}
	if err != nil {
		return "", fmt.Errorf("unknown message %s", id)
	}
	return renderMessage(found), nil
}

func withSharedMemoryStore(root string, write bool, fn func(*sharedMemoryStore) error) error {
	stateDir, err := stateRoot(root)
	if err != nil {
		return err
	}
	if err := ensurePrivateDir(stateDir); err != nil {
		return err
	}
	dir := filepath.Join(stateDir, "memory-mail")
	if err := ensurePrivateDir(dir); err != nil {
		return err
	}
	lock, err := openPrivateFile(filepath.Join(dir, "store.lock"), os.O_CREATE|os.O_RDWR)
	if err != nil {
		return err
	}
	defer lock.Close()
	if err := syscall.Flock(int(lock.Fd()), syscall.LOCK_EX); err != nil {
		return err
	}
	defer syscall.Flock(int(lock.Fd()), syscall.LOCK_UN)
	storePath := filepath.Join(dir, "store.json")
	store := sharedMemoryStore{Participants: map[string]string{}, Read: map[string]map[string]bool{}}
	if file, err := openPrivateFile(storePath, os.O_RDONLY); err == nil {
		raw, readErr := io.ReadAll(io.LimitReader(file, 16<<20))
		_ = file.Close()
		if readErr != nil {
			return readErr
		}
		if len(raw) > 0 {
			if err := json.Unmarshal(raw, &store); err != nil {
				return fmt.Errorf("shared memory mailbox is corrupt: %w", err)
			}
		}
	} else if !errors.Is(err, os.ErrNotExist) {
		return err
	}
	if store.Participants == nil {
		store.Participants = map[string]string{}
	}
	if store.Read == nil {
		store.Read = map[string]map[string]bool{}
	}
	if err := fn(&store); err != nil {
		return err
	}
	if !write {
		return nil
	}
	raw, err := json.MarshalIndent(store, "", "  ")
	if err != nil {
		return err
	}
	tmp, err := os.CreateTemp(dir, ".store.*.tmp")
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
	return os.Rename(tmpPath, storePath)
}
