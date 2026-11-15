#!/usr/bin/env python3
"""Download hourly weather for Almaty (city + mountain grid cell) from the
Open-Meteo Historical Weather API (no API key).

Source  : https://open-meteo.com/en/docs/historical-weather-api  (data licence: CC BY 4.0)
Model   : ECMWF IFS 9 km (analysis + short-range forecasts, available from 2017)
Outputs : data/raw/weather_city_ifs.csv, data/raw/weather_mountain_ifs.csv

The free API is rate-limited per IP address, so every request is retried.
"""
import sys
import time
from pathlib import Path

import pandas as pd
import requests

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
API = "https://archive-api.open-meteo.com/v1/archive"
START, END = "2020-04-01", "2025-11-15"

CITY = dict(name="city", latitude=43.2529, longitude=76.9312)        # same point as the PM2.5 monitor
MOUNTAIN = dict(name="mountain", latitude=43.128, longitude=77.081)  # Shymbulak ski area above the city

CITY_VARS = ("temperature_2m,relative_humidity_2m,dew_point_2m,surface_pressure,precipitation,"
             "snowfall,snow_depth,cloud_cover,cloud_cover_low,shortwave_radiation,wind_speed_10m,"
             "wind_direction_10m,wind_gusts_10m,boundary_layer_height")
MOUNTAIN_VARS = "temperature_2m,wind_speed_10m"


def get_json(params, tries=25):
    last = None
    for attempt in range(tries):
        try:
            r = requests.get(API, params=params, timeout=180)
            if r.status_code == 200:
                return r.json()
            last = f"HTTP {r.status_code}: {r.text[:120]}"
        except requests.RequestException as exc:
            last = repr(exc)[:160]
        print(f"  attempt {attempt + 1} failed ({last}); retrying", flush=True)
        time.sleep(3 + 2 * min(attempt, 6))
    raise RuntimeError(f"request failed after {tries} tries: {last}")


def fetch(point, variables, model, raw_grid_cell):
    params = dict(latitude=point["latitude"], longitude=point["longitude"], start_date=START,
                  end_date=END, hourly=variables, models=model, timezone="UTC",
                  wind_speed_unit="ms")
    if raw_grid_cell:
        # "nan" switches off Open-Meteo's height correction: we want the temperature of the
        # model's own (high) grid cell, not a value adjusted down to the valley.
        params["elevation"] = "nan"
    j = get_json(params)
    df = pd.DataFrame(j["hourly"]).rename(columns={"time": "utc_time"})
    meta = dict(grid_latitude=j["latitude"], grid_longitude=j["longitude"], grid_elevation_m=j["elevation"], model=model)
    return df, meta


def main(model="ecmwf_ifs", tag="ifs"):
    RAW.mkdir(parents=True, exist_ok=True)
    for point, variables, raw_cell in ((CITY, CITY_VARS, False), (MOUNTAIN, MOUNTAIN_VARS, True)):
        out = RAW / f"weather_{point['name']}_{tag}.csv"
        print(f"fetching {point['name']} ({model}) ...", flush=True)
        df, meta = fetch(point, variables, model, raw_cell)
        df.to_csv(out, index=False)
        print(f"  saved {out.name}: {len(df)} hourly rows, {df['utc_time'].iloc[0]} .. {df['utc_time'].iloc[-1]}, meta={meta}")
        pd.Series(meta).to_json(RAW / f"weather_{point['name']}_{tag}_meta.json")
        time.sleep(2)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("ecmwf_ifs", "ifs")))
