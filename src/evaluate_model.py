"""
Evaluate the trained Random Forest model for house price prediction.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_preprocessing import preprocess_dataset
from src.feature_engineering import engineer_features


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "house_price_model.joblib"
)

METRICS_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "metrics.csv"
)


def evaluate_model():
    """
    Load the saved model, generate test predictions,
    calculate regression metrics, and save the results.

    Returns
    -------
    dict
        Dictionary containing MAE, RMSE, and R².
    """

    # Prepare the test data
    X_train, X_test, y_train, y_test = preprocess_dataset()

    X_test = engineer_features(X_test)

    # Load the saved model
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Saved model not found at: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    # Generate predictions
    y_pred = model.predict(X_test)

    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }

    # Save metrics
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

    metrics_df = pd.DataFrame([
        {
            "Model": "Random Forest",
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        }
    ])

    metrics_df.to_csv(
        METRICS_PATH,
        index=False
    )

    print("Model evaluation completed successfully!")
    print("-" * 40)
    print(f"MAE  : ${mae:,.2f}")
    print(f"RMSE : ${rmse:,.2f}")
    print(f"R²   : {r2:.4f}")
    print("-" * 40)
    print(f"Metrics saved to: {METRICS_PATH}")

    return metrics


if __name__ == "__main__":
    evaluate_model()