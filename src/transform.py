import json 
import logging 
from pathlib import Path 

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_latest_json_file(prefix):
    """Load the most recently created JSON file for a data source."""
    files = sorted(RAW_DIR.glob(f"{prefix}_*.json"))
    if not files:
        raise FileNotFoundError(f"No JSON files found for prefix '{prefix}' in {RAW_DIR}")
    file_path = files[-1]  # Get the most recent file

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    logging.info(f"Loaded data from {file_path}")
    return data

def transform_data(data, source):
    """Convert hourly API JSON into a clean DataFrame."""
    hourly = data.get("hourly")

    if not hourly or "time" not in hourly:
        raise ValueError(f"Missing 'hourly' or 'time' data in the {source} API response.")
    df = pd.DataFrame(hourly)
    df = df.rename(columns={"windspeed_10m": "wind_speed_10m"})

    # Parse timestamp and remove invalid or duplicate records.
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])
    df =df.drop_duplicates(subset=["time"], keep="last")

    # Covert measurements to numeric values.
    for column in df.columns:
        if column != "time":
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Reject impossible negativemesurements where appropriate.
    for column in [
        "precipitation",
        "wind_speed_10m",
        "pm2_5",
        "pm10",
        "nitrogen_dioxide",
        "ozone"
        "relative_humidity_2m"
    ]:
        if column in df.columns:
            df.loc[df[column] < 0, column] = float("nan")

    # Relative humidity must be. between 0 and 100.
    if "relative_humidity_2m" in df.columns:
        df.loc[(df["relative_humidity_2m"] > 100) | (df["relative_humidity_2m"] < 0), "relative_humidity_2m"] = float("nan")

    df = df.sort_values("time").reset_index(drop=True)

    # Add metadata for downstream analysis.
    df["city"] = "Fes"
    df["country"] = "Morocco"
    df["source"] = source

    return df

def main():
    datasets = {
        "weather": "weather_data",
        "air_quality": "air_quality_data"
    }

    for source, prefix in datasets.items():
        data = load_latest_json_file(prefix)
        df = transform_data(data, source)

        output_path = PROCESSED_DIR / f"{source}.csv"
        df.to_csv(output_path, index=False)

        logging.info("%s: %d rows, %d columns",
                     source, len(df), len(df.columns))
        logging.info("Processed data saved to %s", output_path)

        print(f"\n{source.upper()} PREVIEW")
        print(df.head())
        print("Missing values:")
        print(df.isnull().sum())


if __name__ == "__main__":
    main()