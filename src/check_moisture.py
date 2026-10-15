
from pathlib import Path
import pandas as pd

path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "combined_data.csv"
)

df = pd.read_csv(path)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Explore sensor relationships
print("Correlation between moisture sensors:")
print(df[["soil_moisture_1", "soil_moisture_2"]].corr())

print("\nMoisture 1 grouped by moisture 2 quartiles:")
df["moisture_2_group"] = pd.qcut(
    df["soil_moisture_2"],
    q=4,
    duplicates="drop"
)

print(
    df.groupby("moisture_2_group", observed=True)[
        ["soil_moisture_1", "soil_temperature", "rainfall"]
    ].agg(["mean", "median", "count"])
)

# Explore how often the readings change
for column in ["soil_moisture_1", "soil_moisture_2"]:
    change = df[column].diff()
    print(f"\n{column}:")
    print("Unchanged readings:", round((change == 0).mean() * 100, 2), "%")
    print("Increasing readings:", round((change > 0).mean() * 100, 2), "%")
    print("Decreasing readings:", round((change < 0).mean() * 100, 2), "%")

print("\nRainfall nonzero readings:", (df["rainfall"] > 0).sum())
print("Rainfall missing readings:", df["rainfall"].isna().sum())
