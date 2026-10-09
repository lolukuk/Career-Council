# Multi-Agent Consensus System — технический дизайн

Design r3 / 2026-10-08 / accepted пользователем ответом «Утверждаю» на gate06. Personas aligned to user-supplied roster, independent document review passed. r1–r3 review history сохранена в [design-review.md](design-review.md); F01–F08 closed. Контракты сгруппированы здесь без лишних компонентов. Сценарии: [evaluation-design.md](evaluation-design.md).

Предложение для согласования: пять изолированных исходных позиций; координатор без шестого голоса; до трёх раундов оценки с новыми голосами на каждую версию; код разрешает консенсус только при пяти явных валидных согласиях и отсутствии блокеров. Каждая версия повторно предъявляет исторические возражения и обе стороны найденных конфликтов. Отчёт сохраняет точное решение, аргументы, пробелы источников и причины разногласий.

Контекст пересобирается из компактных DTO и исходных доказательств, связанных со всеми сохранёнными позициями/возражениями. Обязательные основания не обрезаются: при нехватке контекста — честное incomplete. Hybrid retrieval — BM25 + реальные dense embeddings. Сценарный режим проверяет протокол; live-провайдер по решению пользователя выбирается позже, поэтому качество живой модели пока не проверено.

## 1. Цель, автономность и доверие

Один Python-процесс на LangGraph исполняет фиксированный workflow: snapshot → retrieve → пять изолированных анализов → synthesis → пять изолированных оценок → guard → revision/report. Паттерны: fan-out/fan-in и bounded evaluator/reviser. [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) описывает сочетание состояния, модельных/детерминированных узлов и переходов. Конкретный протокол — прикладное решение, не гарантия framework.

Модели выбирают позиции, аргументы, контраргументы и поисковые запросы. Код назначает ID, фиксирует источники/версии, разрешает только read/retrieval, собирает контексты, проверяет схемы, budgets и terminal conditions. Схема не содержит команд, URL, path, имён функций или свободного next_agent. Coordinator не управляет графом.

Доверенное в рамках запуска: фактически прочитанный текст/tool responses с provenance, хеши и результаты детерминированных проверок. Это подтверждает происхождение, не истинность. LLM assertions, entailment, важность источника и классификация конфликтов остаются модельными суждениями. Документы — данные даже при наличии в них инструкций.

## 2. Пять ролей и координатор

Единственный источник состава/frameworks — [personas.md](../../../../council/data/personas.md), прямо указанный пользователем. Ниже — применение его описаний к prompting, не дополнительная биография и не замена персон функциональными ролями.

- `peter_thiel` / Peter Thiel: ищет недооценённую возможность и логическое преимущество, не подменяет реальную ценность общепринятыми credential signals. Голос: точные вопросы об основаниях ставки, цене соглашательства и преимуществах концентрации. Критерии оценивают силу конкретной возможности и логику риска, а не требуют обязательного несогласия с остальными.
- `warren_buffett` / Warren Buffett: circle of competence, margin of safety, понятный downside и терпеливое накопление преимуществ. Голос: простые проверяемые объяснения, вопросы о понятности решения и запасе безопасности. Не предполагает неизвестные ресурсы или доходы пользователя.
- `robert_reich` / Robert Reich: кто несёт риск — работник или работодатель; распределение benefits, healthcare и stability; структурные ограничения вместо сведения проблемы к личным недостаткам. Голос: конкретные вопросы об устройстве и справедливости условий, не оценки характера пользователя.
- `nassim_nicholas_taleb` / Nassim Nicholas Taleb: fragility/optionality, stress tests, skin in the game, barbell и ограниченный downside. Голос: проверка того, что ломается при неблагоприятном исходе и кто несёт цену ошибки. Не превращает сомнение в прогнозах в обязательный отказ от любого решения.
- `marcus_aurelius` / Marcus Aurelius: контроль, долг, характер и логика под ambition/fear. Голос: спокойные вопросы о контролируемом действии и соответствии обязательствам/ценностям, не обещания внешнего результата. Факты о семье/ценностях появляются только из досье.

Все пять проверяют доказательства, исполнимость и весь проект через свой framework; не выделяются дополнительные evidence/execution/contrarian agents. Эти моделируемые профили не дают знания о Mark до dossier input. В промптах нет выдуманных цитат, биографических фактов или заранее заданной рекомендации. Coordinator составляет решение по всем пяти позициям, обрабатывает конфликты, но не голосует и не закрывает чужое возражение.

