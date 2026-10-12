use crate::domain::BROADCAST_RECIPIENT;
use crate::error::{AppError, Result};

pub const MAX_ALIAS_BYTES: usize = 128;
pub const MAX_ADDRESS_BYTES: usize = 128;
pub const MAX_ROOT_BYTES: usize = 1024;
pub const MAX_SUBJECT_BYTES: usize = 512;
pub const MAX_BODY_BYTES: usize = 256 * 1024;
pub const MAX_IDEMPOTENCY_KEY_BYTES: usize = 128;

pub fn alias(value: &str) -> Result<()> {
    let trimmed = value.trim();
    if trimmed.is_empty()
        || !trimmed
            .chars()
            .all(|ch| ch.is_ascii_alphanumeric() || matches!(ch, '.' | '_' | '-'))
    {
        return Err(AppError::BadRequest(
            "project alias may contain only letters, numbers, dot, underscore, and dash".into(),
        ));
    }
    max_bytes(trimmed, "project alias", MAX_ALIAS_BYTES)?;
    Ok(())
}

pub fn identity(value: &str) -> Result<()> {
    address_path(value, "identity")
}

pub fn role(value: &str) -> Result<()> {
    if value.trim() == BROADCAST_RECIPIENT {
        return Err(AppError::BadRequest(
            "all-agents is a reserved broadcast address, not a role".into(),
        ));
    }
    address_path(value, "role")
}

pub fn recipient(value: &str) -> Result<()> {
    address_path(value, "recipient")
}

fn address_path(value: &str, field: &str) -> Result<()> {
    let trimmed = value.trim();
    if trimmed.is_empty() {
        return Err(AppError::BadRequest(format!("{field} is required")));
    }
    if !trimmed
        .chars()
        .all(|ch| ch.is_ascii_alphanumeric() || matches!(ch, '.' | '_' | '-' | '/'))
    {
        return Err(AppError::BadRequest(format!(
            "{field} may contain only letters, numbers, dot, dash, underscore, and slash"
        )));
    }
    if trimmed.contains("//") || trimmed.starts_with('/') || trimmed.ends_with('/') {
        return Err(AppError::BadRequest(format!(
            "{field} may not contain empty slash-separated segments"
        )));
    }
    max_bytes(trimmed, field, MAX_ADDRESS_BYTES)?;
    Ok(())
}

pub fn root(value: &str) -> Result<()> {
    max_bytes(value, "project root", MAX_ROOT_BYTES)
}

pub fn subject(value: &str) -> Result<()> {
    let trimmed = value.trim();
    if trimmed.is_empty() {
        return Err(AppError::BadRequest("subject is required".into()));
    }
    if trimmed.contains('\r') || trimmed.contains('\n') {
        return Err(AppError::BadRequest(
            "subject may not contain carriage returns or newlines".into(),
        ));
    }
    max_bytes(trimmed, "subject", MAX_SUBJECT_BYTES)
}

pub fn body(value: &str) -> Result<()> {
    max_bytes(value, "body", MAX_BODY_BYTES)
}

pub fn idempotency_key(value: &str) -> Result<()> {
    if value.is_empty() {
        return Ok(());
    }
    max_bytes(value, "idempotency key", MAX_IDEMPOTENCY_KEY_BYTES)?;
    if !value
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.' | b':'))
    {
        return Err(AppError::BadRequest(
            "idempotency key may contain only ASCII letters, numbers, dash, underscore, dot, and colon"
                .into(),
        ));
    }
    Ok(())
}

fn max_bytes(value: &str, field: &str, max: usize) -> Result<()> {
    if value.len() > max {
        return Err(AppError::BadRequest(format!(
            "{field} may not exceed {max} UTF-8 bytes"
        )));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn enforces_address_and_payload_limits() {
        assert!(alias(&"a".repeat(MAX_ALIAS_BYTES)).is_ok());
        assert!(alias(&"a".repeat(MAX_ALIAS_BYTES + 1)).is_err());
        assert!(role(&"r".repeat(MAX_ADDRESS_BYTES)).is_ok());
        assert!(role(&"r".repeat(MAX_ADDRESS_BYTES + 1)).is_err());
        assert!(root(&"x".repeat(MAX_ROOT_BYTES)).is_ok());
        assert!(root(&"x".repeat(MAX_ROOT_BYTES + 1)).is_err());
        assert!(subject(&"s".repeat(MAX_SUBJECT_BYTES)).is_ok());
        assert!(subject(&"s".repeat(MAX_SUBJECT_BYTES + 1)).is_err());
        assert!(subject("safe\nfrom: forged").is_err());
        assert!(body(&"b".repeat(MAX_BODY_BYTES)).is_ok());
        assert!(body(&"b".repeat(MAX_BODY_BYTES + 1)).is_err());
        assert!(idempotency_key(&"k".repeat(MAX_IDEMPOTENCY_KEY_BYTES)).is_ok());
        assert!(idempotency_key(&"k".repeat(MAX_IDEMPOTENCY_KEY_BYTES + 1)).is_err());
        assert!(idempotency_key("answer:mail-20260712_ab.c").is_ok());
        assert!(idempotency_key("unsafe/key").is_err());
    }
}
