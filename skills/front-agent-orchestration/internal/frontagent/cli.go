package frontagent

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"syscall"
	"time"
)

const (
	mainRole    = "main-orchestrator"
	gatewayRole = "gateway"
	stateDir    = "front-agent"
)

func Main(args []string, stdin io.Reader, stdout, stderr io.Writer) int {
	if err := Run(args, stdin, stdout, stderr); err != nil {
		fmt.Fprintln(stderr, err)
		return 1
	}
	return 0
}

func Run(args []string, stdin io.Reader, stdout, stderr io.Writer) error {
	if len(args) == 0 || args[0] == "help" || args[0] == "--help" || args[0] == "-h" {
		printHelp(stdout)
		return nil
	}
	switch args[0] {
	case "main":
		return cmdMain(args[1:], stdout, stderr)
	case "wait-ready":
		return cmdWaitReady(args[1:], stdout, stderr)
	case "gateway":
		return cmdGateway(args[1:], stdout, stderr)
	case "listen":
		return cmdListen(args[1:], stdout, stderr)
	case "send":
		return cmdSend(args[1:], stdin, stdout, stderr)
	case "request", "respond", "event", "wait":
		return fmt.Errorf("%s was removed; use send", args[0])
	case "state":
		return cmdState(args[1:], stdout, stderr)
	default:
		return fmt.Errorf("unknown command: %s", args[0])
	}
}

func printHelp(w io.Writer) {
	fmt.Fprintln(w, `Front Agent protocol CLI

Usage:
  front-agent main [--root <path>]
  front-agent gateway <main-identity> [--root <path>] [--timeout 24h]
  front-agent listen [--root <path>] [--identity <id>] [--timeout 24h] [--stream]
  front-agent send "Subject" [--root <path>] [--identity <id>] [--responds-to <message-id>]
  front-agent state [--root <path>] [--identity <id>]`)
}

func cmdMain(args []string, stdout, stderr io.Writer) error {
	fs := flag.NewFlagSet("main", flag.ContinueOnError)
	fs.SetOutput(stderr)
	root := fs.String("root", "", "Project root.")
	flagArgs, positional, err := splitArgs(args, map[string]bool{"root": true})
	if err != nil {
		return err
	}
	if err := fs.Parse(flagArgs); err != nil {
		return err
	}
	if len(positional) != 0 {
		return errors.New("main does not accept positional arguments")
	}
	start, err := runMail("", "start", "--role", mainRole, rootArgs(*root))
	if err != nil {
		return err
	}
	identity, err := parseField(start, "identity")
	if err != nil {
		return err
	}
	startedAt := nowText()
	if err := saveState(*root, state{Mode: "main", Identity: identity, Role: mainRole, StartedAt: startedAt}); err != nil {
		return err
	}
	if err := detachWaitReady(stdout, *root, identity, "24h"); err != nil {
		return err
	}
	fmt.Fprintf(stdout, "Main identity: %s\n\n", identity)
	fmt.Fprintf(stdout, "Open the gateway session and say:\n\n$front-agent-orchestration gateway %s%s\n\n", identity, displayRootArg(*root))
	fmt.Fprintln(stdout, "Pairing waiter is detached; gateway should pair without another main-side command.")
	fmt.Fprintln(stdout, "After pairing, main should run:")
	fmt.Fprintf(stdout, "%s listen --identity %s%s\n", displayCommand(), identity, displayRootArg(*root))
	return nil
}

