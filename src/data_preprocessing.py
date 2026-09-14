"""
Data preprocessing utilities for the California House Price Prediction project.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


TARGET_COLUMN = "Median_House_Value"

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "California_Houses.csv"
)


def load_dataset(file_path: str | Path = DATA_PATH) -> pd.DataFrame:
    """
    Load the California housing dataset from a CSV file.

    Parameters
    ----------
    file_path : str or Path
        Path to the raw dataset.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path}"
        )

    return pd.read_csv(file_path)


def prepare_features(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
):
    """
    Separate the dataset into features and target.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    target_column : str
        Name of the prediction target.

    Returns
    -------
    X : pd.DataFrame
        Feature data.
    y : pd.Series
        Target values.
    """
    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found in dataset."
        )

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return X, y


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.20,
    random_state: int = 42,
):
    """
    Split features and target into training and testing sets.

    Parameters
    ----------
    X : pd.DataFrame
        Feature data.
    y : pd.Series
        Target values.
    test_size : float
        Proportion of data reserved for testing.
    random_state : int
        Seed for reproducible splitting.

    Returns
    -------
    tuple
        X_train, X_test, y_train, y_test
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )


def preprocess_dataset(
    file_path: str | Path = DATA_PATH,
    target_column: str = TARGET_COLUMN,
    test_size: float = 0.20,
    random_state: int = 42,
):
    """
    Complete dataset loading and train-test preparation pipeline.

    Returns
    -------
    tuple
        X_train, X_test, y_train, y_test
    """
    df = load_dataset(file_path)

    X, y = prepare_features(
        df,
        target_column=target_column,
    )

    X_train, X_test, y_train, y_test = split_data(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = preprocess_dataset()

    print("Preprocessing completed successfully!")
    print(f"Training features: {X_train.shape}")
    print(f"Testing features: {X_test.shape}")
    print(f"Training target: {y_train.shape}")
    print(f"Testing target: {y_test.shape}")