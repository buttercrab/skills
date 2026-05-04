package frontagent

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"sync"
	"time"
)

var mailIDPattern = regexp.MustCompile(`mail-[0-9]{8}-[0-9]{6}-[a-f0-9]{8,16}`)

const (
	frontAgentEnvelopeStart = "--- front-agent-meta ---"
	frontAgentEnvelopeEnd   = "--- front-agent-body ---"
)

type mailSession struct {
	Identity string `json:"identity"`
	Role     string `json:"role"`
}

type mailMessage struct {
	ID             string `json:"id"`
	Project        string `json:"project"`
	SenderIdentity string `json:"sender_identity"`
	SenderRole     string `json:"sender_role"`
	RecipientKind  string `json:"recipient_kind"`
	Recipient      string `json:"recipient"`
	Subject        string `json:"subject"`
	Body           string `json:"body"`
	CreatedAt      string `json:"created_at"`
	CreatedAtNS    int64  `json:"created_at_ns"`
	ReadAt         string `json:"read_at"`
}

type mailInbox struct {
	Project     string        `json:"project"`
	Identity    string        `json:"identity"`
	Role        string        `json:"role"`
	UnreadCount int           `json:"unread_count"`
	Messages    []mailMessage `json:"messages"`
}

type envelope struct {
	Type       string `json:"type,omitempty"`
	Contract   string `json:"contract,omitempty"`
	RespondsTo string `json:"responds_to,omitempty"`
	Body       string `json:"body"`
}

func runMail(stdin string, args ...any) (string, error) {
	flat := flattenArgs(args)
	if len(flat) == 0 {
		return "", errors.New("missing mail command")
	}
	if strings.TrimSpace(os.Getenv("FRONT_AGENT_MAIL_BACKEND")) == "memory" {
		return memoryRunMail(stdin, flat)
	}
	client, err := newAgentMailClient()
	if err != nil {
		return "", err
	}
	return client.run(stdin, flat)
}

func streamMail(stdout, stderr io.Writer, args ...any) error {
	out, err := runMail("", args...)
	if out != "" {
		_, _ = io.WriteString(stdout, out)
	}
	if err != nil {
		_, _ = fmt.Fprintln(stderr, err)
	}
	return err
}

type agentMailClient struct {
	baseURL    string
	token      string
	httpClient *http.Client
}

func newAgentMailClient() (*agentMailClient, error) {
	baseURL := firstEnv("AGENT_MAIL_URL", "AGENT_MAIL_BASE_URL", "PUBLIC_URL")
	if baseURL == "" {
		baseURL = "https://agent-mail.cc"
	}
	token := strings.TrimSpace(os.Getenv("AGENT_MAIL_TOKEN"))
	if token == "" {
		return nil, errors.New("AGENT_MAIL_TOKEN is required for Agent Mail HTTP")
	}
	return &agentMailClient{
		baseURL:    strings.TrimRight(baseURL, "/"),
		token:      token,
		httpClient: &http.Client{Timeout: 15 * time.Second},
	}, nil
}

func firstEnv(names ...string) string {
	for _, name := range names {
		if value := strings.TrimSpace(os.Getenv(name)); value != "" {
			return value
		}
	}
	return ""
}

func (c *agentMailClient) run(stdin string, args []string) (string, error) {
	switch args[0] {
	case "start":
		role := argValue(args, "--role")
		if role == "" {
			return "", errors.New("start requires --role")
		}
		session, err := c.startParticipant(role)
		if err != nil {
			return "", err
		}
		return fmt.Sprintf("identity: %s\nrole: %s\n", session.Identity, session.Role), nil
	case "send":
		root := argValue(args, "--root")
		project, err := projectAlias(root)
		if err != nil {
			return "", err
		}
		if err := c.ensureProject(project, root); err != nil {
			return "", err
		}
		msg, err := c.send(project, argValue(args, "--identity"), argValue(args, "--to"), argValue(args, "--subject"), envelope{
			Type:       argValue(args, "--type"),
			Contract:   argValue(args, "--contract"),
			RespondsTo: argValue(args, "--responds-to"),
			Body:       stdin,
		})
		if err != nil {
			return "", err
		}
		_ = cacheMail(root, msg)
		return fmt.Sprintf("id: %s\n%s\n", msg.ID, msg.ID), nil
	case "inbox":
		return c.inboxText(args)
	case "read":
		if len(args) < 2 {
			return "", errors.New("read requires message id")
		}
		return c.readText(args[1], args)
	default:
		return "", fmt.Errorf("unsupported mail command %q", args[0])
	}
}

