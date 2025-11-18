class PatientProfile(BaseModel):
    age: int
    weight_kg: Optional[float] = None
    allergies: Optional[List[str]] = []
    comorbidities: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []