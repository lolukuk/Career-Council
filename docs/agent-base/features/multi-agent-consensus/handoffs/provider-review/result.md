# PI01 narrow independent investigation — token/context preflight

2026-10-09. Reviewer: existing consensus_design_review, independent от root author. Input: provider-integration.md draft PI01 и current ModelAdapter/check_adapter/invoke. Accepted prototype не переоткрывается. Scope — documentary provider contract investigation; product files read-only.

**Вывод:** прямой OpenAI имеет документированный authoritative Responses input count. Для произвольного user-defined AI Tunnel model надёжный универсальный preflight count **не подтверждён** доступными официальными источниками. Сохраняя исходный guard, безопасный minimal default — capability refusal до отправки досье для модели без установленного accounting contract. Это реальная открытая provider contract граница, а не отказ выбрать «подходящую» модель за пользователя.

## Primary evidence

1. [OpenAI input token count API](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count) документирует POST `/responses/input_tokens` и `object=response.input_tokens`/integer count; request принимает model/input/instructions/tools/text format. [OpenAI token-counting guide](https://developers.openai.com/api/docs/guides/token-counting) описывает предварительный подсчёт. Count должен относиться к тому же provider wire input/schema, что генерация, не к условному числу символов внутреннего Request.
2. [AI Tunnel tokenizer](https://aitunnel.ru/tokenizer) описывает browser-side o200k_base; отдельно предупреждает о других tokenizer у Claude/Gemini/DeepSeek и дополнительном message framing. Точное число для выбранной модели предлагается получать из **usage ответа**. Это post-request evidence, не независимый preflight bound для произвольного payload/model.
3. [AI Tunnel model catalog](https://aitunnel.ru/docs/models) документирует публичный GET `/public/aitunnel/models[/chat]` и `context_size`/`max_output`. Это metadata о лимитах, не mapping exact tokenizer/version/chat/schema serialization. Документация также допускает auto/latest/presets; такие IDs не доказывают фиксированный underlying model. Фактический public catalog200 уже recorded root; reviewer его повторно не запрашивал.
4. Прочитаны [AIT API reference](https://aitunnel.ru/docs/api-reference) и [LLM docs index](https://aitunnel.ru/llms.txt): аналогичный universal input-token-count метод не найден. Это отсутствие документального подтверждения, **не доказательство**, что неизвестный маршрут никогда не существует. OpenAI-compatible `/responses` не подтверждает все subresources.
5. [AIT context compression](https://aitunnel.ru/docs/transforms) описывает удаление/усечение middle messages; plugin по умолчанию выключен, без него слишком длинный input возвращает ошибку. Для данного протокола compression противоречит сохранению pinned context. Server rejection полезен как дополнительная защита, но сам по себе не даёт точный preflight count и не подтверждает отсутствие тарификации/forwarding.
6. [AIT Structured Outputs](https://aitunnel.ru/docs/structured-outputs) не гарантирует одинаковую жёсткость `strict` у всех моделей/endpoints. Поэтому model response всегда проходит существующие strict DTO/citation/consensus validators, даже при успешном schema capability probe.

Ссылки открыты/прочитаны, не использованы как unopened search snippets. Для сравнения OpenAI применён OpenAI Docs; технические факты взяты из официальной документации двух провайдеров. Ключи, raw .env, authentication headers или пользовательское досье никуда не отправлялись.

## PI-F01 — P2: универсальная certified AIT strategy пока не установлена

- Trigger: пользователь вводит произвольный AIT model ID, catalog содержит большой context_size, приложение считает o200k_base/UTF-8 bytes плюс произвольный overhead и ставит reliable_token_accounting=True. Неизвестный backend tokenizer, gateway system additions, schema/framing или alias routing меняют реальный input cost.
- Effect: обещанный preflight guard опирается на недоказанный bound. Post-response usage, большой byte margin, однократный успешный request и наличие catalog200 этот контракт не устанавливают.
- Smallest safe gate: `accounting_strategy=unsupported` для неподтверждённого exact model/route profile. Пользовательский ID принимается как настройка, но model-run отвергается понятно **до** dossier/count/generation network disclosure. Не выбирать другой model, не скрывать отказ lexical/scripted fallback и не принимать вручную env boolean «certified=true» за evidence.
- Supported unlock: documented provider authoritative count для exact route/model **либо** complete verified per-model tokenizer + gateway role/schema/framing/hidden-input contract, дающий доказуемый bound. Profile фиксирует источник/version/context_window/max_output/route/accounting implementation digest. Catalog TTL/identity refresh не переносит автоматически certification на новый backend/alias.
- Disposition: genuine unresolved AIT contract; root должен отразить gate/ограничение в concrete design, а не назвать произвольные модели проверенными. Direct OpenAI интеграция и offline adapter/config work могут продолжаться независимо.

## Минимальная capability/probe стратегия

1. Доверенные base URLs фиксированы отдельно для AIT/OpenAI; ключ только выбранного provider. Catalog чтение не требует ключа. Не переносить AIT-key в прямой OpenAI count или обратно, не считать provider name частью произвольного URL.
2. До run валидировать explicit user model ID, positive context/output limits и выбранную certified accounting strategy. Stable profile не означает hardcoded default model: никакого автоматического выбора модели за пользователя.
3. Возможный будущий **count-only** probe допускается только после подтверждения именно count semantics выбранного endpoint и применимого разрешения. Synthetic nonprivate input; no generation, no fallback. 404/405/501, missing/wrong-shaped count, unsupported model/schema → clear capability refusal. Несколько count-only fixture inputs могут проверить parser/transport, но не доказать универсальную правильность undocumented tokenizer. Сам guessed `/responses/input_tokens` с HTTP200 не разрешает поставить certified=true.
4. На каждый model attempt одна immutable provider payload builder: identical model/input/system/schema/options для count и generation; payload digest traceable. Count+output reserve должны укладываться в context_window и model max_output. Config byte cap сохраняется как отдельный bound; JSON/network bodies/header secrets не смешиваются с модельным контекстом.
5. Не включать context-compression/auto fallback/plugin transforms; не отправлять preset/auto/latest ID как будто frozen model. Если requested alias допускается, отдельно раскрыть routing identity и не наследовать profile fixed model без подтверждения route contract.
6. Current `count_tokens` interface синхронен. Remote authoritative count **нельзя** выполнять блокирующим HTTP внутри event loop: новая async preflight должна входить в уже runtime-owned absolute attempt/run expiry и budget reservation, cancellation/late-result policy R13–R15. Не считать preflight бесплатным по времени/сетевым попыткам и не начинать timeout только после его завершения. Это bounded adapter-interface correction, не новая служба/agent.

## Не считать решением

- bytes/4, JSON bytes×произвольный коэффициент, 3–7 overhead «на все модели», one-time calibration по billed response;
- cross-provider подсчёт direct OpenAI для AIT gateway model на основании одинаковой строки имени;
- `max_tokens=1`/empty generation для измерения prompt usage: это LLM request, dossier disclosure и потенциальная оплата, а не count-only preflight;
- compression для вмещения обязательных аргументов или postfactum output usage как разрешение уже состоявшейся oversized dispatch.

## Evidence status и next step

Выполнены только read-only local interface/intake и official web documentation reads. Никаких tests/CLI/моделей/count POST/generation/keys/install/product edits; новых агентов нет. Public catalog connectivity evidence root + provider HTTP fixtures не доказывают live schema support или reasoning quality. Даже успешный future authenticated count/schema smoke будет integration evidence, а не decision quality пяти персон.

Рекомендуемый root design: direct OpenAI async authoritative count route; AIT отдельный fail-closed capability registry с явно unresolved strategy для неизвестных моделей. Если требуется обещать работающий model-run для любой AIT модели прямо сейчас, сохранение прежнего universal preflight guarantee несовместимо с имеющимися evidence: необходимо сначала достать документированный provider contract, либо отдельно согласовать более слабый server-enforced overflow contract. Reviewer такое ослабление не выбирает молча.

## Конкретная минимальная развилка перепланирования

Root запросил проверить reviewable option с явно различными гарантиями. **Option B ниже документально обоснован как кандидат нового provider design**, но не сохраняет прежнюю универсальную exact-preflight гарантию и ещё не одобрен пользователем. Original PI-F01 evidence остаётся: universal AIT count не установлен.

| Policy | OpenAI | AI Tunnel | Что пользователь получает |
|---|---|---|---|
| A — исходная строгая | Responses async authoritative count, reliable=true при проверенном contract/context metadata | Unsupported accounting → отказ до dossier до появления exact per-model contract | Прежний guard без ослабления; AIT config/connectivity ещё не равен рабочей генерации. |
| B — явно изменённая AIT | То же server_exact async preflight | catalog-selected fixed chat ID, policy=server_enforced, reliable=false; context limit обеспечивает gateway, input count до отправки неизвестен | Можно отправить bounded AIT запрос, сохранив local byte/output/protocol guards; возможен server context refusal после отправки dossier. |

### Почему Option B допустим как честный контракт

[AIT limits](https://aitunnel.ru/docs/limits) описывает model-specific input token limits. [Compression documentation](https://aitunnel.ru/docs/transforms) указывает error для overlong prompt при выключенном plugin. [Errors](https://aitunnel.ru/docs/errors) включает слишком длинный prompt в400; также HTTP200 может содержать error после начала generation. Это основания полагаться на gateway **rejection policy**, но не на предварительный точный count, неоплачиваемость отказа или отсутствие upstream обработки. Такой уровень гарантии должен быть указан до первого AIT dispatch.

Минимальная явная capability модель:

- `token_policy=server_exact`: certified count strategy и reliable=true; count+output reserve проверяются перед generation; remote count await входит в absolute attempt expiry.
- `token_policy=server_enforced`: только явно разрешённый AIT provider policy, reliable=false, positive catalog context_size/max_output, frozen selected ID/catalog digest и API route; preflight_count=null. Этот путь допустим только после user approval revised policy, а не env-флаг, случайно обходящий check_adapter.
- unsupported/default при отсутствии exact strategy **и** разрешения server_enforced → отказ до dossier. Ни один путь не возвращает0 вместо неизвестного count и не именует estimate authoritative.

Для B: полный existing serialized Request byte cap сохраняется; provider wire request/output также ограничены, requested output не выше config reserve/catalog max_output. При невозможности вместить pinned closure локально → прежний incomplete, нельзя послать усечённый контекст. То, что byte cap соблюдён, не доказывает token fit. Actual input/output usage mandatory recorded postresponse и labeled `observed`; если actual usage отсутствует/невалиден, ответ не принимается как валидный модельный результат.

Send один user-provided fixed catalog chat `model`, никаких `auto`, `~…latest`, `models` fallback array, presets, tools/file transforms. [API reference](https://aitunnel.ru/docs/api-reference) документирует optional enabled у context-compression plugin; можно явно отправить `{id:context-compression,enabled:false}` и запретить дополнительные plugins. Returned actual `model` проверяется/фиксируется, mismatch с frozen allowed identity не становится молчаливой сменой модели. JSON schema остаётся provider hint/capability плюс local strict DTO guard, не доказательство semantic truth.

HTTP error и top-level body error проверяются до DTO conversion, включая HTTP200 error. Общий400 не означает однозначно context overflow: тот же статус имеет unknown model/invalid JSON/PII. Exact overflow классифицировать только по проверенному provider error mapping, иначе честный nonretry provider-request failure; не маскировать любое400 в expected incomplete. Raw error.message/metadata могут содержать dossier fragments; logging только redacted category/code, никакой raw body.

### Оставшиеся неизвестные и бюджеты

1. Не установлен exact preflight token count AIT, tokenizer/model snapshot/framing, гарантированная поддержка strict schema на любой user model, неизменность gateway маршрута и стоимость error/cancel. Option B не объявляет эти свойства известными.
2. **AIT сам повторяет upstream429** по [limits](https://aitunnel.ru/docs/limits) и [errors](https://aitunnel.ru/docs/errors). Клиент может запретить свои скрытые retries/fallback, но не доказать max50 upstream model calls с помощью max50 local attempts. Trace должен различать local model attempt/HTTP dispatch и unknown upstream retry count. Абсолютный client deadline ограничивает ожидание/acceptance, не gateway billing/remote execution.
3. Context/output metadata берутся из current catalog с verified positive types и фиксируются; выбранный ID может оказаться unavailable или unsupported во время dispatch. Тогда ясный отказ, без другой модели. Catalog200, count-only transport test или mocked schema response не live-quality evidence.
4. Даже completed authenticated generation smoke докажет integration для выбранной модели/config, а не quality/independent reasoning пяти personas. Current stage keys/count/generation/model tests отсутствуют.

**Decision to present user:** выбрать A (строгий preflight, AIT blocked пока exact contract unavailable) либо B (OpenAI exact + AIT server-enforced без точного предварительного count). До этого решения root может завершать concrete design/HTTP schemas/offline fixtures; исполнение B не разрешено молчанием. Объём runtime change минимален: typed provider policy и async preflight branch, без нового агента/сервиса/инфраструктуры.
