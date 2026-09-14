"""
Exploratory Data Analysis utilities for the California House Price Prediction project.
"""

from pathlib import Path

import matplotlib

# Use a non-interactive backend so plots can be generated
# without requiring Tkinter or a graphical desktop.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.data_preprocessing import DATA_PATH, load_dataset
from src.feature_engineering import FEATURE_COLUMNS


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLOTS_DIR = PROJECT_ROOT / "outputs" / "plots"

TARGET_COLUMN = "Median_House_Value"


def load_eda_dataset(file_path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the dataset for exploratory data analysis."""
    return load_dataset(file_path)


def print_dataset_summary(df: pd.DataFrame) -> None:
    """Print basic information about the dataset."""
    print("Dataset shape:", df.shape)

    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nData types:")
    print(df.dtypes)


def save_target_distribution(
    df: pd.DataFrame,
    output_path: str | Path = PLOTS_DIR / "target_distribution.png",
) -> None:
    """Save the target variable distribution plot."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df[TARGET_COLUMN],
        bins=50,
        kde=True,
    )

    plt.title("Distribution of Median House Value")
    plt.xlabel("Median House Value (USD)")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_correlation_heatmap(
    df: pd.DataFrame,
    output_path: str | Path = PLOTS_DIR / "correlation_heatmap.png",
) -> None:
    """Save a correlation heatmap for the numerical features."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    correlation_matrix = df[
        FEATURE_COLUMNS + [TARGET_COLUMN]
    ].corr()

    plt.figure(figsize=(14, 10))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
    )

    plt.title("Feature Correlation Heatmap")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_income_vs_target(
    df: pd.DataFrame,
    output_path: str | Path = PLOTS_DIR / "income_vs_house_value.png",
) -> None:
    """Save a scatter plot of median income versus house value."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Median_Income",
        y=TARGET_COLUMN,
        alpha=0.4,
    )

    plt.title("Median Income vs Median House Value")
    plt.xlabel("Median Income")
    plt.ylabel("Median House Value (USD)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_coast_distance_vs_target(
    df: pd.DataFrame,
    output_path: str | Path = PLOTS_DIR / "coast_distance_vs_house_value.png",
) -> None:
    """Save a scatter plot of coast distance versus house value."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Distance_to_coast",
        y=TARGET_COLUMN,
        alpha=0.4,
    )

    plt.title("Distance to Coast vs Median House Value")
    plt.xlabel("Distance to Coast")
    plt.ylabel("Median House Value (USD)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def run_eda(file_path: str | Path = DATA_PATH) -> None:
    """Run the complete exploratory data analysis workflow."""
    df = load_eda_dataset(file_path)

    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    print_dataset_summary(df)

    save_target_distribution(df)
    save_correlation_heatmap(df)
    save_income_vs_target(df)
    save_coast_distance_vs_target(df)

    print("\nEDA completed successfully!")
    print(f"Plots saved to: {PLOTS_DIR}")


if __name__ == "__main__":
    run_eda()