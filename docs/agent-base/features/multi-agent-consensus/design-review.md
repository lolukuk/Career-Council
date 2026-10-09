# Independent design review — Multi-Agent Consensus System

Reviewer: отдельный consensus-protocol-reviewer; 2026-10-08. Проверен **design r1**, evaluation-design r1, согласованные requirements, workflow r2, Mermaid runtime/SDLC и фактический `council/tools/tasker.py`. Автор дизайна и reviewer — разные агенты. Ни дизайн, ни код reviewer не изменял.

**Исходный verdict r1: blocked; review r2: pass; текущий final documentary verdict r3: pass.** История и независимые closures приведены далее; F01–F08 закрыты на уровне дизайна. F01–F05 в r1 требовали коррекции/повторной независимой проверки до gate06. F06 — небольшая несогласованность схемы. Необходимость ограниченного workflow, пять runtime-персон, отсутствие шестого голоса, один инженерный reviewer и отсутствие новой инфраструктуры обоснованы. Замечания относятся к протоколу и его проверяемости, а не к выбору стека.

## F01 — P1: снятое блокирующее возражение не перепроверяется при регрессии новой версии

- Section: tech-design **§4 Objection ledger**, **§5 Resolved**, **§7 Pinned**; evaluation-design **E03**. Требования **5, 6, 9**.
- Trigger: V1 получает resources/O1 «переход допустим только при резерве шесть месяцев». Это новое возражение, не initial criterion. V2 включает резерв; resources валидно отмечает O1 resolved, но execution оставляет O2, поэтому consensus отсутствует. В V3 coordinator удаляет резерв, исправляя O2. O1 уже resolved: его нет в обязательных owner checks и open ledger контекста. В следующем раунде previous votes также могут уже не содержать O1. Пять approve по V3 проходят guard без повторной explicit проверки O1.
- Effect: собственная blocking позиция может исчезнуть после промежуточной версии, которая никогда не была итоговым консенсусом. Порождение нового objection при регрессии оставлено памяти/инициативе модели, хотя исходное возражение код уже знает.
- Minimal fix: сделать resolution version-scoped. Каждый исторический blocking objection должен оставаться в pinned context и иметь explicit owner recheck на **каждой** версии; resolved_for_version не даёт следующей версии автоматического освобождения. Допустимое окончательное снятие самого условия требует отдельного явного owner retirement с основанием, которое сохраняется, либо не входит в MVP. Coordinator не имеет права retirement. E03: resolved in nonterminal V2 → condition removed V3; без нового current owner check consensus запрещён.
- Disposition: open.

## F02 — P2: структурные claim checks не охватывают факты внутри остальных полей решения

- Section: tech-design **§5 DecisionProposal/Vote/Approve**, **§6 step7**; evaluation-design **E04/E12**. Требования **3, 4, 6, 11**.
- Trigger: единственный claim C1 = «сначала изучить учебные программы», помеченный assumption. Recommendation = «увольняйтесь завтра: контракт гарантирует зарплату 200000», steps содержат ещё один неподтверждённый факт. Все claim_assessments относятся только к C1. DTO допускает такую форму; отсутствие citation у факта в recommendation не проверяется, и пять полных checks C1 не демонстрируют grounding всего решения.
- Effect: факты обходят набор claim checks через свободные recommendation/steps/alternatives/caveats. Это дополнительная поверхность ложного согласия сверх честно раскрытой ошибки entailment.
- Minimal fix: привязать recommendation и каждый step к существующим version-scoped claim/assumption IDs, явно запретить самостоятельные фактические assertions в прочих narration-полях; reviewer обязан оценить весь semantic payload и явно отметить отсутствие unregistered material assertion. Код проверяет reference completeness, модель — смысловую полноту; не заявлять deterministic extraction/entailment. Добавить negative fixture hidden factual assertion, где корректный reviewer возражает, и missing/unregistered reference fixture, который код отклоняет.
- Disposition: open.

## F03 — P2: pinning не замкнут по evidence references первоначальных позиций

