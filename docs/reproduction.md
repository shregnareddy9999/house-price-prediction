# Reproduction

All Python commands assume the **repository root** as the working directory.

The raw CSV (`data/raw/*`) and the trained artifact (`outputs/house_price_model.joblib`) are gitignored. You must download the dataset and train locally to recreate the model.

## 1. Environment

Python 3.10+ is required (`str | Path` type hints).

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Frontend needs Node.js and npm.

## 2. Dataset

1. Obtain `California_Houses.csv` (see [dataset.md](dataset.md)).
2. Create `data/raw/` if needed.
3. Copy the file to `data/raw/California_Houses.csv`.

Confirm:

```bash
python -m src.data_preprocessing
```

Expected shapes: train `(16512, 13)`, test `(4128, 13)`.

## 3. Train

```bash
python -m src.train_model
```

Writes `outputs/house_price_model.joblib` (`RandomForestRegressor`, 200 trees, `random_state=42`).

## 4. Evaluate

```bash
python -m src.evaluate_model
```

Prints MAE, RMSE, and R² and overwrites [outputs/metrics.csv](../outputs/metrics.csv). Expected production metrics:

- MAE ≈ $30,407.79
- RMSE ≈ $47,883.47
- R² ≈ 0.8250

## 5. Optional EDA

```bash
python -m src.eda
```

Writes plots under `outputs/plots/` (target distribution, heatmap, income scatter, coast scatter). Residual and feature-importance PNGs come from the notebook.

## 6. CLI prediction

```bash
python -m src.predict
```

Uses a built-in sample feature dict and prints a dollar value. Requires the joblib file from step 3.

## 7. Notebook

Open [notebook/house_price_prediction.ipynb](../notebook/house_price_prediction.ipynb) with Jupyter (`jupyter notebook` or VS Code / Cursor). Paths in the notebook are relative (`../data/raw/California_Houses.csv`, `../outputs/...`). Run all cells to regenerate Linear Regression vs Random Forest metrics, residual plots, sample predictions, and the saved model.

## 8. Tests

```bash
pytest
```

[pytest.ini](../pytest.ini) sets `pythonpath = .`. You need the CSV for preprocessing/EDA tests and the trained model for [tests/test_predict.py](../tests/test_predict.py) and [tests/test_evaluate_model.py](../tests/test_evaluate_model.py). Training tests fit a new forest and can take a minute.

## 9. API

With the model file present:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Checks:

- `http://127.0.0.1:8000/` — status JSON
- `http://127.0.0.1:8000/health` — `{"status": "healthy"}`
- Interactive docs: `http://127.0.0.1:8000/docs`

Example `POST /predict` body (same fields as [src/predict.py](../src/predict.py)):

```json
{
  "Median_Income": 5.0,
  "Median_Age": 30.0,
  "Tot_Rooms": 2000.0,
  "Tot_Bedrooms": 400.0,
  "Population": 1000.0,
  "Households": 350.0,
  "Latitude": 34.0,
  "Longitude": -118.0,
  "Distance_to_coast": 10.0,
  "Distance_to_LA": 20.0,
  "Distance_to_SanDiego": 150.0,
  "Distance_to_SanJose": 500.0,
  "Distance_to_SanFrancisco": 550.0
}
```

## 10. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the printed local URL (default `http://127.0.0.1:5173`). The form posts to `http://127.0.0.1:8000/predict`; keep the API running.

## Expected artifacts after a full run

| Artifact | Produced by |
|---|---|
| `outputs/house_price_model.joblib` | `python -m src.train_model` or notebook |
| `outputs/metrics.csv` | `python -m src.evaluate_model` |
| `outputs/sample_predictions.csv` | Notebook |
| `outputs/plots/*.png` | `python -m src.eda` and notebook |
