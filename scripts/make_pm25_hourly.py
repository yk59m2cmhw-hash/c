#!/usr/bin/env python3
"""Aggregate the OpenAQ archive files of location 8876 (Almaty, AirNow feed)
to daily means and print feasibility statistics.

Run:  python3 -I analyze_almaty_pm25.py [data_dir] [out_daily_csv]

Rules (as requested):
  * hourly values < 0 or > 2000 ug/m3 are dropped
  * local day = Asia/Almaty calendar day (zoneinfo: UTC+6 until 2024-02-29, UTC+5 from 2024-03-01)
  * OpenAQ archive timestamps are treated as HOUR-ENDING (each daily file holds
    01:00 ... 00:00(+1 day) local), so 1 h is subtracted before assigning the day
  * a day is valid when it has >= 18 valid hourly values
  * winter = 1 Oct .. 31 Mar, labelled by its starting year (e.g. 2024/25)
Input files are untrusted: they are parsed with gzip+csv only, nothing is executed.
"""
import csv
import gzip
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "openaq_8876")
OUT_DAILY = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "almaty_pm25_daily.csv")
OUT_HOURLY = os.path.join(os.path.dirname(OUT_DAILY), "almaty_pm25_hourly.csv")
LOCATION_ID = "8876"
TZ = ZoneInfo("Asia/Almaty")
MIN_HOURS = 18
THRESH = 35.0

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)


def read_all(data_dir):
    rows = []
    meta = {"files": 0, "bad_rows": 0, "other_param": 0}
    seen = {"location": set(), "sensors_id": set(), "latlon": set(), "parameter": set(), "units": set()}
    for name in sorted(os.listdir(data_dir)):
        if not name.endswith(".csv.gz"):
            continue
        meta["files"] += 1
        with gzip.open(os.path.join(data_dir, name), "rt", encoding="utf-8", errors="replace", newline="") as fh:
            for rec in csv.DictReader(fh):
                try:
                    if rec["location_id"] != LOCATION_ID:
                        meta["bad_rows"] += 1
                        continue
                    seen["parameter"].add(rec["parameter"])
                    if rec["parameter"] != "pm25":
                        meta["other_param"] += 1
                        continue
                    seen["location"].add(rec["location"])
                    seen["sensors_id"].add(rec["sensors_id"])
                    seen["latlon"].add((rec["lat"], rec["lon"]))
                    seen["units"].add(rec["units"])
                    rows.append((rec["datetime"], float(rec["value"])))
                except (KeyError, ValueError, TypeError):
                    meta["bad_rows"] += 1
    return rows, meta, seen


