# Ограничения Java

Reusable template; Java не выбрана. Применяется только для выбранного Java-компонента вместе с [общими правилами](../constraints.md).

## JVM, типы и данные

- Зафиксируйте JDK/JVM, target release, vendor и dependencies. Preview/incubator API не считаются стабильными или доступными в другой JVM. Build target и runtime должны быть совместимы.
- References допускают `null`; unboxing может дать NPE. Generics используют erasure; raw types/unchecked casts не валидируют внешний объект. Проверяйте DTO/tool input при runtime.
- Primitive integer overflow не становится автоматической бизнес-ошибкой. Задайте checked arithmetic/conversions и ranges; для точных величин согласуйте decimal scale/rounding.
- Учитывайте equals/hashCode, identity, mutable keys и mutability коллекций. `final` reference не означает deep immutability. [JLS: Types, Values, Variables](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html).
- Различайте UTF-16 units/code points/graphemes; задайте charset. Время храните с явной zone/offset, deadlines не стройте только на wall clock.

## Concurrency, async и память

- Соблюдайте JMM: visibility, happens-before и safe publication. `volatile` не делает произвольный составной read-modify-write атомарным; выбирайте locks/atomics по инварианту. [Threads and Locks](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html).
- Ограничивайте executors, queues и downstream concurrency. Future timeout не доказывает остановку внешней операции; interrupt кооперативен и не должен терять cancellation semantics.
- Virtual threads не ускоряют CPU-bound вычисления и не отменяют DB/service limits. Pinning для synchronized/native calls и thread-local costs сверяйте с выбранным JDK: ограничения одной версии нельзя переносить на все. [Virtual Threads](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html).
- GC не гарантирует отсутствие пауз/немедленное освобождение внешних ресурсов. Учитывайте heap/native memory, retained references и thread-local lifetime; измеряйте latency на реальной JVM.
- Для AutoCloseable используйте try-with-resources/явный контракт, сохраняя primary/suppressed exceptions. [AutoCloseable](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/AutoCloseable.html).

## Ошибки, безопасность и поставка

- Разделяйте checked/unchecked domain failures и JVM errors; не ловите Throwable ради безусловного продолжения. Unknown side-effect outcome не превращается в successful cancellation. Shutdown завершает executors/resources в пределах deadline.
- Недоверенные deserialization, reflection/class loading, expression engines и process execution требуют отдельного защищённого разрешённого контракта. SQL параметризуется, tools ограничиваются schema/policy.
- Maven/Gradle, framework/ORM и JNI выбираются по утверждённому стеку. Фиксируйте dependency resolution/provenance, classpath/module compatibility и запуск packaged artifact на целевой JVM.
- JIT/warmup, boxing, allocations и GC влияют на измерения. Не обещайте steady-state performance по холодному запуску; native image — отдельная технология со своими resource/reflection constraints.

Проверка: project build/test и существенные concurrency/timeout/resource cases; JVM compatibility, real-tool integration и performance имеют отдельные доказательства. Для Markdown JDK не устанавливается.