func (c *agentMailClient) startParticipant(role string) (mailSession, error) {
	var session mailSession
	return session, c.postJSON("/v1/participants/start", map[string]string{"role": role}, &session)
}

func (c *agentMailClient) ensureProject(alias, root string) error {
	projectRoot, err := projectRoot(root)
	if err != nil {
		return err
	}
	var out map[string]any
	return c.postJSON("/v1/projects", map[string]string{"alias": alias, "root": projectRoot}, &out)
}

func (c *agentMailClient) send(project, identity, to, subject string, env envelope) (mailMessage, error) {
	if identity == "" {
		return mailMessage{}, errors.New("send requires --identity")
	}
	if to == "" {
		return mailMessage{}, errors.New("send requires --to")
	}
	if subject == "" {
		return mailMessage{}, errors.New("send requires --subject")
	}
	var msg mailMessage
	err := c.postJSON("/v1/messages", map[string]string{
		"sender_identity": identity,
		"project":         project,
		"to_kind":         "identity",
		"to":              to,
		"subject":         subject,
		"body":            encodeEnvelope(env),
	}, &msg)
	return msg, err
}

func (c *agentMailClient) inboxText(args []string) (string, error) {
	root := argValue(args, "--root")
	project, err := projectAlias(root)
	if err != nil {
		return "", err
	}
	if err := c.ensureProject(project, root); err != nil {
		return "", err
	}
	identity := argValue(args, "--identity")
	if identity == "" {
		return "", errors.New("inbox requires --identity")
	}
	timeout := parseTimeout(args)
	deadline := time.Now().Add(timeout)
	for {
		out, found, err := c.filteredInbox(project, identity, args)
		if err != nil {
			return "", err
		}
		if found || !hasArg(args, "--wait") {
			return out, nil
		}
		if timeout <= 0 || time.Now().After(deadline) {
			return "", errors.New("timed out waiting for matching mail")
		}
		sleep := 200 * time.Millisecond
		if remaining := time.Until(deadline); remaining < sleep {
			sleep = remaining
		}
		if sleep <= 0 {
			return "", errors.New("timed out waiting for matching mail")
		}
		time.Sleep(sleep)
	}
}

func (c *agentMailClient) filteredInbox(project, identity string, args []string) (string, bool, error) {
	var inbox mailInbox
	path := fmt.Sprintf("/v1/projects/%s/participants/%s/inbox", url.PathEscape(project), url.PathEscape(identity))
	if err := c.getJSON(path, &inbox); err != nil {
		return "", false, err
	}
	var buf strings.Builder
	found := false
	for _, msg := range inbox.Messages {
		full, err := c.readMessage(project, msg.ID, identity)
		if err != nil {
			return "", false, err
		}
		meta := messageMeta(full)
		if !matchesFilters(meta, args) {
			continue
		}
		found = true
		fmt.Fprintf(&buf, "%s\t%s\t%s\n", full.ID, full.SenderIdentity, full.Subject)
	}
	return buf.String(), found, nil
}

func (c *agentMailClient) readText(id string, args []string) (string, error) {
	root := argValue(args, "--root")
	project, err := projectAlias(root)
	if err != nil {
		return "", err
	}
	identity := argValue(args, "--identity")
	if identity == "" {
		return "", errors.New("read requires --identity")
	}
	msg, err := c.readMessage(project, id, identity)
	if err != nil && hasArg(args, "--force") {
		msg, err = readCachedMail(root, id)
	}
	if err != nil {
		return "", err
	}
	text := renderMessage(msg)
	if !hasArg(args, "--no-mark-read") {
		if markErr := c.markRead(project, id, identity); markErr != nil {
			return "", markErr
		}
	}
	return text, nil
}

func (c *agentMailClient) readMessage(project, id, identity string) (mailMessage, error) {
	var msg mailMessage
	path := fmt.Sprintf("/v1/projects/%s/messages/%s?identity=%s", url.PathEscape(project), url.PathEscape(id), url.QueryEscape(identity))
	err := c.getJSON(path, &msg)
	return msg, err
}

