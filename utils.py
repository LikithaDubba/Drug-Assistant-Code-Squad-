# backend/app/utils.py
import csv
from typing import List, Dict

def load_drug_db(path="backend/app/data/drugs.csv"):
    db = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            # expect fields: id,name,class,dose_mg,renally_adjust,notes
            db.append(r)
    return db

def find_alternatives(name: str, db: List[Dict]):
    # naive: find same class alternatives
    target = next((d for d in db if d["name"].lower() == name.lower()), None)
    if not target:
        return []
    same_class = [d for d in db if d["class"] == target["class"] and d["name"] != target["name"]]
    return same_class

def analyze_interactions(drugs: List[str], db: List[Dict], patient=None):
    # placeholder: load interactions CSV with columns drug1,drug2,severity,notes
    interactions = []
    with open("backend/app/data/interactions.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["drug1"].lower() in [d.lower() for d in drugs] and r["drug2"].lower() in [d.lower() for d in drugs]:
                interactions.append({"drug1": r["drug1"], "drug2": r["drug2"], "severity": r["severity"], "notes": r.get("notes","")})
    # Also flag simple contraindications like pregnancy/renalfailure if found in patient.comorbidities
    contraindications = []
    if patient and patient.get("comorbidities"):
        for d in drugs:
            for com in patient["comorbidities"]:
                # very naive:
                if "renal" in com.lower() and db and next((x for x in db if x["name"].lower()==d.lower() and x.get("renally_adjust")=="yes"), None):
                    contraindications.append({"drug":d, "issue":"requires renal adjustment"})
    return {"interactions": interactions, "contraindications": contraindications}

def adjust_dosage(drug_entry: Dict, patient):
    # naive adjustment rules
    base = float(drug_entry.get("dose_mg") or 0)
    age = patient.get("age", 30)
    weight = patient.get("weight_kg") or 70
    # example: reduce by 20% if age > 75
    adj = base
    if age > 75:
        adj *= 0.8
    # pediatric: scale by weight for children < 16
    if age < 16:
        adj = base * (weight / 70)
    # if renal impairment flagged in comorbidities
    if any("renal" in c.lower() for c in (patient.get("comorbidities") or [])):
        adj *= 0.7
    return round(adj, 2)

def parse_prescription(text: str):
    # super naive text parse: split lines and look for drug names and doses
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    parsed = []
    for l in lines:
        parts = l.split()
        # look for numeric token as dose
        dose = next((p for p in parts if any(ch.isdigit() for ch in p)), None)
        name = parts[0] if parts else l
        parsed.append({"raw": l, "name": name, "dose_token": dose})
    return parsed