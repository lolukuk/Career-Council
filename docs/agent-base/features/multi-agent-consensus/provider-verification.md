# Подключение провайдеров: фактическая проверка

2026-10-09 / PI03–PI06. Пользователь утвердил PI02 вариантB и реализацию: AI Tunnel — инструмент проверки; OpenAI доступен проверяющему. Принятый ранее прототип не переоткрыт.

## Реализация

- `settings.py`: локальный .env, env/CLI precedence, отдельный ключ выбранного провайдера, отсутствие default model/legacy fallback, secret-free repr/errors. Исходные локальные ключи не перезаписывались и не выводились.
- `providers.py`: async httpx, фиксированные endpoints, AI Tunnel public chat metadata/JSON Schema/compression disabled; OpenAI Responses/authoritative count, truncation disabled/store=false. Ограниченные wire/response bodies, envelope/status/refusal/tool/identity/usage guards, transport-schema normalization с исходной локальной DTO validation.
- `model.py`: approved policy distinction, async preflight+generation в одной attempt lifetime, audit закрывается при expiry, count после suppressed cancellation не может начать generation. Старые scripted/test adapters совместимы.
- `runtime.py`: model/config provenance в snapshot, usage отклонённых ответов и unknown audit на ошибки, provider/policy/catalog в trace. Единогласие, personas, source/citation/ledger guards не изменялись.
- `main.py`: обе конфигурации из .env или overrides; model settings validation до досье; один async lifecycle для prepare/run/bounded close. `report.py`/README раскрывают exact count vs server-enforced и пределы billing/cancellation.
- httpx0.28.1 объявлен прямой зависимостью; эта же версия уже присутствовала в установленном окружении и requirements.lock.txt. Новые зависимости/SDK не устанавливались.

## Команды и evidence

1. Перед финальными уточнениями: `.venv-consensus/Scripts/python.exe -m pytest council/tests/test_model_boundary.py council/tests/test_cli_report.py -q` — exit0,13 pass1.28s.
2. Первоначальные provider fixtures: `.venv-consensus/Scripts/python.exe -m pytest council/tests/test_providers.py -q` — exit0,36 pass1.23s. После этого добавлены проверки общего count+generation deadline, suppressed count cancellation, unusable catalog; общий suite выполняется заново.
3. Первая полная проверка перед PI06 findings: `.venv-consensus/Scripts/python.exe -m pytest council/tests -q` — exit0,95 passed25.79s. Включала41 provider fixture и прежние54 native/dense/protocol checks.
4. **Окончательная полная проверка после PI06 исправлений**: та же команда — **exit0,103 passed24.19s**. Включает49 provider cases +54 прежних checks. Добавлены HTTP200 error401/429/400/503 с bounded policy/retained usage, positive CLI lifecycle обоих providers без personal credentials, completed expired inner error cleanup. Старый CLI-test также изолирован от personal.env/env keys.

## Исправления по независимому actual review

- PI-R01/P2: HTTP200 bodyerror429/5xx первоначально terminal. Исправлено: безопасный numeric/three-digit code классифицируется как auth/transient/terminal; raw body/error не выводится, полученный usage сохраняется. Actual reviewer повторил свой offline reproduction:429 стал TransientModelError, расход отклонённого ответа сохранён.
- PI-R02/P3: inner perform уже завершился с исключением после expiry, но exception не был retrieved. Исправлено: done child также проходит discard_task; actual reproduction теперь даёт пустой список loop warnings. Добавлен regression fixture.
- Safe provider category сохраняется в event/terminal reason, без raw server message; CLI preparation failures также понятны по безопасному коду.

Первоначальный BLOCKED review/evidence сохранён в handoffs/provider-review/final-result.md. **PI06 final actual PASS**: отдельный reviewer закрыл PI-R01/PI-R02 своим повтором, изучил CLI/cancellation/error fixtures и current103 pass. Дополнительные checks после зелёного полного suite не запускаются без новых findings.