func (c *agentMailClient) markRead(project, id, identity string) error {
	var out map[string]any
	path := fmt.Sprintf("/v1/projects/%s/messages/%s/read", url.PathEscape(project), url.PathEscape(id))
	return c.postJSON(path, map[string]string{"identity": identity}, &out)
}

func (c *agentMailClient) getJSON(path string, out any) error {
	req, err := http.NewRequest(http.MethodGet, c.baseURL+path, nil)
	if err != nil {
		return err
	}
	return c.do(req, out)
}

func (c *agentMailClient) postJSON(path string, in, out any) error {
	raw, err := json.Marshal(in)
	if err != nil {
		return err
	}
	req, err := http.NewRequest(http.MethodPost, c.baseURL+path, bytes.NewReader(raw))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	return c.do(req, out)
}

func (c *agentMailClient) do(req *http.Request, out any) error {
	req.Header.Set("Authorization", "Bearer "+c.token)
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		msg := strings.TrimSpace(string(raw))
		if msg == "" {
			msg = resp.Status
		}
		return errors.New(msg)
	}
	if out == nil || len(raw) == 0 {
		return nil
	}
	return json.Unmarshal(raw, out)
}

func argValue(args []string, name string) string {
	for i := 0; i < len(args); i++ {
		arg := args[i]
		if arg == name && i+1 < len(args) {
			return args[i+1]
		}
		if value, ok := strings.CutPrefix(arg, name+"="); ok {
			return value
		}
	}
	return ""
}

func hasArg(args []string, name string) bool {
	for _, arg := range args {
		if arg == name {
			return true
		}
	}
	return false
}

func parseTimeout(args []string) time.Duration {
	timeoutText := argValue(args, "--timeout")
	if timeoutText == "" {
		return 0
	}
	timeout, err := time.ParseDuration(timeoutText)
	if err != nil {
		return 0
	}
	return timeout
}

func matchesFilters(meta map[string]string, args []string) bool {
	for _, pair := range [][2]string{
		{"--to", "to"},
		{"--contract", "contract"},
		{"--responds-to", "responds_to"},
	} {
		if want := argValue(args, pair[0]); want != "" && meta[pair[1]] != want {
			return false
		}
	}
	return true
}

func encodeEnvelope(env envelope) string {
	var b strings.Builder
	fmt.Fprintln(&b, frontAgentEnvelopeStart)
	if env.Type != "" {
		fmt.Fprintf(&b, "type: %s\n", env.Type)
	}
	if env.Contract != "" {
		fmt.Fprintf(&b, "contract: %s\n", env.Contract)
	}
	if env.RespondsTo != "" {
		fmt.Fprintf(&b, "responds_to: %s\n", env.RespondsTo)
	}
	fmt.Fprintln(&b, frontAgentEnvelopeEnd)
	fmt.Fprint(&b, env.Body)
	return b.String()
}

func decodeEnvelope(body string) envelope {
	if !strings.HasPrefix(body, frontAgentEnvelopeStart+"\n") {
		return envelope{Body: body}
	}
	afterMeta := strings.TrimPrefix(body, frontAgentEnvelopeStart+"\n")
	metaText, bodyText, ok := strings.Cut(afterMeta, frontAgentEnvelopeEnd+"\n")
	if !ok {
		return envelope{Body: body}
	}
	env := envelope{Body: bodyText}
	for _, line := range strings.Split(metaText, "\n") {
		key, value, ok := strings.Cut(line, ":")
		if !ok {
			continue
		}
		switch strings.TrimSpace(key) {
		case "type":
			env.Type = strings.TrimSpace(value)
		case "contract":
			env.Contract = strings.TrimSpace(value)
		case "responds_to":
			env.RespondsTo = strings.TrimSpace(value)
		}
	}
	return env
}

func messageMeta(msg mailMessage) map[string]string {
	env := decodeEnvelope(msg.Body)
	return map[string]string{
		"id":          msg.ID,
		"from":        msg.SenderIdentity,
		"from_role":   msg.SenderRole,
		"to":          msg.Recipient,
		"type":        env.Type,
		"contract":    env.Contract,
		"responds_to": env.RespondsTo,
		"subject":     msg.Subject,
		"created_at":  msg.CreatedAt,
	}
}

