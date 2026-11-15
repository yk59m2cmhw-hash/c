# Deep-tech, AI-for-science, климат/энергия, робототехника, космические вычисления: как формируются идеи

Срез на 15.11.2026. Назначение: банк ПАТТЕРНОВ формирования идей для соло-участника Veritas AI International High School Hackathon 2026 (треки Health, Finance, Climate, Languages; ИИ/ML делает основную работу; ~20 часов; только CPU; без гарантированного платного API; публичные или синтетические данные). Продукты не копировать — брать способ, которым идея была найдена.

**Пометки достоверности**
- [П] — первичный источник (сайт компании, пресс-релиз, SEC, GitHub, научный журнал) или крупное издание (Bloomberg, Reuters, TechCrunch, CNBC, NPR, DCD и т. п.).
- [В] — только вторичные источники/агрегаторы; цифру считать ориентировочной.
- «не подтверждено» — надёжного подтверждения найти не удалось.
- Оценка компании — цена частного раунда, а не доказательство, что технология работает.
- Строки «Почему сейчас / узкое место» — аналитический вывод автора отчёта, а не цитата источника.

**Два спорных названия из запроса**
- «wavr technologies»: компания с таким буквальным названием СУЩЕСТВУЕТ — WAVR Technologies (Лас-Вегас, спин-аут UNLV, получение воды из воздуха). Это не Wayve. Описаны обе: WAVR — в разделе 2, Wayve — в разделе 4.
- «cero 3d»: идентифицировать НЕ удалось. Поиски «Cero 3D», «Cero3D», «Cero AI» не дали ни компании, ни продукта в области ИИ-3D. Созвучные названия не подставлялись. Нужна ссылка, страна или контекст от пользователя.

---

## Компании

### 1. ИИ для науки и биологии

**Isomorphic Labs** (Alphabet, спин-аут DeepMind, Лондон)
- Что: дизайн лекарств на компьютере → собственный пайплайн и сделки с фармой (Lilly, Novartis, J&J — [В]).
- ИИ: ядро. Предсказание структуры комплексов + генеративный дизайн молекул (движок IsoDDE, 10.02.2026, код и веса закрыты [В]).
- Почему сейчас / узкое место: модели класса AlphaFold 3 и огромный капитал / клиника: ни одного препарата в испытаниях на людях, цель «первые испытания» сдвинута с конца 2025 на конец 2026.
- Сигнал: Series B $2,1 млрд, 12.05.2026, лид Thrive Capital [П] https://www.isomorphiclabs.com/articles/isomorphic-labs-announces-series-b-investment-round ; Bloomberg 08.10.2026 — переговоры при оценке ≥$40 млрд, 05.11.2026 — ~$5 млрд при ~$50 млрд, сделка не закрыта [П] https://www.bloomberg.com/news/articles/2026-10-08/alphabet-s-isomorphic-labs-in-funding-talks-for-at-least-40-billion-value , https://thenextweb.com/news/isomorphic-labs-5bn-funding-talks-50bn-valuation

**Cortical Labs** (Мельбурн)
- Что: «биологический компьютер» CL1 — живые человеческие нейроны на электродном чипе; продаётся как прибор (~$35 тыс.) и как облако Cortical Cloud.
- ИИ: не классический ML. Обучается сама нейронная культура в замкнутом контуре «стимуляция ↔ считывание»; софт — интерфейс.
- Почему сейчас / узкое место: зрелость нейронов из стволовых клеток и плотных электродных матриц, спрос на энергоэффективный ИИ / воспроизводимость, срок жизни культур, нет доказанного практического преимущества.
- Сигнал: инвестиция Gobi Partners 04.03.2026, сумма не раскрыта [П] https://www.gobi.vc/news/gobi-partners-backs-cortical-labs-to-advance-thenext-frontier-of-biological-intelligence ; всего привлечено ~$11–12 млн [В]; 120 CL1 в мельбурнском прототипе (заявление компании) https://itbrief.com.au/story/cortical-labs-cl1-commercial-milestone-after-aud-245k-grant

**Lila Sciences** (Flagship Pioneering, Кембридж, США)
- Что: «AI Science Factories» — модели + автоматизированные лаборатории для биологии, химии, материалов.
- ИИ: ядро. Замкнутый цикл «гипотеза → робот-эксперимент → данные → дообучение».
- Почему сейчас / узкое место: рассуждающие LLM + удешевление лабораторной автоматики / капиталоёмкость; не доказано, что цикл даёт открытия быстрее людей.
- Сигнал: seed $200 млн (03.2025), Series A $235 млн + $115 млн (09–10.2025), оценка >$1,3 млрд [В]; Bloomberg 03.06.2026 — переговоры о ~$2 млрд при ~$8,5 млрд до денег; закрытие не подтверждено https://uk.investing.com/news/stock-market-news/lila-sciences-in-talks-for-2b-funding-at-85b-valuation--bloomberg-93CH-4712331

**Periodic Labs** (Сан-Франциско; основатели из OpenAI и DeepMind)
- Что: ИИ-«учёные» + автономные лаборатории для новых материалов.
- ИИ: ядро. Агент планирует синтез и измерения, учится на собственных экспериментах.
- Почему сейчас / узкое место: предсказаний материалов много, экспериментальной проверки мало / синтез медленный, публичных открытий пока нет.
- Сигнал: seed $300 млн (09.2025); Bloomberg 25.03.2026 — переговоры при ~$7 млрд [П] https://www.bloomberg.com/news/articles/2026-03-25/ai-science-startup-periodic-labs-is-in-deal-talks-at-about-7-billion-valuation ; Forbes 07.05.2026 — $500 млн при $7,5 млрд [П] https://www.forbes.com/sites/iainmartin/2026/05/07/former-openai-researcher-to-raise-500-million-for-ai-science-startup/ ; закрытие не подтверждено.

**EvolutionaryScale**
- Что: белковые языковые модели ESM3 → генерация новых белков (сервис Forge).
- ИИ: ядро. Фундаментальная модель для белков (последовательность + структура + функция).
- Почему сейчас / узкое место: миллиарды последовательностей в открытых базах + GPU / мокрая валидация и бизнес-модель.
- Сигнал: seed >$142 млн (06.2024) [П] https://blogs.nvidia.com/blog/evolutionaryscale-esm3-generative-ai-nim-bionemo-h100/ ; 06.11.2025 объявлено о поглощении организацией Biohub (Чан и Цукерберг), сооснователь Alex Rives стал head of science, условия не раскрыты [П] https://www.axios.com/2025/11/06/zuckerberg-chan-biohub-ai-disease ; новых раундов в 2026 не найдено.

**Chai Discovery**
- Что: модели Chai-1/2/3 → антитела и другие молекулы «с нуля» для фармы (Lilly, Pfizer, Novartis [В]).
- ИИ: ядро. Генеративный дизайн + предсказание структуры; у Chai-2 двузначная доля экспериментальных попаданий (заявление компании; в источниках 16–20%).
- Почему сейчас / узкое место: диффузионные модели + проверка десятков кандидатов вместо миллионов / путь от «связывается» до клиники, конкуренция.
- Сигнал: Series C $400 млн при оценке $3,8 млрд, 14.07.2026, лид Index Ventures [В — несколько вторичных источников, первичный релиз не найден] https://pulse2.com/chai-discovery-raises-400-million-series-c-to-advance-ai-driven-molecular-design/ , https://www.citybiz.co/article/874292/chai-discovery-raises-400-million-series-c-to-scale-ai-drug-discovery-platform/

**Recursion** (NASDAQ: RXRX)
- Что: массовая клеточная микроскопия + ИИ-химия → клинический пайплайн и партнёрства с фармой.
- ИИ: предсказание (карты фенотипов), дизайн (Boltz-2; в 2026 открыта модель аффинности Nesso-1), ускорение набора пациентов (заявлено 30–60%).
- Почему сейчас / узкое место: собственный гигантский датасет + открытые модели структуры / клинические результаты, выручка ниже ожиданий.
- Сигнал: отчёт за Q2 2026 (05.08.2026): 5 программ в клинике, ~$557 млн денежных средств, запас до начала 2028 [П] https://www.sec.gov/Archives/edgar/data/0001601830/000160183026000097/exhibit991-q0226.htm ; Q1: выручка $6,47 млн против ожиданий $16,28 млн [В] https://www.investing.com/news/company-news/recursion-q1-2026-slides-ai-pipeline-advances-amid-revenue-challenges-93CH-4681698

**Arc Institute — «виртуальная клетка»** (некоммерческий институт)
- Что: модель State предсказывает ответ клетки на генетическое/химическое возмущение; институт проводит Virtual Cell Challenge.
- ИИ: ядро. Предсказание отклика по данным single-cell.
- Почему сейчас / узкое место: датасеты на 100+ млн клеток (в т. ч. открытый Tahoe-100M компании Tahoe Therapeutics) / обобщение на невиданные клеточные контексты; организаторы сами называют State «стартовым бенчмарком».
- Сигнал: Challenge 2026: старт 20.08.2026, zero-shot по 6 клеточным линиям без обучающего набора, призы $175 тыс., приём закрыт; победители — не подтверждено [П] https://arcinstitute.org/news/virtual-cell-challenge-2026 , https://virtualcellchallenge.org/

