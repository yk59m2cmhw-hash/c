#!/usr/bin/env python3
"""Run the whole experiment and write tables and figures to results/.

    python src/run_experiment.py

Steps: build the daily table -> chronological split -> baselines and model on
validation (to choose alert thresholds) -> refit on train+validation -> ONE
evaluation on the test period -> error analysis -> optional extra test on the
2026 citizen sensor.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import almaty_air as aa

warnings.filterwarnings("ignore")
OUT = aa.ROOT / "results"
# Two low-cost citizen sensors (sensor.community, SDS011) used ONLY for the external check on 2026.
CITIZEN_SENSORS = {78340: "city centre", 90941: "west of the city"}
MIN_CITIZEN_DAYS = 60       # fixed in PROJECT_SPEC.md before the data was looked at: fewer days than this are not reported

# Chart colours (colour-blind-safe palette, checked with a validator)
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
BLUE, ORANGE, AQUA, NEUTRAL = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c"


def linear_model(train: pd.DataFrame):
    """A simple comparison model: ridge regression on the same features, log target."""
    pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 20)))
    pipe.fit(train[aa.FEATURES], np.log1p(train["y"]))
    return lambda rows: np.expm1(pipe.predict(rows[aa.FEATURES]))


def predict_all(fit_rows: pd.DataFrame, rows: pd.DataFrame) -> pd.DataFrame:
    """Every method's forecast for `rows`, using models fitted on `fit_rows` only."""
    model = aa.fit_model(fit_rows)
    low, high = aa.fit_quantile_models(fit_rows)
    out = pd.DataFrame({"target_day": rows["target_day"], "y": rows["y"]}, index=rows.index)
    out["persistence"] = rows["persistence"]
    out["seasonal"] = aa.climatology(fit_rows, rows)
    out["cams"] = rows["cams"] if "cams" in rows else np.nan
    out["linear"] = linear_model(fit_rows)(rows)
    out["model"] = model.predict(rows[aa.FEATURES])
    out["q10"], out["q90"] = low.predict(rows[aa.FEATURES]), high.predict(rows[aa.FEATURES])
    # the sensor-free model: same settings, but airport weather and calendar only (no PM2.5 input at all)
    free = aa.SENSOR_FREE_FEATURES
    out["sensor_free"] = aa.fit_model(fit_rows, free).predict(rows[free])
    free_low, free_high = aa.fit_quantile_models(fit_rows, free)
    out["free_q10"], out["free_q90"] = free_low.predict(rows[free]), free_high.predict(rows[free])
    return out


def season_of(days: pd.Series) -> pd.Series:
    return np.where(days.dt.month.isin([10, 11, 12, 1, 2, 3]), "heating season (Oct-Mar)", "warm season (Apr-Sep)")


