import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import random

# App Configuration
st.set_page_config(page_title="SentinelAI Threat Center", page_icon="🛡️", layout="wide")

st.title("🛡️ SentinelAI: Autonomous Security Operations & Threat Intelligence")
st.caption("Enterprise Demo Environment | Intelligent Perimeter Guard & Predictive Mitigation")

# Initialize session state for system alert history
if "security_alerts" not in st.session_state:
    st.session_state.security_alerts = []
if "system_status" not in st.session_state:
    st.session_state.system_status = "SECURE"

# --- SIDEBAR: ATTACK SURFACE SIMULATOR ---
st.sidebar.header("🕹️ Breach & Attack Simulation (BAS)")
st.sidebar.markdown("Simulate malicious vector payloads to evaluate SentinelAI's neural triage response.")

attack_vector = st.sidebar.selectbox(
    "Select Attack Vector", 
    ["Distributed Denial of Service (DDoS)", "Credential Stuffing", "SQL Injection (SQLi)", "Phishing Exfiltration Burst"]
)
target_zone = st.sidebar.selectbox("Target Infrastructure Zone", ["DMZ-Public-Ingress", "Internal-Database-Cluster", "IAM-Auth-Gateway"])
severity_slider = st.sidebar.slider("Attack Volume / Intensity (Req/sec)", 100, 5000, 1200)

trigger_event = st.sidebar.button("💥 Launch Threat Payload")

# --- CORE INFERENCE & AUTOMATED RESPONSE SIMULATION ---
def process_threat_vector(vector, zone, intensity):
    """
    Simulates SentinelAI's core heuristics and predictive modeling layer, returning
    an algorithmic risk score and a dynamic firewall orchestration directive.
    """
    # Calculate base risk mathematically
    base_risk = (intensity / 5000) * 100
    if zone == "Internal-Database-Cluster":
        base_risk += 15  # Critical asset weight modifier
        
    risk_score = min(float(np.clip(base_risk + random.uniform(-10, 10), 0, 100)), 100.0)
    
    # Classify State and Action
    if risk_score >= 75:
        status = "CRITICAL"
        action = "Orchestrated absolute Zone Isolation; IPs blackholed at edge router via BGP Flowspec."
    elif risk_score >= 40:
        status = "WARNING"
        action = "Rate-limiting applied (mTLS enforced, CAPTCHA challenge injected into gateway layer)."
    else:
        status = "LOW"
        action = "Logged threat sign; verified integrity hashes across local storage vectors."
        
    return risk_score, status, action

# Inject simulated event on button click or random polling interval
if trigger_event:
    score, status, mitigation = process_threat_vector(attack_vector, target_zone, severity_slider)
    
    alert_payload = {
        "Timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "Attack Vector": attack_vector,
        "Target Asset": target_zone,
        "Risk Score (%)": score,
        "Triage Status": status,
        "Automated Mitigation Protocol": mitigation
    }
    st.session_state.security_alerts.insert(0, alert_payload)
    
    # Dynamically scale global system health state
    if status == "CRITICAL":
        st.session_state.system_status = "BREACH_ATTEMPT_DETECTED"
    elif status == "WARNING" and st.session_state.system_status != "BREACH_ATTEMPT_DETECTED":
        st.session_state.system_status = "ELEVATED_RISK"

# --- MAIN DASHBOARD INTERFACE ---
col_status, col_health, col_network = st.columns(3)
with col_status:
    if st.session_state.system_status == "SECURE":
        st.success("🟢 System Defense Matrix: NOMINAL")
    elif st.session_state.system_status == "ELEVATED_RISK":
        st.warning("🟡 System Defense Matrix: ELEVATED RISK")
    else:
        st.error("🔴 System Defense Matrix: ACTIVE TARGET")

with col_health:
    base_health = 100 - len([a for a in st.session_state.security_alerts if a["Triage Status"] == "CRITICAL"]) * 8
    st.metric("Global Perimeter Integrity", f"{max(base_health, 24)}%")

with col_network:
    st.metric("AI Inference Engine Latency", f"{random.uniform(1.2, 4.8):.2f} ms", delta="Sub-5ms SLA Met")

st.markdown("---")

# Render historical ledger of alerts
if st.session_state.security_alerts:
    st.subheader("🚨 Threat Triage Ingestion Stream")
    df_alerts = pd.DataFrame(st.session_state.security_alerts)
    
    # Layout rendering utilizing conditional row highlights
    def highlight_threats(val):
        if val == "CRITICAL": return "background-color: rgba(255, 75, 75, 0.25); color: #ff4b4b; font-weight: bold;"
        if val == "WARNING": return "background-color: rgba(255, 165, 0, 0.2); color: #ffa500;"
        return "background-color: rgba(0, 255, 0, 0.05); color: #00ff00;"

    styled_df = df_alerts.style.map(highlight_threats, subset=["Triage Status"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Risk analytics section
    st.subheader("📊 Analytical Threat Risk Vectors")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Risk Score Trajectory**")
        st.line_chart(df_alerts["Risk Score (%)"])
    with c2:
        st.markdown("**Target Distribution Map**")
        st.bar_chart(df_alerts["Target Asset"].value_counts())
else:
    st.info("No active security threats detected inside the perimeter interface loops. Use the Breach & Attack Simulator sidebar panel to launch a targeted vector payload.")
