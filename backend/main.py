from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User, Lead, Project
from schemas import LeadCreate, ProjectCalculation
import openai
import os

app = FastAPI(title="Telegram CRM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/leads/")
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    return {"id": db_lead.id, "status": "created"}

@app.post("/calculate/")
def calculate_project(calc: ProjectCalculation):
    # AI оценка сложности проекта
    complexity = estimate_complexity(calc.description, calc.features)
    hours = complexity * 10  # базовая формула
    price = hours * 2500
    
    return {
        "complexity": complexity,
        "estimated_hours": hours,
        "price": price,
        "hourly_rate": 2500
    }

def estimate_complexity(description: str, features: list) -> int:
    # Простая логика оценки (позже заменим на AI)
    base_complexity = len(features)
    if "AI" in description.upper():
        base_complexity += 3
    if "мобильное" in description.lower():
        base_complexity += 2
    return min(base_complexity, 10)

@app.get("/leads/")
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)