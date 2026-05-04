package frontagent

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

func TestMain(m *testing.M) {
	os.Setenv("FRONT_AGENT_MAIL_BACKEND", "memory")
	os.Setenv("FRONT_AGENT_TEST_IN_PROCESS_DETACH", "1")
	os.Exit(m.Run())
}

func TestSendQuestionAnswerAndListen(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	questionID := strings.TrimSpace(runCLI(t, []string{
		"send", "Need direction",
		"--root", root,
		"--identity", mainID,
	}, mainQuestionBody()))

	answerID := strings.TrimSpace(runCLI(t, []string{
		"send", "Direction confirmed",
		"--root", root,
		"--identity", gatewayID,
		"--responds-to", questionID,
	}, gatewayAnswerBody("Prototype.")))

	listenOut := runCLI(t, []string{
		"listen",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, "")

	if !strings.Contains(listenOut, answerID) {
		t.Fatalf("listen output missing answer id %q:\n%s", answerID, listenOut)
	}
	if !strings.Contains(listenOut, "answer: Prototype.") {
		t.Fatalf("listen output missing answer body:\n%s", listenOut)
	}
}

func TestGatewayWorkRequiresHumanConfirmation(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Start work",
		"--root", root,
		"--identity", gatewayID,
	}, strings.NewReader("```yaml\nmethod: work\nfrom_role: gateway\nto_role: main\nsummary: Start work.\naction: start\n```\n"), &stdout, &stderr)

	if err == nil {
		t.Fatalf("expected missing human confirmation to be rejected, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "human_confirmed") {
		t.Fatalf("error = %q, want human_confirmed", err.Error())
	}
}

func TestProtocolBodyMustBeFencedYAML(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Start work",
		"--root", root,
		"--identity", gatewayID,
	}, strings.NewReader("method: work\nfrom_role: gateway\nto_role: main\nsummary: Start work.\nhuman_confirmed: true\n"), &stdout, &stderr)

	if err == nil {
		t.Fatalf("expected unfenced body to be rejected, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "fenced YAML") {
		t.Fatalf("error = %q, want fenced YAML", err.Error())
	}
}

func TestProtocolBodyMustBeValidYAMLWithoutDuplicateKeys(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	for name, body := range map[string]string{
		"malformed": "```yaml\nmethod: work\nfrom_role: gateway\nto_role: main\nsummary: [unterminated\nhuman_confirmed: true\n```",
		"duplicate": "```yaml\nmethod: work\nfrom_role: gateway\nto_role: main\nsummary: Start work.\nhuman_confirmed: true\nhuman_confirmed: false\n```",
	} {
		var stdout, stderr bytes.Buffer
		err := Run([]string{
			"send", name,
			"--root", root,
			"--identity", gatewayID,
		}, strings.NewReader(body), &stdout, &stderr)
		if err == nil {
			t.Fatalf("expected %s body to be rejected, stdout=%q stderr=%q", name, stdout.String(), stderr.String())
		}
	}
}

func TestProtocolVersionIsRemoved(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Start work",
		"--root", root,
		"--identity", gatewayID,
	}, strings.NewReader("```yaml\nprotocol_version: 2\nmethod: work\nfrom_role: gateway\nto_role: main\nsummary: Start work.\nhuman_confirmed: true\n```\n"), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected protocol_version to be rejected, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "protocol_version is not used") {
		t.Fatalf("error = %q, want protocol_version is not used", err.Error())
	}
}

func TestOldMethodsAreRejected(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Old task",
		"--root", root,
		"--identity", gatewayID,
	}, strings.NewReader("```yaml\nmethod: task.start\nfrom_role: gateway\nto_role: main\nsummary: Start task.\nhuman_confirmed: true\n```\n"), &stdout, &stderr)

	if err == nil {
		t.Fatalf("expected old method to be rejected, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "not allowed") {
		t.Fatalf("error = %q, want not allowed", err.Error())
	}
}

