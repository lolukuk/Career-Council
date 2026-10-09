# Общий спектр ограничений

Применяйте вместе с [поведением](agent-behavior.md). Отличайте требование продукта, технический предел языка и рекомендацию. Конкретную применимость уточняйте по принятой версии и среде.

| Технология | Статус | Правила |
| --- | --- | --- |
| Python | Reusable template; не выбран | [python.md](languages/python.md) |
| TypeScript | Reusable template; не выбран | [typescript.md](languages/typescript.md) |
| PostgreSQL | Reusable template; не выбран | [postgres.md](postgres.md) |
| Java | Справочник; использование не выбрано | [java.md](languages/java.md) |
| Rust | Справочник; использование не выбрано | [rust.md](languages/rust.md) |
| Go | Справочник; использование не выбрано | [go.md](languages/go.md) |

В задании/дизайне отметьте для каждой существенной категории `applicable`, `not-needed` с причиной или `unknown` с влиянием. Не превращайте unknown в гарантию.

## Категории

| Область | Что должен установить агент |
| --- | --- |
| Версии и среда | Реализацию языка, compiler/runtime, edition/release/MSRV, ОС/CPU и минимальные версии API |
| Типы и схемы | Static/runtime validation, null/absence, generics, mutability, schema version и defaults |
| Числа | Width, overflow, checked conversion, float/decimal, NaN/Infinity, precision и SQL/JSON ranges |
| Текст и время | Bytes/Unicode/graphemes, encoding, нормализацию при необходимости, timezone, wall/monotonic clock |
| Память и ресурсы | Ownership/GC, циклы/ссылки, allocation limits, files/sockets/connections и освобождение |
| Конкурентность | Memory model, races, locks/atomics, visibility, deadlock/livelock, ordering и concurrency limits |
| Async | Blocking calls, scheduler/executor, CPU/I/O separation, lifetime задач, backpressure и queues |
| Отмена | Propagation, deadlines, cooperative cancellation, cleanup, shutdown и unknown side-effect outcome |
| Ошибки | Expected errors/exception/panic, retry classification/budget, partial failure и cause |
| I/O и сеть | Лимиты размера/времени, streaming, разрешённые адреса/пути, TLS и protocol compatibility |
| БД и side effects | Transactions/isolation, constraints, idempotency, concurrency, reconciliation и audit |
| Безопасность | Trust boundaries, validation, deserialization/code execution, injection, secrets и least privilege |
| Зависимости/сборка | Lockfiles, provenance/licensing, toolchain, native dependencies/FFI/ABI, features и reproducibility |
| Портируемость | OS paths/signals/process spawning, CPU width/endian/ABI, libraries, target execution |
| Производительность | Измеренные latency/memory/throughput, cold start, GC/JIT, allocations/boxing и CPU |
| Наблюдаемость | Trace IDs, audit, redaction, log/cardinality/size limits и диагностические доказательства |
| Проверка/эксплуатация | Команды проекта, test environment, failure/race cases, integration/live boundaries, rollback |

## Межъязыковые контракты

Не переносите внутренний объект языка как будто семантика одинакова в другом языке. Согласуйте DTO/schema, field names, optional/null/default, range/decimal format, UTF-8/bytes, timestamp/zone, enum/unknown values, error codes, event ordering, versioning и backwards compatibility.

Timeout и локальная отмена не доказывают отмену внешней записи. Idempotency/reconciliation задаются контрактом исполнителя, а не автоматически типизацией, GC или borrow checker.

## Правила агента

- Не добавляйте технологию ради использования всех шаблонов. Не устанавливайте toolchains для документальной подготовки этого набора.
- Не обходите компилятор/type checker/guard необоснованными cast/ignore/unsafe/unchecked conversion. Необходимое исключение требует инварианта, границ и проверки.
- Недоверенный ввод не выбирает команду, класс, импорт, SQL, файл или сетевой адрес вне утверждённого tool contract. Prompt не заменяет runtime enforcement.
- Не объявляйте систему race-free, memory-safe, portable, performant или exactly-once по названию языка.
- Назначайте проверки существенных свойств командами проекта; не делайте все диагностические средства обязательными для каждого задания. Unrun/failed/skipped отмечайте явно.

Новый существенный предел среды добавляется в constraints конкретной задачи и передаётся архитектору. При противоречии документации и поведения сначала уточняйте version/environment, а не скрывайте проблему изменением теста.