Перед run runtime читает personas.md как отдельно заданную конфигурацию, валидирует ровно пять ожидаемых имён/IDs и фиксирует source content digest + normalized profiles в persona_config. Она frozen на весь run; digest входит в snapshot/config identity и trace. Description/frame каждого профиля pinned только в собственном initial/review input; coordinator видит названия/frameworks плюс все принятые Positions. Файл не является RAG evidence о пользователе и его framework не может подтверждать user claim. Его footer про возможность замены фигур не даёт модели полномочия менять roster, budgets или protocol; неизвестный/дублированный участник отклоняется. Замена/редактирование профиля требует новой pre-run конфигурации и нового run/snapshot.

Достаточно одного model endpoint. Пять промптов не делают модель пятью независимыми источниками истины; correlation/sycophancy проверяются в live-evals. Разные модели и дополнительный verifier не входят в MVP.

## 3. Границы кода и схемы

В `council`: DTO/config; ingestion/read wrapper; hybrid retriever; context builder; model adapter/prompts; LangGraph workflow/guard; deterministic renderer; scenarios. Это модули одного приложения, не сервисы. Нового универсального framework нет.

`main.py` сохраняет исходный user_prompt, вызывает приложение; CLI допускает другой вопрос/досье. Исходные data/tools сохраняются. Output-directory выбирает пользователь/runtime, модель не управляет файлами; каждый run пишет отдельные артефакты.

Pydantic: strict scalar types, extra=forbid, schema_version=1, конечные enum и длины строк/коллекций, NaN/Infinity запрещены. IDs не превращаются в пути. UTF-8 JSON, canonical serialization с sort_keys/фиксированными separators для digest. Принятые DTO immutable; update создаёт новый объект. Не усекать DTO при сериализации.

## 4. State model и ownership

RunState: runtime-owned run_id, phase, snapshot_id, roster, persona_config, config, manifest, evidence_store, initial_positions, decisions, votes_by_version, objection_ledger, conflict_ledger, coverage, usage, events, terminal_reason.

- Manifest: source_id, kind=profile/note/document/task/subtask, origin/location, captured time, source date if known, content digest, read success/error. Источники заморожены до анализа; обновлённые внешние данные требуют нового run/snapshot.
- Evidence: chunk_id, source_id, exact text, offsets/section/JSON location, digest. Derived summaries отделены и не цитируются как первичный текст.
- Initial_positions: ровно один итоговый Position на каждого, immutable после barrier.
- Decisions: append-only VersionedDecision, version начиная с 1. Digest включает весь смысловой payload: recommendation/steps/claims/conditions/caveats/обработку objections и snapshot_id. Голос привязан к run/version/digest.
- Votes_by_version: новый набор на каждую версию. Старые наборы сохраняются только в history.
- Objection ledger: runtime-issued ID, owner_persona, origin_version, optional criterion_id, text, blocking, evidence_refs, checks_by_version и resolution vote reference. Для текущей версии status вычисляется: pending/upheld/resolved_for_this_version. Любой исторический blocking objection вновь pending при новой версии, даже если закрыт в промежуточной. В MVP permanent retirement отсутствует. Coordinator не меняет status.
- Conflict ledger: runtime-issued conflict_id, owner_persona, origin Position/Vote, краткий text, ровно две validated citations на разные исходные утверждения, checks_by_version. Model discovery — assertion о конфликте, не доказанное противоречие. Историческая пара сохраняется; dispositions версии не удаляют обе стороны.
- Coverage: inventory, queries/ranks, viewed chunk IDs, missing categories, unread tool records, uncertainty. Empty retrieval не подтверждает отсутствие факта.
- Events: accepted DTOs/guard results/errors, request/attempt IDs, usage/timings, context digests/model config. Ошибки redacted; секреты/headers не логируются. Report/trace содержат только необходимые короткие цитаты локального приватного досье.

Single writer для версии/guard/report. Пять worker записывают разные map keys через проверяемый reducer; duplicate position/vote отклоняется, даже если payload совпал. Worker получает копию разрешённого контекста, не mutable shared state. Attempts централизованно резервируются до dispatch, чтобы параллельность не превысила лимит. Ошибка reducer — failed, не overwrite.

## 5. Model contract

