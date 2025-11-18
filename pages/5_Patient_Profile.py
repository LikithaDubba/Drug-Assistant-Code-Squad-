import streamlit as st

st.title("Patient Profile")

st.write("Enter patient information. This will be used across all features.")

# Initialize session state
if "patient" not in st.session_state:
    st.session_state.patient = {}

age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=60.0)
allergies = st.text_input("Allergies (comma separated)")
comorbidities = st.text_input("Comorbidities (comma separated)")
current_medications = st.text_input("Current Medications (comma separated)")

if st.button("Save Profile"):
    st.session_state.patient = {
        "age": age,
        "weight_kg": weight,
        "allergies": [a.strip() for a in allergies.split(",") if a.strip()],
        "comorbidities": [c.strip() for c in comorbidities.split(",") if c.strip()],
        "current_medications": [m.strip() for m in current_medications.split(",") if m.strip()]
    }
    st.success("Patient profile saved!")

if st.session_state.patient:
    st.subheader("Current Patient Profile")
    st.json(st.session_state.patient)