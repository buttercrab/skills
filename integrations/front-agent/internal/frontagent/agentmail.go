package frontagent

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	mailIDPattern      = regexp.MustCompile(`mail-[0-9]{8}-[0-9]{6}-[a-f0-9]{8,16}`)
	mailIDExactPattern = regexp.MustCompile(`^mail-[0-9]{8}-[0-9]{6}-[a-f0-9]{8,16}$`)
)

const (
	frontAgentEnvelopeStart = "--- front-agent-meta ---"
	frontAgentEnvelopeEnd   = "--- front-agent-body ---"
)

type mailSession struct {
	Identity         string `json:"identity"`
	Role             string `json:"role"`
	ParticipantToken string `json:"participant_token"`
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
	NextCursor  string        `json:"next_cursor,omitempty"`
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
		if os.Getenv("FRONT_AGENT_MEMORY_SHARED") == "1" {
			return sharedMemoryRunMail(stdin, flat)
		}
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
	baseURL := strings.TrimSpace(os.Getenv("AGENT_MAIL_URL"))
	if baseURL == "" {
		return nil, errors.New("AGENT_MAIL_URL is required for Agent Mail HTTP")
	}
	parsed, err := url.Parse(baseURL)
	if err != nil || parsed.Hostname() == "" || parsed.User != nil || parsed.RawQuery != "" || parsed.Fragment != "" {
		return nil, errors.New("AGENT_MAIL_URL must be an absolute Agent Mail base URL without credentials, query, or fragment")
	}
	if parsed.Scheme != "https" {
		hostIP := net.ParseIP(parsed.Hostname())
		if parsed.Scheme != "http" || (parsed.Hostname() != "localhost" && (hostIP == nil || !hostIP.IsLoopback())) {
			return nil, errors.New("AGENT_MAIL_URL must use https; http is allowed only for a loopback test server")
		}
	}
	token := strings.TrimSpace(os.Getenv("AGENT_MAIL_TOKEN"))
	if token == "" {
		return nil, errors.New("AGENT_MAIL_TOKEN is required for Agent Mail HTTP")
	}
	return &agentMailClient{
		baseURL: strings.TrimRight(baseURL, "/"),
		token:   token,
		httpClient: &http.Client{
			Timeout: 15 * time.Second,
			CheckRedirect: func(*http.Request, []*http.Request) error {
				return http.ErrUseLastResponse
			},
		},
	}, nil
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
		if session.Role != role {
			return "", errors.New("Agent Mail participant role does not match requested role")
		}
		if err := saveParticipantCredential(argValue(args, "--root"), session); err != nil {
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
		identity := argValue(args, "--identity")
		participantToken, err := loadParticipantToken(root, identity)
		if err != nil {
			return "", err
		}
		env := envelope{
			Type:       argValue(args, "--type"),
			Contract:   argValue(args, "--contract"),
			RespondsTo: argValue(args, "--responds-to"),
			Body:       stdin,
		}
		idempotencyKey, releaseSend, err := prepareIdempotentSend(root, identity, argValue(args, "--to"), argValue(args, "--subject"), env)
		if err != nil {
			return "", err
		}
		defer releaseSend()
		msg, err := c.send(project, identity, participantToken, argValue(args, "--to"), argValue(args, "--subject"), idempotencyKey, env)
		if err != nil {
			return "", err
		}
		if err := cacheMail(root, msg); err != nil {
			return "", err
		}
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
	return session, c.postJSON("/v1/participants/start", map[string]string{"role": role}, &session, c.token)
}

func (c *agentMailClient) ensureProject(alias, root string) error {
	return c.ensureProjectContext(context.Background(), alias, root)
}

func (c *agentMailClient) ensureProjectContext(ctx context.Context, alias, root string) error {
	projectRoot, err := projectRoot(root)
	if err != nil {
		return err
	}
	var out map[string]any
	return c.postJSONContext(ctx, "/v1/projects", map[string]string{"alias": alias, "root": projectRoot}, &out, c.token)
}

func (c *agentMailClient) send(project, identity, participantToken, to, subject, idempotencyKey string, env envelope) (mailMessage, error) {
	if identity == "" {
		return mailMessage{}, errors.New("send requires --identity")
	}
	if to == "" {
		return mailMessage{}, errors.New("send requires --to")
	}
	subject = strings.TrimSpace(subject)
	if subject == "" {
		return mailMessage{}, errors.New("send requires --subject")
	}
	if strings.ContainsAny(subject, "\r\n") {
		return mailMessage{}, errors.New("subject must not contain newlines")
	}
	var msg mailMessage
	err := c.postJSON("/v1/messages", map[string]string{
		"project":         project,
		"to_kind":         "identity",
		"to":              to,
		"subject":         subject,
		"body":            encodeEnvelope(env),
		"idempotency_key": idempotencyKey,
	}, &msg, participantToken)
	if err == nil {
		if msg.SenderIdentity != identity || msg.Recipient != to || msg.Subject != subject || msg.Body != encodeEnvelope(env) {
			return mailMessage{}, errors.New("Agent Mail response does not match authenticated send")
		}
		if msg.Project != "" && msg.Project != project {
			return mailMessage{}, errors.New("Agent Mail response project does not match send project")
		}
	}
	return msg, err
}

func (c *agentMailClient) inboxText(args []string) (string, error) {
	root := argValue(args, "--root")
	project, err := projectAlias(root)
	if err != nil {
		return "", err
	}
	identity := argValue(args, "--identity")
	if identity == "" {
		return "", errors.New("inbox requires --identity")
	}
	participantToken, err := loadParticipantToken(root, identity)
	if err != nil {
		return "", err
	}
	timeout := parseTimeout(args)
	waiting := hasArg(args, "--wait")
	if waiting && timeout <= 0 {
		return "", errors.New("timed out waiting for matching mail")
	}
	requestBudget := timeout
	if !waiting {
		requestBudget = 15 * time.Second
	}
	ctx, cancel := context.WithTimeout(context.Background(), requestBudget)
	defer cancel()
	if err := c.ensureProjectContext(ctx, project, root); err != nil {
		if waiting && errors.Is(err, context.DeadlineExceeded) {
			return "", errors.New("timed out waiting for matching mail")
		}
		return "", err
	}
	const maxPagesPerPoll = 10
	for {
		var collected strings.Builder
		foundAny := false
		cursor := ""
		for page := 0; page < maxPagesPerPoll; page++ {
			out, found, nextCursor, err := c.filteredInbox(ctx, project, identity, participantToken, cursor, args)
			if err != nil {
				if waiting && errors.Is(err, context.DeadlineExceeded) {
					return "", errors.New("timed out waiting for matching mail")
				}
				return "", err
			}
			if found {
				foundAny = true
				collected.WriteString(out)
			}
			if nextCursor == "" {
				cursor = ""
				break
			}
			cursor = nextCursor
			if page == maxPagesPerPoll-1 {
				if foundAny {
					return collected.String(), nil
				}
				return "", fmt.Errorf("inbox scan exceeded %d pages; drain or archive unrelated unread mail", maxPagesPerPoll)
			}
		}
		if foundAny || !waiting {
			return collected.String(), nil
		}
		if ctx.Err() != nil {
			return "", errors.New("timed out waiting for matching mail")
		}
		sleep := 200 * time.Millisecond
		if deadline, ok := ctx.Deadline(); ok {
			if remaining := time.Until(deadline); remaining < sleep {
				sleep = remaining
			}
		}
		if sleep <= 0 {
			return "", errors.New("timed out waiting for matching mail")
		}
		timer := time.NewTimer(sleep)
		select {
		case <-ctx.Done():
			timer.Stop()
			return "", errors.New("timed out waiting for matching mail")
		case <-timer.C:
		}
	}
}

func (c *agentMailClient) filteredInbox(ctx context.Context, project, identity, participantToken, cursor string, args []string) (string, bool, string, error) {
	var inbox mailInbox
	query := url.Values{}
	query.Set("limit", "100")
	if cursor != "" {
		query.Set("cursor", cursor)
	}
	path := fmt.Sprintf("/v1/projects/%s/participants/%s/inbox?%s", url.PathEscape(project), url.PathEscape(identity), query.Encode())
	if err := c.getJSONContext(ctx, path, &inbox, participantToken); err != nil {
		return "", false, "", err
	}
	var buf strings.Builder
	found := false
	for _, msg := range inbox.Messages {
		full, err := c.readMessageContext(ctx, project, msg.ID, identity, participantToken)
		if err != nil {
			return "", false, "", err
		}
		meta := messageMeta(full)
		if !matchesFilters(meta, args) {
			continue
		}
		found = true
		fmt.Fprintf(&buf, "%s\t%s\n", full.ID, full.SenderIdentity)
	}
	return buf.String(), found, inbox.NextCursor, nil
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
	participantToken, err := loadParticipantToken(root, identity)
	if err != nil {
		return "", err
	}
	msg, err := c.readMessage(project, id, identity, participantToken)
	if err != nil && hasArg(args, "--force") {
		msg, err = readCachedMail(root, id)
	}
	if err != nil {
		return "", err
	}
	text := renderMessage(msg)
	if !hasArg(args, "--no-mark-read") {
		if markErr := c.markRead(project, id, identity, participantToken); markErr != nil {
			return "", markErr
		}
	}
	return text, nil
}

func (c *agentMailClient) readMessage(project, id, identity, participantToken string) (mailMessage, error) {
	return c.readMessageContext(context.Background(), project, id, identity, participantToken)
}

func (c *agentMailClient) readMessageContext(ctx context.Context, project, id, identity, participantToken string) (mailMessage, error) {
	var msg mailMessage
	path := fmt.Sprintf("/v1/projects/%s/messages/%s?identity=%s", url.PathEscape(project), url.PathEscape(id), url.QueryEscape(identity))
	err := c.getJSONContext(ctx, path, &msg, participantToken)
	return msg, err
}

func (c *agentMailClient) markRead(project, id, identity, participantToken string) error {
	var out map[string]any
	path := fmt.Sprintf("/v1/projects/%s/messages/%s/read", url.PathEscape(project), url.PathEscape(id))
	return c.postJSON(path, map[string]string{"identity": identity}, &out, participantToken)
}

func (c *agentMailClient) getJSON(path string, out any, token string) error {
	return c.getJSONContext(context.Background(), path, out, token)
}

func (c *agentMailClient) getJSONContext(ctx context.Context, path string, out any, token string) error {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, c.baseURL+path, nil)
	if err != nil {
		return err
	}
	return c.do(req, out, token)
}