Position: recommendation; 1–5 arguments; 1–4 criteria; strongest_counterargument; uncertainties/missing_data; conflicts max2. Argument имеет basis=source + citations либо basis=assumption + влияние на вывод. Conflict input содержит text и две citations; runtime проверяет обе по packet данного call и создаёт durable record после initial barrier. Persona/run/snapshot identity runtime-owned. Criteria получают ID persona/local_index от runtime, blocking flag и текст; они неизменяемы, не удаляются под давлением группы.

DecisionProposal: recommendation, steps, 1–8 claims, alternatives, caveats, missing_data, objection_responses для всех исторических blocking и текущих open nonblocking IDs, conflict_responses для всех ledger conflicts, change_summary при version>1. Claim имеет local ID и basis/source refs либо явное assumption; принятые IDs scoped версией. Caveat имеет собственный local ID/text/claim_refs; runtime scopes оба набора как v2/c1 и v2/k1, rejects duplicate IDs. Objection/conflict response — proposed explanation, не изменение ledger.

Recommendation и каждый step — structured section {text,claim_refs,caveat_refs}; claim_refs непусты и ссылаются только на claims этой версии. Alternatives и прочие narration-поля не могут вводить самостоятельные material factual assertions: такие факты регистрируются в claims с basis/citations/assumptions. Код проверяет reference completeness/существование, не извлекает все факты из prose. Весь semantic payload дополнительно оценивается reviewers; это закрывает непредусмотренный обход через поля, но не доказывает безошибочность модели.

Vote: echoed run_id/snapshot_id/target_version/target_digest; verdict=approve/object/abstain; rationale; criterion_checks для всех собственных Criterion IDs (satisfied/unmet + причина); objection_checks для всех исторических blocking и open nonblocking objections владельца (resolved/upheld + основание); conflict_checks для всех конфликтов владельца; claim_assessments для каждого claim; payload_assessment всего проекта; new_objections; new_conflicts max2; change_explanation; evidence_requests max2. Reasoning короткое и проверяемое, скрытая цепочка рассуждений не запрашивается.

Claim assessment: supported/qualified/unsupported + основание; qualified обязательно имеет current-version caveat_ref и condition_text, точно совпадающий с текстом этой caveat. Persona явно оценивает семантическую применимость оговорки к claim. Missing/unknown/foreign/stale caveat IDs отвергаются кодом; случайная чужая caveat не удовлетворяет checks. Для assumption claim обязательна qualified assessment с раскрытой caveat, не маскировка assumption как установленного факта.

Payload_assessment: supported/unsupported, unregistered_assertions (bounded список section refs и описания), rationale. Reviewer проверяет recommendation, каждый step, alternatives/caveats/missing_data/objection/conflict responses, а не только claims; approve требует supported и пустой unregistered_assertions. Такое подтверждение — модельное суждение; backend не обещает deterministic semantic extraction.

Для всех списков checks проверяется точное множество ожидаемых IDs, включая отсутствие duplicate/foreign IDs; совпадение количества недостаточно. Все refs принадлежат текущему snapshot/version/call по их типу. New conflicts валидируются/регистрируются до guard; конфликт, появившийся в текущем Vote, не может получить disposition в том же раунде и требует пересмотра.

Approve требует полный набор claim/criterion/owner-objection/owner-conflict checks и payload_assessment, отсутствие unsupported claims/unregistered assertions/unmet blocking criteria/blocking objections этой версии и объяснение связи с начальной позицией. Qualified требует конкретную применимую caveat в immutable decision. Новое objection/conflict либо abstain запрещает consensus данного раунда.

Objection ID назначает runtime; owner — envelope, не модель. Resolved_for_this_version записывается только по explicit check владельца в валидном голосе текущей версии со ссылкой на response проекта и evidence/claim reference. Coordinator не может закрыть O1 своей строкой resolved. В любой V+1 каждый исторический blocking O1 снова pending и owner обязан повторно оценить его, даже если изменение кажется несвязанным. Initial criteria также проверяются заново. Permanent retirement самого требования в MVP запрещён; evidence/support closure сохраняет историю условия.

Conflict check: unresolved либо uncertainty_in_decision с current caveat_ref и объяснением применения. MVP не имеет automatic truth-resolution/retirement conflict. Каждый исторический conflict перепроверяется владельцем в каждой версии; согласованный план может честно признать неопределённость и предложить сбор данных, но не выбросить отрицательный источник. Guard требует, чтобы каждый conflict имел current owner disposition uncertainty_in_decision и конкретную caveat, которую рассматривают все reviewers в payload_assessment. Unresolved conflict не даёт consensus.

