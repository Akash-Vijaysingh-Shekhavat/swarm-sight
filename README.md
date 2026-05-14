# 🐝 SwarmSight

**A multi-agent AI engine that turns raw CSVs into executive-grade insight reports — in seconds.**

> Built for the Agent Swarms hackathon. Powered by Claude. Orchestrated by a swarm of 5 specialized AI agents.

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io)
[![Claude](https://img.shields.io/badge/LLM-Claude%20Sonnet-purple)](https://anthropic.com)
[![Azure](https://img.shields.io/badge/Powered%20by-Azure%20AI%20Foundry-0078D4?logo=microsoftazure)](https://ai.azure.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

🚀 **Live Demo:** https://swarm-sight.onrender.com *(replace before submission)*

---

## 1. Project Description

Data analysts spend **70% of their time on data prep** — cleaning CSVs, hunting for nulls, manually writing summaries. SwarmSight eliminates that entirely.

Drop in any CSV, describe your goal in plain English, and SwarmSight unleashes a **collaborative swarm of 5 AI agents** that automatically clean your data, surface patterns, validate findings, and produce a polished executive report — with **zero configuration**.

**The problem it solves:** Non-technical users can't easily extract insights from raw data. Technical users waste time on repetitive prep work. SwarmSight automates the entire pipeline, from messy CSV to boardroom-ready insights, in seconds.

**The Agent Swarms theme:** SwarmSight is a direct implementation of agent swarm architecture — each agent is a specialist, they pass structured outputs to each other, and the Validator agent can trigger autonomous retries when quality doesn't meet the bar. It's not just an AI feature; the swarm *is* the product.

---

## 2. Architecture Overview

### The 5-Agent Pipeline

```
User: CSV + Goal
       │
       ▼
  ┌─────────┐    JSON     ┌─────────┐    JSON     ┌──────────┐
  │ Planner │ ──────────► │ Cleaner │ ──────────► │ Analyst  │
  └─────────┘             └─────────┘             └──────────┘
  Reads goal +            Fixes nulls,                  │ JSON
  dataset info,           types, dupes           ┌──────┘
  creates plan            Returns cleaned df      ▼
                                           ┌────────────┐
                                           │  Validator │
                                           └────────────┘
                                           Quality gate — checks
                                           confidence + consistency
                                                 │
                          ┌──────────────────────┴──────────────────────┐
                          │ retry_needed = True                          │ retry_needed = False
                          ▼                                              ▼
              Re-run Analyst or Cleaner                         ┌──────────┐
              (up to MAX_RETRIES = 2)                           │ Reporter │
                                                                └──────────┘
                                                                Synthesizes all outputs
                                                                into executive report
```

### Agent Communication
All agents communicate via **typed Pydantic schemas** defined in `utils/schemas.py`. No agent ever receives raw text from another agent — only validated JSON objects. This makes the swarm deterministic and debuggable.

### The Retry / Self-Healing Mechanism
The Validator agent returns a `retry_needed: bool` and `retry_agent: str` in its output. The orchestrator in `main.py` checks this after each validation pass and re-runs only the failing agent (Analyst or Cleaner), not the entire pipeline. This targeted retry approach saves latency and API cost while guaranteeing output quality.

### SwarmLogger & Live Feed
Every agent calls `logger.log(agent_name, message, status)` which fires a callback to the Streamlit UI, powering the real-time agent activity feed. Users can watch the swarm think in real time.

### ☁️ Built on Microsoft Azure AI Foundry

> **For hackathon judges:** SwarmSight runs entirely on **[Microsoft Azure AI Foundry](https://ai.azure.com)** — Microsoft's enterprise-grade platform for deploying and orchestrating AI models at scale.

All Claude inference is routed through `AnthropicFoundry` (the Azure-native Anthropic client), authenticated via `DefaultAzureCredential` and an Azure AD token provider. This means:

- **Enterprise security** — no raw API keys in the environment; authentication uses Azure AD service principals and short-lived bearer tokens
- **Azure-native deployment** — the app runs on Render but the AI backbone is hosted in Azure, giving access to Azure's SLA, compliance certifications (SOC 2, ISO 27001), and regional data residency
- **Production-ready auth** — `DefaultAzureCredential` automatically adapts between local dev (service principal / `az login`), CI/CD, and production (managed identity), with zero code changes across environments

---

## 3. AI Tools Used

| Tool | Usage |
|---|---|
| **Azure AI Foundry** | Hosts and serves Claude — enterprise-grade AI infrastructure |
| **Claude Sonnet** (`claude-sonnet-4-20250514`) | Powers all 5 agents via `agents/base.py → call_claude()` |
| **`AnthropicFoundry` client** | Azure-native Anthropic SDK client, authenticated via `DefaultAzureCredential` |
| **CrewAI** | Agent framework providing the orchestration layer |
| **Planner agent** | Parses goal + dataset metadata, produces structured analysis plan |
| **Cleaner agent** | Identifies and fixes data quality issues, returns cleaned DataFrame |
| **Analyst agent** | Finds correlations, trends, and anomalies in cleaned data |
| **Validator agent** | Evaluates outputs against confidence thresholds, triggers retries |
| **Reporter agent** | Generates the final executive summary and recommendations |

All Claude calls go through a single `call_claude()` wrapper in `agents/base.py` — never called directly elsewhere, per architecture rules. Claude is prompted to return structured JSON matching the Pydantic schema for each agent. The wrapper uses `AnthropicFoundry` (Azure AI Foundry) rather than the direct Anthropic client, so all inference is authenticated through Azure AD and routed via your Foundry resource.

---

## 4. Setup Instructions

### Prerequisites
- Python 3.11+
- An [Azure AI Foundry](https://ai.azure.com) resource with Claude deployed
- A service principal (or use `az login` for local dev — `DefaultAzureCredential` picks it up automatically)

### Step-by-step

```bash
# 1. Clone the repo
git clone https://github.com/Akash-Vijaysingh-Shekhavat/swarm-sight.git
cd swarm-sight

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Azure credentials
cp .env.example .env
# Open .env and fill in all four Azure vars:
#   AZURE_RESOURCE_NAME   — subdomain of your Foundry endpoint
#   AZURE_CLIENT_ID       — service principal app ID
#   AZURE_TENANT_ID       — your Azure AD tenant ID
#   AZURE_CLIENT_SECRET   — service principal secret

# 5. Launch the app
streamlit run ui/app.py
```

The app will open at `http://localhost:8501`. Upload any CSV, type a goal, and click **Launch Swarm**.

### CLI usage (no UI)

```bash
python main.py data/samples/sales_data.csv "Find top-performing regions and seasonal trends"
```

---

## 5. Dependencies

| Package | Version | Purpose |
|---|---|---|
| `anthropic[foundry]` | ≥0.40.0 | Claude via Azure AI Foundry (`AnthropicFoundry` client) |
| `azure-identity` | ≥1.17.0 | `DefaultAzureCredential` + token provider for Azure AD auth |
| `crewai` | ≥0.28.0 | Agent orchestration framework |
| `streamlit` | ≥1.32.0 | Web UI |
| `pandas` | ≥2.0.0 | Data manipulation |
| `scikit-learn` | ≥1.4.0 | Statistical analysis helpers |
| `plotly` | ≥5.20.0 | Interactive charts in UI |
| `pydantic` | ≥2.0.0 | Typed agent output schemas |
| `python-dotenv` | ≥1.0.0 | Environment variable management |

---

## 6. Team Members & Roles

| Name | Role |
|---|---|
| [Your Name] | ML / Agent Architecture |
| [Teammate] | Frontend / UI (Streamlit) |
| [Teammate] | Data Science / Analytics |

---

## 7. Live Demo

🌐 **https://swarm-sight.onrender.com** *(replace with live URL before submission)*

The demo is deployed on Render.com free tier. No login required — upload any CSV and the swarm runs live.

**Sample datasets to try** (included in `data/samples/`):
- `sales_data.csv` — 200-row e-commerce dataset with intentional nulls and duplicates
- `employee_survey.csv` — 150-row HR survey with mixed data quality
- `iot_sensors.csv` — 300-row sensor data with anomalous readings

---

## 🌐 Deployment

Deploying to Render.com:

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect your GitHub repo
3. Add `ANTHROPIC_API_KEY` as an environment variable in the Render dashboard
4. Click **Deploy** — `render.yaml` handles the rest automatically

The app will be live at `https://swarm-sight.onrender.com` (or your chosen service name).

> **Note:** On Render's free tier, the service spins down after 15 minutes of inactivity. The first request after a cold start may take ~30 seconds.

---

## 📁 Project Structure

```
swarm-sight/
├── main.py              # Swarm orchestrator — run_swarm() entry point
├── requirements.txt
├── .env.example
├── render.yaml          # Render.com deployment config
├── Procfile
├── agents/
│   ├── base.py          # call_claude() — core API wrapper
│   ├── planner.py
│   ├── cleaner.py
│   ├── analyst.py
│   ├── validator.py
│   └── reporter.py
├── ui/
│   └── app.py           # Streamlit frontend with live agent feed
├── utils/
│   ├── schemas.py       # Pydantic output models
│   ├── logger.py        # SwarmLogger — live activity feed
│   └── helpers.py       # CSV utilities
├── data/
│   └── samples/         # Sample CSVs for testing
├── docs/                # Architecture doc, pitch deck, submission checklist
└── tests/               # Unit tests
```

---

## 📄 License

MIT — build on it, hack it, ship it.

---

<p align="center">Built with ☕ and way too much Claude at a hackathon. 🐝</p>
