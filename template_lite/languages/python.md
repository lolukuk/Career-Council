# Ограничения Python

Reusable template; Python не выбран. Применяется только к назначенным Python-компонентам вместе с [общими правилами](../constraints.md). Runtime, версия, framework и package manager ещё не выбраны.

## Типизация и данные

- Type hints сами по себе не проверяют значения при выполнении. Валидируйте внешние DTO/tool arguments/results; `Any`, cast и type-ignore не закрывают нарушение контракта. [typing](https://docs.python.org/3/library/typing.html).
- Различайте `None`, missing field, truthiness и `bool` как подтип `int`. Не смешивайте identity/равенство и shared mutable objects/копии.
- Не используйте общий mutable default для независимых вызовов; проверяйте closure capture, shallow copy, исчерпаемые iterators/generators и mutable class state.
- `int` ограничен ресурсами, а не SQL-разрядностью; float имеет погрешность. Задайте ranges/conversions и decimal contract для точных величин.
- `str`/`bytes` различаются; code points не равны graphemes. Задайте encoding и timezone на границах. [Модель данных](https://docs.python.org/3/reference/datamodel.html).

## Конкурентность, async и ресурсы

- Для CPython установите GIL-enabled/free-threaded режим; не переносите выводы на все реализации. При GIL CPU-bound Python-код не получает обычного многоядерного ускорения от threads; native extensions могут вести себя иначе. Free-threaded build не делает произвольный код thread-safe, несовместимое расширение может вновь включить GIL. Проверяйте зависимости и реальную синхронизацию. [Free threading](https://docs.python.org/3/howto/free-threading-python.html), [threading](https://docs.python.org/3.13/library/threading.html).
- `async` не превращает blocking I/O/CPU-код в неблокирующий. Используйте утверждённый executor/process approach; ограничивайте задачи и queues.
- Cancellation кооперативна. Не подавляйте `CancelledError` ради success; выполняйте cleanup с сохранением отмены. Timeout не доказывает прекращение thread/native/external operation. Управляйте background tasks и их результатами. [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html).
- Закрывайте files/sessions/DB connections через context manager или явно; не полагайтесь на момент GC/`__del__`. Учитывайте cycles и retained objects в caches/generators. [Финализация](https://docs.python.org/3/reference/datamodel.html).
- Для multiprocessing проверьте фактический start method, entry point/import safety и сериализацию. Не передавайте открытую DB connection между процессами и не предполагайте `fork` на Windows.

## Ошибки, безопасность и поставка

- Классифицируйте exceptions, сохраняйте cause; широкий `except` не должен возвращать fake success. Повторы — только по согласованной transient/side-effect policy и с бюджетом.
- Недоверенные eval/exec, dynamic import, pickle и YAML object construction запрещены без отдельно разрешённого защищённого контракта. Процессы вызывайте отдельными аргументами, SQL — с параметрами.
- Фиксируйте interpreter/dependencies, не используйте global environment по умолчанию. Проверьте wheels, ABI/native libraries, ОС/CPU, free-threaded compatibility и ограничения упаковки.
- Ограничивайте input/context, recursion, allocations и cache/history. CPU throughput и portable EXE требуют измерений/нативного доказательства.

## Проверка задания

Используйте реальные project checks: необходимый static checker/lint, существенные unit/scripted-model cases, cleanup/cancellation и integrations. Thread/process safety и packaged runtime требуют отдельных доказательств. Для Markdown toolchain не устанавливается и эти checks не запускаются.
