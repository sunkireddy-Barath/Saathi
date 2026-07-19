from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from .model import HybridDemandForecaster
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
    if not os.path.exists("models/xgboost_forecaster.pkl"):
        print("Model not found. Triggering training on startup...")
        if not os.path.exists("data/historical_sales.csv"):
            from .generate_data import generate_historical_sales
            generate_historical_sales()
        forecaster.train()
    else:
        forecaster.load_model()

@app.post("/predict", response_model=PredictionResponse)
async def predict_demand(req: PredictionRequest):
    try:
        # Generate 30 day forecast
        raw_predictions = forecaster.predict_next_n_days(category=req.category, n_days=30)
        
        # Format response
        forecast_array = [{"day": i+1, "predicted_demand": val} for i, val in enumerate(raw_predictions)]
        
        # Determine best window (highest continuous demand)
        best_day = raw_predictions.index(max(raw_predictions)) + 1
        
        # Simple heuristic rule for recommendation
        avg_demand = sum(raw_predictions) / len(raw_predictions)
        if avg_demand > 20:
            rec = "High demand expected. Stock up raw materials immediately."
        else:
            rec = "Stable demand. Maintain current inventory levels."
            
        return PredictionResponse(
            product_id=req.product_id,
            forecast_data=forecast_array,
            confidence_score=0.85, # Mock confidence for now
            best_selling_window=f"Peak around Day {best_day}",
            recommendation=rec
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