**Google DeepMind — научные модели**
- AlphaFold 3: совместное предсказание структуры белков, ДНК, РНК, лигандов; код открыт, веса только для некоммерческого использования [В] https://www.talindrew.com/guides/alphafold-3-commercial-use ; «AlphaFold 4» — не подтверждено.
- AlphaGenome: до 1 млн «букв» ДНК → регуляторные эффекты вариантов; статья в Nature (т. 649, 2026) [П] https://www.nature.com/articles/s41586-025-10014-0 ; API бесплатен для некоммерческого использования [П] https://github.com/google-deepmind/alphagenome ; AlphaGenome 2 (11.11.2026) — [В].
- AlphaEvolve: LLM + эволюционный поиск + автоматический оценщик → новые алгоритмы. Репозиторий открыт (Apache 2.0, нужен ключ Gemini API, «не официальный продукт Google») [П] https://github.com/google-deepmind/alphaevolve ; ретроспектива 05.2026: возвращено 0,7% вычислительных ресурсов Google [В].
- GNoME: 2,2 млн предсказанных кристаллов (2023). C&EN, 10.2026: >15% записей — почти дубликаты друг друга, ~25% дублируют Materials Project [П — заголовок и выводы, полный текст получить не удалось] https://cen.acs.org/research-integrity/Google-DeepMind-structures-near-duplicates-questionable/104/web/2026/10 ; в 01.2026 Nature опубликовал исправление к статье A-Lab о «новых» материалах [В].
- WeatherNext 2 / GenCast: ансамблевый прогноз погоды. Код и веса на GitHub (код Apache 2.0, остальное CC BY 4.0); мини-версия идёт в бесплатном Colab, полные требуют H100/TPU [П] https://github.com/google-deepmind/weathernext ; дата открытия 06.08.2026 и статья в Nature — [В].
- AlphaEarth Foundations: годовые спутниковые эмбеддинги (10 м, 2017–2024), CC BY 4.0, доступны в Earth Engine [П] https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL

### 2. Климат, энергия, вода

**Quaise Energy** (спин-аут MIT)
- Что: бурение миллиметровыми волнами (гиротрон) до сверхгорячих пород → геотермия почти в любой точке.
- ИИ: не ядро.
- Почему сейчас / узкое место: гиротроны отработаны в термояде, спрос на круглосуточную чистую мощность / физика и инженерия глубокого бурения, капитал.
- Сигнал: финальное закрытие Series B — $180 млн (27.08.2026, включая $35 млн от Nabors), всего $280 млн; Project Obsidian (Орегон), первые электроны в сеть к 2030 [П] https://www.quaise.com/news/quaise-energy-closes-180-million-series-b-with-35-million-investment-by-nabors-industries

**Form Energy**
- Что: железо-воздушная батарея на 100 часов (обратимое «ржавление») для сетей.
- ИИ: не ядро.
- Почему сейчас / узкое место: ВИЭ и дата-центрам нужна многосуточная мощность, железо дёшево / масштаб производства, стоимость (не раскрывается), первые системы малы.
- Сигнал: Google + Xcel Energy — проект 300 МВт / 30 ГВт·ч (24.02.2026) [П] https://www.utilitydive.com/news/worlds-largest-grid-battery-part-of-google-xcel-energy-agreement/813793/ ; Series G $750 млн, 12.08.2026, лид T. Rowe Price, портфель заказов >80 ГВт·ч [П] https://www.energy-storage.news/iron-air-us-ldes-startup-form-energy-secures-us750-million-series-g-financing/ ; оценка компанией не раскрыта.

**Climeworks** (Швейцария)
- Что: прямой захват CO2 из воздуха + закачка в базальт (Исландия) → продажа «удалённых тонн».
- ИИ: не ядро.
- Почему сейчас / узкое место: корпоративный спрос на удаление углерода / физика и энергозатраты: фактический результат намного ниже паспортного.
- Сигнал: установка Mammoth дала 675 т чистого удаления за первое полугодие 2026 против 119 т годом ранее при проектных 36 000 т/год; операционная стоимость тонны упала более чем на 50% (Bloomberg, 10.09.2026) [П] https://www.bloomberg.com/news/articles/2026-09-10/carbon-removal-pioneer-climeworks-increases-co2-capture-sixfold ; раунд $162 млн (07.2025), всего >$1 млрд; сокращение ~22% штата (05.2025) [В] https://www.swissinfo.ch/eng/climate-solutions/why-swiss-carbon-removal-start-up-climeworks-faces-serious-headwinds/89386618

**Commonwealth Fusion Systems (CFS)**
- Что: высокотемпературные сверхпроводящие магниты → компактный токамак SPARC → электростанция ARC.
- ИИ: вспомогательный (симуляции и управление плазмой; ИИ-«цифровой двойник» SPARC в программе DOE — [В]).
- Почему сейчас / узкое место: новые магниты уменьшают размер реактора, спрос на энергию для ИИ / физика (нет плазмы), сроки сдвигаются: 2025 → 2026 → 2027.
- Сигнал: +$1 млрд 30.07.2026 (пенсионные и суверенные фонды), всего $4 млрд; SPARC собран примерно на 80%, научная безубыточность ожидается в 2027 [П] https://techcrunch.com/2026/07/30/fusion-power-darling-commonwealth-fusion-systems-raises-another-1b/

**Helion**
- Что: импульсный термояд с прямым съёмом электричества; прототип Polaris, станция Orion для Microsoft.
- ИИ: не ядро.
- Почему сейчас / узкое место: покупатель с дедлайном (Microsoft, 2028) / физика; формулировки смягчаются.
- Сигнал: Series G $465 млн при оценке $15,5 млрд после денег (04.06.2026), позже раунд вырос до $500 млн [П] https://www.businesswire.com/news/home/20260604740624/en/Helion-Raises-$465-Million-Series-G-Funding-Round-to-Meet-Surging-Global-Demand-for-Power , https://www.geekwire.com/2026/helion-funding-round-grows-to-500m-amid-uncertainty-over-fusion-startups-microsoft-timeline/ ; 02.2026 — D-T синтез и 150 млн °C в Polaris (заявление компании); Axios 08.09.2026: с сайта убран прогноз электричества к 2028, «net electricity» заменено на «демонстрацию электричества» [П] https://www.axios.com/pro/climate-deals/2026/09/08/helion-energy-fusion-net-electricity-date-year

**Fervo Energy** (NASDAQ: FRVO)
- Что: усовершенствованная геотермия: горизонтальное бурение и гидроразрыв из сланцевой отрасли → круглосуточная электроэнергия (Cape Station, Юта).
- ИИ: вспомогательный (аналитика бурения и пласта), не ядро.
- Почему сейчас / узкое место: готовые сланцевые технологии + спрос дата-центров / капитал и исполнение проектов.
- Сигнал: IPO 13.05.2026, $27 за акцию, привлечено ~$1,89 млрд, +33% в первый день, оценка >$10 млрд [П] https://techcrunch.com/2026/05/13/geothermal-startup-fervo-energy-pops-33-in-ipo-debut-fueled-by-ai-data-center-demand/ , https://fortune.com/2026/05/14/fervo-clean-energy-biggest-ipo-10b-valuation-powered-earths-heat-ai-hunger/ ; выдача первой мощности Cape Station — не подтверждено.

**Zanskar**
- Что: ИИ ищет «слепые» геотермальные системы (без признаков на поверхности), затем компания бурит и строит станции.
- ИИ: ядро. Вероятностный прогноз «где бурить» по геофизике, геохимии, дистанционному зондированию.
- Почему сейчас / узкое место: открытые геоданные + дешёвый ML + спрос на базовую мощность / подтверждение стоит скважины, известных систем (меток) мало.
- Сигнал: Series C $115 млн (21.01.2026), всего $180 млн; открытие Big Blind (Невада) [П] https://www.globenewswire.com/news-release/2026/01/21/3222733/0/en/zanskar-raises-115m-series-c-following-record-setting-year-of-geothermal-discoveries.html ; 20-летний договор на 100 МВт с NV Energy для дата-центров Amazon (05.2026, требуется одобрение регулятора, поставка с 2030) [П] https://www.thinkgeoenergy.com/zanskar-to-supply-100-mw-of-geothermal-power-to-amazon-data-centres/

**KoBold Metals**
- Что: ИИ-разведка критических металлов (медь, литий, никель, кобальт) → доли в месторождениях (Mingomba, Замбия).
- ИИ: ядро. Слияние разнородных геоданных и прогноз мест бурения.
- Почему сейчас / узкое место: дефицит металлов для электрификации, оцифровка старых геологических архивов / десятилетний цикл «находка → рудник», капитал, политические риски.
- Сигнал: последняя подтверждённая оценка ~$2,96 млрд (Series C $537 млн, 01.2025); весной 2026 начато строительство Mingomba (>$2,3 млрд, до 300 тыс. т меди в год) [П] https://miningindaba.com/articles/kobold-metals-breaks-ground-on-23-billion-min , https://www.berkeleyside.org/2026/10/05/kobold-metals-berkeley

**Crusoe**
- Что: ИИ-дата-центры «от энергии»: строит там, где электричество дешёвое или избыточное (начинали с попутного газа); кампус в Абилине для OpenAI.
- ИИ: это нагрузка клиента, а не метод компании.
- Почему сейчас / узкое место: главный дефицит ИИ — электричество / капитал, зависимость от нескольких крупных клиентов.
- Сигнал: Series F $3,9 млрд при оценке $30,9 млрд (18.09.2026) [П] https://www.datacenterdynamics.com/en/news/crusoe-raises-39bn-for-ai-data-center-build-out/

**Base Power** (Остин)
- Что: дешёвая установка домашних батарей в Техасе + собственная розничная продажа электроэнергии; парк батарей работает как виртуальная электростанция.
- ИИ: прогноз и оптимизация диспетчеризации парка; ядро — вертикальная интеграция «железо + ритейл».
- Почему сейчас / узкое место: дешёвые батареи, перегруженная сеть / капиталоёмкость, выход за пределы Техаса.
- Сигнал: Series D $1 млрд при оценке $13 млрд (03.08.2026); десятью месяцами ранее — $4 млрд [П] https://www.esgtoday.com/home-battery-startup-base-power-raises-1-billion-at-13-billion-valuation/

**Redwood Materials**
- Что: переработка батарей → катодные материалы; Redwood Energy — «вторая жизнь» батарей электромобилей как накопители для дата-центров (микросеть 12 МВт / 63 МВт·ч для Crusoe).
- ИИ: не ядро.
- Почему сейчас / узкое место: поток отслуживших батарей + дефицит мощности у дата-центров / экономика переработки, сокращение ~10% штата (04.2026) [В].
- Сигнал: Series E $425 млн (01.2026; Google, NVentures), оценка >$6 млрд по словам источника [П] https://heatmap.news/climate-tech/redwood-425-million-series-e

