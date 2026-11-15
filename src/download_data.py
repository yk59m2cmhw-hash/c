#!/usr/bin/env python3
"""Download every public dataset used by the project into data/raw/.

No API keys are needed. Sources:
  1. OpenAQ public archive (AWS S3) - hourly PM2.5 from the reference-grade
     monitor "Almaty-8876" (provider: AirNow), 2020-04 .. 2025-11.
  2. Iowa Environmental Mesonet (IEM) - METAR weather reports from Almaty
     airport (ICAO code UAAA), 2020 .. today.
  3. Open-Meteo Air Quality API - PM2.5 from the CAMS global atmospheric
     model for the monitor's grid cell (used only as a comparison baseline).
  4. sensor.community archive - a citizen low-cost sensor (SDS011, id 78340)
     in central Almaty, 2026 (used only as an extra, never-tuned-on test).

Usage:
    python src/download_data.py            # everything
    python src/download_data.py --only openaq metar
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import gzip
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
HEADERS = {"User-Agent": "almaty-air-school-project/1.0 (student hackathon project)"}

OPENAQ_BUCKET = "https://openaq-data-archive.s3.amazonaws.com"
OPENAQ_LOCATION = 8876          # "Almaty-8876", reference-grade PM2.5, provider AirNow
MONITOR_LAT, MONITOR_LON = 43.252855, 76.93118

METAR_STATION = "UAAA"          # Almaty International Airport
METAR_START = dt.date(2020, 1, 1)

CAMS_START = dt.date(2022, 8, 1)  # first day served by the Open-Meteo air-quality API

SENSOR_IDS, SENSOR_TYPE = (78340, 90941), "sds011"   # two sensor.community nodes in Almaty (city centre, west)
SENSOR_START = dt.date(2026, 1, 11)                  # both appear in the archive in mid-January 2026
SENSOR_MIN_READINGS = 6                              # readings needed for an hourly mean (a sensor reports about 24 an hour)


def http_get(url: str, timeout: int = 120, retries: int = 5) -> bytes | None:
    """GET with retries. Returns None for a 404 (file does not exist)."""
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            last = err
        except Exception as err:  # connection reset, timeout, ...
            last = err
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to download {url}: {last}")


# --------------------------------------------------------------------------- #
# 1. OpenAQ archive
# --------------------------------------------------------------------------- #
def list_openaq_keys(location_id: int) -> list[str]:
    keys, token = [], None
    prefix = f"records/csv.gz/locationid={location_id}/"
    while True:
        url = f"{OPENAQ_BUCKET}/?list-type=2&prefix={urllib.parse.quote(prefix, safe='')}"
        if token:
            url += "&continuation-token=" + urllib.parse.quote(token, safe="")
        xml = http_get(url).decode("utf-8")
        keys += re.findall(r"<Key>([^<]+)</Key>", xml)
        match = re.search(r"<NextContinuationToken>([^<]+)</NextContinuationToken>", xml)
        if not match:
            return sorted(keys)
        token = match.group(1)


def download_openaq() -> Path:
    keys = list_openaq_keys(OPENAQ_LOCATION)
    print(f"[openaq] {len(keys)} daily files for location {OPENAQ_LOCATION}")

    def fetch(key: str) -> list[tuple[str, str]]:
        blob = http_get(f"{OPENAQ_BUCKET}/{key}")
        text = gzip.decompress(blob).decode("utf-8")
        out = []
        for row in csv.DictReader(io.StringIO(text)):
            if row["parameter"] == "pm25":
                # timestamps carry the local UTC offset; store them in UTC
                stamp = dt.datetime.fromisoformat(row["datetime"]).astimezone(dt.timezone.utc)
                out.append((stamp.strftime("%Y-%m-%d %H:%M"), row["value"]))
        return out

    rows: list[tuple[str, str]] = []
    with cf.ThreadPoolExecutor(max_workers=12) as pool:
        for chunk in pool.map(fetch, keys):
            rows += chunk
    rows = sorted(set(rows))
    path = RAW / "openaq_almaty_8876_pm25_hourly.csv"
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["datetime_utc", "pm25"])
        writer.writerows(rows)
    print(f"[openaq] {len(rows)} hourly values, {rows[0][0]} .. {rows[-1][0]} -> {path.name}")
    return path


# --------------------------------------------------------------------------- #
# 2. METAR weather observations (IEM)
# --------------------------------------------------------------------------- #
def download_metar() -> Path:
    end = dt.date.today() + dt.timedelta(days=1)
    fields = ["tmpc", "dwpc", "relh", "drct", "sknt", "gust", "alti", "vsby", "wxcodes", "skyc1", "skyl1"]
    query = [("station", METAR_STATION)] + [("data", f) for f in fields] + [
        ("year1", METAR_START.year), ("month1", METAR_START.month), ("day1", METAR_START.day),
        ("year2", end.year), ("month2", end.month), ("day2", end.day),
        ("tz", "Etc/UTC"), ("format", "onlycomma"), ("latlon", "no"), ("missing", "M"),
        ("trace", "T"), ("direct", "no"), ("report_type", 3), ("report_type", 4),
    ]
    url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?" + urllib.parse.urlencode(query)
    blob = http_get(url, timeout=600)
    lines = blob.decode("utf-8").strip().splitlines()
    path = RAW / "iem_uaaa_metar.csv.gz"
    with gzip.open(path, "wt", newline="") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[metar] {len(lines) - 1} reports, {lines[1].split(',')[1]} .. {lines[-1].split(',')[1]} -> {path.name}")
    return path


# --------------------------------------------------------------------------- #
# 3. CAMS global model PM2.5 (Open-Meteo air-quality API)
# --------------------------------------------------------------------------- #
def download_cams() -> Path:
    end = dt.date.today() - dt.timedelta(days=1)
    rows, start = [], CAMS_START
    while start <= end:
        stop = min(end, start + dt.timedelta(days=364))
        url = ("https://air-quality-api.open-meteo.com/v1/air-quality?"
               f"latitude={MONITOR_LAT}&longitude={MONITOR_LON}&start_date={start}&end_date={stop}"
               "&hourly=pm2_5&timezone=GMT")
        hourly = json.loads(http_get(url))["hourly"]
        rows += [(t.replace("T", " "), v) for t, v in zip(hourly["time"], hourly["pm2_5"]) if v is not None]
        start = stop + dt.timedelta(days=1)
    path = RAW / "cams_openmeteo_almaty_pm25_hourly.csv"
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["datetime_utc", "cams_pm25"])
        writer.writerows(rows)
    print(f"[cams] {len(rows)} hourly values, {rows[0][0]} .. {rows[-1][0]} -> {path.name}")
    return path


# --------------------------------------------------------------------------- #
# 4. Citizen sensors (sensor.community archive, one small CSV per sensor per day)
# --------------------------------------------------------------------------- #
def citizen_hourly(sensor_id: int, cache: Path) -> Path:
    """Hourly PM2.5 means from the cached daily files of one sensor (no network)."""
    hourly: dict[str, list[float]] = {}
    for file in sorted(cache.glob(f"*_sensor_{sensor_id}.csv")):
        for row in csv.DictReader(io.StringIO(file.read_text()), delimiter=";"):
            try:
                value = float(row["P2"])                      # P2 = PM2.5 in ug/m3
            except (ValueError, KeyError, TypeError):
                continue
            if 0 <= value < 999:                              # 999.9 is the sensor's "out of range" reading
                hourly.setdefault(row["timestamp"][:13], []).append(value)
    rows = [[hour.replace("T", " ") + ":00", f"{sum(v) / len(v):.2f}", str(len(v))]
            for hour, v in sorted(hourly.items()) if len(v) >= SENSOR_MIN_READINGS]
    path = RAW / f"sensor_community_{sensor_id}_pm25_hourly.csv"
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["datetime_utc", "pm25", "n_readings"])
        writer.writerows(rows)
    days = len({r[0][:10] for r in rows})
    print(f"[citizen {sensor_id}] {len(rows)} hourly means on {days} days -> {path.name}")
    return path


def download_citizen_sensor() -> Path:
    """Daily files are cached in data/cache/ so an interrupted run can resume.

    The volunteer-run archive is slow and often resets connections (about 2-6 files a minute
    from our machine), so a day that cannot be fetched is skipped, reported, and can be
    filled in by running again. One connection at a time, to be polite.
    """
    cache = RAW.parent / "cache" / "sensor_community"
    cache.mkdir(parents=True, exist_ok=True)
    end = dt.date.today() - dt.timedelta(days=1)
    path = None
    for sensor_id in SENSOR_IDS:
        day, fetched, missing, failed = SENSOR_START, 0, 0, 0
        while day <= end:
            key = day.isoformat()
            target = cache / f"{key}_{SENSOR_TYPE}_sensor_{sensor_id}.csv"
            absent = target.with_suffix(".csv.missing")
            if not target.exists() and not absent.exists():
                url = f"https://archive.sensor.community/{key}/{target.name}"
                try:
                    blob = http_get(url, timeout=60, retries=3)
                except RuntimeError:
                    failed += 1
                    time.sleep(8)
                else:
                    if blob is None:
                        missing += 1
                        absent.write_bytes(b"")      # remember that this day does not exist
                    else:
                        fetched += 1
                        target.write_bytes(blob)
                    time.sleep(1.0)
            day += dt.timedelta(days=1)
        print(f"[citizen {sensor_id}] {fetched} new daily files, {missing} days absent, {failed} days failed (rerun to retry)")
        path = citizen_hourly(sensor_id, cache)
    return path


STEPS = {"openaq": download_openaq, "metar": download_metar, "cams": download_cams, "citizen": download_citizen_sensor}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="+", choices=list(STEPS), help="download only these sources")
    args = parser.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    for name in args.only or list(STEPS):
        try:
            STEPS[name]()
        except Exception as err:
            print(f"[{name}] FAILED: {err}", file=sys.stderr)
            raise


if __name__ == "__main__":
    main()
