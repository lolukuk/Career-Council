# Independent implementation plan review

2026-10-08; input implementation p1/routing p1/task-routing DAG, user-approved design r3 и evaluation r3. Reviewer: отдельный consensus-protocol-reviewer; root — автор плана. Profile Current dispatch и plan-review assignment прочитаны. Design review F01–F08 сохранён read-only.

**Исходный verdict p1: blocked; текущий verdict p2: pass.** P09–P11 closed по независимому closure ниже; исходные findings/dispositions сохранены как история. В p1 P09 — циклический completion contract I03/14, P10/P11 — небольшие traceability/routing уточнения. План по существу минимален: один последовательный исполнитель, один independent reviewer, три связных результата, нет новой инфраструктуры/provider SDK или фиктивных AI-quality claims.

## P09 — P2: I03 done зависит от review14, который зависит от I03

- Exact section: implementation-plan **I03 DoD**: «independent final review ... завершён»; routing **I03 DoD**, task-routing **I03 →14**; утверждённый workflow этапов12–15.
- Trigger: root реализовал CLI/отчёт и выполнил все четыре final checks. I03 нельзя отметить done по его DoD, пока independent14 не завершён; dispatch14 по DAG требует готового I03. Система routing получает незавершённый upstream либо root вынужден считать ещё не выполненный review частью done.
- Effect: цикл готовности; plan-review рискует быть ошибочно принят за final code review, либо проверка readiness обходится вручную.
- Minimal fix: I03 DoD = implementation/checks/report evidence **ready_for_review**. Independent14 получает этот evidence и отдельно даёт reviewed verdict; user15 отдельно accepted. Удалить finished independent14 из leaf DoD, сохранить обязательность14 после I03. В routing/DAG/плане назвать одинаковые границы readiness/done/reviewed/accepted. Findings14 возвращаются в затронутый leaf, после correction новый ready_for_review и14, не в approval под видом implementation done.
- Disposition: open.

## P10 — P3: E05 runtime conflict lifecycle не имеет явного leaf owner

- Exact section: I01 DoD содержит E05; I02 DoD перечисляет E01–E04 и E06–E10, пропуская E05, хотя I02 runtime owns conflict checks/ledger.
- Trigger: I01 проверяет Conflict DTO, paired citations/context pinning; I02 проверяет object/claim guards, но не new_conflict in Vote → mandatory revision и removal of caveat V+1. Все перечисленные focused commands могут пройти, а именно regression сценарий F04 не будет исполнен. «Все E01–E12» в I03 не назначает конкретный runtime test этому месту.
- Effect: ambiguously owned end-to-end E05, несмотря на правильную общую final цель.
- Minimal fix: явно добавить E05 orchestration часть в I02 DoD/test_protocol.py: initial/Vote conflict registration, новый conflict запрещает consensus текущего раунда, обе стороны pinned, every-version owner disposition и missing/stale caveat блокируют next version. I01 оставляет source/context часть E05. Нового компонента/тестового framework не требуется.
- Disposition: open, minor traceability correction.

## P11 — P3: correction edge DAG возвращает любой finding в I01

- Exact section: task-routing **14 Findings and correction routing → I01**, против routing заключительного абзаца «repairs возвращаются в leaf scope».
- Trigger: final reviewer выявляет только report formatting/fidelity bug в I03; diagram отправляет correction в I01, хотя источники/retrieval не изменялись и их checks зелёные.
- Effect: лишнее upstream выполнение либо неверный owner/state переход; противоречие словесному scope contract.
- Minimal fix: correction routing node с affected leaf/dependency impact → I01/I02/I03 по реальному finding; relevant checks и новый review14. Либо явно обозначить I01 edge как условный только для evidence defects. Не повторять весь suite/зелёный upstream без изменения/нового риска.
- Disposition: open, minor diagram correction.

## Traceability и проверенные границы плана

| Contract/scenario | Planned ownership и evidence |
|---|---|
| E01 / E01-personas | I01 frozen persona config/source boundary; I02 allow-listed isolated initial/review contexts, barriers/identity. Exact supplied roster сохранён, новым агентам нет основания. |
| E02–E04 / F01–F02/F05 | I02 test_protocol/model_boundary: exact unanimity/version, historical owner rechecks, whole-payload wiring, qualified caveat/check-ID validation, malformed/repair. Semantic fixtures проверяют refusal wiring, не semantic truth. |
| E05 / F04 | I01 source pairs/pinning; I02 runtime lifecycle должен получить явную E05 строку по P10. |
| E06 / F03 | I01 provenance/chunk offsets/digests/closure; I02 call-visible refs, rejection/repair. |
| E07 | I01 bounded source/native worker/context; I02 attempt/round/token/deadline caps; I03 actual Windows worker stop evidence. Не обещан неопробованный hard-stop. |
| E08 | I01 persona/dossier/source boundary; I02 schema/IDs/allow-list предотвращают state/tool/terminal injection. |
| E09 | I01 actual get_tasks→details/subtasks, issued ID/response identity, retry/failure/cancel. Direct internal JSON bypass запрещён. |
| E10 | I02 total attempt reservation, malformed/auth errors, cancel precedence/late-result rejection; I03 Windows child termination evidence. |
| E11 | I01 fusion fixed vectors; I03 отдельный actual CPU all-MiniLM-L6-v2 encoder semantic-only integration и demos. Только fixed vectors недостаточны; silent skips для hybrid success запрещены. |
| E12 / F08 | I03 exact accepted report/version/digest, dissent/coverage/mode/output failure/CLI exit consistency. Human final choice вне run не меняет protocol state. |
| F06–F07 | Text/diagram terminal separation и exact supplied roster сохранены; E09/E12/E01-personas проверяют implementation consistency. |

