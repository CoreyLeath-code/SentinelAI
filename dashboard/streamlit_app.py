import streamlit as st
import requests

st.title("SentinelAI Dashboard")

features = st.text_input("Enter comma-separated features")

if st.button("Predict"):
    response = requests.post(
        "http://localhost:8000/predict",
        json={"features": [float(x) for x in features.split(",")]}
    )
    st.write(response.json())
