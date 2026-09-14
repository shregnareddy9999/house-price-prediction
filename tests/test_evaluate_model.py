"""
Tests for the model evaluation module.
"""

from pathlib import Path

import pandas as pd

from src.evaluate_model import evaluate_model, METRICS_PATH


def test_evaluation_returns_metrics():
    """Verify that model evaluation returns all required metrics."""
    metrics = evaluate_model()

    assert "MAE" in metrics
    assert "RMSE" in metrics
    assert "R2" in metrics


def test_mae_is_valid():
    """Verify that MAE is a valid positive number."""
    metrics = evaluate_model()

    assert isinstance(metrics["MAE"], float)
    assert metrics["MAE"] > 0


def test_rmse_is_valid():
    """Verify that RMSE is a valid positive number."""
    metrics = evaluate_model()

    assert isinstance(metrics["RMSE"], float)
    assert metrics["RMSE"] > 0


def test_r2_is_valid():
    """Verify that R² is within the expected range."""
    metrics = evaluate_model()

    assert isinstance(metrics["R2"], float)
    assert 0 <= metrics["R2"] <= 1


def test_rmse_is_greater_than_or_equal_to_mae():
    """Verify the expected relationship between RMSE and MAE."""
    metrics = evaluate_model()

    assert metrics["RMSE"] >= metrics["MAE"]


def test_metrics_file_is_created():
    """Verify that the evaluation metrics are saved to CSV."""
    evaluate_model()

    assert Path(METRICS_PATH).exists()
    assert Path(METRICS_PATH).is_file()


def test_metrics_file_contains_expected_columns():
    """Verify that the saved metrics file has the required columns."""
    evaluate_model()

    metrics_df = pd.read_csv(METRICS_PATH)

    assert "Model" in metrics_df.columns
    assert "MAE" in metrics_df.columns
    assert "RMSE" in metrics_df.columns
    assert "R2" in metrics_df.columns


def test_metrics_file_contains_random_forest():
    """Verify that the saved metrics belong to the Random Forest model."""
    evaluate_model()

    metrics_df = pd.read_csv(METRICS_PATH)

    assert len(metrics_df) >= 1
    assert "Random Forest" in metrics_df["Model"].values