func renderMessage(msg mailMessage) string {
	meta := messageMeta(msg)
	keys := []string{"id", "from", "from_role", "to", "type", "contract", "responds_to", "subject", "created_at"}
	var b strings.Builder
	fmt.Fprintln(&b, "---")
	for _, key := range keys {
		if value := meta[key]; value != "" {
			fmt.Fprintf(&b, "%s: %s\n", key, value)
		}
	}
	fmt.Fprintln(&b, "---")
	fmt.Fprint(&b, decodeEnvelope(msg.Body).Body)
	return b.String()
}

func parseField(text, field string) (string, error) {
	prefix := field + ": "
	for _, line := range strings.Split(text, "\n") {
		if value, ok := strings.CutPrefix(line, prefix); ok {
			value = strings.TrimSpace(value)
			if value != "" {
				return value, nil
			}
		}
	}
	return "", fmt.Errorf("missing %s in output", field)
}

func firstMailID(text string) (string, error) {
	id := mailIDPattern.FindString(text)
	if id == "" {
		return "", errors.New("no mail id found in output")
	}
	return id, nil
}

func readMailMeta(id, identity, root string) (map[string]string, error) {
	out, err := runMail("", "read", id, "--identity", identity, "--no-mark-read", rootArgs(root))
	if err != nil {
		return nil, err
	}
	meta, _ := readMailMetaFromText(out)
	return meta, nil
}

func readMailMetaFromText(text string) (map[string]string, string) {
	meta := map[string]string{}
	lines := strings.Split(text, "\n")
	inMeta := false
	bodyStart := len(lines)
	for i, line := range lines {
		if strings.TrimSpace(line) == "---" {
			if !inMeta {
				inMeta = true
				continue
			}
			bodyStart = i + 1
			break
		}
		if !inMeta {
			continue
		}
		key, value, ok := strings.Cut(line, ":")
		if !ok {
			continue
		}
		key = strings.TrimSpace(key)
		value = strings.TrimSpace(value)
		if key != "" {
			meta[key] = value
		}
	}
	return meta, strings.Join(lines[bodyStart:], "\n")
}

func projectAlias(root string) (string, error) {
	project, err := projectRoot(root)
	if err != nil {
		return "", err
	}
	base := filepath.Base(project)
	var clean strings.Builder
	for _, ch := range base {
		if ch >= 'A' && ch <= 'Z' {
			ch += 'a' - 'A'
		}
		if (ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9') || ch == '.' || ch == '_' || ch == '-' {
			clean.WriteRune(ch)
		} else {
			clean.WriteByte('-')
		}
	}
	name := strings.Trim(clean.String(), ".-_")
	if name == "" {
		name = "project"
	}
	sum := sha256.Sum256([]byte(project))
	return fmt.Sprintf("%s-%s", name, hex.EncodeToString(sum[:4])), nil
}

func cacheMail(root string, msg mailMessage) error {
	dir, err := mailCacheDir(root)
	if err != nil {
		return err
	}
	if err := os.MkdirAll(dir, 0700); err != nil {
		return err
	}
	raw, err := json.MarshalIndent(msg, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(filepath.Join(dir, msg.ID+".json"), append(raw, '\n'), 0600)
}

func readCachedMail(root, id string) (mailMessage, error) {
	dir, err := mailCacheDir(root)
	if err != nil {
		return mailMessage{}, err
	}
	raw, err := os.ReadFile(filepath.Join(dir, id+".json"))
	if err != nil {
		return mailMessage{}, err
	}
	var msg mailMessage
	if err := json.Unmarshal(raw, &msg); err != nil {
		return mailMessage{}, err
	}
	return msg, nil
}

func mailCacheDir(root string) (string, error) {
	dir, err := stateRoot(root)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "mail-cache"), nil
}

var memoryMail = struct {
	sync.Mutex
	seq          int
	participants map[string]string
	messages     []mailMessage
	read         map[string]map[string]bool
}{
	participants: map[string]string{},
	read:         map[string]map[string]bool{},
}

