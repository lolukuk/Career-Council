# Независимый final review14 — фактическая реализация

Owner: existing consensus_design_review, отдельный от root author. Mode: реальная независимая проверка кода/evidence, не перенос plan verdict.

Inputs: approved requirements/design r3/evaluation-design, implementation p2, actual council modules/tests/README/lock, verification.md и council/output/*/trace.json/report.md. Full suite46 exit0 и actual dense/native stop уже выполнены; current agree-repeat будет дописан автором до closure. Провайдера/livecalls нет.

Read-only: product code, source data, author requirements/design/plan/state. Exclusive writes: feature final-review.md и handoffs/final-review/result.md,todo.md. Не менять код, не устанавливать зависимости, не выбирать provider. Воспроизводить конкретный counterexample через уже установленный local Python допустимо; никаких paid/live calls.

Review: требования→инварианты→actual implementation→test/evidence; exact-version guard, hidden/qualified claims, all historical obligations/conflicts, transitive pinning, bounded ingestion/native/model calls, snapshot/persona/source integrity, state ownership, correct report/dissent, stage gaps. Проверить реальные сценарные traces и фактические тесты. Указать P1/P2/P3 с минимальным reproducible counterexample/correction, verdict pass/pass-with-risk/blocked; различать protocol, native, dense и live quality.

Не выдавать исходный design/plan pass за actual final pass; реальное прочтение реализации и evidence обязательно. Material finding возвращается в affected I01/I02/I03 для авторского repair, relevant regression и нового closure. User acceptance15 separately pending.