Dependencies/ownership: contracts/sources/context создаются до runtime consumers, consumers до CLI; root-only sequential scopes исключают concurrent file conflicts. conftest.py I01 shared producer, далее исправления возвращаются его владельцу. Reviewer пишет только review/handoff. `.venv-consensus` вместо global install, отдельный concrete lock, model revision/tokenizer trace и CPU path соответствуют согласованному стеку; реальная compatibility ещё не проверена. Неудачная install не считается зелёным check и не разрешает скрытую смену стека.

Native evidence в I03 должно фактически показать прекращение управляемого worker PID после timeout/cancel, bounded join/kill/cleanup и отказ позднего результата. Наличие embedding_worker.py или только mock token не доказательство. План требует actual Windows proof; конкретный test fixture materializes при реализации в заявленном scope. Safe capability/config-denial развилка исходного дизайна остаётся допустимой. Download/bootstrap отделены от bounded run; cache недоступен → сначала подготовить модель, затем выполнить actual dense check, не lexical-only выдача за hybrid.

Provider-later deliverable сформулирован честно: runnable orchestration/report/true retrieval со ScriptedAdapter и neutral adapter contract, без неподключённого SDK и без заявлений «пять AI независимо решили». Непроверенный model режим должен fail before dossier disclosure. Последующий live integration/quality evaluation — отдельный scope после provider/model/budget выбора; текущие planned test результаты этого не заменяют.

Exact planned PowerShell commands достаточны как task checks после materialization; сейчас tests/files продукта не создавались и команды **не запускались**. Review только документов/маршрута, не code-quality/final review. Root исправляет P09–P11 и передаёт plan p2 для independent closure, затем reviewable execution preview/user gate11.

## Independent closure — implementation/routing p2, adaptive r6

2026-10-08. Автор исправил свой план/routing/DAG; reviewer независимо прочитал revised completion contracts всех I01–I03, prerequisites, corrections и gates. Author files и design-review не редактировались reviewer.

**Verdict p2: pass для plan gate08. P09–P11 closed, unresolved plan findings нет.** Это не execution approval11 и не final implementation/code review14.

| Finding | Current disposition | Проверка исходного trigger |
|---|---|---|
| P09 P2 | closed | I03 §DoD теперь implementation/check evidence → done/ready_for_independent_review;14 reviewed после I03 и15 accepted после14. I03 completion не зависит от14/15. Потребитель final review получает готовый code/evidence, не собственный предварительный verdict. |
| P10 P3 | closed | I02 DoD и routing явно назначают E05 whole-round Conflict test_protocol.py; ledger/current-version/caveat/negative-source lifecycle принадлежит runtime leaf, source/context часть остаётся I01. Final E01–E12 сохраняет комплексную проверку. |
| P11 P3 | closed | DAG14 findings ведёт в bounded repair node, затем affected I01/I02/I03. Routing требует dependent regression по затронутому контракту и обновление13 evidence перед новым14. Report-only defect идёт I03, не искусственно в I01. |

Дополнительно устранена forward-readiness неоднозначность I01: его completion требует implemented real-dense interface + focused source/DTO/context/fixture fusion checks; actual dense/native Windows integration остаётся mandatory I03/stage13 evidence. I01 pass не называется verified hybrid, пока future checks отсутствуют. Этот переход позволяет I02 потреблять стабильный контракт, не ожидая dependent I03. I03 затем требует I01/I02 focused readiness и делает actual end-to-end proof.

Первичный dependency route acyclic: approved plan08 + execution11 → I01 focused pass → I02 focused pass → I03 implementation/integration evidence →14 independent reviewed →15 user accepted. Review-driven correction loops допустимы и ограничены affected leaf scope; они не являются completion prerequisite cycle. До11 product work/install не разрешены; текущий design «Утверждаю» не подменяет11.

Все проверки closure документальные. Tests/install/real model/native cancellation/live calls не выполнялись; planned commands и DoD должны исполняться и давать фактический evidence после11. Следующий шаг root — конкретный execution preview/материализация профиля и assignments, затем user11.
