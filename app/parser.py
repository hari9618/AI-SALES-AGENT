"""
parser.py — Robust Pydantic parser with 6 extraction strategies for Gemini 2.5 Flash.
FIXED: Better JSON extraction, smarter text inference, handles all edge cases.
"""

import json
import re
from enum import Enum
from typing import Any, List, Optional

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class LeadCategory(str, Enum):
    PRODUCT_INQUIRY = "product_inquiry"
    PRICING = "pricing"
    SUPPORT = "support"
    PARTNERSHIP = "partnership"
    DEMO_REQUEST = "demo_request"
    COMPLAINT = "complaint"
    GENERAL = "general"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    URGENT = "urgent"


class LeadAnalysisOutput(BaseModel):
    category: LeadCategory = Field(description="Business category of the inquiry.")
    priority: Priority = Field(description="Handling priority level.")
    sentiment: Sentiment = Field(description="Customer emotional tone.")
    ai_response: str = Field(description="Professional AI response to the customer.")
    follow_up: List[str] = Field(description="2-3 actionable follow-up items for the sales team.")
    confidence_score: Optional[float] = Field(default=0.85, ge=0.0, le=1.0)
    escalate: bool = Field(default=False)


lead_parser = PydanticOutputParser(pydantic_object=LeadAnalysisOutput)


def get_format_instructions() -> str:
    return lead_parser.get_format_instructions()


def _get_text(raw: Any) -> str:
    """Extract string from any LangChain output type."""
    if hasattr(raw, "content"):
        return str(raw.content)
    if isinstance(raw, str):
        return raw
    return str(raw)


def _clean_json_text(text: str) -> str:
    """Remove markdown fences and leading/trailing junk."""
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_json(text: str) -> Optional[LeadAnalysisOutput]:
    """Try to parse text as JSON into LeadAnalysisOutput."""
    try:
        data = json.loads(text)
        return LeadAnalysisOutput(**data)
    except Exception:
        return None


def extract_and_parse(raw: Any) -> Optional[LeadAnalysisOutput]:
    """
    6-strategy robust parser for Gemini output.
    Tries progressively looser strategies until one succeeds.
    """
    text = _get_text(raw)

    # Strategy 1: Direct LangChain parser
    try:
        return lead_parser.invoke(raw)
    except Exception:
        pass

    # Strategy 2: Clean markdown fences then parse
    cleaned = _clean_json_text(text)
    result = _parse_json(cleaned)
    if result:
        return result

    # Strategy 3: Find JSON block in markdown
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        result = _parse_json(match.group(1))
        if result:
            return result

    # Strategy 4: Find first { ... } block containing "category"
    match = re.search(r"\{[^{}]*\"category\"[^{}]*\}", text, re.DOTALL)
    if match:
        result = _parse_json(match.group(0))
        if result:
            return result

    # Strategy 5: Find any outermost { ... } block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        result = _parse_json(match.group(0))
        if result:
            return result

    # Strategy 6: Smart inference from plain text
    return _infer_from_text(text)


