"""
SentinelAI — Streamlit control plane dashboard.

Reads data from Postgres (when WAREHOUSE_MODE=postgres) or shows
demo data when the database is unavailable.
"""
import os
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import psycopg2
import psycopg2.extras
import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SentinelAI Dashboard",
    page_icon="🛡️",
    layout="wide",
)

DATABASE_URL   = os.getenv("DATABASE_URL", "")
WAREHOUSE_MODE = os.getenv("WAREHOUSE_MODE", "postgres")
INGESTION_URL  = os.getenv("INGESTION_URL", "http://ingestion-service:8080")
DRIFT_URL      = os.getenv("DRIFT_ENGINE_URL", "http://drift-engine:7070")
LLM_URL        = os.getenv("LLM_GUARD_URL", "http://llm-guard:8000")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@st.cache_resource
def get_connection():
    if WAREHOUSE_MODE != "postgres" or not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        return conn
    except Exception:
        return None


def query_df(sql: str, params=None) -> pd.DataFrame:
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        conn.autocommit = True
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            if not rows:
                return pd.DataFrame()
            return pd.DataFrame(rows, columns=[d[0] for d in cur.description])
    except Exception as exc:
        st.warning(f"Query error: {exc}")
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🛡️ SentinelAI — Control Plane")
st.caption(f"Warehouse: **{WAREHOUSE_MODE}** · refreshed at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")

# Auto-refresh toggle
col_refresh, col_interval, _ = st.columns([1, 1, 6])
with col_refresh:
    auto_refresh = st.checkbox("Auto-refresh", value=False)
with col_interval:
    refresh_interval = st.selectbox("Every", [10, 30, 60], index=1, label_visibility="collapsed")

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📥 Inference Logs", "📊 Drift Scores", "🚨 Incidents", "⚙️ Services"]
)

# ── Inference Logs ──────────────────────────────────────────────────────────
with tab1:
    st.subheader("Recent Inference Logs")
    df = query_df(
        "SELECT id, model_id, model_version, latency_ms, tokens_in, tokens_out, status, created_at "
        "FROM inference_logs ORDER BY created_at DESC LIMIT 100"
    )
    if df.empty:
        st.info("No inference logs yet. Post to `/log` on the ingestion service to populate this table.")
        st.code(
            'curl -X POST http://localhost:8080/log \\\n'
            '  -H "Content-Type: application/json" \\\n'
            '  -d \'{"model_id":"demo","latency_ms":120,"status":"ok"}\'',
            language="bash",
        )
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total logs", len(df))
        col2.metric("Avg latency (ms)", round(df["latency_ms"].mean(), 1) if "latency_ms" in df else "—")
        col3.metric("Error rate", f"{(df['status'] != 'ok').mean() * 100:.1f}%" if "status" in df else "—")
        st.dataframe(df, use_container_width=True)

# ── Drift Scores ─────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Drift Scores")
    df = query_df(
        "SELECT model_id, feature_name, psi, ks_stat, drift_detected, computed_at "
        "FROM drift_scores ORDER BY computed_at DESC LIMIT 200"
    )
    if df.empty:
        st.info("No drift scores yet. POST to `/drift` on the drift-engine service.")
        st.code(
            'curl -X POST http://localhost:7070/drift \\\n'
            '  -H "Content-Type: application/json" \\\n'
            '  -d \'{"model_id":"demo","feature_name":"latency","expected":[0.2,0.3,0.25,0.25],"actual":[0.1,0.35,0.30,0.25]}\'',
            language="bash",
        )
    else:
        drift_count = int(df["drift_detected"].sum()) if "drift_detected" in df else 0
        st.metric("Drift events", drift_count)
        st.dataframe(df, use_container_width=True)

# ── Incidents ────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Incidents")
    df = query_df(
        "SELECT i.id, i.type, i.severity, i.resolved, i.created_at, s.summary "
        "FROM incidents i "
        "LEFT JOIN incident_summaries s ON s.incident_id = i.id "
        "ORDER BY i.created_at DESC LIMIT 100"
    )
    if df.empty:
        st.info("No incidents recorded yet.")
    else:
        open_count = int((~df["resolved"]).sum()) if "resolved" in df else 0
        st.metric("Open incidents", open_count)
        st.dataframe(df, use_container_width=True)

# ── Services ─────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Service Health")
    import requests as req

    services = {
        "ingestion-service": f"{INGESTION_URL}/health",
        "drift-engine":      f"{DRIFT_URL}/health",
        "llm-guard":         f"{LLM_URL}/health",
    }

    cols = st.columns(len(services))
    for col, (name, url) in zip(cols, services.items()):
        try:
            r = req.get(url, timeout=3)
            status = "🟢 Healthy" if r.status_code == 200 else f"🔴 {r.status_code}"
        except Exception as exc:
            status = f"🔴 Unreachable"
        col.metric(name, status)

    st.caption("Prometheus: http://localhost:9090 · Grafana: http://localhost:3000")
