# SwarmSight — Cowork Skill File
# This file tells Claude Cowork everything it needs to know about this project.
# Keep it in the root project folder so Cowork reads it automatically.

## Project Overview
SwarmSight is a multi-agent AI data analysis engine built for a hackathon.
It uses 5 specialized AI agents (Planner, Cleaner, Analyst, Validator, Reporter)
that collaborate to analyze CSV datasets and produce executive insight reports.

## Tech Stack
- Language: Python 3.11+
- Agent framework: CrewAI
- LLM: Claude API (claude-sonnet-4-20250514)
- UI: Streamlit
- Data: Pandas, scikit-learn, Plotly
- Deployment: Render.com (free tier)

## Project Structure
swarm-sight/
├── main.py              # Swarm orchestrator — DO NOT break the run_swarm() signature
├── requirements.txt     # Python dependencies
├── .env.example         # Env vars template (never edit .env directly)
├── agents/
│   ├── base.py          # call_claude() — core API wrapper used by all agents
│   ├── planner.py       # Agent 1: reads goal, creates plan
│   ├── cleaner.py       # Agent 2: cleans the CSV
│   ├── analyst.py       # Agent 3: finds patterns and insights
│   ├── validator.py     # Agent 4: cross-checks outputs, triggers retries
│   └── reporter.py      # Agent 5: writes final report
├── ui/
│   └── app.py           # Streamlit frontend with live agent feed
├── utils/
│   ├── schemas.py       # Pydantic models for all agent outputs
│   ├── logger.py        # SwarmLogger — powers the live activity feed
│   └── helpers.py       # CSV utilities
├── docs/                # Architecture diagram, pitch deck outline, README template
└── .cowork/             # THIS folder — Cowork configuration and task prompts

## Key Rules for Cowork
1. Never change the run_swarm() function signature in main.py
2. Never change the Pydantic schema field names in utils/schemas.py
3. All agent files follow the same pattern: SYSTEM prompt + run() function
4. The SwarmLogger in utils/logger.py must always be called in each agent's run()
5. All API calls go through agents/base.py call_claude() — never call anthropic directly elsewhere
6. Streamlit UI in ui/app.py imports from main.py — keep import paths consistent

## What Cowork CAN do
- Write docs/README.md following the template in docs/README_template.md
- Fill in docs/architecture.md with the architecture description
- Write the pitch deck content in docs/pitch_deck_outline.md
- Generate sample CSV files in data/samples/ for testing
- Write tests in tests/
- Update requirements.txt if new packages are needed
- Write deployment config files (render.yaml, Procfile)

## What Cowork should NOT do
- Do NOT modify agents/*.py code files (that's the dev team's job)
- Do NOT modify main.py
- Do NOT add API keys to any file
- Do NOT delete any existing files without confirmation