**Heirloom**
- Что: прямой захват CO2 циклом известняка; заводы в Луизиане (17 тыс. т/год и 100 тыс. т/год в рамках Project Cypress).
- ИИ: не ядро.
- Почему сейчас / узкое место: налоговые льготы и хабы DOE / зависимость от госфинансирования, сроки.
- Сигнал: объявленные инвестиции $475 млн в Луизиане (2024) [П] https://www.opportunitylouisiana.gov/news/heirloom-carbon-technologies-announces-475-million-investment-to-establish-north-americas-second-direct-air-capture-facility-in-louisiana ; на странице компании — «запуск в 2026» https://www.heirloomcarbon.com/projects ; фактический запуск — не подтверждено.

**Pano AI**
- Что: панорамные камеры на вышках + компьютерное зрение + человек-верификатор → ранние оповещения о дыме для пожарных и энергокомпаний.
- ИИ: ядро. Обнаружение дыма по видео.
- Почему сейчас / узкое место: ответственность энергокомпаний за пожары, дешёвые камеры и связь / экономика покрытия, ложные тревоги, госзакупки.
- Сигнал: Series B $44 млн (06.2025, лид Giant Ventures), всего $89 млн, мониторинг ~30 млн акров (данные компании) [П] https://www.latitudemedia.com/industry-news/pano-ai-raises-44m-series-b-led-by-giant-ventures-to-scale-early-detection-infrastructure/ ; 250+ ведомств и 15 крупных энергокомпаний [В]; нового раунда в 2026 не найдено.

**Tomorrow.io**
- Что: собственные погодные спутники + ИИ-прогноз → погодная аналитика для бизнеса и государств.
- ИИ: ядро. Прогноз и ассимиляция собственных наблюдений.
- Почему сейчас / узкое место: дешёвые малые спутники + ИИ-модели погоды / капитал на группировку, конкуренция с бесплатными госпрогнозами.
- Сигнал: $175 млн на группировку DeepSky (03.02.2026); 13 спутников на орбите [П] https://spacenews.com/tomorrow-io-banks-175-million-for-deepsky-weather-constellation/ , https://www.satellitetoday.com/finance/2026/02/03/tomorrow-io-raises-175m-to-build-out-deepsky-weather-constellation/

**Brightband**
- Что: ИИ-прогноз погоды напрямую из наблюдений + открытые инструменты (архив наблюдений NNJA-AI, набор тестов Extreme Weather Bench).
- ИИ: ядро. Прогноз и ассимиляция данных; бенчмарк как общественный продукт.
- Почему сейчас / узкое место: открытые архивы NOAA/NASA / монетизация при бесплатных конкурентах.
- Сигнал: Series A $10 млн (09.2024) [П] https://techcrunch.com/2024/09/19/brightband-sees-a-bright-and-open-source-future-for-ai-powered-weather-forecasting/ ; Extreme Weather Bench (27.01.2026) [П] https://www.brightband.com/company/news/ ; нового раунда в 2026 не найдено.

**Watershed**
- Что: корпоративный учёт выбросов и отчётность (программное обеспечение).
- ИИ: вспомогательный (извлечение и сопоставление данных); ядро — доверенный учёт.
- Почему сейчас / узкое место: требования раскрытия, вопрос о выбросах ИИ / зависимость от регулирования.
- Сигнал: Series C $100 млн при оценке $1,8 млрд (02.2024) [П] https://trellis.net/article/california-startup-watershed-raises-100-million-emissions-tracking-software/ ; лидер рейтинга Verdantix (11.03.2026) [П] https://www.globenewswire.com/news-release/2026/03/11/3253995/0/en/Independent-Research-Firm-Names-Watershed-a-Leader-in-Carbon-Management-Software.html ; нового раунда в 2026 не найдено.

**WAVR Technologies** (Лас-Вегас, спин-аут UNLV, основана в 2024) — буквальное «wavr technologies»
- Что: получение воды из воздуха в сухом климате (по сообщениям прессы — гель по образцу кожи лягушки, работает при влажности от 10%, заявление компании); целевой спрос — дата-центры.
- ИИ: не ядро.
- Почему сейчас / узкое место: водный стресс на юго-западе США и рост водопотребления дата-центров / масштаб и стоимость, ранняя стадия.
- Сигнал: привлекает $4 млн, из них получено $1,25 млн; выручка по контрактам $975 тыс. (08.2026) [П] https://www.reviewjournal.com/business/vegas-business/innovation/las-vegas-startup-turns-desert-air-into-water-3865505/ , https://www.wavrtechnologies.com/about-us , https://www.benzinga.com/news/topics/25/09/47906771/startup-backed-by-4m-funding-says-it-can-pull-10k-gallons-of-water-a-day-from-desert-air-using-frog-i

**ИИ-модели погоды (класс продукта)**
- GraphCast (DeepMind, 2023): графовая сеть, 0,25°, прогноз на 10 суток менее чем за минуту на одном TPU [П] https://thenextweb.com/news/deepmind-ai-graphcast-weather-forecasting ; веса — CC BY-NC-SA 4.0 [В, по зеркалу] https://huggingface.co/shermansiu/dm_graphcast
- Aurora (Microsoft): фундаментальная модель атмосферы, дообучается под качество воздуха, волны, циклоны. Aurora 1.5 (07.2026): +22 переменные, почасовой шаг, ансамбли, открытые код и веса [П] https://www.microsoft.com/en-us/research/blog/aurora-1-5-extending-open-foundation-models-for-weather-and-earth-system-applications/
- NeuralGCM (Google Research): гибрид «дифференцируемое физическое ядро + ML». 12.01.2026 — версия для осадков, обученная на спутниковых наблюдениях NASA 2001–2018, открытый код [П] https://research.google/blog/neuralgcm-harnesses-ai-to-better-simulate-long-range-global-precipitation/
- ECMWF AIFS: операционная ИИ-система европейского центра. Версия 2 с 12.05.2026: ансамбль из 51 члена, 15 суток, 4 раза в день, первые операционные ИИ-прогнозы волн; открытые данные, веса на Hugging Face [П] https://forum.ecmwf.int/t/ifs-cycle-50r1-and-aifs-v2-implementation-planned-for-12-may-2026/14781 , https://huggingface.co/ecmwf/aifs-ens-2.0

### 3. Вычисления и космос

**Starcloud**
- Что: дата-центры на орбите (солнечная энергия без ночи, излучательное охлаждение).
- ИИ: нагрузка, а не метод.
- Почему сейчас / узкое место: дешёвый запуск + дефицит энергии на Земле / охлаждение, радиация, обслуживание, экономика запусков.
- Сигнал: Starcloud-1 с Nvidia H100 запущен 02.11.2025; обучение nanoGPT и запуск Gemma на орбите (заявление компании) https://starcloud.com/starcloud-1 ; $170 млн при оценке $1,1 млрд (03.2026) https://thenextweb.com/news/starcloud-170m-series ; $250 млн при оценке $2,3 млрд (21.08.2026; Nvidia, Cisco) [П] https://www.bnnbloomberg.ca/business/company-news/2026/08/21/orbital-data-center-startup-starcloud-valued-at-us23-billion-in-latest-funding/ ; срок Starcloud-2 в источниках расходится (10.2026 или 2027).

**Google Project Suncatcher**
- Что: исследовательский проект — кластеры спутников с чипами TPU и лазерной связью.
- ИИ: нагрузка; на спутнике работает открытая модель Gemma.
- Почему сейчас / узкое место: проверка радиационной стойкости TPU и тепловых режимов / энергия и тепло: чипы работают короткими сеансами.
- Сигнал: прототип (совместно с Planet, 4 TPU) запущен 01.10.2026 на SpaceX Transporter-18; обычная орбита с батареями [П] https://www.opb.org/article/2026/10/01/google-launches-project-suncatcher-a-step-towards-ai-data-centers-in-space/ ; первый ответ модели с орбиты 30.10.2026 и план ещё двух спутников для проверки лазерных линий — [В] https://www.technology.org/2026/11/03/google-suncatcher-satellite-gemma-4-orbit-tpu/

**SpaceX / xAI**
- Что: заявка на группировку орбитальных дата-центров; слияние SpaceX и xAI.
- ИИ: нагрузка.
- Почему сейчас / узкое место: собственные ракеты и Starlink / в проспекте IPO компания сама предупреждает, что технология не доказана и может не стать коммерчески жизнеспособной.
- Сигнал: заявка в FCC на до 1 млн спутников (30–31.01.2026) [П] https://www.datacenterdynamics.com/en/news/spacex-files-for-million-satellite-orbital-ai-data-center-megaconstellation/ ; слияние с xAI (02.02.2026) [П] https://www.satellitetoday.com/connectivity/2026/02/02/spacex-acquires-xai-to-pursue-orbital-data-center-constellation/ ; IPO в июне 2026, первые спутники AI1 — конец 2027 или 2028 [П] https://www.datacenterdynamics.com/en/news/spacex-ipo-musks-firm-set-to-launch-first-orbital-data-center-ai1-satellites-in-2027-will-put-compute-on-starlink-craft/ , https://thenextweb.com/news/spacex-orbital-data-centres-ipo-risk-disclosure ; сумма IPO в источниках расходится ($75–85 млрд) [В].

**Blue Origin — Project Sunrise**
- Что: заявка на до 51 600 спутников-дата-центров на солнечно-синхронных орбитах.
- ИИ: нагрузка.
- Почему сейчас / узкое место: гонка за орбитальные слоты / нет ни сроков, ни заявленной мощности.
- Сигнал: заявка в FCC 19.03.2026 [П] https://www.datacenterdynamics.com/en/news/bezos-backed-blue-origin-files-for-approval-to-put-data-centers-in-space/

**Aetherflux** (кратко)
- Космическая солнечная энергия → орбитальные вычисления («Galactic Brain»); 03.2026 — переговоры о раунде при оценке ~$2 млрд, закрытие не подтверждено [П] https://www.datacenterdynamics.com/en/news/space-data-center-company-aetherflux-reportedly-raising-series-b-funding-at-2bn-valuation/

