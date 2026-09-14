"""
FastAPI backend for the California House Price Prediction project.

This API receives house features from the frontend,
passes them to the trained Random Forest model,
and returns the predicted house value.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.predict import predict_house_price


app = FastAPI(
    title="California House Price Prediction API",
    description="API for predicting California house values using a trained Random Forest model.",
    version="1.0.0",
)


# Allow the React frontend to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HouseFeatures(BaseModel):
    """Input features required for house price prediction."""

    Median_Income: float
    Median_Age: float
    Tot_Rooms: float
    Tot_Bedrooms: float
    Population: float
    Households: float
    Latitude: float
    Longitude: float
    Distance_to_coast: float
    Distance_to_LA: float
    Distance_to_SanDiego: float
    Distance_to_SanJose: float
    Distance_to_SanFrancisco: float


@app.get("/")
def root():
    """Return a basic API status message."""
    return {
        "message": "California House Price Prediction API is running.",
        "status": "success",
    }


@app.get("/health")
def health_check():
    """Check whether the API is healthy."""
    return {
        "status": "healthy",
    }


@app.post("/predict")
def predict(features: HouseFeatures):
    """Predict the median house value from the supplied features."""

    input_data = features.model_dump()

    predicted_price = predict_house_price(input_data)

    return {
        "predicted_house_value": round(predicted_price, 2),
        "currency": "USD",
    }