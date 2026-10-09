# I02 — Consensus protocol

Owner: root по skils/consensus-runtime-engineer.md. State: proposed, зависит от approval11 и completed I01. Inputs: design r3, reviewed plan p2, evaluation-design и I01 contracts/evidence/context.

Outcome: LangGraph isolation/barriers для пяти первоначальных позиций и пяти reviews, versioned coordinator drafts, deterministic guard, bounded retries/budgets/cancellation, historical objection/conflict ledger и нейтральный ModelAdapter со ScriptedAdapter. Персонам недоступны позиции других на первом анализе и текущие sibling votes на review.

Files: council/model.py, prompts.py, scripted.py, runtime.py; council/tests/test_protocol.py, test_model_boundary.py. Runtime E05 whole-round conflict test принадлежит I02: conflicting citations/owner disposition/caveat должны сохраняться и перепроверяться на каждой версии.

DoD: fixture protocol и model-boundary checks проходят; нельзя согласиться с другой версией/digest, пропустить голос, скрыть unresolved blockers или принять неполный payload. Прекращение обсуждения сохраняет честный статус и dissent.

Check из корня проекта:

```powershell
.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_protocol.py council/tests/test_model_boundary.py -q
```

Handoff: result.md/todo.md с exit status и известными ограничениями → I03. Live model quality остаётся unrun.
