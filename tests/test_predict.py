"""
Tests for the prediction module.
"""

import pytest

from src.predict import load_model, predict_house_price


SAMPLE_HOUSE = {
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


def test_model_loads_successfully():
    """Verify that the saved Random Forest model can be loaded."""
    model = load_model()

    assert model is not None
    assert model.__class__.__name__ == "RandomForestRegressor"


def test_prediction_returns_float():
    """Verify that prediction returns a floating-point value."""
    prediction = predict_house_price(SAMPLE_HOUSE)

    assert isinstance(prediction, float)


def test_prediction_is_positive():
    """Verify that the predicted house value is positive."""
    prediction = predict_house_price(SAMPLE_HOUSE)

    assert prediction > 0


def test_prediction_is_reasonable():
    """Verify that the prediction falls within a reasonable range."""
    prediction = predict_house_price(SAMPLE_HOUSE)

    assert 0 < prediction < 1_000_000


def test_prediction_is_repeatable():
    """Verify that the same input produces the same prediction."""
    prediction_1 = predict_house_price(SAMPLE_HOUSE)
    prediction_2 = predict_house_price(SAMPLE_HOUSE)

    assert prediction_1 == prediction_2


def test_missing_feature_raises_error():
    """Verify that missing required features raise an error."""
    incomplete_house = SAMPLE_HOUSE.copy()

    del incomplete_house["Median_Income"]

    with pytest.raises(ValueError):
        predict_house_price(incomplete_house)