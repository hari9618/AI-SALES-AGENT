"""
main.py — FastAPI application entry-point.
Provides async REST endpoints for lead analysis, session management,
and an n8n webhook bridge. Full Swagger/OpenAPI support included.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.chains import analyse_lead
from app.guardrails import validate_input
from app.memory import clear_session, list_session_ids
from app.parser import LeadAnalysisOutput
from app.utils import configure_logging, generate_session_id, notify_n8n

# ──────────────────────────────────────────────────────────────
load_dotenv()
configure_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# Lifespan handler (startup / shutdown)
# ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Sales AI System starting up…")
    yield
    logger.info("Sales AI System shut down.")


# ──────────────────────────────────────────────────────────────
# App factory
# ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Sales Automation & Lead Intelligence API",
    description=(
        "Production-grade AI system for automated lead classification, "
        "priority detection, and intelligent response generation. "
        "Powered by Google Gemini 2.5 Flash + LangChain LCEL."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS, templates)
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")


# ──────────────────────────────────────────────────────────────
# Request / Response schemas
# ──────────────────────────────────────────────────────────────
class LeadRequest(BaseModel):
    user_input: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="The customer's message or business query.",
        examples=["We need an enterprise plan for 500 users with API access."],
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversational memory. Auto-generated if omitted.",
    )


class LeadResponse(BaseModel):
    session_id: str
    result: LeadAnalysisOutput
    n8n_notified: bool = False


class SessionListResponse(BaseModel):
    sessions: List[str]
    count: int


class HealthResponse(BaseModel):
    status: str
    version: str


# ──────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Liveness probe — returns 200 when the service is ready."""
    return {"status": "healthy", "version": "1.0.0"}


@app.post(
    "/api/v1/leads/analyse",
    response_model=LeadResponse,
    status_code=status.HTTP_200_OK,
    tags=["Leads"],
    summary="Analyse a customer lead",
    description=(
        "Submit a customer message for full AI-powered lead analysis: "
        "classification, priority detection, sentiment analysis, response generation, "
        "and follow-up recommendations."
    ),
)
async def analyse_lead_endpoint(payload: LeadRequest):
    # Generate session ID if not provided
    session_id = payload.session_id or generate_session_id()

    # Input guard
    guard = validate_input(payload.user_input)
    if not guard.passed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Input rejected by safety guard: {'; '.join(guard.violations)}",
        )

    try:
        result = await analyse_lead(
            user_input=guard.sanitised_text,
            session_id=session_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        logger.error("Chain error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal AI processing error.")

    # Fire-and-forget n8n notification for high-priority leads
    n8n_sent = False
    if result.priority.value in ("critical", "high") or result.escalate:
        n8n_sent = await notify_n8n(
            {
                "session_id": session_id,
                "category": result.category.value,
                "priority": result.priority.value,
                "sentiment": result.sentiment.value,
                "escalate": result.escalate,
                "user_input": payload.user_input[:300],
                "ai_response": result.ai_response[:300],
                "follow_up": result.follow_up,
            }
        )

    return LeadResponse(session_id=session_id, result=result, n8n_notified=n8n_sent)


@app.get(
    "/api/v1/sessions",
    response_model=SessionListResponse,
    tags=["Sessions"],
    summary="List all active sessions",
)
async def list_sessions():
    ids = list_session_ids()
    return {"sessions": ids, "count": len(ids)}


@app.delete(
    "/api/v1/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Sessions"],
    summary="Clear a session's chat history",
)
async def delete_session(session_id: str):
    clear_session(session_id)


@app.post(
    "/api/v1/webhook/n8n",
    tags=["Webhooks"],
    summary="n8n inbound webhook (triggers lead analysis)",
    description="n8n calls this endpoint to inject a lead payload into the AI pipeline.",
)
async def n8n_webhook(request: Request):
    body = await request.json()
    user_input = body.get("message") or body.get("user_input", "")
    session_id = body.get("session_id") or generate_session_id()

    if not user_input:
        raise HTTPException(status_code=400, detail="'message' field is required.")

    guard = validate_input(user_input)
    if not guard.passed:
        return JSONResponse(
            status_code=422,
            content={"error": "Input blocked", "violations": guard.violations},
        )

    try:
        result = await analyse_lead(
            user_input=guard.sanitised_text,
            session_id=session_id,
        )
        return {
            "session_id": session_id,
            "category": result.category.value,
            "priority": result.priority.value,
            "sentiment": result.sentiment.value,
            "ai_response": result.ai_response,
            "follow_up": result.follow_up,
            "escalate": result.escalate,
        }
    except Exception as exc:
        logger.error("Webhook processing error: %s", exc)
        return JSONResponse(status_code=500, content={"error": str(exc)})
