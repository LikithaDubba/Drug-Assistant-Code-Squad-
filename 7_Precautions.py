import streamlit as st
import requests

st.title("Precautions & Safety Guidance")

st.write("Enter any drug (or multiple drugs) to get detailed precautions, warnings, and patient-specific safety advice.")

drugs = st.text_input("Drug(s)", "Warfarin, Aspirin")

patient = st.session_state.get("patient", None)

if st.button("Get Precautions"):
    drug_list = [d.strip() for d in drugs.split(",") if d.strip()]

    payload = {
        "drugs": drug_list,
        "patient": patient
    }

    with st.spinner("Retrieving safety guidance..."):
        resp = requests.post(
            "http://127.0.0.1:8000/api/interactions",
            json=payload
        )

    if resp.ok:
        data = resp.json()

        st.subheader("Interaction Warnings")
        for i in data.get("interactions", []):
            st.error(f"{i['drug1']} + {i['drug2']} — Severity: {i['severity']}\nNotes: {i.get('notes')}")

        if data.get("contraindications"):
            st.warning("Contraindications Found")
            st.json(data["contraindications"])
        else:
            st.success("No contraindications found!")

        # You can also add an AI-based summary:
        if data.get("interactions"):
            st.subheader("AI Precaution Summary")

            ai_req = {
                "prescription_text": ", ".join(drug_list),
                "patient": patient
            }

            ai_resp = requests.post("http://127.0.0.1:8000/api/prescription_analyze", json=ai_req)

            if ai_resp.ok:
                st.write(ai_resp.json()["ai_analysis"])
    else:
        st.error(resp.text)
