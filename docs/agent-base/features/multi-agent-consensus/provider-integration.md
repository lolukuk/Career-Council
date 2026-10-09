# Подключение AI Tunnel и OpenAI — intake и границы

2026-10-09 / draft PI01. Это продолжение после принятого прототипа, не переоткрытие его приёмки. Используется Adaptive Agent Design Team; текущий этап нового подключения00–01, документация изучена, ключевые поля подготовлены. Реализация адаптеров ещё не выполнена, design/plan review и соответствующее execution approval ещё впереди.

## Прямые требования пользователя

Поддержать AI Tunnel (https://aitunnel.ru/) и прямой OpenAI. Пользователь сам задаёт название модели, приложение не выбирает default model и не меняет модель автоматически. Для каждого провайдера своё поле ключа. Остаётся существующий CLI; графических экранов пользователь явно не запрашивал. Пять personas, consensus/version/context/ledger guards и режим scripted сохраняются.

## Подготовленные настройки

`council/.env`: LLM_PROVIDER=aitunnel|openai; LLM_MODEL=<введённое пользователем имя>; AITUNNEL_API_KEY и OPENAI_API_KEY. Источник template — .env.example без секретов. Существующие значения .env сохранены; .env уже указан в council/.gitignore. LLM_API_KEY не удалён; политика legacy fallback должна быть явно задана при реализации, без отправки ключа другому провайдеру. Сейчас приложение .env не считывает.

## Проверенные внешние контракты

- AI Tunnel: [введение](https://aitunnel.ru/docs), [Chat API](https://aitunnel.ru/docs/api-reference), [JSON Schema](https://aitunnel.ru/docs/structured-outputs). Base URL https://api.aitunnel.ru/v1, Bearer authorization; model задаётся строкой, схемы поддерживаются не всеми моделями. Usage содержит prompt/completion tokens и cost_rub. Публичный GET https://api.aitunnel.ru/public/aitunnel/models проверен без ключа: HTTP200, chat mapping содержит context_size/max_output. Два примера структуры metadata прочитаны; это не выбор этих моделей.
- Прямой OpenAI: [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [input token counting](https://developers.openai.com/api/docs/guides/token-counting), [count endpoint](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count). Для Responses имеется авторитетный предварительный count, включая roles/schema overhead.
- AI Tunnel documentation index/API reference не подтвердили аналогичный универсальный count endpoint. OpenAI-compatible chat format не доказывает совпадение tokenizer/model context или поддержку всех Responses subresources. Это открытый design вопрос; нельзя объявлять reliable_token_accounting=True на основании byte estimate.

## Предлагаемый минимальный контур

Один автор реализации, один существующий independent reviewer при готовом дизайне. Настройки/CLI selector и два ModelAdapter/factory поверх уже установленного async httpx; новые SDK/services/agents сейчас не выбираются и не устанавливаются. OpenAI Responses + async token preflight; AI Tunnel endpoint/validated token strategy по установленному контракту. Предварительные count/catalog операции должны попадать в deadline/network accounting и не обходить attempt budgets. Неподдерживаемая модель/schema/capability — понятный отказ, а не model fallback или ослабление consensus guards.

Ключ выбранного провайдера не попадает в Request/trace/report, repr или HTTP error body. Ошибки auth/configuration не retry; transient/invalid response — существующий max2 attempts без скрытых SDK retries. Cancellation/expired attempt semantics R12–R15 сохраняются. Returned actual model identity и usage фиксируются; routing/auto aliases нельзя считать воспроизводимой фиксированной моделью без раскрытия.

## Неопределённости до реализации

Нужно закрыть надёжный предварительный token/context guard для AI Tunnel при user-defined models и нормализацию исходных Pydantic schemas для provider Structured Outputs. Локальный byte cap не заменяет certified token bound. User model input не обещает, что каждая модель из каталога удовлетворяет contracts.

API-ключи на момент read-only проверки отсутствовали; значения не печатались. SDK не добавлялся, LLM calls не отправлялись. После concrete design/review — согласовать минимальный план, реализовать config/provider/error/cancel/usage boundaries, проверять HTTP fixtures + relevant existing protocol suite; live проверку выполнять только с выбранной пользовательской моделью и ключом, её стоимость/объём явно ограничить. Provider connectivity и live reasoning quality — разное evidence.
