"""
Tests for the feature engineering module.
"""

import pandas as pd
import pytest

from src.feature_engineering import (
    FEATURE_COLUMNS,
    select_model_features,
    engineer_features,
)


def test_feature_columns_count():
    """Verify that the project uses exactly 13 model features."""
    assert len(FEATURE_COLUMNS) == 13


def test_feature_columns_are_expected():
    """Verify that all expected features are present."""
    expected_features = [
        "Median_Income",
        "Median_Age",
        "Tot_Rooms",
        "Tot_Bedrooms",
        "Population",
        "Households",
        "Latitude",
        "Longitude",
        "Distance_to_coast",
        "Distance_to_LA",
        "Distance_to_SanDiego",
        "Distance_to_SanJose",
        "Distance_to_SanFrancisco",
    ]

    assert FEATURE_COLUMNS == expected_features


def test_select_model_features():
    """Verify that only the required model features are selected."""
    data = {
        "Median_Income": [5.0, 6.0],
        "Median_Age": [30.0, 40.0],
        "Tot_Rooms": [2000, 3000],
        "Tot_Bedrooms": [400, 600],
        "Population": [1000, 1500],
        "Households": [350, 500],
        "Latitude": [34.0, 35.0],
        "Longitude": [-118.0, -119.0],
        "Distance_to_coast": [10.0, 20.0],
        "Distance_to_LA": [20.0, 30.0],
        "Distance_to_SanDiego": [150.0, 120.0],
        "Distance_to_SanJose": [500.0, 450.0],
        "Distance_to_SanFrancisco": [550.0, 500.0],
        "Extra_Column": [100, 200],
    }

    df = pd.DataFrame(data)

    result = select_model_features(df)

    assert list(result.columns) == FEATURE_COLUMNS
    assert "Extra_Column" not in result.columns
    assert result.shape == (2, 13)


def test_engineer_features():
    """Verify that the feature engineering function returns the correct features."""
    data = {
        feature: [1.0, 2.0]
        for feature in FEATURE_COLUMNS
    }

    df = pd.DataFrame(data)

    result = engineer_features(df)

    assert list(result.columns) == FEATURE_COLUMNS
    assert result.shape == (2, 13)


def test_features_are_not_modified():
    """Verify that feature engineering preserves the original feature values."""
    data = {
        feature: [1.0, 2.0]
        for feature in FEATURE_COLUMNS
    }

    df = pd.DataFrame(data)

    result = engineer_features(df)

    pd.testing.assert_frame_equal(result, df)


def test_missing_feature_raises_error():
    """Verify that missing required features raise a ValueError."""
    data = {
        feature: [1.0, 2.0]
        for feature in FEATURE_COLUMNS[:-1]
    }

    df = pd.DataFrame(data)

    with pytest.raises(ValueError):
        select_model_features(df)


def test_original_dataframe_is_not_modified():
    """Verify that feature selection does not modify the original dataframe."""
    data = {
        feature: [1.0, 2.0]
        for feature in FEATURE_COLUMNS
    }

    df = pd.DataFrame(data)
    original_columns = list(df.columns)

    result = select_model_features(df)

    assert list(df.columns) == original_columns
    assert result is not df