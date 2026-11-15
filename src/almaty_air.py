"""Core library: data loading, feature building, baselines, model and metrics.

The task
--------
Every evening at 18:00 (Almaty time) we forecast TOMORROW's daytime
(08:00-18:00) mean PM2.5 at one monitor in Almaty, using only information
that already exists at 18:00 today. A school can use the forecast to decide
whether tomorrow's PE lessons stay outdoors.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

TZ = "Asia/Almaty"
DAY_START, DAY_END = 8, 18      # "daytime" = school hours, local time
ISSUE_HOUR = 18                 # the forecast is issued at 18:00 local time
MIN_DAY_HOURS = 6               # a daytime mean needs at least 6 of 10 hourly values
ALERT_LEVEL = 35.0              # ug/m3; US EPA 24-hour PM2.5 standard, used as the action level

# Warning thresholds (forecast value above which a warning is given). They were chosen on the
# validation year with tune_threshold() and written into PROJECT_SPEC.md before the test period
# was scored; they are kept fixed here so that every environment evaluates the same rule.
ALERT_THRESHOLDS = {"persistence": 23.0, "seasonal": 26.5, "cams": 18.5, "linear": 29.0, "model": 29.0,
                    # added on 15 Nov 2026 (addendum in PROJECT_SPEC.md): chosen on the validation year with the same
                    # 3-to-1 rule and committed before the sensor-free model was scored on the test period
                    "sensor_free": 36.0}

# Chronological split, fixed BEFORE any model was evaluated (dates are target days).
TRAIN_END = "2023-09-30"
VALID_END = "2024-09-30"        # validation = 2023-10-01 .. 2024-09-30
TEST_END = "2025-11-14"         # test       = 2024-10-01 .. 2025-11-14


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_pm(path: Path, stamp: str = "end") -> pd.Series:
    """Hourly PM2.5 indexed by the LOCAL start of each hour.

    stamp="end": timestamps mark the end of the hourly average (OpenAQ archive).
    stamp="start": timestamps mark the start of the hour (our citizen-sensor file).
    """
    df = pd.read_csv(path)
    index = pd.to_datetime(df["datetime_utc"]).dt.tz_localize("UTC")
    if stamp == "end":
        index = index - pd.Timedelta(hours=1)
    series = pd.Series(df["pm25"].astype(float).to_numpy(), index=pd.DatetimeIndex(index).tz_convert(TZ), name="pm25")
    series = series[~series.index.duplicated()].sort_index()
    return series.clip(lower=0)  # the monitor reports a few slightly negative values near zero


def load_cams(path: Path = RAW / "cams_openmeteo_almaty_pm25_hourly.csv") -> pd.Series:
    df = pd.read_csv(path)
    index = pd.DatetimeIndex(pd.to_datetime(df["datetime_utc"]).dt.tz_localize("UTC")).tz_convert(TZ)
    return pd.Series(df["cams_pm25"].astype(float).to_numpy(), index=index, name="cams").sort_index()


def load_metar(path: Path = RAW / "iem_uaaa_metar.csv.gz") -> pd.DataFrame:
    """Airport weather reports with a local-time index and SI units."""
    df = pd.read_csv(path, na_values=["M"], low_memory=False)
    index = pd.DatetimeIndex(pd.to_datetime(df["valid"]).dt.tz_localize("UTC")).tz_convert(TZ)
    out = pd.DataFrame(index=index)
    out["temp"] = pd.to_numeric(df["tmpc"], errors="coerce").to_numpy()                 # deg C
    out["spread"] = out["temp"] - pd.to_numeric(df["dwpc"], errors="coerce").to_numpy()  # temp - dew point
    out["wind"] = pd.to_numeric(df["sknt"], errors="coerce").to_numpy() * 0.5144         # m/s
    direction = np.deg2rad(pd.to_numeric(df["drct"], errors="coerce").to_numpy())
    out["wind_u"] = -out["wind"] * np.sin(direction)                                     # west->east component
    out["wind_v"] = -out["wind"] * np.cos(direction)                                     # south->north component
    out["pressure"] = pd.to_numeric(df["alti"], errors="coerce").to_numpy() * 33.8639    # hPa
    out["vis"] = (pd.to_numeric(df["vsby"], errors="coerce").to_numpy() * 1.609).clip(max=10.0)  # km, capped at 10
    codes = df["wxcodes"].fillna("").astype(str).to_numpy()
    out["precip"] = pd.Series(codes).str.contains("RA|SN|DZ|SH|GR|PL|SG").to_numpy().astype(float)
    out["fog"] = pd.Series(codes).str.contains("FG|BR").to_numpy().astype(float)
    out["haze"] = pd.Series(codes).str.contains("HZ|FU|DU|SA").to_numpy().astype(float)
    out["calm"] = (out["wind"] < 1.0).astype(float)
    return out.sort_index()


# --------------------------------------------------------------------------- #
# Daily aggregation helpers (all windows end at or before the 18:00 issue time)
# --------------------------------------------------------------------------- #
def _by_day(frame, how: str, min_count: int = 1):
    grouped = frame.groupby(frame.index.tz_localize(None).normalize())
    result = getattr(grouped, how)()
    return result.where(grouped.count() >= min_count)


def daytime(frame, how: str = "mean", min_count: int = 1):
    """Aggregate over 08:00-18:00 of each local day."""
    part = frame[(frame.index.hour >= DAY_START) & (frame.index.hour < DAY_END)]
    return _by_day(part, how, min_count)


def last24h(frame, how: str = "mean", min_count: int = 1):
    """Aggregate over the 24 hours that end at 18:00 of each local day."""
    shifted = frame.copy()
    shifted.index = shifted.index + pd.Timedelta(hours=24 - ISSUE_HOUR)
    return _by_day(shifted, how, min_count)


def overnight(frame, how: str = "mean", min_count: int = 1):
    """Aggregate over 18:00 yesterday .. 08:00 today."""
    shifted = frame.copy()
    shifted.index = shifted.index + pd.Timedelta(hours=24 - ISSUE_HOUR)
    part = shifted[shifted.index.hour < (24 - ISSUE_HOUR) + DAY_START]
    return _by_day(part, how, min_count)


def evening(frame, how: str = "mean", min_count: int = 1):
    """Aggregate over the last 3 hours before the forecast is issued (15:00-18:00)."""
    part = frame[(frame.index.hour >= ISSUE_HOUR - 3) & (frame.index.hour < ISSUE_HOUR)]
    return _by_day(part, how, min_count)


# --------------------------------------------------------------------------- #
# Feature table: one row per "today" (issue day); target = tomorrow's daytime mean
# --------------------------------------------------------------------------- #
PM_FEATURES = ["pm_day", "pm_24h", "pm_night", "pm_evening", "pm_max24h", "pm_day_lag1", "pm_day_lag2", "pm_week", "pm_change"]
WEATHER_FEATURES = ["temp_day", "temp_min24h", "temp_change", "wind_day", "wind_max24h", "wind_evening", "wind_u", "wind_v",
                    "calm_share", "vis_day", "vis_min24h", "spread_day", "pressure_day", "pressure_change",
                    "precip_share", "fog_share", "haze_share"]
CALENDAR_FEATURES = ["season_sin", "season_cos", "weekday", "is_weekend"]
FEATURES = PM_FEATURES + WEATHER_FEATURES + CALENDAR_FEATURES
# Inputs of the sensor-free model: airport weather and the calendar only. It needs no PM2.5 monitor,
# so it still works now that the reference monitor has stopped publishing (last reading: 14 Nov 2025).
SENSOR_FREE_FEATURES = WEATHER_FEATURES + CALENDAR_FEATURES


def add_weather_and_calendar(t: pd.DataFrame, metar: pd.DataFrame) -> pd.DataFrame:
    """Adds the 17 weather inputs and 4 calendar inputs to a table indexed by issue day (today).

    Shared by the experiment and by the live forecast, so both build their inputs with the same code.
    """
    # --- airport weather known at 18:00 today
    t["temp_day"] = daytime(metar["temp"])
    t["temp_min24h"] = last24h(metar["temp"], "min")
    t["temp_change"] = t["temp_day"] - t["temp_day"].shift(1)
    t["wind_day"] = daytime(metar["wind"])
    t["wind_max24h"] = last24h(metar["wind"], "max")
    t["wind_evening"] = evening(metar["wind"])
    t["wind_u"] = daytime(metar["wind_u"])
    t["wind_v"] = daytime(metar["wind_v"])
    t["calm_share"] = last24h(metar["calm"])
    t["vis_day"] = daytime(metar["vis"])
    t["vis_min24h"] = last24h(metar["vis"], "min")
    t["spread_day"] = daytime(metar["spread"])
    t["pressure_day"] = daytime(metar["pressure"])
    t["pressure_change"] = t["pressure_day"] - t["pressure_day"].shift(1)
    t["precip_share"] = last24h(metar["precip"])
    t["fog_share"] = last24h(metar["fog"])
    t["haze_share"] = last24h(metar["haze"])

    # --- calendar of the TARGET day (tomorrow)
    target_day = t.index + pd.Timedelta(days=1)
    angle = 2 * np.pi * target_day.dayofyear / 365.25
    t["season_sin"], t["season_cos"] = np.sin(angle), np.cos(angle)
    t["weekday"] = target_day.dayofweek
    t["is_weekend"] = (target_day.dayofweek >= 5).astype(float)
    t["target_day"] = target_day
    return t


def build_weather_table(metar: pd.DataFrame, first_day, last_day) -> pd.DataFrame:
    """Weather and calendar inputs only, one row per issue day. No PM2.5 data is needed."""
    days = pd.date_range(pd.Timestamp(first_day).normalize(), pd.Timestamp(last_day).normalize(), freq="D")
    return add_weather_and_calendar(pd.DataFrame(index=days), metar)


def build_table(pm: pd.Series, metar: pd.DataFrame, cams: pd.Series | None = None) -> pd.DataFrame:
    days = pd.date_range(pm.index.min().tz_localize(None).normalize(), pm.index.max().tz_localize(None).normalize(), freq="D")
    t = pd.DataFrame(index=days)

    # --- PM2.5 known at 18:00 today
    t["pm_day"] = daytime(pm, "mean", MIN_DAY_HOURS)
    t["pm_24h"] = last24h(pm, "mean", 12)
    t["pm_night"] = overnight(pm, "mean", 6)
    t["pm_evening"] = evening(pm, "mean", 2)
    t["pm_max24h"] = last24h(pm, "max", 12)
    t["pm_day_lag1"] = t["pm_day"].shift(1)
    t["pm_day_lag2"] = t["pm_day"].shift(2)
    t["pm_week"] = t["pm_day"].rolling(7, min_periods=3).mean()
    t["pm_change"] = t["pm_day"] - t["pm_day_lag1"]

    add_weather_and_calendar(t, metar)

    # --- target and reference forecasts
    t["y"] = t["pm_day"].shift(-1)                       # tomorrow's daytime mean (what we predict)
    t["persistence"] = t["pm_day"]                       # "tomorrow = today"
    if cams is not None:
        t["cams"] = daytime(cams, "mean", MIN_DAY_HOURS).shift(-1)   # global model value for tomorrow
    return t


def split(table: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Chronological split by target day. Only rows where truth and persistence both exist."""
    usable = table[table["y"].notna() & table["persistence"].notna()]
    day = usable["target_day"]
    return {
        "train": usable[day <= TRAIN_END],
        "valid": usable[(day > TRAIN_END) & (day <= VALID_END)],
        "test": usable[(day > VALID_END) & (day <= TEST_END)],
    }


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
MODEL_PARAMS = dict(loss="absolute_error", learning_rate=0.05, max_iter=300, max_depth=2,
                    min_samples_leaf=20, l2_regularization=1.0, random_state=0)


