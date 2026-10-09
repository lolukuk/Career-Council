# AI Tunnel и OpenAI: дизайн и план PI02

2026-10-09. Продолжение после принятого прототипа. PI01 intake находится в provider-integration.md; независимое исследование — handoffs/provider-review/result.md. Здесь конкретное решение на согласование. Адаптеры ещё не реализованы, реальные LLM-вызовы не выполнялись.

## Пользовательский интерфейс и автономность

Существующий CLI, оба провайдера, название модели задаёт пользователь; default model и автозамены нет. Подготовленный council/.env содержит LLM_PROVIDER=aitunnel|openai, LLM_MODEL, AITUNNEL_API_KEY, OPENAI_API_KEY. .env.example без секретов, .env исключён через .gitignore. После реализации --mode model читает настройки, --provider/--model переопределяют выбор. Переменные окружения выше .env. Ключ исключительно из поля выбранного провайдера; старый LLM_API_KEY не удаляется, но не используется. Нет ключа/модели — ошибка до подготовки досье и генерации. Сейчас CLI эти поля ещё не читает.

Два адаптера, фабрика и небольшой загрузчик настроек поверх уже установленного async httpx; он объявляется прямой зависимостью. Нового SDK/сервиса/БД/UI не нужно. Root — автор; существующий отдельный reviewer — независимые design/plan/final checks. Новых субагентов нет. Провайдер не получает инструментов; адаптер только сериализует frozen Request, вызывает фиксированный endpoint и разбирает ответ. Прежние пять персон, единогласие по одной версии, evidence/objection guards и финальный выбор человека остаются.

## Решение о контексте

Предлагается **вариант B**, который требует явного согласования изменения прежнего guard для AI Tunnel:

| Провайдер | Честная гарантия |
|---|---|
| OpenAI | server_exact: Responses + авторитетный async input token count перед генерацией, reliable_token_accounting=true. |
| AI Tunnel | server_enforced: Chat Completions, reliable_token_accounting=false, preflight_count=null. Точный универсальный предварительный count не подтверждён; переполнение отклоняет сервер. |

Альтернатива **A** сохраняет исходный строгий guard: AI Tunnel не генерирует до появления документированного точного счётчика для выбранной модели. До согласования B прежние ограничения действуют. Оценка bytes или чужой tokenizer не становится certified count.

Обе политики: serialized Request ≤32768 bytes, резерв ответа2000 tokens, ≤3 rounds, ≤50 локальных попыток, ≤2 attempts одного frozen input, ≤45 секунд на попытку и600 секунд обсуждения. Дополнительный wire-body cap131072 bytes ограничивает schema/serialization expansion. Overflow завершает incomplete без обрезки доказательств. OpenAI exact count + reserve проверяется против отдельного application token budget32768 — это лимит приложения, не утверждение о реальном окне любой введённой модели. Если окно модели меньше, сервер может отказать; truncation=disabled. Unsupported count не заменяется оценкой.

AI Tunnel: пользовательский ID должен присутствовать в публичном chat-каталоге с валидными context_size/max_output; max_output вмещает резерв. Метаданные фиксируются в trace, но не доказывают count. Запрещены auto/latest/preset, fallback models, произвольные base URLs, замена модели и transforms. Context-compression явно отключается: plugins=[{"id":"context-compression","enabled":false}], согласно официальному transforms contract; другие plugins не передаются. Другая returned model — понятный отказ с requested/returned ID, без допуска результата в обсуждение.

## Контракты адаптеров

OpenAI endpoints https://api.openai.com/v1/responses и /responses/input_tokens; AI Tunnel https://api.aitunnel.ru/v1/chat/completions; публичный каталог https://api.aitunnel.ru/public/aitunnel/models. Каталог без досье — внутри bounded preparation lifetime; count и generation вместе входят в одну attempt lifetime. Count uses тот же model/input/instructions/schema, что generation. Минимальное async preflight расширение adapter interface совместимо с существующими scripted/test adapters; task создаётся до preflight. Синхронный count не делает HTTP. HTTP-client без скрытых retries, ограниченный response-body и client cleanup. Expiry/cancel отбрасывает поздний результат, как в принятом прототипе.

