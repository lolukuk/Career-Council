# Ограничения Go

Reusable template; Go не выбран. Применяется только для выбранного Go-компонента вместе с [общими правилами](../constraints.md).

## Типы и данные

- Зафиксируйте toolchain, go/toolchain directives, GOOS/GOARCH, modules и cgo requirements. Семантику loop variables проверяйте по версии языка, не переносите поведение старого кода на все версии.
- Zero value не всегда допустим в домене. Различайте nil pointer, typed nil внутри interface и nil interface; валидируйте DTO/missing/null/zero и error contract.
- Map iteration не даёт стабильного порядка; slices могут разделять backing array. Проверяйте aliasing/append/copy/ownership; не копируйте struct с используемым mutex вопреки его контракту.
- int имеет platform-dependent width; задайте ranges/conversions/overflow/decimal semantics. Generic JSON decoding не гарантирует сохранение произвольной числовой точности.
- String — bytes; byte index/rune не равны grapheme. Согласуйте encoding/validation. [Go Specification](https://go.dev/ref/spec).

## Goroutines, channels и ресурсы

- Goroutine не имеет автоматического общего lifecycle с caller. Ограничивайте число/queues и задайте завершение каждой: возможны leaks и зависшие send/receive.
- Shared state синхронизируется по memory model; goroutines/channels не исключают data race сами по себе. Для maps/shared slices задайте схему доступа. [Memory Model](https://go.dev/ref/mem).
- Для channels назначьте владельца close, buffer/backpressure/shutdown. Send в closed channel вызывает panic; nil channel может блокировать send/receive. Проверяйте select/closed receive/cancellation. [Channel semantics](https://go.dev/ref/spec).
- Context распространяет cancellation/deadline только в участвующий код. Сохраняйте parent, вызывайте cancel для освобождения ресурсов; values не служат набором optional parameters. Отмена не доказывает отсутствие внешнего side effect. [context](https://pkg.go.dev/context).
- Defer выполняется при выходе из функции, не каждого блока цикла. Не накапливайте open resources в долгом цикле; GC не заменяет бизнес-lifecycle.
- sql.DB — управляемый connection pool. Ограничивайте его по нагрузке, закрывайте Rows/transactions, проверяйте итоговые errors. Connection limit может создать ожидания/deadlock при неверном алгоритме. [Database connections](https://go.dev/doc/database/manage-connections).

## Ошибки, безопасность и поставка

- Expected failures возвращайте через error, сохраняйте cause для errors.Is/As. Panic/recover не заменяет domain errors; recovery не является универсальным catch между goroutines.
- Network/process/file tools имеют deadlines, size/address/path limits и параметризованные вызовы. Shell/SQL не выбираются недоверенным текстом модели.
- Согласуйте go.mod/go.sum, dependency provenance, cgo/native ABI/linker и build tags. Cross-build не гарантирует переносимость всей программы; target execution проверяется отдельно.
- Измеряйте GC/allocations, escapes, contention и lock order; успешная сборка не доказывает latency или отсутствие leaks.

Проверка: project build/test/vet и существенные negative/concurrency cases. `go test -race` назначается при реальном shared-state risk на поддерживаемой платформе; детектор видит выполненные пути, не доказывает отсутствие всех races. [Race Detector](https://go.dev/doc/articles/race_detector).

Deadlines, goroutine shutdown, real-tool/DB integrations и target runtime проверяются отдельно. Для Markdown Go не устанавливается.
