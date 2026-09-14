"""
Tests for the exploratory data analysis module.
"""

from pathlib import Path

from src.eda import (
    load_eda_dataset,
    print_dataset_summary,
    save_target_distribution,
    save_correlation_heatmap,
    save_income_vs_target,
    save_coast_distance_vs_target,
)


def test_eda_dataset_loads():
    """Verify that the EDA dataset loads successfully."""
    df = load_eda_dataset()

    assert not df.empty
    assert df.shape == (20640, 14)


def test_print_dataset_summary(capsys):
    """Verify that the dataset summary runs successfully."""
    df = load_eda_dataset()

    print_dataset_summary(df)

    captured = capsys.readouterr()

    assert "Dataset shape:" in captured.out
    assert "Columns:" in captured.out
    assert "Missing values:" in captured.out
    assert "Duplicate rows:" in captured.out
    assert "Data types:" in captured.out


def test_target_distribution_plot(tmp_path):
    """Verify that the target distribution plot is created."""
    df = load_eda_dataset()

    output_path = tmp_path / "target_distribution.png"

    save_target_distribution(df, output_path)

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.stat().st_size > 0


def test_correlation_heatmap(tmp_path):
    """Verify that the correlation heatmap is created."""
    df = load_eda_dataset()

    output_path = tmp_path / "correlation_heatmap.png"

    save_correlation_heatmap(df, output_path)

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.stat().st_size > 0


def test_income_vs_target_plot(tmp_path):
    """Verify that the income versus house value plot is created."""
    df = load_eda_dataset()

    output_path = tmp_path / "income_vs_house_value.png"

    save_income_vs_target(df, output_path)

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.stat().st_size > 0


def test_coast_distance_vs_target_plot(tmp_path):
    """Verify that the coast distance versus house value plot is created."""
    df = load_eda_dataset()

    output_path = tmp_path / "coast_distance_vs_house_value.png"

    save_coast_distance_vs_target(df, output_path)

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.stat().st_size > 0