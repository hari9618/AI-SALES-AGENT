"""
utils.py — Shared utilities: Langfuse tracing, logging, n8n webhook, helpers.
"""

import logging
import os
import uuid
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

import httpx
from dotenv import load_dotenv

# Force load .env at import time
load_dotenv(override=True)

logger = logging.getLogger(__name__)


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _get_langfuse_keys():
    """Read Langfuse keys — supports both LANGFUSE_HOST and LANGFUSE_BASE_URL."""
    pub = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip().strip('"')
    sec = os.getenv("LANGFUSE_SECRET_KEY", "").strip().strip('"')
    # Support both variable names
    host = (
        os.getenv("LANGFUSE_HOST", "")
        or os.getenv("LANGFUSE_BASE_URL", "https://us.cloud.langfuse.com")
    ).strip().strip('"')
    return pub, sec, host


def get_langfuse_client():
    """Return a configured Langfuse client, or None."""
    pub, sec, host = _get_langfuse_keys()

    if not pub or not sec:
        logger.debug("Langfuse credentials not set — observability disabled.")
        return None

    try:
        from langfuse import Langfuse
        client = Langfuse(public_key=pub, secret_key=sec, host=host)
        logger.info("Langfuse client initialised at %s", host)
        return client
    except Exception as exc:
        logger.warning("Langfuse init failed: %s", exc)
        return None


@contextmanager
def langfuse_trace(
    name: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Generator[Any, None, None]:
    client = get_langfuse_client()
    trace = None
    try:
        if client:
            trace = client.trace(name=name, metadata=metadata or {})
        yield trace
    except Exception as exc:
        logger.warning("Langfuse trace error: %s", exc)
        yield None
    finally:
        if client:
            try:
                client.flush()
            except Exception:
                pass


def get_langfuse_callback():
    """Return a LangChain-compatible Langfuse CallbackHandler, or None."""
    pub, sec, host = _get_langfuse_keys()

    if not pub or not sec:
        logger.debug("Langfuse keys missing — callback disabled.")
        return None

    try:
        from langfuse.callback import CallbackHandler
        handler = CallbackHandler(public_key=pub, secret_key=sec, host=host)
        logger.info("Langfuse callback handler ready.")
        return handler
    except Exception as exc:
        logger.warning("Langfuse callback unavailable: %s", exc)
        return None


async def notify_n8n(payload: Dict[str, Any]) -> bool:
    webhook_url = os.getenv("N8N_WEBHOOK_URL", "").strip().strip('"')
    if not webhook_url:
        logger.debug("N8N_WEBHOOK_URL not set — skipping.")
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info("n8n webhook notified successfully.")
            return True
    except Exception as exc:
        logger.warning("n8n webhook failed: %s", exc)
        return False


def generate_session_id() -> str:
    return uuid.uuid4().hex


def truncate(text: str, max_len: int = 200) -> str:
    return text if len(text) <= max_len else text[:max_len] + "…"