func cmdWaitReady(args []string, stdout, stderr io.Writer) error {
	fs := flag.NewFlagSet("wait-ready", flag.ContinueOnError)
	fs.SetOutput(stderr)
	root := fs.String("root", "", "Project root.")
	identity := fs.String("identity", "", "Main identity.")
	timeout := fs.String("timeout", "24h", "Pairing wait timeout.")
	detach := fs.Bool("detach", false, "Start wait-ready in the background and return the child PID.")
	flagArgs, positional, err := splitArgs(args, map[string]bool{"root": true, "identity": true, "timeout": true, "detach": false})
	if err != nil {
		return err
	}
	if err := fs.Parse(flagArgs); err != nil {
		return err
	}
	if len(positional) != 0 {
		return errors.New("wait-ready does not accept positional arguments")
	}
	st, err := selectState(*root, *identity, "main", false)
	if err != nil {
		return err
	}
	if st.PairedAt != "" {
		return fmt.Errorf("main identity %s is already paired with gateway %s", st.Identity, st.PeerIdentity)
	}
	if st.PeerIdentity != "" && st.LastReadyID != "" {
		if _, alive, err := liveProcessLock(*root, st.PeerIdentity, "gateway-ready"); err != nil {
			return err
		} else if alive {
			return sendMainReadyAck(stdout, *root, st, st.PeerIdentity, st.LastReadyID)
		}
		if err := saveState(*root, state{Mode: "main", Identity: st.Identity, Role: mainRole, StartedAt: st.StartedAt}); err != nil {
			return err
		}
		st.PeerIdentity = ""
		st.LastReadyID = ""
	}
	if *detach {
		return detachWaitReady(stdout, *root, st.Identity, *timeout)
	}
	release, lock, err := acquireProcessLock(*root, st.Identity, "wait-ready", "front-agent wait-ready already running for identity %s with pid %d")
	if err != nil {
		return err
	}
	defer release()
	fmt.Fprintln(stdout, "Waiting for gateway readiness...")
	fmt.Fprintf(stdout, "Wait-ready PID: %d\n", lock.PID)
	readyID, meta, err := waitForValidGatewayReady(stderr, st, *root, *timeout)
	if err != nil {
		return err
	}
	gatewayID := meta["from"]
	if err := saveState(*root, state{Mode: "main", Identity: st.Identity, PeerIdentity: gatewayID, Role: mainRole, StartedAt: st.StartedAt, LastReadyID: readyID}); err != nil {
		return err
	}
	if _, err := runMail("", "read", readyID, "--identity", st.Identity, rootArgs(*root)); err != nil {
		return err
	}
	return sendMainReadyAck(stdout, *root, st, gatewayID, readyID)
}

func sendMainReadyAck(stdout io.Writer, root string, st state, gatewayID, readyID string) error {
	ackBody := fmt.Sprintf("```yaml\nmode: main\nidentity: %s\npeer_identity: %s\nready: true\n```\n", st.Identity, gatewayID)
	if _, err := runMail(ackBody, "send", "--to", gatewayID, "--subject", "Main ready", "--identity", st.Identity, "--type", "summary", "--contract", "front_ready", "--responds-to", readyID, rootArgs(root)); err != nil {
		return err
	}
	if err := saveState(root, state{Mode: "main", Identity: st.Identity, PeerIdentity: gatewayID, Role: mainRole, StartedAt: st.StartedAt, PairedAt: nowText(), LastReadyID: readyID}); err != nil {
		return err
	}
	fmt.Fprintf(stdout, "Paired with gateway identity: %s\n", gatewayID)
	fmt.Fprintln(stdout, "Next main command:")
	fmt.Fprintf(stdout, "%s listen --identity %s%s\n", displayCommand(), st.Identity, displayRootArg(root))
	return nil
}

