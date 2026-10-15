
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = DATA / "combined_data.csv"

# Load datasets
moisture = pd.read_excel(DATA / "soil_moisture.xlsx")
temperature = pd.read_excel(DATA / "soil_temperature.xlsx")
rainfall = pd.read_excel(DATA / "rainfall.xlsx")

# Convert timestamps
moisture["Timestamps"] = pd.to_datetime(
    moisture["Timestamps"], errors="coerce"
)
temperature["Timestamps"] = pd.to_datetime(
    temperature["Timestamps"], errors="coerce"
)
rainfall["Data"] = pd.to_datetime(
    rainfall["Data"], dayfirst=True, errors="coerce"
)

# Remove invalid timestamps
moisture = moisture.dropna(subset=["Timestamps"])
temperature = temperature.dropna(subset=["Timestamps"])
rainfall = rainfall.dropna(subset=["Data"])

# Select two soil moisture channels
moisture_columns = [
    c for c in moisture.columns if c != "Timestamps"
]

if len(moisture_columns) < 2:
    raise ValueError("At least two moisture channels are required.")

moisture = moisture[
    ["Timestamps", moisture_columns[0], moisture_columns[1]]
].copy()

moisture.columns = [
    "timestamp", "soil_moisture_1", "soil_moisture_2"
]

# Select soil temperature
temperature = temperature[
    ["Timestamps", "Port1:SoilTemperature"]
].copy()

temperature.columns = ["timestamp", "soil_temperature"]

# Select rainfall
rain_column = next(c for c in rainfall.columns if c != "Data")
rainfall = rainfall[["Data", rain_column]].copy()
rainfall.columns = ["timestamp", "rainfall"]

# Align measurements to 15-minute intervals
for frame in [moisture, temperature, rainfall]:
    frame["timestamp"] = frame["timestamp"].dt.floor("15min")

# Combine using matching timestamps
combined = moisture.merge(
    temperature, on="timestamp", how="inner"
)

combined = combined.merge(
    rainfall, on="timestamp", how="left"
)

combined = combined.sort_values("timestamp")
combined = combined.drop_duplicates("timestamp")

# Save the combined dataset
combined.to_csv(OUTPUT, index=False)

print("Dataset preparation complete.")
print("Rows:", len(combined))
print("Columns:", combined.columns.tolist())
print("Saved to:", OUTPUT)
print(combined.head())
