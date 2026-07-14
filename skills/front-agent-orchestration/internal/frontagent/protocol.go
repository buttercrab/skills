package frontagent

import (
	"fmt"
	"io"
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
	switch method {
	case "question":
		if strings.TrimSpace(bodyScalar(body, "question")) == "" {
			return fmt.Errorf("question requires a non-empty question field")
		}
	case "answer":
		if strings.TrimSpace(bodyScalar(body, "answer")) == "" {
			return fmt.Errorf("answer requires a non-empty answer field")
		}
	case "update":
		status := bodyScalar(body, "status")
		if !allowedUpdateStatus(status) {
			return fmt.Errorf("update status %q is invalid; use accepted, progress, blocked, complete, failed, or cancelled", status)
		}
	}
	return nil
}

func allowedUpdateStatus(status string) bool {
	switch status {
	case "accepted", "progress", "blocked", "complete", "failed", "cancelled":
		return true
	default:
		return false
	}
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
	mapping, err := protocolMapping(body)
	if err != nil {
		return err
	}
	seen := map[string]bool{}
	for i := 0; i < len(mapping.Content); i += 2 {
		keyNode := mapping.Content[i]
		if keyNode.Kind != yaml.ScalarNode || keyNode.Tag != "!!str" {
			return fmt.Errorf("protocol body keys must be strings")
		}
		key := keyNode.Value
		if seen[key] {
			return fmt.Errorf("protocol body contains duplicate key %q", key)
		}
		seen[key] = true
	}
	return nil
}

func protocolMapping(body string) (*yaml.Node, error) {
	text := strings.TrimSpace(body)
	if !strings.HasPrefix(text, "```yaml\n") {
		return nil, fmt.Errorf("protocol body must be fenced YAML starting with ```yaml")
	}
	if !strings.HasSuffix(text, "\n```") {
		return nil, fmt.Errorf("protocol body must end with closing YAML fence")
	}
	payload := strings.TrimSuffix(strings.TrimPrefix(text, "```yaml\n"), "\n```")
	if strings.Contains(payload, "```") {
		return nil, fmt.Errorf("protocol body must not contain nested fences")
	}
	decoder := yaml.NewDecoder(strings.NewReader(payload))
	var node yaml.Node
	if err := decoder.Decode(&node); err != nil {
		return nil, fmt.Errorf("protocol body must contain valid YAML: %w", err)
	}
	var extra yaml.Node
	if err := decoder.Decode(&extra); err != io.EOF {
		if err == nil {
			return nil, fmt.Errorf("protocol body must contain exactly one YAML document")
		}
		return nil, fmt.Errorf("protocol body must contain valid YAML: %w", err)
	}
	if len(node.Content) != 1 || node.Content[0].Kind != yaml.MappingNode {
		return nil, fmt.Errorf("protocol body must be a YAML mapping")
	}
	return node.Content[0], nil
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
	mapping, err := protocolMapping(body)
	if err != nil {
		return ""
	}
	for i := 0; i < len(mapping.Content); i += 2 {
		keyNode := mapping.Content[i]
		valueNode := mapping.Content[i+1]
		if keyNode.Kind == yaml.ScalarNode && keyNode.Tag == "!!str" && keyNode.Value == key && valueNode.Kind == yaml.ScalarNode {
			return valueNode.Value
		}
	}
	return ""
}
