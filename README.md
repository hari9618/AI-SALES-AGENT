# 🧠 AI Sales Automation & Lead Intelligence System

<p align="center">
  <img src="https://media.giphy.com/media/l0HlHFRbmaZtBRhXG/giphy.gif" width="700" />
</p>

<p align="center">
  🚀 Automating Lead Classification · Priority Detection · AI Responses · Slack Automation
</p>

---

## 🧩 Tech Badges

<p align="center">
  <img src="https://img.shields.io/badge/AI-Sales%20Intelligence-blueviolet"/>
  <img src="https://img.shields.io/badge/Google-Gemini%202.5%20Flash-blue"/>
  <img src="https://img.shields.io/badge/LangChain-LCEL-orange"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-green"/>
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red"/>
  <img src="https://img.shields.io/badge/n8n-Automation-pink"/>
  <img src="https://img.shields.io/badge/Langfuse-Observability-yellow"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED"/>
  <img src="https://img.shields.io/badge/AWS-EC2%20Deployed-FF9900"/>
  <img src="https://img.shields.io/badge/Python-3.11+-blue"/>
</p>

---

## 🚀 Live Demo

<p align="center">

| Service | Live URL |
|---------|----------|
| 🎨 **Streamlit UI** | http://44.218.181.69:8501 |
| ⚡ **FastAPI Docs** | http://44.218.181.69:8000/docs |
| 🔄 **n8n Workflows** | http://44.218.181.69:5678 |

</p>

---

## 📌 Project Overview

The **AI Sales Automation & Lead Intelligence System** is a production-grade AI platform that automatically handles incoming business leads and customer queries using Google Gemini 2.5 Flash.

In traditional sales workflows, teams manually read every message, classify it, decide urgency, write responses, and notify the right team. This is **slow, inconsistent, and error-prone**.

This project introduces an **AI-powered autonomous system** that handles the entire sales intelligence pipeline automatically — classifying leads, detecting priority, analysing sentiment, generating professional responses, and firing real-time Slack alerts for high-priority leads.

---

## 🔄 n8n Automation Workflow

<p align="center">
  <img src="https://media.giphy.com/media/3oKIPEqDGUULpEU0aQ/giphy.gif" width="600"/>
</p>

```
Customer Message
      ↓
FastAPI receives & validates
      ↓
LangChain LCEL Pipeline runs
      ↓
Gemini 2.5 Flash analyses
      ↓
Priority detected as HIGH/CRITICAL?
      ↓ YES
n8n Webhook triggered automatically
      ↓
Priority Router checks level
      ↓
🔔 Slack Alert fires to #sales-channel
      ↓
Sales team notified in real-time!
```

### n8n Workflow Nodes:
```
[Webhook Trigger] → [Call FastAPI] → [Priority Router]
                                            ↓ true (high/critical)
                                     [Slack Alert 🔔]
                                            ↓
                                     [Respond to Webhook ✅]
```

---

## ✨ Key Features

### 🤖 AI-Powered Lead Analysis
- Automatically classifies every customer message into 7 business categories
- Detects urgency level with 4 priority tiers
- Analyses customer emotional tone (sentiment)
- Generates professional 2-3 paragraph AI responses

### ⚡ Real-Time Automation (n8n)
- High/Critical priority leads trigger **instant Slack notifications**
- Zero manual intervention required
- Full webhook pipeline with priority routing

### 📊 Lead Intelligence Panel
- Category badge with icon
- Priority indicator with colour coding
- Sentiment detection
- Confidence score (0-100%)
- Escalation flag for human handoff
- 3 specific follow-up recommendations

### 🧠 Conversational Memory
- Session-based chat history
- Context-aware multi-turn conversations
- New chat option with history sidebar

### 🔒 Content Safety (Guardrails)
- Input validation — blocks harmful content
- Output validation — prevents data leakage
- Safe fallback responses

### 📈 Full Observability (Langfuse)
- Every LLM call traced and logged
- Token usage tracking
- Latency monitoring
- Prompt versioning

---

## 🎯 Lead Categories

| Icon | Category | Example |
|------|----------|---------|
| 📦 | Product Inquiry | "What features does your platform have?" |
| 💰 | Pricing | "What are your enterprise plans?" |
| 🛠️ | Support | "I'm getting an error on login" |
| 🤝 | Partnership | "We'd like to integrate with your API" |
| 🎯 | Demo Request | "Can we schedule a demo?" |
| ⚠️ | Complaint | "I was double charged this month!" |
| 💬 | General | "Hi, I have a quick question" |

---

## 🚨 Priority Levels

| Badge | Priority | Triggers |
|-------|----------|---------|
| 🔴 | **Critical** | Billing disputes, outages, legal threats |
| 🟠 | **High** | Enterprise deals, active vendor evaluations |
| 🟡 | **Medium** | Standard product questions, demos |
| 🟢 | **Low** | Greetings, casual inquiries |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🤖 LLM | Google Gemini 2.5 Flash | AI response generation |
| 🔗 AI Framework | LangChain LCEL | Pipeline orchestration |
| ⚡ Backend | FastAPI | Async REST API |
| 🎨 Frontend | Streamlit | Premium dark UI |
| 🔄 Automation | n8n | Slack webhook workflows |
| 📊 Observability | Langfuse | Tracing & monitoring |
| 🐳 Container | Docker + Compose | Deployment |
| ☁️ Cloud | AWS EC2 | Production hosting |
| 🔒 Safety | Custom Guardrails | Content filtering |
| 💾 Memory | LangChain History | Session management |

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────┐
│         Streamlit UI  (Port 8501)            │
│   Dark Enterprise Chat + Insight Cards      │
└──────────────────┬──────────────────────────┘
                   │ HTTP