**Stargate (OpenAI, Oracle, SoftBank)**
- Что: строительство гигаваттных ИИ-дата-центров вместе с генерацией.
- ИИ: нагрузка.
- Почему сейчас / узкое место: спрос на обучение и инференс / электричество, стройка, финансирование.
- Сигнал: по оценке Epoch AI (17–23.04.2026) работает ~0,3 ГВт (Абилин) при >9 ГВт в планах на 7 площадках США к ~2029; расширение Абилина до 2,1 ГВт отменено [П] https://epoch.ai/publications/openai-stargate-where-the-us-sites-stand ; заявление OpenAI о «более 10 ГВт» — это законтрактованная, а не работающая мощность [В].

### 4. Робототехника, физический ИИ, нейроинтерфейсы

**Physical Intelligence**
- Что: фундаментальная модель «зрение–язык–действие» для любых роботов.
- ИИ: ядро. Управление.
- Почему сейчас / узкое место: трансформеры + телеоперационные данные / данных о действиях мало, выручки нет [В].
- Сигнал: $600 млн при оценке $5,6 млрд (11.2025); Bloomberg 27.10.2026 — переговоры о ≥$1 млрд при ~$20 млрд, не закрыто [П] https://www.bloomberg.com/news/articles/2026-10-27/robotics-lab-physical-intelligence-in-talks-for-a-20-billion-valuation

**Figure**
- Что: гуманоидные роботы для заводов, позже для дома.
- ИИ: ядро. Собственная модель управления.
- Почему сейчас / узкое место: дешёвые приводы + модели действий / надёжность, цена, домашнее применение не начато.
- Сигнал: Figure 03 работает на заводе BMW в Спартанбурге на подборе деталей (06.2026) [П] https://www.figure.ai/news/f-03-at-bmw ; последняя подтверждённая оценка $39 млрд (09.2025) [В] https://en.wikipedia.org/wiki/Figure_AI ; новый раунд (10.2026) — не подтверждено.

**1X Technologies**
- Что: домашний гуманоид NEO ($20 тыс. или $499 в месяц; предзаказы с 28.10.2025).
- ИИ: ядро. Управление; данные собираются в домах.
- Почему сейчас / узкое место: потребительский интерес / автономность; подтверждённых поставок клиентам на лето 2026 не найдено [В].
- Сигнал: сообщения о переговорах SoftBank о контрольной доле при оценке ~$6 млрд (08.2026) — не подтверждено [В] https://www.humanoidsdaily.com/companies/1x-technologies

**Skild AI**
- Что: единый «мозг» для роботов любой формы (Skild Brain), лицензируется производителям.
- ИИ: ядро. Управление; обучение в симуляции и на видео.
- Почему сейчас / узкое место: масштабная симуляция / перенос из симуляции в реальность.
- Сигнал: Series C $1,4 млрд при оценке >$14 млрд (14.01.2026, лид SoftBank) [П] https://www.businesswire.com/news/home/20260114335623/en/Skild-AI-Raises-$1.4B-Now-Valued-Over-$14B

**Wayve** (Лондон) — возможное прочтение «wavr»
- Что: «ИИ-водитель» — сквозная модель вождения, лицензируется автопроизводителям и сервисам такси.
- ИИ: ядро. Управление.
- Почему сейчас / узкое место: сквозные модели обучаются на видео без подробных карт / безопасность, регулирование.
- Сигнал: Series D $1,2 млрд (+до $300 млн от Uber) при оценке $8,6 млрд (24.02.2026) [П] https://www.cnbc.com/2026/02/24/wayve-fundraise-nvidia-microsoft.html ; запуск роботакси с Uber в Лондоне — не подтверждено.

**Waymo** (Alphabet)
- Что: коммерческое роботакси.
- ИИ: ядро. Восприятие, прогноз поведения, планирование; массовая симуляция.
- Почему сейчас / узкое место: более 15 лет данных и сенсоров / стоимость парка, регулирование, расширение по городам.
- Сигнал: раунд $16 млрд при оценке $126 млрд (02.2026) [В] https://www.revenuememo.com/p/waymo-funding ; ~500 тыс. платных поездок в неделю (03.2026), цель — 1 млн к концу 2026 [П] https://finance.yahoo.com/news/waymo-eyes-1-million-paid-152515066.html

**Neuralink**
- Что: имплант с 1024 электродами, устанавливаемый роботом → управление устройствами «мыслью»; программы по речи и зрению (Blindsight).
- ИИ: ядро декодирования сигналов мозга.
- Почему сейчас / узкое место: миниатюрная электроника и хирургический робот / регулирование, долговечность, сдвиг сроков Blindsight.
- Сигнал: Series E ~$650 млн (06.2025, оценка ~$9 млрд); 21 участник на 28.01.2026, более поздние цифры (26–28) не сведены — точное число не подтверждено [В] https://www.neurapod.com/neuralink-by-the-numbers

**Synchron**
- Что: нейроинтерфейс-стент, вводится через сосуды без вскрытия черепа; 16 электродов, простые команды.
- ИИ: декодирование; отдельное подразделение Cognitive AI обучает модели на данных мозга.
- Почему сейчас / узкое место: готовая техника сосудистой хирургии / мало каналов, нужно ключевое испытание и одобрение FDA.
- Сигнал: Series D $200 млн (11.2025), всего $345 млн [П] https://www.medtechdive.com/news/synchron-funding-bci-200m/804977/ ; Series E $275 млн (06.2026) — единственный источник, не подтверждено.

**Science Corporation**
- Что: PRIMA — беспроводной фотоэлектрический имплант под сетчатку + очки; возвращает центральное зрение при географической атрофии.
- ИИ: вспомогательный (обработка изображения), ядро — прибор.
- Почему сейчас / узкое место: куплены готовые активы Pixium Vision / возмещение стоимости, статус в США.
- Сигнал: Series C $230 млн (05.03.2026), всего $490 млн [П] https://businesswire.com/news/home/20260305896789/en/Science-Corporation-Closes-%24230-Million-Series-C-to-Accelerate-Commercialization-of-Its-PRIMA-BCI-Retinal-Implant-the-Worlds-Most-Advanced-Vision-Restoration-Technology ; знак CE 22.07.2026, продажи в ~30 странах Европы [П] https://newatlas.com/medical-tech/vision-restoring-retinal-implant-approval-europe/ ; подача на IPO — не подтверждено.

### 5. 3D и мировые модели

**World Labs** (Фэй-Фэй Ли)
- Что: Marble — генерация исследуемых 3D-миров из текста, изображений, видео.
- ИИ: ядро. Генеративная модель пространства.
- Почему сейчас / узкое место: спрос на симуляцию для роботов и на 3D-контент / вычисления, управляемость.
- Сигнал: раунд ~$1 млрд (18.02.2026) [В] https://www.thesaasnews.com/news/world-labs-raises-1b-series-b/ ; 28.09.2026 AMD объявила о покупке за ~$8,2 млрд акциями, закрытие ожидается до конца 2026 [П] https://newsroom.amd.com/news/amd-acquire-world-labs/ , https://www.cnbc.com/2026/09/28/amd-fei-fei-li-world-labs.html

**Meshy**
- Что: 3D-модели из текста и изображений для игр и 3D-печати.
- ИИ: ядро. Генерация.
- Почему сейчас / узкое место: массовый спрос создателей / качество топологии; все цифры — от самой компании.
- Сигнал: Series B ~$400 млн при оценке $1,5 млрд (07.2026); годовая выручка по подписке >$100 млн, 15 млн пользователей (30.09.2026) [П — пресс-релиз] https://www.morningstar.com/news/pr-newswire/20260930cn60225/meshy-surpasses-100-million-in-annual-recurring-revenue-growing-100x-in-under-two-years

**Tripo AI** (VAST, Пекин)
- Что: 3D-фундаментальные модели и полный конвейер (генерация, текстуры, риггинг).
- ИИ: ядро. Генерация.
- Почему сейчас / узкое место: тот же спрос / конкуренция, данные 3D.
- Сигнал: Series B и B+ ~3 млрд юаней (~$446 млн), 01.09.2026 [П — отраслевое издание] https://www.voxelmatters.com/tripo-ai-raises-3-billion-yuan-in-series-b-and-series-b-funding/

**«cero 3d»** — не идентифицировано (см. начало документа).

### 6. Ещё 10 заметных компаний 2025–2026