func memoryRunMail(stdin string, args []string) (string, error) {
	memoryMail.Lock()
	defer memoryMail.Unlock()
	switch args[0] {
	case "start":
		role := argValue(args, "--role")
		if role == "" {
			return "", errors.New("start requires --role")
		}
		memoryMail.seq++
		id := fmt.Sprintf("test-%s-%04d", strings.ReplaceAll(role, "/", "-"), memoryMail.seq)
		memoryMail.participants[id] = role
		return fmt.Sprintf("identity: %s\nrole: %s\n", id, role), nil
	case "send":
		project, err := projectAlias(argValue(args, "--root"))
		if err != nil {
			return "", err
		}
		sender := argValue(args, "--identity")
		if sender == "" {
			return "", errors.New("send requires --identity")
		}
		memoryMail.seq++
		now := time.Now().UTC()
		msg := mailMessage{
			ID:             fmt.Sprintf("mail-%s-%08x", now.Format("20060102-150405"), memoryMail.seq),
			Project:        project,
			SenderIdentity: sender,
			SenderRole:     memoryMail.participants[sender],
			RecipientKind:  "identity",
			Recipient:      argValue(args, "--to"),
			Subject:        argValue(args, "--subject"),
			Body: encodeEnvelope(envelope{
				Type:       argValue(args, "--type"),
				Contract:   argValue(args, "--contract"),
				RespondsTo: argValue(args, "--responds-to"),
				Body:       stdin,
			}),
			CreatedAt:   now.Format(time.RFC3339Nano),
			CreatedAtNS: now.UnixNano(),
		}
		memoryMail.messages = append(memoryMail.messages, msg)
		_ = cacheMail(argValue(args, "--root"), msg)
		return fmt.Sprintf("id: %s\n%s\n", msg.ID, msg.ID), nil
	case "inbox":
		return memoryInboxText(args)
	case "read":
		if len(args) < 2 {
			return "", errors.New("read requires message id")
		}
		return memoryReadText(args[1], args)
	default:
		return "", fmt.Errorf("unsupported mail command %q", args[0])
	}
}

func memoryInboxText(args []string) (string, error) {
	timeout := parseTimeout(args)
	deadline := time.Now().Add(timeout)
	for {
		out, found, err := memoryFilteredInbox(args)
		if err != nil {
			return "", err
		}
		if found || !hasArg(args, "--wait") {
			return out, nil
		}
		if timeout <= 0 || time.Now().After(deadline) {
			return "", errors.New("timed out waiting for matching mail")
		}
		memoryMail.Unlock()
		time.Sleep(20 * time.Millisecond)
		memoryMail.Lock()
	}
}

func memoryFilteredInbox(args []string) (string, bool, error) {
	project, err := projectAlias(argValue(args, "--root"))
	if err != nil {
		return "", false, err
	}
	identity := argValue(args, "--identity")
	if identity == "" {
		return "", false, errors.New("inbox requires --identity")
	}
	var matches []mailMessage
	for _, msg := range memoryMail.messages {
		if msg.Project != project || msg.Recipient != identity {
			continue
		}
		if memoryMail.read[msg.ID] != nil && memoryMail.read[msg.ID][identity] {
			continue
		}
		if !matchesFilters(messageMeta(msg), args) {
			continue
		}
		matches = append(matches, msg)
	}
	sort.Slice(matches, func(i, j int) bool {
		if matches[i].CreatedAtNS == matches[j].CreatedAtNS {
			return matches[i].ID < matches[j].ID
		}
		return matches[i].CreatedAtNS < matches[j].CreatedAtNS
	})
	var b strings.Builder
	for _, msg := range matches {
		fmt.Fprintf(&b, "%s\t%s\t%s\n", msg.ID, msg.SenderIdentity, msg.Subject)
	}
	return b.String(), len(matches) > 0, nil
}

func memoryReadText(id string, args []string) (string, error) {
	identity := argValue(args, "--identity")
	root := argValue(args, "--root")
	project, err := projectAlias(root)
	if err != nil {
		return "", err
	}
	for _, msg := range memoryMail.messages {
		if msg.ID != id || msg.Project != project {
			continue
		}
		if msg.Recipient != identity && msg.SenderIdentity != identity && !hasArg(args, "--force") {
			return "", fmt.Errorf("message %s is not delivered to %s", id, identity)
		}
		if !hasArg(args, "--no-mark-read") {
			if memoryMail.read[id] == nil {
				memoryMail.read[id] = map[string]bool{}
			}
			memoryMail.read[id][identity] = true
		}
		return renderMessage(msg), nil
	}
	msg, err := readCachedMail(root, id)
	if err != nil {
		return "", fmt.Errorf("unknown message %s", id)
	}
	return renderMessage(msg), nil
}
