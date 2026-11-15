# Smog Tomorrow? A PE timetable that follows clean air (Almaty)

**Track:** AI + Climate · **Team:** solo participant (name on the submission form) · **Starting point:** suggested project 4.3.2, Next-day air quality forecast

**Code:** [almaty_smog_tomorrow.ipynb](almaty_smog_tomorrow.ipynb) — runs top to bottom in under a minute, no API key, no GPU ·
[open in Google Colab](https://colab.research.google.com/github/yk59m2cmhw-hash/c/blob/claude/breathing-timetable/almaty_smog_tomorrow.ipynb)

## The problem

Almaty lies in a basin under the mountains, and in winter polluted air gets trapped over the city. In our test data the air was "unhealthy for sensitive groups" or worse on 88 of 216 heating-season days. A PE teacher has to decide the evening before whether tomorrow's lesson can be outdoors. The usual guess, "tomorrow will be like today", fails exactly when it matters: on the first day of a smog episode and on the first clean day after one.

## What we built

**In:** PM2.5 readings up to 18:00 today and tomorrow's weather forecast.
**Out:** tomorrow's average PM2.5 with a likely range, an "outdoors / indoors" advice with the main reasons, and a weekly plan that moves the outdoor lessons to the cleanest days.

```
Forecast made: 01 Feb 2025, 18:00  →  for 02 Feb 2025
Tomorrow's PM2.5: about 41 µg/m³ (likely range 21–58)
Air category: Unhealthy for sensitive groups
Advice for PE: plan the lesson INDOORS
Main reasons: temperature tomorrow — pushes PM2.5 up (+40%); season and day of week — pushes PM2.5 up (+14%); air in the last 24 hours — pushes PM2.5 up (+11%)
What was measured the next day: 98 µg/m³ → the advice was right
```

(This is a replay of a held-out day. The same day is also the model's largest error: it saw the rise, not its size.)

## What we added to the suggested project

1. **A real clock.** The forecast is made at 18:00 and may only use readings that existed then. The persistence baseline gets the same information.
2. **Our own question: does it survive a real weather forecast?** We re-ran the test with archived forecasts issued one and two days earlier.
3. **Our own question: when does "tomorrow = today" fail?** We scored the days when smog starts and when the air clears separately.
4. **From a forecast to an action.** A rule with no tuned numbers picks the 2 outdoor PE days of each school week. It is scored by what children breathe, next to a planner with perfect hindsight.

## How it works

**Data.** Hourly PM2.5 from the reference-grade monitor "Almaty" (OpenAQ location 8876), April 2020 – November 2025: 34,476 valid hours. We dropped negative readings, required 18 of 24 hours for a daily average, and handled Kazakhstan's 2024 time-zone change by hand. Weather comes from Open-Meteo (ECMWF IFS 9 km). This gives 1,282 evenings with inputs and an answer.

**Split by date.** Train to September 2023 (538 evenings), validation to September 2024 (348), test from 11 October 2024 to 13 November 2025 (396). The test period was used once for the forecast.

**Model.** Ridge regression on the logarithm of PM2.5 with 26 inputs: air history, season, and tomorrow's city weather. We chose it on two past winters with a rule written beforehand: take the simplest model unless a more complex one is more than 5% better.

## Results on the held-out test period

| Forecast | Average error, Oct–Mar (µg/m³) | All days |
|---|---|---|
| Persistence: last 24 h at 18:00 | 17.0 | 10.9 |
| Persistence: full calendar day (knows 6 h more) | 15.3 | 9.9 |
| Typical value for the month | 18.5 | 11.7 |
| **Our model** | **12.2** | **8.2** |

The model's error is 4.8 µg/m³ per day smaller than persistence (95% interval 3.0 to 7.0).

| Warning "tomorrow above 35.4 µg/m³", 216 Oct–Mar days, 88 bad | Caught | Missed | False alarms |
|---|---|---|---|
| Persistence, warn if last 24 h above 35.4 | 57 | 31 | 28 |
| Persistence, cutoff tuned like ours | 69 | 19 | 40 |
| **Our model** | **72** | **16** | **22** |

- **When smog starts** (31 days): the model warned on 17, tuned persistence on 12.
- **When the air clears** (28 days): persistence raised a false alarm on all 28, the model on 13.
- **With real weather forecasts** the error did not grow: 12.2 with a one-day-old forecast and 12.1 with a two-day-old one.
- **The timetable** (29 complete school weeks, 2 outdoor lessons each): average PM2.5 on lesson days was 40.0 with a fixed timetable, 37.5 with the rule fed by persistence, 35.4 with the rule fed by our forecast, and 26.7 with perfect hindsight. Our planner removed 35% of the avoidable pollution; it was 4.6 µg/m³ cleaner than a fixed timetable (95% interval 0.8 to 8.8).

![Test period](results/figures/03_test_period.png)

## Where it fails, and why we think so

- **Very dirty days.** On the 11 test days above 100 µg/m³ the forecast was on average 35 µg/m³ too low. The model is a weighted sum trained on few extreme days, so it is cautious at the top.
- **It still misses 14 of 31 smog starts.** The first one in the test period (13 Nov 2024, measured 36) was forecast at 20.
- **The planner is not proven better than the same rule with persistence**: 2.1 µg/m³ cleaner, 95% interval −1.3 to 5.9. It beat the fixed timetable in 17 of 29 weeks and lost in 12.
- **Weeks with no clean day.** In the dirtiest test week (3–7 Feb 2025) the planner waited for cleaner air that never came and was forced onto Thursday and Friday (117 and 110), although Tuesday (83) was the least bad. It only sees one day ahead.
- **The likely range is a little too narrow**: built to hold 80% of days, it held 76%.
- **Two ideas did not help** on past winters and were left out: an inversion signal (mountain minus city temperature) and gradient boosting.

## What we'd do next

1. Give the planner forecasts for the whole week, so it can compare tomorrow with the days after it.
2. Connect a live sensor at a school. The public archive of this monitor ends on 14 November 2025, so the demo replays held-out days.

## Honest notes

- One monitor is one point in the city. This is a prototype, not health advice; a school should set its own rule.
- Before the rules were fixed, a quick correlation check was run on all years, including the test period. No input was chosen because of it.
- The timetable section was added after the forecast test. Its rule has no tuned numbers and was tried on the validation year first; the forecasting model was not changed.
- All numbers above are printed by the notebook and saved in `results/metrics.json`.

## Sources

- **Air data:** OpenAQ, [location 8876 "Almaty"](https://explore.openaq.org/locations/8876), provider AirNow, licence US Public Domain; downloaded from the [public OpenAQ archive](https://docs.openaq.org/aws/about).
- **Weather data:** [Open-Meteo](https://open-meteo.com/) Historical Weather API and Previous Runs API (ECMWF IFS), licence CC BY 4.0.
- **Air categories:** [US EPA AQI fact sheet, 2024](https://www.epa.gov/system/files/documents/2024-02/pm-naaqs-air-quality-index-fact-sheet.pdf).
- **Libraries:** pandas, NumPy, scikit-learn, Matplotlib; Gradio for the optional demo page; LightGBM was tried during development; jupytext and nbclient built the notebook.
- **Starting point:** Veritas AI project brief 4.3.2.
- **AI tools:** Claude Code (Anthropic's AI coding agent). It wrote the code and the first draft of this text, downloaded the data and proposed the evaluation steps, following my task, constraints and choices. EDIT BEFORE SUBMITTING: describe in one sentence what you did yourself.