- **Project Prometheus** (Безос): ИИ для инженерного проектирования и производства («artificial general engineer»). ИИ — ядро (дизайн). Узкое место: продукта и клиентов публично нет. Сигнал: $6,2 млрд при запуске (11.2025); раунд $10 млрд при оценке $38 млрд (04.2026, FT/Bloomberg) [П] https://thenextweb.com/news/bezos-project-prometheus-10-billion , https://finance.yahoo.com/sectors/technology/articles/bezos-physical-ai-lab-closed-204011972.html
- **Xaira Therapeutics**: ИИ-поиск лекарств с собственной генерацией данных. Модель виртуальной клетки X-Cell на собственном наборе возмущений (17.03.2026) [П] https://www.businesswire.com/news/home/20260317710096/en/Xaira-Therapeutics-Launches-X-Cell-Its-First-Virtual-Cell-Model-Trained-on-the-Largest-Ever-Genome-Wide-Perturbation-Dataset-X-AtlasPisces ; привлечено ~$1,3 млрд [В]; кандидатов в лекарства не раскрыто [В].
- **Edison Scientific** (спин-аут FutureHouse): «ИИ-учёный» Kosmos — многочасовой цикл «литература → анализ данных → гипотезы → отчёт с цитатами». Сигнал: seed $70 млн при оценке ~$250 млн (12.2025) [П] https://techfundingnews.com/edison-raises-70m-ai-scientist-platform/
- **CuspAI**: генеративный дизайн промышленных материалов. Сигнал: $450 млн при оценке $2,6 млрд (20.07.2026) [П] https://siliconangle.com/2026/07/20/ai-materials-science-startup-cuspai-raises-450m-funding/
- **WindBorne Systems**: 600+ долгоживущих метеошаров + собственная ИИ-модель WeatherMesh. Сигнал: Series B $37 млн, оценка $250 млн (05.08.2026) [П] https://techcrunch.com/2026/08/05/ai-makes-weather-prediction-better-can-windborne-make-it-lucrative/
- **Muon Space / FireSat** (с Earth Fire Alliance и Google Research): спутники для обнаружения пожаров; цель — очаги 5×5 м с обновлением каждые 20 минут при ~50 спутниках. Сигнал: первые три рабочих спутника запущены в июле 2026 [П] https://www.muonspace.com/press/muon-space-deploys-first-three-operational-firesat-satellites-for-earth-fire-alliance
- **Rainmaker**: засев облаков с дронов + радарная проверка результата. Сигнал: Series B $100 млн (21.09.2026); «145 млн проверенных галлонов» — заявление компании [П — пресс-релиз] https://finance.yahoo.com/technology/articles/rainmaker-raises-100m-series-b-100000545.html
- **Merge Labs** (Сэм Альтман): неинвазивный нейроинтерфейс на ультразвуке и молекулярных метках. Сигнал: seed ~$250 млн (01.2026), крупнейший чек — OpenAI [П] https://www.theregister.com/2026/01/16/openai_merge_labs_brain_interface_investment/
- **Unitree Robotics**: дешёвые гуманоиды и четвероногие роботы. Сигнал: IPO в Шанхае 19.08.2026, рост в первый день в несколько раз, капитализация ~$50 млрд (цифры расходятся) [П] https://www.forbes.com/sites/johnkoetsier/2026/08/19/unitree-ipos-massive-629-pop-makes-agility-robotics-look-super-cheap/
- **Jua** (Цюрих): ИИ-модель погоды EPT-2 для энерготрейдинга (связка «погода → цена»). Сигнал: Series A ~€10 млн (06.2025) [П] https://siliconcanals.com/jua-closes-e10m-series-a-round/ ; заявления о превосходстве над моделями Google и Microsoft — собственные, независимо не проверены https://thenextweb.com/news/swiss-startup-jua-ai-weather-forecaster-outperforms-microsoft-google

---

## Паттерны формирования идей

Формат: суть (2 предложения) → кто так делает → почему работает → как сжать до 20 часов на CPU с публичными данными по трекам. Везде обязательны: наивная базовая модель для сравнения, отложенная выборка, одна числовая метрика.

### Шпаргалка по данным и лицензиям (что подтверждено в этой работе)
- Open-Meteo: данные CC BY 4.0; бесплатный API только для некоммерческого использования, без ключа, <10 000 запросов в день. Есть Historical Weather (ERA5 с 1940), Historical Forecast (с 2021), Previous Runs (с 01.2024), Ensemble, Air Quality, Flood (GloFAS), Climate Change (CMIP6), Satellite Radiation. https://open-meteo.com/en/terms , https://open-meteo.com/en/features
- ERA5 и CAMS (Copernicus): CC BY 4.0 со 02.07.2025. https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464
- NASA FIRMS (активные пожары): открытые данные NASA, бесплатный ключ MAP_KEY, просят указывать источник. https://www.earthdata.nasa.gov/data/tools/firms
- NASA POWER (солнечная радиация, метео): на сайте NASA указана CC BY 4.0, в зеркалах встречается CC0 — лицензию проверить. https://power.larc.nasa.gov/llms.txt
- OpenAQ (качество воздуха): единой лицензии нет, она зависит от источника — смотреть endpoint licenses; ключ API бесплатный. https://docs.openaq.org/resources/licenses
- USGS (землетрясения): общественное достояние США, без ключа — по сторонним описаниям, сверить с политикой USGS. https://apis.io/apis/u-s-geological-survey/u-s-geological-survey-earthquakes-api/
- NOAA: лицензию проверить (не подтверждено в этой работе).
- World Bank Open Data: по умолчанию CC BY 4.0, если у набора не указано иное. https://data.worldbank.org/summary-terms-of-use
- PhysioNet PTB-XL (ЭКГ, 12 отведений): CC BY 4.0. https://registry.opendata.aws/ptb-xl/ Остальные наборы PhysioNet — лицензию проверять по каждому.
- Kaggle Credit Card Fraud (ULB): по стороннему описанию DbCL 1.0 — проверить на странице Kaggle. https://www.github.com/amazon-science/fraud-dataset-benchmark
- Mozilla Common Voice: CC0. https://github.com/common-voice/common-voice
- FLORES+ (параллельные предложения, 200+ языков): CC BY-SA 4.0. https://huggingface.co/datasets/openlanguagedata/flores_plus
- Tatoeba: CC BY, точную версию проверить.
- AlphaEarth Satellite Embeddings: CC BY 4.0, нужен аккаунт Earth Engine. https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
- Чужие веса моделей тоже имеют лицензии: GraphCast — CC BY-NC-SA, AlphaFold 3 и AlphaGenome — только некоммерческое использование.

### П1. Обученный эмулятор вместо дорогой симуляции
Модель учится на выходах дорогой физической симуляции или на архиве реанализа и выдаёт тот же ответ в тысячи раз быстрее. Скорость превращается в новые возможности: ансамбли, перебор сценариев, работа на слабом железе.
Кто: GraphCast / WeatherNext 2, ECMWF AIFS, Aurora.
Почему работает: десятилетия архивов дают бесплатную разметку; качество честно проверяется на отложенных годах.
- Climate: бустинг «предикторы ERA5 → завтрашняя температура/осадки в моём городе» против persistence и климатологии; Open-Meteo Historical Weather API (CC BY 4.0).
- Health: суррогат эпидемической модели SEIR: сгенерировать 10–50 тыс. синтетических вспышек, обучить «параметры → высота и дата пика», показать ускорение и ошибку; данные синтетические.
- Finance: суррогат метода Монте-Карло для риска портфеля: обучить на синтетических траекториях, показать ускорение при контролируемой ошибке; синтетика.
- Languages: дистилляция: большая многоязычная модель один раз размечает тексты, маленькая (логистическая регрессия на символьных n-граммах) повторяет её на CPU; FLORES+ (CC BY-SA 4.0).

### П2. Фундаментальная модель для новой модальности (эмбеддинги как сырьё)
Самообучение на огромном неразмеченном корпусе «нового языка» (белки, ДНК, атмосфера, клетки, спутниковые снимки, действия робота) даёт представления, из которых дёшево решаются десятки задач. Школьнику не нужно обучать такую модель: достаточно взять готовые эмбеддинги и поставить сверху лёгкий классификатор.
Кто: AlphaFold 3 / ESM3 / Chai (белки), AlphaGenome (ДНК), Aurora (атмосфера), AlphaEarth (снимки), Physical Intelligence / Skild (действия).
Почему работает: разметки мало, сырых данных много; линейная модель поверх эмбеддингов считается на CPU.
- Climate: AlphaEarth Satellite Embeddings (CC BY 4.0) → логистическая регрессия «застройка / лес / вода / поле» по 200–500 вручную размеченным точкам своего региона.
- Health: признаки ЭКГ из PTB-XL (CC BY 4.0) или эмбеддинги малой белковой модели (лицензию проверить) + лёгкий классификатор.
- Finance: малая готовая модель временных рядов в режиме zero-shot (лицензию проверить) против наивного сезонного прогноза на рядах World Bank (CC BY 4.0).
- Languages: эмбеддинги малой многоязычной модели предложений (лицензию проверить) → поиск «вопрос на русском → предложение на английском»; FLORES+.

### П3. ИИ-разведка: где бурить, копать, строить
Самое дорогое действие (скважина, рудник, стройка) совершается после того, как модель по публичным геоданным ранжирует места по вероятности успеха. Продукт — рост доли удачных попыток, а не красивая карта.
Кто: KoBold Metals, Zanskar (месторождение Big Blind без признаков на поверхности), частично Fervo.
Почему работает: прогноз стоит на порядки меньше ошибки; открытых геоданных много; неопределённость считается явно.
- Climate: «где ставить солнечные панели / датчики воздуха / пункты охлаждения»: NASA POWER (лицензию проверить) + Open-Meteo, проверка на отложенных точках.
- Health: «где не хватает медпункта или аптеки»: модель спроса по открытым данным о населении и OpenStreetMap (лицензии проверить); метрика — покрытие при k новых точках.
- Finance: «где люди без банковского счёта»: World Bank Global Findex (CC BY 4.0 по умолчанию) → вероятность отсутствия счёта по признакам + объяснение факторов.
- Languages: «где переводчик ошибётся»: модель предсказывает плохие переводы без эталона, чтобы человек проверял только их; FLORES+.

### П4. Замкнутый цикл «модель предлагает → эксперимент проверяет → модель учится»
Модель сама выбирает следующий эксперимент там, где она наименее уверена, а результат сразу становится обучающим примером. Данные накапливаются как собственный актив.
Кто: Lila Sciences, Periodic Labs, Recursion, Xaira.
Почему работает: каждая проверка несёт максимум информации; нужно в разы меньше меток.
- Health: активное обучение на PTB-XL: модель выбирает, какие ЭКГ «отдать врачу на разметку»; график «качество от числа меток» против случайного выбора.
- Finance: какие транзакции отправлять на ручную проверку; Kaggle Credit Card Fraud (лицензию проверить) или синтетика.
- Climate: байесовская оптимизация размещения k датчиков или настроек батареи в простом симуляторе.
- Languages: активная разметка: модель выбирает 20 предложений, участник размечает сам, цикл повторяется; тексты Tatoeba (лицензию проверить).

### П5. Коррекция глобальной модели локальными данными
Глобальная модель хороша в среднем, но систематически ошибается в конкретном месте или группе. Лёгкая модель поверх неё учит остаточную ошибку по локальным наблюдениям.
Кто: Tomorrow.io, WindBorne, Jua, Brightband.
Почему работает: хватает малой выборки; базовая модель бесплатна; выигрыш измерим «до и после».
- Climate: Open-Meteo Previous Runs API (прогнозы с фиксированной заблаговременностью) + фактические значения → бустинг на остатках для своего города; метрика — средняя абсолютная ошибка против сырого прогноза.
- Health: перекалибровка готовой шкалы риска под другую популяцию: показать, как калибровка падает и восстанавливается; публичные табличные наборы (лицензию проверить).
- Finance: поправка наивного сезонного прогноза погодными признаками (спрос на электроэнергию, продажи); Open-Meteo + открытые данные энергосистем (лицензию проверить).
- Languages: постредактор поверх готового переводчика под типичные ошибки русскоязычных (артикли, предлоги); пары «ошибка → исправление» из синтетики и собственной разметки.

