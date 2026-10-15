
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "future_dryness_model.joblib"

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
features = bundle["features"]

print("Live Soil Moisture Prediction")
print("Enter readings in the same units as the training dataset.")
print("Type 'q' to quit.\n")

while True:
    try:
        moisture_1 = input("Soil moisture 1: ").strip()
        if moisture_1.lower() == "q":
            break

        moisture_2 = float(input("Soil moisture 2: "))
        temperature = float(input("Soil temperature (°C): "))
        rainfall = float(input("Rainfall: "))

        sample = pd.DataFrame([{
            "soil_moisture_1": float(moisture_1),
            "soil_moisture_2": moisture_2,
            "soil_temperature": temperature,
            "rainfall": rainfall,
        }], columns=features)

        prediction = int(model.predict(sample)[0])
        probability = model.predict_proba(sample)[0][1]

        if prediction == 1:
            print(
                f"\nPrediction: LOW MOISTURE in approximately "
                f"{bundle['forecast_minutes']} minutes."
            )
        else:
            print(
                f"\nPrediction: NOT LOW MOISTURE in approximately "
                f"{bundle['forecast_minutes']} minutes."
            )

        print(f"Model confidence for LOW MOISTURE: {probability:.1%}\n")

    except ValueError:
        print("Please enter valid numeric readings.\n")
    except KeyboardInterrupt:
        break

print("\nPrediction session ended.")