def fit_model(train: pd.DataFrame, features: list[str] = FEATURES, **overrides) -> HistGradientBoostingRegressor:
    """Gradient-boosted trees. Handles missing feature values natively."""
    model = HistGradientBoostingRegressor(**{**MODEL_PARAMS, **overrides})
    model.fit(train[features], train["y"])
    return model


def fit_quantile_models(train: pd.DataFrame, features: list[str] = FEATURES, low: float = 0.1, high: float = 0.9):
    params = {k: v for k, v in MODEL_PARAMS.items() if k != "loss"}
    return tuple(HistGradientBoostingRegressor(loss="quantile", quantile=q, **params).fit(train[features], train["y"])
                 for q in (low, high))


def climatology(train: pd.DataFrame, rows: pd.DataFrame) -> np.ndarray:
    """Seasonal baseline: the average for that calendar month in the training years."""
    by_month = train.groupby(train["target_day"].dt.month)["y"].mean()
    return rows["target_day"].dt.month.map(by_month).to_numpy()


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #
def mae(y, pred) -> float:
    return float(np.mean(np.abs(np.asarray(y) - np.asarray(pred))))


def alert_counts(y, pred, threshold: float, level: float = ALERT_LEVEL) -> dict:
    """Alert = forecast above `threshold`. Bad day = truth above `level`."""
    y, pred = np.asarray(y), np.asarray(pred)
    bad, alert = y > level, pred > threshold
    hit, missed = int((bad & alert).sum()), int((bad & ~alert).sum())
    false_alarm, quiet = int((~bad & alert).sum()), int((~bad & ~alert).sum())
    return {"bad_days": hit + missed, "caught": hit, "missed": missed, "false_alarms": false_alarm, "correct_quiet": quiet,
            "recall": hit / max(1, hit + missed), "precision": hit / max(1, hit + false_alarm)}


