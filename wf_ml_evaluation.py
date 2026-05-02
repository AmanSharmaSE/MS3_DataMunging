# wf_ml_evaluation.py

import os
from typing import Dict, List

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from wf_ml_training import (
    load_data,
    build_feature_target_split,
    train_all_models,
)
from wf_ml_prediction import load_model


DATA_PROCESSED_DIR = "data_processed"
EVALUATION_DIR = "evaluation"
TRAIN_PATH = os.path.join(DATA_PROCESSED_DIR, "train_listings.csv")
TEST_PATH = os.path.join(DATA_PROCESSED_DIR, "test_listings.csv")
SUMMARY_PATH = os.path.join(EVALUATION_DIR, "summary.txt")


def save_train_test_sets(train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    """
    Save training and test datasets into data_processed folder.
    """
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)


def compute_regression_metrics(y_true, y_pred) -> Dict[str, float]:
    """
    Compute regression evaluation metrics.
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_true, y_pred)

    return {
        "RMSE": rmse,
        "R2": r2,
    }


def evaluate_single_model(model_path: str, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """
    Load one saved model and evaluate it on test data.
    """
    model = load_model(model_path)
    y_pred = model.predict(X_test)
    return compute_regression_metrics(y_test, y_pred)


def format_results_table(results: List[Dict[str, float]]) -> str:
    """
    Format evaluation results as plain text table.
    """
    lines = []
    header = f"{'Model':<30} {'RMSE':>15} {'R2':>15}"
    lines.append(header)
    lines.append("-" * len(header))

    for row in results:
        lines.append(
            f"{row['model_name']:<30} "
            f"{row['RMSE']:>15.4f} "
            f"{row['R2']:>15.4f}"
        )

    return "\n".join(lines)


def run_evaluation(test_size: float = 0.2, random_state: int = 42) -> List[Dict[str, float]]:
    """
    Main evaluation workflow:
    - load processed data
    - split 80/20 into representative train and test sets
    - save split datasets
    - train all models on train set
    - evaluate all models on test set
    - write summary to evaluation/summary.txt
    """
    os.makedirs(EVALUATION_DIR, exist_ok=True)

    df = load_data()

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    save_train_test_sets(train_df, test_df)

    if len(test_df) < 30:
        raise ValueError(
            f"Test dataset has only {len(test_df)} samples. "
            "Assignment requires at least 30 samples."
        )

    X_train, y_train = build_feature_target_split(train_df)
    X_test, y_test = build_feature_target_split(test_df)

    saved_model_paths = train_all_models(X_train, y_train)

    results = []
    for model_filename, model_path in saved_model_paths.items():
        metrics = evaluate_single_model(model_path, X_test, y_test)
        results.append({
            "model_name": model_filename.replace(".pkl", ""),
            "RMSE": metrics["RMSE"],
            "R2": metrics["R2"],
        })

    summary_lines = []
    summary_lines.append("SER541 Machine Learning Evaluation Summary")
    summary_lines.append("")
    summary_lines.append(f"Total dataset size: {len(df)}")
    summary_lines.append(f"Training set size: {len(train_df)}")
    summary_lines.append(f"Test set size: {len(test_df)}")
    summary_lines.append(f"Train fraction: {1 - test_size:.2f}")
    summary_lines.append(f"Test fraction: {test_size:.2f}")
    summary_lines.append("")
    summary_lines.append("Evaluation Metrics:")
    summary_lines.append("- RMSE (Root Mean Squared Error)")
    summary_lines.append("- R2 (Coefficient of Determination)")
    summary_lines.append("")
    summary_lines.append("Model Results:")
    summary_lines.append(format_results_table(results))

    best_model = min(results, key=lambda x: x["RMSE"])
    summary_lines.append("")
    summary_lines.append(f"Best model by RMSE: {best_model['model_name']}")
    summary_lines.append(f"Best RMSE: {best_model['RMSE']:.4f}")
    summary_lines.append(f"Best R2: {best_model['R2']:.4f}")

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    print(f"Saved evaluation summary to: {SUMMARY_PATH}")
    return results


def main() -> None:
    results = run_evaluation()

    print("\nEvaluation Results:")
    for row in results:
        print(
            f"{row['model_name']:<30} "
            f"RMSE={row['RMSE']:.4f} "
            f"R2={row['R2']:.4f}"
        )


if __name__ == "__main__":
    main()