def summarise(pred: pd.DataFrame, thresholds: dict[str, float], methods: list[str]) -> dict:
    """All headline numbers for one evaluation period."""
    result = {"n_days": int(len(pred)), "bad_days": int((pred["y"] > aa.ALERT_LEVEL).sum()),
              "first_day": str(pred["target_day"].min().date()), "last_day": str(pred["target_day"].max().date()),
              "methods": {}}
    base = aa.mae(pred["y"], pred["persistence"])
    change = (pred["y"] > aa.ALERT_LEVEL) != (pred["persistence"] > aa.ALERT_LEVEL)
    onset = change & (pred["y"] > aa.ALERT_LEVEL)
    result["change_days"] = {"total": int(change.sum()), "smog_arrives": int(onset.sum()), "smog_clears": int((change & ~onset).sum())}
    seasons = pd.Series(season_of(pred["target_day"]), index=pred.index)
    for name in methods:
        ok = pred[name].notna()
        y, p = pred.loc[ok, "y"], pred.loc[ok, name]
        entry = {"n": int(ok.sum()), "mae": aa.mae(y, p), "bias": float((p - y).mean()),
                 "mae_gain_vs_persistence_pct": 100 * (1 - aa.mae(y, p) / aa.mae(y, pred.loc[ok, "persistence"]))}
        entry["mae_by_season"] = {s: aa.mae(y[seasons[ok] == s], p[seasons[ok] == s]) for s in sorted(seasons.unique())}
        entry["alerts_tuned"] = {"threshold": thresholds[name], **aa.alert_counts(y, p, thresholds[name])}
        entry["alerts_at_35"] = aa.alert_counts(y, p, aa.ALERT_LEVEL)
        right_side = (p > aa.ALERT_LEVEL) == (y > aa.ALERT_LEVEL)
        entry["change_days_right_side"] = {"total": int(right_side[change[ok]].sum()),
                                           "smog_arrives": int(right_side[onset[ok]].sum()),
                                           "smog_clears": int(right_side[(change & ~onset)[ok]].sum())}
        if name != "persistence":
            low, high = aa.block_bootstrap_gain(y, p, pred.loc[ok, "persistence"])
            entry["mae_gain_ci95"] = [low, high]
        result["methods"][name] = entry
    result["persistence_mae"] = base
    if "q10" in pred:
        result["band_10_90_coverage"] = float(((pred["y"] >= pred["q10"]) & (pred["y"] <= pred["q90"])).mean())
        result["band_mean_width"] = float((pred["q90"] - pred["q10"]).mean())
    if "free_q10" in pred:
        result["sensor_free_band_10_90_coverage"] = float(((pred["y"] >= pred["free_q10"]) & (pred["y"] <= pred["free_q90"])).mean())
    return result


# --------------------------------------------------------------------------- #
# Figures
# --------------------------------------------------------------------------- #
def style(ax, title: str, subtitle: str = "") -> None:
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=10, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(title, loc="left", color=INK, fontsize=13, fontweight="bold", pad=22 if subtitle else 10)
    if subtitle:
        ax.text(0, 1.03, subtitle, transform=ax.transAxes, color=MUTED, fontsize=10, va="bottom")