func detachWaitReady(stdout io.Writer, root, identity, timeout string) error {
	if lock, alive, err := liveProcessLock(root, identity, "wait-ready"); err != nil {
		return err
	} else if alive {
		return fmt.Errorf("front-agent wait-ready already running for identity %s with pid %d", identity, lock.PID)
	}
	exe, err := os.Executable()
	if err != nil {
		return err
	}
	logPath := waitReadyLogPath(root, identity)
	if err := os.MkdirAll(filepath.Dir(logPath), 0700); err != nil {
		return err
	}
	logFile, err := os.OpenFile(logPath, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0600)
	if err != nil {
		return err
	}
	childArgs := []string{"wait-ready", "--identity", identity, "--timeout", timeout}
	childArgs = append(childArgs, rootArgs(root)...)
	if os.Getenv("FRONT_AGENT_TEST_IN_PROCESS_DETACH") == "1" {
		go func() {
			defer logFile.Close()
			_ = cmdWaitReady(childArgs[1:], logFile, logFile)
		}()
		pid := os.Getpid()
		if err := waitForDetachedWaitReady(pid, root, identity, 2*time.Second); err != nil {
			return err
		}
		fmt.Fprintf(stdout, "Detached pairing waiter PID: %d\n", pid)
		fmt.Fprintf(stdout, "Pairing waiter log: %s\n", logPath)
		return nil
	}
	defer logFile.Close()
	cmd := exec.Command(exe, childArgs...)
	cmd.Stdout = logFile
	cmd.Stderr = logFile
	cmd.Stdin = nil
	cmd.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
	if err := cmd.Start(); err != nil {
		return err
	}
	pid := cmd.Process.Pid
	if err := cmd.Process.Release(); err != nil {
		return err
	}
	if err := waitForDetachedWaitReady(pid, root, identity, 2*time.Second); err != nil {
		return err
	}
	fmt.Fprintf(stdout, "Detached pairing waiter PID: %d\n", pid)
	fmt.Fprintf(stdout, "Pairing waiter log: %s\n", logPath)
	return nil
}

func waitForDetachedWaitReady(pid int, root, identity string, timeout time.Duration) error {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		if lock, alive, err := liveProcessLock(root, identity, "wait-ready"); err != nil {
			return err
		} else if alive && lock.PID == pid {
			return nil
		} else if alive {
			return fmt.Errorf("detached wait-ready pid %d did not own wait-ready lock for %s; lock belongs to pid %d", pid, identity, lock.PID)
		}
		if !processAlive(pid) {
			return fmt.Errorf("detached wait-ready exited before creating its lock; see %s", waitReadyLogPath(root, identity))
		}
		time.Sleep(20 * time.Millisecond)
	}
	return fmt.Errorf("detached wait-ready did not become ready within %s; see %s", timeout, waitReadyLogPath(root, identity))
}

func waitForValidGatewayReady(stderr io.Writer, st state, root, timeoutText string) (string, map[string]string, error) {
	timeout, err := time.ParseDuration(timeoutText)
	if err != nil {
		return "", nil, err
	}
	if readyID, meta, ok, err := findValidGatewayReady(stderr, st, root); err != nil {
		return "", nil, err
	} else if ok {
		return readyID, meta, nil
	}
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		remaining := time.Until(deadline)
		wait := time.Second
		if remaining < wait {
			wait = remaining
		}
		if wait <= 0 {
			break
		}
		line, err := runMail("", "inbox", "--wait", "--identity", st.Identity, "--to", st.Identity, "--contract", contractReady, "--timeout", wait.String(), rootArgs(root))
		if err != nil {
			if isWaitTimeout(err) {
				continue
			}
			return "", nil, err
		}
		if readyID, meta, ok, err := validateReadyIDs(stderr, st, root, mailIDPattern.FindAllString(line, -1)); err != nil {
			return "", nil, err
		} else if ok {
			return readyID, meta, nil
		}
	}
	return "", nil, fmt.Errorf("timed out waiting for valid gateway readiness")
}

func findValidGatewayReady(stderr io.Writer, st state, root string) (string, map[string]string, bool, error) {
	inbox, err := runMail("", "inbox", "--identity", st.Identity, "--to", st.Identity, "--contract", contractReady, rootArgs(root))
	if err != nil {
		return "", nil, false, err
	}
	return validateReadyIDs(stderr, st, root, mailIDPattern.FindAllString(inbox, -1))
}

