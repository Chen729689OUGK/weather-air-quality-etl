
import logging
import os

import psycopg2
from dotenv import load_dotenv

PROJECT_DIR = __import__("pathlib").Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "weather_db",
    "user": "weather_user",
    "password": os.getenv("POSTGRES_PASSWORD"),
}

CHECKS = {
    "weather_observations": """
        SELECT
            COUNT(*),
            COUNT(*) FILTER (WHERE observation_time IS NULL),
            COUNT(*) FILTER (
                WHERE relative_humidity_2m < 0
                   OR relative_humidity_2m > 100
            ),
            COUNT(*) FILTER (
                WHERE precipitation < 0 OR wind_speed_10m < 0
            )
        FROM weather_observations
    """,
    "air_quality_observations": """
        SELECT
            COUNT(*),
            COUNT(*) FILTER (WHERE observation_time IS NULL),
            COUNT(*) FILTER (
                WHERE pm2_5 < 0 OR pm10 < 0
                   OR nitrogen_dioxide < 0 OR ozone < 0
            ),
            COUNT(*) FILTER (WHERE european_aqi < 0)
        FROM air_quality_observations
    """,
}


def main():
    if not DB_CONFIG["password"]:
        raise ValueError("POSTGRES_PASSWORD is missing from .env")

    failed = False

    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            for table, query in CHECKS.items():
                cursor.execute(query)
                rows, missing_times, invalid_measurements, invalid_index = (
                    cursor.fetchone()
                )

                logging.info("%s: %s rows", table, rows)
                logging.info("Missing timestamps: %s", missing_times)
                logging.info(
                    "Invalid measurements: %s", invalid_measurements
                )
                logging.info("Invalid index values: %s", invalid_index)

                if rows == 0 or missing_times or invalid_measurements or invalid_index:
                    failed = True

    if failed:
        raise SystemExit("Data quality validation FAILED")

    logging.info("All data quality checks passed!")


if __name__ == "__main__":
    main()