def fig_timeseries(pred: pd.DataFrame, path: Path) -> None:
    part = pred[(pred["target_day"] >= "2024-11-01") & (pred["target_day"] <= "2025-02-28")]
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=160)
    days = part["target_day"]
    ax.fill_between(days, part["q10"], part["q90"], color=BLUE, alpha=0.16, linewidth=0, label="Model's 10-90% range")
    ax.plot(days, part["y"], color=INK, linewidth=2, label="Measured")
    ax.plot(days, part["model"], color=BLUE, linewidth=2, label="Model forecast (made the evening before)")
    ax.axhline(aa.ALERT_LEVEL, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(1.005, aa.ALERT_LEVEL, "35 µg/m³\naction level", transform=ax.get_yaxis_transform(), color=MUTED, fontsize=9, va="center")
    ax.set_ylabel("Daytime PM2.5, µg/m³", color=MUTED, fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", frameon=False, fontsize=10, labelcolor=INK)
    style(ax, "Forecast vs. what was measured: winter 2024-25 (test period, never seen in training)",
          "Each point is one day. The forecast for a day was made at 18:00 the day before.")
    fig.autofmt_xdate(rotation=0, ha="center")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_mae(summary: dict, path: Path) -> None:
    names = [("persistence", "Tomorrow = today\n(persistence)"), ("seasonal", "Average for\nthe month"),
             ("cams", "Global model\n(CAMS)"), ("linear", "Linear model"), ("model", "Our model\n(boosted trees)"),
             ("sensor_free", "Sensor-free\n(weather only)")]
    values = [summary["methods"][k]["mae"] for k, _ in names]
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=160)
    bars = ax.bar([label for _, label in names], values, width=0.58, color=[NEUTRAL] * 4 + [BLUE, AQUA])
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.25, f"{value:.1f}", ha="center", color=INK, fontsize=11)
    ax.set_ylabel("Mean absolute error, µg/m³ (lower is better)", color=MUTED, fontsize=10)
    ax.set_ylim(0, max(values) * 1.15)
    style(ax, f"Average miss on {summary['n_days']} test days", "Forecast of tomorrow's daytime PM2.5, Oct 2024 - Nov 2025")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_alerts(summary: dict, path: Path) -> None:
    names = [("persistence", "Tomorrow = today"), ("cams", "Global model (CAMS)"), ("model", "Our model"),
             ("sensor_free", "Sensor-free (weather only)")]
    missed = [summary["methods"][k]["alerts_tuned"]["missed"] for k, _ in names]
    false = [summary["methods"][k]["alerts_tuned"]["false_alarms"] for k, _ in names]
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8.4, 4.4), dpi=160)
    b1 = ax.bar(x - 0.2, missed, width=0.36, color=BLUE, label="Smog days missed (no warning given)")
    b2 = ax.bar(x + 0.2, false, width=0.36, color=ORANGE, label="False alarms (warning on a clean day)")
    for bars in (b1, b2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.6, f"{int(bar.get_height())}", ha="center", color=INK, fontsize=11)
    ax.set_xticks(x, [label for _, label in names])
    ax.set_ylabel("Days (lower is better)", color=MUTED, fontsize=10)
    ax.set_ylim(0, max(missed + false) * 1.25)
    ax.legend(loc="upper right", frameon=False, fontsize=10, labelcolor=INK)
    style(ax, f"Warning mistakes on the test period ({summary['bad_days']} smog days out of {summary['n_days']})",
          "Each method uses the warning threshold chosen for it on validation data (a miss counts 3x a false alarm)")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def citizen_check(table: pd.DataFrame, metar: pd.DataFrame, cams: pd.Series, thresholds: dict) -> dict | None:
    """External check: frozen models against two citizen sensors in 2026. Nothing is fitted or tuned on this data.

    The models are trained on every reference-monitor day (2020-04 .. 2025-11). For each sensor the 'truth' is that
    sensor's own next-day daytime mean, so this is a different instrument, in a different place, in a different year.
    """
    usable = table[table["y"].notna() & table["persistence"].notna()]
    result, daily = {}, {}
    for sensor_id, place in CITIZEN_SENSORS.items():
        path = aa.RAW / f"sensor_community_{sensor_id}_pm25_hourly.csv"
        if not path.exists():
            continue
        t = aa.build_table(aa.load_pm(path, stamp="start"), metar, cams)
        rows = t[t["y"].notna() & t["persistence"].notna()]
        if len(rows) < MIN_CITIZEN_DAYS:
            continue
        pred = predict_all(usable, rows)
        pred.round(2).to_csv(OUT / f"citizen_2026_sensor_{sensor_id}_predictions.csv", index=False)
        fig_citizen(pred, sensor_id, place, OUT / f"fig_citizen_2026_sensor_{sensor_id}.png")
        daily[sensor_id] = t["pm_day"].dropna()
        entry = {"place": place, "n_days": int(len(pred)), "first_day": str(pred["target_day"].min().date()),
                 "last_day": str(pred["target_day"].max().date()), "bad_days": int((pred["y"] > aa.ALERT_LEVEL).sum()),
                 "heating_season_days": int(pred["target_day"].dt.month.isin([10, 11, 12, 1, 2, 3]).sum()), "methods": {}}
        for name in ("persistence", "cams", "model", "sensor_free"):
            ok = pred[name].notna()
            y, f = pred.loc[ok, "y"], pred.loc[ok, name]
            entry["methods"][name] = {"n": int(ok.sum()), "mae": aa.mae(y, f), "bias": float((f - y).mean()),
                                      "rank_correlation": float(y.corr(f, method="spearman")),
                                      "alerts": {"threshold": thresholds[name], **aa.alert_counts(y, f, thresholds[name])}}
        result[str(sensor_id)] = entry
    if len(daily) == 2:      # how well do the two sensors agree with each other on the same days?
        a, b = (daily[k] for k in CITIZEN_SENSORS)
        both = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna()
        result["between_sensors"] = {"n_days": int(len(both)), "rank_correlation": float(both["a"].corr(both["b"], method="spearman")),
                                     "mean_centre": float(both["a"].mean()), "mean_west": float(both["b"].mean()),
                                     "same_side_of_35": float(((both["a"] > aa.ALERT_LEVEL) == (both["b"] > aa.ALERT_LEVEL)).mean())}
    return result or None


