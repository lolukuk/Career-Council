# template_lite — reusable templates

Заготовки поведения, профиля, задания и технологических ограничений для будущей неизвестной задачи. Они не являются утверждённым дизайном, выбранным стеком или материализованными project agents.

| Заготовка | Назначение |
| --- | --- |
| [agent-behavior.md](agent-behavior.md) | Поведение, разрешения, доверие, проверки и передача |
| [agent-profile.md](agent-profile.md) | Будущий доменный профиль `skils/<feature>-<domain-role>.md` |
| [task-assignment.md](task-assignment.md) | Ограниченное задание с одним владельцем и DoD |
| [constraints.md](constraints.md) | Общие ограничения и правила применимости |
| [languages/python.md](languages/python.md) | Python template |
| [languages/java.md](languages/java.md) | Java template |
| [languages/rust.md](languages/rust.md) | Rust template |
| [languages/go.md](languages/go.md) | Go template |
| [languages/typescript.md](languages/typescript.md) | TypeScript template |
| [postgres.md](postgres.md) | PostgreSQL template |

Конкретный язык, persistence, framework/SDK, model provider, deployment model и инфраструктура пока не выбраны. Все перечисленные технологии имеют одинаковый статус reusable template; Python/TypeScript/PostgreSQL не являются основой утверждённого стека.

## Применение после получения задачи

1. Используйте [bootstrap contract](../docs/agent-base/README.md) и [каталог templates](../agent-templates/README.md).
2. Создавайте feature workspace progressively; сначала требования и Why Agent? decision, затем необходимые решения и артефакты соответствующих стадий.
3. Только при достаточном контексте заполните нужный профиль и сохраните в `skils/<feature>-<domain-role>.md`. Сейчас папка не создаётся; незаменённые placeholders означают неготовый template.
4. Выбирайте ограничения только фактически выбранных технологий. В assignment фиксируйте версии/runtime/ОС, применимость, исключения и unknown; для ненужных conditional решений — `not-needed` с причиной.
5. Задания, разрешения, решения и результаты сохраняйте в feature workspace; при resume используйте status, decisions, routing, todos и handoffs.

Наличие шаблонов не разрешает вводить языки, зависимости или сервисы. Уже полученные разрешения сохраняются. Спектр ограничений уточняется по принятой версии, реализации языка, платформе и библиотекам; ограничения разных сред не переносятся автоматически.

Официальные источники находятся рядом с технологическими правилами. Версия документации не означает выбора project toolchain. При документальной подготовке не устанавливаются языки, БД и SDK. [agent-templates/template_lite.md](../agent-templates/template_lite.md) сохранён как совместимая точка входа к этим заготовкам.
