use std::sync::Arc;

use axum::{
    Json, Router,
    extract::{Path, Query, State},
    http::{HeaderMap, HeaderValue, StatusCode, header},
    response::IntoResponse,
    routing::{get, post},
};
use serde::Deserialize;
use serde_json::json;

use crate::{
    domain::{AddProject, MarkRead, SendMessage, StartParticipant},
    error::{AppError, Result},
    mcp::McpHub,
    store::Store,
};

#[derive(Clone)]
pub struct AppState {
    pub store: Store,
    pub token: String,
    pub credential_admin_token: Option<String>,
    pub mcp: McpHub,
}

pub fn router(state: AppState) -> Router {
    Router::new()
        .route("/live", get(live))
        .route("/health", get(ready))
        .route("/ready", get(ready))
        .route(
            "/mcp",
            get(crate::mcp::mcp_get)
                .post(crate::mcp::mcp_post)
                .delete(crate::mcp::mcp_delete),
        )
        .route("/v1/participants/start", post(start_participant))
        .route(
            "/v1/participants/{identity}/credential",
            post(issue_participant_credential),
        )
        .route("/v1/participants", get(list_participants))
        .route("/v1/projects", get(list_projects).post(add_project))
        .route("/v1/messages", post(send_message))
        .route(
            "/v1/projects/{project}/participants/{identity}/inbox",
            get(read_inbox),
        )
        .route(
            "/v1/projects/{project}/messages/{mail_id}",
            get(read_message),
        )
        .route(
            "/v1/projects/{project}/messages/{mail_id}/read",
            post(mark_read),
        )
        .with_state(Arc::new(state))
}

async fn live() -> impl IntoResponse {
    (StatusCode::OK, Json(json!({ "ok": true })))
}

async fn ready(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    if state.store.ready().await {
        (StatusCode::OK, Json(json!({ "ok": true })))
    } else {
        (
            StatusCode::SERVICE_UNAVAILABLE,
            Json(json!({ "ok": false, "error": "database unavailable" })),
        )
    }
}

async fn start_participant(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Json(input): Json<StartParticipant>,
) -> Result<impl IntoResponse> {
    authorize(&state, &headers)?;
    let session = state.store.start_http(input).await?;
    let mut response_headers = HeaderMap::new();
    response_headers.insert(header::CACHE_CONTROL, HeaderValue::from_static("no-store"));
    Ok((response_headers, Json(session)))
}

async fn issue_participant_credential(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Path(identity): Path<String>,
) -> Result<impl IntoResponse> {
    authorize_credential_admin(&state, &headers)?;
    let session = state.store.issue_participant_credential(&identity).await?;
    let mut response_headers = HeaderMap::new();
    response_headers.insert(header::CACHE_CONTROL, HeaderValue::from_static("no-store"));
    Ok((response_headers, Json(session)))
}

async fn list_participants(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
) -> Result<impl IntoResponse> {
    authorize(&state, &headers)?;
    Ok(Json(
        json!({ "participants": state.store.participants().await? }),
    ))
}

async fn add_project(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Json(input): Json<AddProject>,
) -> Result<impl IntoResponse> {
    authorize(&state, &headers)?;
    let project = state.store.add_project(&input.alias, &input.root).await?;
    crate::mcp::notify_resource(&state, "agent-mail://projects").await;
    crate::mcp::notify_list_changed(&state).await;
    Ok(Json(project))
}

async fn list_projects(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
) -> Result<impl IntoResponse> {
    authorize(&state, &headers)?;
    Ok(Json(json!({ "projects": state.store.projects().await? })))
}

async fn send_message(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Json(mut input): Json<SendMessage>,
) -> Result<impl IntoResponse> {
    let participant = authorize_participant(&state, &headers).await?;
    if !input.sender_identity.trim().is_empty()
        && input.sender_identity.trim() != participant.identity
    {
        return Err(AppError::Forbidden);
    }
    input.sender_identity = participant.identity;
    let message = state.store.send(input).await?;
    crate::mcp::notify_matching_inboxes(&state, &message.project).await;
    Ok(Json(message))
}