Новые тесты: настройки/key isolation, реальные сериализованные wire formats через MockTransport, count cap/no generation, provider refusals/error bodies/usage/mismatch, bounded401/429/400 handling, три сценария agree/revise/disagree через **каждый** live adapter с fixture content, context policies, schema/default/tuple local guards, network/cancellation/late-preflight boundaries. Для каждого сценария проверяется сохранение consensus/no_consensus и отсутствие секретов в trace/report. Это HTTP fixtures и сценарные ответы, не реальные LLM-решения.

## Не проверено

Ни одной платной генерации/count-auth call не запускалось; ключи/модели пользователю предстоит задать. Live connectivity, remote enforcement, соответствие backend tokenizer/revision и качество reasoning не подтверждены. Точный предварительный count AI Tunnel отсутствует; локальная отмена/50 attempts не доказывают удалённую отмену/денежный предел. Historical54 tests2026-10-08 сохраняют свою дату.

PI06 independent actual code/evidence review — PASS. Реализация и offline verification завершены; пользовательская приёмка successor15 не объявляется заранее.


Authorized live continuation / 2026-10-09: credentials configured by user, AI Tunnel exact gpt-6-luna-pro. Connectivity/schema synthetic smoke passed, but three full bounded runs failed output cap2000; no initial5 barrier/decision/consensus. Corrective deltas: upstream cap field, optional explicit effort (defaults unchanged), bounded frozen prompt and original-schema bounds descriptions. Current full check110 passed31.27s exit0; local DTO/citation/consensus guards and2000/32768 budgets retained. Single none diagnostics also failed (criteria too_long before bounds correction; post-fix schema passed but local ValueError; final output2015 exceeded cap). Provider default-pro or none profile quality not certified, direct OpenAI live unrun without its key. Historical accepted prototype15/PI06 offline PASS preserved. Current evidence provider-live-verification.md, review handoffs/provider-review/live-result.md. Author correction/verification complete with unsuccessful live outcome; independent closure pending. Further paid repeat requires different user-selected exact model/provider or separately approved budget change; async user choice pending. No extra agents, framework components, publishing or infrastructure work.


PI07 implementation checkpoint /2026-10-09: independent design+serialplan PASS (handoffs/provider-review/live-result.md), user directly authorized AIT conditionaltest exception. Root implemented explicit --aitunnel-test-mode, Settings AIT-only bool, Capabilities strict/aitunnel_test, shared provider+runtime ceiling8000 vs requested2000, snapshot/trace/preparation profile and perattempt excess accounting, report test-only labeling. Strictdefault/OpenAI/body/model/refusal/DTO/citation/context/consensus/retry/time guards unchanged. Existing fixtures expanded for3753/8000/8001 and AITtest agree/revise/disagree, wrong-provider earlyreject. Exact current full check `.venv-consensus/Scripts/python.exe -m pytest council/tests -q`: exit0,117 passed33.30s (session38599). New actual real-dossier fullCLI withnone+AITtest flag session26669 running; no current liveposition/decision/consensus claim until terminal artifact. Existing reviewer code/final evidence review ongoing, no other agents/infrastructure.


PI07 failedlive/repair checkpoint: first conditional-profile fullCLI session26669 exit1, report council/output/24399613e83e4ecf9c1561dc9520e10c/report.md;34.01s,10attempts,0positions/decisions, six received outputs2015/1865/1915/1909/1691/1823 (reported costs0.67/0.65/0.66/0.66/0.59/0.45), all localDTO/citation/ID validation rejected. Four cancelledattemptusage rows missing in this historicaltrace, costs unknown, notzero. Independentreview BLOCKED PI07-R01/P2 perattemptcancel audit; preserve originalfailure.

Root cancellationrepair: runtime.call except asyncio.CancelledError records reserved attempt as acceptedfalse/unknown counts/excessnull/requested2000 and cancelled event before rethrow; no late result accepted/unboundedcleanup. Added one existing-file siblingfailure/cancelled4 regression requiring5attempts/events/usage bijection and noacceptedposition/decision.