Provider JSON Schema — транспортная нормализация Pydantic schema (required/additionalProperties, optional/default, tuple constructs). Локальные исходные DTO, длины, tuple cardinality, citations и consensus invariants сохраняются даже если транспортная схема слабее. Nullable placeholders optional полей преобразуются обратно к defaults только по заранее вычисленной карте; required/null-allowed fields не переписываются. Unsupported schema/model — terminal, без перехода к свободному тексту или другой модели. Refusal, length/incomplete, tool calls, multiple alternatives, отсутствие текста/usage не являются валидным решением.

Auth/configuration/unsupported model/schema/context overflow — terminal, без retry. 429/5xx/network timeout — прежний bounded retry того же frozen input. Ошибка возможна внутри AI Tunnel HTTP200: проверять envelope до content. HTTP400 неоднозначен, не считать его всегда context overflow. Ошибки выводить безопасными кодами, без raw response/error body, заголовков, ключа или досье. Ключ вне Request/trace/report/repr. JSON/DTO/citation repair сохраняет max2; содержательное возражение не retry ради согласия.

Trace: provider, requested/returned model, accounting policy, preflight count/null, local dispatches, usage каждого полученного ответа, включая не принятые в обсуждение. AI Tunnel cost_rub — только сообщённая провайдером стоимость; balance не сохраняется. Usage при ошибке/отмене может быть unknown, не ноль. Count operations не смешиваются с generation usage. **50 локальных attempts не гарантируют50 upstream calls или денежный потолок:** AI Tunnel документирует внутренние retries429. Локальная отмена не доказывает остановку генерации/списаний на сервере. Отчёт показывает эти ограничения.

## Минимальный последовательный план

| Задача / владелец | Scope | Критерий готовности |
|---|---|---|
| PI03/root | settings/providers/factory/schema transport, env.example, requirements/lock | HTTP fixtures: key isolation, no-key/no-model, wire formats, schema/refusal/usage/identity/errors, no secrets. |
| PI04/root, послеPI03 | model async preflight/capabilities, runtime usage, CLI lifecycle/report/README | Fixtures: count+generation one deadline, overbudget/context overflow без cropping, cancellation/late payload,401 terminal,429 bounded. |
| PI05/root, послеPI04 | целевые сценарии и существующий regression suite | .venv-consensus/Scripts/python.exe -m pytest council/tests -q → exit0; прежние scripted isolation/unanimity/dissent guards. |
| PI06/existing reviewer, послеPI05 | actual code/evidence review | Независимый PASS либо исправления и повтор затронутых проверок. |

Проверки добавляются в существующие council/tests с mock HTTP transport, без нового eval framework. Они доказывают границы адаптеров и protocol regression, не качество живой модели. Автоматической платной проверки нет: пользователь должен выбрать модель и заполнить ключ прежде отдельного live запуска. Пока не заявляются connectivity или live reasoning quality. Исторические54 tests относятся к принятому прототипу2026-10-08, свежих PI02 результатов нет.

## Источники и gates

