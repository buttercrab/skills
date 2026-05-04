package frontagent

import (
	"fmt"
	"strings"

	"gopkg.in/yaml.v3"
)

const (
	contractReady   = "front_ready"
	contractMessage = "front_message"

	roleMain    = "main"
	roleGateway = "gateway"
)

func validateReadyForMain(meta map[string]string, body string, st state) error {
	if err := validateReadyMeta(meta, st.Identity, ""); err != nil {
		return err
	}
	if err := validateNotStale(meta, st.StartedAt); err != nil {
		return err
	}
	if bodyScalar(body, "mode") != "gateway" {
		return fmt.Errorf("front_ready body mode %q does not match gateway", bodyScalar(body, "mode"))
	}
	if bodyScalar(body, "identity") != meta["from"] {
		return fmt.Errorf("front_ready body identity %q does not match sender %q", bodyScalar(body, "identity"), meta["from"])
	}
	if bodyScalar(body, "peer_identity") != st.Identity {
		return fmt.Errorf("front_ready body peer_identity %q does not match main %q", bodyScalar(body, "peer_identity"), st.Identity)
	}
	if bodyScalar(body, "ready") != "true" {
		return errorsForReady("ready", bodyScalar(body, "ready"))
	}
	return nil
}

func validateReadyForGateway(meta map[string]string, body string, st state, readyID string) error {
	if err := validateReadyMeta(meta, st.Identity, readyID); err != nil {
		return err
	}
	if err := validateNotStale(meta, st.StartedAt); err != nil {
		return err
	}
	if meta["from"] != st.PeerIdentity {
		return fmt.Errorf("front_ready sender %q does not match main %q", meta["from"], st.PeerIdentity)
	}
	if bodyScalar(body, "mode") != "main" {
		return fmt.Errorf("front_ready body mode %q does not match main", bodyScalar(body, "mode"))
	}
	if bodyScalar(body, "identity") != st.PeerIdentity {
		return fmt.Errorf("front_ready body identity %q does not match main %q", bodyScalar(body, "identity"), st.PeerIdentity)
	}
	if bodyScalar(body, "peer_identity") != st.Identity {
		return fmt.Errorf("front_ready body peer_identity %q does not match gateway %q", bodyScalar(body, "peer_identity"), st.Identity)
	}
	if bodyScalar(body, "ready") != "true" {
		return errorsForReady("ready", bodyScalar(body, "ready"))
	}
	return nil
}

func validateReadyMeta(meta map[string]string, to, respondsTo string) error {
	if meta["contract"] != contractReady {
		return fmt.Errorf("message %s is not a front_ready", meta["id"])
	}
	if meta["from"] == "" {
		return fmt.Errorf("front_ready %s is missing sender", meta["id"])
	}
	if meta["to"] != to {
		return fmt.Errorf("front_ready recipient %q does not match identity %q", meta["to"], to)
	}
	if respondsTo != "" && meta["responds_to"] != respondsTo {
		return fmt.Errorf("front_ready responds_to %q does not match ready %q", meta["responds_to"], respondsTo)
	}
	return nil
}

func errorsForReady(key, value string) error {
	return fmt.Errorf("front_ready body %s %q does not match true", key, value)
}

func validateOutgoingBody(body string, st state, respondsTo string) error {
	if err := validateEnvelopeBody(body, roleName(st), peerRoleName(st)); err != nil {
		return err
	}
	return validateMessageBody(body, roleName(st), respondsTo)
}

func validateIncomingMessage(meta map[string]string, body string, st state, respondsTo string) error {
	if err := validatePairedMeta(meta, st, contractMessage, respondsTo); err != nil {
		return err
	}
	if err := validateEnvelopeBody(body, peerRoleName(st), roleName(st)); err != nil {
		return err
	}
	return validateMessageBody(body, peerRoleName(st), meta["responds_to"])
}

func validatePairedMeta(meta map[string]string, st state, contract, respondsTo string) error {
	if meta["contract"] != contract {
		return fmt.Errorf("message %s is not a %s", meta["id"], contract)
	}
	if respondsTo != "" && meta["responds_to"] != respondsTo {
		return fmt.Errorf("%s responds_to %q does not match request %q", contract, meta["responds_to"], respondsTo)
	}
	if meta["from"] != st.PeerIdentity {
		return fmt.Errorf("%s sender %q does not match paired peer %q", contract, meta["from"], st.PeerIdentity)
	}
	if meta["to"] != st.Identity {
		return fmt.Errorf("%s recipient %q does not match identity %q", contract, meta["to"], st.Identity)
	}
	if err := validateNotStale(meta, st.PairedAt); err != nil {
		return err
	}
	return nil
}

