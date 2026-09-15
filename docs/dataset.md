# Dataset and preprocessing

## Source

The model uses **California_Houses.csv**: 20,640 rows and 14 columns of 1990 California census **block-group** housing data, with extra geographic distance features.

The file is the public “California Housing Prices” extra-features table (commonly distributed on Kaggle as *fedesoriano / California Housing Prices*), derived from the StatLib / Pace & Barry California housing dataset (the same family of data as `sklearn.datasets.fetch_california_housing`).

Place the CSV at:

```
data/raw/California_Houses.csv
```

That path is gitignored (`data/raw/*`). Training, EDA, tests, and the notebook all read this location via [src/data_preprocessing.py](../src/data_preprocessing.py) (`DATA_PATH`).

## Target

| Column | Meaning |
|---|---|
| `Median_House_Value` | Median house value for the block group, in USD (1990) |

## Features (13)

| Column | Role |
|---|---|
| `Median_Income` | Median household income (dataset units, typically tens of thousands of USD) |
| `Median_Age` | Median age of houses in the block group |
| `Tot_Rooms` | Total rooms in the block group |
| `Tot_Bedrooms` | Total bedrooms in the block group |
| `Population` | Block-group population |
| `Households` | Number of households |
| `Latitude` | Geographic latitude |
| `Longitude` | Geographic longitude |
| `Distance_to_coast` | Distance to the coast (meters in this extra-features table) |
| `Distance_to_LA` | Distance to Los Angeles |
| `Distance_to_SanDiego` | Distance to San Diego |
| `Distance_to_SanJose` | Distance to San Jose |
| `Distance_to_SanFrancisco` | Distance to San Francisco |

The ordered list is defined as `FEATURE_COLUMNS` in [src/feature_engineering.py](../src/feature_engineering.py).

## Preprocessing

Implemented in [src/data_preprocessing.py](../src/data_preprocessing.py):

1. **Load** the CSV (`load_dataset`). Missing file raises `FileNotFoundError`.
2. **Separate** features and target (`prepare_features`). The target column is dropped from `X`.
3. **Split** with `train_test_split(test_size=0.20, random_state=42)`.

Resulting shapes (asserted in [tests/test_data_preprocessing.py](../tests/test_data_preprocessing.py)):

| Split | Rows | Feature columns |
|---|---|---|
| Train | 16,512 | 13 |
| Test | 4,128 | 13 |

There is **no imputation or scaling** in the production pipeline. Tests assert that the loaded features contain zero missing values. Linear Regression in the notebook uses `StandardScaler` inside a `Pipeline`; Random Forest does not need scaling.

## Feature engineering

[src/feature_engineering.py](../src/feature_engineering.py) only **selects and orders** the 13 columns above. Distances to the coast and cities are already present in the CSV, so no new geographic features are computed at train or serve time. Extra columns are dropped; missing required columns raise `ValueError`.

The same `engineer_features` function is used in training, evaluation, and `predict_house_price`, which keeps the API payload aligned with the fitted model.
