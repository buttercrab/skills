package frontagent

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"regexp"
	"sort"
	"strconv"
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

func validateWorkAuthorityRoot(body, root string) error {
	method := bodyScalar(body, "method")
	if method != "work" && method != "update" {
		return nil
	}
	authority, err := parseWorkAuthority(body)
	if err != nil {
		return err
	}
	canonical, err := projectRoot(root)
	if err != nil {
		return err
	}
	if authority.RepositoryRoot != canonical {
		return fmt.Errorf("work authority repository_root %q does not match canonical root %q", authority.RepositoryRoot, canonical)
	}
	return nil
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
	if err := validateClosedMethodBody(body, method, fromRole); err != nil {
		return err
	}
	switch method {
	case "work":
		original := bodyScalar(body, "original_request")
		if strings.TrimSpace(original) == "" {
			return fmt.Errorf("work requires a non-empty original_request")
		}
		authority, err := parseWorkAuthority(body)
		if err != nil {
			return err
		}
		if authority.Sequence != 0 {
			return fmt.Errorf("work authority sequence must be 0")
		}
		sum := sha256.Sum256([]byte(original))
		if authority.OriginalRequestSHA256 != hex.EncodeToString(sum[:]) {
			return fmt.Errorf("work authority original_request_sha256 does not match original_request")
		}
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
		authority, err := parseWorkAuthority(body)
		if err != nil {
			return err
		}
		if authority.Sequence < 1 {
			return fmt.Errorf("update work authority sequence must be at least 1")
		}
	}
	return nil
}

