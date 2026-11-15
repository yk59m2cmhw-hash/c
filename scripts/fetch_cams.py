#!/usr/bin/env python3
"""Download hourly PM2.5 of the CAMS global atmospheric model for the monitor's grid cell (no API key).

Source : https://open-meteo.com/en/docs/air-quality-api  (CAMS global forecasts, Copernicus Atmosphere
         Monitoring Service; these are MODEL ESTIMATES, not measurements)
Output : data/raw/cams_openmeteo_almaty_pm25_hourly.csv   (datetime_utc, cams_pm25)

The archive starts in August 2022 and keeps the freshest model runs for past days.

    python scripts/fetch_cams.py [end=yesterday]
"""
import csv
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
API = "https://air-quality-api.open-meteo.com/v1/air-quality"
MONITOR_LAT, MONITOR_LON = 43.252855, 76.93118          # the reference monitor (OpenAQ location 8876)
START = date(2022, 8, 1)


def get_hourly(start: date, stop: date) -> dict:
    params = dict(latitude=MONITOR_LAT, longitude=MONITOR_LON, start_date=str(start), end_date=str(stop),
                  hourly="pm2_5", timezone="GMT")
    last = None
    for attempt in range(20):
        try:
            r = requests.get(API, params=params, timeout=180)
            if r.status_code == 200:
                return r.json()["hourly"]
            last = f"HTTP {r.status_code}: {r.text[:120]}"
        except requests.RequestException as exc:
            last = repr(exc)[:160]
        print(f"  attempt {attempt + 1} failed ({last}); retrying", flush=True)
        time.sleep(3 + 2 * min(attempt, 6))
    raise SystemExit(f"failed: {last}")


def main(end: str | None = None) -> None:
    last_day = date.fromisoformat(end) if end else datetime.now(timezone.utc).date() - timedelta(days=1)
    rows, start = [], START
    while start <= last_day:                                # the API serves at most about a year per request
        stop = min(last_day, start + timedelta(days=364))
        hourly = get_hourly(start, stop)
        rows += [(t.replace("T", " "), v) for t, v in zip(hourly["time"], hourly["pm2_5"]) if v is not None]
        start = stop + timedelta(days=1)
    out = RAW / "cams_openmeteo_almaty_pm25_hourly.csv"
    with out.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["datetime_utc", "cams_pm25"])
        writer.writerows(rows)
    print(f"saved {out.name}: {len(rows)} hourly values, {rows[0][0]} .. {rows[-1][0]}")


if __name__ == "__main__":
    main(*sys.argv[1:2])
