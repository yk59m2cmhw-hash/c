# Подача: ответы формы, видео, чек-лист

Форма: https://airtable.com/appypCyHN77hElIcS/shrXA5VBFdugmoXl6 · дедлайн **16 ноября 09:59 по Алматы** (15 ноября 23:59 ET). Подавать можно повторно, засчитывается последняя подача. Поля ниже сверены с живой формой 15 ноября в 22:50 по Алматы.

## 1. Ответы для формы

| Поле формы | Что вписать | По-русски |
|---|---|---|
| Project Title * | `Smog Tomorrow: should tomorrow's PE lesson be outdoors?` | «Смог завтра: проводить ли завтра физкультуру на улице?» |
| Your Full Name * / Your School * / Your Email * | впиши сам, как должно быть в сертификате | — |
| Building As * | вариант для одного участника (Solo) | один |
| Code Link * | `https://github.com/yk59m2cmhw-hash/c/tree/claude/sleepy-mendel-te40eu` | репозиторий, ветка с последней версией |
| Write-up Link | `https://github.com/yk59m2cmhw-hash/c/blob/claude/sleepy-mendel-te40eu/README.md` | README и есть write-up |
| Write-up File | оставить пустым | нужен только один вариант write-up |
| Demo Video Link | ссылка на загруженное тобой видео (см. раздел 2) | необязательно, но рекомендуют |
| Track * | Climate | — |
| One-Sentence Pitch | текст ниже | — |
| New to AI? | ответь честно про себя | — |
| Rules Confirmation | отметь, только если согласен с каждым пунктом | см. ниже |
| Anything Else We Should Know | текст ниже | — |

**One-Sentence Pitch** (вписать как есть):

`Smog Tomorrow helps a PE teacher in Almaty decide the evening before whether tomorrow's lesson can be outdoors, by forecasting tomorrow's school-hours PM2.5 from airport weather, with or without a PM2.5 monitor.`

Смысл: помогает учителю физкультуры в Алматы накануне вечером решить, можно ли завтра заниматься на улице, прогнозируя завтрашний PM2.5 в школьные часы по погоде аэропорта, с монитором PM2.5 или без него.

**Anything Else We Should Know** (вписать как есть; в форме нет отдельных полей «Starting point», «What we added» и «Credits», поэтому они здесь):

```
Starting point: suggested project 4.3.2 (Next-day air quality forecast).
What we added: our own city and user (Almaty schools; a school-hours target forecast at 18:00); a comparison with the free CAMS global model, which reads 13.6 µg/m³ too low here; a sensor-free model that uses airport weather only and forecasts the real tomorrow, because the public record of the monitor we trained on ends on 14 Nov 2025; a warning rule with a stated cost (a missed smog day counts 3x a false alarm), with missed days and false alarms reported separately. The settings were committed to git before each model was scored on the test period (commits 7f98623 and 37fb006).
Honest notes: the main model misses more smog days than the persistence baseline (16 against 11) and the sensor-free model misses 19, while both raise fewer false alarms. The sensor-free model was scored after the main model, so it was a second look at the same test period. The live forecast cannot be scored yet.
Credits: OpenAQ public archive (location 8876, provider AirNow); Iowa Environmental Mesonet METAR archive (station UAAA); CAMS global forecasts via the Open-Meteo Air Quality API; scikit-learn, pandas, NumPy, matplotlib, Gradio; Veritas AI project brief 4.3.2. AI tool: Claude Code (Anthropic), an AI coding agent, which did most of the engineering under my direction; this is stated in the write-up.
The demo video is a screen recording of the working demo with captions instead of a voice-over.
```

Смысл по-русски: отправная точка 4.3.2; что добавили (свой город и пользователь, сравнение с CAMS, модель без датчика с живым прогнозом, правило тревоги с ценой ошибки, фиксация настроек в git до теста); честные оговорки (обе модели пропускают больше смоговых дней, чем baseline; вторая модель оценена на том же тесте вторым заходом; живой прогноз пока нельзя проверить); источники данных, библиотеки и AI-инструмент; видео записано с подписями вместо голоса.

