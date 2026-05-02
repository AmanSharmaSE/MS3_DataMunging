# wf_ml_training.py

import os
import pickle
from typing import Dict, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor


PROCESSED_DATA_PATH = os.path.join("data_processed", "processed_listings.csv")
MODELS_DIR = "models"

TARGET_COLUMN = "price"
NUMERIC_FEATURES = ["accommodates", "bedrooms", "number_of_reviews"]
CATEGORICAL_FEATURES = ["room_type"]


def load_data() -> pd.DataFrame:
    """
    Load processed dataset from the data_processed folder.
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data not found: {PROCESSED_DATA_PATH}")

    df = pd.read_csv(PROCESSED_DATA_PATH)
    return df


def build_feature_target_split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """e
    Split dataframe into feature matrix X and target vector y.
    """
    required_cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y


def build_preprocessor(scale_numeric: bool = True) -> ColumnTransformer:
    """
    Build preprocessing pipeline for numeric and categorical features.
    """
    numeric_transformer = Pipeline(
        steps=[
            ("scaler", StandardScaler()) if scale_numeric else ("passthrough", "passthrough")
        ]
    )

    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def build_baseline_model() -> Pipeline:
    """
    Build baseline model using only one feature: accommodates.
    This is a simpler model and acts as a reasonable baseline.
    """
    baseline_numeric_features = ["accommodates"]
    baseline_categorical_features = []

    baseline_preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), baseline_numeric_features)
        ],
        remainder="drop"
    )

    model = Pipeline(
        steps=[
            ("preprocessor", baseline_preprocessor),
            ("regressor", LinearRegression())
        ]
    )
    return model


def build_full_linear_model() -> Pipeline:
    preprocessor = build_preprocessor(scale_numeric=True)
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression())
        ]
    )
    return model


def build_ridge_model() -> Pipeline:
    preprocessor = build_preprocessor(scale_numeric=True)
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", Ridge(alpha=1.0))
        ]
    )
    return model


def build_lasso_model() -> Pipeline:
    preprocessor = build_preprocessor(scale_numeric=True)
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", Lasso(alpha=0.1, max_iter=10000))
        ]
    )
    return model


def build_random_forest_model() -> Pipeline:
    preprocessor = build_preprocessor(scale_numeric=False)
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(
                n_estimators=100,
                random_state=42
            ))
        ]
    )
    return model


def save_model(model, filename: str) -> str:
    """
    Save a trained model into the models folder.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    out_path = os.path.join(MODELS_DIR, filename)

    with open(out_path, "wb") as f:
        pickle.dump(model, f)

    return out_path


def train_all_models(X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, str]:
    """
    Train all required models and save them to disk.
    Returns a dictionary mapping model names to saved file paths.
    """
    saved_paths = {}

    models = {
        "baseline_linear.pkl": build_baseline_model(),
        "linear_regression.pkl": build_full_linear_model(),
        "ridge_regression.pkl": build_ridge_model(),
        "lasso_regression.pkl": build_lasso_model(),
        "random_forest_regression.pkl": build_random_forest_model(),
    }

    for model_filename, model in models.items():
        model.fit(X_train, y_train)
        saved_path = save_model(model, model_filename)
        saved_paths[model_filename] = saved_path
        print(f"Saved model: {saved_path}")

    return saved_paths


def main() -> None:
    """
    Standalone training entry point.
    This trains on the entire processed dataset.
    In evaluation, you should instead pass only the training split.
    """
    df = load_data()
    X, y = build_feature_target_split(df)
    train_all_models(X, y)


if __name__ == "__main__":
    main()