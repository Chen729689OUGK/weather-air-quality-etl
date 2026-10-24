import json 
import logging 
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

# Project paths 
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Fes, Morocco 
LATITUDE = 34.0333
LONGITUDE = -5.0000
TIMEZONE = "Africa/Casablanca"

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_weather_data(url, params):
    """Fetch weather data from the API."""
    response = requests.get(url, params=params, timeout=30)
    if not response.ok:
        print(f"Error fetching data from {url}: {response.status_code} - {response.text}")
    response.raise_for_status()
    data = response.json()
    if data.get("error"):
            raise ValueError(data.get("reason", "API returned an error without a reason."))
    return data

def save_data_to_json(data, filename):
    """Save raw data to a JSON file."""
    filepath = RAW_DIR / filename
    with filepath.open("w", encoding="utf-8") as file :
        json.dump(data, file, indent=2, ensure_ascii=False)
    logging.info(f"Data saved to {filepath}")

def main():
    run_time = datetime.now(ZoneInfo(TIMEZONE)).strftime("%Y%m%d_%H%M%S")
    
    weather_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,windspeed_10m",
        "forecast_days": 3,
        "timezone": TIMEZONE
    }

    air_quality_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "pm2_5,pm10,nitrogen_dioxide,ozone,european_aqi",
        "forecast_days": 3,
        "timezone": TIMEZONE
    }

    try:
        logging.info("Fetching weather data...")
        weather_data = fetch_weather_data(WEATHER_API_URL, weather_params)
        save_data_to_json(weather_data, f"weather_data_{run_time}.json")
    
        logging.info("Fetching air quality data...")
        air_quality_data = fetch_weather_data(AIR_QUALITY_API_URL, air_quality_params)
        save_data_to_json(air_quality_data, f"air_quality_data_{run_time}.json")

        logging.info("Data extraction completed successfully.") 

        print("Weather hourly records:",
              len(weather_data.get("hourly", {}).get("time", []))
              )
        print("Air quality hourly records:",
              len(air_quality_data.get("hourly", {}).get("time", [])))

    except (requests.RequestException, ValueError, KeyError) as error:
        logging.error(f"An error occurred: {error}")
        raise 

if __name__ == "__main__":
    main()