func validateEnvelopeBody(body, fromRole, toRole string) error {
	if err := validateProtocolBodyFormat(body); err != nil {
		return err
	}
	if strings.TrimSpace(bodyScalar(body, "protocol_version")) != "" {
		return fmt.Errorf("protocol_version is not used")
	}
	method := bodyScalar(body, "method")
	if strings.TrimSpace(method) == "" {
		return fmt.Errorf("method is required")
	}
	if bodyScalar(body, "from_role") != fromRole {
		return fmt.Errorf("from_role %q does not match %q", bodyScalar(body, "from_role"), fromRole)
	}
	if bodyScalar(body, "to_role") != toRole {
		return fmt.Errorf("to_role %q does not match %q", bodyScalar(body, "to_role"), toRole)
	}
	if strings.TrimSpace(bodyScalar(body, "summary")) == "" {
		return fmt.Errorf("summary is required")
	}
	return nil
}

func validateMessageBody(body, fromRole, respondsTo string) error {
	method := bodyScalar(body, "method")
	if !allowedMessageMethod(fromRole, method) {
		return fmt.Errorf("method %q is not allowed from %s", method, fromRole)
	}
	if method == "answer" && strings.TrimSpace(respondsTo) == "" {
		return fmt.Errorf("answer requires --responds-to")
	}
	if method != "answer" && strings.TrimSpace(respondsTo) != "" {
		return fmt.Errorf("--responds-to is only valid for answer")
	}
	if requiresHumanConfirmation(fromRole) && bodyScalar(body, "human_confirmed") != "true" {
		return fmt.Errorf("%s from gateway requires human_confirmed: true", method)
	}
	return nil
}

func validateOriginalQuestion(meta map[string]string, body string, st state) error {
	if meta["contract"] != contractMessage {
		return fmt.Errorf("message %s is not a %s", meta["id"], contractMessage)
	}
	if meta["from"] != st.PeerIdentity {
		return fmt.Errorf("front_message sender %q does not match paired peer %q", meta["from"], st.PeerIdentity)
	}
	if meta["to"] != st.Identity {
		return fmt.Errorf("front_message recipient %q does not match identity %q", meta["to"], st.Identity)
	}
	if err := validateNotStale(meta, st.PairedAt); err != nil {
		return err
	}
	if err := validateEnvelopeBody(body, peerRoleName(st), roleName(st)); err != nil {
		return err
	}
	if bodyScalar(body, "method") != "question" {
		return fmt.Errorf("answer responds_to must reference question, got %q", bodyScalar(body, "method"))
	}
	return validateMessageBody(body, peerRoleName(st), "")
}

func allowedMessageMethod(fromRole, method string) bool {
	switch fromRole {
	case roleGateway:
		return method == "work" || method == "answer" || method == "note"
	case roleMain:
		return method == "update" || method == "question" || method == "note"
	default:
		return false
	}
}

func requiresHumanConfirmation(fromRole string) bool {
	return fromRole == roleGateway
}

func validateProtocolBodyFormat(body string) error {
	text := strings.TrimSpace(body)
	if !strings.HasPrefix(text, "```yaml\n") {
		return fmt.Errorf("protocol body must be fenced YAML starting with ```yaml")
	}
	if !strings.HasSuffix(text, "\n```") {
		return fmt.Errorf("protocol body must end with closing YAML fence")
	}
	payload := strings.TrimSuffix(strings.TrimPrefix(text, "```yaml\n"), "\n```")
	if strings.Contains(payload, "```") {
		return fmt.Errorf("protocol body must not contain nested fences")
	}
	var node yaml.Node
	if err := yaml.Unmarshal([]byte(payload), &node); err != nil {
		return fmt.Errorf("protocol body must contain valid YAML: %w", err)
	}
	if len(node.Content) != 1 || node.Content[0].Kind != yaml.MappingNode {
		return fmt.Errorf("protocol body must be a YAML mapping")
	}
	seen := map[string]bool{}
	mapping := node.Content[0]
	for i := 0; i < len(mapping.Content); i += 2 {
		key := mapping.Content[i].Value
		if seen[key] {
			return fmt.Errorf("protocol body contains duplicate key %q", key)
		}
		seen[key] = true
	}
	return nil
}

func roleName(st state) string {
	if st.Mode == "gateway" {
		return roleGateway
	}
	return roleMain
}

func peerRoleName(st state) string {
	if roleName(st) == roleGateway {
		return roleMain
	}
	return roleGateway
}

func bodyScalar(body, key string) string {
	prefix := key + ":"
	text := strings.TrimSpace(body)
	if strings.HasPrefix(text, "```yaml\n") && strings.HasSuffix(text, "\n```") {
		text = strings.TrimSuffix(strings.TrimPrefix(text, "```yaml\n"), "\n```")
	}
	for _, line := range strings.Split(text, "\n") {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "```") || strings.HasPrefix(line, "#") {
			continue
		}
		if value, ok := strings.CutPrefix(line, prefix); ok {
			return strings.Trim(strings.TrimSpace(value), `"'`)
		}
	}
	return ""
}
