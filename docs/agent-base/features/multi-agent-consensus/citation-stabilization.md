# C04-R1 / r10 — стабилизация выбора цитат

## Разрешение следующего one-run R2e

Пользователь явно ответил «Разрешаю ещё один запуск» после конкретного c4/caveat diagnosis, full159passed48.44s и independent actual49focused15.51s/PASS WITH RISK. Новый отдельный лимит1, предыдущий extra1/1 и исходный additional3/3 не сбрасываются. R2e live starts, outcome unknown; любой повтор после этого одного требует нового разрешения и установленной причины/исправления.

## Дополнительное разрешение после R2d

Пользователь явно разрешил **ещё один полный платный запуск**, ответ: «Разрешаю ещё один запуск». Это отдельный лимит1, прежние новые3/3 остаются исчерпанными. Gate: exact full154passed58.87s exit0 и independent latest delta PASS WITH RISK/own34focused6.77s. Запуск R2d начинается с unchanged input/model/provider/personas/config; после него дополнительный лимит1/1, автоматического повтора нет. Полный outcome ещё unknown.

Продолжение r9, 2026-10-09; исходные FR-1–FR-9, стек, пять персон, вопрос, provider/model и числовые лимиты сохраняются. Текущий пользователь явно поручил диагностику, выбор минимального решения, реализацию и проверки до следующего платного запуска. Старый лимит C06 3/3 исчерпан; новый количественный бюджет платных попыток не задан. Работа и независимые reviews разрешены текущим поручением; платные вызовы пока не выполняются.

## Диагноз и альтернативы

Trace ec65ba6: request overflow, 0 positions; e7af238: pinned closure overflow, 5 positions, 0 decisions; 1100b8f: Buffett дважды quote_not_exact, Reich один раз, 3 индивидуальных accepted, 0 атомарных positions/decisions. Тексты отклонённых ответов намеренно не сохранялись: точную ошибочную строку восстановить из trace нельзя. Доказанный дефект контракта: свободное воспроизведение <=400 символов из исходного Markdown/JSON с CRLF, экранированием и форматированием. Repair содержит лишь stage/code, без пути к ошибке и способов выбора. DTO строго локальный; transport schema передаёт bounds как descriptions, а не гарантированное исполнение провайдером.

| Альтернатива | Оценка |
| --- | --- |
| Только усилить инструкции копирования | Уже не помогло live3; оставляет генерацию символов |
| Добавить допустимые цитаты, сохранить свободный quote | Дублирует контекст, та же ошибка копирования |
| Выбрать ID заранее выделенного фрагмента | Выбрано: детерминированное разрешение, меньше output JSON, точный provenance |
| Восстановить quote по похожему тексту | Запрещено: подмена исходного выбора |
| Новый сервис или дополнительный semantic judge | Не нужен для ошибки копирования; меняет calls/infra |

Фрагменты режутся детерминированно из frozen chunk.text по абзацам/границам слов, <=400 символов. ID связывает chunk и точные start/end. В citation-bearing requests evidence.text проецируется в список selectable excerpts без дублирования текста; output Citation содержит только evidence_id. Backend разрешает только ID из показанного пакета, сверяет digest/исходный текст, строит прежний Citation(chunk_id,quote) и выполняет неизменную строгую валидацию DTO, quotes и протокола. Прежние exact DTO/trace/report сохраняются. Raw quote не принимается как fallback. Никакой поиск похожей цитаты, нормализация или автоматическое решение за модель.

Точность текста не доказывает релевантность: persona должна выбирать фрагмент, прямо поддерживающий конкретный факт; inference отделяется как assumption. Координатор сохраняет пять вкладов, все консультанты проверяют semantic support каждого claim и всего текста; unsupported запрещает consensus. Это не универсальная детерминированная гарантия entailment.

Repair: прежние max2 attempts; fresh identity, те же frozen evidence/question/version; безопасный путь ошибочного citation, конкретная фиксированная инструкция и ограниченный список ID уже показанных фрагментов. Ошибочный raw output/exception text не сохраняется. Все проекции входят в измерение request; max32768/2000/50/600 неизменны. Barrier остаётся атомарным: failed advisor не заменяется фиктивным голосом.