def _infer_from_text(text: str) -> Optional[LeadAnalysisOutput]:
    """
    Last resort: intelligently infer all fields from plain text.
    This ensures even if JSON parsing completely fails, we still
    return a useful structured response.
    """
    t = text.lower()

    # ── Category ──
    if any(w in t for w in ["complaint", "dissatisfied", "unhappy", "terrible", "worst", "refund", "charged", "double"]):
        category = LeadCategory.COMPLAINT
    elif any(w in t for w in ["price", "pricing", "cost", "plan", "enterprise", "billing", "invoice", "quote"]):
        category = LeadCategory.PRICING
    elif any(w in t for w in ["demo", "demonstration", "trial", "see the product", "show me"]):
        category = LeadCategory.DEMO_REQUEST
    elif any(w in t for w in ["support", "help", "issue", "problem", "error", "bug", "broken", "not working"]):
        category = LeadCategory.SUPPORT
    elif any(w in t for w in ["partner", "partnership", "reseller", "collaborate", "integrate"]):
        category = LeadCategory.PARTNERSHIP
    elif any(w in t for w in ["product", "feature", "how does", "what is", "api", "integration", "capability"]):
        category = LeadCategory.PRODUCT_INQUIRY
    else:
        category = LeadCategory.GENERAL

    # ── Priority ──
    if any(w in t for w in ["urgent", "critical", "immediately", "emergency", "asap", "down", "outage", "losing money"]):
        priority = Priority.CRITICAL
    elif any(w in t for w in ["enterprise", "500", "1000", "evaluating", "vendor", "important", "high priority"]):
        priority = Priority.HIGH
    elif any(w in t for w in ["low", "minor", "whenever", "no rush"]):
        priority = Priority.LOW
    else:
        priority = Priority.MEDIUM

    # ── Sentiment ──
    if any(w in t for w in ["angry", "frustrated", "terrible", "worst", "unacceptable", "bad", "hate", "awful"]):
        sentiment = Sentiment.NEGATIVE
    elif any(w in t for w in ["urgent", "immediately", "asap", "emergency", "critical"]):
        sentiment = Sentiment.URGENT
    elif any(w in t for w in ["great", "excellent", "happy", "interested", "excited", "love", "amazing", "good"]):
        sentiment = Sentiment.POSITIVE
    else:
        sentiment = Sentiment.NEUTRAL

    # ── Use text as response if it's a real AI response ──
    if len(text) > 100:
        ai_response = text[:1000]
    else:
        # Generate contextual response based on inferred category
        responses = {
            LeadCategory.GENERAL: "Hello! Welcome — I'm your AI Sales Assistant. I'm here to help with any questions about our products, pricing, demos, or support. How can I assist you today?",
            LeadCategory.COMPLAINT: "I sincerely apologize for the inconvenience you've experienced. Your satisfaction is our top priority, and I want to resolve this immediately. Could you share more details so I can escalate this to the right team right away?",
            LeadCategory.PRICING: "Thank you for your interest in our pricing! We have flexible plans designed for businesses of all sizes. I'd love to understand your specific needs so I can recommend the best option. Could you share more about your team size and requirements?",
            LeadCategory.DEMO_REQUEST: "We'd love to show you our platform in action! I can arrange a personalized demo tailored to your specific use case. When would be a good time for your team?",
            LeadCategory.SUPPORT: "I'm here to help resolve your issue as quickly as possible. Could you provide more details about what you're experiencing? Our support team is standing by.",
            LeadCategory.PARTNERSHIP: "Thank you for your interest in partnering with us! We have an active partner program with great benefits. I'd love to learn more about your organization and explore how we can collaborate.",
            LeadCategory.PRODUCT_INQUIRY: "Great question! Our platform offers a comprehensive suite of features designed to help businesses like yours. I'd be happy to walk you through our capabilities and how they might fit your needs.",
        }
        ai_response = responses.get(category, responses[LeadCategory.GENERAL])

    # ── Follow-ups ──
    followups = {
        LeadCategory.COMPLAINT: ["Escalate to support team immediately", "Issue resolution within 24 hours", "Follow up with satisfaction survey"],
        LeadCategory.PRICING: ["Send pricing deck within 1 hour", "Schedule pricing call", "Share ROI calculator"],
        LeadCategory.DEMO_REQUEST: ["Book demo within 2 hours", "Send pre-demo questionnaire", "Prepare custom demo environment"],
        LeadCategory.SUPPORT: ["Create support ticket", "Assign to technical team", "Follow up within 4 hours"],
        LeadCategory.PARTNERSHIP: ["Send partnership overview deck", "Schedule partnership discovery call", "Loop in partnerships team"],
        LeadCategory.PRODUCT_INQUIRY: ["Send product brochure", "Schedule product walkthrough", "Share customer case studies"],
        LeadCategory.GENERAL: ["Qualify the lead further", "Send welcome email", "Add to nurture sequence"],
    }
    follow_up = followups.get(category, followups[LeadCategory.GENERAL])

    return LeadAnalysisOutput(
        category=category,
        priority=priority,
        sentiment=sentiment,
        ai_response=ai_response,
        follow_up=follow_up,
        confidence_score=0.75,
        escalate=(priority == Priority.CRITICAL),
    )