Weather and Air Quality ETL Pipeline

Automated data pipeline for weather and air quality data in Fes, Morocco.

Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline that collects weather and air quality forecast data, transforms it into structured datasets, loads it into PostgreSQL, and validates data quality.

The pipeline is orchestrated with Python and can be scheduled to run automatically using cron on macOS.

Objectives

* Retrieve weather and air quality data from public APIs.
* Transform raw JSON responses into clean, structured CSV datasets.
* Store processed data in a PostgreSQL relational database.
* Implement data quality checks and SQL analytics.
* Automate pipeline execution and maintain execution logs.

Architecture

Open-Meteo APIs
      |
      v
   EXTRACT
      |
      v
 Raw JSON files
   data/raw/
      |
      v
  TRANSFORM
      |
      v
 Processed CSV files
 data/processed/
      |
      v
    LOAD
      |
      v
 PostgreSQL Database
      |
      v
   VALIDATE
      |
      v
 Quality checks and SQL analytics
Orchestration: Python
Scheduling: cron
Logging: logs/

Technologies

* Python — pipeline orchestration and data processing
* Pandas — data transformation and cleaning
* Requests — API requests
* Open-Meteo APIs — weather and air quality forecast data
* PostgreSQL — relational data storage
* Docker Compose — database deployment
* SQL — analytics and data quality checks
* cron — scheduled execution on macOS

Data Sources

The project uses Open-Meteo weather and air quality APIs for Fes, Morocco.

Weather variables include temperature, relative humidity, precipitation, and wind speed.

Air quality variables include PM2.5, PM10, nitrogen dioxide, ozone, and European Air Quality Index (European AQI).

Note: Open-Meteo provides forecast data for these endpoints. These values should not be interpreted as direct measurements from local monitoring stations.

Project Structure

weather-air-quality-etl/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── sql/
│   ├── schema.sql
│   └── analytics.sql
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── validate.py
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md

Installation and Setup

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd weather-air-quality-etl

2. Create a virtual environment

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

python -m pip install -r requirements.txt

4. Configure environment variables

Create a .env file containing the PostgreSQL password expected by docker-compose.yml:

POSTGRES_PASSWORD=your_password

Use a secure password and do not commit .env to Git.

5. Start PostgreSQL

docker compose up -d

The database is configured on host port 5433.

Run the Pipeline

Execute the complete pipeline with:

python src/main.py

The orchestration runs the following stages:

1. Extract: retrieve API data and save raw JSON files.
2. Transform: clean and convert the data into CSV files.
3. Load: create the database schema and load data into PostgreSQL.
4. Validate: run data quality checks.

The loading process uses upserts to update existing observations instead of creating duplicate records for the same city and timestamp.

Data Quality and Analytics

The project includes validation checks for:

* Presence of data in the database tables
* Missing observation timestamps
* Invalid humidity values
* Negative precipitation, wind speed, and air quality measurements
* Duplicate city and timestamp combinations

SQL queries provide summaries of weather conditions, average and maximum European AQI, high-AQI periods, and missing values.

Logging and Automation

Pipeline execution logs are stored in logs/etl.log.

On macOS, cron can schedule automatic execution. The current local setup is configured to run daily at 08:00, provided the Mac is available and the PostgreSQL service is running.

Key Engineering Concepts

* ETL pipeline design
* API data ingestion
* Data cleaning and transformation
* Relational database modeling
* Idempotent data loading
* Data quality validation
* SQL analytics
* Docker-based database deployment
* Pipeline orchestration, logging, and scheduling

Future Improvements

* Add unit and integration tests.
* Build a Power BI dashboard for weather and air quality trends.
* Add retry logic and API failure handling.
* Deploy the pipeline to a cloud environment.
* Introduce workflow orchestration with a dedicated scheduling tool.

Author
JADE-DINE ALABI

Big Data and AI student interested in Data Engineering, Data Analytics, and Business Intelligence.