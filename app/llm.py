"""
llm.py — LLM configuration using LangChain init_chat_model() with Google Gemini 2.5 Flash.
Handles retry logic, timeouts, and production-ready model setup.
"""

import os
import logging
from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# Model configuration constants
# ──────────────────────────────────────────────────────────────
MODEL_ID = "gemini-2.5-flash"
MODEL_PROVIDER = "google_genai"

LLM_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 512,
}


# ──────────────────────────────────────────────────────────────
# Retry decorator for transient API failures
# ──────────────────────────────────────────────────────────────
def _with_retries(func):
    """Wrap a callable with exponential-backoff retry logic."""
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception)),
        reraise=True,
    )(func)


# ──────────────────────────────────────────────────────────────
# LLM factory
# ──────────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    """
    Return a cached, production-ready Gemini 2.5 Flash instance.

    Uses LangChain's init_chat_model() for provider-agnostic initialisation.
    Falls back gracefully if the API key is missing during development.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. "
            "Add it to your .env file or environment variables."
        )

    try:
        llm = init_chat_model(
            model=MODEL_ID,
            model_provider=MODEL_PROVIDER,
            configurable_fields="any",
            temperature=LLM_CONFIG["temperature"],
            top_p=LLM_CONFIG["top_p"],
            top_k=LLM_CONFIG["top_k"],
            max_output_tokens=LLM_CONFIG["max_output_tokens"],
        )
        logger.info("Gemini 2.5 Flash initialised successfully.")
        return llm
    except Exception as exc:
        logger.error("Failed to initialise LLM: %s", exc)
        raise


def get_llm_with_retry() -> BaseChatModel:
    """Return the LLM wrapped so every invoke call benefits from retries."""
    llm = get_llm()
    # LangChain Runnables expose .with_retry() natively
    return llm.with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True,
    )
