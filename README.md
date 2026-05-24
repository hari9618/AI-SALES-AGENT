# 🧠 AI Sales Automation & Lead Intelligence System

> **Production-grade AI platform** for automated lead classification, priority detection, sentiment analysis, and intelligent response generation.
> Built with **Google Gemini 2.5 Flash · LangChain LCEL · FastAPI · Streamlit · Docker · n8n · Langfuse**.

---

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start (Local)](#quick-start-local)
- [Environment Variables](#environment-variables)
- [Docker Setup](#docker-setup)
- [Gemini API Setup](#gemini-api-setup)
- [Langfuse Setup](#langfuse-setup)
- [n8n Setup](#n8n-setup)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [API Reference](#api-reference)
- [Features](#features)

---

## 🏗 Architecture Overview

```
Customer Query
      │
      ▼
┌─────────────────┐        ┌──────────────────────┐
│  Streamlit UI   │◄──────►│  FastAPI Backend      │
│  (Port 8501)    │        │  (Port 8000)          │
└─────────────────┘        └──────────┬───────────┘
                                       │
                           ┌──────────▼───────────┐
                           │  LangChain LCEL       │
                           │  Pipeline             │
                           │  ┌─────────────────┐  │
                           │  │ Guardrails      │  │
                           │  │ Prompt Engine   │  │
                           │  │ Gemini 2.5 Flash│  │
                           │  │ Pydantic Parser │  │
                           │  │ Memory / History│  │
                           │  └─────────────────┘  │
                           └──────────┬───────────┘
                                       │
                     ┌─────────────────┼──────────────┐
                     ▼                 ▼              ▼
              ┌───────────┐   ┌──────────────┐  ┌──────────┐
              │ Langfuse  │   │  n8n Webhook │  │ Response │
              │ (Tracing) │   │  (Automation)│  │ to User  │
              └───────────┘   └──────────────┘  └──────────┘
```

---

## ⚡ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Google Gemini 2.5 Flash |
| AI Framework | LangChain LCEL (latest) |
| Backend API | FastAPI (async) |
| Frontend | Streamlit (premium dark UI) |
| Observability | Langfuse |
| Content Safety | Custom Guardrails layer |
| Automation | n8n |
| Containerisation | Docker + Docker Compose |
| Output Parsing | Pydantic v2 |
| Deployment | AWS EC2 ready |

---

## 📁 Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routes, lifespan
│   ├── llm.py           # Gemini 2.5 Flash via init_chat_model()
│   ├── prompt.py        # ChatPromptTemplate, few-shot, CoT, Langfuse
│   ├── parser.py        # Pydantic schema + PydanticOutputParser
│   ├── chains.py        # LCEL pipeline (Parallel, Branch, Passthrough)
│   ├── memory.py        # InMemoryChatMessageHistory + RunnableWithMessageHistory
│   ├── guardrails.py    # Input/output content safety layer
│   ├── utils.py         # Langfuse client, n8n notifier, helpers
│   └── static/          # CSS, HTML templates
│
├── streamlit_app/
│   └── app.py           # Dark enterprise chat UI
│
├── workflows/
│   └── n8n_workflow.json # Importable n8n automation workflow
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerised run)
- Google Gemini API key

### 1. Clone & set up

```bash
git clone https://github.com/your-username/ai-sales-system.git
cd ai-sales-system

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY (minimum required)
```

### 3. Run FastAPI backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run Streamlit frontend (new terminal)

```bash
cd ai-sales-system
streamlit run streamlit_app/app.py --server.port 8501
```

Open **http://localhost:8501** to access the UI.
Swagger docs: **http://localhost:8000/docs**

---

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | Gemini API key from Google AI Studio |
| `LANGFUSE_PUBLIC_KEY` | Optional | Langfuse project public key |
| `LANGFUSE_SECRET_KEY` | Optional | Langfuse project secret key |
| `LANGFUSE_HOST` | Optional | Default: `https://cloud.langfuse.com` |
| `N8N_WEBHOOK_URL` | Optional | n8n webhook URL for automations |
| `FASTAPI_BASE_URL` | Optional | Default: `http://localhost:8000` |
| `APP_ENV` | Optional | `production` or `development` |

---

## 🐳 Docker Setup

```bash
# 1. Copy and configure .env
cp .env.example .env
# Set GOOGLE_API_KEY in .env

# 2. Build and start all services
docker-compose up --build -d

# 3. Check service health
docker-compose ps
docker-compose logs fastapi

# 4. Access
#   Streamlit UI  → http://localhost:8501
#   FastAPI docs  → http://localhost:8000/docs
#   n8n UI        → http://localhost:5678
```

---

## 🤖 Gemini API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add to `.env`:
   ```
   GOOGLE_API_KEY=AIza...your_key_here
   ```
4. The system uses **Gemini 2.5 Flash** (`gemini-2.5-flash`)

---

## 📊 Langfuse Setup

Langfuse provides tracing, token tracking, and prompt management.

1. Create a free account at [cloud.langfuse.com](https://cloud.langfuse.com)
2. Create a new project → copy **Public Key** and **Secret Key**
3. Add to `.env`:
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
4. *(Optional)* Create a prompt named `sales-ai-system` in the Langfuse UI to manage the system prompt remotely.
5. Traces will appear automatically in your Langfuse dashboard after the first API call.

---

## 🔄 n8n Setup

n8n handles automated workflows triggered by high-priority leads.

### Using Docker Compose
n8n is included as a service and starts automatically on port **5678**.

### Manual Import
1. Open **http://localhost:5678**
2. Go to **Workflows → Import from File**
3. Upload `workflows/n8n_workflow.json`
4. Update the Slack webhook URL and email credentials in the workflow
5. Activate the workflow

### Trigger
The workflow listens at `http://localhost:5678/webhook/sales-lead`.
The FastAPI backend automatically POSTs to this URL for `critical` and `high` priority leads.

---

## ☁️ AWS EC2 Deployment

### 1. Launch EC2 instance
- AMI: **Ubuntu 22.04 LTS**
- Instance type: `t3.medium` (minimum) / `t3.large` (recommended)
- Security Group — open inbound ports: `22`, `8000`, `8501`, `5678`

### 2. SSH and install Docker

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Deploy application

```bash
# Clone repository
git clone https://github.com/your-username/ai-sales-system.git
cd ai-sales-system

# Configure environment
cp .env.example .env
nano .env   # Add your API keys

# Start services
docker-compose up --build -d

# Verify
docker-compose ps
```

### 4. Access your deployment
- **Streamlit**: `http://<EC2_PUBLIC_IP>:8501`
- **FastAPI docs**: `http://<EC2_PUBLIC_IP>:8000/docs`
- **n8n**: `http://<EC2_PUBLIC_IP>:5678`

### 5. (Optional) Nginx reverse proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api  { proxy_pass http://localhost:8000; }
    location /     { proxy_pass http://localhost:8501; }
}
```

---

## 📡 API Reference

### POST `/api/v1/leads/analyse`
Analyse a customer lead.

**Request body:**
```json
{
  "user_input": "We need an enterprise plan for 500 users with API access.",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "session_id": "abc123",
  "n8n_notified": true,
  "result": {
    "category": "pricing",
    "priority": "high",
    "sentiment": "positive",
    "ai_response": "Thank you for your inquiry...",
    "follow_up": ["Schedule enterprise demo", "Send pricing deck"],
    "confidence_score": 0.92,
    "escalate": false
  }
}
```

### GET `/api/v1/sessions`
List all active sessions.

### DELETE `/api/v1/sessions/{session_id}`
Clear a session's chat history.

### GET `/health`
Service health check.

---

## ✨ Features

- **🎯 Smart Lead Classification** — 7 business categories with confidence scoring
- **⚡ Priority Detection** — Critical / High / Medium / Low with auto-escalation
- **💬 Sentiment Analysis** — Positive / Neutral / Negative / Urgent detection
- **🤖 AI Response Generation** — Professional, empathetic responses via Gemini 2.5 Flash
- **📋 Follow-up Recommendations** — 2–3 actionable next steps for the sales team
- **🔒 Content Safety** — Input/output guardrails with harmful content filtering
- **💾 Conversational Memory** — Session-based context awareness across turns
- **📊 Observability** — Full Langfuse tracing, token tracking, and prompt management
- **🔄 Workflow Automation** — n8n webhook integration for Slack/email notifications
- **🎨 Premium UI** — Dark enterprise Streamlit interface with animated insights panel
- **🐳 Docker Ready** — One-command deployment with Docker Compose
- **☁️ AWS Ready** — EC2 deployment guide included

---

## 🤝 Contributing
PRs welcome. Please follow the existing code style and add type hints.

## 📄 License
MIT