func TestGatewayCanSubmitWorkAndMainCanListen(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	workID := strings.TrimSpace(runCLI(t, []string{
		"send", "Start work",
		"--root", root,
		"--identity", gatewayID,
	}, gatewayWorkBody()))

	listenOut := runCLI(t, []string{
		"listen",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, "")

	if !strings.Contains(listenOut, workID) {
		t.Fatalf("listen output missing work id %q:\n%s", workID, listenOut)
	}
	if !strings.Contains(listenOut, "method: work") {
		t.Fatalf("listen output missing work body:\n%s", listenOut)
	}
}

func TestListenDrainsAllUnreadMessages(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	questionID := strings.TrimSpace(runCLI(t, []string{
		"send", "Need direction",
		"--root", root,
		"--identity", mainID,
	}, mainQuestionBody()))
	answerID := strings.TrimSpace(runCLI(t, []string{
		"send", "Direction confirmed",
		"--root", root,
		"--identity", gatewayID,
		"--responds-to", questionID,
	}, gatewayAnswerBody("Prototype.")))
	workID := strings.TrimSpace(runCLI(t, []string{
		"send", "Start work",
		"--root", root,
		"--identity", gatewayID,
	}, gatewayWorkBody()))

	listenOut := runCLI(t, []string{
		"listen",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, "")

	for _, id := range []string{answerID, workID} {
		if !strings.Contains(listenOut, id) {
			t.Fatalf("listen output missing %s:\n%s", id, listenOut)
		}
	}
}

func TestGatewayListenRequiresExplicitTimeout(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"listen",
		"--root", root,
		"--identity", gatewayID,
	}, strings.NewReader(""), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected gateway bare listen to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "requires explicit --timeout") {
		t.Fatalf("error = %q, want explicit timeout guidance", err.Error())
	}

	runCLI(t, []string{
		"listen",
		"--root", root,
		"--identity", gatewayID,
		"--timeout", "0",
	}, "")
}

func TestListenRejectsConcurrentListenerForSameIdentity(t *testing.T) {
	root := t.TempDir()
	mainID, _ := pairSessions(t, root)

	done := make(chan error, 1)
	go func() {
		var stdout, stderr bytes.Buffer
		err := Run([]string{
			"listen",
			"--root", root,
			"--identity", mainID,
			"--timeout", "500ms",
		}, strings.NewReader(""), &stdout, &stderr)
		if err != nil {
			err = fmt.Errorf("%w; stdout=%q stderr=%q", err, stdout.String(), stderr.String())
		}
		done <- err
	}()

	waitForListenerLock(t, root, mainID)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"listen",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, strings.NewReader(""), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected concurrent listen to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "already running") {
		t.Fatalf("error = %q, want already running", err.Error())
	}

	select {
	case err := <-done:
		if err != nil {
			t.Fatal(err)
		}
	case <-time.After(3 * time.Second):
		t.Fatal("first listen did not finish")
	}
}

func TestWaitReadyRejectsAlreadyPairedMain(t *testing.T) {
	root := t.TempDir()
	mainID, _ := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"wait-ready",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, strings.NewReader(""), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected already paired wait-ready to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "already paired") {
		t.Fatalf("error = %q, want already paired", err.Error())
	}
}

func TestListenCleansStaleListenerLock(t *testing.T) {
	root := t.TempDir()
	mainID, _ := pairSessions(t, root)
	dir, err := listenerLockDir(root)
	if err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(dir, 0700); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(dir, mainID+".json"), []byte(`{"identity":"`+mainID+`","pid":-1,"started_at":"stale"}`+"\n"), 0600); err != nil {
		t.Fatal(err)
	}

	runCLI(t, []string{
		"listen",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, "")

	if _, err := os.Stat(filepath.Join(dir, mainID+".json")); !os.IsNotExist(err) {
		t.Fatalf("stale listener lock was not removed, stat error=%v", err)
	}
}

