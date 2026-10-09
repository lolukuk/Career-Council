# План реализации и проверок — Multi-Agent Consensus System

## Актуальное состояние r9 — 2026-10-09

C01–C05 реализованы. C06: проверки выполнены, критерий полного живого результата **не пройден**. Точная команда `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q` завершилась exit0: **133 passed in 12.94s**. Измерение 1200 документов / 300 заметок PASS: 22 906 байт, 14.713 с, sampled peak process tree 650 575 872 байт; настоящий dense encoder, классификатор в измерении scripted. Это не production SLA и не доказательство качества живого фильтра.

Выполнены все три разрешённых полных платных запуска: incomplete / incomplete / failed. В live2 зафиксированы пять валидных позиций; в live3 только три принятых индивидуальных ответа, общий атомарный этап пяти позиций не завершён. Последний отказ: Buffett дважды `citation_quote_not_exact`, затем отменён repair Reich. Проект решения и пять голосов не получены. Четвёртый запуск не разрешён и не выполнялся; строгие guards и лимиты не ослаблены.

05/08 independent design/plan PASS; C-R01 inventory-evidence исправлен и независимо CLOSED. 14 final review: implementation PASS / full-live acceptance BLOCKED (см. handoffs/corrective-review/result.md). 15 отдельная пользовательская приёмка FR-1–FR-9 **открыта**. Историческая приёмка scripted-прототипа сохранена. Модель AI Tunnel / gpt-6-luna-pro, входной user_prompt и числовые лимиты сохранены; Git-коммита нет.

Фактические результаты и ограничения: [общий аудит](../../../career-council-review-2026-10-09.md), [live3 report](../../../../council/output/1100b8f39a594601af28e5fa7ccd25ba/report.md), [scale metadata](../../../../council/output/scale-73855c2e7c4f4bcea3cd24ea77966fd4/metadata.json). Для закрытия задания нужна отдельно согласованная коррекция воспроизводимого нарушения точных цитат и новая разрешённая live-проверка; до этого готовность к полной приёмке не заявляется.


## История промежуточных состояний C01–C06

## C01–C05 checkpoint / 2026-10-09
C01 audit/current route saved; 05/08 independent corrective design/plan PASS. C02–C05 implemented serially. C-R01 initial independent BLOCKED (inventory tool exposed detail evidence) preserved, corrected by immutable actual API inventory source; independently CLOSED with23 affected checks and direct repro exit0, see handoffs/corrective-review/result.md. Author full131 passed32.39s exit0 before final context-priority adjustment. Final adjustment gives optional slots to documents/notes before uncited structured tasks; cited/tool data remains pinned. Scale failures preserved at scale-6162bf6dfb064a9fb1f2e0dc2588c52a and scale-46576e5d9cfd4e358464fcaad53ff1b2; corpus query primary weight3 and source-type selection corrected, current repeat pending. C06 running, live runs0/3; full-product acceptance15 pending. No model/prompt/DTO guard relaxation or commit.


## Current correction r9 / C01–C06 — approved
One serial root implementer, separate reviewer; no new stack/runtime personas/DB or commit. C01 general review/FR matrix/current headers and flows. C02 hybrid shortlist≤20 notes, ONE bounded structured relevance operation (max2 attempts), unknown selected IDs rejected, empty relevant set valid; note/task/subtask no fallback, transitive citations preserved. C03 typed ToolAction JSON: name∈{get_tasks,get_task_details,get_subtasks,finish}, task_id nullable with operation validation; LangGraph dispatches shared wrapper over API-captured frozen run snapshot and returns scoped records/evidence/provenance. All five have access; max3 tool dispatches per advisor. Unknown IDs/writes denied; actual API calls and snapshot reads accounted separately. Additional LLM calls share max50 attempts/600s.
C04 keep Position/Proposal/Vote and exact quote/digest checks unchanged. Compact stage instructions, safe validation_stage/code on second attempt; repair request has new ID/digest and original task reference, question/evidence/version/roster unchanged. No raw exception/output logging. Existing2000 output/32768 bytes maintained; insufficiency is a blocker, never automatic relaxation.
C05 render accepted recommendation/steps/risks/caveats/missing data and five positions; exact JSON in trace. Root product entry, README diagram/rationale/future. C06 one recorded1200document/300note scale scenario with relevant/negative/noise ground truth, serialized≤32768 bytes, measured time and memory; all-noise and mixed note cases, empty/error API and bounded tools. Exact `.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q`; then≤3 full current-model runs, repeat only after actual cause/fix. Expected five positions + decision + useful consensus/no_consensus and selected tool. Reviewer checks semantic citations/personalization/contrasts; user acceptance remains separate. Failed live after cap leaves original assignment open.