def main():
    rows, meta, seen = read_all(DATA_DIR)
    print(f"files read: {meta['files']}, hourly rows: {len(rows)}, unparsable rows: {meta['bad_rows']}, non-pm25 rows: {meta['other_param']}")
    print("location names:", sorted(seen["location"]), "| sensors:", sorted(seen["sensors_id"]),
          "| lat/lon:", sorted(seen["latlon"]), "| parameters:", sorted(seen["parameter"]), "| units:", sorted(seen["units"]))

    df = pd.DataFrame(rows, columns=["datetime", "value"])
    df["offset"] = df["datetime"].str[-6:]
    df["utc_end"] = pd.to_datetime(df["datetime"], utc=True, format="ISO8601")
    print("UTC offsets found in files (rows):", df["offset"].value_counts().to_dict())
    for off, g in df.groupby("offset"):
        print(f"   offset {off}: {g['datetime'].min()} .. {g['datetime'].max()}")
    print("minute-of-hour values:", sorted(df["utc_end"].dt.minute.unique().tolist()))

    n_dup = int(df.duplicated("utc_end").sum())
    df = df.sort_values("utc_end").drop_duplicates("utc_end", keep="last")
    n_neg = int((df["value"] < 0).sum())
    n_big = int((df["value"] > 2000).sum())
    print(f"duplicate timestamps removed: {n_dup}; negative values dropped: {n_neg}; values > 2000 dropped: {n_big}")
    print("raw value range before filtering: min", df["value"].min(), "max", df["value"].max())
    df = df[(df["value"] >= 0) & (df["value"] <= 2000)].copy()

    # hour-ending -> hour-beginning, then Asia/Almaty local calendar day
    df["utc_start"] = df["utc_end"] - pd.Timedelta(hours=1)
    df["local_start"] = df["utc_start"].dt.tz_convert(TZ)
    df["date"] = df["local_start"].dt.date
    print(f"valid hourly values: {len(df)}; first hour (local start) {df['local_start'].min()}, last {df['local_start'].max()}")

    # hourly file for downstream use
    df[["utc_start", "local_start", "value"]].rename(columns={"value": "pm25"}).to_csv(OUT_HOURLY, index=False)

    g = df.groupby("date")["value"]
    daily = pd.DataFrame({"n_hours": g.count(), "mean_all": g.mean(), "pm25_max": g.max()})
    full_idx = pd.date_range(min(daily.index), max(daily.index), freq="D").date
    daily = daily.reindex(full_idx)
    daily.index.name = "date"
    daily["n_hours"] = daily["n_hours"].fillna(0).astype(int)
    daily["valid"] = daily["n_hours"] >= MIN_HOURS
    daily["pm25_mean"] = daily["mean_all"].where(daily["valid"]).round(2)
    daily["pm25_max"] = daily["pm25_max"].where(daily["valid"])
    out = daily[["pm25_mean", "pm25_max", "n_hours", "valid"]]
    out.to_csv(OUT_DAILY)

    d = out.copy()
    d.index = pd.to_datetime(d.index)
    print("\n=== DATE RANGE ===")
    print(f"daily series (Asia/Almaty local days): {d.index.min().date()} .. {d.index.max().date()} "
          f"({len(d)} calendar days, {int(d['valid'].sum())} valid = {100 * d['valid'].mean():.1f}% of span)")
    v = d[d["valid"]]
    print(f"first valid day {v.index.min().date()}, last valid day {v.index.max().date()}")

    print("\n=== % OF DAYS WITH VALID DATA PER YEAR (valid = >=18 h) ===")
    for y, gy in d.groupby(d.index.year):
        days_in_year = 366 if pd.Timestamp(year=y, month=1, day=1).is_leap_year else 365
        print(f"{y}: valid {int(gy['valid'].sum()):3d} / {days_in_year} calendar days = {100 * gy['valid'].sum() / days_in_year:5.1f}%"
              f"   (within data span {gy.index.min().date()}..{gy.index.max().date()}: {100 * gy['valid'].mean():5.1f}%)")

    print("\n=== MONTHLY MEAN PM2.5 (ug/m3; mean of valid daily means; '(n)' = valid days) ===")
    mm = v["pm25_mean"].groupby([v.index.year, v.index.month]).agg(["mean", "count"])
    tab = mm["mean"].unstack(1).round(1)
    cnt = mm["count"].unstack(1)
    tab.index.name = "year"
    tab.columns = [f"{m:02d}" for m in tab.columns]
    print(tab.to_string(na_rep="  -"))
    print("valid days per month:")
    cnt.index.name = "year"
    cnt.columns = [f"{m:02d}" for m in cnt.columns]
    print(cnt.fillna(0).astype(int).to_string())
    clim = v["pm25_mean"].groupby(v.index.month).mean().round(1)
    print("all-years mean by calendar month:", {f"{m:02d}": float(x) for m, x in clim.items()})

    print("\n=== WINTERS (1 Oct .. 31 Mar) ===")
    wy = np.where(d.index.month >= 10, d.index.year, np.where(d.index.month <= 3, d.index.year - 1, -1))
    d["winter"] = wy
    d["prev"] = d["pm25_mean"].shift(1)  # calendar-consecutive because index is a complete daily range
    results = []
    for w in sorted(x for x in set(wy) if x != -1):
        gw = d[d["winter"] == w]
        start, end = pd.Timestamp(w, 10, 1), pd.Timestamp(w + 1, 3, 31)
        n_cal = (end - start).days + 1
        nvalid = int(gw["valid"].sum())
        n_exc = int((gw["pm25_mean"] > THRESH).sum())
        pairs = gw.dropna(subset=["pm25_mean", "prev"])
        mae = float((pairs["pm25_mean"] - pairs["prev"]).abs().mean()) if len(pairs) else float("nan")
        rmse = float(np.sqrt(((pairs["pm25_mean"] - pairs["prev"]) ** 2).mean())) if len(pairs) else float("nan")
        complete = (d.index.min() <= start) and (d.index.max() >= end) and nvalid / n_cal >= 0.9
        results.append((w, n_cal, nvalid, n_exc, len(pairs), mae, rmse, complete, pairs, gw))
        print(f"winter {w}/{str(w + 1)[2:]}: valid days {nvalid:3d}/{n_cal} ({100 * nvalid / n_cal:5.1f}%), "
              f"days with daily mean > {THRESH:g}: {n_exc:3d} ({100 * n_exc / max(nvalid, 1):4.1f}% of valid), "
              f"winter mean {gw['pm25_mean'].mean():5.1f}, max daily {gw['pm25_mean'].max():6.1f}, "
              f"persistence MAE {mae:5.2f} RMSE {rmse:5.2f} (n={len(pairs)})"
              f"{'  [complete: fully inside data range and >=90% valid]' if complete else '  [incomplete]'}")

    comp = [r for r in results if r[7]]
    print("\n=== PERSISTENCE BASELINE (tomorrow = today), MOST RECENT COMPLETE WINTER ===")
    if comp:
        w, n_cal, nvalid, n_exc, n_pairs, mae, rmse, _, pairs, gw = comp[-1]
        print(f"winter {w}/{str(w + 1)[2:]}: MAE = {mae:.2f} ug/m3, RMSE = {rmse:.2f} ug/m3, n = {n_pairs} day pairs "
              f"(both days valid, target day in the winter); mean of target days {pairs['pm25_mean'].mean():.1f}, "
              f"median {pairs['pm25_mean'].median():.1f}")
        obs = pairs["pm25_mean"] > THRESH
        pred = pairs["prev"] > THRESH
        tp, fp = int((obs & pred).sum()), int((~obs & pred).sum())
        fn, tn = int((obs & ~pred).sum()), int((~obs & ~pred).sum())
        print(f"persistence as a '>{THRESH:g} tomorrow' warning: hits {tp}, misses {fn}, false alarms {fp}, correct negatives {tn} "
              f"(recall {tp / max(tp + fn, 1):.2f}, precision {tp / max(tp + fp, 1):.2f})")
    else:
        print("no complete winter found")

    print("\n=== SANITY CHECKS ON THE HOURLY SERIES (is it a live measurement?) ===")
    h = df.set_index("local_start")["value"]
    for y, hy in h.groupby(h.index.year):
        same = (hy.diff() == 0)
        run = (same != same.shift()).cumsum()
        longest = int(same.groupby(run).sum().max()) + 1 if len(hy) else 0
        print(f"{y}: hours {len(hy):5d}, mean {hy.mean():5.1f}, median {hy.median():5.1f}, p95 {hy.quantile(0.95):6.1f}, max {hy.max():6.1f}, "
              f"share of hours equal to previous hour {100 * same.mean():4.1f}%, longest run of identical values {longest} h")

    print(f"\nwrote {OUT_DAILY}\nwrote {OUT_HOURLY}")


if __name__ == "__main__":
    main()
