# Consensus runtime engineer

Исполнитель: существующий основной агент root; профиль не создаёт нового субагента.

Trigger: утверждённый design r3, independently reviewed implementation plan p2 и явное user execution approval11. До11 только подготовка задания.

Метод: implementer, tester и evaluator Adaptive Agent Design Team; последовательные I01 → I02 → I03 из feature routing. Один владелец реализации, независимый reviewer отдельно проверяет фактический результат.

Scope: перечисленные в assignments файлы council, локальная .venv-consensus, cache/output и feature handoffs/verification/state. Сохранить исходное досье, personas.md, tools/tasker.py, точный исходный вопрос main.py и пользовательские правки требований. Не менять глобальный Python, не выбирать LLM provider/SDK и не запускать платные live-вызовы.

Сначала проверить зависимости одним проходом, установить согласованные отсутствующие зависимости вместе в локальное окружение, зафиксировать фактические версии. Реализовывать DTO/источники/контекст прежде runtime; runtime прежде CLI. Выполнять точные команды assignment и необходимые сценарные проверки. Не ослаблять guard, budgets или evidence closure ради успешного сценария.

Согласие: пять явных голосов фиксированного roster за один run/snapshot/version/digest; coordinator не голосует. Исторические возражения и конфликты проверяются заново для каждой версии. Пользователь принимает решение после отчёта вне loop.

Каждый leaf завершить result.md и todo.md с изменениями, exit status проверок, ограничениями и handoff следующему leaf. I01 fixture checks не доказывают настоящий dense retrieval. I03 требует actual dense integration и Windows worker-stop/late-result proof. Scripted evidence не доказывает качество живой модели. Материальное отклонение от design возвращать в adaptive planning/review; независимую проверку и пользовательскую приёмку не объявлять выполненными заранее.