## Маршрут и проверки

R1 diagnosis/design → independent design/plan review → R2 selection boundary/context/prompt → R3 existing full pytest + evidence-ID/exact-quote/repair/semantic refusal cases → independent final review → новый live budget / полный результат → 15 user acceptance. Автор root; reviewer по существующему skils/consensus-protocol-reviewer.md, код read-only, exclusive output handoffs/citation-review/. Без commit и новых сервисов.

Команда обязательного full check: `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q`. Дополнительно offline воспроизведение сохранённых пяти позиций live2 через текущую context sizing, без вызова провайдера. Проверить draft/review growth, доступность evidence, strict structured-output conversion, fresh repair и semantic unsupported guard. Ни scripted checks, ни code PASS не заменяют полный live report.

Состояние: diagnosis/design готов; independent review pending, implementation pending. Фактическая текущая suite будет записана после выполнения.

## Реализованный boundary и исправления sizing

Сохранённые live2 позиции выявили overflow после первой ID-проекции и после source dedup: проверки не выдавались за PASS. Альтернатива увеличению caps — lossless сериализация: citations в model input заменяются exact span-ID, source origin/location вынесены один раз на source_id, schema title/default annotations убраны (все types/required/nullability/bounds сохранены, DTO defaults остаются локально). Internal DTO/trace/digest не переписываются. Все символы chunk.text, включая CRLF/пробелы, сохранены в последовательности excerpts; любой audit span восстановим из показанных текстов и offsets. Audit span не автоматически selectable: output resolver принимает только перечисленные excerpt IDs.

Mandatory category уже удовлетворён цитированным profile/document chunk: дополнительный произвольный chunk той же категории не дублируется. Optional RAG slots резервируют1024bytes для repair; mandatory closure по-прежнему проверяется по полному32768byte guard. Если обязательный пакет помещается, но repair нет — завершение incomplete, не обход лимита. Длинные historical позиции показывают малый headroom; новый ID output и brief stage hints уменьшают эту стоимость, без гарантии вместимости любой максимальной DTO/ledger.

Baseline133passed; первый post-change144passed. Следующий full1failed/144passed из-за source_id в новой test fixture, затем исправление. Финальная suite pending. Новая пользовательская авторизация: до3 полных paid, только после full suite/independent review; повтор только concrete cause+fix. Точные модели и исходный input не изменяются.

## Offline gate / actual evidence

Финальный на тот момент full145passed29.52s exit0; новый boundary/source_id assertion и metadata-only delta требуют свежего full check (running). [Измерение](citation-sizing.json) воспроизводит именно saved live2 пять больших позиций, proposal scripted только для sizing: draft31719bytes; пять reviews32491–32661bytes≤32768. Repair на таком тяжёлом historical review33116–33286bytes превышает cap и будет отказан до dispatch; это сохранённый budget risk, не успешный repair и не причина увеличить лимит. Сначала не помещались обе проекции; lossless dedup, schema annotations и mandatory category reuse дали первый admissible пакет. Новые ID outputs должны быть короче, но это ещё не live evidence. Максимальные DTO/ledger по-прежнему могут завершить incomplete. Начальный review проверяет outcome/dissent как прежде.

Все quote whitespace/CRLF сохранены без нормализации; exact span audit references восстановимы из показанного текста. Output принимает только IDs с явным selectable entry, source_id/digest/текст/видимость сверяются. Schema repair дополнительно включает только schema-trusted paths без inputs/messages. Pure copied quote fallback запрещён.

### Pre-paid final offline gate

Точная команда `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q`: **146 passed in29.58s, exit0**. Проверки включают valid/invalid/unshown/tampered IDs, source identity/digest, exact/nonexact quotes, Unicode/CRLF/JSON и lossless segmentation, raw-quote fallback refusal, wire schema/internal DTO defaults, safe targeted repair, actual selected offset при identical source paragraphs и semantic unsupported refusal. Reviewer CIT-F01 initial finding сохранён: reverse lookup по равному quote мог записать два ID вместо выбранного одного; исправлен accumulator validated raw selections, regression включён.

