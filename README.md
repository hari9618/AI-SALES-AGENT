# 🧠 AI Sales Automation & Lead Intelligence System

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=00C8FF&center=true&vCenter=true&width=800&lines=AI+Sales+Automation+System+%F0%9F%9A%80;Lead+Classification+%7C+Priority+Detection;Powered+by+Gemini+2.5+Flash+%F0%9F%A4%96;LangChain+LCEL+%7C+FastAPI+%7C+Streamlit;Deployed+on+AWS+EC2+%F0%9F%8C%90" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDd4bno2dHZtdmQ1NWI2NXBhMzlvemN6NTdxMmY5ejF6dXpxZmk3MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qgQUggAC3Pfv687qPC/giphy.gif" width="700"/>
</p>

<p align="center">
  <b>🚀 Automating Lead Classification · Priority Detection · AI Responses · Real-time Slack Automation</b>
</p>

---

## 🧩 Tech Badges

<p align="center">
  <img src="https://img.shields.io/badge/Google-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-LCEL-FF6B35?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/n8n-Automation-EA4B71?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Langfuse-Observability-F59E0B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS-EC2%20Deployed-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

---

## 🚀 Live Demo

<p align="center">

| Service | Live URL | Status |
|---------|----------|--------|
| 🎨 **Streamlit UI** | http://44.218.181.69:8501 | ![Live](https://img.shields.io/badge/status-live-brightgreen) |
| ⚡ **FastAPI Docs** | http://44.218.181.69:8000/docs | ![Live](https://img.shields.io/badge/status-live-brightgreen) |
| 🔄 **n8n Workflows** | http://44.218.181.69:5678 | ![Live](https://img.shields.io/badge/status-live-brightgreen) |

</p>

---

## 📌 Project Overview

The **AI Sales Automation & Lead Intelligence System** is a production-grade AI platform that automatically handles incoming business leads and customer queries using **Google Gemini 2.5 Flash**.

In traditional sales workflows, teams **manually** read every message, classify it, decide urgency, write responses, and notify the right team. This is **slow, inconsistent, and error-prone**.

This project introduces an **AI-powered autonomous system** that handles the entire sales intelligence pipeline automatically — classifying leads, detecting priority, analysing sentiment, generating professional responses, and firing **real-time Slack alerts** for high-priority leads.

---

## 🔄 n8n Automation Workflow

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWU5NWNlYzI4ZTdhNzM5NTkwOGM2NjI4OTI1ZTY5ZDEzNGM4NjM3OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.gif" width="500"/>
</p>

```
📩 Customer Message Arrives
          ↓
🛡️  Guardrails validates input
          ↓
🧠 LangChain LCEL Pipeline runs
          ↓
🤖 Gemini 2.5 Flash analyses
          ↓
📊 Pydantic Parser structures output
          ↓
    Priority = HIGH or CRITICAL?
       ↓ YES              ↓ NO
🔔 n8n Webhook      ✅ Return response
       ↓
📋 Priority Router
       ↓
💬 Slack Alert → #sales-channel
       ↓
👥 Sales Team Notified Instantly!
```

### n8n Workflow Architecture:
```
[Webhook Trigger] ──► [Call FastAPI Lead Analysis]
                                  ↓
                        [Priority Router]
                         ↓ true    ↓ false
                   [Slack Alert]  [Respond]
                         ↓
                   [Respond to Webhook ✅]
```

---

## ✨ Key Features

### 🤖 AI-Powered Lead Analysis
- Automatically classifies every customer message into **7 business categories**
- Detects urgency level with **4 priority tiers**
- Analyses customer emotional tone **(sentiment)**
- Generates professional **2-3 paragraph AI responses**
- **Confidence scoring** for every classification

### ⚡ Real-Time Automation (n8n)
- High/Critical priority leads trigger **instant Slack notifications**
- Zero manual intervention required
- Full webhook pipeline with intelligent priority routing

### 📊 Lead Intelligence Panel
- 🏷️ Category badge with icon
- 🚦 Priority indicator with colour coding
- 😊 Sentiment detection
- 📈 Confidence score (0-100%)
- 🚨 Escalation flag for human handoff
- ✅ 3 specific follow-up recommendations

### 🧠 Conversational Memory
- Session-based chat history
- Context-aware multi-turn conversations
- New chat option with full history sidebar

### 🔒 Content Safety (Guardrails)
- Input validation — blocks harmful/malicious content
- Output validation — prevents sensitive data leakage
- Smart fallback responses

### 📈 Full Observability (Langfuse)
- Every LLM call **traced and logged**
- Token usage tracking
- Latency monitoring
- Remote prompt versioning

---

## 🎯 Lead Categories

| Icon | Category | Trigger Example |
|------|----------|----------------|
| 📦 | Product Inquiry | "What features does your platform have?" |
| 💰 | Pricing | "What are your enterprise plans for 500 users?" |
| 🛠️ | Support | "I'm getting a 500 error on login" |
| 🤝 | Partnership | "We'd like to integrate with your API" |
| 🎯 | Demo Request | "Can we schedule a demo this week?" |
| ⚠️ | Complaint | "I was double charged this month!" |
| 💬 | General | "Hi, I have a quick question" |

---

## 🚨 Priority Levels