func validateReadyIDs(stderr io.Writer, st state, root string, ids []string) (string, map[string]string, bool, error) {
	var latestID string
	var latestMeta map[string]string
	for _, readyID := range ids {
		read, err := runMail("", "read", readyID, "--identity", st.Identity, "--no-mark-read", rootArgs(root))
		if err != nil {
			return "", nil, false, err
		}
		meta, body := readMailMetaFromText(read)
		if err := validateReadyForMain(meta, body, st); err != nil {
			fmt.Fprintf(stderr, "Rejected %s: %v\n", readyID, err)
			if _, markErr := runMail("", "read", readyID, "--identity", st.Identity, rootArgs(root)); markErr != nil {
				return "", nil, false, markErr
			}
			continue
		}
		if _, alive, err := liveProcessLock(root, meta["from"], "gateway-ready"); err != nil {
			return "", nil, false, err
		} else if !alive {
			fmt.Fprintf(stderr, "Rejected %s: gateway readiness sender %s is not live\n", readyID, meta["from"])
			if _, markErr := runMail("", "read", readyID, "--identity", st.Identity, rootArgs(root)); markErr != nil {
				return "", nil, false, markErr
			}
			continue
		}
		latestID = readyID
		latestMeta = meta
	}
	if latestID == "" {
		return "", nil, false, nil
	}
	return latestID, latestMeta, true, nil
}

func cmdGateway(args []string, stdout, stderr io.Writer) error {
	for _, arg := range args {
		if arg == "--token" || strings.HasPrefix(arg, "--token=") {
			return errors.New("gateway no longer accepts --token; rerun main and use the printed tokenless gateway command")
		}
	}
	fs := flag.NewFlagSet("gateway", flag.ContinueOnError)
	fs.SetOutput(stderr)
	root := fs.String("root", "", "Project root.")
	timeout := fs.String("timeout", "24h", "Pair acknowledgement timeout.")
	flagArgs, positional, err := splitArgs(args, map[string]bool{"root": true, "timeout": true})
	if err != nil {
		return err
	}
	if err := fs.Parse(flagArgs); err != nil {
		return err
	}
	if len(positional) != 1 {
		return errors.New("gateway requires main identity")
	}
	mainID := positional[0]
	if err := validateIdentity(mainID); err != nil {
		return err
	}
	mainState, err := selectState(*root, mainID, "main", false)
	if err != nil {
		return err
	}
	if mainState.PairedAt != "" {
		return fmt.Errorf("main identity %s is already paired with gateway %s", mainID, mainState.PeerIdentity)
	}
	if mainState.PeerIdentity != "" {
		return fmt.Errorf("main identity %s is already in pending pairing with gateway %s", mainID, mainState.PeerIdentity)
	}
	releasePairing, _, err := acquireProcessLock(*root, mainID, "pairing", "front-agent gateway pairing already running for main identity %s with pid %d")
	if err != nil {
		return err
	}
	defer releasePairing()
	if waiter, alive, err := liveProcessLock(*root, mainID, "wait-ready"); err != nil {
		return err
	} else if !alive {
		return fmt.Errorf("main pairing waiter is not running for %s; rerun front-agent main%s before running gateway", mainID, displayRootArg(*root))
	} else {
		fmt.Fprintf(stdout, "Main pairing waiter PID: %d\n", waiter.PID)
	}
	start, err := runMail("", "start", "--role", gatewayRole, rootArgs(*root))
	if err != nil {
		return err
	}
	if _, alive, err := liveProcessLock(*root, mainID, "wait-ready"); err != nil {
		return err
	} else if !alive {
		return fmt.Errorf("main wait-ready stopped before gateway readiness could be sent for %s", mainID)
	}
	identity, err := parseField(start, "identity")
	if err != nil {
		return err
	}
	startedAt := nowText()
	if err := saveState(*root, state{Mode: "gateway", Identity: identity, PeerIdentity: mainID, Role: gatewayRole, StartedAt: startedAt}); err != nil {
		return err
	}
	release, _, err := acquireProcessLock(*root, identity, "gateway-ready", "front-agent gateway already waiting for identity %s with pid %d")
	if err != nil {
		return err
	}
	defer release()
	body := fmt.Sprintf("```yaml\nmode: gateway\nidentity: %s\npeer_identity: %s\nready: true\n```\n", identity, mainID)
	readyOut, err := runMail(body, "send", "--to", mainID, "--subject", "Gateway ready", "--identity", identity, "--type", "summary", "--contract", "front_ready", rootArgs(*root))
	if err != nil {
		return err
	}
	readyID, err := firstMailID(readyOut)
	if err != nil {
		return err
	}
	fmt.Fprintf(stdout, "Gateway identity: %s\n", identity)
	fmt.Fprintln(stdout, "Waiting for main acknowledgement...")
	ackID, err := waitForValidMainAck(stderr, state{Mode: "gateway", Identity: identity, PeerIdentity: mainID, Role: gatewayRole, StartedAt: startedAt}, readyID, *root, *timeout)
	if err != nil {
		return err
	}
	if err := saveState(*root, state{Mode: "gateway", Identity: identity, PeerIdentity: mainID, Role: gatewayRole, StartedAt: startedAt, PairedAt: nowText(), LastReadyID: readyID}); err != nil {
		return err
	}
	if _, err := runMail("", "read", ackID, "--identity", identity, rootArgs(*root)); err != nil {
		return err
	}
	fmt.Fprintf(stdout, "Paired with main identity: %s\n", mainID)
	fmt.Fprintln(stdout, "Gateway is paired and ready for human input.")
	fmt.Fprintln(stdout, "At the start of each human-facing turn, drain pending main messages with:")
	fmt.Fprintf(stdout, "%s listen --timeout 0 --identity %s%s\n", displayCommand(), identity, displayRootArg(*root))
	return nil
}

