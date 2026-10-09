# Проверка реализации — фактическое evidence

Текущий итог: final code54 passed19.69s exit0; три postrepair CLI сценария exit0; independent14 PASS/R12–R15 closed. Native timeout/cancel и настоящие dense embeddings проверены. User15 accepted по прямому «Принимаю», live unconfigured/unrun. Начальные46/53 passes и прежние пробелы ниже сохранены как история; текущие результаты и closure см. финальные разделы.

Дата: 2026-10-08. Implementation p2, design r3. Gate11 accepted. Это продуктовые проверки, а не design trace. Python 3.13.0 / Windows; локальное .venv-consensus, фактические зависимости в council/requirements.lock.txt.

## Выполненные команды

| Проверка | Результат |
|---|---|
| `.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_sources.py council/tests/test_retrieval.py council/tests/test_context.py -q` | exit0, 15 passed, повтор после context correction 0.25s |
| `.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_protocol.py council/tests/test_model_boundary.py -q` | exit0, 26 passed, 2.03s |
| `.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_dense_integration.py -q` | exit0, 2 passed, 77.67s; actual model и Windows child kill/wait |
| `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q` | exit0, 46 passed39.08s; после parent-scoped subtask/cancel/capability correction: exit0, 46 passed24.82s |
| `.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario agree` | exit0, consensus; initial report503065c89aad42c8845528d8c8279d8c; current-code repeat exit0, report65a37b0a585c4e45b6caa5e5a1a1bf9d. |
| `.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario revise` | exit0, consensus; report d88a5ace359e4b989b4f7e2a9774ffdf |
| `.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario disagree` | exit0, no_consensus; report73df8defaa2a42898797bfb34cae53df |

Отчёты и trace.json находятся в council/output/<run_id>/. Данные читались из данного досье и через реальный предоставленный Tasker API, не напрямую из tasker.json. CLI использует настоящие embeddings; индекс/cache фиксирует model/revision/chunk settings и source content identity.

## Покрытие и границы

- E01/E01-personas: fixed frozen roster, initial allow-list, five positions barrier; review packet одинаков по evidence, текущие sibling votes отсутствуют. Tests inspect serialized inputs.
- E02/E04: missing/foreign roster, wrong run/digest, absent/duplicate checks, conditional approval, unsupported claim/payload, blank explanation и foreign caveat не дают consensus. Это negative protocol fixtures, не semantic intelligence evidence.
- E03: revise owner resolved; disagree upheld; regression V2 resolved→V3 missing recheck failed. Coordinator не пишет ledger status.
- E05: initial Conflict, version1/version2 explicit owner checks, потеря пары в ranking не вытесняет citations, removal caveat blocks next version.
- E06: unseen/fabricated quotes rejected, transitive closure pinned; source/vector alignment и offsets checked.
- E07: attempts/context/query/source bounds; mandatory closure overflow incomplete. Native Windows stop proven via deliberately slow real child PID and kill/wait; late output absent. Native timeout uses same cleanup path; separate actual timeout-specific fixture не выполнялся.
- E08: model-controlled consensus/next_agent extra fields rejected. Это output-boundary injection fixture; live prompt resistance не проверена.
- E09: sequential Tasker list/details/subtasks, transient retry/exhaustion, KeyError nonretry, duplicate task IDs/identity/parent mismatch rejected. Empty/missing category incomplete; other invalid input failed.
- E10: malformed JSON same-frozen-request repair, exhausted/auth errors, model timeout, cancellation before vote acceptance and token-cap deny before dispatch.
- E11: fixture BM25/dense branches/RRF/stable ties плюс настоящие embeddings с paraphrase-only semantic hit, rare lexical hit и длинным источником без truncation.
- E12: exact accepted JSON payload/digest in report, all voices/mode/human scope, unconfigured model CLI and output-write cleanup tested.

Live provider/model/SDK отсутствуют по решению пользователя. Calls/scripted semantic assessments не являются качеством живой AI-системы; token usage scripted=null. Обоснованность выводов в живом режиме и корреляция/sycophancy пяти промптов остаются непроверенными.

I03 implementation/check ready для independent14; окончательный agree-repeat exit0. Review verdict и user acceptance15 не подменяются результатом pytest.


## Author repair R12–R14 / original blocked evidence preserved
R12: all required scalar text incl. Check rationale rejects whitespace. R13: absolute attempt expiry/active identity removed before cancel; bounded detach/discard late response instead of unbounded wait_for/gather cleanup. R14: shared remaining discussion deadline/cancel into managed query and ranking; daemon result bridge rejects late output and avoids default executor shutdown wait.
Focused I01:15 passed0.07s exit0; I02:32 passed2.52s exit0; actual dense/native tests:3 passed14.25s exit0, now includes tight discussion deadline/native child stop separately from cancel. Full regression and three actual-dossier demos running. Independent closure not yet received; live unconfigured/unrun.

Author post-R12–R14 full regression:53 passed20.77s exit0; agree9c5e7e81fc9d4565b5904c83e7b1ba87 consensus, revise2a5a1ace41634f198420ad79c74537d8 consensus, disagreead3bd757a6984309bcf5f1005a44dcfc no_consensus; exact demo commands all exit0. Subsequent reviewer P3 R13 cleanup race required consume already-done expired task exceptions; added loop-exception fixture and rerun pending. Original failed outputs/initial passes retained as history.


## Current final code evidence / 2026-10-08
Final command: .\.venv-consensus\Scripts\python.exe -m pytest council/tests -q → exit0, 54 passed19.69s. Current focused protocol/model33 passed2.65s exit0. Postrepair native/dense3 passed14.25s; reviewer independently repeated tight native deadline1 passed0.36s. Three postrepair actual-dossier CLI demos all exit0: agree9c5e7e81fc9d4565b5904c83e7b1ba87 (consensus1 round11 attempts), revise2a5a1ace41634f198420ad79c74537d8 (consensus2 rounds17 attempts), disagreead3bd757a6984309bcf5f1005a44dcfc (no_consensus3 rounds23 attempts). All89 sources/298 exact chunks. Subsequent one-line cleanup fixes only detached exception retrieval, not accepted decision/report behaviour; full54 confirms normal/negative paths. Initial46/53 passes and original R12–R15 failures above are historical evidence, not current unresolved findings. Current independent closure/pass awaits reviewer recording verdict; acceptance15 pending. Live unconfigured/unrun.


Final closure / 2026-10-08: independent14 PASS; R12–R15 closed. Current full54 passed19.69s, three postrepair actual-dossier demos exit0, actual dense/native proof и reviewer reproductions сохранены. Stage15 waiting-user, не accepted. Live unconfigured/unrun.


User acceptance / 2026-10-08: прямой ответ «Принимаю» закрывает15 после actual independent14 PASS. Принят согласованный минимальный scripted protocol prototype с actual hybrid retrieval,54 checks и тремя сценарными отчётами. Принятие не означает live LLM quality: provider/model/SDK/live evals unconfigured/unrun и требуют отдельного будущего задания. Текущий scope завершён.


Eval documentation closure / 2026-10-09: EV01 root completed evaluation r4/README; EV02 existing independent reviewer documentary PASS, T6 attribution precision closed. Architecture/layers/scenarios/E01–E12/metrics/rubric/reproduction links documented without current live checks. No runtime/test code changes or fresh executions; historical54 results dated2026-10-08 retained. Original product accepted15 preserved; this directly requested documentation task completed, no additional user gate.