Original user_prompt AST сравнен с Git HEAD: совпадает. Initial packets из saved live2 tool/evidence state29420–31188bytes; targeted repair30040–31808≤32768. Сохранённые большие пять позиций: draft31719, reviews32491–32661; historical reviewrepair overflow33116–33286 сохранён как fail-before-dispatch risk. [Полные числа](citation-sizing.json). Нет оплаченных вызовов на стадии sizing; scripted proposal используется исключительно для измерения формы review, не для product result. Independent final review gate выполняется, paid0/3.

## Live1 / correction R2b

Новый live1 f0f30579d55e457983f456670a7a58a7 FAILED:25 attempts (notes1/tools15/initial9), три individual accepted,0 atomic positions/decisions,50.025s; known8.75rub subtotal/1unknown usage. Buffett/Marcus исправили выбор на repair; Reich дважды citation_selection_not_shown, Taleb repair отменён после barrier failure. Точное ошибочное ID отсутствует в trace: гипотеза вычисления subspan по parseable range не объявляется доказанным фактом. Доказано нарушение request-local allow-list.

R2b: opaque stable q+12hex hash IDs из chunk/digest/exact start/end, collision failclosed через catalog; dynamic wire evidence_id.enum содержит все и только показанные варианты. Context candidate sizing и actual call используют одинаковую effective schema; review intersection строит enum заново. Unknown/raw-quote/digest guards сохранены. Unique exact retained citation переводится в q-ID; исторический/ambiguous quote имеет отдельный source_span marker, обозначающий точное записанное literal, не исходный selected model ID и не selectable entry. All text/CRLF сохраняется. Existing ScriptedAdapter обновлён только как protocol fixture, реальные выводы им не подменяются. Новый full/sizing/review до live2; paid1/3.

R2b full:148passed50.96s exit0. Перед этим27failed119passed30.69s из-за legacy scripted fixture lookup `.split(':')` после opaque-ID изменения; fixture исправлен, реальный результат не подменялся. [Actual v2 sizing](citation-sizing-v2.json): enum включён; initial30464–31572, historical pinned draft30684. Очень длинные old free-quote позиции продолжают budget stress в review; отказ guard сохранён. V2 генерирует exact predefined selections, для которых retained Citation компактен в input; фактическое полное выполнение ещё не подтверждено. Paid1/3, independent delta final review pending.

R2b actual independent delta code review PASS WITH RISK; reviewer own28focused passed2.75s. Additional real-dossier representative v2 sizing uses clearly synthetic5positions×3arguments/3criteria,3claims/3steps; draft31704, reviews31465–31635, repair32096–32266≤32768. Это shape/byte evidence, не полноценный model result. Старые свободные substring позиции дают review33057–33227; safe overflow negative retained. Current code unchanged since full148 exit0. Gate для разрешённого live2 пройден; live2 running, paid2/3 initiated, max3 remains.

## Live2 / final bounded corrective R2c

Live2 [465e5e84](../../../../council/output/465e5e84e42843c0aadc95d9a2a8e761/trace.json) INCOMPLETE:21attempts (notes1/tools14/initial5/draft1),5atomic positions/1decision/0votes,58.980s,7.21rub known/0unknown. **Ни одного quote/ID/schema/protocol rejection**. Citation defect removed on this live path; full product result still absent. Actual review projected14367bytes positions+5018decision+8411evidence; uncited personal tool-prefetch pinning added2.3–4.2k unnecessarily. Removing unused tools alone still gives38374–38544byte review; generation-count-only compact fixture likewise overflow. Failures preserved, no limits raised.

