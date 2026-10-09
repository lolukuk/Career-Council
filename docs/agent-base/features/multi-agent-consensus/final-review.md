# Independent actual final review14

2026-10-08; reviewer consensus-protocol-reviewer, отдельный от root author. Input: фактический current-code council, tests, approved design r3/implementation p2, verification.md и текущие agree/revise/disagree trace artifacts. Это самостоятельная проверка реализации, не перенос design/plan pass.

**Исходный verdict: blocked. Текущий final verdict после авторских исправлений: pass.** R12–R14 P2 и последующий R15 P3 independently closed ниже; исходные контрпримеры сохранены. Они воспроизведены reviewer локальным установленным Python без provider/install/network calls. Product files reviewer не изменял; scoped outputs только этот review и final-review handoff.

## R12 — P2: whitespace обоснования каждого check пропускаются в consensus

- Files/lines: schemas.py **179–183** `Check.rationale: Short`; runtime.py **65–79** `validate_vote`. Design §5/§6, requirements3/4/6, E04 «missing justification».
- Trigger: adapter возвращает обычный approve с непустыми общими rationale/change_explanation/payload_assessment, но для всех `criterion_checks`/`claim_assessments` меняет rationale на `' '`. Short проверяет min_length1, а strip-проверка validate_vote относится только к трём outer полям.
- Actual reproduction: subclass ScriptedAdapter; после `super().generate(request)` для stage review пройти по criterion_checks/objection_checks/conflict_checks/claim_assessments и присвоить `check['rationale']=' '`. Run Council с fixture retriever из conftest и реальным frozen personas.md.
- Observed reviewer output: **`blank_check_rationales: consensus rounds 1 checks [('v1/c1', "' '")]`**. Все пять approve приняты без содержательной причины конкретного claim/criterion. Это structural empty-justification bypass, не спор о семантической истинности.
- Minimal correction: nonblank validator для каждого Check.rationale и иных required justification fields; reject whitespace в schema/validate, bounded repair остаётся max2 total. Добавить E04 negative checks для каждой группы, включая owner resolution/conflict disposition; не требовать detector качества произвольного непустого текста.
- Owner: I02 (schema fix возвращается I01 owner root при необходимости). Current disposition: open.

## R13 — P2: результат после model timeout принимается, если coroutine подавила cancellation

- Files/lines: model.py **68–75** `asyncio.wait_for`; runtime.py **177–211** call/acceptance; E10 late-result/model timeout.
- Trigger: adapter `generate` делает await sleep(.05), при CancelledError ждёт ещё .02 и возвращает валидный scripted payload. Config(model_timeout=.001). asyncio.wait_for ждёт отмену coroutine; подавленная отмена может вернуть Response вместо TimeoutError. Runtime проверяет только run deadline/cancel, а attempt deadline не фиксируется и request не деактивируется при истечении timeout.
- Actual reproduction: subclass ScriptedAdapter:

```python
async def generate(self, request):
    try:
        await asyncio.sleep(.05)
    except asyncio.CancelledError:
        await asyncio.sleep(.02)
    return await super().generate(request)
```

- Observed reviewer output: **`suppressed_cancel_late_response: consensus timeout 0.001 elapsed 0.176 accepted 11 attempts 11`**. Все11 Responses после заданного attempt timeout accepted, включая пять голосов; late result protection на terminal run не защищает истекший attempt.
- Effect: timeout boolean/capability promise adapter недостаточен для request acceptance; зависший cancel cleanup также может ждать без границы в gather. Даже future cooperative provider должен иметь deterministic expired-request denial.
- Minimal correction: runtime-owned absolute attempt expiry/active attempt identity; timeout деактивирует request до отмены, Response после expiry never accepted. Cleanup/drain ограничить, late result suppress/reject без попытки утверждать остановку внешней тарификации. Recoverable retry всё ещё same frozen input/max2 total. Добавить E10 suppressed-cancel returning-late negative fixture и проверку limited cleanup; malformed/current normal adapter поведение сохранить.
- Owner: I02. Current disposition: open.

## R14 — P2: retrieval не ограничен оставшимся discussion deadline

- Files/lines: runtime.py **158–166 active**, **233 initial search**, **319 feedback search**; retrieval.py **49–62 request**, timeout берётся из preparation_timeout; requirements7/design §9/E07/E10.
- Trigger: один native/query search начинается непосредственно перед discussion deadline. `await asyncio.to_thread(search, queries)` не получает remaining deadline; encoder managed получает preparation_timeout (до300s), даже когда осталось .02s discussion. Active проверяется только после завершения search.
- Actual reproduction: fixture retriever.search wrapper `time.sleep(.2); return original(queries)`, Council Config(deadline=.02). Никаких native/LLM вызовов для этой reviewer reproduction не нужно.
- Observed reviewer output: **`retrieval_deadline: incomplete cap 0.02 elapsed 0.222 attempts 0`**. Статус честный, но остановка происходит более чем через десятикратный заданный предел; сам retrieval продолжает работу. Default near600s может добавить до300s native query wait.
- Minimal correction: deadline/cancel envelope от discussion в retriever/encoder query; worker timeout = minimum собственного лимита и remaining run time, interruption/kill/wait доbounded completion. Initial и feedback поиски используют одну policy. На coroutine/дедлайне остановить именно native child, не только отвязать to_thread и продолжить фоновую загрузку. Deadline истёк → incomplete; user cancel → cancelled; late packet не используется. Regression E07/E10 с slow managed child, tight remaining discussion deadline и отсутствие late child/output; actual timeout-specific cleanup evidence сохранить отдельно от existing cancel test.
- Owner: I01 retrieval + I02 orchestration integration. Current disposition: open.

