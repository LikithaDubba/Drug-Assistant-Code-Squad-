# frontend/pages/1_Home.py
import streamlit as st

st.set_page_config(page_title="Drug Assistant — Home", layout="wide")
st.title("Drug Assistant")
st.markdown("""
Welcome — choose a page from the left (Streamlit's pages menu) or the top to access:
- Drug Comparison
- Interaction Analysis
- Alternative Drug Suggestions
- Patient Profile
- Prescription Analyzer
- Precautions
- Antidote Mode (Emergency)
""")
st.info("This tool is for informational purposes only. Not a substitute for medical advice.")