- Section: tech-design **§7 Pinned/Packing**, **§8 Citation**; evaluation-design **E01/E06/E07**. Требования **3, 9, 10**.
- Trigger: initial Position цитирует optional chunk X. Он не относится к mandatory category и пока не цитирован decision/previous vote/open blocking objection/conflict. При упаковке coordinator или следующего reviewer packet X удаляется ради бюджета, хотя Position с ссылкой на X pinned. Coordinator пытается повторно использовать argument/X, но X не показан этому call: strict citation guard отвергает ссылку; либо coordinator превращает аргумент в assumption и теряет source support.
- Effect: позиция сохраняется, но доказательство, на котором она основана, становится недоступным новым участникам проверки; обязательная поддержка зависит от случайного ranking. В design перечислены citations decision/previous votes, но не initial Positions.
- Minimal fix: pin transitive evidence closure всех retained/pinned DTO, включая все original Positions, criteria references при наличии, актуальные и сохраняемые objections/conflicts. References должны разрешаться в exact original chunks текущего snapshot. Если замыкание не помещается, incomplete/context_overflow; не удалять источник и не понижать его до assumption. E07: X вытеснен ranking, но остаётся pinned через Position, либо честный overflow.
- Disposition: open.

## F04 — P2: model-discovered conflict не имеет схемы и durable состояния

- Section: tech-design **§4 RunState**, **§5 Position/DecisionProposal/Vote**, **§7 Pinned**, **§8 conflicts**; evaluation-design **E05**. Требования **4, 9, 11**.
- Trigger: evidence persona видит A «работодатель разрешает part-time» и B «договор запрещает part-time», пишет противоречие в uncertainties. Ни одно принятое DTO не имеет conflict record с обеими citations; uncertainties — свободный текст. Coordinator выбирает A; B больше не попадает в top-k. По §7 «нерешённые conflicts» должны быть pinned, однако записать такой conflict в trusted state нечем, а deterministic извлечение из prose не заявлено.
- Effect: негативное доказательство может исчезнуть между раундами; E05 требует свойство, для которого нет protocol representation. Код не должен угадывать пары citations или смысл противоречия.
- Minimal fix: добавить компактный bounded Conflict DTO в Position и при необходимости Vote: runtime ID, text, two validated source references, owner/origin, resolution или explicit uncertainty disposition, visible history. Pinned closure сохраняет обе стороны до явного disposition, который не означает доказанную истинность одной стороны. Не нужен отдельный agent/verifier. E05 проверяет durable record и оба chunks после потери ranking.
- Disposition: open.

## F05 — P2: qualified assessment не адресует конкретную caveat

- Section: tech-design **§5 Vote/Approve/Claim IDs**; evaluation-design **E04**. Требования **4, 5, 6**.
- Trigger: immutable decision содержит caveat K1 «зарплата зависит от места работы». Persona ставит claim C1 qualified с причиной «при условии продажи квартиры». В схеме у assessment нет caveat_ref; условие присутствия оговорки нельзя проверить структурно. Случайное наличие K1 может ошибочно считаться достаточным для qualified approve.
- Effect: одобрение может иметь приватное условие, которого нет в принятом решении, несмотря на явный запрет conditional approve. Сравнение свободного текста потребовало бы дополнительного semantic gate, который не задан.
- Minimal fix: runtime/version-scoped caveat IDs и обязательный существующий caveat_ref для qualified; reviewer явно подтверждает соответствие условия exact caveat text. Код проверяет ID, model — semantic correspondence. Если подходящей оговорки нет, object/abstain и новая версия, а не approve. Criterion/objection checks также проверять по точному set IDs, reject duplicates/foreign IDs, а не только количеству. E04: missing/foreign/stale caveat ID и неверное условие.
- Disposition: open.

## F06 — P3: runtime diagram объединяет ошибки подготовки с разными terminal outcomes

- Section: runtime.mmd **B → Source or retrieval failure → Incomplete** против tech-design **§8 dense failure**, **§9 invalid DTO**. Требование **8**.
- Trigger: dense model недоступна → текст требует failed/retrieval_unavailable, Mermaid ведёт в incomplete. Невалидный tasker DTO также failed по §9, но Source failure в diagram ведёт в incomplete.
- Effect: схема и текст задают разные stop semantics; разработчик может реализовать неверный статус технической ошибки.
- Minimal fix: разделить B edges: missing mandatory source/deadline/budget/context → incomplete; retrieval unavailable/invalid source DTO → failed. SDLC gates согласованы с workflow и замечаний не требуют.
- Disposition: open.

## Проверенные границы и остаточный риск

