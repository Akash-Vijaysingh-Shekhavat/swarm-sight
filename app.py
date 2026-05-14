"""
SwarmSight UI — Streamlit app with live agent activity feed.
Run: streamlit run ui/app.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from main import run_swarm
from utils.logger import logger

# --- Page config ---
st.set_page_config(
    page_title="SwarmSight",
    page_icon="⚡",
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
<style>
.agent-log { font-family: monospace; font-size: 13px; padding: 6px 10px; border-radius: 6px; margin: 3px 0; }
.log-running  { background: #1e293b; color: #94a3b8; border-left: 3px solid #3b82f6; }
.log-success  { background: #14271f; color: #6ee7b7; border-left: 3px solid #10b981; }
.log-error    { background: #2d1515; color: #fca5a5; border-left: 3px solid #ef4444; }
.log-retry    { background: #2d1f0a; color: #fcd34d; border-left: 3px solid #f59e0b; }
.agent-tag    { font-weight: 700; margin-right: 6px; }
.metric-card  { text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("⚡ SwarmSight")
st.caption("Multi-Agent Data Analysis Engine — 5 AI agents working together")

col_left, col_right = st.columns([1, 1], gap="large")

# ===================== LEFT: Input Panel =====================
with col_left:
    st.subheader("1. Upload your data")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        df_raw = pd.read_csv(uploaded)
        st.success(f"Loaded: {len(df_raw)} rows × {len(df_raw.columns)} columns")
        with st.expander("Preview data"):
            st.dataframe(df_raw.head(5), use_container_width=True)

    st.subheader("2. Set your goal")
    user_goal = st.text_area(
        "What do you want to learn from this data?",
        placeholder="e.g. Find sales trends, identify anomalous customers, discover which features correlate with churn",
        height=100,
    )

    run_btn = st.button("🚀 Launch Swarm", type="primary", use_container_width=True)

# ===================== RIGHT: Agent Activity Feed =====================
with col_right:
    st.subheader("Agent Activity Feed")
    feed_placeholder = st.empty()

    AGENT_COLORS = {
        "Planner": "🧠",
        "Cleaner": "🧹",
        "Analyst": "📊",
        "Validator": "✅",
        "Reporter": "📝",
        "Orchestrator": "⚙️",
    }

    def render_feed(events):
        html = ""
        for e in events:
            icon = AGENT_COLORS.get(e["agent"], "•")
            css = f"log-{e['status']}"
            html += f'<div class="agent-log {css}"><span class="agent-tag">{icon} {e["agent"]}</span>{e["timestamp"]} — {e["message"]}</div>'
        feed_placeholder.markdown(html or "<p style='color:#94a3b8'>Waiting for swarm to start...</p>", unsafe_allow_html=True)

    render_feed([])

# ===================== Run the swarm =====================
if run_btn:
    if not uploaded:
        st.error("Please upload a CSV file first.")
    elif not user_goal.strip():
        st.error("Please enter a goal for the analysis.")
    else:
        with st.spinner("Swarm running..."):
            events_live = []

            def on_event(event):
                events_live.append(event)
                render_feed(events_live)

            results = run_swarm(df_raw, user_goal, log_callback=on_event)

        st.success("Swarm complete!")

        # ===================== Results =====================
        st.divider()
        st.subheader("📋 Final Report")

        report = results["reporter"]
        clean  = results["cleaner"]
        anal   = results["analyst"]

        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows cleaned", f"{clean.rows_after:,}", f"-{clean.duplicates_removed} dupes")
        m2.metric("Nulls fixed", clean.nulls_fixed)
        m3.metric("Key findings", len(anal.key_findings))
        m4.metric("Anomalies", len(anal.anomalies))

        st.markdown(f"**{report.title}**")
        st.markdown(report.executive_summary)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Key Insights**")
            for i, ins in enumerate(report.key_insights, 1):
                st.markdown(f"{i}. {ins}")
        with col_b:
            st.markdown("**Recommendations**")
            for r in report.recommendations:
                st.markdown(f"→ {r}")

        # Cleaned data download
        st.divider()
        csv_dl = results["cleaned_df"].to_csv(index=False)
        st.download_button("⬇ Download Cleaned Data", csv_dl, "cleaned_data.csv", "text/csv")

        # Chart: null distribution before/after
        if not results["cleaned_df"].empty:
            null_before = df_raw.isnull().sum()
            null_before = null_before[null_before > 0]
            if not null_before.empty:
                fig = px.bar(
                    x=null_before.index, y=null_before.values,
                    labels={"x": "Column", "y": "Nulls before cleaning"},
                    title="Nulls fixed per column",
                    color_discrete_sequence=["#3b82f6"]
                )
                st.plotly_chart(fig, use_container_width=True)
