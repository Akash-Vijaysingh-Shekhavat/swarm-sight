# SwarmSight — Cowork Task Prompts
# Copy-paste these prompts directly into Cowork, one task at a time.
# Always grant Cowork access to the /swarm-sight folder before starting.

---

## TASK 1 — Generate Sample Test Data
Goal: Create realistic sample CSV files so the dev team can test the swarm immediately.

PROMPT:
"Read the SKILL.md file in the .cowork folder to understand the SwarmSight project.
Then create 3 sample CSV files in the data/samples/ folder:

1. sales_data.csv — 200 rows of e-commerce sales data with columns:
   order_id, customer_id, product_name, category, quantity, unit_price, total_price,
   order_date, region, sales_rep. Include ~15 intentional nulls and ~5 duplicate rows
   spread across the file (to test the Cleaner agent).

2. employee_survey.csv — 150 rows of employee satisfaction survey with columns:
   employee_id, department, tenure_years, satisfaction_score (1-10), engagement_score,
   manager_rating, would_recommend (yes/no), last_promotion_date. Include mixed data quality.

3. iot_sensors.csv — 300 rows of IoT sensor readings with columns:
   sensor_id, location, temperature, humidity, pressure, battery_level, timestamp,
   status (active/inactive/error). Include some anomalous readings (very high/low values).

Make the data realistic, varied, and messy enough to show off the Cleaner and Analyst agents."

---

## TASK 2 — Write the GitHub README
Goal: Create a complete, submission-ready README.md in the project root.

PROMPT:
"Read the SKILL.md file in .cowork/ and the template in docs/README_template.md.
Then write a comprehensive README.md in the project root folder.

The README must include these exact sections (hackathon requirement):
1. Project Description — what SwarmSight does, the problem it solves, the Agent Swarms theme
2. Architecture Overview — describe the 5-agent pipeline (Planner → Cleaner → Analyst → Validator → Reporter), how agents communicate via JSON schemas, the retry/self-healing mechanism
3. AI Tools Used — Claude API (claude-sonnet-4-20250514), CrewAI, list each agent's role
4. Setup Instructions — step by step: clone repo, pip install -r requirements.txt, set ANTHROPIC_API_KEY in .env, run streamlit run ui/app.py
5. Dependencies — list key packages from requirements.txt with versions
6. Team Members & Roles — use placeholder names: [Your Name] - ML/Agent Architecture, [Teammate] - Frontend/UI, [Teammate] - Data Science
7. Live Demo — placeholder: https://swarm-sight.onrender.com (replace before submission)

Keep it under 3 pages equivalent. Make it professional and impressive for judges.
Save as README.md in the project root."

---

## TASK 3 — Write the Architecture Document
Goal: Create a detailed architecture doc for slide 4 of the pitch deck.

PROMPT:
"Read the SKILL.md in .cowork/ and all files in the agents/ folder (base.py, planner.py,
cleaner.py, analyst.py, validator.py, reporter.py).

Write a detailed architecture document at docs/architecture.md that explains:

1. System Overview — how the 5 agents form a pipeline
2. Agent Communication — how JSON schemas (from utils/schemas.py) pass data between agents
3. The Retry/Self-Healing Loop — how the Validator agent detects issues and the Orchestrator
   in main.py retries failed agents up to MAX_RETRIES times
4. The SwarmLogger — how real-time events flow to the Streamlit UI
5. Data Flow Diagram (describe as text/ASCII art):
   User Upload → Planner → Cleaner → Analyst → Validator → (retry loop) → Reporter → UI
6. Why This Architecture Wins — bullet points on scalability, modularity, observability

This document will be used to create the architecture diagram slide in the pitch deck."

---

## TASK 4 — Write the Pitch Deck Content
Goal: Create complete slide-by-slide content for the 10-slide PDF deck.

PROMPT:
"Read the SKILL.md in .cowork/, docs/architecture.md, and README.md.

Write the complete content for a 10-slide pitch deck at docs/pitch_deck_outline.md.
For each slide, write the exact text that should appear on that slide.

Judging criteria to emphasize (include these weights as speaker notes):
- AI Integration & Intelligence Design: 25 pts
- System Architecture & Engineering Quality: 25 pts
- Communication, Presentation & UX: 15 pts
- Prototype Readiness & Scalability: 15 pts
- Problem Depth & Product Clarity: 10 pts
- Market Understanding & Product Fit: 10 pts

