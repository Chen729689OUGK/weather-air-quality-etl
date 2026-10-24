
CREATE TABLE IF NOT EXISTS weather_observations (
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    observation_time TIMESTAMP NOT NULL,
    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION,
    source VARCHAR(50) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city, observation_time)
);

CREATE TABLE IF NOT EXISTS air_quality_observations (
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    observation_time TIMESTAMP NOT NULL,
    pm2_5 DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    nitrogen_dioxide DOUBLE PRECISION,
    ozone DOUBLE PRECISION,
    european_aqi DOUBLE PRECISION,
    source VARCHAR(50) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city, observation_time)
);

CREATE INDEX IF NOT EXISTS idx_weather_time
    ON weather_observations (observation_time);

CREATE INDEX IF NOT EXISTS idx_air_quality_time
    ON air_quality_observations (observation_time);