func (c *agentMailClient) postJSON(path string, in, out any, token string) error {
	return c.postJSONContext(context.Background(), path, in, out, token)
}

func (c *agentMailClient) postJSONContext(ctx context.Context, path string, in, out any, token string) error {
	raw, err := json.Marshal(in)
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.baseURL+path, bytes.NewReader(raw))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	return c.do(req, out, token)
}

func (c *agentMailClient) do(req *http.Request, out any, token string) error {
	if strings.TrimSpace(token) == "" {
		return errors.New("Agent Mail authorization credential is missing")
	}
	req.Header.Set("Authorization", "Bearer "+token)
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	raw, err := io.ReadAll(io.LimitReader(resp.Body, 2<<20))
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
			fmt.Fprintf(&b, "%s: %s\n", key, strconv.Quote(value))
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
	if err := validateMailID(id); err != nil {
		return "", err
	}
	return id, nil
}

func inboxMailIDs(text string) []string {
	var ids []string
	for _, line := range strings.Split(text, "\n") {
		field, _, _ := strings.Cut(line, "\t")
		field = strings.TrimSpace(field)
		if validateMailID(field) == nil {
			ids = append(ids, field)
		}
	}
	return ids
}

func validateMailID(id string) error {
	if !mailIDExactPattern.MatchString(id) {
		return fmt.Errorf("invalid Agent Mail message id %q", id)
	}
	return nil
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
		if unquoted, err := strconv.Unquote(value); err == nil {
			value = unquoted
		}
		if key != "" {
			if _, duplicate := meta[key]; !duplicate {
				meta[key] = value
			}
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
	if err := validateMailID(msg.ID); err != nil {
		return err
	}
	env := decodeEnvelope(msg.Body)
	if env.Contract != contractMessage || bodyScalar(env.Body, "method") != "question" {
		return nil
	}
	dir, err := mailCacheDir(root)
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
	raw, err := json.MarshalIndent(msg, "", "  ")
	if err != nil {
		return err
	}
	tmp, err := os.CreateTemp(dir, "."+msg.ID+".*.tmp")
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
	if err := os.Rename(tmpPath, filepath.Join(dir, msg.ID+".json")); err != nil {
		return err
	}
	return pruneMailCache(dir, 256)
}

func readCachedMail(root, id string) (mailMessage, error) {
	if err := validateMailID(id); err != nil {
		return mailMessage{}, err
	}
	dir, err := mailCacheDir(root)
	if err != nil {
		return mailMessage{}, err
	}
	file, err := openPrivateFile(filepath.Join(dir, id+".json"), os.O_RDONLY)
	if err != nil {
		return mailMessage{}, err
	}
	defer file.Close()
	raw, err := io.ReadAll(io.LimitReader(file, 2<<20))
	if err != nil {
		return mailMessage{}, err
	}
	var msg mailMessage
	if err := json.Unmarshal(raw, &msg); err != nil {
		return mailMessage{}, err
	}
	if msg.ID != id {
		return mailMessage{}, fmt.Errorf("cached message id %q does not match requested id %q", msg.ID, id)
	}
	return msg, nil
}

func pruneMailCache(dir string, keep int) error {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return err
	}
	type cachedFile struct {
		name    string
		modTime time.Time
	}
	var files []cachedFile
	for _, entry := range entries {
		if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".json") {
			continue
		}
		info, err := entry.Info()
		if err != nil {
			return err
		}
		files = append(files, cachedFile{name: entry.Name(), modTime: info.ModTime()})
	}
	sort.Slice(files, func(i, j int) bool { return files[i].modTime.Before(files[j].modTime) })
	for len(files) > keep {
		if err := os.Remove(filepath.Join(dir, files[0].name)); err != nil {
			return err
		}
		files = files[1:]
	}
	return nil
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
		subject := argValue(args, "--subject")
		if strings.ContainsAny(subject, "\r\n") {
			return "", errors.New("subject must not contain newlines")
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
		memoryMail.messages = append(memoryMail.messages, msg)
		if err := cacheMail(argValue(args, "--root"), msg); err != nil {
			return "", err
		}
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
		fmt.Fprintf(&b, "%s\t%s\n", msg.ID, msg.SenderIdentity)
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
	if hasArg(args, "--force") {
		msg, err := readCachedMail(root, id)
		if err == nil {
			return renderMessage(msg), nil
		}
	}
	return "", fmt.Errorf("unknown message %s", id)
}