- Actual tasker имеет get_tasks(), get_task_details(id), get_subtasks(id); design вызывает их в правильной иерархии и не подменяет API чтением internal JSON. TaskerServiceError transient, KeyError у двух ID methods. На реализации важно валидировать unique roster IDs, details.task_id == requested ID и parent scope subtask IDs: валидный тип строки не устанавливает provenance. Это уточнение текущего validated-DTO контракта, не новая инфраструктура.
- Version digest, runtime-owned identity, five-vote barrier и history-only старых votes описаны достаточно ясно. Схема не даёт coordinator написать terminal status. Prompt injection не может детерминированно назначить роль/tool/terminal, но может испортить смысл ответов; эта semantic граница честно раскрыта.
- Preparation deadline300s и optional embedding subprocess пока не являются проверенной hard-stop гарантией. Допустимое решение: при implementation capability probe установить bounded cancellation; если native inference не отменяется, использовать уже предусмотренный managed worker **или запрещать такую run config**. Без этой развилки cap нельзя обещать; execution plan должен включить stop/late-result evidence. Аналогично provider billing после local cancellation не гарантируется. Это design risk, а не требование новой службы.
- 23 normal calls/46 attempts при max_rounds=3/max2 attempts соответствуют приведённой арифметике. Budget/time exhaustion должно остановить dispatch до резервирования новой попытки. Monetary live budget остаётся unknown, 18 live runs — proposed, не разрешённые запуски.
- Semantic truth, качественное обнаружение conflicts и реальный независимый анализ общей моделью нельзя доказать scripted fixtures. Разделение offline, actual embeddings и live evaluation сохранено правильно.

## Evidence / checks

Выполнено только independent document/source inspection и adversarial reasoning по перечисленным трассам; продуктовые тесты, embeddings, provider calls и quality evaluation **не запускались**. Counterexamples — design traces, не результаты исполненного прототипа. Автор должен сохранить эти findings/dispositions, исправить материал и передать r2 на reviewer closure; reviewer не утверждает пользовательский gate06.

## Independent closure — review r2 / 2026-10-08

Повторно проверены авторские tech-design r2, evaluation-design r2, runtime.mmd, decisions, workflow/status. Исходные тексты F01–F06 и их r1 dispositions сохранены выше как история; текущие dispositions находятся в этой таблице. Дизайн исправлял автор, reviewer его не соавтор.

**Verdict r2: pass для документального design gate05. Новых существенных findings не выявлено.** Это разрешает предъявить конкретный дизайн на пользовательский gate06, не разрешает автоматически implementation/execution и не является подтверждением работающего продукта.

| Finding | Current disposition | Независимая проверка исходного контрпримера |
|---|---|---|
| F01 P1 | closed — design corrected | §4/§5: O1 resolved_for_V2 снова pending в V3, permanent retirement запрещён; historical owner recheck обязателен. §7 хранит O1 и его support. V3 без safeguard/current owner check не проходит §6 guard. E03 содержит именно nonterminal V2 → regression V3. |
| F02 P2 | closed — design corrected | §5 recommendation/steps structured с непустыми current claim_refs; payload_assessment включает весь semantic payload и unregistered_assertions. Отсутствующий ID отклоняет код; спрятанный factual assertion должен вызвать model object. E04 разделяет structural reference failure и semantic fixture. Безошибочное извлечение фактов не заявляется. |
| F03 P2 | closed — design corrected | §7 явно задаёт transitive closure всех retained DTO, включая initial Positions/criteria, historical ledger и Votes. X не вытесняется ranking и не понижается до assumption; missing X → provenance_error, overflow → incomplete. E06/E07 проверяют X и overflow. |
| F04 P2 | closed — design corrected | §4/§5 Conflict DTO/ledger хранит обе validated citations, origin/owner/checks_by_version; every-version owner disposition связан с конкретной caveat. Новое conflict в Vote требует следующего раунда. §7 сохраняет обе стороны независимо от ranking. E05 включает потерю ranking и удаление caveat следующей версии. |
| F05 P2 | closed — design corrected | §5 qualified имеет current-version caveat_ref и condition_text == exact caveat text; expected check ID sets проверяются на duplicate/foreign/missing IDs. Для semantic applicability reviewer обязан дать явную оценку. E04 включает missing/foreign/stale IDs, mismatched condition text и неприменимое условие. Случайная K1 не заменяет условие продажи квартиры. |
| F06 P3 | closed — diagram corrected | B → Missing mandatory source/preparation limit ведёт в incomplete; B → Invalid source DTO/retrieval unavailable ведёт в failed. Это согласовано с §8/§9 и E09. |