## Что фактически проверено

Прочитаны actual schemas/runtime/context/model, source/tasker wrapper, retrieval/worker, CLI/prompts/scripted/report и все семь test modules/conftest. DTO frozen, source-only citations, exact-ID check sets, version/digest binding, every-version owner objection/conflict checks и current caveat links реализованы, а не только описаны. Fixed roster/persona config взяты из supplied file; первоначальная изоляция и current sibling votes исключены allow-list. Dense path реально SentenceTransformer, не hash vectors; worker import/load внутри managed child.

Reviewer независимо прочитал текущие traces:

| Run | Actual trace outcome | Versions/attempts | Provenance/engine |
|---|---|---|---|
| 65a37b0a585c4e45b6caa5e5a1a1bf9d | scripted consensus | 1/11 | 89 sources,298 chunks; all-MiniLM-L6-v2; stopped worker return0 |
| d88a5ace359e4b989b4f7e2a9774ffdf | scripted consensus после owner recheck | 2/17 | 89/298; current owner o1 checks; two stopped worker events |
| 73df8defaa2a42898797bfb34cae53df | scripted no_consensus | 3/23 | 89/298; o1 сохранён; five votes/each version |

Для каждой версии есть пять exact roster votes; ledger/history/accepted decision доступны в trace. Report renderer не вызывает дополнительный LLM, включает canonical exact decision, голоса, dissent/missing data/citations, human final choice вне run и scripted disclosure. В source API реально sequence get_tasks→get_task_details/get_subtasks; model не задаёт tool names/paths. Output-write cleanup tested в существующем suite.

Author verification full suite **46 passed24.82s exit0** и actual dense/native tests прочитаны как evidence; reviewer full suite/демо не повторял без новых изменений. Actual dense test проверяет paraphrase-only source, rare lexical hit и source tails; actual Windows cancellation test проверяет child stopped/returncode/absence of late output. Native **timeout-specific** fixture пока не исполнен и это честно записано автором; R14 repair должен закрыть остающуюся deadline ветку. Green46 не покрывает три reproduced cases выше.

## Ограничения и remaining work

- Scripted reasoning/semantic assessments остаются fixtures. No live provider/model/SDK/calls, no live support precision/sycophancy/quality evidence; пользователь отложил provider. Готовность neutral adapter не равна подтверждённой AI-системе.
- Entailment/полноту источников/правильность initial framework reasoning невозможно доказать substring и schema; эта граница явно раскрыта. Новый verifier-agent не требуется для исправления R12–R14.
- Root исправляет affected I01/I02, добавляет focused regressions и выполняет требуемые checks/relevant vertical demos. Failed reviewer evidence выше сохраняется. Reviewer затем проверяет author code/evidence closure; пользовательская acceptance15 отдельно и пока не получена.

## Independent author-repair closure — first pass

Reviewer прочитал исправленные schemas/model/runtime/retrieval и новые targeted tests, затем самостоятельно повторил исходные три adversarial workloads без live/install. Slow search wrapper адаптирован только к новому deadline/cancel keyword interface; workload sleep(.2)/discussion cap(.02) сохранён. Исходные failed outputs выше не удалены.

| Finding | Actual repeated result | Provisional disposition |
|---|---|---|
| R12 | `failed rounds1 guard_true False` вместо consensus при whitespace reasons. Новый DTO validator проверяет каждый required scalar text; four check groups covered author fixtures. | Functional fix verified; current-code full/vertical evidence pending. |
| R13 | `failed elapsed0.044 accepted0 active_attempts0` вместо consensus11 accepted. Absolute attempt expiry/identity authoritative, cancellation не восстанавливает request. | Functional fix verified; обнаружен небольшой отдельный cleanup finding R15 ниже. |
| R14 | `incomplete cap0.02 elapsed0.022 attempts0`; после завершения slow fixture `positions0/ranked0/coverage0`. | Functional fix verified; native/dependent full evidence pending. |

§ search теперь передаёт shared absolute deadline/cancel в encoder и ranking checkpoints; daemon bridge не ждёт default executor shutdown и не принимает late packet. Author новый actual native tight-deadline test прочитан: запускает настоящий child, замеряет run return отдельно, затем подтверждает child stopped/nonzero return/отсутствие late file/coverage. First-pass author evidence: I01 focused15 exit0, I02 focused32 exit0, actual dense/native3 exit0; full53/three current-dossier demos ещё ожидаются для окончательного verdict.

### R15 — P3: already-done expired task error не извлекается

