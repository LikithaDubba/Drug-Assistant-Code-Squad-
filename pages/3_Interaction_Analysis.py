# frontend/pages/3_Interaction_Analysis.py
import streamlit as st
import requests

st.title("Drug Interaction Analysis")
drugs = st.text_area("List current medications (comma separated)", "Warfarin, Aspirin")
if st.button("Analyze"):
    drug_list = [d.strip() for d in drugs.split(",") if d.strip()]
    with st.spinner("Analyzing..."):
        resp = requests.post("http://127.0.0.1:8000/api/interactions", json={"drugs": drug_list})
    if resp.ok:
        out = resp.json()
        st.write("Interactions:")
        for i in out.get("interactions", []):
            st.write(f"- {i['drug1']} + {i['drug2']} → Severity: {i['severity']}. {i.get('notes')}")
        if out.get("contraindications"):
            st.warning("Contraindications found:")
            for c in out["contraindications"]:
                st.write(c)
    else:
        st.error(resp.text)