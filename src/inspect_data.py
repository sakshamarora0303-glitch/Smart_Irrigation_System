\
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

files = {
    "Soil moisture": "soil_moisture.xlsx",
    "Soil temperature": "soil_temperature.xlsx",
    "Rainfall": "rainfall.xlsx",
}

for name, filename in files.items():
    file_path = DATA_FOLDER / filename

    print("\n" + "=" * 50)
    print(name)

    if not file_path.exists():
        print(f"FILE NOT FOUND: {filename}")
        continue

    df = pd.read_excel(file_path)

    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())
    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))