R2c selected minimal bounded correction:
- initial CompactPosition generation subset2arguments/1compoundcriterion, strict local validation before original Position normalization; fields/basis/citations/counterargument/unknowns remain;
- complete initial wire JSON≤1600UTF8bytes, a stricter stage envelope matching existing350visible-token objective; specific bounded repair, no truncation and no cap increase; envelope/schema digest included in frozen snapshot/trace;
- tool observations passed only in initial/tools; all actually cited tool sources remain transitive pinned;
- review owns full original criterion, peers share full recommendation/arguments/counterargument/conflicts/**missing_data**; only peer criterion bodies omitted, evaluated by each owner, consensus still requires all5;
- schema titles/default annotations/definition names deduplicated by aliases; all types/required/nullability/bounds and DTO default restoration unchanged.

Independent design rejects dropping peer missing_data (CIT-D03); that alternative was NOT implemented. One deciding criterion must contain every blocking condition; unknown/unmet clause forbids satisfied/approval. Accepted live2 positions/decision/ledger never rewritten into compact content.

Current exact full: **152passed100.33s exit0**. Includes compact-vs-original DTO strictness, uncited tool isolation/cited tool pin, full peer uncertainty/owner criterion retention, byte-specific fresh repair, aliases/enum equality/defaults and all prior invariants. [Compact sizing](citation-sizing-compact.json) is explicitly synthetic byte-only, carrying ALL ACTUAL live2 source citations plus UNCHANGED actual5claim/2caveat/4step proposal: new wire1118–1256≤1600, reviews29320–29497, repair29951–30128≤32768. These numbers are not new advisor reasoning or semantic proof. Earlier too-large compact fixture retained as failed approach. Actual independent final delta review pending; paid2/3, final permitted live3 awaits gate. General max DTO/ledger growth may still fail safely; no guarantee of fit or consensus.

R2c actual independent final review PASS WITH RISK, CIT-D03 closed; reviewer32focused passed4.40s. Full152author exit0 + byte-only source-footprint checks recorded separately. Final authorized paid3 starts; no guarantee of semantic success or consensus.


## R2d / окончательный фактический результат этого бюджета

Live3 `10556af0245c429fa1f0fafe16bf7ee9`: FAILED, 26attempts/53.655s, 0 atomic positions/decisions/votes. Пять initial first attempts и Reich repair отклонены по position_byte_budget; четыре peer repair отменены barrier. Известный subtotal7.20rub,4usageunknown; это не полный денежный расход. Вместе новые live1–3:23.16rub known subtotal,5unknown usage. Новые paid3/3; дополнительных вызовов нет.

Доказанная причина — несоответствие1600byte whole-wire envelope совокупным permissive generation bounds; сами поля могли быть формально валидны, но текст не укладывался. Точный raw reject отсутствует, поэтому конкретные длины полей и семантика не реконструируются. Production ProviderAdapter уже canonicalizes restore_defaults(json.loads(text)); whitespace-гипотеза исключена для этого AIT live. Дополнительная canonicalization нужна лишь для единообразия custom adapter контрактов.

Минимальный offline R2d: recommendation200chars, argument200/impact80, criterion240, counter240, missing3×100; cardinality citations и original DTO не сокращены. Whole1600 guard сохранён. При oversized ответа event/repair содержит только canonical initial_wire_bytes и размеры известных fields, actual/maximum bytes, конкретные prose targets. Raw text, unknown model keys и provider secrets не записываются; fresh attempt/request и исходный snapshot сохраняются. Политика прямо запрещает срезать значимые факты, поддержку, counterargument, unknowns, blocking clauses и conflicts. При невозможности поместить их — безопасный failure, не согласие. Schema-bound char count не является гарантией UTF8 bytes: разрешённые верхние границы в сумме всё ещё превышают1600; arbitrary max DTO/ledger может overflow. Поэтому данный delta — code correction с риском, не доказанная стабилизация live.

Добавлены regressions numeric safe repair, formatting invariance для custom adapters и generation-field bounds versus unchanged original positions. Первый новый full1failed153passed59.06s был ошибкой test assertion e['stage'] на guard event; исправлен на get. Свежая обязательная точная команда `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q`: **154passed58.87s exit0**. Independent actual latest delta **PASS WITH RISK**, own34focused6.77s exit0, без material code findings. Уже выполненные source identity/digest/valid-invalid-ID/exact-inexact-quote/semantic unsupported отказ cases остаются в полном наборе.

Сводка FR: фиксированная пятёрка, LangGraph independent initial/barriers/draft/review/revision, read-only Tasker, BM25+dense+RRF, frozen provenance/versions/bounds реализованы и offline проверены. Лучший новый live2 дал5atomicpositions+1draft и0citation/schema/protocol errors, но review не состоялся; новая wire selection устранила свободное воспроизведение цитат в том run. Live3 завершился до citation guard. Полезный полный отчёт с рассмотрением всех пяти позиций/рисков/несогласия не получен. Универсальная semantic entailment не доказана: backend проверяет точность/видимость, model review должен оценивать поддержку конкретного утверждения; fixture unsupported refusal не заменяет настоящую оценку смысла. FR-1/FR-2/FR-3 и полный FR-1–FR-9 outcome остаются открытыми.

Gates12/R2d done,13/offline done,14/code independent PASS WITH RISK;13/live и14/semantic BLOCKED3/3,15pending. Следующий полный оплаченный run требует нового явного бюджета и нового применимого gate. Нельзя объявлять successful consensus на основании этого work или synthetic sizing. Исходные accepted traces/positions и данные не переписаны; без commit/push/новых сервисов.


## r10 / R2e — текущий checkpoint после дополнительного live

Пользователь разрешил ещё один полный live после R2d; он выполнен, отдельный лимит **1/1 исчерпан**. Run `b8a17d9bdec54861882e922a0adc2cc3` FAILED:32attempts/66.695s, notes1/tools15/initial5/draft1/review10;5atomicpositions+1decision,0atomicvotes. Все5 initial приняты first try, exact ID/digest/quote/protocol guards passed, wire1218–1344bytes. Draft принят; все5 reviews first и Marcus repair отклонены protocol ValueError, четыре peer repair cancelled. Известный10.93rub subtotal,4unknownusage;5reported outputs превысили requested2000, оставаясь внутри ранее согласованного test-only8000ceiling. Лимиты не менялись. Generic validation_rejected в старом trace не позволяет восстановить точную причину каждого rejected vote.

Доказанный saved-draft дефект: claim v1/c4 basis=assumption, caveats v1/k1→c1 и v1/k2→c2, **ни одна caveat не относится к c4**. Поэтому qualified c4 не мог пройти guard, supported assumption тоже запрещён; допустимый unsupported по-прежнему был возможен. Дефект не объявляется доказанной причиной всех шести ошибок голосов. Новый scoped_proposal guard воспроизведён offline на именно сохранённом actual draft: assumption lacks applicable caveat.

R2e реализован минимально: координатор получает bounded адресный repair до5review-вызовов, если assumption не связан с конкретной caveat; никакой caveat/linkage не подставляется backend. Каждый известный literal validate_vote получил фиксированный safe code/path/instruction, без raw rejected text/model ID/exception body. Все прежние semantic/identity/citation/version guards сохранены; unsupported/object/abstain не превращаются в approve. Dynamic vote schema enums не добавлены: пока exact rejectedvote cause неизвестна, лишнее увеличение schema/context не требуется.

Свежая точная full-команда `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q`: **159passed48.44s exit0**. Новые checks: uncaveated draft repaired BEFORE barrier, повторная ошибка draft не вызывает ни одного review, linked caveat не форсирует согласие, specific assumption-as-fact и safeidentity repair. Independent design critique R2e PASS WITH RISK; **independent actual code review PASS WITH RISK**, own49focused15.51s exit0; reviewer повторно выполнил turn после account-limit interruption, без material findings. Полный FR-1–FR-9 outcome ещё open; новый платный запуск требует нового явного бюджета И пройденного applicable review gate (159full/49independentfocused завершены). Ниже сохранены предшествующие checkpoints.



## R2f текущая corrective wave / context revision

R2e final paid `8ee57ef138fe450bbd87a06057779b44` INCOMPLETE revision context_overflow,29attempts103.438s. Реально получены5positions+1decision+5atomic VALID object votes. Координатор исправил uncaveated assumption после targeted repair; Taleb исправил caveat_condition; guard false, все пять разногласий и5obligations сохранены. Known11.61rub0unknownusage. Дополнительныйone-run лимит1/1 исчерпан; paid повторов нет. Полный FR outcome не закрыт.

Offline EXACT actual mandatory nextrevision59287bytes; source footprint/positions/decision unchanged. previous_votes26846bytes, positions6267, decision5283, evidence7975, obligations2235. Полные старые проверки повторяли всю историю вопреки requirements9 (history не копируется целиком); статус supported не позволяет слепо удалять rationale: он может содержать уникальную qualification. CIT-RV01 учтён — **все** старые rationale остаются дословно.

First R2f design independent PASS WITH RISK: generation-only CompactProposal/CompactVote, все прежние cardinality/refs/conditiontext bounds и original state DTO сохраняются, local generation prose bounds; exact lossless feedback columns/identity/condition text/UNIQUE exact ledger reference packing. Current implementation completed; original sources/old accepted records не переписаны. Positive/negative/qualified explanations не фильтруются. Versioned decoder восстанавливает full old JSON, including null/defaults/arrays/order; pinning beforeprojection.

Full verification first R2f1failed168passed55.85s: new test incorrectly validated WIRE q-citations by original Proposal внутриfixture before runtimebound; исправлен catalog+resolve_output original-valid assertion, productionguard не менялся. Independent focus reproduces same fixture issue and checks conflict ledger exact/duplicate fallback; actualcode no materialfindings, finalfreshfull pending.

Sizing [citation-sizing-r2f.json](citation-sizing-r2f.json): oldactual wholeVote roundtrip PASS, afterlosslessfeedbackpacking actualmandatory52798 >32768 (safe refusal). Clearly SYNTHETIC futurebody3round fixture stops atv2draft; это FAILED approach, не greenfit/success. Даже отдельный очень короткий hypotheticalv2 обязательный35854 >32768. Дальнейшее сокращение meaningfuldata или повышениеcap не выбрано. Alternative design: generic lossless column tables для repeated input records только laterrounds, every literal value preserved, explicit fieldcolumns/rows/mapkeys/missingmarker with escaping. Это Request input representation; original backend state/quotecheck/schema/output unchanged. Alternative independentdesign review pending; implement only afterreview. Full semantic/live acceptance остаётсяopen; новыйpaid требуетновогоявногоone-run authorization и завершённыхfull/reviewgates.


## r10 / R2f retained checkpoint after user steering

User explicitly requested: «Оставь 34 037 сильнее оптимизировать не требуется». Further optimization stopped. The just-started additional decision/caveat references, trailing-null feedback v2 and policy condensation were reverted. Retained: generation-only CompactProposal/CompactVote bounds, lossless complete feedback v1 and readable context record tables v1. All source text, supported-check qualifications, missing values vs null, immutable decision identity/provenance and strict output/semantic/transition guards preserved. Context measurement, dispatch and bounded repair use the same encoded full Request; outputs never use the input decoder. No new service/database, model/provider/persona/question change, budget increase or paid run.

Retained behavior passed exact full `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q`: **188 passed54.55s, exit0**. Independent codec review found CIT-T01 (numeric missing sentinel equality), fixed with exact boolean True and three negative tests; own packing19passed0.86s, prior combined78passed38.18s. Latest design-only feedback v2 approval does NOT mean implementation retained. Citation/feedback/pinning/repair and three-round scripted protocol checks passed; scripted fixtures are not live outcomes.

[citation-sizing-r2f-tables.json](citation-sizing-r2f-tables.json): explicitly SYNTHETIC byte fixture using the last actual five initial positions/source citations and exact caveat conditions. Round1 six mandatory contexts+repairs fit; round2 draft **34037 >32768**, so sizing gate remains FAIL and further optimization was stopped by the user. Old actual revision is50394 bytes after tables and still safely rejected; full input table roundtrip is exact. No claim that any real model can read compressed inputs correctly or that all possible DTO maxima fit. First diagnostic trace read used the wrong Windows default encoding; corrected to explicit UTF8, original trace/source digests are intact and files were not modified.

Latest paid run remains `8ee57ef138fe450bbd87a06057779b44`, INCOMPLETE revision context overflow after5positions+1decision+5valid object votes,29attempts/103.4375s,11.61rub known/0unknown. Its separately authorized one-run budget **1/1 consumed**. No additional live performed. Full FR-1–FR-9 acceptance open;32768-byte guard still blocks demonstrated34037-byte context. Route12/retained implementation done →13/offline tests PASS but sizing FAIL →14/independent codec review PASS WITH RISK →13/live not ready (size+paid budget) →15/pending. Historical checkpoints below are preserved.

