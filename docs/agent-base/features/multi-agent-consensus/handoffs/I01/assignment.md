# I01 — Evidence packet

Owner: root по skils/consensus-runtime-engineer.md. State: waiting-user11; выполнение не начато. Inputs: утверждённый design r3, requirements, evaluation-design, reviewed plan p2 и оригинальные personas/source/tasker.

Outcome: strict DTO, замороженный manifest/evidence, ограниченный read-only Tasker wrapper, BM25+dense RRF, transitive context pinning и контролируемый embedding worker. Локальные согласованные зависимости и lock фактических версий.

Files: council/__init__.py, schemas.py, sources.py, retrieval.py, embedding_worker.py, context.py, requirements.txt, requirements.lock.txt; council/tests/conftest.py, test_sources.py, test_retrieval.py, test_context.py. Исходные данные и tools/tasker.py сохраняются.

Dependencies: independent plan review08 pass и user approval11. DoD: source/DTO/context/fixture-fusion checks проходят; worker contract реализован. Actual dense/native proof обязателен позднее в I03 и не является будущей предпосылкой закрытия I01.

Check из корня проекта:

```powershell
.\.venv-consensus\Scripts\python.exe -m pytest council/tests/test_sources.py council/tests/test_retrieval.py council/tests/test_context.py -q
```

Handoff: result.md/todo.md с exit status и границами проверенного → I02. Новых implementation agents нет.
