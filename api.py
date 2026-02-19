# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from logic import calculate_coins, calculate_risk_score
from db import create_table, insert_simulation

# Create DB table at startup
create_table()

app = FastAPI(title="CRED Rewards Optimizer API")

# ✅ Request model
class RewardRequest(BaseModel):
    amount: float
    cibil: int
    streak: int
    fraud: bool = False
    days_late: int = 0

# ✅ Response model
class RewardResponse(BaseModel):
    coins: float
    risk_score: float
    explanation: str

# 🔍 Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 🎯 Predict rewards
@app.post("/predict", response_model=RewardResponse)
def predict_reward(data: RewardRequest):
    coins, explanation = calculate_coins(
        data.amount,
        data.cibil,
        data.streak,
        data.fraud
    )

    risk_score = calculate_risk_score(
        data.cibil,
        data.days_late
    )

    # ✅ Save to database
    insert_simulation(
        data.amount,
        data.cibil,
        data.streak,
        data.fraud,
        coins,
        risk_score
    )

    return {
        "coins": coins,
        "risk_score": risk_score,
        "explanation": explanation
    }

# 🔁 Simulation endpoint
@app.post("/simulate", response_model=RewardResponse)
def simulate_reward(data: RewardRequest):
    coins, explanation = calculate_coins(
        data.amount,
        data.cibil,
        data.streak,
        data.fraud
    )

    risk_score = calculate_risk_score(
        data.cibil,
        data.days_late
    )

    # ✅ Save to database
    insert_simulation(
        data.amount,
        data.cibil,
        data.streak,
        data.fraud,
        coins,
        risk_score
    )

    return {
        "coins": coins,
        "risk_score": risk_score,
        "explanation": explanation
    }
