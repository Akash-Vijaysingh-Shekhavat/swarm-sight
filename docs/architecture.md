# SwarmSight — System Architecture

## 1. System Overview

SwarmSight is built around a **linear pipeline of 5 specialized AI agents**, each with a single responsibility and a typed JSON output contract. The pipeline is orchestrated by `main.py`, which drives agents in sequence, collects outputs, and manages the retry loop.

```
run_swarm(df, user_goal)
    │
    ├── 1. Planner   → PlannerOutput
    ├── 2. Cleaner   → CleanerOutput + cleaned DataFrame
    ├── 3. Analyst   → AnalystOutput
    ├── 4. Validator → ValidatorOutput  (may trigger retries)
    └── 5. Reporter  → ReporterOutput
```

Each agent is implemented as a Python module in `agents/` with:
- A `SYSTEM_PROMPT` constant defining the agent's role and output schema
- A `run(...)` function that calls `call_claude()` and returns a Pydantic model

No agent knows about another agent's internals. They communicate only through the structured outputs passed by the orchestrator.

---

## 2. Agent Communication — JSON Schemas

All inter-agent data is passed as **validated Pydantic objects**, defined in `utils/schemas.py`.

```
Orchestrator (main.py)
     │
     │  passes PlannerOutput ──────────────────────►  Cleaner.run(df, plan)
     │  passes CleanerOutput + cleaned_df ──────────►  Analyst.run(df_clean, plan)
     │  passes CleanerOutput + AnalystOutput ────────►  Validator.run(clean_out, analyst_out)
     │  passes all outputs ───────────────────────────►  Reporter.run(plan, clean, analyst, validator)
```

**Why this matters:** Claude is prompted to return JSON matching the exact schema for each agent. The `call_claude()` wrapper in `agents/base.py` parses the raw response and returns a plain dict, which the agent's `run()` function then validates into a Pydantic model. If parsing fails, the error surfaces immediately rather than silently corrupting downstream agents.

**Schema contract example:**
```python
class ValidatorOutput(BaseModel):
    confidence_score: float        # 0.0–1.0
    issues_found: list[str]
    retry_needed: bool
    retry_agent: str               # "Analyst" | "Cleaner" | "None"
    validation_notes: str
```

---

## 3. The Retry / Self-Healing Loop

The Validator is the quality gate of the swarm. After the Analyst runs, the Validator independently evaluates both the cleaning output and the analysis output.

```python
# main.py — orchestrator retry loop
for attempt in range(MAX_RETRIES):           # MAX_RETRIES = 2
    validator_out = validator.run(clean_out, analyst_out)

    if not validator_out.retry_needed:
        break                                # quality passed → continue to Reporter

    if validator_out.retry_agent == "Analyst":
        analyst_out = analyst.run(df_clean, plan)    # re-run only Analyst
    elif validator_out.retry_agent == "Cleaner":
        df_clean, clean_out = cleaner.run(df, plan)  # re-run only Cleaner
```

**Key design decisions:**
- **Targeted retries, not full restarts.** Only the failing agent re-runs, preserving other outputs and saving API cost.
- **Bounded retries.** `MAX_RETRIES = 2` prevents infinite loops. After 2 attempts, the pipeline proceeds with the best output available.
- **Validator is independent.** The Validator uses a separate Claude call with a strict evaluation prompt — it doesn't share context with the agents it's judging, preventing sycophancy.

---

## 4. The SwarmLogger

`utils/logger.py` implements `SwarmLogger`, a lightweight event bus that connects agent execution to the Streamlit UI's live feed.

**Architecture:**
```
Agent.run()
    │
    └── logger.log(agent_name, message, status)
            │
            └── self._callback(event_dict)   ← set by Streamlit UI
                    │
                    └── feed_placeholder.markdown(html)   ← live update
```

**Event structure:**
```python
{
    "agent":     "Analyst",
    "message":   "Found 3 significant correlations",
    "status":    "success",   # info | success | error | retry
    "timestamp": "14:23:05"
}
```

The Streamlit app sets the callback via `logger.set_callback(on_event)` before calling `run_swarm()`. Each agent fires log events at key moments (start, API call, completion, errors), which the UI renders in real time as colour-coded monospace cards.

---

## 5. Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         USER (Streamlit UI)                          │
│          Upload CSV + Type Goal + Click "Launch Swarm"               │
└───────────────────┬──────────────────────────────────────────────────┘
                    │  df (DataFrame) + user_goal (str)
                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR  main.py                            │
│                        run_swarm()                                   │
└──┬───────────────────────────────────────────────────────────────────┘
   │
   │ dataset_info + user_goal
   ▼
┌──────────┐   PlannerOutput (JSON)
│ PLANNER  │ ─────────────────────────────────────────────────────────►
└──────────┘                                                           │
   (Claude)                                                            │
                                                                       │ plan
   ┌───────────────────────────────────────────────────────────────────┘
   │
   ▼
┌──────────┐   CleanerOutput (JSON) + cleaned_df
│ CLEANER  │ ─────────────────────────────────────────────────────────►
└──────────┘                                                           │
   (Claude)                                                            │
                                                                       │ df_clean, clean_out
   ┌───────────────────────────────────────────────────────────────────┘
   │
   ▼
┌──────────┐   AnalystOutput (JSON)
│ ANALYST  │ ─────────────────────────────────────────────────────────►
└──────────┘                                                           │
   (Claude)                                                            │
                                                                  ┌────┘
                                                                  │ analyst_out
                                                                  ▼
                                                          ┌───────────────┐
                                                          │   VALIDATOR   │
                                                          └───────┬───────┘
                                                            (Claude)
                                                                  │
                               ┌──────────────────────────────────┤
                               │ retry_needed=True                │ retry_needed=False
                               ▼                                  ▼
                     Re-run Analyst or Cleaner           ┌──────────────┐
                     (max 2 attempts)                    │   REPORTER   │
                               │                         └──────┬───────┘
                               └──────────────────────►   (Claude)    │
                                                                       │
                                                                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     STREAMLIT UI  ui/app.py                          │
│  Metrics | Executive Summary | Key Insights | Recommendations        │
│  Download Cleaned CSV | Null-fix Chart | Live Agent Feed             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. Why This Architecture Wins

**Modularity**
Each agent is a self-contained file. Swapping out the Analyst logic or upgrading to a different Claude model requires changing one file, not the entire system.

**Observability**
The SwarmLogger gives full visibility into every agent decision in real time. Users see exactly which agent is running, how long it takes, and whether retries were triggered.

**Self-healing quality**
The Validator + retry loop means the system corrects itself before the user sees a bad output. Most pipelines fail silently; SwarmSight fails loudly and fixes it automatically.

**Scalability**
Adding a 6th agent (e.g., a Visualizer) requires: create `agents/visualizer.py`, add a schema to `utils/schemas.py`, and add one line to `main.py`. Nothing else changes.

**Cost efficiency**
Targeted retries (re-run one agent, not the whole pipeline) keep API costs low even when quality issues are detected.

**Deterministic outputs**
Pydantic schema validation at every agent boundary means a bad Claude response is caught immediately, not silently passed downstream. The system either produces correct output or fails fast with a clear error.
