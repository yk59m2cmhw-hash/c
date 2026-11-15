#!/usr/bin/env python3
"""Checks that a forecast uses nothing measured after 18:00 on the day it is issued.

For a sample of evenings we delete every PM2.5 reading and weather report after
18:00 of that day, rebuild the feature table, and require that
  1. all 30 model inputs for that evening are exactly the same as before, and
  2. the answer (tomorrow's value) is no longer available.
If an input secretly used later data, it would change and the test would fail.

    python tests/test_no_leakage.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import almaty_air as aa  # noqa: E402


def main() -> None:
    pm = aa.load_pm(aa.RAW / "openaq_almaty_8876_pm25_hourly.csv")
    metar = aa.load_metar()
    full = aa.build_table(pm, metar)
    usable = full[full["y"].notna() & full["persistence"].notna()]
    evenings = usable.sample(40, random_state=0).index
    for day in evenings:
        cutoff = pd.Timestamp(day).tz_localize(aa.TZ) + pd.Timedelta(hours=aa.ISSUE_HOUR)
        cut = aa.build_table(pm[pm.index < cutoff], metar[metar.index < cutoff])
        before = full.loc[day, aa.FEATURES].astype(float).to_numpy()
        after = cut.loc[day, aa.FEATURES].astype(float).to_numpy()
        same = np.isclose(before, after, equal_nan=True)
        assert same.all(), f"{day.date()}: inputs changed when later data was removed: {[f for f, ok in zip(aa.FEATURES, same) if not ok]}"
        assert pd.isna(cut.loc[day, "y"]), f"{day.date()}: the answer is still visible after removing later data"
    # the three periods must not overlap and must be in time order
    parts = aa.split(full)
    assert parts["train"]["target_day"].max() < parts["valid"]["target_day"].min() < parts["valid"]["target_day"].max() < parts["test"]["target_day"].min()
    print(f"OK: {len(evenings)} evenings checked, no model input uses data after 18:00; train < validation < test in time.")


if __name__ == "__main__":
    main()
