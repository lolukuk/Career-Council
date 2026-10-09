# Оценка совета консультантов по описанию кейса

Current retained R2f: user requested to leave the demonstrated SYNTHETIC34037-byte context and stop optimizing. Complete suite188passed54.55s; codec independent PASS WITH RISK/CIT-T01 fixed.32768 cap unchanged, sizing FAIL; no further paid call, full FR-1–FR-9 acceptance remains open. Exact history and artifacts: docs/agent-base/features/multi-agent-consensus/citation-stabilization.md.

## Latest r10 / R2e

Последний separately authorized live `b8a17d9bdec54861882e922a0adc2cc3`:5first-try exact-ID initial positions1218–1344bytes +1draft, затем FAILED на review protocol,0atomicvotes. Дополнительный лимит1/1 исчерпан. Saved draft содержит assumption c4 без связанной caveat; early coordinator guard+specific safe protocol repair реализованы offline. **159passed48.44s exit0**, independent design PASS WITH RISK, independent actual code review PASS WITH RISK/49focused15.51s. Полное FR-1–FR-9 outcome не принято; точную причину всех rejected votes старый generic trace не сохраняет. [Все actual results/диагноз/guards/gates](agent-base/features/multi-agent-consensus/citation-stabilization.md). Ниже исторические checkpoint/evidence.

## Текущий successor r10 / citation stabilization

**Полное задание ещё не выполнено.** Выбор exact frozen excerpts по request-local evidence ID внедрён вместо свободного воспроизведения цитат; strict quote/digest/visibility/provenance guards сохранены. Новые3/3 разрешённых запуска завершились failed/incomplete; лучший `465e5e84e42843c0aadc95d9a2a8e761` получил5позиции+1draft без citation/schema/protocol errors, но mandatory review closure превышала32768. Последний `10556af0245c429fa1f0fafe16bf7ee9` FAILED по новому generation byte envelope1600,0atomicpositions/decisions. Он не прошёл citation guard; это не evidence точности всех его цитат.

После него offline исправлены field bounds и safe addressed repair/size diagnostics, без увеличения лимитов или замены результатов. Последняя полная проверка154passed58.87s exit0; независимый latest code review PASS WITH RISK,34focused6.77s. FR-1/FR-2/FR-3 и семантическое качество полного пятистороннего отчёта остаются открытыми. Дополнительных paid calls нет; новый run требует нового явного бюджета. [Полный root-cause/альтернативы/изменения/риски](agent-base/features/multi-agent-consensus/citation-stabilization.md), [checkpoint/gates](agent-base/features/multi-agent-consensus/workflow.md), [независимый review](agent-base/features/multi-agent-consensus/handoffs/citation-review/result.md). Далее сохранён исторический r9 audit.

## Текущий аудит и согласованный корректирующий маршрут C01–C06

2026-10-09. Пользователь утвердил выполнение C01–C06 по всем FR-1–FR-9. Только Markdown/локальные изменения, без Git-коммита. Текущий профиль AI Tunnel / gpt-6-luna-pro сохраняется. Исходный user_prompt неизменен относительно Git HEAD council/. Прежняя приёмка scripted-прототипа остаётся историческим фактом, а приёмка полного задания открыта.

Read-only baseline: точная команда `.\\.venv-consensus\\Scripts\\python.exe -m pytest council/tests -q` → 123 passed, 26.49s, exit0. Среди сохранённых полных model trace шесть failed, ноль полных пяти позиций и решений; single-position диагностики не являются полным советом. Git имеется в council/, но общий обзор и feature-workspace расположены вне его; большая часть реализации untracked. Эти факты уточняют прежний обзор ниже.