Conditional_approve отсутствует в enum. Можно безусловно одобрить проект «сначала получить данные, затем решать вопрос увольнения», если такое условие входит в immutable decision. Это согласие с планом, не подтверждение полученных данных. «Согласен только если неизвестный факт окажется верен» не считается approve.

ModelAdapter: request(stage,envelope,system_policy,untrusted_payload,response_schema,caps) → payload/usage/model_identity. ScriptedAdapter использует fixtures; live provider/model/SDK не выбираются до конфигурации. Live adapter обязан сообщить context window, надёжный token accounting и timeout/cancel capabilities. Непроверенная конфигурация запрещает live-run до отправки досье. Scripted mode явно маркируется, не называется AI-демонстрацией.

DTO field limits: recommendation/rationale/change_explanation ≤1500 chars каждый, criterion/objection text ≤600, argument/claim ≤800; collections выше ограничены. Лимит new_objections ≤3/persona/round, uncertainties ≤5 и steps ≤8. При превышении schema error, не обрезание. Разрешённый текстовый язык выбирается конфигурацией (report ru по умолчанию); источник цитируется на исходном языке.

## 6. Протокол и guard

1. Created → preparing: прочитать/валидировать источники, frozen snapshot/indexes.
2. Preparing → analyzing: общий evidence packet, пять изолированных входов. Initial builder использует allow-listed поля, не сериализацию всего RunState. Sibling outputs/проект недоступны.
3. Barrier: ровно пять валидных Positions. После исчерпания attempts неполный набор → failed; synthesis по четырём позициям запрещён.
4. Analyzing → drafting: coordinator предлагает V1; schema/citation guards, сохранение всех обязательств и ответов на открытые objections; freeze version/digest.
5. Drafting → reviewing: пять изолированных оценок одинакового проекта/evidence packet. Вход включает все компактные original Positions, ledger и previous-round votes. Sibling votes текущего раунда недоступны до barrier.
6. Reviewing → checking: пять accepted Votes либо failed. Применить owner-authorized resolutions/new objections; затем guard.
7. Consensus iff set participants ровно {peter_thiel,warren_buffett,robert_reich,nassim_nicholas_taleb,marcus_aurelius}, frozen из валидированного personas.md; один Vote/persona; envelope и echoed run/snapshot/version/digest совпадают; все verdict=approve; точные sets всех checks полны; payload assessments supported; unsupported/unregistered claims/unmet blocking criteria/current pending or upheld blocking objections/unresolved conflicts отсутствуют; qualified/conflict caveat refs current-valid; citations валидны; mandatory context/source coverage присутствует; budgets/cancel не нарушены. Только код пишет terminal consensus.
8. Correctly formed objection/abstain → revising, если rounds осталось; иначе no_consensus. Bounded retrieval в frozen snapshot → coordinator V+1 + change_summary → пять новых оценок. Старые votes не переносятся.
9. Structural failure после repair → failed; deadline/budget/mandatory context overflow → incomplete; user cancellation → cancelled. No_consensus означает проведённый, но не согласованный разговор, а не недоступную модель.
10. Terminal → deterministic report/trace → END. Output write error предъявляется отдельно; usable report не выдумывается. Crash recovery не реализуется.

Unknown persona/tool/enum, duplicate, old digest, missing justification не засчитываются. Repair использует тот же frozen input и новую attempt identity; вторая невалидная попытка завершает узел. Корректное object/abstain не retry ради approve.

## 7. Context engineering

Полное состояние не равно model context. Initial: system persona/policy, question, snapshot metadata, общий bounded dossier/provenance, профиль ограничений и coverage gaps. Никакой sibling position/draft/prior chat. Последовательное выполнение допустимо при такой же изоляции DTO.

Coordinator: пять original Positions, latest decision if any, все исторические blocking и open nonblocking objections, все conflicts, previous votes, evidence/coverage. Reviewer: own original + все пять compact Positions + latest decision + тот же ledger/history + previous votes + общий evidence packet. Согласие оценивается при одинаковом review packet в раунде.

Pinned: вопрос/ограничения, exact current decision, все пять Positions с criteria, все исторические blocking и open nonblocking objections, все historical/current conflicts с обеими сторонами, previous votes и coverage gaps. Нельзя поручить coordinator «удобно» пересказать и удалить возражения.

