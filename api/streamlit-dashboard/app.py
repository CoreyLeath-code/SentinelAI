import streamlit as st

st.set_page_config(
    page_title="SentinelAI Control Plane",
    layout="wide"
)

st.title("SentinelAI — AI Reliability Control Plane")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Overview", "Model Drift", "LLM Monitoring", "System Metrics"]
)

if page == "Overview":
    st.subheader("System Overview")
    st.write("SentinelAI monitors AI systems for drift, anomalies, and LLM risks.")

elif page == "Model Drift":
    st.subheader("Model Drift Dashboard")
    st.metric("PSI Score", "0.08")
    st.metric("KS Statistic", "0.12")
    st.warning("Drift within acceptable threshold.")

elif page == "LLM Monitoring":
    st.subheader("LLM Monitoring")
    st.metric("Hallucination Risk", "Low")
    st.metric("Average Token Usage", "512 tokens")

elif page == "System Metrics":
    st.subheader("Infrastructure Metrics")
    st.metric("P95 Latency", "220ms")
    st.metric("Throughput", "120 RPS")