| ID / приоритет | Подтверждённая проблема | Доказательство | Исправление / приёмка |
| --- | --- | --- | --- |
| A01 / P1 | Нет полного живого результата | council/output/*/trace.json, последующий PI08 | C04/C06: пять валидных позиций, решение, полезный consensus или no_consensus |
| A02 / P2 | Current headers и схемы показывают старые стадии | workflow/status/routing, artifacts/flows | C01: отдельный актуальный successor, история сохраняется |
| A03 / P2 | Прежний обзор неверно объявляет FR-7/FR-8 необязательными | прежние разделы 2 и 5 ниже; council/task.md | C01/C03: LangGraph обязателен, read-tool доступен консультантам |
| A04 / P2 | Шумные заметки принудительно закрепляются | council/context.py mandatory category fallback | C02: shortlist≤20, bounded relevance filter, допустим ноль релевантных |
| A05 / P2 | API-prefetch не доказывает доступность tool агентам | council/sources.py; исходный Council.analyze | C03: model-selected typed action и зарегистрированный dispatch |
| A06 / P2 | Нет измеренного evidence целевого масштаба | прежние проверки используют маленький мок | C06: 1200 документов/300 заметок, gold hits, шум, bytes/time/memory |
| A07 / P2 | Отчёт смешивает пользовательский совет и точный JSON | council/report.py | C05: план, риски, пять вкладов; точная версия в trace |
| A08 / P2 | Нет отдельного future-раздела и актуального корневого входа | council/README.md; root README | C05: запуск, схема, rationale, развитие |

| Требование | Состояние baseline | Корректирующая задача / критерий |
| --- | --- | --- |
| FR-1 | Пять frozen personas; живое совместное качество не подтверждено | C04/C06: различимые принципы, аргументы и контраргументы всех пяти |
| FR-2 | LangGraph protocol проверен fixtures | C05/C06: общий результат отражает все пять позиций и несогласие |
| FR-3 | CLI реализован; полный model run failed | C04/C06: один неизменённый входной промт → полезный полный отчёт |
| FR-4 | BM25+dense+RRF, bounded context | C06: 1200 документов без переноса всего корпуса в LLM |
| FR-5 | Источники индексируются, note fallback допускает шум | C02/C06: фильтр shortlist, all-noise и mixed случаи |
| FR-6 | Профиль/financial/goals pinned | C06: факты и ограничения цитируются без выдумывания |
| FR-7 | Hierarchical API wrapper есть только при preparation | C03/C06: три read tools доступны пяти агентам, фактический выбор tool |
| FR-8 | StateGraph с fan-out/fan-in и revision loop | C03/C06: explicit bounded tool dispatch и сохранение координации |
| FR-9 | Ограничения описаны, отдельного future-раздела нет | C05: roadmap без заявления нереализованных возможностей |

Маршрут: C01 документы → C02 отбор → C03 tools → C04 repair → C05 report/README → C06 scale/full pytest/live → независимое review → пользовательская приёмка. Один root implementer; независимый reviewer проверяет дизайн/результат, не меняет implementation files. Нового стека, API записи, БД или дополнительных runtime персон нет.

Live: максимум три полных запуска; повтор только после конкретной установленной ошибки и исправления. Дополнительные note/tool/repair модельные вызовы входят в max50 attempts/600s; каждый operation max2 attempts, tool loop≤3 на консультанта, API calls≤100. DTO/quotes/digests/consensus guards и 32768-byte/2000-output defaults сохраняются. Нехватка контракта/бюджета — blocker, а не повод ослабить проверки. При трёх неуспехах исходное задание не принимается.

Итоговое состояние: C01–C05 implemented; design/plan PASS и C-R01 closure PASS. C06 offline/scale PASS, live3/3 исчерпаны без полного решения; original-product acceptance BLOCKED/pending. Текущие подробности и новые A09 ниже. Ниже сохранён исходный обзор как исторический материал. Его заявления об отсутствии Git, обязательности Tasker и LangGraph, числе traces и текущих тестах заменены актуальным аудитом выше.

## C06 actual evidence / checkpoint

- Scale PASS: council/output/scale-465e90dacfd54ddc9dc6d20f9d03791c; 1200documents/300notes, real dense/scripted filter; all explicit gold positive/negative hits, no selected synthetic noise. Serialized request28581bytes; cached index/query measurement13.085s; sampled peak parent136331264/tree650608640bytes (~620MiB). This is a representative synthetic case, not a production SLA or live semantic filter proof. Initial failed measurements retained.
- Live1/3: council/output/ec65ba6a1f88475780cdecc8881f4ee6, incomplete complete-serialized-request byte budget;10attempts, five actual selected snapshot tool dispatches,0positions/decisions. Note filter selected15/20. Known reported cost2.11rubles, four unknown cancelled usage rows; no claim of full cost. Cause established: tool instruction appended after sizing + duplicate tool evidence. Fixed: instruction in measured payload, tool results reference evidence IDs instead of duplicating chunks; no numerical budget increase.
- Additional300-note deterministic regression revealed tied dense rankings bury lexical signals. Corrected separate lexical lane≤5 within existing20 shortlist. New fullcheck and measured repeat pending; live2 only after concrete repair verification. Current-profile remains unchanged. Full-product acceptance pending.

## C06 scale / live2 checkpoint

Final scale after lexical-lane fix PASS: council/output/scale-8a171828a65a401294a68e340464512b; real dense,1200docs/300notes, both gold positive/negative documents and notes visible, no synthetic selected noise. Request28718bytes,17.270s cached preparation/query, sampled parent137252864/tree649621504bytes. Filter is explicitly scripted and does not certify live classification quality. Measurement source in council/output/scale-measurement-20261009/run.py; psutil7.2.2 is measurement-only.

Live2/3: council/output/e7af238a4d1d48bdb83af33a1079ea4d → incomplete pinned closure. Five valid positions committed,13 actual model-selected Tasker dispatches,22 attempts,0decisions,46.079s. Known reported cost9.67rubles, no unknown usage in this run. Safe repair fixed Taleb nonexact citation on second attempt. Exact offline size diagnosis from frozen positions with no optional context:37228bytes(pos14058,evidence12303,frameworks1733,schema3342); exceeds32768. Current fix omits only unused evidence hash/offset audit metadata from model input and duplicate coordinator persona descriptions. Full source texts/positions and immutable registry/trace/citation/digest guards retained, each initial/review advisor still receives its complete frozen framework. No numerical budget change. Last fullpaid run3 follows current full check and independent context-review. Product acceptance still pending.

## Итог выполнения C01–C06 / 2026-10-09

C01–C05 реализованы локально, без Git-коммита. Пользовательский `user_prompt` в main.py повторно сравнен AST с HEAD council/: совпадает. `.env`, модель, исходные persona/data файлы не менялись. Совместное выполнение по всем FR пока не принято: C06 исчерпал разрешённые три живые попытки без проекта решения.

### Последняя проверка и масштаб

Точная команда: `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q` → **133 passed in 12.94s, exit0**. Проверены полностью шумные/смешанные300 заметок, пустые задачи/подзадачи, API errors, неизвестные ID/write operations, отдельный inventory/detail scope, bounded tool loop, repair identities и transitive evidence pinning. Новые проверки измеряют риски корректирующего плана; исторические результаты не заменяют текущий full suite.

Команда измерения: `.\.venv-consensus\Scripts\python.exe -m council.output.scale-measurement-20261009.run` → **PASS, exit0**. [Metadata](../council/output/scale-73855c2e7c4f4bcea3cd24ea77966fd4/metadata.json): 1200 документов,300 заметок,1756 фрагментов. Положительные и отрицательные gold-документы/заметки найдены и показаны; selected synthetic noise=0; shortlist≤20. Полный serialized request=**22 906 байт≤32768**. Cached preparation/query=14.713s; sampled peak parent135946240/tree650575872bytes (~620.4MiB), interval0.1s. Корпус синтетический, dense encoder настоящий, note-filter scripted: это воспроизводимое доказательство выборки/размера, не live semantic classifier certification или production SLA. Ранние неуспешные измерения сохранены выше.

### Три разрешённых полных живых запуска

Одинаковая команда из корня: `.\.venv-consensus\Scripts\python.exe -X utf8 -m council.main --mode model --reasoning-effort none --aitunnel-test-mode`. Исходный вопрос/досье/AI Tunnel/gpt-6-luna-pro сохранены. Явный ранее принятый test-only gateway profile запрашивает2000 и допускает reported≤8000; строгий production default не менялся. Любой дополнительный note/tool/repair вызов включён в общие attempts/usage.

| Запуск / trace | Результат и причина | Attempts / snapshot dispatch | Зафиксированные позиции / решения | Время / известный расход |
| --- | --- | --- | --- | --- |
| [1 / ec65ba6](../council/output/ec65ba6a1f88475780cdecc8881f4ee6/trace.json) | incomplete: complete serialized request byte budget; исправлены post-sizing tool metadata и duplicate evidence |10 /5|0 /0|22.808s;2.11руб subtotal,4unknown rows|
| [2 / e7af238](../council/output/e7af238a4d1d48bdb83af33a1079ea4d/trace.json) | incomplete: pinned closure; без optional37228bytes; исправлена только audit metadata/duplicate coordinator frameworks projection |22 /13|5 /0|46.079s;9.67руб,0unknown rows|
| [3 / 1100b8f](../council/output/1100b8f39a594601af28e5fa7ccd25ba/trace.json) | failed: Buffett2×citation_quote_not_exact; Reich первая quote invalid,repair отменён после barrier failure |23 /11|0 /0(3individual initial accepted)|38.597s;7.05руб subtotal,1unknown row|

Последняя попытка содержит notes1/tools15/initial7 операций; requests≤29952bytes,22 фактических Tasker API вызова подготовки и11 обращений консультантов к неизменному снимку учтены отдельно. Safe repair получил новый request ID и те же источники/вопрос/версию. Автоматической подмены цитат/валидации/согласия нет. Атомарный этап правильно не коммитит три частичных ответа как пять позиций. Отчёт3 является диагностикой **failed**, не полезным no_consensus. Суммарный **известный subtotal18.83руб**, пять usage rows неизвестны: это не полный денежный итог. Четвёртая платная попытка не выполнялась.

### Замечания после реализации

| ID / приоритет | Итог и доказательство | Статус / задача |
| --- | --- | --- |
| A01 / P1 | В live2 есть5positions, во всех трёх нет проекта/голосов | OPEN; C06 full-result acceptance blocked |
| A02 / P2 | Актуальные r9 headers, route и схемы обновлены; прежние записи под историей | CLOSED C01 |
| A03 / P2 | FR-7/FR-8 явно обязательны в аудите/README | CLOSED C01/C03 |
| A04 / P2 | Нет forced note fallback; bounded filter/empty/mixed/allnoise tests | CLOSED code C02; live precision отдельный evidence, не гарантия |
| A05 / P2 | Все5 выбирали Tasker action; live3 11scoped dispatch,22API calls; inventory/details отделены | CLOSED C03; independent C-R01 closure |
| A06 / P2 | Измерение1200/300 PASS,bytes/time/memory/gold/noise зафиксированы | CLOSED C06 representative scope; production/live-filter SLA не заявлен |
| A07 / P2 | Renderer выводит recommendation/steps/risks/missing/five positions; технический JSON в trace | CLOSED C05 implementation; полный live отчёт блокирует A01 |
| A08 / P2 | README отдельные rationale/future и актуальная схема; root вход | CLOSED C05 |
| A09 / P1 | live3 Buffett нарушает точную цитату на обеих attempts несмотря на code-only safe repair | OPEN C04-R1 (следующее согласование): диагностировать/улучшить протокол выбора и repair точной цитаты в том же frozen evidence и бюджете, не нормализовать неподходящий quote и не ослаблять guard; независимое review и новая разрешённая live-проверка до закрытия |

### FR-1–FR-9: фактическая приёмка

| FR | Реализовано и проверено | Оставшийся критерий |
| --- | --- | --- |
| FR-1 |5frozen frameworks+distinct voices; live2 five valid cited positions,28citations independently verified|Контраст практических вкладов полного обсуждения не подтверждён; схожий conservative совет noted reviewer|
| FR-2 |LangGraph fan-out/barrier,draft/review/revision guards проверены fixtures|Полный живой проект учитывает все5 и даёт полезный consensus/no_consensus|
| FR-3 |Один неизменённый prompt,CLI,readable report+trace|Завершённый live результат вместо diagnosticfailed|
| FR-4 |BM25+dense+RRF;1200docs representative PASS;≤32768bytes|Production recall/SLA требуют отдельного развития, не входят в текущий measured scope|
| FR-5 |Shortlist≤20,model-filter1bounded operation;zero-relevant valid;allnoise/mixed300 regressions|Live note relevance quality на размеченной выборке не сертифицировано|
| FR-6 |Frozen structured KB,pinnedprofile/financial/goals;live2 supported42k/35k/~6h citations audited|Поддержка фактов итогового решения не проверена, потому что его нет|
| FR-7 |get_tasks/details/subtasks typed wrapper,snapshot provenance;all5actual selections;no writes/unknownID|Implementation/evidence criterion закрыт;final user acceptance pending|
| FR-8 |StateGraph explicit control,coordination,tools,barrier/versioned guards|Actual live draft/review cycle не достигнут|
| FR-9 |README rationale,diagram,separate development section|Documentary criterion закрыт;final user acceptance pending|

Независимые design/plan, inventory correction, compact context/repair и persona-policy review PASS. [Финальное review](agent-base/features/multi-agent-consensus/handoffs/corrective-review/result.md) разделяет code readiness и BLOCKED полное живое выполнение. Историческое15 accepted scripted остаётся в силе; отдельное15 исходного задания открыто. Новый план/платный лимит не согласованы и автоматически не начаты.

## Исторический обзор до корректирующего маршрута

Дата: 9 октября 2026 года. Проверена текущая реализация `council/`, тесты и сохранённые отчёты. Код и исходный промт не менялись. Новые платные запросы к модели не выполнялись.

**Моя оценка: около 5/10 за готовность к сдаче; около 8/10 за инженерную проработку протокола. Главная задача пока не продемонстрирована: нет сохранённого успешного полного ответа реальной модели, в котором совместно участвуют все пять консультантов.** Это экспертная оценка, а не балл по неизвестной шкале интервьюера.

## Что подтверждено

- Команда `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q` выполнена сейчас: **123 passed in 20.18s**, exit 0. Включены проверки протокола, источников, контекста, провайдеров и dense-интеграции.
- В `council/output/*/trace.json` найдены **пять полных запусков в режиме model; все failed**, без зафиксированного набора пяти позиций и без проекта решения. Есть ещё две отдельные диагностики позиции, которые не исполняют весь совет. Это выборка сохранённых артефактов, а не оценка вероятности успеха будущих запусков.
- Сценарные прогоны показывают consensus, пересмотр и no_consensus. Они проверяют переходы состояния и защиты, но ответы в них заранее написаны.
- В `main.py:26` присутствует исходный вопрос о переходе из mechanical engineering в software development. В этой проверке он не менялся. Историческую неизменность без исходного эталона или истории версий подтвердить нельзя: рабочая папка не является Git-репозиторием.

## 1. Координация консультантов — сильная часть, ориентировочно 8/10

В `runtime.py:359` пять участников независимо формируют исходные позиции. Они не видят ответы соседей на этом этапе. Координатор получает все позиции и создаёт общую версию; затем каждый консультант проверяет её по своим критериям. При возражениях запускается следующий раунд, при исчерпании лимита сохраняется несогласие. Это настоящее проектирование координации, а не пять независимых ответов, склеенных в конце.

Особенно хорошо сделаны фиксация версии и digest, проверка полного состава участников, принадлежности проверок и возражений, сохранение конфликтующих источников и запрет координатору самостоятельно закрывать чужие возражения. Переход в consensus разрешает код. Есть ограничения числа раундов, попыток и времени.

Выбранная схема «независимые позиции → синтез → независимая критика → пересмотр» подходит кейсу. Свободный чат между пятью агентами для выполнения задания не обязателен. Отдельный координатор допустим: он выполняет синтез и не получает шестого голоса.

Компромиссы: единогласие строже, чем требуется в описании. Все пять точек зрения могут быть видны и в полезном результате с явно сохранённым несогласием. Один и тот же провайдер/модель для всех ролей оставляет коррелированные ошибки; количество голосов не превращает вывод в истину. Наконец, схема пока не подтверждена полным живым обсуждением.

## 2. Источники данных — хорошая база, ориентировочно 7/10

Профиль, корпус и заметки действительно загружаются. Работает гибридный поиск: BM25, настоящие Sentence Transformers embeddings и объединение рангов RRF. Есть кэш, разбиение с точными offsets и проверкой отсутствия потерянных хвостов, происхождение цитат и ограничение размера полного запроса. Цели, ограничения и финансовый раздел профиля закрепляются в контексте. Это разумнее передачи всех документов каждому консультанту.

Есть три существенные границы:

1. `context.py:8` проверяет точное присутствие цитаты в показанном фрагменте, но не доказывает, что цитата поддерживает утверждение. В успешном сценарном trace `503065c89aad42c8845528d8c8279d8c` все пять участников цитируют только `## goals\r\n\r\n` — заголовок без факта. Это наглядная граница формальной проверки, а не доказательство такого поведения живой модели.
2. `context.py:37` требует хотя бы один фрагмент каждой категории, включая заметки, и при необходимости берёт первый доступный. Dense-поиск не имеет порога релевантности. Поэтому полностью шумный набор заметок всё равно попадёт в контекст. Текущий кейс не доказывает качество отбора на 300 заметках.
3. Tasker и подзадачи обязательны в `sources.py:104` и при построении контекста. В данном сообщении пользователя такого источника нет. Он присутствует в локальном `council/task.md`, поэтому это не произвольное добавление; но при оценке именно предоставленного описания лишняя обязательная зависимость снижает переносимость. Не следует штрафовать за отсутствие agent tool-calling или требовать Tasker как условие этого кейса.