One AITtest single-person diagnostic council/output/live-validation-b07af0f0df8143d4aa230acfd80837b8/metadata.json: output2052/input28927/cost0.63, schema passed4criteria/5arguments, one exactquotationguardfailure. Diagnostic-position.json is expressly NOT an accepted Position; evidence.json supplies shown evidence for local inspection. Exactcause: model collapsed CRLF into space; whitespace-normalized quote matches but contiguous exact substring doesnot. POLICY now instructs copy punctuation/whitespace exactly, prefer singleline, nojoining/normalization, decodedJSONquote mustmatch; sourcebasisneedsrefs/assumptionnone. No automaticquote repair or loosenedcitationguard.

Postrepair exact fullcheck `.venv-consensus/Scripts/python.exe -m pytest council/tests -q`: exit0,118 passed26.97s (session45838). Prior117/26.35 prompt-only run predates cancellationrepair, superseded notremoved. One current full real-dossier AITtest+none CLI session44982 running; actual finaloutcome and independentclosure pending.


PI07 current terminal live result /2026-10-09: postrepair `.venv-consensus/Scripts/python.exe -X utf8 -m council.main --mode model --reasoning-effort none --aitunnel-test-mode` session44982 exit1. Artifact council/output/f03b53115da344e7a308909e9a7ea15a/report.md +trace.json. Actual37.13s,8attempts/events/usage rows withbijectiveattemptIDs,6received (input/output:28592/1656,28914/1894,28945/1892,29191/2183,29015/2046,28749/1741; reportedcosts0.59/0.62/0.62/0.65/0.63/0.44),2cancelledexplicitunknownrows. Known reported subtotal3.55rubles is NOT fullrunprice; two remote canceledcosts unknown. Every outputrequested2000, twoexcessflagsTrue, canceledflagsnull. AITtest admission ceiling8000 worked, nooverbudgetfailure.

Peter/Warren singleinitial calls accepted; otherthree firstcalls rejectedValueError, Robert secondcall rejectedValueError, two remaining secondcalls cancelled. No completefivebarrier, so atomicinitial_positions remain0 anddecisions0. This is intentionalphaseisolation, notproofthose two responsesweren't individuallyvalid. Specificcause ofthese currentValueErrors not logged (citation/ID/JSONvalidation category), notassumedidentical to independentlydiagnosedCRLFcase. Statusfailed/RuntimeError protocol-source-modelfailure honestlyreported; no forcedapproval, fakepositions, declaredunanimity or livequalityscore. Currentprompt improvesstrictquotations but doesnotguaranteemodelcompliance.

Current full118 passed26.97s exit0; independent reviewer owncancelregression1 passed0.80s exit0, finalPI07closurependingactualtraceinspection. Previous117PASS/cancelgapBLOCKED/history preserved. PI07implementation/currentboundedverification complete (actualliveunsuccessful permittedbyexplicitplanDoD); further same-model blindfullruns stopped. AI Tunnelconditionalprofile excludedfromprod; defaultAIstrict/directOpenAIstrict unchanged, directOpenAIliveunrunwithoutitskey. Existing acceptedprototype15 notrescinded; no requestfornewtechnology/extraagents or looseningprovenance/consensus.


PI07 final closure /2026-10-09: existing independent reviewer actual PASS recorded handoffs/provider-review/live-result.md/todo.md. PI07-R01 closed by own focused1 passed0.80s exit0, authorfull118 passed26.97s exit0 and independently inspected terminal f03trace8attempt/events/usage bijection/6known+2nullunknown/excess2183+2046/2individualaccepted/0atomicpositions/0decisions/failed. No remainingmaterialproductcorrection; implementation13 verification and14 independentreview completed. Live protocol FAIL acknowledged, never mislabeled no_consensus/quality orproductioncertification. ConditionalAIT exception authorized and delivered; oldexternalmodelchoice superseded.15 successor useracceptance remains separate, prioracceptedprototype preserved. Current report ready, no furtherpaidrepeat/code/check/install/publicationpendinginPI07.