### П6. Раннее обнаружение по камерам, спутникам, датчикам
Модель непрерывно смотрит на поток данных и поднимает тревогу раньше человека. Ценность измеряется выигранным временем и числом ложных тревог на одно верное срабатывание.
Кто: Pano AI (камеры + человек-верификатор), FireSat / Muon Space, Waymo.
Почему работает: ущерб растёт нелинейно со временем обнаружения; датчики дешёвые; человек в контуре гасит ложные тревоги.
- Climate: NASA FIRMS + погода Open-Meteo → риск пожара на завтра по ячейкам сетки одного региона; метрики PR-AUC и «тревог на одно попадание».
- Health: ранний признак нарушения ритма по ЭКГ (PTB-XL) или прогноз «опасных дней» по качеству воздуха (OpenAQ, лицензии по источникам).
- Finance: раннее обнаружение мошенничества или аномальных расходов с ограничением на число ложных тревог; Kaggle Credit Card Fraud (лицензию проверить) или синтетика.
- Languages: детектор мошеннических сообщений на русском и английском; публичные наборы SMS-спама (лицензию проверить) + синтетика.

### П7. Перенести вычисления туда и тогда, где энергия дешёвая и чистая
Гибкую нагрузку двигают в пространстве (к дешёвой энергии, вплоть до орбиты) или во времени (к часам избытка). Для этого нужен прогноз цены или углеродной интенсивности и планировщик.
Кто: Crusoe, Starcloud, Google Project Suncatcher, SpaceX / xAI, Blue Origin.
Почему работает: узкое место ИИ — электричество, а не чипы (Stargate: ~0,3 ГВт работает при >9 ГВт в планах на 04.2026).
- Climate: прогноз углеродной интенсивности сети на 24 часа + планировщик гибких нагрузок; бэктест «кг CO2 сэкономлено» на открытых данных энергосистем (лицензию проверить).
- Finance: прогноз почасовой цены электроэнергии + сдвиг нагрузки; бэктест экономии в деньгах (те же источники).
- Languages: каскад моделей: маленькая отвечает сама, большую зовёт только при низкой уверенности; график «качество от доли тяжёлых вызовов».
- Health: применимо слабо; только на синтетике — предсказать, какие обращения можно обслужить дистанционно.

### П8. Свой датчик — свои данные
Компания владеет уникальным источником наблюдений, а модель строится уже поверх него. Модели быстро становятся общедоступными, уникальные данные — нет.
Кто: Tomorrow.io (спутники), WindBorne (шары), Pano AI (камеры), Recursion / Xaira / Tahoe (собственные клеточные данные), Neuralink (имплант).
Почему работает: конкуренту нечем обучить такую же модель.
Ограничение хакатона: данные должны быть публичными или синтетическими, поэтому «свой датчик» заменить на собственную разметку публичных данных или собственный генератор синтетики.
- Languages: своя разметка 300–500 публичных предложений (тип ошибки, уровень сложности) → модель, которой нет у других; Tatoeba (лицензию проверить).
- Climate: своя разметка точек на спутниковых эмбеддингах AlphaEarth (CC BY 4.0) под локальный класс (свалки, теплицы, гари).
- Health: своя разметка качества записи (шум, артефакт) на подвыборке PTB-XL.
- Finance: своя разметка публичных текстов жалоб или заголовков по категориям (лицензию источника проверить).

### П9. Физика + ML (гибрид)
Известные законы и формулы остаются каркасом, а ML учит только то, что формула не объясняет. Это требует меньше данных и лучше ведёт себя вне обучающего диапазона.
Кто: NeuralGCM, CFS (цифровой двойник плазмы), Zanskar (ML + физические модели недр).
Почему работает: модель не тратит данные на то, что уже известно; экспертам проще ей доверять.
- Climate: модель ясного неба + ML-поправка на облачность → прогноз солнечной выработки; NASA POWER (лицензию проверить), Open-Meteo Satellite Radiation.
- Health: эпидемическая модель SIR + ML-остаток; синтетика или открытые ряды заболеваемости (лицензию проверить).
- Finance: формула Блэка–Шоулза или сезонная модель + ML-остаток; синтетика, World Bank.
- Languages: правила (морфология, транслитерация) + ML только для исключений, например расстановка ударений.

### П10. Генеративный дизайн + быстрый отбор
Модель не оценивает готовое, а предлагает тысячи вариантов; дешёвый фильтр оставляет десяток для дорогой проверки. Ценность — в качестве фильтра и разнообразии лучших кандидатов.
Кто: Chai Discovery, Isomorphic Labs, EvolutionaryScale, CuspAI, Meshy / Tripo, Project Prometheus.
Почему работает: генерация дешёвая, проверка дорогая.
- Health: кандидаты-пептиды простыми мутациями + модель-оценщик на публичных данных активности (лицензию проверить); метрика — обогащение лучших k на отложенных данных; только расчёт, без медицинских утверждений.
- Climate: генерация конфигураций «панели + батарея + тариф» → эмулятор оценивает → фронт Парето.
- Finance: генерация стресс-сценариев или вариантов бюджета → модель риска отбирает худшие и лучшие; синтетика.
- Languages: генерация упражнений (пропуски, неправильные варианты) → модель сложности отбирает подходящие по уровню; тексты Tatoeba (лицензию проверить).

### П11. Поиск с автоматическим судьёй (паттерн AlphaEvolve)
Если решение можно оценить программой, перебор с отбором лучших вариантов обгоняет интуицию. Судья-программа исключает выдумки: плохое решение просто не проходит.
Кто: AlphaEvolve, Edison Scientific (Kosmos).
Почему работает: метрика объективна и дешёва; результат можно перепроверить.
- Climate: символьная регрессия ищет компактную формулу индекса жары, которая точнее стандартной на данных ERA5 / Open-Meteo.
- Health: эволюционный поиск простой балльной шкалы риска (не более 7 признаков) против логистической регрессии; публичный табличный набор (лицензию проверить).
- Finance: поиск понятных правил скоринга против «чёрного ящика»; публичный набор о дефолтах (лицензию проверить).
- Languages: поиск правил исправления неверной раскладки клавиатуры и транслита (русский ↔ английский) с автоматической метрикой точности.

### П12. Измерение и проверка как продукт
Компания продаёт не эффект, а доверенное число: сколько выброшено, насколько точен прогноз, сработал ли засев. Тот, кто задаёт линейку, направляет деньги и исследования.
Кто: Watershed (учёт выбросов), Brightband (Extreme Weather Bench), Arc Institute (Virtual Cell Challenge), Rainmaker (радарная проверка).
Почему работает: разрыв между заявленным и измеренным огромен (Climeworks Mammoth: 675 т за полугодие при проектных 36 000 т в год).
- Climate: мини-бенчмарк экстремальной погоды для своей страны: сравнить несколько моделей через Open-Meteo в дни жары и ливней + мета-модель, выбирающая лучшую под ситуацию.
- Health: аудит калибровки и равенства качества по подгруппам (возраст, пол) для классификатора на PTB-XL.
- Finance: честный стенд бэктеста прогнозов (скользящее окно, без заглядывания в будущее) на рядах World Bank + ансамбль.
- Languages: мини-бенчмарк распознавания речи для малоресурсного языка; Common Voice (CC0; наличие языка проверить), малая модель распознавания на CPU (лицензию проверить).

### П13. Якорный покупатель с острой проблемой
Идея формулируется от ограничения конкретного платёжеспособного покупателя, у которого только что изменились условия. Договор с ним превращает научный риск в финансируемый проект.
Кто: Fervo и Zanskar (дата-центрам нужна круглосуточная мощность), Helion (договор с Microsoft), Form Energy (Google + Xcel), Redwood (микросеть для Crusoe), WAVR (вода для дата-центров).
Почему работает: спрос доказан до того, как построен продукт.
- Health: прогноз неявок на приём → число освобождённых слотов; публичный набор о неявках (лицензию проверить).
- Finance: прогноз стоимости денежного перевода для мигрантов; World Bank Remittance Prices Worldwide (лицензию проверить).
- Climate: прогноз потребления воды и энергии на охлаждение для заданного климата; погода Open-Meteo + синтетическая нагрузка.
- Languages: один пользователь — русскоязычный школьник, читающий английскую научную аннотацию: модель находит и упрощает трудные термины.

### П14. Перенос зрелой технологии из соседней отрасли
Берётся метод, уже отлаженный в другой отрасли, и применяется к новой задаче. Новизна — в применении, а не в изобретении.
Кто: Fervo (сланцевое бурение → геотермия), Quaise (гиротроны термояда → бурение), Redwood (батареи электромобилей → сеть), Synchron (стенты → нейроинтерфейс), Science Corp (купленный имплант PRIMA).
Почему работает: самое трудное уже сделано другими.
- Health ← Finance: методы поиска мошенничества (isolation forest, автоэнкодер) для поиска аномальных ЭКГ.
- Finance ← Climate: ансамбли и метеорологические метрики вероятностного прогноза для расходов и продаж.
- Climate ← Languages: поиск похожих прошлых ситуаций как поиск похожих текстов (аналоговый прогноз по ERA5).
- Languages ← биоинформатика: выравнивание последовательностей + классификатор для поиска родственных слов в близких языках.

### П15. Синтетический мир как тренировочная площадка
Модель учится в симуляции, где редкие и опасные случаи можно создавать без ограничений, а затем проверяется на реальных данных. Честный проект обязательно измеряет разрыв между симуляцией и реальностью.
Кто: Waymo, Wayve, World Labs (Marble), Skild AI, Physical Intelligence.
Почему работает: реальные данные редки, дороги или недоступны из-за приватности.
- Health: обучить на синтетических пациентах (генератор Synthea — лицензию проверить), проверить на небольшом реальном публичном наборе, показать разрыв.
- Finance: симулятор транзакций с внедрённым мошенничеством → проверка на реальном наборе Kaggle (лицензию проверить).
- Climate: симулятор дома с батареей на погоде одного года → проверка на другом годе; Open-Meteo.
- Languages: синтетический шум (опечатки, чужая раскладка, транслит) → модель исправления, проверка на реальных ошибках.

