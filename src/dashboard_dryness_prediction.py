
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "future_dryness_model.joblib"


def predict_future_dryness(
    soil_moisture_1,
    soil_moisture_2,
    soil_temperature,
    rainfall,
):
    """Return a 30-minute dryness prediction, or an explanatory error."""

    if not MODEL_PATH.exists():
        return {
            "available": False,
            "message": f"Model file not found: {MODEL_PATH}",
        }

    values = {
        "soil_moisture_1": soil_moisture_1,
        "soil_moisture_2": soil_moisture_2,
        "soil_temperature": soil_temperature,
        "rainfall": rainfall,
    }

    if any(value is None for value in values.values()):
        return {
            "available": False,
            "message": (
                "Prediction unavailable: one or more required "
                "sensor or weather inputs are missing."
            ),
        }

    try:
        values = {key: float(value) for key, value in values.items()}
        bundle = joblib.load(MODEL_PATH)
        model = bundle["model"]
        features = bundle["features"]

        sample = pd.DataFrame([values], columns=features)
        prediction = int(model.predict(sample)[0])
        probability = float(model.predict_proba(sample)[0][1])

        return {
            "available": True,
            "prediction": prediction,
            "probability": probability,
            "forecast_minutes": int(bundle["forecast_minutes"]),
            "threshold": float(bundle["low_moisture_threshold"]),
            "message": (
                "Predicted low moisture"
                if prediction == 1
                else "Low moisture not predicted"
            ),
        }
    except Exception as exc:
        return {
            "available": False,
            "message": f"Prediction failed: {exc}",
        }
