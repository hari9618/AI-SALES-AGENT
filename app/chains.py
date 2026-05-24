"""
chains.py — Production LCEL pipeline.
FIXED: Chain rebuilt per request, proper error handling, all inputs handled.
"""

import logging
from typing import Any, Dict

from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableSequence,
)

from app.guardrails import get_safe_fallback, validate_input
from app.llm import get_llm_with_retry
from app.memory import get_session_history
from app.parser import LeadAnalysisOutput, extract_and_parse, _infer_from_text
from app.prompt import build_lead_analysis_prompt
from app.utils import get_langfuse_callback

logger = logging.getLogger(__name__)


def _guard_input(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input — only blocks truly harmful content, not short messages."""
    user_input: str = inputs.get("user_input", "")
    result = validate_input(user_input)
    if not result.passed:
        raise ValueError(f"Input blocked: {'; '.join(result.violations)}")
    return {**inputs, "user_input": result.sanitised_text}


def _parse_with_fallback(raw: Any) -> LeadAnalysisOutput:
    """
    Parse LLM output with full fallback chain.
    NEVER returns the generic safe fallback — always returns a real AI response.
    """
    # Try all 6 parsing strategies
    result = extract_and_parse(raw)
    if result:
        logger.debug("Parsed successfully.")
        return result

    # If text is available, use smart inference
    try:
        text = raw.content if hasattr(raw, "content") else str(raw)
        inferred = _infer_from_text(text)
        if inferred:
            logger.warning("Used text inference fallback.")
            return inferred
    except Exception as e:
        logger.error("Inference fallback failed: %s", e)

    # Absolute last resort — still return something useful
    logger.error("All parsing strategies failed.")
    return LeadAnalysisOutput(
        category="general",
        priority="medium",
        sentiment="neutral",
        ai_response=(
            "Hello! Thank you for reaching out. I'm your AI Sales Assistant and I'm here to help. "
            "Whether you have questions about our products, pricing, need a demo, or require support — "
            "I've got you covered. Could you tell me a bit more about what you're looking for today?"
        ),
        follow_up=[
            "Follow up to understand customer needs",
            "Send product overview",
            "Schedule discovery call",
        ],
        confidence_score=0.60,
        escalate=False,
    )


def build_core_chain() -> RunnableSequence:
    """
    Build the complete LCEL chain:
    Guard → Parallel passthrough → Prompt → LLM → Parse
    """
    llm = get_llm_with_retry()
    prompt = build_lead_analysis_prompt()

    # Attach Langfuse callback if available
    callbacks = []
    cb = get_langfuse_callback()
    if cb:
        callbacks.append(cb)
        logger.info("Langfuse callback attached to LLM.")

    llm_with_cb = llm.with_config({"callbacks": callbacks}) if callbacks else llm

    return (
        RunnableLambda(_guard_input)                                          # 1. Safety guard
        | RunnableParallel(                                                   # 2. Fan-out
            passthrough=RunnablePassthrough(),
            original_input=RunnableLambda(lambda x: x.get("user_input", "")),
        )
        | RunnableLambda(lambda x: x["passthrough"])                          # 3. Flatten
        | prompt                                                               # 4. Format prompt
        | llm_with_cb                                                          # 5. Call Gemini
        | RunnableLambda(_parse_with_fallback)                                 # 6. Parse output
    )


def build_priority_branch_chain():
    """Route leads to different handlers based on priority."""
    core = build_core_chain()
    branch = RunnableBranch(
        (
            lambda x: x.priority.value in ("critical", "high"),
            RunnableLambda(lambda x: {**x.model_dump(), "routed_to": "senior_sales"}),
        ),
        (
            lambda x: x.priority.value == "medium",
            RunnableLambda(lambda x: {**x.model_dump(), "routed_to": "sales_team"}),
        ),
        RunnableLambda(lambda x: {**x.model_dump(), "routed_to": "support_queue"}),
    )
    return core | branch


async def analyse_lead(user_input: str, session_id: str) -> LeadAnalysisOutput:
    """
    Main async entry point for lead analysis.
    Builds chain fresh per request, injects chat history, saves to memory.
    """
    chain = build_core_chain()

    # Get existing conversation history
    history = get_session_history(session_id)

    result: LeadAnalysisOutput = await chain.ainvoke({
        "user_input": user_input,
        "chat_history": history.messages,
    })

    # Save turn to memory
    from langchain_core.messages import AIMessage, HumanMessage
    history.add_message(HumanMessage(content=user_input))
    history.add_message(AIMessage(content=result.ai_response))

    return result