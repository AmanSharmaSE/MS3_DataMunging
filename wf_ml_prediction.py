# wf_ml_prediction.py

import os
import pickle
from typing import Union

import pandas as pd


MODELS_DIR = "models"
DEFAULT_MODEL_PATH = os.path.join(MODELS_DIR, "linear_regression.pkl")


def load_model(model_path: str = DEFAULT_MODEL_PATH):
    """
    Load a trained model from disk.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model


def predict_from_dataframe(input_df: pd.DataFrame, model_path: str = DEFAULT_MODEL_PATH):
    """
    Predict output(s) from a pandas DataFrame.
    Expected columns:
        - accommodates
        - bedrooms
        - number_of_reviews
        - room_type
    """
    model = load_model(model_path)
    predictions = model.predict(input_df)
    return predictions


def predict_single_record(
    accommodates: Union[int, float],
    bedrooms: Union[int, float],
    number_of_reviews: Union[int, float],
    room_type: str,
    model_path: str = DEFAULT_MODEL_PATH
) -> float:
    """
    Predict price for a single Airbnb listing record.
    """
    input_df = pd.DataFrame([
        {
            "accommodates": accommodates,
            "bedrooms": bedrooms,
            "number_of_reviews": number_of_reviews,
            "room_type": room_type,
        }
    ])

    prediction = predict_from_dataframe(input_df, model_path=model_path)[0]
    return float(prediction)


def main() -> None:
    """
    Example standalone prediction.
    """
    predicted_price = predict_single_record(
        accommodates=4,
        bedrooms=2,
        number_of_reviews=15,
        room_type="Entire home/apt",
        model_path=DEFAULT_MODEL_PATH
    )

    print(f"Predicted price: {predicted_price:.2f}")


if __name__ == "__main__":
    main()