func waitForValidMainAck(stderr io.Writer, st state, readyID, root, timeoutText string) (string, error) {
	timeout, err := time.ParseDuration(timeoutText)
	if err != nil {
		return "", err
	}
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		remaining := time.Until(deadline)
		wait := time.Second
		if remaining < wait {
			wait = remaining
		}
		if wait <= 0 {
			break
		}
		line, err := runMail("", "inbox", "--wait", "--identity", st.Identity, "--to", st.Identity, "--contract", contractReady, "--responds-to", readyID, "--timeout", wait.String(), rootArgs(root))
		if err != nil {
			if isWaitTimeout(err) {
				continue
			}
			return "", err
		}
		for _, ackID := range mailIDPattern.FindAllString(line, -1) {
			read, err := runMail("", "read", ackID, "--identity", st.Identity, "--no-mark-read", rootArgs(root))
			if err != nil {
				return "", err
			}
			meta, body := readMailMetaFromText(read)
			if err := validateReadyForGateway(meta, body, st, readyID); err != nil {
				fmt.Fprintf(stderr, "Rejected %s: %v\n", ackID, err)
				if _, markErr := runMail("", "read", ackID, "--identity", st.Identity, rootArgs(root)); markErr != nil {
					return "", markErr
				}
				continue
			}
			return ackID, nil
		}
	}
	return "", fmt.Errorf("timed out waiting for valid main acknowledgement")
}