Дополнительные уточнения также проверены: §9 unique task roster, details.task_id == request, parent-scoped subtask IDs и wrapper-owned parent linkage согласованы с actual mock API. Native inference/load допускаются только при подтверждённой bounded capability, managed-worker stop/rejection либо pre-run config denial; E07 требует evidence выбранной развилки. Атомарное внешнее snapshot чтение честно не обещается.

Семантические пределы сохранены: source substring не доказывает entailment; все пять одинаково ошибающихся моделей могут дать protocol consensus; структурные payload refs не гарантируют, что narration не скрывает факт; применимость caveat и conflict discovery требуют model/live evaluation. Они не замаскированы как deterministic guarantees и не требуют новых verifier-агентов для MVP.

Checks r2: только independent reading, сопоставление схем/контрактов/сценариев и повторное adversarial reasoning F01–F06. Тесты прототипа, реальные embeddings, native cancellation и live calls **не запускались и не считаются проверенными**. Execution plan должен материализовать E01–E12 и проверять именно эти свойства; user design approval ещё требуется.

## Focused persona delta review — r3 / 2026-10-08

Scope: прямое указание пользователя использовать `council/data/personas.md`. Прочитан весь исходный файл; независимо сопоставлены design r3 §2/4/5/6/7/8/12, requirement1, evaluation T2–T4/E01-personas, runtime labels и D10/D11. Полный infrastructure review не повторялся. История r1/r2 и закрытые F01–F06 остаются действующими.

**Persona delta verdict: pass. Общий requirement scope остаётся pending по F08.** F07 закрыт после точечной авторской коррекции, проверка которой приведена ниже. Это не скрытое согласование human loop и не пользовательский gate06; all requirements resolved не заявляется.

| Persona / exact runtime ID | Сопоставление framework с данным источником |
|---|---|
| Peter Thiel / peter_thiel | Недооценённая возможность, реальная ценность вместо credential signaling, основания концентрированной ставки. Initial/review должен включать полное frozen source description, в том числе отношение к hedged keep-options-open moves; краткое design summary не заменяет его. |
| Warren Buffett / warren_buffett | Circle of competence, margin of safety, понятный downside, patient compounding. Не назначен обязательным противником и не получает выдуманные ресурсы пользователя. |
| Robert Reich / robert_reich | Распределение риска worker/employer, benefits/healthcare/stability, структурный риск. Framework не сводится к персональному осуждению пользователя. |
| Nassim Nicholas Taleb / nassim_nicholas_taleb | Fragility/optionality, stress, skin in the game, barbell/capped downside. Полное source description сохраняет также upside без искусственного ограничения; обязательное несогласие не предписано. |
| Marcus Aurelius / marcus_aurelius | Контроль, duty/character, проверка логики ambition/fear. Семья/ценности/конкретный выбор появляются из dossier, а не persona config. |

Фиксированного решения для какой-либо persona не задано. T2–T4 явно scripted cases, не прогноз живого Buffett/Thiel и не forced outcomes. Strongest_counterargument общий для всех пяти, дополнительный contrarian/evidence/execution agent не добавлен. Coordinator остаётся без голоса.

§2/§4 задают frozen persona_config с source digest и normalized profiles; digest входит в snapshot/config identity и trace. Изменение personas.md mid-run не меняет сохранённый профиль; footer «Swap figures» не расширяет полномочия модели. §6 exact participant set совпадает с §2, diagram и E01-personas. Своя description pinned в initial/review, общий evidence packet остаётся общим; coordinator получает названия/frameworks и позиции. Наличие различных persona policy contexts не нарушает равенство review dossier/decision.

Adversarial trace: исходный файл содержит описание Buffett, затем mid-run изменён на fictional resources; accepted run должен продолжить с frozen Buffett, а fake resources Vote отклоняется exact set guard. Другой trace: модель цитирует biography/framework из personas.md как подтверждение размера сбережений Mark; §2 запрещает попадание persona config в dossier evidence и E01-personas требует rejection. Это specification reasoning, не исполненные проверки.

