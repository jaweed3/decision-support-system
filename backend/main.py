from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import pandas as pd

from database import get_db, engine, Base
from models import Laptop
from topsis import calculate_topsis
from ai_service import ai_service

app = FastAPI(title="NEON-DECISION API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # In a real app, you'd use migrations (Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to NEON-DECISION AI API"}

@app.get("/laptops", response_model=List[dict])
async def get_laptops(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Laptop).limit(100))
    laptops = result.scalars().all()
    return [
        {
            "id": l.id,
            "model_name": l.model_name,
            "brand": l.brand,
            "price": l.price,
            "ram_gb": l.ram_gb,
            "ssd_gb": l.ssd_gb,
            "spec_score": l.spec_score,
            "no_of_cores": l.no_of_cores,
            "used_price": l.used_price
        } for l in laptops
    ]

@app.post("/recommend")
async def recommend(
    weights: List[float], 
    budget: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    # Fetch data
    result = await db.execute(select(Laptop))
    laptops = result.scalars().all()
    
    data = [
        {
            "id": l.id,
            "model_name": l.model_name,
            "brand": l.brand,
            "price": l.price,
            "ram_gb": l.ram_gb,
            "ssd_gb": l.ssd_gb,
            "spec_score": l.spec_score,
            "no_of_cores": l.no_of_cores,
            "used_price": l.used_price
        } for l in laptops
    ]
    
    if not data:
        raise HTTPException(status_code=404, detail="No laptops found in database")

    # Filter by budget if provided
    if budget:
        data = [d for d in data if d["price"] <= budget]

    if not data:
         raise HTTPException(status_code=404, detail="No laptops match your budget")

    # criteria: price, ram, ssd, spec_score, cores
    criteria = ["price", "ram_gb", "ssd_gb", "spec_score", "no_of_cores"]
    # price is cost (False), others are benefit (True)
    benefit = [False, True, True, True, True]
    
    ranked_df = calculate_topsis(data, criteria, weights, benefit)
    
    return ranked_df.to_dict(orient="records")

@app.post("/consult")
async def consult(query: str, db: AsyncSession = Depends(get_db)):
    # 1. AI Extracts requirements
    reqs = await ai_service.extract_requirements(query)
    
    # Default weights if extraction fails or is partial
    # Order: Price, RAM, SSD, Spec, Cores
    weights = [0.3, 0.25, 0.2, 0.15, 0.1]
    
    budget = reqs.get("budget_max") if reqs else None
    
    # 2. Run Recommendations
    recommendations = await recommend(weights, budget, db)
    
    if not recommendations:
        return {"error": "No laptops found matching your criteria"}
        
    best_match = recommendations[0]
    
    # 3. AI generates summary
    summary = await ai_service.get_recommendation_summary(best_match, query)
    
    return {
        "requirements": reqs,
        "recommendations": recommendations[:10], # Top 10
        "ai_summary": summary
    }
