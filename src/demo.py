"""The demo: pick an evening -> forecast for the next day, next to what really happened.

Used by app.py (Gradio web page) and by the notebook.
"""
from __future__ import annotations

import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import almaty_air as aa

warnings.filterwarnings("ignore")

INK, MUTED, GRID, SURFACE, BLUE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#2a78d6"
# evenings from the test period: smog arrives / clean summer day / smog clears / a missed smog day / a false alarm
EXAMPLES = ["2024-12-16", "2025-07-09", "2025-10-31", "2025-10-27", "2024-12-07"]

# plain-language names for the inputs we explain to the user
PLAIN = {
    "pm_24h": "PM2.5 over the last 24 hours", "pm_day": "today's daytime PM2.5", "pm_evening": "PM2.5 in the last 3 hours",
    "pm_night": "last night's PM2.5", "pm_week": "average PM2.5 this week", "temp_min24h": "coldest temperature in the last 24 hours",
    "temp_day": "today's daytime temperature", "pressure_day": "air pressure today", "pressure_change": "pressure change since yesterday",
    "wind_day": "today's wind speed", "wind_evening": "wind in the last 3 hours", "vis_day": "visibility at the airport today",
    "temp_change": "temperature change since yesterday", "precip_share": "rain or snow in the last 24 hours",
}
UNITS = {"pm": "µg/m³", "temp": "°C", "pressure": "hPa", "wind": "m/s", "vis": "km", "precip": "share of reports"}


