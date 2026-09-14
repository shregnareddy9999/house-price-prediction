"""
Tests for the model training module.
"""

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

from src.train_model import train_model, save_model


def test_train_model_returns_random_forest():
    """Verify that training returns a Random Forest regressor."""
    model = train_model()

    assert isinstance(model, RandomForestRegressor)


def test_model_has_expected_number_of_trees():
    """Verify that the trained model contains 200 trees."""
    model = train_model()

    assert model.n_estimators == 200


def test_model_is_fitted():
    """Verify that the model has been fitted successfully."""
    model = train_model()

    assert hasattr(model, "estimators_")
    assert len(model.estimators_) == 200


def test_model_has_expected_features():
    """Verify that the model was trained using 13 features."""
    model = train_model()

    assert model.n_features_in_ == 13


def test_save_model(tmp_path):
    """Verify that a trained model can be saved successfully."""
    model = train_model()

    model_path = Path(tmp_path) / "test_model.joblib"

    save_model(model, model_path)

    assert model_path.exists()
    assert model_path.is_file()
    assert model_path.stat().st_size > 0