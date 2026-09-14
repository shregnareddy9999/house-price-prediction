"""
Train the Random Forest regression model for house price prediction.
"""

from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor

from src.data_preprocessing import preprocess_dataset
from src.feature_engineering import engineer_features


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "house_price_model.joblib"
)


def train_model():
    """
    Prepare the dataset and train the Random Forest model.

    Returns
    -------
    RandomForestRegressor
        Trained Random Forest regression model.
    """
    X_train, X_test, y_train, y_test = preprocess_dataset()

    X_train = engineer_features(X_train)

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    return model


def save_model(model, model_path: str | Path = MODEL_PATH):
    """
    Save the trained model using joblib.

    Parameters
    ----------
    model : RandomForestRegressor
        Trained model.
    model_path : str or Path
        Destination path for the saved model.
    """
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)

    print(f"Model saved successfully to: {model_path}")


if __name__ == "__main__":
    trained_model = train_model()

    save_model(trained_model)

    print("Random Forest training completed successfully!")