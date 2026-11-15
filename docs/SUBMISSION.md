# Подача: ответы формы, сценарий видео, чек-лист

Форма: https://airtable.com/appypCyHN77hElIcS/shrXA5VBFdugmoXl6 · дедлайн **16 ноября 09:59 Алматы**. Можно подавать повторно, засчитывается последняя подача.

## 1. Ответы для формы

| Поле | Что вписать | По-русски |
|---|---|---|
| Project Title | `Smog Tomorrow: should tomorrow's PE lesson be outdoors?` | «Смог завтра: проводить ли завтра физкультуру на улице?» |
| Your Full Name / School / Email | впиши сам, как должно быть в сертификате | — |
| Building As | Solo (вариант для одного участника) | один |
| Code Link | `https://github.com/yk59m2cmhw-hash/c` | репозиторий |
| Write-up Link | `https://github.com/yk59m2cmhw-hash/c#readme` | README и есть write-up |
| Demo Video Link | ссылка на твоё видео (YouTube unlisted или Google Drive «anyone with the link») | необязательно, но рекомендуют |
| Track | Climate | — |
| One-Sentence Pitch | `Smog Tomorrow helps a PE teacher in Almaty decide the evening before whether tomorrow's lesson can be outdoors, by forecasting tomorrow's daytime PM2.5 from today's air and airport weather measurements.` | помогает учителю физкультуры в Алматы накануне вечером решить про урок на улице, прогнозируя завтрашний дневной PM2.5 |
| New to AI? | ответь честно про себя | — |
| Rules Confirmation | отметь, только если согласен с каждым пунктом | см. ниже |
| Anything Else We Should Know | текст ниже | — |

**Если в форме появятся поля «Starting point» и «What we added»** (они есть в официальном примере):
- Starting point: `4.3.2 Next-day air quality forecast`
- What we added: `Our own city and user (Almaty schools; a school-hours target forecast at 18:00). A comparison with the free CAMS global model, which reads 13.6 µg/m³ too low here. An analysis of the 69 days when air quality changed sides of the 35 µg/m³ level. A warning rule with a stated cost (a missed smog day counts 3x a false alarm), with missed days and false alarms reported separately. The split and settings were committed to git before the test period was scored.`
- Datasets, models and AI tools used: `OpenAQ public archive (location 8876, provider AirNow); Iowa Environmental Mesonet METAR archive (station UAAA); CAMS global forecasts via Open-Meteo Air Quality API; scikit-learn, pandas, NumPy, matplotlib, Gradio; Claude Code (Anthropic) AI coding agent, which did most of the engineering under my direction.`

**Anything Else We Should Know** (вписать как есть):
`An AI coding agent (Claude Code) did most of the engineering; this is stated in the write-up. The evaluation protocol was committed to git before the test period was scored (commit 7f98623). The model misses more smog days than the persistence baseline (16 against 11) while raising fewer false alarms; we report both.`

**Про галочку Rules Confirmation.** Пункт «we can explain every part of our project» — про тебя лично. Сначала пройди `docs/EXPLAIN_RU.md`, разделы 3–8. Пункт «all the work was done between Nov 14 and Nov 15» выполнен: первый коммит сделан 15 ноября.

## 2. Сценарий видео (до 2 минут)
Запись экрана с голосом, монтаж не нужен. Говори медленно; читать с листа можно.

| Время | Что на экране | Что сказать (English) | Смысл |
|---|---|---|---|
| 0:00–0:15 | страница демо | "In winter, smoke gets trapped over Almaty. A PE teacher must decide the evening before: is tomorrow's lesson outdoors or indoors? Smog Tomorrow gives a forecast for that decision." | проблема и пользователь |
| 0:15–0:45 | ввести `2024-12-16`, нажать **Forecast tomorrow** | "This is the evening of December 16, 2024. Today was clean, 23 micrograms. The model forecasts 63 for tomorrow and gives a smog warning. The next day the monitor measured 67. The simple rule, tomorrow equals today, would have said 23." | вход → выход рядом с фактом |
| 0:45–1:10 | пример `2025-10-27` | "Here is a day the model got wrong. It forecast 28, no warning, but the next day was 69. The model cannot see tomorrow's weather, so it misses sudden changes." | честный провал |
| 1:10–1:40 | README: таблица Results | "The data: five years of hourly measurements from one monitor and weather reports from Almaty airport. The model is gradient boosted trees. On 398 test days its average error is 12.3, against 15.3 for the baseline and 16.6 for a global model. It gives fewer false alarms, 52 against 76, but it misses more smog days, 16 against 11." | данные, модель, baseline |
| 1:40–2:00 | README: What we'd do next | "Next, I would add tomorrow's weather forecast and weather balloon data, and test the warning with real PE teachers. Thank you." | ограничение и следующий шаг |

**Как получить страницу демо для записи:**
1. Открой [ноутбук в Colab](https://colab.research.google.com/github/yk59m2cmhw-hash/c/blob/claude/relaxed-dirac-2g7xn0/notebooks/SmogTomorrow.ipynb), войди в Google-аккаунт.
2. Меню **Runtime → Run all**, подожди около минуты. Если Colab спросит про запуск чужого ноутбука — «Run anyway».
3. Последняя ячейка напечатает ссылку вида `https://….gradio.live` — открой её. Это и есть демо.
4. Запиши экран (Windows: Win+Alt+R или Win+Shift+R; Mac: Cmd+Shift+5; телефон не подойдёт).
5. Загрузи на YouTube как **Unlisted** или в Google Drive с доступом «Anyone with the link». Открой ссылку в режиме инкогнито — должна работать без входа.

Если Colab не работает: видео необязательно. Подача без видео полная.

## 3. Чек-лист перед отправкой
- [ ] Открыл в режиме инкогнито: репозиторий, README, ноутбук, видео — всё открывается без входа.
- [ ] Прошёл `docs/EXPLAIN_RU.md` и могу своими словами рассказать путь данных и baseline.
- [ ] В README строка **Team** — как ты хочешь (сейчас «Bakdaulet (solo)»).
- [ ] Имя, школа и email в форме написаны так, как должны быть в сертификате.
- [ ] Отправил форму и увидел подтверждение Airtable.
- [ ] Первая подача сделана не позже 23:00 Алматы; после правок можно подать ещё раз.

Если что-то сломалось при отправке: написать на contact@veritasai.com со ссылками на код и write-up — так сказано в правилах.
