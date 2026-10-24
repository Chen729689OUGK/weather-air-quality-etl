# Weather and Air Quality ETL Pipeline

An automated ETL pipeline that collects weather and air quality forecast data for Fes, Morocco, transforms it into structured datasets, stores it in PostgreSQL, and validates data quality.

## Overview

This project demonstrates an end-to-end data engineering workflow using Python, REST APIs, PostgreSQL, SQL, and Docker Compose. The pipeline can be scheduled daily on macOS using cron.


The pipeline is orchestrated with Python and can be scheduled to run automatically using cron on macOS.

## Objectives

* Retrieve weather and air quality data from public APIs.
* Transform raw JSON responses into clean, structured datasets.
* Load observations into a PostgreSQL database.
* Validate data quality and prevent duplicate records.
* Perform analytical queries using SQL.
* Automate execution and maintain logs.

## Architecture

```text

+---------------------------+
|       Open-Meteo APIs     |
| Weather & Air Quality     |
+-------------+-------------+
              |
              v
+---------------------------+
| EXTRACT                   |
| Retrieve API responses    |
| Save raw JSON data        |
+-------------+-------------+
              |
              v
+---------------------------+
| TRANSFORM                 |
| Clean and structure data  |
| Generate processed CSVs   |
+-------------+-------------+
              |
              v
+---------------------------+
| LOAD                      |
| Insert data into          |
| PostgreSQL                |
+-------------+-------------+
              |
              v
+---------------------------+
| VALIDATE                  |
| Run data quality checks   |
+-------------+-------------+
              |
              v
+---------------------------+
| SQL Analytics             |
| Weather and air quality   |
| summaries                 |
+---------------------------+
Orchestration : Python
Database      : PostgreSQL
Deployment    : Docker Compose
Scheduling    : cron
Logging       : logs/

```

## Technologies

* Python — pipeline orchestration and data processing
* Pandas — data cleaning and transformation
* Requests — API communication
* Open-Meteo APIs — weather and air quality forecasts
* PostgreSQL — relational data storage
* Docker Compose — database deployment
* SQL — analytics and validation
* cron — scheduled execution on macOS

## Data Sources

The pipeline retrieves forecast data for Fes, Morocco, using the Open-Meteo weather and air quality APIs.

Weather variables include temperature, relative humidity, precipitation, and wind speed.

Air quality variables include PM2.5, PM10, nitrogen dioxide, ozone, and the European Air Quality Index (European AQI).

Important: These API values are forecast data and should not be interpreted as direct measurements from local monitoring stations.

## Project Structure

```text

weather-air-quality-etl/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── validate.py
│   └── main.py
├── sql/
│   ├── schema.sql
│   └── analytics.sql
├── tests/
├── data/
├── logs/
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md

```

## Installation and Setup

### 1. Clone the repository

```bash

git clone https://github.com/Chen729689OUGK/weather-air-quality-etl.git
cd weather-air-quality-etl

```

### 2. Create and activate a virtual environment

```bash

python3 -m venv .venv
source .venv/bin/activate

```

### 3. Install dependencies

```bash

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

```

### 4. Configure environment variables

Create a .env file in the project root with the PostgreSQL password expected by docker-compose.yml.

```bash

cat > .env <<'EOF'
POSTGRES_PASSWORD=your_secure_password
EOF

```

Replace your_secure_password with your own secure password. Never commit your .env file to GitHub.

### 5. Start PostgreSQL

```bash

docker compose up -d

```

The database is configured on host port 5433.

## Run the Pipeline

Execute the complete pipeline with:

The database is exposed on host port 5433.

### 6. Run the ETL pipeline:

```bash

python src/main.py

```

### 7. Stop PostgreSQL

```bash

docker compose down

```

## Pipeline Workflow

The pipeline executes four main stages:

 1. Extract: retrieve weather and air quality data from the APIs and save raw JSON files.
 2. Transform: clean the data and generate structured CSV files.
 3. Load: create the database schema and load observations into PostgreSQL.
 4. Validate: check database contents and data quality rules.

## Data Quality and Analytics

The loading process uses upserts to update existing observations instead of creating duplicates for the same city and timestamp.

## Data Quality and SQL Analytics

The validation stage checks:

* Data availability in database tables
* Missing observation timestamps
* Invalid humidity values
* Negative precipitation, wind speed, and air quality measurements
* Duplicate city and timestamp combinations

The SQL scripts also support analytical queries on weather conditions, European AQI summaries, high-AQI periods, and missing values.

## Logging and Automation

Execution logs are stored locally in logs/etl.log.

The pipeline can be scheduled using macOS cron. The current local configuration is intended to run daily at 08:00, provided the Mac is available and the PostgreSQL service is running.

## Key Engineering Concepts

* ETL pipeline design
* REST API ingestion
* Data cleaning and transformation
* Relational database modeling
* Idempotent data loading
* Data quality validation
* SQL analytics
* Docker-based database deployment
* Logging and scheduled automation

## Future Improvements

* Expand automated unit and integration tests
* Build a Power BI dashboard for weather and air quality trends
* Add retry logic and API failure handling
* Deploy the pipeline to a cloud environment
* Introduce a dedicated workflow orchestration tool

## Screenshots

### 1.ETL Pipeline Execution

Successful execution of the ETL pipeline, including data extraction, transformation, validation, and loading.

### 2.PostgresSQL Data Storage

Verification of weather observations successfully stored in the PostgreSQL database.


Author

JADE-DINE ALABI

Big Data and AI student interested in Data Engineering, Data Analytics, and Business Intelligence.