def fig_citizen(pred: pd.DataFrame, sensor_id: int, place: str, path: Path) -> None:
    """Frozen forecasts against one citizen sensor in 2026, one panel per stretch of days."""
    pred = pred.sort_values("target_day")
    gap = pred["target_day"].diff().dt.days.fillna(1) > 45           # a new panel after a long gap (the warm season)
    groups = [g for _, g in pred.groupby(gap.cumsum())]
    widths = [max(len(g), 12) for g in groups]
    fig, axes = plt.subplots(1, len(groups), figsize=(11, 4.4), dpi=160, sharey=True, gridspec_kw={"width_ratios": widths}, squeeze=False)
    for i, (ax, g) in enumerate(zip(axes[0], groups)):
        ax.plot(g["target_day"], g["y"], color=INK, linewidth=2, label="Measured by the citizen sensor")
        ax.plot(g["target_day"], g["sensor_free"], color=AQUA, linewidth=2, label="Sensor-free model (frozen)")
        ax.plot(g["target_day"], g["model"], color=BLUE, linewidth=1.6, label="Main model, fed with the sensor's readings (frozen)")
        ax.axhline(aa.ALERT_LEVEL, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
        style(ax, "", "")
        ax.set_ylim(bottom=0)
        ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(bymonthday=[1, 15]))
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b"))
        if i == 0:
            ax.set_ylabel("Daytime PM2.5, µg/m³", color=MUTED, fontsize=10)
            ax.legend(loc="upper right", frameon=False, fontsize=9, labelcolor=INK)
    axes[0][-1].text(1.01, aa.ALERT_LEVEL, "35 µg/m³", transform=axes[0][-1].get_yaxis_transform(), color=MUTED, fontsize=9, va="center")
    fig.suptitle(f"External check, 2026: forecasts run well above citizen sensor {sensor_id} ({place})", x=0.01, ha="left",
                 color=INK, fontsize=13, fontweight="bold")
    fig.text(0.01, 0.9, "A different instrument, place and year. The models were trained on the reference monitor and not adjusted.",
             color=MUTED, fontsize=10)
    fig.tight_layout(rect=(0, 0, 0.97, 0.9))
    fig.savefig(path)
    plt.close(fig)