- File: runtime.py `Council.call`, ветка проверки expiry перед `task.result()` и finally cleanup.
- Trigger: invoke уже done с TimeoutError; runtime видит истёкший expires и raises раньше task.result. Finally добавляет discard callback только когда task ещё not done. Ошибка finished task остаётся unobserved.
- Actual reviewer repetition R13: **10** loop exception-handler messages `Task exception was never retrieved`. Отдельно first repeat вывел TimeoutError tracebacks в stderr. Terminal status/consensus denial правильные; это не возвращение R13 bypass.
- Effect: шумные незавершённые cleanup diagnostics; возможный error body trusted adapter может попасть в default loop logging вместо redacted event. Current reproduction содержит только локальный TimeoutError, live secrets не использовались.
- Minimal fix: извлекать exception already-done expired/cancelled attempt через discard_task или done callback также для done ветки, без принятия payload. Проверить R13 regression с loop handler ==0. Не ждать unbounded provider cleanup и не ослаблять expiry.
- Owner I02 root. Current disposition: open, minor cleanup. До final pass root должен дать corrected evidence либо явно принять небольшой риск; новые stack/agent не нужны.

## Final independent closure14 — current repaired code / 2026-10-08

Reviewer повторно прочитал author-owned corrections в schemas/model/runtime/retrieval и regression tests; самостоятельно выполнил все три первоначальных workloads и дополнительный cleanup case. После последней cleanup-коррекции продуктовый snapshot стабилен. Current results переопределяют исторические open/provisional dispositions выше, не удаляя исходного evidence.

| Finding | Current disposition | Independent closure evidence |
|---|---|---|
| R12 P2 | closed | Исходный whitespace mutation теперь `failed rounds1 guard_true False`. DTO scalar validator rejects blank required reasons; авторские четыре check-group fixtures входят в regression suite. |
| R13 P2 | closed | Suppressed-cancellation response теперь `failed accepted0 active_attempts0`; absolute expiry/identity authoritative, expired payload не принимается. После cleanup-коррекции independent повтор также failed/0 accepted/0active. |
| R14 P2 | closed | Slow search .2s при discussion cap .02s возвращает `incomplete elapsed0.022 attempts0`; после завершения late fixture positions/ranked/coverage остаются0. Shared deadline/cancel проходит до managed query child и ranking. |
| R15 P3 | closed | Автор добавил discard_task для already-done task. Reviewer сам повторил suppressed-cancel case с loop handler и GC: **warnings0** вместо исходных10, accepted0/active0. Error извлекается без принятия payload; pending branch по-прежнему bounded detach/discard. |

Reviewer самостоятельно выполнил native deadline regression: `.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_dense_integration.py::test_discussion_deadline_stops_actual_query_child -q`, **exit0,1 passed0.36s**. Test запускает реальный Windows child, проверяет exact propagated deadline, incomplete run без model calls, child stopped/returncode, отсутствие late file и coverage. Это отдельная фактическая timeout proof сверх прежнего native cancel test; не inferred из worker file.

Прочитано окончательное author evidence в verification.md **Current final code evidence**: exact full task check `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q` → **exit0,54 passed19.69s**; focused protocol/model33 passed2.65s; actual dense/native3 passed14.25s. Full54 выполнен автором после последней cleanup-коррекции, reviewer его не выдаёт за собственный повтор. Broad re-run без новых изменений не понадобился.

Reviewer независимо прочитал postrepair actual-dossier traces:

| Current artifact run | Outcome | Versions / attempts |
|---|---|---|
| 9c5e7e81fc9d4565b5904c83e7b1ba87 | scripted consensus | 1 /11 |
| 2a5a1ace41634f198420ad79c74537d8 | scripted consensus после revision | 2 /17 |
| ad3bd757a6984309bcf5f1005a44dcfc | scripted no_consensus с dissent | 3 /23 |

Все три:89 sources/298 chunks; настоящая dense конфигурация, native stopped return0; exact roster и votes каждой версии, ledger/immutable decision сохранены. CLI demo команды автора exit0. Последняя one-line cleanup change не меняет accepted decision/report behaviour, full54 проверяет normal и negative paths на final code.

**Final verdict14: pass для согласованного минимального прототипа. R12–R15 closed; unresolved actionable final-review findings нет.** Design/plan pass сами по себе не использовались как доказательство качества реализации: verdict основан на actual code inspection, independently reproduced failures/closures, native execution и final regression/artifacts evidence.

Материальные границы сохраняются: это scripted protocol prototype с настоящим hybrid retrieval и нейтральным будущим ModelAdapter. Живого провайдера/SDK/LLM calls нет; semantic grounding, prompt resistance, fidelity/различие reasoning пяти персон, correlated errors/sycophancy и live decision quality **не проверены**. Async cancellation предполагает работоспособный event loop/trusted cooperative adapter; остановка внешней тарификации не обещается. Никаких дополнительных агентов/инфраструктуры reviewer не потребовал.

User acceptance15 отдельно **pending**. Root может предъявить реализацию, отчёты и фактические границы пользователю; independent pass не означает, что человек уже принял результат.
