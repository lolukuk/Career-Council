# Решения и согласования

- D01 / 2026-10-08 / accepted: требования и рекомендуемый стек. Источник — прямой ответ пользователя «Согласую» на совместный gate. Scope: Python, LangGraph, Pydantic, BM25 + Sentence Transformers, pytest, CLI/local artifacts, read-only tasker.
- D02 / design r1 / proposed: фиксированный workflow вместо свободного supervisor. Модель не выбирает следующий узел и не объявляет terminal state.
- D03 / design r1 / proposed: ровно пять голосующих персон; координатор синтеза без голоса. Общий LLM допустим, но корреляция ошибок раскрывается и оценивается.
- D04 / design r1 / proposed: provider-neutral ModelAdapter; live provider/model/SDK unknown. Не добавлять SDK и не объявлять live-качество проверенным до конфигурации. Реальные embeddings — Sentence Transformers; model ID выбирается под язык досье при реализации и фиксируется в manifest.
- D08 / 2026-10-08 / accepted: пользователь ответил «Провайдера выберу позже» на вопрос live-конфигурации. Провайдер/модель/SDK не выбираются сейчас; разрешённая работа по дизайну/сценариям продолжается. Это не отказ от будущего real-model режима и не подтверждение live-quality.
- D05 / design r1 / proposed: компактные позиции и objection ledger вместо общей растущей истории. Обязательное содержание не обрезается молча.
- D06 / design r1 / proposed: JSON-трасса/Markdown-отчёт без crash recovery, DB, distributed workers и UI.
- D07 / design r1 / proposed: структурный guard не доказывает semantic truth; это ограничение раскрывается пользователю.
- D09 / design r2 / reviewed, pending user approval: каждый исторический blocker/Conflict перепроверяется владельцем на каждой версии, permanent retirement отсутствует; transitive evidence closure сохраняет основания. Whole-payload reviewer assessment и typed claim/caveat references закрывают обход assertions через narration. Исходный review r1 blocked (F01–F06); независимый closure r2 pass, все findings closed. Документальная проверка не означает исполненный/качественный live-прототип.

Design approval, execution approval и финальная приёмка не получены. Независимый review не заменяет пользовательское согласование.
Историческое состояние предыдущей строки: до gate06. Текущее согласование см. D13 ниже; execution approval и финальная приёмка пока не получены.

- D10 / 2026-10-08 / explicit user requirement: состав/persona descriptions берутся из council/data/personas.md — Peter Thiel, Warren Buffett, Robert Reich, Nassim Nicholas Taleb, Marcus Aurelius. Design r3 заменяет прежние fictional profiles, sets IDs, prompting/retrieval aspects и scenario owners; roster заморожен в run config и не является evidence о пользователе. Core consensus protocol без изменений; focused independent review требуется до gate06.
- D11 / 2026-10-08 / accepted clarification: локальный текст human mediator сохранён; на вопрос о scope пользователь ответил «Человек принимает итоговое решение». Human decision — после отчёта вне agent loop, не persona vote и не изменение consensus status. Интерактивное вмешательство между раундами не требуется; budgets сохраняются. Дополнительный runtime node/agent не вводится.
- D12 / design r3 / reviewed pending design approval: persona delta independently passed, outdated requirement sentence F07 corrected/closed; F08 human scope independently closed по прямому ответу пользователя. Final documentary r3 pass, F01–F08 closed. Это не design approval пользователя, не product/live evidence.
- D13 / 2026-10-08 / accepted: прямое «Утверждаю» в ответ на gate06 design r3. Разрешён переход к плану минимального прототипа и проверок; стек и scope прежние, provider later. Конкретный execution plan проходит самостоятельный quality/user gate по выбранному framework; этот новый план ещё не предъявлялся.
- D14 / implementation p2 / proposed: independent p1 review blocked P09–P11; устранён I03↔14 cycle, E05 runtime проверка закреплена за I02, corrections14 возвращаются в affected leaf с dependent rechecks. Code-ready/reviewed/user-accepted раздельны. Corrections ожидают independent closure; execution approval отсутствует.


- D15 / implementation p2 / independently reviewed: closure PASS, P09–P11 closed. Routing09 acyclic, root engineer profile и assignments I01/I02/I03 материализованы для preview10. Один исполнитель, existing independent reviewer; код/зависимости/tests/dense/native/live не запускались. Следующий gate11 — user execution approval; user acceptance15 отдельно.

- D16 / 2026-10-08 / accepted: пользователь ответил «Утверждаю» на конкретный reviewed execution plan p2. Gate11 закрыт; I01→I02→I03 разрешены. Provider/live-quality остаются позже; приёмка15 отдельно.

- D17 / adaptive r7 / bounded author repair: independent actual14 blocked R12–R14; no scope/stack/team/provider change. Root routed I01/I02 schema/check reasoning, expired attempt cleanup and shared native-query deadline fixes, dependent regression I03. User execution11 authorizes necessary fixes; acceptance15 remains pending. Original findings/evidence preserved.

- D18 / 2026-10-08 / independently reviewed final PASS: R12–R15 closed, original blocked/evidence preserved. Current54 tests exit0; agree/revise/disagree actual-dossier demos exit0; actual embeddings/native deadline/cancel proven within documented fixture scope. User15 acceptance waiting; live provider/semantic quality unconfigured/unrun. Author source files/personas/tasker/original question preserved.

- D19 / 2026-10-08 / accepted: прямое «Принимаю» закрывает gate15. Утверждённый scope прототипа завершён, independent14 PASS/R12–R15 closed и фактическое evidence сохраняются. Live provider/model quality остаются unconfigured/unrun; приёмка не запускает новый live этап автоматически.

- D20 / 2026-10-09 / explicit user scope: evaluation r4 — архитектурный offline eval без текущих live LLM tests. Four levels, trace cases, E01–E12/evidence, metrics/oracles и scoring rubric. Runtime/design r3/accepted product unchanged; new tests/provider/SDK/calls не вводятся. EV02 focused documentary review uses existing reviewer; prior54 evidence dated2026-10-08 preserved.

- D21 / 2026-10-09 / documentary reviewed PASS: evaluation r4 architecture/offline scope independently checked; T6 evidence attribution corrected, no open findings. EV01/EV02 done, no current live/tests/CLI/model runs. Product acceptance15 preserved, no SDK/provider/runtime change.
