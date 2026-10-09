# Совет консультантов

Current retained R2f: user requested to leave the demonstrated SYNTHETIC34037-byte context and stop optimizing. Complete suite188passed54.55s; codec independent PASS WITH RISK/CIT-T01 fixed.32768 cap unchanged, sizing FAIL; no further paid call, full FR-1–FR-9 acceptance remains open. Exact history and artifacts: docs/agent-base/features/multi-agent-consensus/citation-stabilization.md.

Продукт находится в [council](council/README.md): инструкция запуска, схема LangGraph, обоснование архитектуры и направления развития. Исходный вопрос о смене карьеры сохранён в council/main.py. Обычный AI-запуск из этой папки: `.\.venv-consensus\Scripts\python.exe -m council.main --mode model`; scripted запускается только явно для проверки протокола и не заменяет AI-совет.

[Общий аудит и согласованный план C01–C06](docs/career-council-review-2026-10-09.md). [Текущий маршрут и gates](docs/agent-base/features/multi-agent-consensus/workflow.md). Полное задание принимается отдельно от исторического scripted-прототипа; текущие evidence/status указаны в аудите. Изменения локальные, без коммита.

Проверки: **159 тестов прошли**. Последний отдельно разрешённый live дал пять валидных позиций и draft, затем failed при проверке голосов. Исправлен найденный несвязанный assumption/caveat и safe protocol repair; независимое review последнего кода PASS WITH RISK (49focused15.51s). [Текущий checkpoint и evidence](docs/agent-base/features/multi-agent-consensus/citation-stabilization.md). Полный FR-1–FR-9 outcome не принят, разрешённые платные лимиты исчерпаны.

## Сохранённая история нейтральной базы

# База для агентской задачи

Нейтральная заготовка на основе `template_lite` и Adaptive Agent Design Team. Предметная задача ещё не задана; язык, модель, инструменты, хранение и архитектура остаются открытыми.

Для старта опишите задачу свободным текстом или заполните [форму постановки](docs/agent-base/templates/task.md): кто решает какую проблему, какой результат нужен, откуда берутся данные, какие действия разрешены и как проверить успех. Неизвестные поля можно оставить `unknown`.

Дальше применяется [порядок работы](docs/agent-base/README.md): анализ → проверка необходимости агента → требования → согласование применимых технологий → дизайн и независимое ревью → план и маршрут → выполнение → проверки → принятие. Текущий запрос разрешает подготовку этой базы; он не является согласованием будущей архитектуры или запуска продукта.

| Раздел | Назначение |
| --- | --- |
| [docs/agent-base](docs/agent-base/README.md) | Порядок работы, шаблоны состояния и контрактов |
| [template_lite](template_lite/README.md) | Существующие правила поведения, языковые ограничения, профиль и задание |
| [agent-templates](agent-templates/README.md) | Правила применения шаблонов инженерных ролей |

Состояние bootstrap на 2026-10-08: база подготовлена, продуктовая feature и активная команда не созданы. После постановки реальной задачи состояние ведётся в её файлах, а не в этом описании. Для подготовки Markdown не нужны установка инструментов, сборка продукта или вызовы модели.
