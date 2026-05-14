# 🐝 SwarmSight

**A multi-agent AI engine that turns raw CSVs into executive-grade insight reports — in seconds.**

> Built for hackers. Powered by Claude. Orchestrated by a swarm.

---

## ✨ What It Does

Drop in any CSV, describe your goal in plain English, and SwarmSight unleashes **5 specialized AI agents** that collaborate, self-correct, and produce a polished analytical report — complete with trends, anomalies, and recommendations.

No dashboards to configure. No SQL to write. Just answers.

---

## 🤖 The Swarm

| Agent | Role |
|---|---|
| 🗺️ **Planner** | Reads your goal + dataset, builds the analysis strategy |
| 🧹 **Cleaner** | Detects and fixes nulls, types, outliers — silently |
| 🔍 **Analyst** | Finds patterns, correlations, and anomalies |
| ✅ **Validator** | Cross-checks outputs, triggers retries if quality fails |
| 📝 **Reporter** | Synthesizes everything into a crisp executive report |

Agents talk to each other. If the Validator isn't satisfied, it sends the Analyst or Cleaner back to try again — up to **2 automatic retries**.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent Framework | CrewAI |
| LLM | Claude (claude-sonnet-4-20250514) |
| UI | Streamlit |
| Data | Pandas, scikit-learn, Plotly |
| Deployment | Render.com |

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/Akash-Vijaysingh-Shekhavat/swarm-sight.git
cd swarm-sight
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up your API key

```bash
cp .env.example .env
# Open .env and add your Anthropic API key
```

### 3. Run the Streamlit UI

```bash
streamlit run ui/app.py
```

### 4. Or run from the CLI

```bash
python main.py data/samples/sample.csv "Find revenue trends and top-performing segments"
```

---

## 📁 Project Structure

```
swarm-sight/
├── main.py              # Swarm orchestrator — run_swarm() entry point
├── requirements.txt
├── .env.example
├── agents/
│   ├── base.py          # call_claude() — shared API wrapper
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
└── data/
    └── samples/         # Sample CSVs for testing
```

---

## 🔄 How the Swarm Works

```
CSV + Goal
    │
    ▼
 Planner ──► Cleaner ──► Analyst
                              │
                          Validator
                         ╱         ╲
                    ✅ Pass      ❌ Retry
                         ╲         ╱
                          Reporter
                              │
                              ▼
                      Executive Report
```

The Validator acts as a quality gate — if outputs don't meet confidence thresholds, it fires targeted retries rather than restarting the whole pipeline.

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🌐 Deployment

The app is configured for **Render.com** (free tier). Once you've pushed to GitHub, connect the repo in Render and set `ANTHROPIC_API_KEY` as an environment variable.

---

## 📄 License

MIT — build on it, hack it, ship it.

---

<p align="center">Built with ☕ and way too much Claude at a hackathon.</p>
