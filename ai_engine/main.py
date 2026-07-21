from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from model import HybridDemandForecaster
import os

app = FastAPI(title="Saathi AI Engine", description="Hybrid Demand Forecasting API")
forecaster = HybridDemandForecaster()

class PredictionRequest(BaseModel):
    product_id: str
    category: str # e.g. Silk, Cotton, Wool

class PredictionResponse(BaseModel):
    product_id: str
    forecast_data: List[Dict[str, Any]] # daily predictions
    confidence_score: float
    best_selling_window: str
    recommendation: str

@app.on_event("startup")
async def startup_event():
    # Attempt to load or train model on startup
    if not os.path.exists("models/hybrid_forecaster.pkl"):
        print("Model not found. Triggering training on startup...")
        if not os.path.exists("data/historical_sales.csv"):
            from generate_data import generate_historical_sales
            generate_historical_sales()
        forecaster.train()
    else:
        forecaster.load_model()

@app.post("/predict")
async def predict_demand(req: PredictionRequest):
    try:
        # Generate 30 day forecast and get real confidence score
        raw_predictions, confidence_score = forecaster.predict_next_n_days(category=req.category, n_days=30)
        
        # Format response
        forecast_array = {"days": list(range(1, 31)), "demand": raw_predictions}
        
        # Determine best and worst window
        best_day = raw_predictions.index(max(raw_predictions)) + 1
        worst_day = raw_predictions.index(min(raw_predictions)) + 1
        
        expected_demand_units = sum(raw_predictions)
        
        # Simple heuristic rule for recommendation
        avg_demand = expected_demand_units / len(raw_predictions)
        
        if avg_demand > 20:
            rec_action = "increase_stock"
            rec_reason = "Strong macro-trends and micro-fads point to high upcoming demand."
            comp_level = "High"
        else:
            rec_action = "maintain_stock"
            rec_reason = "Stable baseline demand predicted without significant viral fads."
            comp_level = "Medium"
            
        # The expected revenue requires price which isn't in this request, but the backend handles it.
        # So we just pass back what we can.
            
        return {
            "product_id": req.product_id,
            "forecast_data": forecast_array,
            "confidence_score": round(confidence_score, 2),
            "best_selling_window": f"Days {max(1, best_day-2)}-{min(30, best_day+2)}",
            "worst_selling_window": f"Days {max(1, worst_day-2)}-{min(30, worst_day+2)}",
            "expected_demand_units": expected_demand_units,
            "competition_level": comp_level,
            "recommendation": {"action": rec_action, "reason": rec_reason},
            "model_version": "sequential_residual_v2"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