## Historical records

Implementation plan p2 / adaptive revision r6 / 2026-10-08. Input: user-approved design r3, requirements и evaluation-design r3; независимый design review F01–F08 closed. p1 review blocked P09–P11 сохранён в plan-review.md; p2 independent closure PASS, P09–P11 closed. Execution p2 user-approved11 и implemented; current focused/full54 pass. Actual review closure14 и user15 отдельно.

## Минимальный результат

Работающий CLI прототип в существующей `council`: пять профилей точно из personas.md; frozen dossier/read tasker; настоящий hybrid retrieval; ограниченные persona contexts; LangGraph workflow/versioned decision/пять оценок/deterministic guard; отчёт и JSON-трасса. Сценарный adapter демонстрирует agree/revise/disagree и проверяет протокол. ModelAdapter — нейтральный интерфейс для будущего провайдера; реальный LLM connector/SDK не выбирается, live-quality не объявляется проверенным.

Сценарные позиции не выдаются за независимо полученный AI-анализ. Поиск с настоящими embeddings проверяется отдельно от fixed-vector tests. Готовый report не перефразирует accepted decision, human final choice не меняет consensus status.

## Команда и выполнение

Один исполнитель — root, совмещает contracts/retrieval/runtime/evals; один отдельный reviewer уже материализован для независимых reviews. Новых субагентов разработки/infra/evidence judge нет. Root работает по профилю `skils/consensus-runtime-engineer.md`, материализован на10 перед исполнением. Reviewer читает план/дизайн, пишет только plan-review/handoff; итоговое review позже выполняется отдельно по фактическому коду/checks.

Три последовательных leaf результата с одним owner и непересекающимися первичными scopes; dependent fixes возвращаются владельцу соответствующего leaf. Атомарный маршрут: [routing.md](routing.md), [DAG](artifacts/flows/task-routing.mmd). Полный SDLC по-прежнему workflow.md.

## I01 — Проверяемый evidence packet

Владелец root. Inputs: design §2–5/7–9, actual source files/tasker API. Outputs: `council/__init__.py`, `schemas.py`, `sources.py`, `retrieval.py`, `embedding_worker.py`, `context.py`, `requirements.txt`, `requirements.lock.txt`; tests `test_sources.py`, `test_retrieval.py`, `test_context.py`, shared `conftest.py`.

Результат: strict DTOs и frozen persona config из given file, источник/offset/digest registry, real hierarchical tasker read wrapper с bounded retries/identity checks, tokenizer-aware chunking, BM25/dense RRF, coverage и transitive pinned evidence closure. Context builder использует allow-list, целые optional chunks и fail-closed overflow. Все источники/roster сохраняются, personas не являются RAG evidence о Mark.

Локальное окружение `.venv-consensus` в project root; approved Python 3.13. Создать окружение только после11. Установить все согласованные зависимости одной операцией из requirements (LangGraph, Pydantic, pytest, Sentence Transformers/CPU dependency chain), не в global Python; сохранить конкретный проверенный lock. Новых библиотек для web/DB/provider не добавлять. Probe уже показал отсутствующие langgraph/pydantic/pytest/sentence_transformers/torch; Py3.13 доступен. Wheel/ABI compatibility проверяется при установке; не скрывать installation failure как зелёную проверку.

