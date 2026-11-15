# How the raw data files were made

None of the scripts needs an API key. The notebook itself never calls an API: it reads the saved files in `data/raw/`.

| Script | What it does | Output in `data/raw/` |
|---|---|---|
| `fetch_pm25.py` | Downloads the daily files of OpenAQ location 8876 from the public OpenAQ archive | (daily files) |
| `make_pm25_hourly.py <folder> <out.csv>` | Cleans them and writes the hourly table | `almaty_pm25_hourly_openaq8876.csv` |
| `fetch_weather.py` | Hourly weather for the city and a mountain grid cell (Open-Meteo Historical Weather API, ECMWF IFS 9 km) | `weather_city_ifs.csv`, `weather_mountain_ifs.csv` |
| `fetch_forecast_archive.py` | Real archived forecasts for the test period (Open-Meteo Previous Runs API) | `forecast_archive_city.csv` |
| `fetch_forecast_archive.py 2026-01-01 2026-11-17 forecast_archive_city_2026.csv` | The same for 2026 | `forecast_archive_city_2026.csv` |
| `fetch_cams.py` | PM2.5 of the CAMS global model for the monitor's grid cell (Open-Meteo Air Quality API; model estimates, not measurements) | `cams_openmeteo_almaty_pm25_hourly.csv` |
| `fetch_citizen_sensor.py 2026-01-01 2026-11-14` | Daily files of the citizen sensor (sensor.community archive, SDS011 no. 78340) and their hourly averages | `citizen_sds011_78340_hourly.csv` |

The free Open-Meteo API limits requests per IP address, so the weather scripts retry.