## 3. Качество итогового ответа — главный незакрытый пункт, ориентировочно 2/10

Транспорт реальной модели реализован: `providers.py` поддерживает AI Tunnel и OpenAI. Поэтому старое утверждение «адаптера нет» уже неверно. Однако подключения и отдельных валидных ответов недостаточно для сдачи.

Последний сохранённый полный model trace `f03b53115da344e7a308909e9a7ea15a` завершился failed: Peter Thiel и Warren Buffett дали индивидуально принятые ответы, Robert Reich исчерпал попытки после ValueError, оставшиеся запросы отменены. Пять позиций коммитятся только после общего барьера, поэтому в состоянии совета осталось 0 позиций и 0 решений. **Это не no_consensus: содержательное обсуждение ещё не началось.** Точную причину старого ValueError восстановить нельзя, поскольку этот trace не сохранял нужной детализации. Текущий код диагностики улучшен, но старую причину это не доказывает.

В строгих предыдущих прогонах отказ происходил и по превышению лимита ответа. Даже разрешённый тестовый потолок 8000 при запрошенных 2000 не обеспечил полный результат. Вывод: настройки, размер обязательного JSON и стратегия повторов пока не подтверждены как надёжный совместный контракт с выбранной моделью.

Рабочий scripted-ответ слишком общий: «проверить переход без немедленного увольнения», уточнить расходы и сделать проект. Пять рекомендаций различаются короткими готовыми фразами, но аргументы одинаковы, а draft берёт аргумент первой позиции (`scripted.py`). Это нормальный fixture для тестов. Выдавать его за выполнение задачи AI-советом нельзя.