| Badge | Priority | Triggers | Action |
|-------|----------|---------|--------|
| 🔴 | **Critical** | Billing disputes, outages, legal | Instant escalation |
| 🟠 | **High** | Enterprise deals, vendor evaluations | Slack alert fired |
| 🟡 | **Medium** | Standard demos, product questions | Normal queue |
| 🟢 | **Low** | Greetings, casual inquiries | Nurture sequence |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🤖 LLM | Google Gemini 2.5 Flash | AI response generation |
| 🔗 AI Framework | LangChain LCEL | Pipeline orchestration |
| ⚡ Backend | FastAPI (Async) | REST API + Swagger |
| 🎨 Frontend | Streamlit | Premium dark enterprise UI |
| 🔄 Automation | n8n | Slack webhook workflows |
| 📊 Observability | Langfuse | Tracing & monitoring |
| 🐳 Container | Docker + Compose | Multi-service deployment |
| ☁️ Cloud | AWS EC2 (t3.small) | Production hosting |
| 🔒 Safety | Custom Guardrails | Content filtering |
| 💾 Memory | LangChain History | Session management |
| 📦 Parsing | Pydantic v2 | Structured output |

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────┐
│            Streamlit UI  (Port 8501)              │
│    Dark Enterprise Chat + Lead Insight Cards     │
└─────────────────────┬────────────────────────────┘
                      │ HTTP POST
┌─────────────────────▼────────────────────────────┐
│           FastAPI Backend (Port 8000)             │
│     Async Endpoints + Swagger + Validation       │
└─────────────────────┬────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────┐
│          LangChain LCEL Pipeline                 │
│                                                  │
│  🛡️ Guard → 📝 Prompt → 🤖 Gemini → 📊 Parser  │
└──────┬──────────────┬──────────────┬─────────────┘
       │              │              │
  ┌────▼────┐   ┌─────▼─────┐  ┌────▼────┐
  │Langfuse │   │  Memory   │  │  n8n    │
  │Tracing  │   │ Sessions  │  │Port5678 │
  └─────────┘   └───────────┘  └────┬────┘
                                     │
                               ┌─────▼─────┐
                               │   Slack   │
                               │  Alerts 🔔│
                               └───────────┘
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
├── Dockerfile             # Multi-stage production build
├── docker-compose.yml     # 3-service orchestration
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
.\env\Scripts\Activate    # Windows
source env/bin/activate   # Linux/Mac
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

```env
GOOGLE_API_KEY=your_gemini_api_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://us.cloud.langfuse.com
N8N_WEBHOOK_URL=your_n8n_webhook_url
FASTAPI_BASE_URL=http://localhost:8000
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
# Build and start all 3 services
docker-compose up --build -d

# Check running containers
docker-compose ps

# View logs
docker-compose logs fastapi
docker-compose logs streamlit
```

---

## ☁️ AWS EC2 Deployment

```bash
# 1. Connect to EC2
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP

# 2. Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu

# 3. Clone repo
git clone https://github.com/hari9618/AI-SALES-AGENT.git
cd AI-SALES-AGENT

# 4. Create .env and add your keys
nano .env

# 5. Deploy
docker-compose up --build -d
```

---

## 🧠 How It Works

```
1️⃣  Customer sends message via Streamlit UI
          ↓
2️⃣  FastAPI validates with Guardrails layer
          ↓
3️⃣  LangChain LCEL pipeline processes:
      → Few-shot + CoT prompt injected
      → Gemini 2.5 Flash generates JSON
      → 6-strategy Pydantic parser runs
          ↓
4️⃣  Response + insight cards displayed in UI
          ↓
5️⃣  Priority = HIGH/CRITICAL?
      → YES: n8n webhook fires automatically
      → Slack notification sent to sales team
          ↓
6️⃣  Langfuse logs full trace + tokens
          ↓
7️⃣  Memory saves conversation for context
```

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

✔ Building production **LangChain LCEL** pipelines  
✔ **Google Gemini 2.5 Flash** integration via init_chat_model()  
✔ **Pydantic v2** output parsing with 6 fallback strategies  
✔ **n8n workflow automation** with webhook routing  
✔ **Langfuse** observability and remote prompt management  
✔ **FastAPI** async backend with Swagger documentation  
✔ **Docker** multi-container production deployment  
✔ **AWS EC2** cloud deployment with Elastic IP  
✔ **Content safety guardrails** implementation  
✔ Session-based **conversational memory**  

---

## 🎯 Future Improvements

🔹 CRM integration (HubSpot / Salesforce)  
🔹 Email automation via SendGrid  
🔹 Lead scoring ML model  
🔹 Multi-language support  
🔹 Analytics dashboard with charts  
🔹 WhatsApp integration via Twilio  
🔹 RAG-based company knowledge base  
🔹 Model explainability (SHAP)  

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

<p align="center">
  <img src="https://img.shields.io/github/stars/hari9618/AI-SALES-AGENT?style=social"/>
  <img src="https://img.shields.io/github/forks/hari9618/AI-SALES-AGENT?style=social"/>
</p>

<p align="center">
  Made with ❤️ by Thota Hari Krishna
</p>

---

## 📢 Tags

`AI` `Sales Automation` `LangChain` `LCEL` `Gemini` `FastAPI` `Streamlit` `n8n` `Langfuse` `Docker` `AWS` `Python` `Guardrails` `Lead Intelligence` `Generative AI` `LLM` `Automation`