Dense модель для текущего англоязычного корпуса: `sentence-transformers/all-MiniLM-L6-v2`, CPU, model_id/revision/tokenizer settings traceable. [Официальный пример Sentence Transformers](https://sbert.net/docs/sentence_transformer/usage/usage.html) показывает такую модель. Загрузка публичных весов/локальный cache — dependency preparation, не paid live LLM. Проверить реальный tokenizer/max_seq_length и нормализацию векторов; не использовать hash-vectors как dense substitute.

Один local managed worker допустим для гарантируемого timeout/cancel native load/embedding. Это вспомогательный процесс, не агент/сервис. Python Windows spawn-safe entry point, контролируемые аргументы/temp files, bounded output, explicit join/kill/cleanup; нет worker-supplied imports/paths. Источники ограничиваются до materialization/index; preparation limit не обходится повторной загрузкой.

DoD: E01-personas/E05/E06/E07 source/closure bounds/E08 input boundary/E09/E11 реализованы на этом уровне. Fixed-vector fixtures проверяют fusion; real-dense test отдельно проверяет actual encoder и semantic-only hit. Mandatory categories отсутствуют → честный gap/incomplete, не invented data.

Implementation/focused-check completion I01 не зависит от будущего I03: интерфейс real dense реализован, DTO/source/context и fusion проверены fixtures, integrated real-model proof ещё pending13. Check (planned): `.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_sources.py council/tests/test_retrieval.py council/tests/test_context.py -q`. Real-dense integration/native proof — отдельные обязательные I03/stage13 checks с подготовленным cache; не silently skip и не выдавать focused fixture pass за verified hybrid.

## I02 — Ограниченный протокол обсуждения

Prerequisite I01 pass. Владелец root. Outputs: `council/model.py`, `prompts.py`, `scripted.py`, `runtime.py`; tests `test_protocol.py`, `test_model_boundary.py`.

Результат: нейтральный typed ModelAdapter и явно помеченный ScriptedAdapter; five-isolated initial analyses и five-isolated reviews; LangGraph lifecycle; complete schema/citation validation; request identity/attempt reservation/retry/late-result handling; immutable versions/digests; exact roster check; every-version historical blocker/conflict owner checks; typed claim/caveat refs/full payload assessment; bounded retrieval feedback; honest terminal statuses.

Coordinator не получает право закрывать owner blocker либо писать terminal. Repair — та же frozen request, максимум две total attempts, не новая попытка получить согласие вместо object. Live capabilities/token accounting интерфейс задаётся, но отсутствующая provider config не даёт model-run и не отправляет досье. Source provenance и model assertions остаются раздельными.

DoD: E01–E04 и E06–E10 orchestration части; explicit E05 whole-round Conflict scenario в test_protocol.py: discovery пары в Position/Vote, durable ledger, потеря negative source в ranking, сохранение пары/context/caveat, новая версия и explicit owner disposition. Это runtime ownership I02, source/provenance часть E05 принадлежит I01. Сохранение F01–F08. State mutation только root/runtime, worker outputs immutable; budgets зарезервированы до dispatch; cancellation precedence/late results проверены. Scripted semantic counterexamples проверяют wiring отказа, не реальные интеллектуальные способности модели.

Check (planned): `.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_protocol.py council/tests/test_model_boundary.py -q`.

## I03 — Запуск, отчёт и полная проверка вертикального среза

Prerequisites I01/I02 pass. Владелец root. Outputs: `council/main.py`, `report.py`, `README.md`, tests `test_cli_report.py`, `test_dense_integration.py`; пользовательские report/trace под `council/output/<run_id>/`; проверочное evidence в feature `verification.md`, handoffs I01–I03 result/todo и actual routing state.

Результат: CLI сохраняет заданный user_prompt, позволяет выбрать scripted agree/revise/disagree и другое dossier/question; library injection ModelAdapter оставляет путь к будущему provider, CLI model без настройки отклоняется честно. Report/trace exact payload/version, все voices, dissent/missing data/coverage/mode; output errors не выдают usable artifact. Инструкция запуска, Mermaid, rationale/limitations/future ideas в README. CLI runnable из project root через `-m council.main`; стандартный прямой entry point сохраняется либо его поддержка явно указывается, исходный prompt не изменяется.

Final checks (planned, exact команды для Windows PowerShell):

```powershell
.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q
.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario agree
.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario revise
.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario disagree
```

Тесты включают actual dense integration после explicit model preparation, не только fixture vectors. Demo commands используют реальное предоставленное досье/tasker wrapper и true dense path; exit0 означает корректный завершённый report, включая honest no_consensus для disagree, а не единогласие любой ценой. Failed/incomplete/cancelled имеют отдельные причины и ненулевой CLI exit, реализуется consistency check в E12.

E12 проверяет report fidelity/false user approval/no post-vote rewrite/output failure. Native subprocess termination/late-result exclusion из I01 проверяются на Windows здесь; наличие кода worker не считается доказанным stop. Измерения времени/attempts записываются по факту, не выдумываются. Инвариантные negative fixtures: 0 ложных consensus outcomes на фиксированном наборе.

Implementation/check DoD I03: все checks exit0, полное покрытие E01–E12 с раздельным evidence unit/scripted/real embeddings; demo reports inspectable; live eval explicitly not run. После этих evidence I03 done/ready_for_independent_review и stage13 done; это prerequisites14, а не его результат. Independent14 отдельно присваивает reviewed verdict; только user15 — accepted. Если blocker14, correction task в affected leaf и relevant checks; повтор не делает I03 или15 автоматически accepted.

## Риски и развилки

- Live provider/model выбран позже пользователем. Deliverable сейчас — исполнимый протокол с scenario adapter и готовым контрактом подключения; не полноценная подтверждённая AI-система/AI-quality. После выбора adapter/SDK/live budget нужен отдельный bounded integration/eval этап.
- CPU dependencies/model cache могут требовать загрузки; setup failure исправляется в рамках того же agreed stack и проверки повторяются. Новый interpreter/framework/model-provider не выбирается скрыто.
- Mandatory pinned evidence может превысить context; expected incomplete — корректное ограничение. Нельзя ослаблять pinning/guards ради удачной demo. Если provided normal dossier не вмещается, вернуть конкретное измерение и reviewed bounded adjustment, не менять лимит молча.
- Cancel/timeout native worker и provider отличаются: local worker stop проверяется; external provider billing/cancel не обещается.
- Нет инфраструктурных этапов, UI, write task tools, package EXE, remote publication, DB или дополнительного verifier-agent. Artifact download/install dependencies и локальное выполнение — единственные новые технические действия.

## Gates

07 plan → independent08 critique → 09 validated routing → 10 root profile/assignments/preview → 11 пользовательское разрешение конкретного выполнения → 12–13 bounded implementation/checks (I03 ready_for_review) → independent14 reviewed →15 user accepted. Коррекции14 направляются в affected I01/I02/I03, затем dependent regression checks/13 evidence update и новое14; не всегда в I01. Качество и проверки не заменяются планом. Текущий user ответ «Утверждаю» закрывает design06; историческое состояние этой фразы — до gate11; конкретный implementation-plan p2 затем утверждён пользователем (D16).

p2 corrections: P09 — устранён I03↔14 cycle; P10 — E05 whole-round scenario assigned I02/test_protocol.py; P11 — repairs routed affected leaf с dependent rechecks. New stack/scope/provider не введены.