Для убедительной сдачи нужен живой единый ответ, использующий конкретику Марка: $42 тыс. накоплений, $14 тыс. стоимости обучения, доходы, ипотеку, ребёнка, время и тревоги семьи; проверяющий перенос инженерного опыта в software; различающий удовольствие от хобби и работу разработчиком. Должно быть видно, что именно каждый из пяти взглядов внёс в общий план, какие предположения остались и что нужно проверить до увольнения. Это описание ожидаемой глубины, а не заранее предписанный «правильный» карьерный совет.

## 4. Код — ориентировочно 8/10

Сильные стороны: разделены источники, retrieval, контекст, провайдеры, схемы и runtime; строгие DTO; проверяемые переходы; контролируемые повторы и отмена; trace, расходы и отчёт; существенные отрицательные сценарии в тестах. Текущие 123 теста прошли.

Ограничения: почти весь протокол сосредоточен в большом `Council`; `GraphState` содержит только `next`, а позиции, голоса и версии хранятся в mutable `self`. LangGraph реально исполняет workflow, но его возможности хранения и восстановления состояния здесь почти не используются. Для локального прототипа это допустимо; после перезапуска полноценное продолжение обсуждения не реализовано.

Markdown-отчёт содержит большой JSON точной версии. Это полезно для аудита, но пользовательский совет приходится извлекать из технического вывода. Стоит отдельно показывать читабельный план и вклад пяти взглядов, сохраняя точную проверенную версию в trace. Большое количество документации и guards заслуживает внимания, но не компенсирует отсутствие работающего основного сценария.