func cmdListen(args []string, stdout, stderr io.Writer) error {
	fs := flag.NewFlagSet("listen", flag.ContinueOnError)
	fs.SetOutput(stderr)
	root := fs.String("root", "", "Project root.")
	identity := fs.String("identity", "", "Identity.")
	timeout := fs.String("timeout", "24h", "Listen timeout.")
	stream := fs.Bool("stream", false, "Keep listening until timeout. Normal listen exits after the first valid delivery.")
	flagArgs, positional, err := splitArgs(args, map[string]bool{"root": true, "identity": true, "timeout": true, "stream": false})
	if err != nil {
		return err
	}
	if err := fs.Parse(flagArgs); err != nil {
		return err
	}
	if len(positional) != 0 {
		return errors.New("listen does not accept positional arguments")
	}
	timeoutProvided := flagProvided(args, "timeout")
	st, err := selectState(*root, *identity, "", true)
	if err != nil {
		return err
	}
	if st.Mode == "gateway" && !timeoutProvided {
		return errors.New("gateway listen requires explicit --timeout; use --timeout 0 to drain at human-turn boundaries, or --timeout <duration> only when intentionally waiting for main")
	}
	release, err := acquireListenerLock(*root, st.Identity)
	if err != nil {
		return err
	}
	defer release()
	printed, err := drainUnreadProtocols(stdout, stderr, st, *root)
	if err != nil {
		return err
	}
	if printed > 0 && !*stream {
		return nil
	}
	if *timeout == "" || *timeout == "0" {
		return nil
	}
	fmt.Fprintf(stderr, "Listening for protocol messages for identity %s...\n", st.Identity)
	return listenValidated(stdout, stderr, st, *root, *timeout, *stream)
}

func cmdSend(args []string, stdin io.Reader, stdout, stderr io.Writer) error {
	fs := flag.NewFlagSet("send", flag.ContinueOnError)
	fs.SetOutput(stderr)
	root := fs.String("root", "", "Project root.")
	identity := fs.String("identity", "", "Identity.")
	respondsTo := fs.String("responds-to", "", "Question message id this answer responds to.")
	flagArgs, positional, err := splitArgs(args, map[string]bool{"root": true, "identity": true, "responds-to": true})
	if err != nil {
		return err
	}
	if err := fs.Parse(flagArgs); err != nil {
		return err
	}
	if len(positional) != 1 {
		return errors.New("send requires subject")
	}
	st, err := selectState(*root, *identity, "", true)
	if err != nil {
		return err
	}
	body, err := readProtocolBody(stdin, "send")
	if err != nil {
		return err
	}
	if err := validateOutgoingBody(body, st, *respondsTo); err != nil {
		return err
	}
	sendArgs := []any{"send", "--to", st.PeerIdentity, "--subject", positional[0], "--identity", st.Identity, "--type", mailTypeForMethod(body), "--contract", contractMessage}
	if *respondsTo != "" {
		if err := validateRespondsToQuestion(st, *respondsTo, *root); err != nil {
			return err
		}
		if err := ensureNoExistingAnswer(st, *respondsTo, *root); err != nil {
			return err
		}
		sendArgs = append(sendArgs, "--responds-to", *respondsTo)
	}
	sendArgs = append(sendArgs, rootArgs(*root))
	out, err := runMail(body, sendArgs...)
	if err != nil {
		return err
	}
	id, err := firstMailID(out)
	if err != nil {
		return err
	}
	if *respondsTo != "" {
		if _, err := runMail("", "read", *respondsTo, "--identity", st.Identity, rootArgs(*root)); err != nil {
			return err
		}
	}
	fmt.Fprintf(stdout, "%s\n", id)
	return nil
}

func mailTypeForMethod(body string) string {
	switch bodyScalar(body, "method") {
	case "question":
		return "question"
	case "answer":
		return "decision"
	case "update":
		return "summary"
	default:
		return "note"
	}
}

func validateRespondsToQuestion(st state, questionID, root string) error {
	read, err := runMail("", "read", questionID, "--identity", st.Identity, "--no-mark-read", rootArgs(root))
	if err != nil {
		return err
	}
	meta, questionBody := readMailMetaFromText(read)
	return validateOriginalQuestion(meta, questionBody, st)
}