┌──────────────────▼──────────────────────────┐
│         FastAPI Backend (Port 8000)          │
│    /api/v1/leads/analyse  +  Swagger        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        LangChain LCEL Pipeline              │
│                                             │
│  Guardrails → Prompt → Gemini → Parser     │
│       ↓           ↓        ↓        ↓      │
│   Safety      Few-Shot    LLM    Pydantic   │
└──────┬──────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────┐
│              Supporting Services            │
│                                             │
│  Langfuse (Tracing)  Memory (Sessions)     │
│  n8n (Port 5678)     Guardrails (Safety)   │
│       ↓                                     │
│  Slack Alerts 🔔                            │
└─────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI-SALES-AGENT/
│
├── app/
│   ├── main.py          # FastAPI app + all endpoints
│   ├── llm.py           # Gemini 2.5 Flash via init_chat_model()
│   ├── prompt.py        # Few-shot + CoT + Langfuse prompts
│   ├── parser.py        # Pydantic schema + 6-strategy parser
│   ├── chains.py        # LCEL Pipeline (Parallel/Branch/Pass)
│   ├── memory.py        # InMemoryChatMessageHistory
│   ├── guardrails.py    # Input/output content safety
│   └── utils.py         # Langfuse client + n8n notifier
│
├── streamlit_app/
│   └── app.py           # Premium dark enterprise UI
│
├── workflows/
│   └── n8n_workflow.json  # Importable n8n automation
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository
```bash
git clone https://github.com/hari9618/AI-SALES-AGENT.git
cd AI-SALES-AGENT
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv env
.\env\Scripts\Activate   # Windows
source env/bin/activate  # Linux/Mac
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

```env
GOOGLE_API_KEY=your_gemini_api_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://us.cloud.langfuse.com
N8N_WEBHOOK_URL=your_n8n_webhook_url
```

### 5️⃣ Run FastAPI Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6️⃣ Run Streamlit Frontend
```bash
streamlit run streamlit_app/app.py
```

---

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up --build -d

# Check running containers
docker-compose ps

# View logs
docker-compose logs fastapi
```

---

## ☁️ AWS EC2 Deployment

```bash
# Connect to EC2
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu

# Clone and deploy
git clone https://github.com/hari9618/AI-SALES-AGENT.git
cd AI-SALES-AGENT
# Create .env with your keys
docker-compose up --build -d
```

---

## 🧠 How It Works

```
1️⃣  Customer sends message via Streamlit UI
2️⃣  FastAPI validates with Guardrails
3️⃣  LangChain LCEL pipeline processes:
      → Few-shot prompt injected
      → Gemini 2.5 Flash generates JSON
      → Pydantic parser structures output
4️⃣  Response displayed with insight cards
5️⃣  If HIGH/CRITICAL → n8n webhook fires
6️⃣  Slack notification sent to sales team
7️⃣  Langfuse logs entire trace
8️⃣  Memory saves conversation for context
```

---

## 📷 Application Preview
<img width="1908" height="898" alt="Screenshot 2026-05-25 121354" src="https://github.com/user-attachments/assets/a6f617bd-829c-4464-93cf-9a5342d15a12" />


### 🎨 Main Chat Interface
> Premium dark enterprise UI with real-time lead insights panel

### 📊 Lead Intelligence Panel
> Category · Priority · Sentiment · Confidence · Follow-ups

### 🔔 Slack Automation
> Automatic notifications for high-priority leads via n8n

### 📈 Langfuse Dashboard
> Full observability — traces, tokens, latency

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/leads/analyse` | Analyse a customer lead |
| `GET` | `/api/v1/sessions` | List active sessions |
| `DELETE` | `/api/v1/sessions/{id}` | Clear session history |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/webhook/n8n` | n8n inbound webhook |

---

## 📚 What I Learned

✔ Building production LangChain LCEL pipelines  
✔ Google Gemini 2.5 Flash integration  
✔ Pydantic output parsing with fallback strategies  
✔ n8n workflow automation with webhooks  
✔ Langfuse observability and prompt management  
✔ FastAPI async backend development  
✔ Docker multi-container deployment  
✔ AWS EC2 production deployment  
✔ Content safety guardrails implementation  
✔ Session-based conversational memory  

---

## 🎯 Future Improvements

🔹 CRM integration (HubSpot/Salesforce)  
🔹 Email automation via SendGrid  
🔹 Lead scoring with ML model  
🔹 Multi-language support  
🔹 Voice input for leads  
🔹 Analytics dashboard with charts  
🔹 WhatsApp integration via Twilio  
🔹 RAG-based company knowledge base  

---

## 👨‍💻 Author

**Thota Hari Krishna**  
AI Enthusiast | Gen AI Engineer | Full Stack AI Developer

🔗 GitHub: https://github.com/hari9618

---

## ⭐ Support

If you like this project:

⭐ **Star the repository**  
📢 **Share with others**  
🔗 **Connect on LinkedIn**  

---

## 📢 Tags

`AI` `Sales Automation` `LangChain` `LCEL` `Gemini` `FastAPI` `Streamlit` `n8n` `Langfuse` `Docker` `AWS` `Python` `Guardrails` `Lead Intelligence` `Generative AI`
