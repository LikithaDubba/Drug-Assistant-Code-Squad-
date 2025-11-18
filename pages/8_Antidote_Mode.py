# frontend/pages/8_Antidote_Mode.py
import streamlit as st
import requests

st.set_page_config(page_title="Antidote Mode")
st.title("Antidote Mode — Emergency Guidance")
st.markdown("If a major toxic combo is detected this page generates a stepwise protocol and a contact template for poison control.")

drugs = st.text_input("Drugs involved (comma separated)", "Warfarin, Ibuprofen")
if st.button("Generate Emergency Protocol"):
    drug_list = [d.strip() for d in drugs.split(",") if d.strip()]
    with st.spinner("Generating..."):
        resp = requests.post("http://127.0.0.1:8000/api/antidote_mode", json={"drugs": drug_list})
    if resp.ok:
        out = resp.json()
        if out.get("severe_interactions"):
            st.error("Major interaction(s) detected — follow protocol below immediately.")
            st.subheader("Protocol")
            st.write(out["protocol"])
            st.subheader("Contact Template (use to call poison control)")
            st.json(out["contact_template"])
        else:
            st.success(out.get("message"))
    else:
        st.error(resp.text)