# --------------------------------------------------------------------------- #
def markdown_report(valid: dict, test: dict, worst: pd.DataFrame, importance: pd.Series, citizen: dict | None, ablation: dict,
                    matched: dict) -> str:
    label = {"persistence": "Tomorrow = today (persistence)", "seasonal": "Average for the month", "cams": "Global model (CAMS)",
             "linear": "Linear model (ridge)", "model": "**Our model (boosted trees)**",
             "sensor_free": "Sensor-free model (weather + calendar only)"}
    lines = ["# Results (generated by `src/run_experiment.py`)", ""]
    for title, s in (("Validation (used to choose settings)", valid), ("Test (evaluated once, after settings were frozen)", test)):
        lines += [f"## {title}: {s['first_day']} .. {s['last_day']}, {s['n_days']} days, {s['bad_days']} smog days (> 35 µg/m³)", "",
                  "| Method | MAE, µg/m³ | vs persistence | Heating season MAE | Warm season MAE | Smog days caught | Missed | False alarms |",
                  "|---|---|---|---|---|---|---|---|"]
        for name, m in s["methods"].items():
            a = m["alerts_tuned"]
            seasons = list(m["mae_by_season"].values())
            gain = "-" if name == "persistence" else f"{m['mae_gain_vs_persistence_pct']:+.0f}%"
            lines.append(f"| {label[name]} | {m['mae']:.1f} | {gain} | {seasons[0]:.1f} | {seasons[1]:.1f} | "
                         f"{a['caught']} / {a['bad_days']} | {a['missed']} | {a['false_alarms']} |")
        lines.append("")
    lines += ["## Which inputs matter (validation only, MAE in µg/m³)", "", "| Inputs given to the model | Validation MAE |", "|---|---|",
              f"| none: tomorrow = today | {valid['persistence_mae']:.1f} |"]
    lines += [f"| {k} | {v:.1f} |" for k, v in ablation.items()] + [""]
    lines += ["## Warnings with the plain rule 'warn if the forecast is above 35' (test)", "",
              "| Method | Smog days caught | Missed | False alarms |", "|---|---|---|---|"]
    for name, mm in test["methods"].items():
        a = mm["alerts_at_35"]
        lines.append(f"| {label[name]} | {a['caught']} / {a['bad_days']} | {a['missed']} | {a['false_alarms']} |")
    lines.append("")
    lines += ["## Does the warning result depend on the threshold? (test; added after the test was scored, descriptive)", "",
              "Fewest false alarms each method can reach while missing at most N smog days, when its threshold is swept on the test days:", "",
              "| Missed at most | Tomorrow = today | Global model (CAMS) | Our model | Sensor-free model |", "|---|---|---|---|---|"]
    lines += [f"| {n} | {matched['persistence'][n]} | {matched['cams'][n]} | {matched['model'][n]} | {matched['sensor_free'][n]} |"
              for n in matched["model"]] + [""]
    m, f = test["methods"]["model"], test["methods"]["sensor_free"]
    c = test["change_days"]
    lines += [f"95% interval for the model's MAE gain over persistence on test: {m['mae_gain_ci95'][0]:.1f} .. {m['mae_gain_ci95'][1]:.1f} µg/m³ "
              "(bootstrap over weeks).", "",
              f"Days when the air crossed the 35 µg/m³ line between today and tomorrow: {c['total']} "
              f"({c['smog_arrives']} smog arrives, {c['smog_clears']} smog clears). Persistence is wrong on all of them by construction; "
              f"the model's forecast was on the correct side on {m['change_days_right_side']['total']} "
              f"({m['change_days_right_side']['smog_arrives']} arrivals, {m['change_days_right_side']['smog_clears']} clearings).", "",
              f"Model's 10-90% range contained the measured value on {100 * test['band_10_90_coverage']:.0f}% of test days (target 80%).", "",
              "## Forecasting without any PM2.5 sensor (added on 15 Nov 2026)", "",
              "The public record of the reference monitor ends on 14 Nov 2025, so today neither our main model nor 'tomorrow = today' can be "
              "computed for the real tomorrow. The sensor-free model uses airport weather and the calendar only. Its inputs, settings and "
              "warning threshold (36.0, chosen on validation) were committed in `37fb006` before it was scored on the test period. "
              "The test period had already been scored once for the main model, so this is a second look at the same period.", "",
              "| Test period | Tomorrow = today | Our model | Sensor-free model |", "|---|---|---|---|",
              f"| MAE, µg/m³ | {test['methods']['persistence']['mae']:.1f} | {m['mae']:.1f} | {f['mae']:.1f} |",
              f"| 95% interval of the MAE gain over persistence | - | {m['mae_gain_ci95'][0]:.1f} .. {m['mae_gain_ci95'][1]:.1f} | "
              f"{f['mae_gain_ci95'][0]:.1f} .. {f['mae_gain_ci95'][1]:.1f} |",
              f"| Smog days missed (of {test['bad_days']}) | {test['methods']['persistence']['alerts_tuned']['missed']} | "
              f"{m['alerts_tuned']['missed']} | {f['alerts_tuned']['missed']} |",
              f"| False alarms | {test['methods']['persistence']['alerts_tuned']['false_alarms']} | {m['alerts_tuned']['false_alarms']} | "
              f"{f['alerts_tuned']['false_alarms']} |",
              f"| Correct side on the {c['total']} change days | 0 | {m['change_days_right_side']['total']} | {f['change_days_right_side']['total']} |",
              f"| 10-90% range contains the measured value | - | {100 * test['band_10_90_coverage']:.0f}% | "
              f"{100 * test['sensor_free_band_10_90_coverage']:.0f}% |", "",
              "## Largest misses on the test period", "", worst.to_markdown(index=False), "",
              "## What the model relies on (drop in accuracy when one input is shuffled, test period)", "",
              importance.round(2).to_frame("MAE increase, µg/m³").to_markdown(), ""]
    if citizen:
        names = {"persistence": "That sensor's own 'tomorrow = today'", "cams": "Global model (CAMS)",
                 "model": "Our main model, fed with that sensor's readings", "sensor_free": "Our sensor-free model (no PM2.5 input)"}
        lines += ["## External check on two citizen sensors, 2026 (added on 15 Nov 2026)", "",
                  "A different instrument (low-cost SDS011 optical sensors from sensor.community), in different places in Almaty, in a year "
                  "no model has seen. The models are frozen: trained on the reference monitor (2020-04 .. 2025-11), with the thresholds above. "
                  "Nothing was fitted or tuned on this data, and the plan for this check was written in PROJECT_SPEC.md before the data was "
                  "looked at. 'Measured' here means the citizen sensor's own next-day daytime mean, which is not reference-grade: these sensors "
                  "read too high in humid air and are not calibrated against the reference monitor. Read the rank correlation (do the forecast "
                  "and the sensor order the days the same way; 1 is perfect) before the MAE.", ""]
        for sensor_id, c in citizen.items():
            if sensor_id == "between_sensors":
                continue
            lines += [f"### Sensor {sensor_id} ({c['place']}): {c['first_day']} .. {c['last_day']}, {c['n_days']} days "
                      f"({c['heating_season_days']} in the heating season), {c['bad_days']} days above 35 µg/m³ by this sensor", "",
                      "| Method | Rank correlation | MAE, µg/m³ | Bias, µg/m³ | Smog days caught | Missed | False alarms |", "|---|---|---|---|---|---|---|"]
            for name, cm in c["methods"].items():
                al = cm["alerts"]
                lines.append(f"| {names[name]} | {cm['rank_correlation']:.2f} | {cm['mae']:.1f} | {cm['bias']:+.1f} | "
                             f"{al['caught']} / {al['bad_days']} | {al['missed']} | {al['false_alarms']} |")
            lines.append("")
        if "between_sensors" in citizen:
            bs = citizen["between_sensors"]
            lines += [f"The two sensors against each other on the same {bs['n_days']} days: rank correlation {bs['rank_correlation']:.2f}; "
                      f"mean {bs['mean_centre']:.1f} (centre) and {bs['mean_west']:.1f} (west) µg/m³; they are on the same side of 35 µg/m³ on "
                      f"{100 * bs['same_side_of_35']:.0f}% of days. This is how much 'the truth' itself differs between two places and two devices.", ""]
    return "\n".join(lines)


