
import logging
import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
SCHEMA_FILE = PROJECT_DIR / "sql" / "schema.sql"

load_dotenv(PROJECT_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "weather_db",
    "user": "weather_user",
    "password": os.getenv("POSTGRES_PASSWORD"),
}

TABLES = {
    "weather.csv": {
        "table": "weather_observations",
        "columns": [
            "city", "country", "time",
            "temperature_2m", "relative_humidity_2m",
            "precipitation", "wind_speed_10m", "source",
        ],
    },
    "air_quality.csv": {
        "table": "air_quality_observations",
        "columns": [
            "city", "country", "time",
            "pm2_5", "pm10", "nitrogen_dioxide",
            "ozone", "european_aqi", "source",
        ],
    },
}


def clean_value(value):
    """Convert Pandas missing values to SQL NULL."""
    if pd.isna(value):
        return None
    return value


def load_csv(cursor, filename, table, columns):
    filepath = PROCESSED_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Missing processed file: {filepath}")

    df = pd.read_csv(filepath)

    if df.empty:
        logging.warning("%s contains no records", filename)
        return 0

    # Map CSV column 'time' to database column 'observation_time'.
    df["time"] = pd.to_datetime(df["time"], errors="raise")

    expected = set(columns)
    missing = expected - set(df.columns)

    if missing:
        raise ValueError(
            f"{filename} is missing columns: {sorted(missing)}"
        )

    df = df[columns].copy()
    df = df.rename(columns={"time": "observation_time"})

    db_columns = [
        "city", "country", "observation_time",
        *[c for c in columns if c not in {"city", "country", "time"}],
    ]

    records = [
        tuple(clean_value(value) for value in row)
        for row in df.itertuples(index=False, name=None)
    ]

    update_columns = [
        c for c in db_columns
        if c not in {"city", "observation_time"}
    ]

    updates = ", ".join(
        f"{c} = EXCLUDED.{c}" for c in update_columns
    )

    query = f"""
        INSERT INTO {table} ({", ".join(db_columns)})
        VALUES %s
        ON CONFLICT (city, observation_time)
        DO UPDATE SET {updates},
                      loaded_at = CURRENT_TIMESTAMP
    """

    execute_values(cursor, query, records, page_size=500)
    logging.info("%s: loaded %d records", table, len(records))

    return len(records)


def main():
    if not DB_CONFIG["password"]:
        raise ValueError("POSTGRES_PASSWORD is missing from .env")

    schema = SCHEMA_FILE.read_text(encoding="utf-8")
    if not schema.strip():
        raise ValueError(f"Schema file is empty: {SCHEMA_FILE}")

    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema)

            total = 0
            for filename, config in TABLES.items():
                total += load_csv(
                    cursor,
                    filename,
                    config["table"],
                    config["columns"],
                )

    logging.info("Load complete: %d CSV records processed", total)


if __name__ == "__main__":
    main()