### П16. Узкий вход — потом широкая платформа
Сначала решается одна узкая задача, где ошибка терпима, а польза очевидна. Работающее внедрение даёт данные и доверие для расширения.
Кто: Figure (одна операция на заводе BMW), Waymo (город за городом), Science Corp (одно заболевание), Synchron (простые команды), Meshy (модели для игр и печати).
Почему работает: узкую задачу реально довести до работающего состояния.
- Health: «пригодна ли запись ЭКГ для анализа?» вместо «ИИ-врача».
- Finance: один тип расходов или один тип мошенничества.
- Climate: одна опасность в одном городе.
- Languages: один класс ошибок — артикли a/the у русскоязычных (в русском языке артиклей нет).

### П17. Вероятностный прогноз вместо точечного
Модель выдаёт не одно число, а распределение или интервал с проверенным покрытием. Решения зависят от «хвостов», поэтому платят именно за калиброванную неопределённость.
Кто: GenCast / WeatherNext 2, ECMWF AIFS ENS (51 член), Zanskar.
Почему работает: ИИ сделал ансамбли дешёвыми; интервал легко проверить на истории.
- Climate: квантильная регрессия или конформные интервалы для температуры или PM2.5; сравнение покрытия с Open-Meteo Ensemble API.
- Health: конформное предсказание с вариантом «воздержаться и передать врачу»; метрики — покрытие и доля отказов.
- Finance: интервалы для расходов или денежного потока, проверка покрытия на бэктесте.
- Languages: подсветка слов с низкой уверенностью распознавания или перевода для проверки человеком.

### П18. ИИ-учёный: агент, соединяющий инструменты
Система сама проходит цепочку «литература → гипотеза → анализ данных → отчёт со ссылками». Узкое место смещается с генерации идей на их проверку.
Кто: Edison Scientific (Kosmos), Xaira (X-Scientist), Lila, Periodic.
Почему работает: рутинные шаги автоматизируются, человек проверяет выводы.
Ограничение: без платного API и на CPU делать версию без большой языковой модели — поиск + ранжирование + классификация.
- Health: проверка утверждения: найти в публичных аннотациях PubMed (условия использования проверить) фрагменты «за» и «против» и классифицировать их.
- Languages: межъязыковой поиск: вопрос по-русски → английские источники.
- Finance: автоматический отчёт об аномалиях в открытом ряду с вкладом признаков.
- Climate: «паспорт события»: аналоги волны жары в архиве ERA5 + оценка редкости.

### Быстрый выбор для 20 часов на CPU (связки с самым низким риском)
1. П5 × Climate — поправка прогноза для своего города: API без ключа, одна метрика, понятная базовая модель.
2. П16 + П15 × Languages — артикли у русскоязычных: узко, синтетика + своя разметка, сильная сторона участника — русский язык.
3. П6 × Climate — риск пожара на завтра по FIRMS + погоде.
4. П4 × Health — активное обучение на PTB-XL: результат — кривая экономии меток.
5. П17 × Finance — интервалы с проверенным покрытием вместо точечного прогноза.

---

## Анти-паттерны

1. **Заявлять физический или клинический эффект, который нельзя измерить за 20 часов.** «Модель спасает жизни / сокращает CO2» — недоказуемо. Заявлять только офлайн-метрику на отложенных данных и явные ограничения. Урок индустрии: Climeworks (675 т за полугодие против 36 000 т в год), Helion (смягчение формулировок о сроках), исправление к статье A-Lab о «новых» материалах.
2. **Утечка данных и нечестная валидация.** Случайное разбиение для временных рядов и соседних точек, записи одного пациента в обучении и тесте, подбор параметров на тестовой выборке. Для времени — разбиение по датам, для людей — по пациентам, для карт — по регионам.
3. **Нет наивной базовой модели.** Без persistence, климатологии, сезонного наивного прогноза или логистической регрессии любое число бессмысленно. Даже Arc Institute называет свою модель State «стартовым бенчмарком».
4. **Обёртка над платной языковой моделью.** ИИ должен делать основную работу сам; демо не должно зависеть от платного API и интернета. Использовать малые локальные модели и классический ML.
5. **Непосильный масштаб.** Обучать с нуля модель погоды, 3D или робота, качать гигабайты снимков на CPU. Брать готовые эмбеддинги, одну территорию, табличные признаки.
6. **Данные с неясной лицензией или приватные.** Скрейпинг сайтов, медицинские данные знакомых, наборы Kaggle без проверки лицензии, клинические базы с обязательной аккредитацией, чужие веса с запретом коммерческого использования. Для каждого набора записать лицензию и требование указания источника.
7. **Медицинский диагноз и инвестиционный совет.** «Ставит диагноз» и «предсказывает цену акций» — зона наибольшего риска и переобучения. Формулировать как поддержку решения, сортировку или прогноз физических и поведенческих величин (спрос, расходы, риск события).
8. **Путать «объявлено» с «работает».** Оценка компании и анонс — не результат: Stargate — ~0,3 ГВт в работе при «более 10 ГВт» законтрактованных; Project Prometheus — $38 млрд без публичного продукта; GNoME — много предсказаний, часть из них дубликаты. В своём проекте разделять «сделано и измерено» и «планируется».

---

## Источники

Все ссылки ниже реально использованы в работе (поиск и чтение 15.11.2026).

**ИИ для науки**
- https://www.isomorphiclabs.com/articles/isomorphic-labs-announces-series-b-investment-round
- https://www.bloomberg.com/news/articles/2026-10-08/alphabet-s-isomorphic-labs-in-funding-talks-for-at-least-40-billion-value
- https://thenextweb.com/news/isomorphic-labs-5bn-funding-talks-50bn-valuation
- https://www.airosetta.com/en/news/isomorphic-labs-isodde-drug-design-engine
- https://www.gobi.vc/news/gobi-partners-backs-cortical-labs-to-advance-thenext-frontier-of-biological-intelligence
- https://www.datacenterdynamics.com/en/news/australian-startup-cortical-labs-unveils-worlds-first-commercial-biological-computer/
- https://itbrief.com.au/story/cortical-labs-cl1-commercial-milestone-after-aud-245k-grant
- https://uk.investing.com/news/stock-market-news/lila-sciences-in-talks-for-2b-funding-at-85b-valuation--bloomberg-93CH-4712331
- https://research.contrary.com/company/lila-sciences
- https://www.bloomberg.com/news/articles/2026-03-25/ai-science-startup-periodic-labs-is-in-deal-talks-at-about-7-billion-valuation
- https://www.forbes.com/sites/iainmartin/2026/05/07/former-openai-researcher-to-raise-500-million-for-ai-science-startup/
- https://blogs.nvidia.com/blog/evolutionaryscale-esm3-generative-ai-nim-bionemo-h100/
- https://www.axios.com/2025/11/06/zuckerberg-chan-biohub-ai-disease
- https://pulse2.com/chai-discovery-raises-400-million-series-c-to-advance-ai-driven-molecular-design/
- https://www.citybiz.co/article/874292/chai-discovery-raises-400-million-series-c-to-scale-ai-drug-discovery-platform/
- https://www.sec.gov/Archives/edgar/data/0001601830/000160183026000097/exhibit991-q0226.htm
- https://www.investing.com/news/company-news/recursion-q1-2026-slides-ai-pipeline-advances-amid-revenue-challenges-93CH-4681698
- https://arcinstitute.org/news/virtual-cell-challenge-2026
- https://virtualcellchallenge.org/
- https://www.citybiz.co/article/729454/tahoe-therapeutics-raises-30m/
- https://www.talindrew.com/guides/alphafold-3-commercial-use
- https://www.nature.com/articles/s41586-025-10014-0
- https://github.com/google-deepmind/alphagenome
- https://www.i-scoop.eu/alphagenome-2/
- https://github.com/google-deepmind/alphaevolve
- https://buildmind.ai/blog/google-deepmind-alphaevolve-may-2026-production-algorithm-discovery/
- https://cen.acs.org/research-integrity/Google-DeepMind-structures-near-duplicates-questionable/104/web/2026/10
- https://github.com/google-deepmind/weathernext
- https://datanorth.ai/news/google-deepmind-open-sources-weathernext-2-and-weathernext-cyclones
- https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
- https://medium.com/google-earth/alphaearth-foundations-satellite-embeddings-now-available-on-google-cloud-storage-f9ab0f7252d6
- https://thenextweb.com/news/bezos-project-prometheus-10-billion
- https://finance.yahoo.com/sectors/technology/articles/bezos-physical-ai-lab-closed-204011972.html
- https://www.businesswire.com/news/home/20260317710096/en/Xaira-Therapeutics-Launches-X-Cell-Its-First-Virtual-Cell-Model-Trained-on-the-Largest-Ever-Genome-Wide-Perturbation-Dataset-X-AtlasPisces
- https://techfundingnews.com/edison-raises-70m-ai-scientist-platform/
- https://siliconangle.com/2026/07/20/ai-materials-science-startup-cuspai-raises-450m-funding/

