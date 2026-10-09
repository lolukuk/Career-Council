# I03 — Runnable prototype and scenarios

Owner: root по skils/consensus-runtime-engineer.md. State: proposed, зависит от approval11 и completed I02. Inputs: design r3, reviewed plan p2, evaluation-design и I01/I02 results.

Files: council/main.py, report.py, README.md; council/tests/test_cli_report.py, test_dense_integration.py; council/output/<run_id>/report/trace и feature verification.md. Сохранить исходный career question.

Outcome: runnable CLI, детерминированный Markdown/JSON report, полная trace, agree/revise/disagree сценарии с пятью фиксированными персонами, actual dense retrieval и Windows subprocess-stop/late-result evidence. Actual dense tests нельзя заменить fixed vectors или skip с заявлением hybrid verified.

Checks из корня проекта:

```powershell
.\.venv-consensus\Scripts\python.exe -m pytest council/tests -q
.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario agree
.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario revise
.\.venv-consensus\Scripts\python.exe -m council.main --mode scripted --scenario disagree
```

DoD: команды проходят exit0; agree/revise consensus относится к сценарному adapter, disagree выдаёт завершённый no_consensus с dissent. Failed/incomplete/cancelled возвращают nonzero. Verification фиксирует результаты E01–E12, настоящего dense и native cancellation; live provider/model checks явно unconfigured/unrun.

Handoff: result.md/todo.md и фактический код/evidence → independent review14. I03 done = ready_for_independent_review; reviewed14 и user accepted15 отдельны. Исправления review возвращаются в affected I01/I02/I03 с необходимыми dependent regressions.
