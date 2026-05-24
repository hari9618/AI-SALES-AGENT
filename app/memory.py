"""
memory.py — Session-based chat history using LangChain's latest recommended approach.
Uses InMemoryChatMessageHistory with RunnableWithMessageHistory for LCEL integration.
"""

import logging
from typing import Dict

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import Runnable

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# In-process session store (swap for Redis in production)
# ──────────────────────────────────────────────────────────────
_SESSION_STORE: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieve (or create) a chat history object for the given session.
    Uses InMemoryChatMessageHistory — replace with RedisChatMessageHistory
    for multi-replica / persistent deployments.
    """
    if session_id not in _SESSION_STORE:
        _SESSION_STORE[session_id] = InMemoryChatMessageHistory()
        logger.debug("New session created: %s", session_id)
    return _SESSION_STORE[session_id]


def clear_session(session_id: str) -> None:
    """Wipe all messages for a session (i.e. 'New Chat')."""
    if session_id in _SESSION_STORE:
        del _SESSION_STORE[session_id]
        logger.info("Session cleared: %s", session_id)


def list_session_ids() -> list[str]:
    """Return all active session IDs."""
    return list(_SESSION_STORE.keys())


def wrap_with_history(chain: Runnable, session_id_key: str = "session_id") -> Runnable:
    """
    Wrap an LCEL chain with RunnableWithMessageHistory so that every
    invocation automatically loads/saves chat history.

    The chain's input dict must contain the key specified by session_id_key.
    chat_history is injected automatically; user_input carries the human turn.
    """
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="user_input",
        history_messages_key="chat_history",
        output_messages_key="output",
    )