var (
	uuidPattern = regexp.MustCompile(`^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`)
	hashPattern = regexp.MustCompile(`^[0-9a-f]{64}$`)
	taskPattern = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,63}$`)
)

type packetAuthority struct {
	PacketSchemaVersion int      `json:"packet_schema_version,omitempty"`
	PacketID            string   `json:"packet_id"`
	TaskID              string   `json:"task_id"`
	PacketPath          string   `json:"packet_path"`
	PacketRevision      int      `json:"packet_revision"`
	ProtectedDigest     string   `json:"protected_digest"`
	ApprovalID          string   `json:"approval_id"`
	AuthorityClasses    []string `json:"authority_classes,omitempty"`
	CoordinatorID       string   `json:"coordinator_id"`
	CoordinatorEpoch    int      `json:"coordinator_epoch"`
	StateGeneration     int      `json:"state_generation"`
	LifecycleStatus     string   `json:"lifecycle_status"`
	ExecutionHead       *string  `json:"execution_head"`
}

type workAuthority struct {
	SchemaVersion         string           `json:"schema_version"`
	WorkID                string           `json:"work_id"`
	Sequence              int              `json:"sequence"`
	OriginalRequestSHA256 string           `json:"original_request_sha256"`
	AlignmentMode         string           `json:"alignment_mode"`
	GatewayClassification string           `json:"gateway_classification"`
	RepositoryRoot        string           `json:"repository_root"`
	PacketBinding         *packetAuthority `json:"packet_binding"`
}

func validateClosedMethodBody(body, method, fromRole string) error {
	mapping, err := protocolMapping(body)
	if err != nil {
		return err
	}
	required := map[string]bool{"method": true, "from_role": true, "to_role": true, "summary": true}
	allowed := map[string]bool{}
	for key := range required {
		allowed[key] = true
	}
	if fromRole == roleGateway {
		required["human_confirmed"] = true
		allowed["human_confirmed"] = true
	}
	switch method {
	case "work":
		for _, key := range []string{"original_request", "work_authority"} {
			required[key] = true
			allowed[key] = true
		}
		for _, key := range []string{"requirements", "constraints", "acceptance_criteria"} {
			allowed[key] = true
		}
	case "update":
		for _, key := range []string{"status", "work_authority"} {
			required[key] = true
			allowed[key] = true
		}
		for _, key := range []string{"result", "tests", "blocker"} {
			allowed[key] = true
		}
	case "question":
		required["question"] = true
		allowed["question"] = true
	case "answer":
		required["answer"] = true
		allowed["answer"] = true
	case "note":
		allowed["context"] = true
	}
	seen := map[string]bool{}
	for i := 0; i < len(mapping.Content); i += 2 {
		key := mapping.Content[i].Value
		seen[key] = true
		if !allowed[key] {
			return fmt.Errorf("%s contains unknown field %q", method, key)
		}
	}
	for key := range required {
		if !seen[key] {
			return fmt.Errorf("%s requires field %q", method, key)
		}
	}
	for _, key := range []string{"requirements", "constraints", "acceptance_criteria", "tests"} {
		if node := mappingNodeValue(mapping, key); node != nil {
			if err := validateStringSequence(node, key); err != nil {
				return err
			}
		}
	}
	return nil
}

func mappingNodeValue(mapping *yaml.Node, key string) *yaml.Node {
	for i := 0; i < len(mapping.Content); i += 2 {
		if mapping.Content[i].Kind == yaml.ScalarNode && mapping.Content[i].Value == key {
			return mapping.Content[i+1]
		}
	}
	return nil
}

func validateStringSequence(node *yaml.Node, field string) error {
	if node.Kind != yaml.SequenceNode || len(node.Content) == 0 {
		return fmt.Errorf("%s must be a non-empty sequence", field)
	}
	for _, item := range node.Content {
		if item.Kind != yaml.ScalarNode || item.Tag != "!!str" || strings.TrimSpace(item.Value) == "" {
			return fmt.Errorf("%s items must be non-empty strings", field)
		}
	}
	return nil
}

func scalarString(node *yaml.Node, field string) (string, error) {
	if node == nil || node.Kind != yaml.ScalarNode || node.Tag != "!!str" || strings.TrimSpace(node.Value) == "" {
		return "", fmt.Errorf("work authority %s must be a non-empty string", field)
	}
	return node.Value, nil
}

func scalarInt(node *yaml.Node, field string) (int, error) {
	if node == nil || node.Kind != yaml.ScalarNode || node.Tag != "!!int" {
		return 0, fmt.Errorf("work authority %s must be an integer", field)
	}
	value, err := strconv.Atoi(node.Value)
	if err != nil {
		return 0, fmt.Errorf("work authority %s must be an integer", field)
	}
	return value, nil
}

func exactMapping(node *yaml.Node, fields []string, label string) error {
	if node == nil || node.Kind != yaml.MappingNode {
		return fmt.Errorf("%s must be a mapping", label)
	}
	expected := map[string]bool{}
	for _, field := range fields {
		expected[field] = true
	}
	seen := map[string]bool{}
	for i := 0; i < len(node.Content); i += 2 {
		key := node.Content[i]
		if key.Kind != yaml.ScalarNode || key.Tag != "!!str" || seen[key.Value] || !expected[key.Value] {
			return fmt.Errorf("%s has duplicate or unknown field %q", label, key.Value)
		}
		seen[key.Value] = true
	}
	if len(seen) != len(expected) {
		missing := []string{}
		for field := range expected {
			if !seen[field] {
				missing = append(missing, field)
			}
		}
		sort.Strings(missing)
		return fmt.Errorf("%s is missing fields %v", label, missing)
	}
	return nil
}

func parseWorkAuthority(body string) (workAuthority, error) {
	mapping, err := protocolMapping(body)
	if err != nil {
		return workAuthority{}, err
	}
	node := mappingNodeValue(mapping, "work_authority")
	fields := []string{"schema_version", "work_id", "sequence", "original_request_sha256", "alignment_mode", "gateway_classification", "repository_root", "packet_binding"}
	if err := exactMapping(node, fields, "work_authority"); err != nil {
		return workAuthority{}, err
	}
	get := func(key string) *yaml.Node { return mappingNodeValue(node, key) }
	result := workAuthority{}
	if result.SchemaVersion, err = scalarString(get("schema_version"), "schema_version"); err != nil || (result.SchemaVersion != "work_authority/v1" && result.SchemaVersion != "work_authority/v2") {
		return workAuthority{}, fmt.Errorf("work authority schema_version must be work_authority/v1 or work_authority/v2")
	}
	if result.WorkID, err = scalarString(get("work_id"), "work_id"); err != nil || !uuidPattern.MatchString(result.WorkID) {
		return workAuthority{}, fmt.Errorf("work authority work_id must be a lowercase UUID")
	}
	if result.Sequence, err = scalarInt(get("sequence"), "sequence"); err != nil || result.Sequence < 0 {
		return workAuthority{}, fmt.Errorf("work authority sequence must be non-negative")
	}
	if result.OriginalRequestSHA256, err = scalarString(get("original_request_sha256"), "original_request_sha256"); err != nil || !hashPattern.MatchString(result.OriginalRequestSHA256) {
		return workAuthority{}, fmt.Errorf("work authority original_request_sha256 must be SHA-256")
	}
	if result.AlignmentMode, err = scalarString(get("alignment_mode"), "alignment_mode"); err != nil || (result.AlignmentMode != "packet" && result.AlignmentMode != "none") {
		return workAuthority{}, fmt.Errorf("work authority alignment_mode must be packet or none")
	}
	if result.GatewayClassification, err = scalarString(get("gateway_classification"), "gateway_classification"); err != nil {
		return workAuthority{}, err
	}
	classifications := map[string]bool{"explicit-invocation": true, "existing-packet": true, "material-decision": true, "destructive": true, "production": true, "security-privacy": true, "costly": true, "external-mutation": true, "none": true}
	if !classifications[result.GatewayClassification] {
		return workAuthority{}, fmt.Errorf("work authority gateway_classification is invalid")
	}
	if result.RepositoryRoot, err = scalarString(get("repository_root"), "repository_root"); err != nil || !strings.HasPrefix(result.RepositoryRoot, "/") {
		return workAuthority{}, fmt.Errorf("work authority repository_root must be absolute")
	}
	packetNode := get("packet_binding")
	if result.AlignmentMode == "none" {
		if packetNode == nil || packetNode.Kind != yaml.ScalarNode || packetNode.Tag != "!!null" || result.GatewayClassification != "none" {
			return workAuthority{}, fmt.Errorf("none alignment requires packet_binding: null and gateway_classification: none")
		}
		return result, nil
	}
	if result.GatewayClassification == "none" {
		return workAuthority{}, fmt.Errorf("packet alignment requires a trigger classification")
	}
	packet, err := parsePacketAuthority(packetNode, result.SchemaVersion)
	if err != nil {
		return workAuthority{}, err
	}
	result.PacketBinding = &packet
	return result, nil
}

func parsePacketAuthority(node *yaml.Node, workSchema string) (packetAuthority, error) {
	fields := []string{"packet_id", "task_id", "packet_path", "packet_revision", "protected_digest", "approval_id", "coordinator_id", "coordinator_epoch", "state_generation", "lifecycle_status", "execution_head"}
	if workSchema == "work_authority/v1" {
		fields = append(fields, "authority_classes")
	} else {
		fields = append(fields, "packet_schema_version")
	}
	if err := exactMapping(node, fields, "packet_binding"); err != nil {
		return packetAuthority{}, err
	}
	get := func(key string) *yaml.Node { return mappingNodeValue(node, key) }
	result := packetAuthority{}
	var err error
	for field, target := range map[string]*string{"packet_id": &result.PacketID, "task_id": &result.TaskID, "packet_path": &result.PacketPath, "protected_digest": &result.ProtectedDigest, "approval_id": &result.ApprovalID, "coordinator_id": &result.CoordinatorID, "lifecycle_status": &result.LifecycleStatus} {
		*target, err = scalarString(get(field), field)
		if err != nil {
			return packetAuthority{}, err
		}
	}
	if !uuidPattern.MatchString(result.PacketID) || !uuidPattern.MatchString(result.ApprovalID) || !uuidPattern.MatchString(result.CoordinatorID) || !taskPattern.MatchString(result.TaskID) || result.PacketPath != ".planning/"+result.TaskID || !hashPattern.MatchString(result.ProtectedDigest) {
		return packetAuthority{}, fmt.Errorf("packet_binding identity or path is invalid")
	}
	for field, target := range map[string]*int{"packet_revision": &result.PacketRevision, "coordinator_epoch": &result.CoordinatorEpoch, "state_generation": &result.StateGeneration} {
		*target, err = scalarInt(get(field), field)
		if err != nil {
			return packetAuthority{}, err
		}
	}
	if result.PacketRevision < 1 || result.CoordinatorEpoch < 1 || result.StateGeneration < 0 {
		return packetAuthority{}, fmt.Errorf("packet_binding counters are invalid")
	}
	if workSchema == "work_authority/v1" {
		classes := get("authority_classes")
		if classes == nil || classes.Kind != yaml.SequenceNode || len(classes.Content) == 0 || len(classes.Content) > 3 {
			return packetAuthority{}, fmt.Errorf("packet_binding authority_classes is invalid")
		}
		seen := map[string]bool{}
		for _, item := range classes.Content {
			if item.Kind != yaml.ScalarNode || item.Tag != "!!str" || !map[string]bool{"P": true, "R": true, "T": true}[item.Value] || seen[item.Value] {
				return packetAuthority{}, fmt.Errorf("packet_binding authority_classes is invalid")
			}
			seen[item.Value] = true
			result.AuthorityClasses = append(result.AuthorityClasses, item.Value)
		}
		if !sort.StringsAreSorted(result.AuthorityClasses) {
			return packetAuthority{}, fmt.Errorf("packet_binding authority_classes must be sorted")
		}
	} else {
		result.PacketSchemaVersion, err = scalarInt(get("packet_schema_version"), "packet_schema_version")
		if err != nil || result.PacketSchemaVersion != 2 {
			return packetAuthority{}, fmt.Errorf("packet_binding packet_schema_version must be 2")
		}
	}
	statuses := map[string]bool{"approved": true, "executing": true, "verifying": true, "needs_reapproval": true, "blocked": true, "cancelled": true, "complete": true}
	if !statuses[result.LifecycleStatus] {
		return packetAuthority{}, fmt.Errorf("packet_binding lifecycle_status is invalid")
	}
	head := get("execution_head")
	if head == nil {
		return packetAuthority{}, fmt.Errorf("packet_binding execution_head is required")
	}
	if head.Kind == yaml.ScalarNode && head.Tag == "!!null" {
		result.ExecutionHead = nil
	} else {
		value, err := scalarString(head, "execution_head")
		if err != nil || !hashPattern.MatchString(value) {
			return packetAuthority{}, fmt.Errorf("packet_binding execution_head must be null or SHA-256")
		}
		result.ExecutionHead = &value
	}
	return result, nil
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