class Forecaster:
    """Everything the demo needs, built once at start-up from the files in data/raw/."""

    def __init__(self) -> None:
        pm = aa.load_pm(aa.RAW / "openaq_almaty_8876_pm25_hourly.csv")
        self.table = aa.build_table(pm, aa.load_metar(), aa.load_cams())
        parts = aa.split(self.table)
        # alert threshold: chosen on validation with a model that saw only the training years
        early = aa.fit_model(parts["train"])
        self.threshold = aa.tune_threshold(parts["valid"]["y"], early.predict(parts["valid"][aa.FEATURES]))
        # final model: trained on train+validation, so every test-period evening is unseen
        fit_rows = pd.concat([parts["train"], parts["valid"]])
        self.model = aa.fit_model(fit_rows)
        self.low, self.high = aa.fit_quantile_models(fit_rows)
        self.typical = fit_rows[aa.FEATURES].median()
        self.test = parts["test"]
        self.first, self.last = self.test.index.min(), self.test.index.max()

    def explain(self, row: pd.Series, top: int = 3) -> list[str]:
        """Ask the model 'what if this input had its ordinary value?' and report the biggest shifts."""
        base = float(self.model.predict(row[aa.FEATURES].to_frame().T.astype(float))[0])
        shifts = []
        for name, label in PLAIN.items():
            if pd.isna(row[name]):
                continue
            changed = row[aa.FEATURES].copy()
            changed[name] = self.typical[name]
            shift = base - float(self.model.predict(changed.to_frame().T.astype(float))[0])
            shifts.append((abs(shift), shift, name, label))
        lines = []
        for _, shift, name, label in sorted(shifts, reverse=True)[:top]:
            unit = UNITS[name.split("_")[0]]
            direction = "pushes the forecast up" if shift > 0 else "pulls the forecast down"
            lines.append(f"{label}: **{row[name]:.1f} {unit}** (typical over the year: {self.typical[name]:.1f}) {direction} by about {abs(shift):.0f} µg/m³")
        return lines

    def forecast(self, evening: str):
        """Returns (markdown text, matplotlib figure) for the evening of the given date."""
        try:
            day = pd.Timestamp(str(evening or "").strip()[:10])
        except (ValueError, TypeError):
            day = pd.NaT
        if pd.isna(day):
            return f"**Could not read the date “{evening}”.** Please type it as YYYY-MM-DD, for example 2024-12-16.", None
        day = day.normalize()
        if not (self.first <= day <= self.last):
            return (f"**Pick a date between {self.first.date()} and {self.last.date()}.** These are the test-period evenings: "
                    "the model never saw them in training, so the comparison with reality is fair."), None
        if day not in self.test.index:
            return (f"**No forecast for {day.date()}:** the monitor has too few daytime readings on this day or the next one. "
                    "Please pick a neighbouring date."), None

        row = self.test.loc[day]
        x = row[aa.FEATURES].to_frame().T.astype(float)
        pred, low, high = (float(m.predict(x)[0]) for m in (self.model, self.low, self.high))
        low, high = min(low, pred), max(high, pred)
        truth, today = float(row["y"]), float(row["persistence"])
        tomorrow = (day + pd.Timedelta(days=1)).strftime("%A, %d %B %Y")
        warn = pred > self.threshold
        bad = truth > aa.ALERT_LEVEL

        decision = ("### ⚠️ Smog warning: plan PE **indoors** tomorrow" if warn
                    else "### ✅ No warning: PE can stay **outdoors** tomorrow")
        if warn and bad:
            verdict = "✔ The warning was right: the day was above the 35 µg/m³ action level."
        elif warn and not bad:
            verdict = "✘ False alarm: the day turned out below the action level."
        elif not warn and bad:
            verdict = "✘ Missed smog day: no warning was given, but the day was above the action level."
        else:
            verdict = "✔ Correct: no warning, and the day stayed below the action level."
        naive_wrong = (today > aa.ALERT_LEVEL) != bad
        naive = (f"“Tomorrow = today” would have said {today:.0f} µg/m³ — "
                 + ("on the wrong side of the action level." if naive_wrong else "on the correct side of the action level."))

        text = "\n\n".join([
            f"## Forecast for {tomorrow}",
            f"Made at 18:00 on {day.date()} from that day's air and weather measurements.",
            decision,
            f"**Expected daytime PM2.5 (08:00–18:00): about {pred:.0f} µg/m³**, likely between {low:.0f} and {high:.0f}. "
            f"A warning is given when the forecast is above {self.threshold:.0f} µg/m³.",
            "**Why:**\n" + "\n".join(f"- {line}" for line in self.explain(row)),
            "---",
            f"## What actually happened\n**Measured: {truth:.0f} µg/m³.** {verdict}\n\n{naive}",
            "*Prototype for one monitor in Almaty. The model cannot see tomorrow's weather, so sudden changes are often missed; "
            "on the test period it missed 16 of 119 smog days and raised 52 false alarms.*",
        ])
        return text, self.plot(day, pred, low, high, truth)

    def plot(self, day, pred, low, high, truth):
        history = self.table.loc[day - pd.Timedelta(days=6): day, "pm_day"]
        tomorrow = day + pd.Timedelta(days=1)
        fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=120)
        fig.set_facecolor(SURFACE)
        ax.set_facecolor(SURFACE)
        ax.plot(history.index, history.values, color=INK, linewidth=2, marker="o", markersize=5, label="Measured (known at forecast time)")
        ax.plot([day, tomorrow], [history.iloc[-1], truth], color=INK, linewidth=1.2, linestyle=(0, (2, 3)))
        ax.plot([tomorrow], [truth], color=INK, marker="o", markersize=9, markerfacecolor=SURFACE, markeredgewidth=2, linestyle="none",
                label="Measured the next day")
        ax.errorbar([tomorrow], [pred], yerr=[[pred - low], [high - pred]], color=BLUE, marker="s", markersize=9, capsize=5, linewidth=2,
                    linestyle="none", label="Forecast with likely range")
        ax.axhline(aa.ALERT_LEVEL, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
        ax.text(1.01, aa.ALERT_LEVEL, "35 µg/m³", transform=ax.get_yaxis_transform(), color=MUTED, fontsize=8, va="center")
        ax.set_ylim(bottom=0, top=max(60.0, float(np.nanmax([history.max(), truth, high])) * 1.3))
        ax.set_ylabel("Daytime PM2.5, µg/m³", color=MUTED, fontsize=9)
        ax.set_xticks(list(history.index) + [tomorrow], [d.strftime("%d %b") for d in list(history.index) + [tomorrow]])
        ax.tick_params(colors=MUTED, labelsize=8, length=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False, fontsize=8, labelcolor=INK)
        fig.tight_layout()
        return fig


def build_app(forecaster: Forecaster | None = None):
    import gradio as gr

    fc = forecaster or Forecaster()
    with gr.Blocks(title="Smog Tomorrow: Almaty") as app:
        gr.Markdown(
            "# Smog Tomorrow: should tomorrow's PE lesson be outdoors?\n"
            "An evening forecast of tomorrow's daytime air pollution (PM2.5) for schools in Almaty, Kazakhstan. "
            f"Pick any evening from the test period ({fc.first.date()} to {fc.last.date()}). The model never saw these days in training, "
            "so you can compare its forecast with what was really measured.")
        with gr.Row():
            date = gr.Textbox(label="Evening of (YYYY-MM-DD)", value=EXAMPLES[0], max_length=10, scale=3)
            button = gr.Button("Forecast tomorrow", variant="primary", scale=1)
        gr.Examples(examples=EXAMPLES, inputs=date, label="Examples: smog arrives · clean summer day · smog clears · a missed smog day · a false alarm")
        with gr.Row():
            text = gr.Markdown()
            chart = gr.Plot(show_label=False)
        button.click(fc.forecast, inputs=date, outputs=[text, chart])
        date.submit(fc.forecast, inputs=date, outputs=[text, chart])
    return app
