#!/usr/bin/env python3
"""Checks the live (sensor-free) forecast path without using the network.

1. For past evenings, the live code must build exactly the same weather and
   calendar inputs as the experiment did, so the live model is the tested model.
2. Weather reports after 18:00 of the issue day must not change the forecast.
3. Before 18:00 the forecast must be issued for the previous evening, not for today.

    python tests/test_live_forecast.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import almaty_air as aa  # noqa: E402
from live import LiveForecaster  # noqa: E402


def main() -> None:
    pm = aa.load_pm(aa.RAW / "openaq_almaty_8876_pm25_hourly.csv")
    metar = aa.load_metar()
    table = aa.build_table(pm, metar)
    live = LiveForecaster(table)
    evenings = aa.split(table)["test"].sample(25, random_state=1).index
    for day in evenings:
        late = pd.Timestamp(day).tz_localize(aa.TZ) + pd.Timedelta(hours=23)          # asked at 23:00 the same day
        f = live.forecast(metar=metar, now=late)
        assert f["issued_for_evening"] == str(day.date()), (day, f["issued_for_evening"])
        want = table.loc[day, aa.SENSOR_FREE_FEATURES].astype(float).to_numpy()
        got = np.array([np.nan if f["inputs"][k] is None else f["inputs"][k] for k in aa.SENSOR_FREE_FEATURES])
        assert np.allclose(want, got, atol=0.006, equal_nan=True), f"{day.date()}: live inputs differ from the experiment's inputs"
        # the same question asked the next morning (more reports exist by then) must give the same answer
        morning = pd.Timestamp(day).tz_localize(aa.TZ) + pd.Timedelta(hours=24 + 9)
        g = live.forecast(metar=metar, now=morning)
        assert g["issued_for_evening"] == f["issued_for_evening"] and g["forecast_pm25"] == f["forecast_pm25"], f"{day.date()}: later reports changed the forecast"
        # asked at 15:00, today's evening has not come yet: the forecast is for the evening before
        early = live.forecast(metar=metar, now=pd.Timestamp(day).tz_localize(aa.TZ) + pd.Timedelta(hours=15))
        assert early["issued_for_evening"] < f["issued_for_evening"], f"{day.date()}: a forecast was issued before 18:00"
    print(f"OK: {len(evenings)} evenings checked; live inputs equal the experiment's inputs, and nothing after 18:00 is used.")


if __name__ == "__main__":
    main()
