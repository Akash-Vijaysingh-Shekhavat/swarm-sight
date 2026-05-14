"""
SwarmSight — Multi-Agent Data Analysis Engine
Entry point: orchestrates the full agent swarm pipeline.
"""
import os
import pandas as pd
from dotenv import load_dotenv
from utils.logger import logger
from utils.helpers import get_dataset_info
from agents import planner, cleaner, analyst, validator, reporter

load_dotenv()

MAX_RETRIES = 2

def run_swarm(df: pd.DataFrame, user_goal: str, log_callback=None) -> dict:
    """
    Orchestrate the full 5-agent swarm on a dataframe.
    Returns a dict with all agent outputs.
    """
    if log_callback:
        logger.set_callback(log_callback)

    logger.clear()
    results = {}

    # 1. Planner
    dataset_info = get_dataset_info(df)
    plan = planner.run(user_goal, dataset_info)
    results["plan"] = plan

    # 2. Cleaner
    df_clean, clean_out = cleaner.run(df, plan)
    results["cleaner"] = clean_out
    results["cleaned_df"] = df_clean

    # 3. Analyst
    analyst_out = analyst.run(df_clean, plan)
    results["analyst"] = analyst_out

    # 4. Validator — with retry loop
    for attempt in range(MAX_RETRIES):
        validator_out = validator.run(clean_out, analyst_out)
        results["validator"] = validator_out

        if not validator_out.retry_needed:
            break

        if validator_out.retry_agent == "Analyst":
            logger.log("Orchestrator", f"Retry {attempt+1}/{MAX_RETRIES}: Re-running Analyst...", "retry")
            analyst_out = analyst.run(df_clean, plan)
            results["analyst"] = analyst_out
        elif validator_out.retry_agent == "Cleaner":
            logger.log("Orchestrator", f"Retry {attempt+1}/{MAX_RETRIES}: Re-running Cleaner...", "retry")
            df_clean, clean_out = cleaner.run(df, plan)
            results["cleaner"] = clean_out

    # 5. Reporter
    report_out = reporter.run(plan, clean_out, analyst_out, validator_out)
    results["reporter"] = report_out

    logger.log("Orchestrator", "Swarm complete ✓", "success")
    return results


if __name__ == "__main__":
    # CLI test run
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/samples/sample.csv"
    goal = sys.argv[2] if len(sys.argv) > 2 else "Find key trends and anomalies in this dataset"

    df = pd.read_csv(csv_path)
    results = run_swarm(df, goal)
    print("\n=== FINAL REPORT ===")
    print(results["reporter"].model_dump_json(indent=2))