func TestListenWaitsForOneValidMessageThenExits(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	type result struct {
		out string
		err error
	}
	done := make(chan result, 1)
	go func() {
		var stdout, stderr bytes.Buffer
		err := Run([]string{
			"listen",
			"--root", root,
			"--identity", mainID,
			"--timeout", "5s",
		}, strings.NewReader(""), &stdout, &stderr)
		if err != nil {
			err = fmt.Errorf("%w; stdout=%q stderr=%q", err, stdout.String(), stderr.String())
		}
		done <- result{out: stdout.String(), err: err}
	}()

	waitForListenerLock(t, root, mainID)
	workID := strings.TrimSpace(runCLI(t, []string{
		"send", "Start work",
		"--root", root,
		"--identity", gatewayID,
	}, gatewayWorkBody()))

	select {
	case got := <-done:
		if got.err != nil {
			t.Fatal(got.err)
		}
		if !strings.Contains(got.out, workID) || !strings.Contains(got.out, "method: work") {
			t.Fatalf("listen output missing work %q:\n%s", workID, got.out)
		}
	case <-time.After(6 * time.Second):
		t.Fatal("listen did not exit after first valid message")
	}
}

func TestListenRejectsSpoofedProtocolMessage(t *testing.T) {
	root := t.TempDir()
	mainID, _ := pairSessions(t, root)

	spoofStart, err := runMail("", "start", "--role", gatewayRole, rootArgs(root))
	if err != nil {
		t.Fatal(err)
	}
	spoofID, err := parseField(spoofStart, "identity")
	if err != nil {
		t.Fatal(err)
	}
	_, err = runMail(gatewayWorkBody(), "send",
		"--to", mainID,
		"--subject", "Spoofed work",
		"--identity", spoofID,
		"--type", "question",
		"--contract", contractMessage,
		rootArgs(root),
	)
	if err != nil {
		t.Fatal(err)
	}

	var stdout, stderr bytes.Buffer
	err = Run([]string{
		"listen",
		"--root", root,
		"--identity", mainID,
		"--timeout", "0",
	}, strings.NewReader(""), &stdout, &stderr)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(stdout.String(), "method: work") {
		t.Fatalf("listen printed spoofed body:\nstdout:\n%s\nstderr:\n%s", stdout.String(), stderr.String())
	}
	if !strings.Contains(stderr.String(), "Rejected") {
		t.Fatalf("listen did not report rejected spoof:\nstdout:\n%s\nstderr:\n%s", stdout.String(), stderr.String())
	}
}

func TestMainCanSendUpdateToGateway(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	updateID := strings.TrimSpace(runCLI(t, []string{
		"send", "Work accepted",
		"--root", root,
		"--identity", mainID,
	}, mainUpdateAcceptedBody()))

	listenOut := runCLI(t, []string{
		"listen",
		"--root", root,
		"--identity", gatewayID,
		"--timeout", "0",
	}, "")
	if !strings.Contains(listenOut, updateID) {
		t.Fatalf("listen output missing update %q:\n%s", updateID, listenOut)
	}
	if !strings.Contains(listenOut, "method: update") {
		t.Fatalf("listen output missing update body:\n%s", listenOut)
	}
}

func TestAnswerRequiresRespondsTo(t *testing.T) {
	root := t.TempDir()
	_, gatewayID := pairSessions(t, root)

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Direction confirmed",
		"--root", root,
		"--identity", gatewayID,
	}, strings.NewReader(gatewayAnswerBody("Prototype.")), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected answer without responds-to to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "answer requires --responds-to") {
		t.Fatalf("error = %q, want responds-to guidance", err.Error())
	}
}

