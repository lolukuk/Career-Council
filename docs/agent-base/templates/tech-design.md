# Дизайн: <feature>

Создавать на 04 после одобренных требований и применимого stack gate. Это заготовка связанного lightweight-дизайна; для сложной задачи вынесите существенные контракты в отдельные файлы `agent/`. Каждое поле требует решения или явного `unknown`/`not-needed` с причиной; неразрешённые существенные вопросы блокируют gate.

## Основания и компоненты

- Requirements/why-agent/одобрения/revision: <реальные ссылки>.
- Выбранная минимальная автономия и альтернативы: <...>.
- Согласованный стек и версии, границы компонентов: <...>.
- Вход → обработка → выход; значимая sequence/state схема: <...>.

## Agent spec: цель, права и остановка

Актор/права, вход, наблюдаемый успех: <...>.
Свобода выбора модели и детерминированные действия runtime: <...>.
Разрешённое/запрещённое, clarification, cancellation и safe failure: <...>.
Конкретные max steps/time/tokens/tool calls/retries/context и источник пределов: <...>.

## Tool catalog и trust boundary

Для каждого tool отдельно: имя, точная schema входа/выхода/ошибок, read/mutate, source of truth и provenance идентификаторов; auth/permissions/preconditions; область эффекта; timeout/retry budget; idempotency/concurrency/reconciliation; audit/redaction: <...>.

Модель предлагает. Runtime проверяет schema, allow-list, происхождение аргументов, права и бизнес-инварианты, исполняет действие и владеет side effects. Prompt или tool output не расширяют права.

## State model и policies

Trusted observations/детерминированные выводы отдельно от model claims: <...>.
Run lifecycle, переходы, guard/denial behavior, transient/durable state, recovery: <...>.
Персональные данные/секреты, prompt/tool-output injection, допустимые адреса/пути: <...>.
Защита изменяющих операций и конкретное пользовательское разрешение: <...>.

## Model contract и context

Согласованный model/provider, структурированные решения tool_call/clarification/final или эквивалент, schema, malformed/unknown handling: <...>.
Сборка prompt/context, лимиты, сокращение, чувствительные данные и проверка финальных утверждений по evidence: <...>.
RAG/memory/context-strategy: <только по потребности; причина применимости>.

## Failure model

Tool/model errors, классификация повторов и пределы, deadlines/cancellation propagation, cleanup: <...>.
Неизвестный результат внешней записи → reconciliation/terminal unknown → решение о повторе: <...>.
Без downstream deduplication/reconciliation нельзя обещать exactly-once; timeout не доказывает отмену внешнего эффекта.

## Проверка и review

Нормальный trace и существенные failure/abuse traces, инварианты → cases/assertions/evidence: <ссылка на verification>.
Тестовые заглушки/scripted model отдельно от integration/live-model evidence: <...>.
Независимый reviewer, findings/severity, исправления или явное risk acceptance: <...>.
Design approval: <не получено до явного источника>.
