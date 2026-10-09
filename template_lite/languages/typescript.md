# Ограничения TypeScript

Reusable template; TypeScript не выбран. Компонент/runtime неизвестны. Применяйте [общие ограничения](../constraints.md) только для выбранного TypeScript-компонента.

- Types стираются: annotations/assertions не валидируют runtime data. Проверяйте DTO/JSON/tools; any/as/non-null assertion/ts-ignore не доказывают корректность. [TypeScript Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html).
- Зафиксируйте compiler, tsconfig/target/strict/null settings, modules и package manager/lockfile. Compile-time API declarations не гарантируют runtime availability.
- Node.js/browser/Deno/Bun выбираются отдельно: APIs/permissions/globals/deployment guarantees не переносятся автоматически.
- Для Node.js не блокируйте event loop CPU/sync I/O; async calls могут расходовать bounded worker pool. Назначьте concurrency/backpressure. [Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop).
- Обрабатывайте rejected promises, task lifetime и cancellation. AbortSignal/timeout не гарантируют отмену неподдерживающего API/внешней записи. Не допускайте unbounded retries/Promise.all.
- Number имеет границы точности целых; BigInt/decimal требуют wire format. Разведите undefined/null/missing; согласуйте JSON/bytes/dates/strings с фактически выбранными компонентами.
- Shared mutation/closures/workers требуют ownership/concurrency analysis; readonly не означает runtime freeze.
- Ограничьте caches/listeners/timers/sockets/input/context. GC не завершает протокол. Не переносите secrets/permissions в неразрешённый client bundle/model context.
- Фиксируйте dependencies/native addon compatibility; eval/dynamic import/process/package scripts исполняются только по разрешённому контракту.

Проверка: заданные build/typecheck/tests и существенные runtime/scripted-model cases. Typecheck не доказывает policy/integration/performance. Для Markdown эти команды не запускаются.