func TestDuplicateAnswerRejected(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	questionID := strings.TrimSpace(runCLI(t, []string{
		"send", "Need direction",
		"--root", root,
		"--identity", mainID,
	}, mainQuestionBody()))

	_ = strings.TrimSpace(runCLI(t, []string{
		"send", "Direction confirmed",
		"--root", root,
		"--identity", gatewayID,
		"--responds-to", questionID,
	}, gatewayAnswerBody("Prototype.")))

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Direction confirmed again",
		"--root", root,
		"--identity", gatewayID,
		"--responds-to", questionID,
	}, strings.NewReader(gatewayAnswerBody("Production.")), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected duplicate answer to be rejected, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "already has answer") {
		t.Fatalf("error = %q, want already has answer", err.Error())
	}
}

func TestDashLeadingSubjectUsesDoubleDash(t *testing.T) {
	root := t.TempDir()
	mainID, gatewayID := pairSessions(t, root)

	messageID := strings.TrimSpace(runCLI(t, []string{
		"send",
		"--root", root,
		"--identity", mainID,
		"--", "-dash subject",
	}, mainQuestionBody()))

	meta, err := readMailMeta(messageID, gatewayID, root)
	if err != nil {
		t.Fatal(err)
	}
	if got, want := meta["subject"], "-dash subject"; got != want {
		t.Fatalf("subject = %q, want %q", got, want)
	}
}

func TestMainPrintsRootAndStartsPairingWaiter(t *testing.T) {
	root := t.TempDir()
	t.Setenv("FRONT_AGENT_CMD", "/tmp/front-agent")
	out := runCLI(t, []string{"main", "--root", root}, "")
	mainID := parseIdentity(t, out, "Main identity:")

	if !strings.Contains(out, fmt.Sprintf("--root %q", root)) {
		t.Fatalf("main output missing quoted root %q:\n%s", root, out)
	}
	if !strings.Contains(out, "Detached pairing waiter PID:") {
		t.Fatalf("main output missing detached pairing waiter pid:\n%s", out)
	}
	if strings.Contains(out, "--token") || strings.Contains(out, "Pairing token:") {
		t.Fatalf("main output still mentions removed token pairing:\n%s", out)
	}
	if strings.Contains(out, "wait-ready --identity") {
		t.Fatalf("main output exposes hidden wait-ready command:\n%s", out)
	}
	if !strings.Contains(out, fmt.Sprintf("$front-agent-orchestration gateway %s --root %q", mainID, root)) {
		t.Fatalf("main output missing rooted gateway command:\n%s", out)
	}
	if lock, alive, err := liveProcessLock(root, mainID, "wait-ready"); err != nil {
		t.Fatal(err)
	} else if !alive || lock.PID == 0 {
		t.Fatalf("main did not start live pairing waiter: %+v alive=%v", lock, alive)
	}
}

func TestHelpShowsMinimalPublicCommands(t *testing.T) {
	var stdout, stderr bytes.Buffer
	if err := Run([]string{"help"}, strings.NewReader(""), &stdout, &stderr); err != nil {
		t.Fatalf("help failed: %v", err)
	}
	out := stdout.String()
	for _, want := range []string{
		"main [--root <path>]",
		"gateway <main-identity> [--root <path>] [--timeout 24h]",
		"listen [--root <path>] [--identity <id>] [--timeout 24h]",
		"send \"Subject\" [--root <path>] [--identity <id>] [--responds-to <message-id>]",
		"state [--root <path>] [--identity <id>]",
	} {
		if !strings.Contains(out, want) {
			t.Fatalf("help output missing %q:\n%s", want, out)
		}
	}
	for _, removed := range []string{" request ", " respond ", " event ", " wait <request-id>", "wait-ready"} {
		if strings.Contains(out, removed) {
			t.Fatalf("help output contains removed command %q:\n%s", removed, out)
		}
	}
}

func TestGatewayRejectsRemovedTokenFlag(t *testing.T) {
	root := t.TempDir()
	mainOut := runCLI(t, []string{"main", "--root", root}, "")
	mainID := parseIdentity(t, mainOut, "Main identity:")

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"gateway", mainID,
		"--token", "old",
		"--root", root,
	}, strings.NewReader(""), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected removed token flag to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "no longer accepts --token") {
		t.Fatalf("error = %q, want no longer accepts --token", err.Error())
	}
}

