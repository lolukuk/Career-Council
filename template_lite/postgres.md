# Ограничения PostgreSQL

Reusable template; PostgreSQL не выбран. Version/schema/extensions/ORM неизвестны. Используйте [общие ограничения](constraints.md) и материализованный профиль на основе postgres-engineer только при подтверждённом выборе PostgreSQL.

- Определите source of truth/state ownership. Evidence, model suggestions и audit различаются; JSONB/text модели не становятся доверенным фактом автоматически.
- Constraints/keys/transactions поддерживают реальные инварианты. Read Committed может видеть изменённое состояние между запросами транзакции; Serializable может завершаться serialization failure и требует предусмотренного retry всей транзакции. [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html).
- Конкурентная проверка «нет записи → вставить» опирается на constraint/locking protocol. Определите idempotency scope/key/uniqueness и conflict/result/retry semantics.
- DB transaction не атомарна с произвольным external tool. Unknown outcome требует downstream contract/reconciliation; outbox не гарантирует exactly-once delivery.
- Согласуйте SQL ranges/numeric scale/null/default/timezone/bytes/text/JSON с фактически выбранными потребителями.
- Используйте parameterized SQL/least privilege. Модель не выбирает произвольные SQL/таблицу/роль вне tool schema/policy; secrets/audit имеют access/retention rules.
- Pool sizes, long transactions, locks/deadlocks и retries ограничиваются требованиями. Timeout клиента не доказывает отсутствие commit.
- Миграция описывает compatibility/locks/data impact/rollout/rollback/recovery. Разрушительные операции требуют имеющегося разрешения.
- ORM/migration tool/RLS/pgvector/extensions выбираются по задаче. Индексы/performance подтверждаются query patterns и измерениями.

Проверка migrations/constraints/transactions — на разрешённой test DB с указанной версией. SQL review/mock не равны executed integration. Для подготовки этого набора PostgreSQL не устанавливается.
