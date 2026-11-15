#!/usr/bin/env python3
"""Download one citizen-science PM2.5 sensor from the public sensor.community archive (no API key)
and turn its readings into an hourly table.

Source  : https://archive.sensor.community/  (one CSV file per sensor per day; licence: Open Database License, ODbL)
Sensor  : SDS011 no. 78340, central Almaty (43.2474 N, 76.9569 E), a low-cost optical sensor
Output  : data/raw/citizen_sds011_78340_hourly.csv   (utc_start, local_start, pm25, n_readings)

The cleaning rules below were fixed BEFORE any forecast was scored on this sensor:
  * a reading is dropped if PM2.5 is negative or above 2000 µg/m³ (same glitch rule as the reference monitor);
  * an hourly value is the mean of the readings in that hour and needs at least 6 readings
    (the sensor reports about every 2.5 minutes);
  * no humidity or calibration correction is applied.

    python scripts/fetch_citizen_sensor.py [start=2025-01-01] [end=yesterday]
"""
import io
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "cache" / "sensor_community"          # daily files as downloaded (not committed)
OUT = ROOT / "data" / "raw" / "citizen_sds011_78340_hourly.csv"
SENSOR_ID, SENSOR_TYPE = 78340, "sds011"
MIN_READINGS_PER_HOUR = 6
URL = "https://archive.sensor.community/{day}/{day}_{kind}_sensor_{sid}.csv"


def fetch_day(day: str) -> str:
    """Download one daily file. Returns 'cached', 'ok', 'missing' (no file that day) or 'failed'."""
    path = CACHE / f"{day}.csv"
    if path.exists():
        return "cached"
    url = URL.format(day=day, kind=SENSOR_TYPE, sid=SENSOR_ID)
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=90)
            if r.status_code == 200 and r.text.startswith("sensor_id"):
                path.write_text(r.text)
                return "ok"
            if r.status_code == 404:
                path.with_suffix(".missing").touch()
                return "missing"
        except requests.RequestException:
            pass
        time.sleep(2 + 2 * attempt)
    return "failed"


def hourly_table() -> pd.DataFrame:
    frames = []
    for path in sorted(CACHE.glob("*.csv")):
        df = pd.read_csv(io.StringIO(path.read_text()), sep=";", usecols=["timestamp", "P2"])
        frames.append(df)
    raw = pd.concat(frames, ignore_index=True)
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], errors="coerce")           # UTC
    raw["P2"] = pd.to_numeric(raw["P2"], errors="coerce")
    raw = raw.dropna()
    raw = raw[(raw["P2"] >= 0) & (raw["P2"] <= 2000)]
    grouped = raw.groupby(raw["timestamp"].dt.floor("h"))["P2"]
    hourly = pd.DataFrame({"pm25": grouped.mean().round(2), "n_readings": grouped.count()})
    hourly = hourly[hourly["n_readings"] >= MIN_READINGS_PER_HOUR]
    hourly.index.name = "utc_start"
    out = hourly.reset_index()
    out.insert(1, "local_start", out["utc_start"] + pd.Timedelta(hours=5))           # Almaty has been UTC+5 since 1 March 2024
    return out


def main(start: str = "2025-01-01", end: str | None = None) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    last = date.fromisoformat(end) if end else datetime.now(timezone.utc).date() - timedelta(days=1)
    days = [str(d.date()) for d in pd.date_range(start, last, freq="D")
            if not (CACHE / f"{d.date()}.missing").exists()]
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch_day, days))
    print({status: results.count(status) for status in sorted(set(results))}, flush=True)
    table = hourly_table()
    table.to_csv(OUT, index=False)
    print(f"saved {OUT.name}: {len(table):,} hourly values, {table['utc_start'].min()} .. {table['utc_start'].max()} (UTC)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