func ensureNoExistingAnswer(st state, questionID, root string) error {
	inbox, err := runMail("", "inbox", "--identity", st.PeerIdentity, "--contract", contractMessage, "--responds-to", questionID, rootArgs(root))
	if err != nil {
		return err
	}
	receiver := state{Mode: peerMode(st), Identity: st.PeerIdentity, PeerIdentity: st.Identity, Role: peerRole(st), PairedAt: st.PairedAt}
	for _, id := range mailIDPattern.FindAllString(inbox, -1) {
		read, err := runMail("", "read", id, "--identity", st.PeerIdentity, "--no-mark-read", rootArgs(root))
		if err != nil {
			return err
		}
		meta, body := readMailMetaFromText(read)
		if meta["contract"] != contractMessage || meta["responds_to"] != questionID {
			continue
		}
		if err := validateIncomingMessage(meta, body, receiver, questionID); err != nil {
			continue
		}
		return fmt.Errorf("question %s already has answer %s", questionID, meta["id"])
	}
	return nil
}

func peerMode(st state) string {
	if st.Mode == "gateway" {
		return "main"
	}
	return "gateway"
}

func peerRole(st state) string {
	if st.Mode == "gateway" {
		return mainRole
	}
	return gatewayRole
}

func cmdState(args []string, stdout, stderr io.Writer) error {
	fs := flag.NewFlagSet("state", flag.ContinueOnError)
	fs.SetOutput(stderr)
	root := fs.String("root", "", "Project root.")
	identity := fs.String("identity", "", "Identity.")
	flagArgs, positional, err := splitArgs(args, map[string]bool{"root": true, "identity": true})
	if err != nil {
		return err
	}
	if err := fs.Parse(flagArgs); err != nil {
		return err
	}
	if len(positional) != 0 {
		return errors.New("state does not accept positional arguments")
	}
	st, err := selectState(*root, *identity, "", false)
	if err != nil {
		return err
	}
	view := stateView{
		Mode:         st.Mode,
		Identity:     st.Identity,
		PeerIdentity: st.PeerIdentity,
		Role:         st.Role,
		StartedAt:    st.StartedAt,
		PairedAt:     st.PairedAt,
		LastReadyID:  st.LastReadyID,
		PairingState: pairingState(st),
	}
	if st.Mode == "main" {
		lock, alive, err := liveProcessLock(*root, st.Identity, "wait-ready")
		if err != nil {
			return err
		}
		view.WaitReady = &waitReadyView{
			Alive:     alive,
			PID:       lock.PID,
			StartedAt: lock.StartedAt,
			LogPath:   waitReadyLogPath(*root, st.Identity),
		}
	}
	raw, err := json.MarshalIndent(view, "", "  ")
	if err != nil {
		return err
	}
	fmt.Fprintln(stdout, string(raw))
	return nil
}

type stateView struct {
	Mode         string         `json:"mode"`
	Identity     string         `json:"identity"`
	PeerIdentity string         `json:"peer_identity,omitempty"`
	Role         string         `json:"role"`
	StartedAt    string         `json:"started_at,omitempty"`
	PairedAt     string         `json:"paired_at,omitempty"`
	LastReadyID  string         `json:"last_ready_id,omitempty"`
	PairingState string         `json:"pairing_state"`
	WaitReady    *waitReadyView `json:"wait_ready,omitempty"`
}

type waitReadyView struct {
	Alive     bool   `json:"alive"`
	PID       int    `json:"pid,omitempty"`
	StartedAt string `json:"started_at,omitempty"`
	LogPath   string `json:"log_path,omitempty"`
}

func pairingState(st state) string {
	if st.PairedAt != "" {
		return "paired"
	}
	if st.Mode == "gateway" && st.PeerIdentity != "" {
		return "waiting_for_main_ack"
	}
	if st.Mode == "main" {
		return "waiting_for_gateway"
	}
	return "created"
}

func printUnreadContract(stdout, stderr io.Writer, st state, contract, root string) (int, error) {
	inbox, err := runMail("", "inbox", "--identity", st.Identity, "--contract", contract, rootArgs(root))
	if err != nil {
		return 0, err
	}
	printed := 0
	for _, id := range mailIDPattern.FindAllString(inbox, -1) {
		didPrint, err := printValidatedMessage(stdout, stderr, st, id, contract, root)
		if err != nil {
			return printed, err
		}
		if didPrint {
			printed++
		}
	}
	return printed, nil
}

