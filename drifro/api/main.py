# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# Import modules
from data_ingestion import satellite, climate, social_media
from models import cnn_model, nlp_model, forecast, optimization

import pandas as pd
import torch

app = FastAPI(title="DRIFRO API")

# Pydantic models for request validation.
class Location(BaseModel):
    lat: float
    lon: float

class City(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the DRIFRO API"}

# api/main.py (updated snippet)
@app.post("/satellite/")
def analyze_satellite(location: Location):
    try:
        # Fetch satellite image
        img = satellite.get_satellite_image(location.lat, location.lon)
        
        # Preprocess and predict
        input_tensor = cnn_model.preprocess_image(img).unsqueeze(0)
        model = cnn_model.SimpleCNN()
        model.load_state_dict(torch.load("models/cnn_model.py"))  # Load trained weights
        model.eval()
        with torch.no_grad():
            output = model(input_tensor)
        
        # Convert prediction to class label
        prediction = output.argmax().item()
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Satellite analysis failed: {str(e)}")

@app.get("/climate/")  # For climate data retrieval
def get_weather(city: str = "New York"):
    try:
        data = climate.get_climate_data(city)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/social/")  # For social media data analysis
def analyze_social(keyword: str = "flood"):
    try:
        tweets = social_media.get_tweets(keyword=keyword)
        sentiments = [nlp_model.get_sentiment(tweet) for tweet in tweets]
        return {"tweets": tweets, "sentiments": sentiments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast/")  # For disaster forecasting
def forecast_endpoint():
    try:
        df = pd.DataFrame({
            'ds': pd.date_range(start='2023-01-01', periods=100, freq='H'),
            'y': [i * 0.5 for i in range(100)]
        })
        forecast_df = forecast.forecast_disaster(df)
        result = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(24).to_dict(orient="records")
        return {"forecast": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/optimize/")  # For resource optimization
def optimize_resources():
    try:
        demand = {"zone1": 10, "zone2": 5, "zone3": 8}
        available = 15
        allocations = optimization.allocate_resources(demand, available)
        return {"allocations": allocations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
