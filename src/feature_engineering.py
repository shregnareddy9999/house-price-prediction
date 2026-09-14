"""
Feature engineering utilities for the California House Price Prediction project.
"""

import pandas as pd


FEATURE_COLUMNS = [
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


def select_model_features(
    df: pd.DataFrame,
    feature_columns: list[str] = FEATURE_COLUMNS,
) -> pd.DataFrame:
    """
    Select and order the features expected by the model.

    Parameters
    ----------
    df : pd.DataFrame
        Input feature DataFrame.
    feature_columns : list[str]
        Ordered list of features expected by the model.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the model features in the correct order.
    """
    missing_features = [
        column for column in feature_columns
        if column not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    return df[feature_columns].copy()


def engineer_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Prepare the dataset features for model training or prediction.

    No additional derived features are created because the dataset
    already contains the required numerical geographic and demographic
    variables.

    Parameters
    ----------
    df : pd.DataFrame
        Input feature DataFrame.

    Returns
    -------
    pd.DataFrame
        Prepared feature DataFrame.
    """
    return select_model_features(df)


if __name__ == "__main__":
    print("Feature engineering module loaded successfully!")
    print("Expected model features:")
    for feature in FEATURE_COLUMNS:
        print(f"- {feature}")