func drainUnreadProtocols(stdout, stderr io.Writer, st state, root string) (int, error) {
	return printUnreadContract(stdout, stderr, st, contractMessage, root)
}

func listenValidated(stdout, stderr io.Writer, st state, root, timeoutText string, stream bool) error {
	timeout, err := time.ParseDuration(timeoutText)
	if err != nil {
		return err
	}
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		remaining := time.Until(deadline)
		wait := time.Second
		if remaining < wait {
			wait = remaining
		}
		if wait <= 0 {
			break
		}
		line, err := runMail("", "inbox", "--wait", "--identity", st.Identity, "--contract", contractMessage, "--timeout", wait.String(), rootArgs(root))
		if err != nil {
			if isWaitTimeout(err) {
				continue
			}
			return err
		}
		for _, id := range mailIDPattern.FindAllString(line, -1) {
			printed, err := printValidatedMessage(stdout, stderr, st, id, contractMessage, root)
			if err != nil {
				return err
			}
			if printed && !stream {
				if _, err := drainUnreadProtocols(stdout, stderr, st, root); err != nil {
					return err
				}
				return nil
			}
		}
	}
	return nil
}

func isWaitTimeout(err error) bool {
	text := strings.ToLower(err.Error())
	return strings.Contains(text, "timeout") || strings.Contains(text, "timed out") || strings.Contains(text, "no matching")
}

func printValidatedMessage(stdout, stderr io.Writer, st state, id, contract, root string) (bool, error) {
	read, err := runMail("", "read", id, "--identity", st.Identity, "--no-mark-read", rootArgs(root))
	if err != nil {
		return false, err
	}
	meta, body := readMailMetaFromText(read)
	if err := validateIncomingByContract(meta, body, st, contract, root); err != nil {
		fmt.Fprintf(stderr, "Rejected %s: %v\n", id, err)
		_, markErr := runMail("", "read", id, "--identity", st.Identity, rootArgs(root))
		return false, markErr
	}
	marked, err := runMail("", "read", id, "--identity", st.Identity, rootArgs(root))
	if err != nil {
		return false, err
	}
	fmt.Fprint(stdout, marked)
	if !strings.HasSuffix(marked, "\n") {
		fmt.Fprintln(stdout)
	}
	return true, nil
}

func validateIncomingByContract(meta map[string]string, body string, st state, contract, root string) error {
	if contract != contractMessage {
		return fmt.Errorf("unsupported contract %q", contract)
	}
	if err := validateIncomingMessage(meta, body, st, meta["responds_to"]); err != nil {
		return err
	}
	if bodyScalar(body, "method") != "answer" {
		return nil
	}
	requestID := meta["responds_to"]
	requestRead, err := runMail("", "read", requestID, "--identity", st.Identity, "--no-mark-read", "--force", rootArgs(root))
	if err != nil {
		return err
	}
	requestMeta, requestBody := readMailMetaFromText(requestRead)
	questionReceiver := state{
		Mode:         peerMode(st),
		Identity:     st.PeerIdentity,
		PeerIdentity: st.Identity,
		Role:         peerRole(st),
		PairedAt:     st.PairedAt,
	}
	return validateOriginalQuestion(requestMeta, requestBody, questionReceiver)
}

func readProtocolBody(stdin io.Reader, command string) (string, error) {
	body, err := io.ReadAll(stdin)
	if err != nil {
		return "", err
	}
	text := string(body)
	if strings.TrimSpace(text) == "" {
		return "", fmt.Errorf("%s body is required on stdin", command)
	}
	return text, nil
}

func displayRootArg(root string) string {
	if strings.TrimSpace(root) == "" {
		return ""
	}
	return fmt.Sprintf(" --root %q", root)
}

func displayCommand() string {
	if command := strings.TrimSpace(os.Getenv("FRONT_AGENT_CMD")); command != "" {
		return command
	}
	return os.Args[0]
}