Evidence pinning — transitive closure всех retained/pinned DTO refs: original Positions/criteria, ledger objections/conflicts, current Decision, previous Votes и disclosure conditions. Каждая ссылка разрешается в exact frozen chunk. Если Position ссылается на X, X нельзя вытеснить новым ranking, заменить summary или понизить source argument до assumption. Missing ref → failed/provenance_error; closure overflow → incomplete/context_overflow. Resolved-for-V2 objection и обе conflict citations остаются в closure V3.

Packing: pinned → nearest supporting/counterevidence → optional chunks по rank/diversity. Удаляются только optional целые chunks. Пinned overflow → incomplete/context_overflow. Ограниченные DTO не обрезаются после принятия. Full manifest вне context; внутрь relevant entries/coverage summary. Summarizer-agent не нужен.

Max input bytes и max tokens проверяются отдельно. Live token accounting учитывает весь сериализованный payload, response schema/system overhead и output reserve по tokenizer/certified bound провайдера. Byte limit сам по себе не считается token limit.

## 8. Retrieval, полнота и provenance

Chunks: Markdown по секциям/абзацам; notes по records; profile по тематическим секциям; tasks/subtasks по tool records. Чанкинг использует реальный tokenizer/max_seq_length embeddings, без silent truncation; overlap и offsets фиксируются. Profile goals/constraints/resources mandatory; tasker mandatory для career-demo. General dossier может pre-run явно исключить tasker, не во время обсуждения.

Initial queries: question + пять аспектов frameworks из personas.md (недооценённое преимущество; компетенция/запас безопасности; распределение трудового риска; fragility/optionality; контроль/обязательства). Это аспекты поиска, не предопределённые ответы. BM25 и cosine dense search по S1; реальные embeddings Sentence Transformers, кэш по content/model/config digest. Model ID/dimensions/config фиксируются. Недоступная dense model → failed/retrieval_unavailable; lexical-only fallback не выдаётся за hybrid.

Каждая ветвь top20, union RRF k=60, tie-break chunk_id. Exact duplicates dedup по content digest с сохранением origins. Packet содержит mandatory chunks и не более 20 optional по budget; сначала mandatory categories/аспекты, затем общий ranking. Запрос может не дать релевантных результатов — пробел фиксируется.

После review: до 2 queries/persona, до 300 chars/query, максимум 10 distinct queries/round с dedup (включая сформулированные runtime conflict queries). Caps rejected requests отражаются в coverage. Только frozen local corpus, no web/new URL. Retrieval не меняет snapshot_id, но меняет packet digest и следующую версию.

Citation {chunk_id,quote}: chunk был действительно показан этому model call; exact nonempty substring original chunk, ≤400 chars. Manifest-only unseen reference, выдуманная цитата/summary-as-source отклоняются. Model-discovered conflicts сохраняются с обеими цитатами, counterevidence pinned на следующих раундах. Моковые даты 2024 не считаются текущими сведениями.

Проверка цитаты подтверждает наличие текста, не entailment. Claims оценивают reviewers и отдельно размеченные live-evals. Top-k не доказывает отсутствие других конфликтов. Отчёт показывает counts loaded/read-failed/viewed sources, missing categories, поиск/фильтрацию/ограничения. Gold relevant source recall и support precision измеряются только там, где есть eval-разметка.

## 9. Tools, limits и отказ

Tasker wrapper: get_tasks() → validated unique task-ID roster; затем для каждого выданного ID последовательно get_task_details(id), get_subtasks(id). Details.task_id == requested ID; subtask IDs unique в parent scope, parent linkage задаётся wrapper из validated request, не LLM. Эти три метода есть в моке. Read напрямую из tasker.json не заменяет integration path. IDs только из get_tasks того же snapshot; неизвестный ID отклоняется до API. Frozen snapshot означает acquired set, не обещание атомарного point-in-time чтения динамического внешнего API.

TaskerServiceError transient: max3 attempts/call, backoff 0.1/0.3 s, shared budget/deadline/cancel. KeyError для выданного ID → inconsistent_snapshot без retries; невалидный DTO → failed. Ошибка не превращается в empty success. Default career-run требует полный tasker snapshot, иначе incomplete/source_unavailable; partial mode только explicit pre-run config, отражённый в manifest/report.

