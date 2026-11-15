# How the raw data files were made

All four scripts need no API key. The notebook itself never calls an API: it reads the saved files in `data/raw/`.

| Script | What it does |
|---|---|
| `fetch_pm25.py` | Downloads the daily files of OpenAQ location 8876 from the public OpenAQ archive |
| `make_pm25_hourly.py <folder> <out.csv>` | Cleans them and writes the hourly table (`almaty_pm25_hourly.csv` next to `<out.csv>`; saved in the repo as `almaty_pm25_hourly_openaq8876.csv`) |
| `fetch_weather.py` | Hourly weather for the city and a mountain grid cell (Open-Meteo Historical Weather API, ECMWF IFS 9 km) |
| `fetch_forecast_archive.py` | Real archived forecasts for the test period (Open-Meteo Previous Runs API) |

The free Open-Meteo API limits requests per IP address, so the weather scripts retry.