def run() -> dict:
    """Runs everything, writes results/ and returns the main objects (used by the notebook)."""
    OUT.mkdir(exist_ok=True)
    pm = aa.load_pm(aa.RAW / "openaq_almaty_8876_pm25_hourly.csv")
    metar, cams = aa.load_metar(), aa.load_cams()
    table = aa.build_table(pm, metar, cams)
    parts = aa.split(table)
    train, valid, test = parts["train"], parts["valid"], parts["test"]
    methods = ["persistence", "seasonal", "cams", "linear", "model", "sensor_free"]

    # 1) validation: models fitted on train only; alert thresholds are chosen here
    pred_valid = predict_all(train, valid)
    retuned = {name: aa.tune_threshold(pred_valid["y"][pred_valid[name].notna()], pred_valid[name].dropna()) for name in methods}
    thresholds = aa.ALERT_THRESHOLDS     # the values recorded before the test was scored (see almaty_air.py)
    summary_valid = summarise(pred_valid, thresholds, methods)

    # 1b) ablation on validation only: what do the weather inputs add?
    ablation = {}
    for label, feats in (("PM2.5 history + calendar", aa.PM_FEATURES + aa.CALENDAR_FEATURES),
                         ("Weather + calendar (no PM2.5 sensor at all)", aa.WEATHER_FEATURES + aa.CALENDAR_FEATURES),
                         ("All inputs (final)", aa.FEATURES)):
        ablation[label] = aa.mae(valid["y"], aa.fit_model(train, feats).predict(valid[feats]))

    # 2) test: models refitted on train+validation, evaluated once
    fit_rows = pd.concat([train, valid])
    pred_test = predict_all(fit_rows, test)
    summary_test = summarise(pred_test, thresholds, methods)

    # 2b) descriptive check added after the test was scored: is the warning result an accident of the threshold?
    # For each method, sweep the threshold on the test days and keep the fewest false alarms for a given number of misses.
    matched = {}
    for name in ("persistence", "cams", "model", "sensor_free"):
        ok = pred_test[name].notna()
        best: dict[int, int] = {}
        for threshold in np.arange(5.0, 80.25, 0.25):
            c = aa.alert_counts(pred_test.loc[ok, "y"], pred_test.loc[ok, name], threshold)
            best[c["missed"]] = min(best.get(c["missed"], 10**6), c["false_alarms"])
        matched[name] = {str(budget): min(v for k, v in best.items() if k <= budget) for budget in (5, 8, 11, 16, 20, 30)}

    # 3) error analysis: largest misses, with what the weather did on the target day (not a model input)
    next_wind = aa.daytime(metar["wind"]).shift(-1).reindex(pred_test.index)
    next_precip = aa.daytime(metar["precip"]).shift(-1).reindex(pred_test.index)
    worst = pred_test.assign(error=pred_test["model"] - pred_test["y"], wind_today=test["wind_day"], wind_target_day=next_wind,
                             precip_target_day=next_precip)
    worst = worst.reindex(worst["error"].abs().sort_values(ascending=False).index).head(8)
    worst_table = pd.DataFrame({
        "Target day": worst["target_day"].dt.strftime("%Y-%m-%d"), "Today": worst["persistence"].round(0),
        "Forecast": worst["model"].round(0), "Measured": worst["y"].round(0), "Error": worst["error"].round(0),
        "Wind today, m/s": worst["wind_today"].round(1), "Wind on target day, m/s": worst["wind_target_day"].round(1),
        "Rain/snow on target day": np.where(worst["precip_target_day"] > 0, "yes", "no")})

    final_model = aa.fit_model(fit_rows)
    perm = permutation_importance(final_model, test[aa.FEATURES], test["y"], scoring="neg_mean_absolute_error", n_repeats=20, random_state=0)
    importance = pd.Series(perm.importances_mean, index=aa.FEATURES).sort_values(ascending=False).head(8)

    # 4) external check: two low-cost citizen sensors in 2026 (frozen models; nothing is tuned on this data)
    summary_citizen = citizen_check(table, metar, cams, thresholds)

    # 5) save everything
    pred_test.round(2).to_csv(OUT / "test_predictions.csv", index=False)
    pred_valid.round(2).to_csv(OUT / "validation_predictions.csv", index=False)
    worst_table.to_csv(OUT / "worst_misses.csv", index=False)
    metrics = {"split": {k: {"n_days": int(len(v)), "first": str(v["target_day"].min().date()), "last": str(v["target_day"].max().date())}
                         for k, v in parts.items()},
               "alert_level": aa.ALERT_LEVEL, "alert_thresholds_chosen_on_validation": thresholds,
               "alert_thresholds_retuned_in_this_environment": retuned, "false_alarms_at_matched_misses_test": matched,
               "library_versions": {"scikit-learn": __import__("sklearn").__version__, "pandas": pd.__version__, "numpy": np.__version__}, "model_params": aa.MODEL_PARAMS,
               "n_features": len(aa.FEATURES), "n_features_sensor_free": len(aa.SENSOR_FREE_FEATURES), "validation": summary_valid, "test": summary_test, "citizen_2026": summary_citizen,
               "feature_importance_test": importance.round(3).to_dict(),
               "ablation_validation_mae": ablation}
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    (OUT / "RESULTS.md").write_text(markdown_report(summary_valid, summary_test, worst_table, importance, summary_citizen, ablation, matched))
    fig_timeseries(pred_test, OUT / "fig_forecast_vs_measured.png")
    fig_mae(summary_test, OUT / "fig_mae_by_method.png")
    fig_alerts(summary_test, OUT / "fig_alert_mistakes.png")
    return {"metrics": metrics, "test_predictions": pred_test, "worst_misses": worst_table, "importance": importance,
            "ablation": ablation, "table": table, "parts": parts, "matched": matched}


def main() -> None:
    run()
    print((OUT / "RESULTS.md").read_text())


if __name__ == "__main__":
    main()