[OpenAI counting](https://developers.openai.com/api/docs/guides/token-counting), [count API](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs); [AI Tunnel API](https://aitunnel.ru/docs/api-reference), [schema](https://aitunnel.ru/docs/structured-outputs), [models](https://aitunnel.ru/docs/models), [tokenizer](https://aitunnel.ru/tokenizer), [transforms](https://aitunnel.ru/docs/transforms), [limits](https://aitunnel.ru/docs/limits), [errors](https://aitunnel.ru/docs/errors). Independent reviewer оставил evidence server overflow/refusal и gateway retries в provider-review/result.md.

Пользователь уже подтвердил требования обоих провайдеров и самостоятельный ввод модели. Прямое объявление существующего httpx входит в план; новый stack/SDK не выбирается. PI02 independent design review — PASS conditional explicit approval B; proposed plan review — PASS, material documentary blockers отсутствуют (handoffs/provider-review/design-plan-result.md). Это documentary evidence, не проверка реализации. Design06 и execution11 ожидают явного согласия с вариантом B и этим планом; один явный ответ может закрыть оба пользовательских checkpoint, независимые проверки не отменяются. Приёмка15 исходного прототипа сохранена.

2026-10-09 execution update: пользователь явно утвердилB/этот план (AI Tunnel для проверки, проверяющий может использоватьOpenAI);06/11 accepted. PI03–PI05 implemented, full103 passed24.19s exit0 после actual PI06 findings; независимое final closure ожидается. Здесь исторический дизайн, текущее actual evidence в provider-verification.md.


## PI07 — явный условный тестовый профиль AI Tunnel (2026-10-09)

Прямое user steering после actual live failures: «Для Ai Tunnel подойдет условность, она не будет использована в проде». Это авторизует ограниченное test-only допущение для gateway accounting; не отменяет требования к источникам, пяти персонам и реальному согласованию. Новый стек/сервис/агент не нужен. Перед кодом — независимый review существующим reviewer, затем root implementation/full applicable verification/live attempt/review; ранее принятое prototype15 сохраняется.

Конкретный контракт: optional CLI `--aitunnel-test-mode`, default false, работает только с выбранным AI Tunnel и mode=model. Прямой OpenAI с этим флагом отвергается до раскрытия досье. Library Settings имеет явный bool, его producer также проверяет AIT-only. .env/keys/model/default reasoning не меняются; текущий запуск явно использует flag и none.

Запрашиваемый output cap остаётся Config.output_tokens=2000 и передаётся провайдеру. В opt-in профиле фактический reported output до жёсткого потолка8000 принимается к обычной DTO/citation validation, а превышение запрошенного cap явно учитывается.8000 соответствует существующей верхней границе output budget в Config; конечный test ceiling выбран для ограниченного прототипа, не для prod. >8000 terminal, missing/noninteger/negative counts, model mismatch, refusal/truncation и malformed payload по-прежнему отвергаются. Тестовая уступка не обещает денежный потолок/точность gateway counts/остановку remote billing.

Capabilities.output_limit_policy='strict' либо 'aitunnel_test'; check_adapter допускает вторую исключительно provider=aitunnel + server_enforced + reliable=false. Frozen helper вычисляет effective acceptance ceiling (strict=request.output_tokens, test=8000), используется и provider, и runtime. Test flag сам по себе не изменяет output requested/certified OpenAI context reserve; exact count+generation OpenAI и strict custom adapters сохраняются. Serialized Request32768bytes, wire131072bytes, body caps,2 retries,50 attempts,45s/600s, source limits/rounds3 без изменений.

Snapshot/trace фиксируют policy/ceiling, каждой usage записью requested_output_tokens и output_limit_exceeded (при известных output counts, иначе null). Report явно помечает тестовый допуск, cap2000/ceiling8000/число excess ответов; default strict profile не маркируется условным. Failed historical traces сохраняются. DTO/cardinality/citation exact substring/transitive pinning/original-position independence/unanimity/exact version guards без исключений. No autoapprove/fallback/fake answers.

Atomic route serial root PI07a settings/CLI/model capability/provider/runtime/report; PI07b existing provider/regression fixtures + exact full `.venv-consensus/Scripts/python.exe -m pytest council/tests -q`; PI07c один full real-dossier CLI `--mode model --reasoning-effort none --aitunnel-test-mode`, honest report даже при failure/incomplete/no_consensus; PI07d existing reviewer independent final. Tests: opt-in excess accepted only AIT, defaultAIT/OpenAI rejected excess,>8000 rejected, wrong-providerflag early reject, missing usage/refusal/citation/consensus unchanged, profile/excess actual trace/report. Live quality не объявляется из одной проверки. Остальные сценарии доступны existing scripted demos, уже проверены accepted prototype; не запускать их заново без regression причины.

User intent/exception authorized; independent design/plan verdict pending. Root не начинает этот material delta до review PASS. Если реальный run блокируется новым локальным context/DTO guard — сохранить причину и исправлять только в авторизованном guard contract, не переносить test accounting exception на provenance/consensus.
