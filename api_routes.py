# backend/app/api_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .model_loader import GraniteModel
from .utils import load_drug_db, find_alternatives, analyze_interactions, adjust_dosage, parse_prescription

router = APIRouter()
model = GraniteModel()  # loads on import (see model_loader)

# Simple request/response schemas
class PatientProfile(BaseModel):
    age: int
    weight_kg: Optional[float] = None
    allergies: Optional[List[str]] = []
    comorbidities: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []

class PrescriptionRequest(BaseModel):
    prescription_text: str
    patient: Optional[PatientProfile] = None

# Load data once
drug_db = load_drug_db()

@router.get("/drugs/search")
def search_drugs(q: str, limit: int = 10):
    results = [d for d in drug_db if q.lower() in d["name"].lower()]
    return results[:limit]

@router.post("/compare")
def drug_compare(name: str):
    # returns alternatives and a ranking
    alts = find_alternatives(name, drug_db)
    if not alts:
        raise HTTPException(status_code=404, detail="Drug not found or no alternatives.")
    return {"drug": name, "alternatives": alts}

@router.post("/interactions")
def interaction_analysis(drugs: List[str], patient: Optional[PatientProfile] = None):
    analysis = analyze_interactions(drugs, drug_db, patient)
    return analysis

@router.post("/alternatives_dosage")
def alternatives_and_dosage(name: str, patient: PatientProfile):
    alts = find_alternatives(name, drug_db)
    adjusted = [ {**a, "adjusted_dose": adjust_dosage(a, patient)} for a in alts ]
    return {"alternatives": adjusted}

@router.post("/prescription_analyze")
def prescription_analyze(req: PrescriptionRequest):
    parsed = parse_prescription(req.prescription_text)
    # pass parsed to model for deeper analysis / precautionary notes
    prompt = f"Analyze prescription and highlight contraindications, precautions and possible interactions:\nPrescription: {req.prescription_text}\nPatient: {req.patient}\nParsed: {parsed}"
    ai_out = model.ask(prompt, max_new_tokens=256)
    return {"parsed": parsed, "ai_analysis": ai_out}

@router.post("/antidote_mode")
def antidote_mode(drugs: List[str], patient: Optional[PatientProfile] = None):
    # For toxic combinations: build quick protocol
    analysis = analyze_interactions(drugs, drug_db, patient)
    # if major interaction severity -> generate emergency protocol
    severe = [i for i in analysis.get("interactions", []) if i["severity"] == "major"]
    if not severe:
        return {"message": "No major toxic combos detected.", "details": analysis}
    prompt = ("You are a medical summarization assistant. For the following emergency drug interaction(s), "
              "generate step-by-step reversal protocol, immediate first-aid, and standard antidotes if appropriate. "
              "Include recommended contacts (poison control) and what data to share:\n"
              f"{severe}\nPatient: {patient}")
    ai_out = model.ask(prompt, max_new_tokens=512)
    # NOTE: do NOT auto-place calls — return instructions and contact template
    contact_template = {
        "poison_control_number": "LOCAL_POISON_CONTROL_NUMBER",
        "message_to_send": f"Patient on {drugs}. {ai_out[:240]}..."
    }
    return {"severe_interactions": severe, "protocol": ai_out, "contact_template": contact_template}