## 5. Масштаб 1000+ документов и устная защита

Для такой задачи выбранный LangGraph объясним явными стадиями и циклом пересмотра. По текущему коду честное обоснование должно признавать, что тот же bounded workflow можно выразить обычным async Python; преимущества восстановления состояния понадобятся после переноса состояния внутрь графа. Фреймворк не является самостоятельным критерием успеха в предоставленном описании.

RAG уже отделяет размер корпуса от размера запроса к LLM, но **1000+ документов не проверены нагрузкой**. Сейчас источники и векторы материализуются целиком, similarity считается Python-циклом по всем векторам, обмен с worker использует JSON. Вызов query worker снова загружает encoder. Бюджет запроса 32 KiB включает схемы, пять позиций, решение и историю: pinned-материал может переполнить его даже при небольшом корпусе.

На защите достаточно последовательно объяснить: предварительная и инкрементальная индексация; измерение recall и шума на размеченных запросах; векторизованный/индексный поиск при измеренной необходимости; хранение provenance и версий; управление растущим контекстом; восстановление обсуждения; измерение задержки, стоимости и качества итогов. Внешняя векторная БД не обязательна только из-за числа 1000. Это направления развития, а не реализованные возможности.

Фактическую устную защиту на 5–10 минут по коду оценить нельзя. Документы показывают понимание многих компромиссов, но не доказывают, что кандидат способен ясно объяснить их устно.

## 6. Использование AI во время сессии

В проекте есть routing, handoffs и записи независимых проверок: видны следы организованной работы с AI. Но файлы не заменяют наблюдение самой сессии. Без её истории нельзя достоверно оценить качество запросов кандидата к AI, проверку сгенерированного кода и самостоятельность решений. Этот критерий оставлен **неоценённым**, а не засчитан как провал.

## Что важнее исправить перед сдачей

1. Получить один успешный полный живой прогон исходного вопроса с пятью позициями и одним полезным итогом. Consensus не обязателен: допустим общий результат с честным несогласием.
2. На этом результате проверить персонализацию, смысловую поддержку цитат и видимый вклад каждого консультанта. Тесты fixtures сохранить как проверку протокола.
3. Согласовать размеры ответа/схем и подход к repair с реальной моделью; измерить надёжность на нескольких содержательных вариантах кейса, а не только повторять транспортные smoke-проверки.
4. Подготовить краткую устную защиту координации, единогласия, общего контекста, ограничений retrieval и пути к 1000+ документам.

**Вердикт:** сильный прототип инфраструктуры обсуждения, но пока неполная реализация задачи по результату. На интервью основное преимущество — грамотный протокол; основной риск — продемонстрировать тестовый consensus вместо работающего совета.
