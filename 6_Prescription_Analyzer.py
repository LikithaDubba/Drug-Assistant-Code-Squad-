import streamlit as st
import requests
import json

st.title("Prescription Analyzer")

st.write("Paste your prescription below. The system will extract drugs, doses, warnings, and AI analysis.")

prescription_text = st.text_area("Prescription Text", height=200)

# Get patient profile if saved
patient = st.session_state.get("patient", None)

if st.button("Analyze Prescription"):
    payload = {
        "prescription_text": prescription_text,
        "patient": patient
    }

    with st.spinner("Analyzing prescription..."):
        resp = requests.post(
            "http://127.0.0.1:8000/api/prescription_analyze",
            json=payload
        )

    if resp.ok:
        out = resp.json()

        st.subheader("Extracted Prescription Data")
        st.json(out["parsed"])

        st.subheader("AI Clinical Analysis")
        st.write(out["ai_analysis"])
    else:
        st.error(resp.text)