**Климат, энергия, вода, погода**
- https://www.quaise.com/news/quaise-energy-closes-180-million-series-b-with-35-million-investment-by-nabors-industries
- https://www.quaise.com/news/quaise-energy-raises-134-million-in-first-close-of-series-b-to-build-worlds-first-superhot-geothermal-power-plant
- https://www.utilitydive.com/news/worlds-largest-grid-battery-part-of-google-xcel-energy-agreement/813793/
- https://www.energy-storage.news/iron-air-us-ldes-startup-form-energy-secures-us750-million-series-g-financing/
- https://www.bloomberg.com/news/articles/2026-09-10/carbon-removal-pioneer-climeworks-increases-co2-capture-sixfold
- https://www.swissinfo.ch/eng/climate-solutions/why-swiss-carbon-removal-start-up-climeworks-faces-serious-headwinds/89386618
- https://techcrunch.com/2026/07/30/fusion-power-darling-commonwealth-fusion-systems-raises-another-1b/
- https://www.businesswire.com/news/home/20260604740624/en/Helion-Raises-$465-Million-Series-G-Funding-Round-to-Meet-Surging-Global-Demand-for-Power
- https://www.geekwire.com/2026/helion-funding-round-grows-to-500m-amid-uncertainty-over-fusion-startups-microsoft-timeline/
- https://www.axios.com/pro/climate-deals/2026/09/08/helion-energy-fusion-net-electricity-date-year
- https://techcrunch.com/2026/02/13/fusion-startup-helion-hits-blistering-temps-as-it-races-toward-2028-deadline/
- https://techcrunch.com/2026/05/13/geothermal-startup-fervo-energy-pops-33-in-ipo-debut-fueled-by-ai-data-center-demand/
- https://fortune.com/2026/05/14/fervo-clean-energy-biggest-ipo-10b-valuation-powered-earths-heat-ai-hunger/
- https://www.globenewswire.com/news-release/2026/01/21/3222733/0/en/zanskar-raises-115m-series-c-following-record-setting-year-of-geothermal-discoveries.html
- https://www.thinkgeoenergy.com/zanskar-to-supply-100-mw-of-geothermal-power-to-amazon-data-centres/
- https://www.renewableenergymagazine.com/geothermal/zanskar-inks-100-mw-ppa-to-provide-20260520
- https://miningindaba.com/articles/kobold-metals-breaks-ground-on-23-billion-min
- https://www.berkeleyside.org/2026/10/05/kobold-metals-berkeley
- https://www.datacenterdynamics.com/en/news/crusoe-raises-39bn-for-ai-data-center-build-out/
- https://www.esgtoday.com/home-battery-startup-base-power-raises-1-billion-at-13-billion-valuation/
- https://heatmap.news/climate-tech/redwood-425-million-series-e
- https://www.energy-storage.news/redwood-energy-positions-second-life-bess-as-essential-infrastructure-for-us-data-centre-load-growth-domestic-manufacturing-needs/
- https://www.opportunitylouisiana.gov/news/heirloom-carbon-technologies-announces-475-million-investment-to-establish-north-americas-second-direct-air-capture-facility-in-louisiana
- https://www.heirloomcarbon.com/projects
- https://www.latitudemedia.com/industry-news/pano-ai-raises-44m-series-b-led-by-giant-ventures-to-scale-early-detection-infrastructure/
- https://www.forbes.com/sites/afdhelaziz/2026/07/09/how-pano-and-sonia-kastner-a-using-ai-to-stop-wildfires-across-america/
- https://spacenews.com/tomorrow-io-banks-175-million-for-deepsky-weather-constellation/
- https://www.satellitetoday.com/finance/2026/02/03/tomorrow-io-raises-175m-to-build-out-deepsky-weather-constellation/
- https://techcrunch.com/2024/09/19/brightband-sees-a-bright-and-open-source-future-for-ai-powered-weather-forecasting/
- https://www.brightband.com/company/news/
- https://trellis.net/article/california-startup-watershed-raises-100-million-emissions-tracking-software/
- https://www.globenewswire.com/news-release/2026/03/11/3253995/0/en/Independent-Research-Firm-Names-Watershed-a-Leader-in-Carbon-Management-Software.html
- https://www.reviewjournal.com/business/vegas-business/innovation/las-vegas-startup-turns-desert-air-into-water-3865505/
- https://www.wavrtechnologies.com/about-us
- https://www.benzinga.com/news/topics/25/09/47906771/startup-backed-by-4m-funding-says-it-can-pull-10k-gallons-of-water-a-day-from-desert-air-using-frog-i
- https://thenextweb.com/news/deepmind-ai-graphcast-weather-forecasting
- https://huggingface.co/shermansiu/dm_graphcast
- https://www.microsoft.com/en-us/research/blog/aurora-1-5-extending-open-foundation-models-for-weather-and-earth-system-applications/
- https://research.google/blog/neuralgcm-harnesses-ai-to-better-simulate-long-range-global-precipitation/
- https://forum.ecmwf.int/t/ifs-cycle-50r1-and-aifs-v2-implementation-planned-for-12-may-2026/14781
- https://huggingface.co/ecmwf/aifs-ens-2.0
- https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data
- https://techcrunch.com/2026/08/05/ai-makes-weather-prediction-better-can-windborne-make-it-lucrative/
- https://www.muonspace.com/press/muon-space-deploys-first-three-operational-firesat-satellites-for-earth-fire-alliance
- https://finance.yahoo.com/technology/articles/rainmaker-raises-100m-series-b-100000545.html
- https://siliconcanals.com/jua-closes-e10m-series-a-round/
- https://thenextweb.com/news/swiss-startup-jua-ai-weather-forecaster-outperforms-microsoft-google

**Вычисления и космос**
- https://starcloud.com/starcloud-1
- https://thenextweb.com/news/starcloud-170m-series
- https://www.bnnbloomberg.ca/business/company-news/2026/08/21/orbital-data-center-startup-starcloud-valued-at-us23-billion-in-latest-funding/
- https://www.npr.org/2026/10/01/nx-s1-5983697/project-suncatcher-google-ai-data-center-space
- https://www.opb.org/article/2026/10/01/google-launches-project-suncatcher-a-step-towards-ai-data-centers-in-space/
- https://www.technology.org/2026/11/03/google-suncatcher-satellite-gemma-4-orbit-tpu/
- https://www.datacenterdynamics.com/en/news/spacex-files-for-million-satellite-orbital-ai-data-center-megaconstellation/
- https://www.satellitetoday.com/connectivity/2026/02/02/spacex-acquires-xai-to-pursue-orbital-data-center-constellation/
- https://www.datacenterdynamics.com/en/news/spacex-ipo-musks-firm-set-to-launch-first-orbital-data-center-ai1-satellites-in-2027-will-put-compute-on-starlink-craft/
- https://thenextweb.com/news/spacex-orbital-data-centres-ipo-risk-disclosure
- https://www.datacenterdynamics.com/en/news/bezos-backed-blue-origin-files-for-approval-to-put-data-centers-in-space/
- https://www.datacenterdynamics.com/en/news/space-data-center-company-aetherflux-reportedly-raising-series-b-funding-at-2bn-valuation/
- https://epoch.ai/publications/openai-stargate-where-the-us-sites-stand
- https://stargate.how/news/has-stargate-reached-10-gw

**Робототехника и нейроинтерфейсы**
- https://www.bloomberg.com/news/articles/2026-10-27/robotics-lab-physical-intelligence-in-talks-for-a-20-billion-valuation
- https://www.figure.ai/news/f-03-at-bmw
- https://www.bmwblog.com/2026/06/26/bmw-figure-03-humanoid-robot-spartanburg-plant/
- https://en.wikipedia.org/wiki/Figure_AI
- https://www.humanoidsdaily.com/companies/1x-technologies
- https://en.wikipedia.org/wiki/1X_Technologies
- https://www.businesswire.com/news/home/20260114335623/en/Skild-AI-Raises-$1.4B-Now-Valued-Over-$14B
- https://www.cnbc.com/2026/02/24/wayve-fundraise-nvidia-microsoft.html
- https://finance.yahoo.com/news/waymo-eyes-1-million-paid-152515066.html
- https://www.revenuememo.com/p/waymo-funding
- https://www.neurapod.com/neuralink-by-the-numbers
- https://www.medtechdive.com/news/synchron-funding-bci-200m/804977/
- https://app.dealroom.co/news/feed/synchron-raises-275m-to-commercialise-stentrode-brain-computer-interface
- https://businesswire.com/news/home/20260305896789/en/Science-Corporation-Closes-%24230-Million-Series-C-to-Accelerate-Commercialization-of-Its-PRIMA-BCI-Retinal-Implant-the-Worlds-Most-Advanced-Vision-Restoration-Technology
- https://newatlas.com/medical-tech/vision-restoring-retinal-implant-approval-europe/
- https://www.theregister.com/2026/01/16/openai_merge_labs_brain_interface_investment/
- https://www.forbes.com/sites/johnkoetsier/2026/08/19/unitree-ipos-massive-629-pop-makes-agility-robotics-look-super-cheap/
- https://www.caixinglobal.com/2026-07-31/robotics-startup-unitree-launches-620-million-star-market-ipo-102469723.html

**3D и мировые модели**
- https://www.thesaasnews.com/news/world-labs-raises-1b-series-b/
- https://newsroom.amd.com/news/amd-acquire-world-labs/
- https://www.cnbc.com/2026/09/28/amd-fei-fei-li-world-labs.html
- https://www.morningstar.com/news/pr-newswire/20260930cn60225/meshy-surpasses-100-million-in-annual-recurring-revenue-growing-100x-in-under-two-years
- https://pulse2.com/meshy-surpasses-100-million-in-arr-after-raising-nearly-400-million-at-1-5-billion-valuation/
- https://www.voxelmatters.com/tripo-ai-raises-3-billion-yuan-in-series-b-and-series-b-funding/

**Данные и лицензии**
- https://open-meteo.com/en/terms
- https://open-meteo.com/en/features
- https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464
- https://www.earthdata.nasa.gov/data/tools/firms
- https://firms.modaps.eosdis.nasa.gov/api/area/csv
- https://power.larc.nasa.gov/llms.txt
- https://docs.openaq.org/resources/licenses
- https://docs.openaq.org/using-the-api/api-key
- https://apis.io/apis/u-s-geological-survey/u-s-geological-survey-earthquakes-api/
- https://data.worldbank.org/summary-terms-of-use
- https://registry.opendata.aws/ptb-xl/
- https://www.physionet.org/content/ptb-xl/1.0.3/
- https://www.github.com/amazon-science/fraud-dataset-benchmark
- https://github.com/common-voice/common-voice
- https://huggingface.co/datasets/openlanguagedata/flores_plus
