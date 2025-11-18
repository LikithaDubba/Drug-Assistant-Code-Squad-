import streamlit as st
import requests

st.title("Alternative Drugs & Dosage Adjustment")

st.write("Enter a drug and patient details to get safer alternatives with adjusted dosage.")

drug = st.text_input("Drug Name", "Metformin")

st.subheader("Patient Details")
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=70.0)
allergies = st.text_input("Allergies (comma separated)", "")
comorbidities = st.text_input("Comorbidities (comma separated)", "")

if st.button("Get Alternatives & Adjusted Dosage"):
    payload = {
        "name": drug,
        "patient": {
            "age": age,
            "weight_kg": weight,
            "allergies": [a.strip() for a in allergies.split(",") if a.strip()],
            "comorbidities": [c.strip() for c in comorbidities.split(",") if c.strip()],
        }
    }
    
    with st.spinner("Contacting backend..."):
        resp = requests.post("http://127.0.0.1:8000/api/alternatives_dosage", json=payload)

    if resp.ok:
        data = resp.json()
        st.subheader("Suggestions")
        
        for alt in data["alternatives"]:
            st.write(f"""
                **{alt['name']}**  
                - Base Dose: {alt.get('dose_mg')} mg  
                - Adjusted Dose: **{alt['adjusted_dose']} mg**  
                - Notes: {alt.get('notes')}
            """)
    else:
        st.error(resp.text)