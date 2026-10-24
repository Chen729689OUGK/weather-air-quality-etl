
-- 1. Number of records in each table
SELECT 'Weather' AS dataset, COUNT(*) AS total_records
FROM weather_observations
UNION ALL
SELECT 'Air Quality', COUNT(*)
FROM air_quality_observations;


-- 2. Average weather conditions
SELECT
    city,
    ROUND(AVG(temperature_2m)::numeric, 2) AS avg_temperature,
    ROUND(AVG(relative_humidity_2m)::numeric, 2) AS avg_humidity,
    ROUND(AVG(wind_speed_10m)::numeric, 2) AS avg_wind_speed
FROM weather_observations
GROUP BY city;


-- 3. Hourly air-quality overview
SELECT
    city,
    ROUND(AVG(pm2_5)::numeric, 2) AS avg_pm25,
    ROUND(AVG(pm10)::numeric, 2) AS avg_pm10,
    ROUND(AVG(european_aqi)::numeric, 2) AS avg_european_aqi,
    MAX(european_aqi) AS max_european_aqi
FROM air_quality_observations
GROUP BY city;


-- 4. Hours with the highest European AQI
SELECT
    city,
    observation_time,
    pm2_5,
    pm10,
    european_aqi
FROM air_quality_observations
WHERE european_aqi IS NOT NULL
ORDER BY european_aqi DESC
LIMIT 10;


-- 5. Missing values in weather measurements
SELECT
    COUNT(*) FILTER (WHERE temperature_2m IS NULL)
        AS missing_temperature,
    COUNT(*) FILTER (WHERE relative_humidity_2m IS NULL)
        AS missing_humidity,
    COUNT(*) FILTER (WHERE precipitation IS NULL)
        AS missing_precipitation,
    COUNT(*) FILTER (WHERE wind_speed_10m IS NULL)
        AS missing_wind_speed
FROM weather_observations;


-- 6. Check for duplicate city/timestamp combinations
SELECT city, observation_time, COUNT(*) AS occurrences
FROM weather_observations
GROUP BY city, observation_time
HAVING COUNT(*) > 1;
