"""
Tests for the data preprocessing module.
"""

from src.data_preprocessing import (
    load_dataset,
    prepare_features,
    split_data,
    preprocess_dataset,
    TARGET_COLUMN,
)


def test_dataset_loads_successfully():
    """Verify that the raw dataset can be loaded."""
    df = load_dataset()

    assert not df.empty
    assert df.shape == (20640, 14)


def test_target_column_exists():
    """Verify that the target column exists in the dataset."""
    df = load_dataset()

    assert TARGET_COLUMN in df.columns


def test_prepare_features():
    """Verify that features and target are separated correctly."""
    df = load_dataset()

    X, y = prepare_features(df)

    assert TARGET_COLUMN not in X.columns
    assert len(X.columns) == 13
    assert len(y) == len(df)


def test_split_data():
    """Verify that the train/test split has the expected sizes."""
    df = load_dataset()
    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = split_data(X, y)

    assert len(X_train) == 16512
    assert len(X_test) == 4128
    assert len(y_train) == 16512
    assert len(y_test) == 4128


def test_preprocess_dataset():
    """Verify the complete preprocessing workflow."""
    X_train, X_test, y_train, y_test = preprocess_dataset()

    assert X_train.shape == (16512, 13)
    assert X_test.shape == (4128, 13)
    assert y_train.shape == (16512,)
    assert y_test.shape == (4128,)


def test_features_contain_no_missing_values():
    """Verify that the resulting features contain no missing values."""
    X_train, X_test, _, _ = preprocess_dataset()

    assert X_train.isnull().sum().sum() == 0
    assert X_test.isnull().sum().sum() == 0