func TestGatewayFailsClearlyWithoutLivePairingWaiter(t *testing.T) {
	root := t.TempDir()
	mainOut := runCLI(t, []string{"main", "--root", root}, "")
	mainID := parseIdentity(t, mainOut, "Main identity:")
	waitDir, err := processLockDir(root, "wait-ready")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.Remove(filepath.Join(waitDir, mainID+".json")); err != nil {
		t.Fatal(err)
	}

	var stdout, stderr bytes.Buffer
	err = Run([]string{
		"gateway", mainID,
		"--root", root,
		"--timeout", "100ms",
	}, strings.NewReader(""), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected missing pairing waiter to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "pairing waiter is not running") {
		t.Fatalf("error = %q, want pairing waiter is not running", err.Error())
	}
}

func TestRestartedWaitReadyConsumesExistingGatewayReady(t *testing.T) {
	root := t.TempDir()
	mainID := createMainWithoutWaiter(t, root)

	gatewayStart, err := runMail("", "start", "--role", gatewayRole, rootArgs(root))
	if err != nil {
		t.Fatal(err)
	}
	gatewayID, err := parseField(gatewayStart, "identity")
	if err != nil {
		t.Fatal(err)
	}
	if err := saveState(root, state{Mode: "gateway", Identity: gatewayID, PeerIdentity: mainID, Role: gatewayRole, StartedAt: nowText()}); err != nil {
		t.Fatal(err)
	}
	release, _, err := acquireProcessLock(root, gatewayID, "gateway-ready", "front-agent gateway already waiting for identity %s with pid %d")
	if err != nil {
		t.Fatal(err)
	}
	defer release()
	body := fmt.Sprintf("```yaml\nmode: gateway\nidentity: %s\npeer_identity: %s\nready: true\n```\n", gatewayID, mainID)
	readyOut, err := runMail(body, "send",
		"--to", mainID,
		"--subject", "Gateway ready",
		"--identity", gatewayID,
		"--type", "summary",
		"--contract", contractReady,
		rootArgs(root),
	)
	if err != nil {
		t.Fatal(err)
	}
	readyID := mustFirstMailID(t, readyOut)

	waitOut := runCLI(t, []string{
		"wait-ready",
		"--root", root,
		"--identity", mainID,
		"--timeout", "1s",
	}, "")
	if !strings.Contains(waitOut, "Paired with gateway identity: "+gatewayID) {
		t.Fatalf("wait-ready did not pair existing gateway ready:\n%s", waitOut)
	}
	mainState, err := selectState(root, mainID, "main", true)
	if err != nil {
		t.Fatal(err)
	}
	if mainState.LastReadyID != readyID || mainState.PeerIdentity != gatewayID {
		t.Fatalf("main state after restarted wait-ready = %+v, want ready %s peer %s", mainState, readyID, gatewayID)
	}
}