def tune_threshold(y, pred, cost_miss: float = 3.0, cost_false_alarm: float = 1.0, level: float = ALERT_LEVEL) -> float:
    """Pick the alert threshold that minimises cost on VALIDATION data.

    A missed smog day (children exercise in unhealthy air) is counted as three
    times worse than a false alarm (one PE lesson moved indoors for nothing).
    """
    best, best_cost = level, np.inf
    for threshold in np.arange(15.0, 60.5, 0.5):
        c = alert_counts(y, pred, threshold, level)
        cost = cost_miss * c["missed"] + cost_false_alarm * c["false_alarms"]
        if cost < best_cost - 1e-9 or (abs(cost - best_cost) < 1e-9 and abs(threshold - level) < abs(best - level)):
            best, best_cost = float(threshold), cost
    return best


def change_days(rows: pd.DataFrame, level: float = ALERT_LEVEL) -> pd.Series:
    """Days when tomorrow lands on the other side of the action level than today.

    'Tomorrow = today' is wrong on every one of these days by construction.
    """
    return (rows["y"] > level) != (rows["persistence"] > level)


def block_bootstrap_gain(y, pred_model, pred_base, block: int = 7, rounds: int = 2000, seed: int = 0) -> tuple[float, float]:
    """95% interval for (baseline MAE - model MAE), resampling whole weeks to respect autocorrelation."""
    y, pm, pb = np.asarray(y), np.asarray(pred_model), np.asarray(pred_base)
    diff = np.abs(y - pb) - np.abs(y - pm)
    blocks = [diff[i:i + block] for i in range(0, len(diff), block)]
    rng = np.random.default_rng(seed)
    gains = []
    for _ in range(rounds):
        pick = rng.integers(0, len(blocks), len(blocks))
        gains.append(np.concatenate([blocks[i] for i in pick]).mean())
    return float(np.percentile(gains, 2.5)), float(np.percentile(gains, 97.5))
