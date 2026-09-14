"""
Prediction utilities for the California House Price Prediction project.
"""

from pathlib import Path

import joblib
import pandas as pd

from src.feature_engineering import engineer_features


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "house_price_model.joblib"
)


def load_model(model_path: str | Path = MODEL_PATH):
    """
    Load the trained Random Forest model.

    Parameters
    ----------
    model_path : str or Path
        Path to the saved model.

    Returns
    -------
    RandomForestRegressor
        Loaded trained model.
    """
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Saved model not found at: {model_path}"
        )

    return joblib.load(model_path)


def predict_house_price(
    input_data: dict,
    model=None,
) -> float:
    """
    Predict the median house value for a single input.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the 13 model features.
    model : optional
        Trained model. If not provided, the saved model is loaded.

    Returns
    -------
    float
        Predicted median house value.
    """
    if model is None:
        model = load_model()

    input_df = pd.DataFrame([input_data])

    input_df = engineer_features(input_df)

    prediction = model.predict(input_df)[0]

    return float(prediction)


if __name__ == "__main__":
    sample_house = {
        "Median_Income": 5.0,
        "Median_Age": 30.0,
        "Tot_Rooms": 2000.0,
        "Tot_Bedrooms": 400.0,
        "Population": 1000.0,
        "Households": 350.0,
        "Latitude": 34.0,
        "Longitude": -118.0,
        "Distance_to_coast": 10.0,
        "Distance_to_LA": 20.0,
        "Distance_to_SanDiego": 150.0,
        "Distance_to_SanJose": 500.0,
        "Distance_to_SanFrancisco": 550.0,
    }

    predicted_price = predict_house_price(sample_house)

    print("Prediction generated successfully!")
    print(f"Predicted House Value: ${predicted_price:,.2f}")