func TestWaitReadyRejectsDeadGatewayReady(t *testing.T) {
	root := t.TempDir()
	mainID := createMainWithoutWaiter(t, root)

	gatewayStart, err := runMail("", "start", "--role", gatewayRole, rootArgs(root))
	if err != nil {
		t.Fatal(err)
	}
	gatewayID, err := parseField(gatewayStart, "identity")
	if err != nil {
		t.Fatal(err)
	}
	if err := saveState(root, state{Mode: "gateway", Identity: gatewayID, PeerIdentity: mainID, Role: gatewayRole, StartedAt: nowText()}); err != nil {
		t.Fatal(err)
	}
	body := fmt.Sprintf("```yaml\nmode: gateway\nidentity: %s\npeer_identity: %s\nready: true\n```\n", gatewayID, mainID)
	_, err = runMail(body, "send",
		"--to", mainID,
		"--subject", "Gateway ready",
		"--identity", gatewayID,
		"--type", "summary",
		"--contract", contractReady,
		rootArgs(root),
	)
	if err != nil {
		t.Fatal(err)
	}

	var stdout, stderr bytes.Buffer
	err = Run([]string{
		"wait-ready",
		"--root", root,
		"--identity", mainID,
		"--timeout", "100ms",
	}, strings.NewReader(""), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected dead gateway readiness to fail, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(stderr.String(), "gateway readiness sender "+gatewayID+" is not live") {
		t.Fatalf("stderr = %q, want dead gateway rejection", stderr.String())
	}
	mainState, err := selectState(root, mainID, "main", false)
	if err != nil {
		t.Fatal(err)
	}
	if mainState.PairedAt != "" || mainState.PeerIdentity != "" {
		t.Fatalf("main paired with dead gateway: %+v", mainState)
	}
}

func TestSelectStatePrefersRequestedGatewayMode(t *testing.T) {
	root := t.TempDir()
	mainID := "main-id"
	gatewayID := "gateway-id"
	if err := saveState(root, state{Mode: "main", Identity: mainID, PeerIdentity: gatewayID, Role: mainRole, PairedAt: nowText()}); err != nil {
		t.Fatal(err)
	}
	if err := saveState(root, state{Mode: "gateway", Identity: gatewayID, PeerIdentity: mainID, Role: gatewayRole, PairedAt: nowText()}); err != nil {
		t.Fatal(err)
	}

	st, err := selectState(root, "", "gateway", true)
	if err != nil {
		t.Fatal(err)
	}
	if st.Identity != gatewayID {
		t.Fatalf("selected identity = %q, want %q", st.Identity, gatewayID)
	}
}

func TestLegacyCommandsAreRemoved(t *testing.T) {
	for _, command := range []string{"request", "respond", "event", "wait", "ask", "tell", "monitor"} {
		var stdout, stderr bytes.Buffer
		err := Run([]string{command}, strings.NewReader(""), &stdout, &stderr)
		if err == nil {
			t.Fatalf("expected %s to be removed, stdout=%q stderr=%q", command, stdout.String(), stderr.String())
		}
		if !strings.Contains(err.Error(), "removed") && !strings.Contains(err.Error(), "unknown command") {
			t.Fatalf("%s error = %q, want removed or unknown command", command, err.Error())
		}
	}
}

func TestLatestDocsOnly(t *testing.T) {
	forbidden := []string{
		"protocol_version",
		"front_request",
		"front_response",
		"front_event",
		"task.",
		"human.decision",
		"human.clarification",
	}
	err := filepath.WalkDir(".", func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if entry.IsDir() {
			switch entry.Name() {
			case ".git", ".front-agent":
				return filepath.SkipDir
			default:
				return nil
			}
		}
		switch filepath.Ext(path) {
		case ".md", ".yaml", ".yml", ".sh":
		default:
			return nil
		}
		raw, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		text := strings.ToLower(string(raw))
		for _, needle := range forbidden {
			if strings.Contains(text, needle) {
				t.Fatalf("%s contains removed protocol reference %q", path, needle)
			}
		}
		return nil
	})
	if err != nil {
		t.Fatal(err)
	}
}

func TestSendRejectsUnpairedState(t *testing.T) {
	root := t.TempDir()
	if err := saveState(root, state{Mode: "gateway", Identity: "gateway-id", PeerIdentity: "main-id", Role: gatewayRole}); err != nil {
		t.Fatal(err)
	}

	var stdout, stderr bytes.Buffer
	err := Run([]string{
		"send", "Direction",
		"--root", root,
		"--identity", "gateway-id",
	}, strings.NewReader(gatewayWorkBody()), &stdout, &stderr)
	if err == nil {
		t.Fatalf("expected unpaired gateway error, stdout=%q stderr=%q", stdout.String(), stderr.String())
	}
	if !strings.Contains(err.Error(), "not paired") {
		t.Fatalf("error = %q, want not paired", err.Error())
	}
}

