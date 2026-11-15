#!/usr/bin/env python3
"""Download REAL archived weather forecasts for the test period (Open-Meteo Previous Runs API, no key).

For every hour the API returns the value from the latest model run AND the value that had been
forecast 1 day earlier (`_previous_day1`) and 2 days earlier (`_previous_day2`).
We use the older forecasts to test the model with weather that was truly known in advance.

Source : https://open-meteo.com/en/docs/previous-runs-api   (data licence: CC BY 4.0)
Output : data/raw/forecast_archive_city.csv
"""
import time
from pathlib import Path

import pandas as pd
import requests

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
API = "https://previous-runs-api.open-meteo.com/v1/forecast"
VARS = ["temperature_2m", "relative_humidity_2m", "surface_pressure", "precipitation", "snowfall",
        "cloud_cover", "shortwave_radiation", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]


def main():
    hourly = ",".join(v + s for v in VARS for s in ("", "_previous_day1", "_previous_day2"))
    params = dict(latitude=43.2529, longitude=76.9312, start_date="2024-09-25", end_date="2025-11-15",
                  hourly=hourly, models="best_match", timezone="UTC", wind_speed_unit="ms")
    last = None
    for attempt in range(25):
        try:
            r = requests.get(API, params=params, timeout=180)
            if r.status_code == 200:
                j = r.json()
                df = pd.DataFrame(j["hourly"]).rename(columns={"time": "utc_time"})
                df.to_csv(RAW / "forecast_archive_city.csv", index=False)
                print(f"saved {len(df)} hourly rows; grid=({j['latitude']}, {j['longitude']}); "
                      f"nulls per column (max): {int(df.isna().sum().max())}")
                print(df.isna().sum()[df.isna().sum() > 0].to_string())
                return
            last = f"HTTP {r.status_code}: {r.text[:120]}"
        except requests.RequestException as exc:
            last = repr(exc)[:160]
        print(f"  attempt {attempt + 1} failed ({last}); retrying", flush=True)
        time.sleep(3 + 2 * min(attempt, 6))
    raise SystemExit(f"failed: {last}")


if __name__ == "__main__":
    main()