Retriever принимает строки/enum kind/snapshot-owned refs; возвращает validated chunks/ranks/coverage. Vote может предложить query, но не функцию/endpoint. Allow-list/caps действуют кодом; точно-однократная доставка provider/read не обещается.

Предлагаемые runtime defaults: max_rounds=3; max_model_attempts=50; max_tasker_calls=100; model timeout45s/attempt; discussion deadline600s; payload32768 bytes/call; output2000 tokens/call плюс проверенный provider context cap. Normal max: 5 initial + 3 coordinators + 15 reviews =23 calls; max2 attempts даёт46, общий limit50. Это configurable safety limits, не пользовательский timebox/latency promise.

Подготовка ограничена отдельно: max_sources5000, file ≤8MiB, total source bytes≤64MiB, chunks≤20000, chunk bytes≤4096, embedding dimensions≤1024, preparation deadline300s. Model/index preparation не скрыта из elapsed trace. При implementation capability probe проверяется bounded cancellation: если native inference/load не останавливаются, используется один managed local subprocess с подтверждённым stop/late-result rejection либо такая configuration запрещается до run. Это не сервис/агент. Hard-stop не обещается без подтверждённой capability; execution plan должен включать E07/E10 evidence этой развилки. Cached embedding model предпочтительна; download/bootstrap отделён от run.

Transient model error/timeout — max2 total attempts включая исходный. Schema/citation error — одна repair attempt в том же max2, не 2+2; same frozen input. Authentication/unknown model/capability error и содержательное возражение не retry. Все attempts reserve до dispatch. Cooperative cancellation: pending tasks cancel, поздний result terminal/nonactive request отвергается. Локальная отмена не доказывает прекращение тарификации внешнего LLM. Никаких model-controlled writes.

## 10. Отчёт и гарантии

Код генерирует Markdown из accepted state без финального LLM. Статус/причина, exact version/digest, recommendation, пять initial voices/current votes, изменения версий, unresolved dissent/missing data, citations/короткие quotes, coverage/usage и mode=scripted/model. Accepted decision не перефразируется в несогласованную шестую версию.

Trace JSON: все versions/votes/ledger, request identities/context and evidence digests, budgets и model/embedding config. Исходники досье не переписываются, секреты/headers не сохраняются. Локальные артефакты с приватным контекстом не публикуются.

Обоснованный консенсус означает unanimous protocol с проверяемыми основаниями и раскрытыми caveats, не истинность/полноту корпуса. Live-quality остаётся непроверенным до evals. Honest завершение может быть планом получения данных или no_consensus. По прямому уточнению пользователя «Человек принимает итоговое решение»: человек рассматривает готовый отчёт вне bounded agent loop. Human choice не голосует, не снимает objections и не изменяет protocol status; можно выбрать действие при no_consensus, сохранив отчёт о разногласиях.

Схемы: [runtime.mmd](artifacts/flows/runtime.mmd), [sdlc.mmd](artifacts/flows/sdlc.mmd). Перед gate06 независимый reviewer сопоставляет описание, схемы и сценарии.

## 11. Коррекция r2 по независимому review

F01: version-scoped objection checks без permanent retirement. F02: section claim_refs + whole-payload assessment с честной semantic границей. F03: transitive pinned evidence closure. F04: bounded Conflict DTO/ledger, current owner caveat disposition и обе persistent citations. F05: version-scoped caveats, exact condition_text, точные sets checks. F06: схема различает missing mandatory source и invalid/retrieval failure. Tasker provenance и bounded native-cancel capability уточнены. Отдельный reviewer independently verified r2, все F01–F06 closed, document verdict pass. Это не результат проверки исполнения; пользовательское design approval ожидается.

## 12. Уточнение r3 по personas.md

По прямому указанию пользователя заменены ранее предложенные fictional personas, set IDs, рамки prompting/retrieval и примеры сценариев. Добавлена frozen persona_config из предоставленного файла и проверка отсутствия подмены user evidence личным framework. Протокол версий/единогласия/ledger/pinning/budgets и инфраструктурные границы сохранены. Focused r3 review pass, F07 outdated wording и F08 mediator scope independently closed; r1/r2 history сохранена. Локальный текст human mediator сохранён и пояснён прямым ответом пользователя: человек принимает итоговое решение по отчёту, интерактивного human node/шестого голоса нет. Проверки продукта/live unrun.
