# Task 6 context

This repository implements **Task 6 — Linear Regression: House Price Prediction**. Each assignment bullet maps to a concrete artifact below.

Linear Regression is trained and scored in [notebook/house_price_prediction.ipynb](../notebook/house_price_prediction.ipynb) (with `StandardScaler`). Random Forest is the **saved production model** used by [src/train_model.py](../src/train_model.py), [src/evaluate_model.py](../src/evaluate_model.py), and the FastAPI service, because it is stronger on the same 80/20 test split.

## Rubric mapping

### Dataset source referenced and preprocessing included

| Detail | Location |
|---|---|
| Dataset identity, columns, split | [dataset.md](dataset.md) |
| Load, target split, train/test | [src/data_preprocessing.py](../src/data_preprocessing.py) |
| Feature selection and order | [src/feature_engineering.py](../src/feature_engineering.py) |
| Notebook load and EDA | [notebook/house_price_prediction.ipynb](../notebook/house_price_prediction.ipynb) |

Expected file: `data/raw/California_Houses.csv` (20,640 rows × 14 columns). The CSV is gitignored; see [reproduction.md](reproduction.md).

### Trained regression model with RMSE (or MAE) and R² on the test set

| Detail | Location |
|---|---|
| Linear Regression metrics | Notebook comparison table |
| Random Forest metrics | [outputs/metrics.csv](../outputs/metrics.csv) |
| Evaluation script | [src/evaluate_model.py](../src/evaluate_model.py) |

Held-out test set (4,128 rows, `random_state=42`):

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Linear Regression | $50,404.86 | $69,353.01 | 0.6330 |
| Random Forest | $30,407.79 | $47,883.47 | 0.8250 |

### Residual plot and at least five sample predictions vs actual

| Detail | Location |
|---|---|
| Random Forest residual plot | [outputs/plots/random_forest_residuals.png](../outputs/plots/random_forest_residuals.png) |
| Linear Regression residual plot | Notebook (not saved as a separate PNG) |
| Five actual vs predicted rows | [outputs/sample_predictions.csv](../outputs/sample_predictions.csv) |
| Narrative | [evaluation.md](evaluation.md) |

### Saved model artifact and reproduction instructions

| Detail | Location |
|---|---|
| Artifact path | `outputs/house_price_model.joblib` |
| Training entry point | `python -m src.train_model` |
| Full environment and run steps | [reproduction.md](reproduction.md) |

The joblib file is listed in `.gitignore` because it is a large generated binary. Training from the same script and seed recreates it.

## Deliverables

| Deliverable | Path |
|---|---|
| Repo | This project |
| Notebook | [notebook/house_price_prediction.ipynb](../notebook/house_price_prediction.ipynb) |
| Scripts | [src/](../src/) |
| Saved model | `outputs/house_price_model.joblib` (after training) |
| Evaluation plots | [outputs/plots/](../outputs/plots/) |
| Sample predictions | [outputs/sample_predictions.csv](../outputs/sample_predictions.csv) |
| Summary | [evaluation.md](evaluation.md) and the root [README.md](../README.md) |
| Interactive app | [backend/main.py](../backend/main.py), [frontend/](../frontend/) |
| Architecture | [architecture.md](architecture.md) |
