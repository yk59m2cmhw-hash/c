# Smog Tomorrow: should tomorrow's PE lesson be outdoors?

**Track:** AI + Climate
**Team:** Bakdaulet (solo)

**Notebook with saved outputs:** [`notebooks/SmogTomorrow.ipynb`](notebooks/SmogTomorrow.ipynb) · [open in Colab](https://colab.research.google.com/github/yk59m2cmhw-hash/c/blob/claude/relaxed-dirac-2g7xn0/notebooks/SmogTomorrow.ipynb) · **All results:** [`results/RESULTS.md`](results/RESULTS.md)

## The problem

Almaty, Kazakhstan, lies at the foot of high mountains, and in the heating season smoke gets trapped over the city. At the monitor we use, daytime PM2.5 was above 35 µg/m³ on 119 of 398 measured days between October 2024 and November 2025, all but two of them from October to March. A PE teacher has to decide the evening before whether tomorrow's lessons can be outdoors, and the simplest guess is that tomorrow will be like today.

## What we built

Every evening at 18:00 the tool takes today's air and weather measurements and forecasts tomorrow's school hours (08:00–18:00): the expected PM2.5, a likely range, a plain decision (**PE indoors** or **PE outdoors**) and the three inputs that moved the forecast most. In the demo you pick an evening from the test period and see the forecast next to what was measured the next day.

> Evening of 16 Dec 2024: today was clean (23 µg/m³). Forecast: about 63 µg/m³, likely 39–113, ⚠️ smog warning. Measured the next day: 67 µg/m³.

## What we added

We started from suggested project **4.3.2 Next-day air quality forecast** and added:

- **Our own place and user:** Almaty, a school, and a target that matches the decision (the mean over school hours, forecast at 18:00 from data that already exists).
- **Our own question 1: is a free global forecast enough for Almaty?** No. The CAMS global model reads 13.6 µg/m³ too low here, and with the plain rule "warn above 35" it would have warned on only 47 of 119 smog days.
- **Our own question 2: what happens on the days the air changes?** These are the days a forecast is for, and "tomorrow = today" is wrong on every one of them.
- **A stated decision rule and a locked test.** A missed smog day counts three times a false alarm, and every method's warning threshold was chosen on validation data with that rule. The split and settings were committed to git (`7f98623`) before the test period was scored.

## How it works

**Data.** 34,534 hourly PM2.5 readings (Apr 2020 – Nov 2025) from a reference-grade monitor in Almaty and 126,509 weather reports from Almaty airport. A day counts only if at least 6 of its 10 daytime hours were measured; outage days are dropped, not filled in. This leaves 1,348 evening-to-next-day pairs.

**Model.** Gradient-boosted decision trees (scikit-learn) on 30 inputs: recent PM2.5, airport weather (wind, temperature, pressure, visibility, rain or snow, fog) and the calendar. Trees fit here because the effect of weather is not a straight line and some readings are missing.

**Split by date, never shuffled.** Train to Sep 2023 (598 days), validation Oct 2023 – Sep 2024 (352 days, used for every choice), test Oct 2024 – Nov 2025 (398 days, scored once).

## Results

Test period: 398 days, 119 smog days. MAE is the average miss in µg/m³.

| Method | MAE | Smog days missed | False alarms |
|---|---|---|---|
| Baseline: tomorrow = today | 15.3 | 11 | 76 |
| Global model (CAMS) | 16.6 | 9 | 83 |
| Linear model | 13.1 | 21 | 45 |
| **Our model** | **12.3** | 16 | 52 |

Our baseline scored 15.3 and our model 12.3 on held-out test data, 20% lower (95% interval for the gain: 1.7 to 4.5 µg/m³). The model raises a third fewer false alarms than the baseline but **misses more smog days, 16 against 11**, so by our 3-to-1 rule it is only modestly ahead (100 cost points against 109). On the 69 days when the air crossed the 35 line, the model was on the right side 36 times.

![Forecast against measurements in winter 2024-25](results/fig_forecast_vs_measured.png)

**Where it fails.** The eight largest misses are all in January–February 2025, when PM2.5 doubled or halved overnight (80 → 165; 184 → 48). Wind at the airport was about 2 m/s on both days with no rain or snow, so nothing in our inputs announced the change. We think the cause is the temperature inversion above the city forming or breaking, which a ground station 14 km away cannot see, and the model knows nothing about tomorrow's weather. Also, the monitor's public record stops on 14 Nov 2025, so the demo replays past evenings instead of forecasting the real tomorrow.

## What we'd do next

- Add tomorrow's weather forecast and weather-balloon data so the model can see inversions, then check whether the January misses shrink.
- Connect a sensor that reports today, and try the warning with PE teachers at a school in Almaty for one month.

## Sources

- **PM2.5:** OpenAQ public data archive, location [8876 "Almaty"](https://explore.openaq.org/locations/8876), provider AirNow ([archive docs](https://docs.openaq.org/aws/about)).
- **Weather:** Iowa Environmental Mesonet [ASOS/METAR archive](https://mesonet.agron.iastate.edu/request/download.phtml), station UAAA.
- **Global model:** CAMS global forecasts (Copernicus Atmosphere Monitoring Service) through the [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api).
- **Libraries:** pandas, NumPy, scikit-learn, matplotlib, Gradio. **Starting point:** Veritas AI project brief 4.3.2.
- **AI tools:** Claude Code (Anthropic), an AI coding agent. It did most of the engineering: it found the data sources, wrote the code, ran the experiments and drafted this write-up. I set the task and its rules (one real user, public data only, a fair baseline, a test period locked before scoring, honest reporting), reviewed the results, and can explain every step.

---

## Run it yourself

No API key, no GPU, about one minute.

```bash
pip install -r requirements.txt
python src/run_experiment.py     # rebuilds every number and figure in results/
python app.py                    # opens the demo page
```

`python src/download_data.py` fetches the raw data again from the original sources; the copies used for the reported numbers are in `data/raw/`.

| Path | What it is |
|---|---|
| `src/download_data.py` | downloads all data |
| `src/almaty_air.py` | features, baselines, model, metrics |
| `src/run_experiment.py` | the whole experiment → `results/` |
| `src/demo.py`, `app.py` | the demo page |
| `notebooks/SmogTomorrow.ipynb` | the same steps as a notebook, outputs saved |
| `PROJECT_SPEC.md` | the evaluation protocol, written before the test was scored |
