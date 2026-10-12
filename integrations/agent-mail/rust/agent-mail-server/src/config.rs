use clap::Parser;
use std::net::SocketAddr;

#[derive(Debug, Clone, Parser)]
pub struct Config {
    #[arg(long, env = "AGENT_MAIL_DATABASE_URL")]
    pub database_url: String,

    #[arg(long, env = "AGENT_MAIL_BIND", default_value = "127.0.0.1:8787")]
    pub bind: SocketAddr,

    #[arg(long, env = "AGENT_MAIL_TOKEN")]
    pub token: String,

    #[arg(long, env = "AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN")]
    pub credential_admin_token: Option<String>,
}

impl Config {
    pub fn from_env() -> Self {
        Self::parse()
    }

    pub fn validate(&self) -> anyhow::Result<()> {
        anyhow::ensure!(
            !self.token.trim().is_empty(),
            "AGENT_MAIL_TOKEN must not be empty"
        );
        anyhow::ensure!(
            self.token == self.token.trim(),
            "AGENT_MAIL_TOKEN must not have leading or trailing whitespace"
        );
        if let Some(token) = &self.credential_admin_token {
            anyhow::ensure!(
                !token.trim().is_empty(),
                "AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN must not be empty when configured"
            );
            anyhow::ensure!(
                token == token.trim(),
                "AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN must not have leading or trailing whitespace"
            );
            anyhow::ensure!(
                token.trim() != self.token.trim(),
                "AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN must differ from AGENT_MAIL_TOKEN"
            );
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::Config;
    use clap::Parser;

    #[test]
    fn rejects_empty_token() {
        let config = Config::try_parse_from([
            "agent-mail-server",
            "--database-url",
            "postgres://localhost/test",
            "--token",
            "",
        ])
        .unwrap();
        assert!(config.validate().is_err());
    }

    #[test]
    fn rejects_equal_service_and_credential_admin_tokens() {
        let config = Config::try_parse_from([
            "agent-mail-server",
            "--database-url",
            "postgres://localhost/test",
            "--token",
            "same-secret",
            "--credential-admin-token",
            "same-secret",
        ])
        .unwrap();
        let error = config.validate().unwrap_err().to_string();
        assert!(error.contains("must differ"));
    }
}