Slide structure:
Slide 1 - Title: SwarmSight, tagline, team names, hackathon name
Slide 2 - Problem: 'Analysts spend 70% of time on data prep, 30% on actual insight'
Slide 3 - Solution: What SwarmSight does in one sentence + 3 bullet benefits
Slide 4 - Architecture: Describe the 5-agent pipeline for a visual diagram
Slide 5 - AI Integration: Claude API usage per agent, JSON schemas, retry logic
Slide 6 - How It Works: Step-by-step user flow (upload CSV → swarm runs → get report)
Slide 7 - Demo Screenshots: Write captions for 3 UI screenshots to be added
Slide 8 - Tech Stack: List all technologies with logos placeholder
Slide 9 - Impact & Market: 2-3 target personas, market size, use cases
Slide 10 - What's Next: 3-month roadmap, enterprise features, team ask

Include speaker notes for each slide with what to say during the live pitch."

---

## TASK 5 — Write the Test Suite
Goal: Create basic tests so the team can verify each agent works before the demo.

PROMPT:
"Read the SKILL.md in .cowork/ and all files in agents/ and utils/.

Write a test file at tests/test_agents.py that tests each agent with mock data.
Use Python's built-in unittest (no pytest needed).

Tests to write:
1. test_schemas — import all schemas from utils/schemas.py, verify they instantiate correctly
2. test_logger — verify SwarmLogger logs events and calls the callback
3. test_helpers — test load_csv, get_dataset_info with a small inline DataFrame
4. test_cleaner_cleaning — create a dirty DataFrame (with nulls/dupes), run cleaner.run(),
   verify the cleaned DataFrame has fewer nulls
5. test_full_pipeline — mock the call_claude function to return valid JSON,
   run the full run_swarm() pipeline, verify all 5 result keys exist

Also write a simple tests/test_data.py that:
- Loads each CSV in data/samples/
- Verifies it has at least 100 rows and expected columns
- Prints a pass/fail summary

Add instructions at the top: 'Run with: python -m pytest tests/ or python tests/test_agents.py'"

---

## TASK 6 — Create Deployment Config
Goal: Set up files needed to deploy on Render.com (free tier) for the live demo URL.

PROMPT:
"Read the SKILL.md in .cowork/ and requirements.txt.

Create these deployment files:

1. render.yaml in the project root:
   - Service type: web
   - Build command: pip install -r requirements.txt
   - Start command: streamlit run ui/app.py --server.port $PORT --server.address 0.0.0.0
   - Environment variable: ANTHROPIC_API_KEY (mark as secret)
   - Free tier settings

2. Procfile in the project root:
   web: streamlit run ui/app.py --server.port $PORT --server.address 0.0.0.0

3. runtime.txt in the project root:
   python-3.11.0

4. .streamlit/config.toml:
   [server]
   headless = true
   enableCORS = false
   [theme]
   primaryColor = '#3b82f6'
   backgroundColor = '#0f172a'
   secondaryBackgroundColor = '#1e293b'
   textColor = '#f1f5f9'

5. Update README.md to add a 'Deployment' section explaining how to deploy to Render:
   - Go to render.com, create new Web Service
   - Connect GitHub repo
   - Add ANTHROPIC_API_KEY as environment variable
   - Deploy — the render.yaml handles everything else"

---

## TASK 7 — Final Submission Checklist
Goal: Verify all 4 deliverables are ready before the June 7 deadline.

PROMPT:
"Read the SKILL.md in .cowork/ and all files in the project.

Create a submission checklist at docs/SUBMISSION_CHECKLIST.md that:

1. Lists all 4 required deliverables:
   □ Project Deck (PDF) — TeamName_Deck.pdf, max 10 slides, max 20MB
   □ Demo Video — MP4, max 3 min, YouTube unlisted link, min 720p
   □ GitHub Repository — public, README.md complete
   □ Prototype Live Link — URL working, no login required

2. For each deliverable, checks off what's already done in this project folder

3. Lists exactly what's still missing (things Cowork cannot do):
   - Record the demo video
   - Export the pitch deck to PDF
   - Push code to GitHub (git init, git push)
   - Deploy to Render and get the live URL
   - Upload video to YouTube and get the unlisted link

4. Creates a final 3-day pre-submission schedule:
   June 5: Record video + export deck PDF
   June 6: Deploy to Render + get live URL + final README update
   June 7: Submit on HackerEarth before midnight

5. Adds a 'File Naming' section:
   - Rename the deck PDF to: [YourTeamName]_Deck.pdf
   - Video filename: [YourTeamName]_Demo.mp4"
