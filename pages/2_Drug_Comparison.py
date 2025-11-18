# frontend/pages/2_Drug_Comparison.py
import streamlit as st
import requests

st.title("Drug Comparison")
drug = st.text_input("Enter drug name", value="Warfarin")
if st.button("Compare"):
    with st.spinner("Querying backend..."):
        resp = requests.post("http://127.0.0.1:8000/api/compare", params={"name": drug})
    if resp.ok:
        data = resp.json()
        st.subheader(f"Alternatives for {data['drug']}")
        for a in data["alternatives"]:
            st.write(f"- {a['name']} ({a.get('dose_mg') or 'n/a'} mg) — Notes: {a.get('notes')}")
    else:
        st.error(resp.text)