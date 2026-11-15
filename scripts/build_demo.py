"""Build the data block of demo.html from the saved results of the notebook.

    python scripts/build_demo.py

Nothing is trained here. The script reads

    results/model.json            the final model: 26 inputs, their scaling, the weights, the warning cutoff
    results/predictions_test.csv  every held-out evening: the inputs, the answer, the baseline
    results/metrics.json          the scores quoted on the page
    data/raw/almaty_pm25_hourly_openaq8876.csv   only for the 14-day yardstick of the timetable rule

and writes them into demo.html between the DATA markers. The page then computes each forecast in the
browser from the model weights. scripts/check_demo.js verifies that the page reproduces the notebook's
forecast for every held-out evening.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
QUOTA, LOOKBACK, MIN_HOURS_PER_DAY = 2, 14, 18      # the same constants as in the notebook (sections 1 and 8)


def heating_season(dates):
    return pd.Series(pd.to_datetime(dates)).dt.month.isin([10, 11, 12, 1, 2, 3]).to_numpy()


def daily_means():
    """Daily PM2.5 averages of the reference monitor, as in the notebook: local calendar days, >= 18 hours."""
    raw = pd.read_csv(ROOT / "data/raw/almaty_pm25_hourly_openaq8876.csv")
    s = pd.Series(raw["pm25"].to_numpy(), index=pd.to_datetime(raw["local_start"].str[:19]))
    s = s[(s >= 0) & (s <= 2000)].groupby(level=0).mean().asfreq("h")
    g = s.groupby(s.index.normalize())
    return g.mean().where(g.count() >= MIN_HOURS_PER_DAY)


def play_timetable(rows, estimate_col, history, quota=QUOTA):
    """The timetable rule of notebook section 8, replayed over every complete Oct-Mar school week."""
    by_day = rows.set_index("target_date")
    weeks = []
    for monday in pd.date_range(by_day.index.min().normalize(), by_day.index.max(), freq="W-MON"):
        days = [monday + pd.Timedelta(days=i) for i in range(5)]
        if not all(d in by_day.index for d in days) or not heating_season(days).all():
            continue
        owed, chosen, log = quota, [], []
        for i, day in enumerate(days):
            left = 5 - i
            evening = day - pd.Timedelta(days=1)
            recent = history[evening - pd.Timedelta(days=LOOKBACK): evening - pd.Timedelta(days=1)].dropna()
            estimate = float(by_day.loc[day, estimate_col])
            bar = None
            if owed == 0:
                go, why = False, "done"
            elif owed >= left:
                go, why = True, "forced"
            else:
                bar = float(np.quantile(recent, owed / left)) if len(recent) >= 5 else float("inf")
                go, why = estimate <= bar, "bar"
            log.append({"day": day.strftime("%Y-%m-%d"), "forecast": round(estimate, 1), "go": bool(go), "why": why,
                        "bar": None if bar is None or not np.isfinite(bar) else round(bar, 1),
                        "owed": owed, "left": left, "measured": round(float(by_day.loc[day, "target"]), 1)})
            if go:
                chosen.append(day)
                owed -= 1
        measured = by_day.loc[days, "target"]
        weeks.append({"monday": monday.strftime("%Y-%m-%d"), "days": log,
                      "rule": float(measured.loc[chosen].mean()), "fixed": float(measured.mean()),
                      "best": float(measured.nsmallest(quota).mean())})
    return weeks


def kind_of_day(last24, target, level):
    dirty_now, dirty_next = last24 > level, target > level
    return 1 if (dirty_next and not dirty_now) else 2 if (dirty_next and dirty_now) else 3 if dirty_now else 4


def main():
    model = json.loads((ROOT / "results/model.json").read_text())
    metrics = json.loads((ROOT / "results/metrics.json").read_text())
    test = pd.read_csv(ROOT / "results/predictions_test.csv", parse_dates=["issue_day", "target_date"])
    features, level = model["features"], model["alert_level"]
    cutoff_model, cutoff_pers = metrics["cutoffs"]["model"], metrics["cutoffs"]["persistence"]
    assert cutoff_model == model["cutoff"]

    winter = heating_season(test["target_date"])
    kinds = [kind_of_day(a, b, level) for a, b in zip(test["pm_last24"], test["target"])]
    rows = [{"d": r.issue_day.strftime("%Y-%m-%d"), "t": r.target_date.strftime("%Y-%m-%d"),
             "x": [float(getattr(r, f)) for f in features], "y": float(r.target), "p": float(r.persistence),
             "nb": float(r.model), "k": k, "w": bool(w)}
            for r, k, w in zip(test.itertuples(), kinds, winter)]

    # ---- the timetable: replay with our forecast and with persistence; must reproduce the notebook's numbers
    history = daily_means()
    weeks = play_timetable(test, "model", history)
    weeks_pers = play_timetable(test, "persistence", history)
    saved = metrics["timetable_test"]["2"]
    got = {"weeks": len(weeks), "fixed timetable": np.mean([w["fixed"] for w in weeks]),
           "rule + our forecast": np.mean([w["rule"] for w in weeks]),
           "rule + persistence": np.mean([w["rule"] for w in weeks_pers]),
           "perfect hindsight": np.mean([w["best"] for w in weeks])}
    for key, value in got.items():
        assert abs(value - saved[key]) < 0.006, (key, value, saved[key])
    for week, week_pers in zip(weeks, weeks_pers):
        week["rule_persistence"] = round(week_pers["rule"], 1)
        for key in ("rule", "fixed", "best"):
            week[key] = round(week[key], 1)

    # ---- example evenings, each chosen by a rule (not by hand)
    t = test.assign(kind=kinds, winter=winter, warn=test["model"] >= cutoff_model)
    w = t[t["winter"]]
    error = (w["model"] - w["target"]).abs()
    dirtiest_monday = max(weeks, key=lambda x: x["fixed"])["monday"]
    examples = [
        ("start_first", w[w["kind"] == 1].iloc[0]["issue_day"]),
        ("start_caught", w[(w["kind"] == 1) & w["warn"]].iloc[0]["issue_day"]),
        ("clears_first", w[w["kind"] == 3].iloc[0]["issue_day"]),
        ("largest_error", w.loc[error.idxmax(), "issue_day"]),
        ("dirtiest_week", pd.Timestamp(dirtiest_monday) - pd.Timedelta(days=1)),
    ]
    examples = [{"id": name, "d": pd.Timestamp(day).strftime("%Y-%m-%d")} for name, day in examples]
    assert all(e["d"] in {r["d"] for r in rows} for e in examples)

    alerts = metrics["alerts_oct_mar"]
    mae = metrics["mae"]
    kinds_table = metrics["by_kind_of_day"]
    scores = {
        "days_oct_mar": metrics["test_days_oct_mar"], "days_all": metrics["test_days"],
        "period": metrics["test_period"],
        "mae_model": mae["Our model (Ridge, air history + weather)"]["MAE Oct-Mar"],
        "mae_persistence": mae["Persistence (last 24 h at 18:00)"]["MAE Oct-Mar"],
        "gain_ci": metrics["gain_vs_persistence_oct_mar"],
        "gain_text": f"{float((w['persistence'] - w['target']).abs().mean() - (w['model'] - w['target']).abs().mean()):.1f}",
        "alerts_model": {k: alerts["Our model"][k] for k in ("bad days", "caught", "missed", "false alarms")},
        "alerts_persistence": {k: alerts["Persistence (last 24 h at 18:00)"][k] for k in ("bad days", "caught", "missed", "false alarms")},
        "starts": {"days": kinds_table["1. smog starts (clean -> bad)"]["days"],
                   "model": kinds_table["1. smog starts (clean -> bad)"]["model_warned"],
                   "persistence": kinds_table["1. smog starts (clean -> bad)"]["persistence_warned"]},
        "clears": {"days": kinds_table["3. air clears (bad -> clean)"]["days"],
                   "model": kinds_table["3. air clears (bad -> clean)"]["model_warned"],
                   "persistence": kinds_table["3. air clears (bad -> clean)"]["persistence_warned"]},
        "timetable": {"weeks": saved["weeks"], "fixed": saved["fixed timetable"], "persistence": saved["rule + persistence"],
                      "model": saved["rule + our forecast"], "best": saved["perfect hindsight"],
                      "vs_fixed": metrics["timetable_test_quota2"]["cleaner_than_fixed"],
                      "vs_fixed_ci": metrics["timetable_test_quota2"]["ci95_vs_fixed"],
                      "vs_persistence": metrics["timetable_test_quota2"]["cleaner_than_persistence_planner"],
                      "vs_persistence_ci": metrics["timetable_test_quota2"]["ci95_vs_persistence"]},
        "external": {"model": metrics["external_2026"]["table"]["Our frozen model + a real forecast, 2 days old (main)"]["MAE Oct-Mar"],
                     "persistence": metrics["external_2026"]["table"]["Persistence (last 24 h at 18:00), same sensor"]["MAE Oct-Mar"]},
    }
    data = {"model": {k: model[k] for k in ("features", "log_columns", "mean", "scale", "coef", "intercept", "cutoff",
                                             "alert_level", "likely_range_log", "reasons")},
            "cutoff_persistence": cutoff_pers, "rows": rows, "weeks": weeks, "examples": examples, "scores": scores}

    page = ROOT / "demo.html"
    html = page.read_text(encoding="utf-8")
    block = ("<!--DATA-START (written by scripts/build_demo.py; do not edit by hand)-->\n"
             '<script id="smog-data">window.SMOG_DATA = '
             + json.dumps(data, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")
             + ";</script>\n<!--DATA-END-->")
    new_html, count = re.subn(r"<!--DATA-START.*?<!--DATA-END-->", lambda _: block, html, flags=re.S)
    assert count == 1, "demo.html must contain exactly one DATA block"
    page.write_text(new_html, encoding="utf-8")
    print(f"demo.html: {len(rows)} evenings, {len(weeks)} school weeks, {len(new_html) / 1024:.0f} KB")
    print("timetable check against results/metrics.json passed:", {k: round(float(v), 2) for k, v in got.items()})
    print("examples:", examples)


if __name__ == "__main__":
    main()
