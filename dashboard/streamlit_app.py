import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="SentinelAI Dashboard", layout="wide")

st.title("🚨 SentinelAI - Real-Time Monitoring Dashboard")

# Simulated metrics
latency = np.random.randint(50, 150)
throughput = np.random.randint(800, 1200)
error_rate = np.random.uniform(0, 5)

# Metrics Row
col1, col2, col3 = st.columns(3)

col1.metric("Latency (ms)", latency)
col2.metric("Throughput (req/sec)", throughput)
col3.metric("Error Rate (%)", round(error_rate, 2))

st.markdown("---")

# Simulated anomaly detection
st.subheader("🔍 Anomaly Detection")

data = np.random.randn(100)
df = pd.DataFrame(data, columns=["Signal"])

st.line_chart(df)

if abs(data[-1]) > 2:
    st.error("⚠️ Anomaly Detected!")
else:
    st.success("✅ System Stable")

# Logs
st.subheader("📜 Recent Logs")

logs = [f"Event {i}: Status OK" for i in range(5)]
for log in logs:
    st.text(log)

# Refresh simulation
time.sleep(1)
st.experimental_rerun()
