import streamlit as st
import requests

st.set_page_config(page_title="SentinelAI Dashboard")

st.title("🛡 SentinelAI")

prompt = st.text_area("Enter prompt")

if st.button("Run Inference"):
    res = requests.post(
        "http://localhost:8000/infer/",
        json={"prompt": prompt}
    )
    st.write(res.json())