Coreguards после замены IDs сохранены: isolation/barrier, exact version unanimity, version-scoped historical blocker checks, paired Conflict ledger и caveat disposition, transitive evidence closure, typed claim refs/whole-payload assessment, exact caveat/check IDs, bounded/no-consensus/incomplete outcomes. Новых protocol findings в persona delta нет.

### F07 — P3: устаревшая фраза о необязательных знаменитостях

- Section: requirements **«Данные существующей заготовки»**, предложение «Персонажи знаменитостей из локального задания — примеры, не обязательные роли» против **Проверяемое поведение 1**, design **§2**, D10.
- Trigger/effect: implementer читает описание исходных материалов и сохраняет прежние fictional profiles как допустимую опцию, хотя последнее прямое указание фиксирует supplied roster. Документ имеет две несовместимые формулировки состава.
- Minimal fix: заменить только устаревшее предложение уточнением, что текущий пользовательский запрос задаёт обязательный roster из personas.md; не менять пользовательский human mediator текст.
- Current disposition: open; небольшой documentary risk, persona delta сам по себе согласован.

### F08 — P2: scope human mediator требует явного решения пользователя

- Section: requirements **«Результат и границы»** (сохранённое локальное дополнение), design **§12**, D11; взаимодействие с **§6 terminal/bounds**.
- Trigger: человек меняет компенсацию/ограничение между раундами; это меняет frozen dossier/decision identity и требует определить, новый ли это run, новый snapshot или отдельная bounded pause. Текущий прототип без human node не задаёт правила такого перехода. Другой смысл — человек выбирает итоговый вариант после no_consensus — вообще не требует runtime вмешательства.
- Effect: разные интерпретации приводят к разному scope; считать interactive human node согласованным нельзя. Принуждение persona согласиться также не заменяет five explicit current-version checks.
- Minimal fix: дождаться уже заданного пользователю уточнения. Для решения только после report зафиксировать границу и оставить протокол; для вмешательства между раундами отдельно спроектировать snapshot/version/context/budget/stop semantics и провести focused review до implementation.
- Current disposition: pending user requirement clarification, не persona-design defect. Original wording сохранён; reviewer не выбирает ответ за пользователя.

Все r3 checks — document/source reading и adversarial comparison. Tests/live calls/embedding/persona-quality evaluation не запускались; fidelity живой модели и различие frameworks в её реальных выводах остаются evaluation задачей.

### Small closure F07 — r3

Автор заменил только устаревшую фразу requirements в «Данные существующей заготовки»: теперь состав/frameworks фиксированы пользовательским personas.md, task.md examples не заменяют этот состав. Reviewer независимо прочитал исправленную строку44; противоречие requirement1/D10 устранено. Строка8 про mediator сохранена. **F07 current disposition: closed. F08 остаётся pending user scope clarification. Итог focused persona verdict: pass**, без объявления полного requirement/design approval и без human node.

### Focused closure F08 — итог review r3 / 2026-10-08

Получен прямой ответ пользователя на вопрос scope: **«Человек принимает итоговое решение»**. Root передал этот ответ reviewer; независимо проверены новый поясняющий абзац requirements, tech-design §10/§12, evaluation E12, accepted D11 и workflow/status. Исходный локальный текст и pending-history выше сохранены.

F08 current disposition: **closed — user scope clarified**. Человек рассматривает завершённый отчёт после bounded agent loop. Его выбор при no_consensus сохраняет статус и разногласия; выбор не становится шестым голосом, не разрешает coordinator закрыть objections и не снимает budgets. Поэтому новые runtime node/agent, pause/resume, snapshot mutation и согласование новой архитектуры не требуются. Это отвечает обоим исходным вариантам контрпримера: промежуточный human intervention не входит в scope, итоговый human action не подменяет protocol consensus.

**Final r3 verdict: pass для документального independent design review. F01–F08 закрыты; unresolved review findings нет.** Это не означает пользовательское утверждение самого дизайна, execution approval, product implementation либо подтверждённое качество живых персон. Закрытый вопрос scope — часть требований, а не автоматическое разрешение следующих gates.

Closure F08 выполнен только по user answer и согласованности названных документов; full infrastructure review не повторялся, код/авторский дизайн reviewer не менял. Tests/live/embeddings/native cancellation unrun. Следующий шаг — предъявить итоговый r3 и review пользователю на gate06.