func pairSessions(t *testing.T, root string) (string, string) {
	t.Helper()

	mainOut := runCLI(t, []string{"main", "--root", root}, "")
	mainID := parseIdentity(t, mainOut, "Main identity:")
	waitForWaitReadyLock(t, root, mainID)

	gatewayOut := runCLI(t, []string{
		"gateway", mainID,
		"--root", root,
		"--timeout", "5s",
	}, "")
	gatewayID := parseIdentity(t, gatewayOut, "Gateway identity:")

	return mainID, gatewayID
}

func createMainWithoutWaiter(t *testing.T, root string) string {
	t.Helper()
	start, err := runMail("", "start", "--role", mainRole, rootArgs(root))
	if err != nil {
		t.Fatal(err)
	}
	mainID, err := parseField(start, "identity")
	if err != nil {
		t.Fatal(err)
	}
	if err := saveState(root, state{Mode: "main", Identity: mainID, Role: mainRole, StartedAt: nowText()}); err != nil {
		t.Fatal(err)
	}
	return mainID
}

func waitForWaitReadyLock(t *testing.T, root, identity string) {
	t.Helper()
	dir, err := processLockDir(root, "wait-ready")
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(dir, identity+".json")
	deadline := time.Now().Add(2 * time.Second)
	for time.Now().Before(deadline) {
		if _, err := os.Stat(path); err == nil {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("wait-ready lock %s was not created", path)
}

func runCLI(t *testing.T, args []string, stdin string) string {
	t.Helper()
	var stdout, stderr bytes.Buffer
	var input io.Reader = strings.NewReader(stdin)
	if err := Run(args, input, &stdout, &stderr); err != nil {
		t.Fatalf("Run(%v) failed: %v\nstdout:\n%s\nstderr:\n%s", args, err, stdout.String(), stderr.String())
	}
	return stdout.String()
}

func parseIdentity(t *testing.T, out, prefix string) string {
	t.Helper()
	for _, line := range strings.Split(out, "\n") {
		if value, ok := strings.CutPrefix(line, prefix); ok {
			value = strings.TrimSpace(value)
			if value != "" {
				return value
			}
		}
	}
	t.Fatalf("missing %q in output:\n%s", prefix, out)
	return ""
}

func waitForListenerLock(t *testing.T, root, identity string) {
	t.Helper()
	dir, err := listenerLockDir(root)
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(dir, identity+".json")
	deadline := time.Now().Add(2 * time.Second)
	for time.Now().Before(deadline) {
		if _, err := os.Stat(path); err == nil {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("listener lock %s was not created", path)
}

func mainQuestionBody() string {
	return "```yaml\nmethod: question\nfrom_role: main\nto_role: gateway\nsummary: Choose implementation direction.\nquestion: Prototype or production?\n```\n"
}

func gatewayAnswerBody(answer string) string {
	return fmt.Sprintf("```yaml\nmethod: answer\nfrom_role: gateway\nto_role: main\nsummary: Decision confirmed.\nhuman_confirmed: true\nanswer: %s\n```\n", answer)
}

func gatewayWorkBody() string {
	return "```yaml\nmethod: work\nfrom_role: gateway\nto_role: main\nsummary: Implement feature.\nhuman_confirmed: true\naction: start\nrequirements:\n  - Add the feature.\nacceptance_criteria:\n  - Tests pass.\n```\n"
}

func mainUpdateAcceptedBody() string {
	return "```yaml\nmethod: update\nfrom_role: main\nto_role: gateway\nsummary: Work accepted.\nstatus: accepted\n```\n"
}

func mustFirstMailID(t *testing.T, out string) string {
	t.Helper()
	id, err := firstMailID(out)
	if err != nil {
		t.Fatalf("missing mail id in output:\n%s", out)
	}
	return id
}
