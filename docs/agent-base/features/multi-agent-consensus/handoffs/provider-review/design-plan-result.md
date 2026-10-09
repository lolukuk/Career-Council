# PI02 independent design and plan review

2026-10-09. Reviewer: consensus_design_review; author: root. Проверен provider-design.md PI02, включая explicit context-compression disabled. Accepted prototype15 сохранён.

**Design: PASS conditional on explicit user approval B. Proposed plan: PASS; execution11 pending user approval.** Блокирующих документальных findings нет. Это не подтверждение реализации, connectivity, live качества или новых тестов.

## Adversarial checks

- Arbitrary AIT ID без точного tokenizer: reliable=false/count=null сохраняют правду; каталог не выдаётся за счётчик. B явно меняет старый guard, A остаётся fail-closed. Нет certification через bytes/o200k или синтетический2xx.
- OpenAI count ниже32768 при меньшем реальном окне: дизайн прямо допускает server refusal, truncation disabled. server_exact означает точность count;32768 — application budget, не модельное окно. В preview согласования сохранить эту границу: предварительное доказательство вместимости в реальное окно arbitrary model не заявляется и для OpenAI.
- Compression/alias/fallback скрывает потерю evidence/смену модели: fixed catalog ID, explicit plugin disabled, отсутствие transforms/fallback/presets и отказ mismatched returned ID описаны. Это не доказательство неизменности внутренних backend провайдера; такая гарантия не заявлена.
- Nullable placeholders/tuple normalization ослабляют DTO: predefined default map не переписывает required/null-allowed поля; исходные local length/cardinality/citation/consensus guards решающие. Unsupported model/schema terminal без text/model fallback.
- Preflight тратит45s перед ещё45s generation: task до async preflight, обе операции в одной attempt lifetime; sync count без HTTP; late/cancel guard сохранён. Local cancellation не доказывает remote stop/billing stop.
- HTTP200 error/неоднозначный400/upstream429: envelope проверяется до content,400 не всегда context overflow, local50 не объявлен remote/cost cap. Rejected response usage сохраняется при наличии; unknown не равен0. Raw error/dossier/key не логируются.
- Два ключа и CLI override: только selected provider key, env precedence определена, legacy key игнорируется. Model/key absence до dossier preparation; secrets вне Request/trace/report/repr.

## Plan and remaining proof

PI03→PI04→PI05→PI06 — конечная последовательность, один автор и отдельный reviewer, без циклического DoD, новых агентов или инфраструктуры. PI03/PI04 предметные mock-HTTP fixtures; PI05 требует existing suite exit0; PI06 actual code/evidence review с исправлениями и повтором затронутых checks. Design06/execution11 не закрыты этим review.

В PI06 проверить wiring: policy-specific admission вместо старого unconditional reliable guard; task/deadline до HTTP; одинаковый count/generate input/schema; terminal error без retry; provider key isolation; output limit/wire cap; default/nullable/tuple transport вместе с исходной local validation; rejected usage; отсутствие late state mutation. Это существующие plan scope/fixtures, новый harness не нужен.

Остаточные ограничения B: точный AIT preflight неизвестен; server backend snapshot, remote stop/cost не сертифицированы; поддержку выбранного ID/схемы подтвердит будущий фактический ответ. Mocks не доказывают server enforcement или reasoning quality. До approval строгий AIT guard действует. Historical PI-F01 exact accounting не объявлен технически исправленным.

Evidence: текущий PI02 и прежнее handoffs/provider-review/result.md; [OpenAI count API](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count), [AIT transforms](https://aitunnel.ru/docs/transforms), [models](https://aitunnel.ru/docs/models), [limits](https://aitunnel.ru/docs/limits), [errors](https://aitunnel.ru/docs/errors). Это документальный контракт, не live доказательство.

Current dispatch: только чтение и reviewer handoff; no credentials, product edits, tests, models, installations, live calls или новые агенты. Исторические54 tests не являются PI02 evidence.
