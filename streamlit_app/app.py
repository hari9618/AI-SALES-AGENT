"""
streamlit_app/app.py — Premium dark enterprise Sales AI UI.
FIXED: Better error handling, typing indicator, chat history saved properly,
       insight panel always visible after first message.
"""

import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000").strip().strip('"')
API_ENDPOINT = f"{FASTAPI_BASE_URL}/api/v1/leads/analyse"

PRIORITY_COLORS = {"critical": "#FF3B3B", "high": "#FF8C00", "medium": "#FFD700", "low": "#00C851"}
PRIORITY_ICONS  = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
SENTIMENT_ICONS = {"positive": "😊", "neutral": "😐", "negative": "😠", "urgent": "⚡"}
CATEGORY_ICONS  = {
    "product_inquiry": "📦", "pricing": "💰", "support": "🛠️",
    "partnership": "🤝", "demo_request": "🎯", "complaint": "⚠️", "general": "💬",
}

st.set_page_config(
    page_title="SalesAI — Lead Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

.stApp { background:#090C10; font-family:'Space Grotesk',sans-serif; color:#E2E8F0; }

section[data-testid="stSidebar"] { background:#0D1117 !important; border-right:1px solid #1E2D3D; }
section[data-testid="stSidebar"] * { color:#CBD5E1 !important; }

.sales-header {
    background:linear-gradient(135deg,#0D1117 0%,#161B22 100%);
    border:1px solid #1E2D3D; border-radius:16px; padding:28px 36px;
    margin-bottom:24px; position:relative; overflow:hidden;
}
.sales-header::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(0,200,255,0.12) 0%,transparent 70%);
}
.header-title {
    font-size:2rem; font-weight:700;
    background:linear-gradient(90deg,#00C8FF,#0096FF,#7B2FFF);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin:0 0 6px 0;
}
.header-sub { color:#64748B; font-size:0.95rem; }

.msg-user {
    background:linear-gradient(135deg,#1A2744,#1E3A5F);
    border:1px solid #2D4A7A; border-radius:16px 16px 4px 16px;
    padding:14px 18px; margin-left:auto; max-width:78%;
    font-size:0.93rem; line-height:1.6; color:#E2E8F0;
    animation:slideInRight 0.25s ease; margin-bottom:12px;
}
.msg-ai {
    background:linear-gradient(135deg,#111827,#1F2937);
    border:1px solid #374151; border-radius:16px 16px 16px 4px;
    padding:14px 18px; max-width:78%;
    font-size:0.93rem; line-height:1.6; color:#D1D5DB;
    animation:slideInLeft 0.25s ease; margin-bottom:12px;
}
.msg-label { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px; opacity:0.6; }

@keyframes slideInRight { from{transform:translateX(20px);opacity:0} to{transform:translateX(0);opacity:1} }
@keyframes slideInLeft  { from{transform:translateX(-20px);opacity:0} to{transform:translateX(0);opacity:1} }

.insight-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:20px 0; }
.insight-card {
    background:#0D1117; border:1px solid #1E2D3D; border-radius:12px; padding:16px;
    transition:border-color 0.2s,transform 0.2s;
}
.insight-card:hover { border-color:#00C8FF44; transform:translateY(-2px); }
.insight-label { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#4B5563; margin-bottom:8px; }
.insight-value { font-size:1.05rem; font-weight:600; color:#E2E8F0; }

.followup-wrap {
    background:#0D1117; border:1px solid #1E2D3D; border-left:3px solid #0096FF;
    border-radius:0 12px 12px 0; padding:16px 20px; margin-top:16px;
}
.followup-item { display:flex; align-items:flex-start; gap:10px; padding:7px 0; font-size:0.88rem; color:#94A3B8; border-bottom:1px solid #1E2D3D33; }
.followup-item:last-child { border-bottom:none; }
.followup-dot { width:6px; height:6px; background:#0096FF; border-radius:50%; margin-top:6px; flex-shrink:0; }

.escalate-banner {
    background:linear-gradient(135deg,#2D1515,#3B1818); border:1px solid #FF3B3B44;
    border-radius:10px; padding:12px 18px; font-size:0.85rem; color:#FCA5A5;
    display:flex; align-items:center; gap:10px; margin-top:12px;
}

.empty-state { text-align:center; padding:48px 24px; color:#374151; }
.empty-icon  { font-size:2.5rem; margin-bottom:12px; }

.stTextArea textarea {
    background:#0D1117 !important; border:1px solid #1E2D3D !important;
    border-radius:12px !important; color:#E2E8F0 !important;
    font-family:'Space Grotesk',sans-serif !important; font-size:0.93rem !important;
}
.stTextArea textarea:focus { border-color:#0096FF !important; box-shadow:0 0 0 2px #0096FF22 !important; }

.stButton>button {
    background:linear-gradient(135deg,#0061FF,#0096FF) !important; color:white !important;
    border:none !important; border-radius:10px !important;
    font-family:'Space Grotesk',sans-serif !important; font-weight:600 !important;
    font-size:0.9rem !important; padding:10px 24px !important;
    transition:opacity 0.2s,transform 0.15s !important;
}
.stButton>button:hover { opacity:0.88 !important; transform:translateY(-1px) !important; }

.hist-item {
    background:#161B22; border:1px solid #1E2D3D; border-radius:8px;
    padding:10px 14px; margin-bottom:8px; font-size:0.82rem; color:#94A3B8;
    overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}

hr { border-color:#1E2D3D !important; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#090C10; }
::-webkit-scrollbar-thumb { background:#1E2D3D; border-radius:3px; }
</style>
""", unsafe_allow_html=True)


# ── State init ────────────────────────────────────────────────
def _init_state():
    defaults = {
        "session_id": uuid.uuid4().hex,
        "messages": [],
        "chat_sessions": [],
        "current_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ── API call ──────────────────────────────────────────────────
def call_api(user_input: str, session_id: str) -> Optional[Dict[str, Any]]:
    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(API_ENDPOINT, json={"user_input": user_input, "session_id": session_id})
            resp.raise_for_status()
            return resp.json()
    except httpx.ConnectError:
        st.error("⚠️ Cannot connect to FastAPI. Make sure it's running on port 8000.")
    except httpx.TimeoutException:
        st.error("⏱️ Request timed out. The AI is taking too long — try again.")
    except httpx.HTTPStatusError as e:
        st.error(f"API Error {e.response.status_code}: {e.response.text[:200]}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)[:200]}")
    return None


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px 0'>
        <div style='font-size:1.3rem;font-weight:700;
                    background:linear-gradient(90deg,#00C8FF,#0096FF);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
            🧠 SalesAI
        </div>
        <div style='font-size:0.78rem;color:#4B5563;margin-top:4px;'>Lead Intelligence Platform</div>
    </div>
    <hr style='margin:8px 0 16px 0'>
    """, unsafe_allow_html=True)

    if st.button("＋  New Conversation", use_container_width=True):
        if st.session_state.messages:
            preview = st.session_state.messages[0]["content"][:50] + "…"
            st.session_state.chat_sessions.insert(0, {
                "id": st.session_state.session_id,
                "preview": preview,
                "ts": datetime.now().strftime("%H:%M"),
            })
        st.session_state.session_id = uuid.uuid4().hex
        st.session_state.messages = []
        st.session_state.current_result = None
        st.rerun()

    st.markdown("<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#4B5563;margin:16px 0 8px 0;font-weight:600;'>Chat History</div>", unsafe_allow_html=True)

    if st.session_state.chat_sessions:
        for s in st.session_state.chat_sessions[:10]:
            st.markdown(f"<div class='hist-item'><span style='color:#4B5563;margin-right:6px;'>{s['ts']}</span>{s['preview']}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#374151;font-size:0.82rem;text-align:center;padding:20px 0;'>No previous chats yet.</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Quick test prompts ──
    st.markdown("<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#4B5563;margin-bottom:8px;font-weight:600;'>🧪 Quick Test</div>", unsafe_allow_html=True)
    test_prompts = {
        "👋 Greeting": "hi",
        "💰 Enterprise Deal": "We are a 500-person fintech company looking for enterprise CRM with API integrations. What are your plans?",
        "🚨 Urgent Complaint": "Your system has been down for 3 hours and we are losing $10,000 per hour. Fix this immediately!",
        "🎯 Demo Request": "We are evaluating 3 vendors this week. Can you do a demo tomorrow for our team of 20?",
    }
    for label, prompt in test_prompts.items():
        if st.button(label, use_container_width=True, key=f"test_{label}"):
            st.session_state["prefill"] = prompt
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.72rem;color:#374151;'>Session: <code style='color:#4B5563'>{st.session_state.session_id[:12]}…</code></div>", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class='sales-header'>
    <div class='header-title'>AI Sales Intelligence</div>
    <div class='header-sub'>Automated lead classification · Priority detection · AI-powered responses · Real-time insights</div>
</div>
""", unsafe_allow_html=True)

col_chat, col_insights = st.columns([3, 2], gap="large")

# ── Chat column ───────────────────────────────────────────────
with col_chat:
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='msg-user'><div class='msg-label'>You · {msg.get('ts','')}</div>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='msg-ai'><div class='msg-label'>🧠 SalesAI</div>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-icon'>🎯</div>
            <div style='font-size:1rem;font-weight:500;color:#4B5563;'>Submit any customer message to begin</div>
            <div style='font-size:0.83rem;margin-top:8px;color:#374151;'>
                Pricing · Complaints · Demos · Greetings · Support — anything works
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Pre-fill from quick test buttons
    default_text = st.session_state.pop("prefill", "")

    user_input = st.text_area(
        "Customer message",
        value=default_text,
        placeholder="Type any customer message — 'hi', complaints, pricing questions, demo requests…",
        height=110,
        label_visibility="collapsed",
        key="input_box",
    )

    btn_col, info_col = st.columns([1, 3])
    with btn_col:
        analyse_btn = st.button("Analyse Lead →", use_container_width=True)
    with info_col:
        st.markdown("<div style='font-size:0.78rem;color:#374151;padding-top:10px;'>Powered by Gemini 2.5 Flash · LangChain LCEL · Langfuse Tracing</div>", unsafe_allow_html=True)


# ── Insights column ───────────────────────────────────────────
with col_insights:
    st.markdown("<div style='font-size:0.85rem;font-weight:600;color:#4B5563;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:16px;'>Lead Intelligence Panel</div>", unsafe_allow_html=True)

    if st.session_state.current_result:
        r = st.session_state.current_result
        priority   = r.get("priority", "medium")
        category   = r.get("category", "general")
        sentiment  = r.get("sentiment", "neutral")
        escalate   = r.get("escalate", False)
        confidence = r.get("confidence_score")
        follow_ups = r.get("follow_up", [])

        p_color = PRIORITY_COLORS.get(priority, "#64748B")
        p_icon  = PRIORITY_ICONS.get(priority, "⚪")
        s_icon  = SENTIMENT_ICONS.get(sentiment, "😐")
        c_icon  = CATEGORY_ICONS.get(category, "💬")

        st.markdown(f"""
        <div class='insight-grid'>
            <div class='insight-card'>
                <div class='insight-label'>Category</div>
                <div class='insight-value'>{c_icon} {category.replace('_',' ').title()}</div>
            </div>
            <div class='insight-card'>
                <div class='insight-label'>Priority</div>
                <div class='insight-value'><span style='color:{p_color}'>{p_icon} {priority.title()}</span></div>
            </div>
            <div class='insight-card'>
                <div class='insight-label'>Sentiment</div>
                <div class='insight-value'>{s_icon} {sentiment.title()}</div>
            </div>
            <div class='insight-card'>
                <div class='insight-label'>Confidence</div>
                <div class='insight-value'>{f"{confidence:.0%}" if confidence else "85%"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if escalate:
            st.markdown("<div class='escalate-banner'>🚨 <strong>Escalation Required</strong> — Route to senior sales rep immediately.</div>", unsafe_allow_html=True)

        if follow_ups:
            items_html = "".join(f"<div class='followup-item'><div class='followup-dot'></div>{fu}</div>" for fu in follow_ups)
            st.markdown(f"""
            <div class='followup-wrap'>
                <div style='font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#4B5563;margin-bottom:10px;'>
                    Recommended Follow-ups
                </div>
                {items_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#0D1117;border:1px dashed #1E2D3D;border-radius:12px;padding:40px 24px;text-align:center;color:#374151;'>
            <div style='font-size:1.8rem;margin-bottom:10px;'>📊</div>
            <div style='font-size:0.88rem;'>Lead insights will appear here after analysis.</div>
            <div style='font-size:0.78rem;margin-top:8px;color:#2D3748;'>Try the quick test buttons in the sidebar →</div>
        </div>
        """, unsafe_allow_html=True)


# ── Trigger analysis ──────────────────────────────────────────
if analyse_btn and user_input and user_input.strip():
    ts = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": user_input.strip(), "ts": ts})

    with st.spinner("🧠 Analysing lead with Gemini AI…"):
        data = call_api(user_input.strip(), st.session_state.session_id)

    if data:
        result = data.get("result", {})
        ai_response = result.get("ai_response", "")

        if ai_response:
            st.session_state.messages.append({"role": "ai", "content": ai_response, "ts": datetime.now().strftime("%H:%M")})
            st.session_state.current_result = result

            if data.get("n8n_notified"):
                st.toast("🔔 Slack alert sent for high priority lead!", icon="✅")
        else:
            st.error("AI returned an empty response. Please try again.")

    st.rerun()