async fn read_inbox(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Path((project, identity)): Path<(String, String)>,
    Query(query): Query<InboxQuery>,
) -> Result<impl IntoResponse> {
    let participant = authorize_participant(&state, &headers).await?;
    require_identity(&participant.identity, &identity)?;
    let limit = query.limit.unwrap_or(DEFAULT_INBOX_LIMIT);
    if !(1..=MAX_INBOX_LIMIT).contains(&limit) {
        return Err(AppError::BadRequest(format!(
            "inbox limit must be between 1 and {MAX_INBOX_LIMIT}"
        )));
    }
    Ok(Json(
        state
            .store
            .inbox_page(&project, &identity, limit, query.cursor.as_deref())
            .await?,
    ))
}

const DEFAULT_INBOX_LIMIT: usize = 100;
const MAX_INBOX_LIMIT: usize = 200;

#[derive(Default, Deserialize)]
struct InboxQuery {
    limit: Option<usize>,
    cursor: Option<String>,
}

#[derive(Deserialize)]
struct MessageQuery {
    identity: String,
}

async fn read_message(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Path((project, mail_id)): Path<(String, String)>,
    Query(query): Query<MessageQuery>,
) -> Result<impl IntoResponse> {
    let participant = authorize_participant(&state, &headers).await?;
    require_identity(&participant.identity, &query.identity)?;
    Ok(Json(
        state
            .store
            .message(&project, &mail_id, &query.identity)
            .await?,
    ))
}

async fn mark_read(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Path((project, mail_id)): Path<(String, String)>,
    Json(input): Json<MarkRead>,
) -> Result<impl IntoResponse> {
    let participant = authorize_participant(&state, &headers).await?;
    require_identity(&participant.identity, &input.identity)?;
    state
        .store
        .mark_read(&project, &mail_id, &input.identity)
        .await?;
    crate::mcp::notify_resource(&state, &crate::mcp::inbox_uri(&project, &input.identity)).await;
    crate::mcp::notify_matching_message_resources(&state, &project, &mail_id).await;
    Ok(Json(json!({ "marked_read": mail_id })))
}

pub(crate) fn authorize(state: &AppState, headers: &HeaderMap) -> Result<()> {
    let Some(value) = headers.get(axum::http::header::AUTHORIZATION) else {
        return Err(AppError::Unauthorized);
    };
    let Ok(text) = value.to_str() else {
        return Err(AppError::Unauthorized);
    };
    if text == format!("Bearer {}", state.token) {
        Ok(())
    } else {
        Err(AppError::Unauthorized)
    }
}

async fn authorize_participant(
    state: &AppState,
    headers: &HeaderMap,
) -> Result<crate::domain::Participant> {
    let token = bearer_token(headers)?;
    state.store.participant_for_token(token).await
}

fn bearer_token(headers: &HeaderMap) -> Result<&str> {
    let value = headers
        .get(axum::http::header::AUTHORIZATION)
        .ok_or(AppError::Unauthorized)?;
    let text = value.to_str().map_err(|_| AppError::Unauthorized)?;
    text.strip_prefix("Bearer ").ok_or(AppError::Unauthorized)
}

fn require_identity(authenticated: &str, requested: &str) -> Result<()> {
    if authenticated == requested {
        Ok(())
    } else {
        Err(AppError::Forbidden)
    }
}

fn authorize_credential_admin(state: &AppState, headers: &HeaderMap) -> Result<()> {
    let Some(expected) = &state.credential_admin_token else {
        return Err(AppError::Forbidden);
    };
    if bearer_token(headers)? == expected {
        Ok(())
    } else {
        Err(AppError::Unauthorized)
    }
}
