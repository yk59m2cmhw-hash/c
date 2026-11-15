#!/usr/bin/env python3
"""Forecast the REAL tomorrow, with no PM2.5 sensor at all.

    python src/live.py

The public record of the reference monitor we trained on ends on 14 Nov 2025,
so the main model cannot be run for the real tomorrow. This script downloads the latest weather
reports from Almaty airport (free, no key) and runs the sensor-free model:
airport weather and the calendar only. The result is written to
results/live_forecast.json.

This forecast cannot be checked against the reference monitor (no public data).
What we do know is how the same kind of model did on the 398 test days of
2024-25; see results/RESULTS.md.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import urllib.parse
import urllib.request

import pandas as pd

import almaty_air as aa

STATION = "UAAA"                 # Almaty International Airport
MIN_DAY_REPORTS = 10             # weather reports needed between 08:00 and 18:00 to call the day "observed"
FIELDS = ["tmpc", "dwpc", "relh", "drct", "sknt", "gust", "alti", "vsby", "wxcodes", "skyc1", "skyl1"]
HEADERS = {"User-Agent": "almaty-air-school-project/1.0 (student hackathon project)"}

# plain-language names for the weather inputs we explain to the user
PLAIN = {
    "temp_min24h": ("coldest temperature in the last 24 hours", "°C"), "temp_day": ("today's daytime temperature", "°C"),
    "temp_change": ("temperature change since yesterday", "°C"), "pressure_day": ("air pressure today", "hPa"),
    "pressure_change": ("pressure change since yesterday", "hPa"), "wind_day": ("today's wind speed", "m/s"),
    "wind_max24h": ("strongest wind in the last 24 hours", "m/s"), "vis_day": ("visibility at the airport today", "km"),
    "vis_min24h": ("worst visibility in the last 24 hours", "km"), "calm_share": ("share of calm reports in the last 24 hours", ""),
    "precip_share": ("rain or snow in the last 24 hours (share of reports)", ""), "fog_share": ("fog or mist in the last 24 hours (share of reports)", ""),
}


def fetch_recent_metar(days: int = 12, timeout: int = 60) -> pd.DataFrame:
    """Raw airport reports for the last `days` days from the Iowa Environmental Mesonet archive."""
    end = dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1)
    start = end - dt.timedelta(days=days + 1)
    query = [("station", STATION)] + [("data", f) for f in FIELDS] + [
        ("year1", start.year), ("month1", start.month), ("day1", start.day),
        ("year2", end.year), ("month2", end.month), ("day2", end.day),
        ("tz", "Etc/UTC"), ("format", "onlycomma"), ("latlon", "no"), ("missing", "M"),
        ("trace", "T"), ("direct", "no"), ("report_type", 3), ("report_type", 4)]
    url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?" + urllib.parse.urlencode(query)
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=timeout) as resp:
        text = resp.read().decode("utf-8")
    return pd.read_csv(io.StringIO(text), na_values=["M"], low_memory=False)


class LiveForecaster:
    """The sensor-free model, trained on every day that has a reference measurement (2020-04 .. 2025-11)."""

    def __init__(self, table: pd.DataFrame | None = None) -> None:
        if table is None:
            table = aa.build_table(aa.load_pm(aa.RAW / "openaq_almaty_8876_pm25_hourly.csv"), aa.load_metar())
        self.features = aa.SENSOR_FREE_FEATURES
        rows = table[table["y"].notna()]
        self.n_train_days = int(len(rows))
        self.model = aa.fit_model(rows, self.features)
        self.low, self.high = aa.fit_quantile_models(rows, self.features)
        self.typical = rows[self.features].median()
        self.threshold = aa.ALERT_THRESHOLDS["sensor_free"]

    def explain(self, row: pd.Series, top: int = 3) -> list[str]:
        """Ask the model 'what if this input had its ordinary value?' and report the biggest shifts."""
        x = row[self.features].astype(float)
        base = float(self.model.predict(x.to_frame().T)[0])
        shifts = []
        for name, (label, unit) in PLAIN.items():
            if pd.isna(x[name]):
                continue
            changed = x.copy()
            changed[name] = self.typical[name]
            shift = base - float(self.model.predict(changed.to_frame().T)[0])
            shifts.append((abs(shift), shift, name, label, unit))
        lines = []
        for _, shift, name, label, unit in sorted(shifts, reverse=True)[:top]:
            direction = "pushes the forecast up" if shift > 0 else "pulls the forecast down"
            lines.append(f"{label}: {x[name]:.1f} {unit} (typical over the year: {self.typical[name]:.1f}) {direction} by about {abs(shift):.0f} µg/m³".replace("  ", " "))
        return lines

    def forecast(self, metar: pd.DataFrame | None = None, now: pd.Timestamp | None = None) -> dict:
        """Forecast for the day after the latest evening whose 18:00 has passed and whose weather was observed.

        `metar` (already parsed) and `now` can be passed in for testing; by default fresh reports are downloaded.
        """
        source = "saved file in data/raw/"
        if metar is None:
            metar = aa.load_metar()
            try:
                fresh = aa.parse_metar(fetch_recent_metar())
                metar = pd.concat([metar[metar.index < fresh.index.min()], fresh]).sort_index()
                source = "downloaded now from the Iowa Environmental Mesonet"
            except Exception as err:      # no network: fall back to the saved file and say so
                source = f"saved file in data/raw/ (download failed: {type(err).__name__})"
        now = (pd.Timestamp(now) if now is not None else pd.Timestamp.now(tz=aa.TZ))
        now = now.tz_localize(aa.TZ) if now.tzinfo is None else now.tz_convert(aa.TZ)
        metar = metar[metar.index <= now]

        # latest day whose 18:00 has passed and that has enough daytime reports
        day = now.tz_localize(None).normalize() if now.hour >= aa.ISSUE_HOUR else now.tz_localize(None).normalize() - pd.Timedelta(days=1)
        daytime_reports = aa.daytime(metar["temp"], "count")
        for _ in range(7):
            if daytime_reports.get(day, 0) >= MIN_DAY_REPORTS:
                break
            day -= pd.Timedelta(days=1)
        else:
            raise RuntimeError("No recent day has enough airport weather reports for a forecast.")
        cutoff = day.tz_localize(aa.TZ) + pd.Timedelta(hours=aa.ISSUE_HOUR)
        used = metar[metar.index < cutoff]                       # nothing after 18:00 of the issue day is used
        row = aa.build_weather_table(used, day - pd.Timedelta(days=3), day).loc[day]
        x = row[self.features].astype(float).to_frame().T
        pred, low, high = (float(m.predict(x)[0]) for m in (self.model, self.low, self.high))
        low, high = min(low, pred), max(high, pred)
        target = day + pd.Timedelta(days=1)
        return {
            "issued_for_evening": str(day.date()), "target_day": str(target.date()), "target_weekday": target.strftime("%A"),
            "forecast_pm25": round(pred, 1), "likely_low": round(low, 1), "likely_high": round(high, 1),
            "warning": bool(pred > self.threshold), "warning_threshold": self.threshold, "action_level": aa.ALERT_LEVEL,
            "why": self.explain(row), "weather_source": source,
            "weather_reports_used_today": int(daytime_reports.get(day, 0)),
            "last_weather_report_used": str(used.index.max()),
            "generated_at": str(pd.Timestamp.now(tz=aa.TZ).round("s")),
            "model": f"sensor-free: {len(self.features)} weather and calendar inputs, trained on {self.n_train_days} days with reference measurements",
            "inputs": {k: (None if pd.isna(v) else round(float(v), 2)) for k, v in row[self.features].items()},
        }


def as_text(f: dict) -> str:
    decision = ("### ⚠️ Smog warning: plan PE **indoors**" if f["warning"] else "### ✅ No warning: PE can stay **outdoors**")
    return "\n\n".join([
        f"## Forecast for {f['target_weekday']}, {pd.Timestamp(f['target_day']).strftime('%d %B %Y')}",
        f"Made from Almaty airport weather up to 18:00 on {f['issued_for_evening']} ({f['weather_reports_used_today']} daytime reports; {f['weather_source']}). "
        "**No PM2.5 measurement is used.**",
        decision,
        f"**Expected daytime PM2.5 (08:00–18:00): about {f['forecast_pm25']:.0f} µg/m³**, likely between {f['likely_low']:.0f} and {f['likely_high']:.0f}. "
        f"A warning is given when the forecast is above {f['warning_threshold']:.0f} µg/m³.",
        "**Why:**\n" + "\n".join(f"- {line}" for line in f["why"]),
        "*This forecast cannot be checked against the reference monitor, whose public record ends on 14 Nov 2025. "
        "On 398 test days in 2024-25 the same kind of model missed 19 of 119 smog days and raised 40 false alarms. "
        "The number is the level expected at the former reference monitor, not at your school: in 2026 the model's numbers ran well above "
        "a low-cost citizen sensor in the city centre. Prototype, not an official warning.*",
    ])


def main() -> None:
    forecast = LiveForecaster().forecast()
    path = aa.ROOT / "results" / "live_forecast.json"
    path.write_text(json.dumps(forecast, indent=2, ensure_ascii=False))
    print(as_text(forecast))
    print(f"\nSaved to {path.relative_to(aa.ROOT)}")


if __name__ == "__main__":
    main()
