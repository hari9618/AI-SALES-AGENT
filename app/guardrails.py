"""
guardrails.py — Content safety layer.
FIXED: Removed minimum length check — short inputs like "hi" now pass through.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)

# ── Blocked patterns (only truly harmful content) ─────────────
_BLOCKED_INPUT_PATTERNS: List[str] = [
    r"\b(ignore previous instructions|forget your instructions|jailbreak|dan mode)\b",
    r"\b(bomb|explosive|weapon|poison|drug trafficking|child abuse)\b",
    r"\b(hack|exploit|sql injection|xss attack|ddos)\b",
    r"(system prompt|override safety|bypass filter)",
]
_BLOCKED_INPUT_RE = re.compile("|".join(_BLOCKED_INPUT_PATTERNS), re.IGNORECASE)

_BLOCKED_OUTPUT_PATTERNS: List[str] = [
    r"(my api key|secret key|password is|token =)",
]
_BLOCKED_OUTPUT_RE = re.compile("|".join(_BLOCKED_OUTPUT_PATTERNS), re.IGNORECASE)

MAX_INPUT_LENGTH = 2000
MAX_OUTPUT_LENGTH = 3000

SAFE_FALLBACK_RESPONSE = (
    "Thank you for reaching out to us! "
    "I'm here to help. Could you please provide more details about your inquiry "
    "so I can assist you better? Feel free to ask about our products, pricing, "
    "demos, or any support needs."
)


@dataclass
class GuardResult:
    passed: bool
    sanitised_text: str
    violations: List[str] = field(default_factory=list)


def validate_input(user_input: str) -> GuardResult:
    """
    Screen input for harmful content.
    NOTE: Short inputs like 'hi' are ALLOWED — the AI handles them gracefully.
    """
    violations: List[str] = []

    # Strip and handle empty
    user_input = user_input.strip()
    if not user_input:
        return GuardResult(
            passed=False,
            sanitised_text=user_input,
            violations=["Empty input."]
        )

    # Length truncation (not a block — just trim)
    if len(user_input) > MAX_INPUT_LENGTH:
        user_input = user_input[:MAX_INPUT_LENGTH]

    # Harmful pattern check
    if _BLOCKED_INPUT_RE.search(user_input):
        violations.append("Input contains potentially harmful content.")
        logger.warning("Blocked input pattern detected.")
        return GuardResult(passed=False, sanitised_text=user_input, violations=violations)

    return GuardResult(passed=True, sanitised_text=user_input, violations=violations)


def validate_output(ai_response: str) -> GuardResult:
    violations: List[str] = []
    if len(ai_response) > MAX_OUTPUT_LENGTH:
        ai_response = ai_response[:MAX_OUTPUT_LENGTH] + "…"
    if _BLOCKED_OUTPUT_RE.search(ai_response):
        violations.append("Response contained restricted information.")
        return GuardResult(passed=False, sanitised_text=SAFE_FALLBACK_RESPONSE, violations=violations)
    return GuardResult(passed=True, sanitised_text=ai_response, violations=violations)


def get_safe_fallback() -> str:
    return SAFE_FALLBACK_RESPONSE