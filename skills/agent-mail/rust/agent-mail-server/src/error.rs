use axum::{
    Json,
    http::StatusCode,
    response::{IntoResponse, Response},
};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("{0}")]
    BadRequest(String),
    #[error("{0}")]
    NotFound(String),
    #[error("{0}")]
    Conflict(String),
    #[error("unauthorized")]
    Unauthorized,
    #[error("forbidden")]
    Forbidden,
    #[error(transparent)]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let status = match &self {
            AppError::BadRequest(_) => StatusCode::BAD_REQUEST,
            AppError::NotFound(_) => StatusCode::NOT_FOUND,
            AppError::Conflict(_) => StatusCode::CONFLICT,
            AppError::Unauthorized => StatusCode::UNAUTHORIZED,
            AppError::Forbidden => StatusCode::FORBIDDEN,
            AppError::Database(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        let message = match self {
            AppError::Database(err) => {
                tracing::error!(error = %err, "database request failed");
                "internal server error".to_string()
            }
            err => err.to_string(),
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}

pub type Result<T> = std::result::Result<T, AppError>;
