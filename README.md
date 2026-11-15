# Smog Tomorrow? A PE timetable that follows clean air (Almaty)

**Track:** AI + Climate · **Team:** solo participant (name on the submission form) · **Starting point:** suggested project 4.3.2, Next-day air quality forecast

**Code:** [almaty_smog_tomorrow.ipynb](almaty_smog_tomorrow.ipynb) with saved outputs; it runs top to bottom in under a minute, no API key, no GPU ·
[open in Google Colab](https://colab.research.google.com/github/yk59m2cmhw-hash/c/blob/claude/keen-bohr-rsb2xk/almaty_smog_tomorrow.ipynb) ·
every number below is printed by the notebook and saved in [`results/metrics.json`](results/metrics.json)

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

(A replay of a held-out day. It is also the model's largest error: it saw the rise, not its size.)

## What we added to the suggested project

1. **A real clock.** The forecast is made at 18:00 from readings that existed then; the baseline gets the same information.
2. **A real weather forecast.** The test is repeated with archived forecasts issued one and two days earlier.
3. **The days that matter.** Smog starts and clearings are scored separately.
4. **An action.** A rule with no tuned numbers picks the 2 outdoor PE days of each school week, scored by what children breathe.
5. **A professional rival.** The free global CAMS model, next to "tomorrow = today".
6. **A harder second test.** The frozen model on 2026 data from a different, low-cost sensor, under rules committed to git before the run. The forecast failed it, and we report that.

## How it works

**Data.** Hourly PM2.5 from the reference-grade monitor "Almaty" (OpenAQ location 8876), April 2020 – November 2025, and weather from Open-Meteo (ECMWF IFS 9 km): 1,282 evenings with inputs and an answer.

**Split by date, never shuffled.** Train to September 2023 (538 evenings), validation to September 2024 (348), test from 11 October 2024 to 13 November 2025 (396), scored once for the forecast.

**Model.** Ridge regression on the logarithm of PM2.5 with 26 inputs: air history, season and tomorrow's city weather. It was chosen on two past winters by a rule written beforehand: take the simplest model unless a more complex one is more than 5% better. Gradient boosting and an inversion signal did not pass.

## Results on the held-out test period

| Forecast | Average error, Oct–Mar (µg/m³) | All days |
|---|---|---|
| Persistence: last 24 h at 18:00 | 17.0 | 10.9 |
| Typical value for the month | 18.5 | 11.7 |
| Global model (CAMS) | 16.6 | 11.0 |
| **Our model** | **12.2** | **8.2** |

Our baseline scored 17.0 and our model 12.2 on held-out test data: 4.8 µg/m³ less error per day (95% interval 3.0 to 7.0).

| Warning "tomorrow above 35.4 µg/m³", 216 Oct–Mar days, 88 bad | Caught | Missed | False alarms |
|---|---|---|---|
| Persistence, cutoff tuned like ours | 69 | 19 | 40 |
| Global model (CAMS), cutoff tuned like ours | 87 | 1 | 66 |
| **Our model** | **72** | **16** | **22** |

- **When smog starts** (31 days) the model warned on 17, persistence on 12. **When the air clears** (28 days) persistence raised a false alarm on all 28, the model on 13.
- **With real weather forecasts** the error did not grow (12.2 and 12.1). **The global model** reads 10.7 µg/m³ too low here and catches the bad days only by warning on 153 of the 216 days.
- **The timetable** (29 school weeks, 2 outdoor lessons each): PM2.5 on lesson days was 40.0 with a fixed timetable, 37.5 with the rule fed by persistence, 35.4 with the rule fed by our forecast and 26.7 with perfect hindsight. Our planner was 4.6 µg/m³ cleaner than a fixed timetable (95% interval 0.8 to 8.8).

![Test period](results/figures/03_test_period.png)

## Where it fails, and why we think so

- **On a different sensor.** On a low-cost citizen sensor 2 km away (January – November 2026) the frozen model lost to persistence: 9.9 against 7.5 µg/m³ on Oct–Mar days (1.3 to 3.4 worse). It had learned the level of its own monitor: this sensor reads about 0.68 times what the model expects. Correcting that one number, in a second test also written down first, brought the error level with persistence (3.9 against 4.2) but not below it. The timetable rule still helped there (14.9 against 17.5 for a fixed timetable, interval 0.2 to 5.2), because it only has to rank the days.
- **During school hours.** The model forecasts the daily average, but the air between 08:00 and 18:00 is dirtier (51.8 against 39.1 µg/m³). Counted by school hours, our warning missed 34 of 115 bad days (persistence 32). A cutoff tuned for school hours on the validation year misses 7 (persistence 19) but raises 61 false alarms.
- **On the dirtiest days.** On the 11 test days above 100 µg/m³ the forecast was on average 35 µg/m³ too low, and it still missed 14 of 31 smog starts.
- **The planner is not proven better than the same rule with persistence** (2.1 µg/m³ cleaner, 95% interval −1.3 to 5.9).

![2026, a sensor the model never saw](results/figures/05_external_2026.png)

## What we'd do next

1. Forecast school hours directly, and give the planner forecasts for the whole week.
2. Put a sensor at one school, collect one winter of readings, re-fit the model to it and try the warning with its PE teachers.

## Honest notes

- A prototype, not health advice. One monitor is one point in the city.
- Before the rules were fixed, a quick correlation check was run on all years, including the test period; no input was chosen because of it. The timetable, CAMS and school-hours checks came after the forecast test and did not change the model. Each 2026 test used rules committed before its run (`dd8b550`, `62ff508`).
- The two instruments never ran at the same time, so we cannot tell whether the 2026 sensor reads low or the air was cleaner. More notes are at the end of the notebook.

## Sources

- **Air data:** OpenAQ, [location 8876 "Almaty"](https://explore.openaq.org/locations/8876), provider AirNow, licence US Public Domain; downloaded from the [public OpenAQ archive](https://docs.openaq.org/aws/about).
- **Weather data:** [Open-Meteo](https://open-meteo.com/) Historical Weather API and Previous Runs API (ECMWF IFS), licence CC BY 4.0.
- **Global model:** CAMS global forecasts (Copernicus Atmosphere Monitoring Service) through the [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api).
- **2026 sensor:** [sensor.community](https://sensor.community/) archive, SDS011 sensor no. 78340, licence ODbL.
- **Air categories:** [US EPA AQI fact sheet, 2024](https://www.epa.gov/system/files/documents/2024-02/pm-naaqs-air-quality-index-fact-sheet.pdf).
- **Libraries:** pandas, NumPy, scikit-learn, Matplotlib, requests; LightGBM was tried during development; jupytext and nbclient built the notebook.
- **Starting point:** Veritas AI project brief 4.3.2.
- **AI tools:** Claude Code (Anthropic's AI coding agent). It did most of the engineering: it found the data sources, wrote the code, ran the experiments and drafted this text. I set the task and its rules (one real user, public data only, a fair baseline, a test period locked before scoring, honest reporting of weak results), chose the Climate track, asked for the timetable step and reviewed the results.

---

**Run it yourself.** `pip install -r requirements.txt`, then open the notebook and run all cells. It reads the saved files in `data/raw/` and calls no API. How those files were downloaded: [`scripts/`](scripts/README.md). Process notes in Russian (protocol, requirements, status): [`docs/process_ru/`](docs/process_ru/).