**Про галочку Rules Confirmation.** Ты подтверждаешь шесть пунктов:
1. Вся работа сделана между 00:00 ET 14 ноября и 23:59 ET 15 ноября. Выполнено: первый коммит 15 ноября.
2. AI/ML делает основную работу. Да: прогноз строит обученная модель.
3. Указаны все данные, модели, tutorials и AI-инструменты, **и ты можешь объяснить каждую часть проекта**. Это про тебя лично: пройди `docs/EXPLAIN_RU.md`, разделы 3–8 и 12.
4. Только публичные данные, личных данных нет. Да.
5. Результаты настоящие. Да: каждое число пересчитывается командой `python src/run_experiment.py`.
6. Все перечисленные участники участвовали. Ты один.

## 2. Видео (до 2 минут)

Готовый файл: `docs/demo_video.mp4` (1 мин 54 с, 2,8 МБ). Это автоматическая запись экрана настоящей работающей демо-страницы с английскими подписями, без голоса. Записано скриптом `docs/video/record.js`.

Что в нём по секундам:

| Время | Что на экране | Подпись (English) | Смысл |
|---|---|---|---|
| 0:00–0:12 | титул | проблема: смог зимой, учитель решает накануне вечером | проблема и пользователь |
| 0:12–0:41 | вкладка «Tomorrow (live)» | вход: свежие сводки аэропорта, без датчика → выход: около 57 µg/m³, «PE indoors», причины; это настоящее завтра, 16 ноября 2026 | настоящий вход → выход |
| 0:41–1:08 | вкладка «Replay», 16.12.2024 | прогноз 63, измерено на следующий день 67; «завтра как сегодня» сказало бы 23 | прогноз рядом с фактом |
| 1:08–1:22 | пример 27.10.2025 | прогноз 28, предупреждения нет; измерено 69 — пропущенный смоговый день | честный провал |
| 1:22–1:45 | два графика | данные, модель, 398 тестовых дней; MAE 15.3 / 12.3 / 13.2; ложных тревог меньше, пропусков больше | подход и сравнение с baseline |
| 1:45–1:54 | финальный кадр | ограничения и следующие шаги | ограничение |

**Что сделать тебе (5–10 минут):**
1. Скачай файл `docs/demo_video.mp4` (он же приложен в чате).
2. Загрузи на YouTube как **Unlisted** («Доступ по ссылке») или в Google Drive с доступом **«Anyone with the link can view»**.
3. Открой ссылку в режиме инкогнито: должна открываться без входа.
4. Вставь ссылку в поле Demo Video Link.

Хочешь свой голос поверх записи — можно, но не обязательно: правила просят только запись экрана до 2 минут. Подача без видео тоже считается полной.

**Запасной путь, если захочешь записать сам:** открой [ноутбук в Colab](https://colab.research.google.com/github/yk59m2cmhw-hash/c/blob/claude/sleepy-mendel-te40eu/notebooks/SmogTomorrow.ipynb) → Runtime → Run all → последняя ячейка даст ссылку `https://….gradio.live` → запиши экран по таблице выше.

## 3. Чек-лист перед отправкой
- [ ] Открыл в режиме инкогнито: Code Link, Write-up Link, видео — всё открывается без входа.
- [ ] Прошёл `docs/EXPLAIN_RU.md` (разделы 3–8 и 12) и могу своими словами рассказать путь данных, baseline и зачем нужна модель без датчика.
- [ ] В README строка **Team** — как ты хочешь (сейчас «Bakdaulet (solo)»).
- [ ] Имя, школа и email в форме написаны так, как должны быть в сертификате.
- [ ] Отправил форму и увидел подтверждение Airtable. Запиши время отправки.
- [ ] Если подавал раньше со старой ссылкой — подай ещё раз с новыми ссылками из таблицы выше: засчитывается последняя подача.

Если что-то сломалось при отправке: сразу написать на contact@veritasai.com со ссылками на код и write-up — так сказано в правилах.
