from __future__ import annotations

import json
from pathlib import Path

from .schemas import ROSTER, canonical


def render(trace):
    mode_note = ('Сценарные ответы проверяют протокол; качество живой модели не проверено.'
                 if trace['mode'] == 'scripted' else
                 'Режим выбранного LLM-провайдера. Формальное согласие не доказывает качество решения.')
    lines = ['# Отчёт совета пяти персон', '', f"Статус: **{trace['status']}**", '',
             trace['reason'], '', f"Режим: `{trace['mode']}`. {mode_note}",
             '', f"Вопрос: {trace['question']}", '',
             'Человек принимает итоговое решение после отчёта. Его выбор не меняет статус согласия персон.', '']
    if trace['mode'] == 'model':
        requested = trace.get('requested_output_tokens', 2000)
        ceiling = trace.get('accepted_output_token_ceiling', requested)
        excess = sum(u.get('output_limit_exceeded') is True for u in trace.get('usage', []))
        output_note = ('Условный тестовый режим AI Tunnel. Превышения запрошенного лимита допускаются '
                       'только до отдельного жёсткого потолка; этот профиль не предназначен для production.'
                       if trace.get('output_limit_policy') == 'aitunnel_test' else 'Строгая проверка лимита ответа.')
        lines += [output_note, f'Запрошено: {requested} токенов; потолок приёма: {ceiling}; '
                  f'полученных ответов с превышением: {excess}.', '']
        lines += [f"Провайдер: `{trace.get('provider', 'unknown')}`; модель: `{trace.get('model', 'unknown')}`; "
                  f"учёт контекста: `{trace.get('accounting_policy', 'unknown')}`.", '',
                  f"Reasoning effort: `{trace.get('reasoning_effort') or 'model-default'}`. "
                  'Эта настройка влияет на расход и качество модели; none используется для проверки процесса.', '',
                  'Предварительный count OpenAI ограничивает бюджет приложения, не подтверждает окно любой модели. '
                  'AI Tunnel проверяет переполнение на сервере без точного предварительного count; сжатие отключено.', '',
                  'Лимит попыток относится к локальным запросам. Внутренние повторы провайдера и расходы '
                  'после отмены неизвестны. Usage полученных ответов, включая отклонённые, сохранён в trace; '
                  'отсутствующие данные не означают нулевой расход.', '']
    decisions = trace.get('decisions', [])
    current = decisions[-1] if decisions else None
    if current:
        payload = current['payload']
        lines += ['## Рекомендация и план', '', payload['recommendation']['text'], '', 'Шаги:', '']
        lines += [f"{i}. {step['text']}" for i, step in enumerate(payload['steps'], 1)]
        lines += ['', 'Альтернативы:', ''] + ['- ' + text for text in payload['alternatives']]
        lines += ['', '## Риски и условия решения', '']
        lines += ['- ' + caveat['text'] for caveat in payload['caveats']]
        if not payload['caveats']:
            lines += ['Отдельные условия не сформулированы; это не означает отсутствия риска.']
        lines += ['', f"Версия {current['version']}, digest `{current['digest']}`. "
                  'Полный неизменный JSON решения сохранён в trace.json.', '']
    else:
        lines += ['Согласованного проекта нет; анализ не завершён.', '']
    names = {p['id']: p['name'] for p in trace.get('persona_config', {}).get('personas', [])}
    latest = trace.get('votes_by_version', {}).get(str(current['version']), {}) if current else {}
    if current and set(latest) == set(ROSTER):
        lines += ['## Общий итог после обсуждения', '']
        cap = trace.get('config', {}).get('max_rounds')
        if trace['status'] == 'no_consensus':
            lines += [f'Обсуждение завершено после {len(decisions)} из {cap} разрешённых раундов. '
                      'Единогласного одобрения нет. План выше остаётся предложением с условиями; '
                      'возражения ниже входят в итог и не считаются устранёнными.', '']
        lines += ['Оценки общего проекта и основания разногласий:', '']
        for owner in ROSTER:
            vote = latest[owner]
            lines += [f"- {names.get(owner, owner)} — {vote['verdict']}: "
                      + vote['payload_assessment']['rationale']]
            for check in vote['criterion_checks']:
                if check['status'] == 'unmet':
                    lines += [f"  Условие {check['id']} не выполнено: {check['rationale']}"]
            for check in vote['claim_assessments']:
                if check['status'] in ('qualified', 'unsupported'):
                    lines += [f"  Утверждение {check['id']} / {check['status']}: {check['rationale']}"]
            for assertion in vote['payload_assessment']['unregistered_assertions']:
                lines += ['  Непроверенное утверждение в тексте: ' + assertion]
        lines += ['']
    lines += ['## Пять позиций и текущие оценки', '']
    for owner in ROSTER:
        position = trace.get('initial_positions', {}).get(owner)
        vote = latest.get(owner)
        initial_events = [e for e in trace.get('events', []) if e.get('stage') == 'initial' and e.get('persona') == owner]
        partial = any(e.get('accepted') is True for e in initial_events)
        position_note = ('Ответ персоны прошёл проверку, но общий этап пяти позиций не завершён; '
                         'позиция не зафиксирована в состоянии обсуждения.' if partial else 'Позиция не получена.')
        lines += [f"### {names.get(owner, owner)}", '', position['recommendation'] if position else position_note, '']
        if not position and initial_events:
            last = initial_events[-1]
            details = {'citation_not_shown': 'Ссылка на фрагмент, не показанный персоне.',
                       'citation_quote_not_exact': 'Цитата не совпадает с дословным фрагментом источника.',
                       'evidence_digest': 'Нарушена целостность фрагмента источника.',
                       'schema_invalid': 'Ответ не соответствует требуемой структуре.',
                       'check_ids': 'Повторяющиеся, отсутствующие или чужие идентификаторы проверок.',
                       'usage_total': 'Некорректный общий счётчик токенов провайдера.'}
            detail = details.get(last.get('validation_code'))
            if last.get('error') == 'CancelledError':
                detail = 'Запрос отменён; ответ не завершён.'
            if detail:
                lines += [detail, '']
        if position:
            lines += ['Аргументы этого взгляда:', '']
            lines += ['- ' + argument['text'] for argument in position['arguments']]
            lines += ['', 'Критерии:', ''] + ['- ' + criterion['text'] for criterion in position['criteria']]
            lines += ['Контраргумент: ' + position['strongest_counterargument'], '']
        if vote:
            lines += [f"Оценка: **{vote['verdict']}** — {vote['rationale']}", '', vote['change_explanation'], '']
        else:
            lines += ['Текущий голос не получен.', '']
    lines += ['## Возражения и противоречия', '']
    for item in trace.get('objection_ledger', []):
        checks = trace.get('objection_checks_by_version', {}).get(item['id'], {})
        check = checks.get(str(current['version'])) if current else None
        lines += [f"- {item['id']} / {names.get(item['owner'], item['owner'])}: {item['text']} ({check['status'] if check else 'pending'})."]
    for item in trace.get('conflict_ledger', []):
        checks = trace.get('conflict_checks_by_version', {}).get(item['id'], {})
        check = checks.get(str(current['version'])) if current else None
        lines += [f"- {item['id']} / {names.get(item['owner'], item['owner'])}: {item['text']} ({check['status'] if check else 'pending'})."]
    if not trace.get('objection_ledger') and not trace.get('conflict_ledger'):
        lines += ['Зафиксированных возражений/противоречий нет. Это не доказательство их отсутствия в досье.']
    lines += ['', '## Недостающие данные', '']
    gaps = list(dict.fromkeys([g for p in trace.get('initial_positions', {}).values() for g in p['missing_data']] +
                             (current['payload']['missing_data'] if current else [])))
    lines += ['- ' + gap for gap in gaps] or ['Пробелы не оценены.']
    for owner, vote in latest.items():
        lines += [f"- {names.get(owner, owner)} просит проверить: {query}"
                  for query in vote.get('evidence_requests', [])]
    lines += ['', '## Источники и границы проверки', '']
    manifest = trace.get('manifest', [])
    viewed = {id_ for event in trace.get('events', []) for id_ in event.get('evidence_ids', [])}
    viewed_sources = {trace['evidence_store'][id_]['source_id'] for id_ in viewed}
    lines += [f"Загружено источников: {len(manifest)}; показано моделям: {len(viewed_sources)}; chunks: {len(viewed)}.",
              'Полный inventory, поисковые ранги, версии, голоса и происхождение цитат сохранены в trace.json.',
              'Исходные даты досье не подтверждают актуальность сведений. Проверка substring не доказывает смысловую поддержку вывода.', '']
    from .schemas import citation_refs
    cited = list(dict.fromkeys((c.chunk_id, c.quote) for c in citation_refs(trace)))
    registry = {s['source_id']: s for s in manifest}
    for id_, quote in cited:
        e = trace.get('evidence_store', {}).get(id_)
        if e:
            s = registry[e['source_id']]
            lines += [f"- `{id_}` · `{s['origin']}` `{s['location']}` [{e['start']}:{e['end']}]: {json.dumps(quote, ensure_ascii=False)}"]
    lines += ['', f"Раундов: {len(decisions)}; model attempts: {trace.get('attempts', 0)}; время: {trace.get('elapsed', 0):.2f} с.", '']
    return '\n'.join(lines)


def write_report(trace, output: Path):
    output.mkdir(parents=True, exist_ok=False)
    # Do not announce a usable pair if either write fails.
    try:
        (output / 'trace.json').write_text(canonical(trace), encoding='utf-8')
        (output / 'report.md').write_text(render(trace), encoding='utf-8')
    except Exception:
        for name in ('trace.json', 'report.md'):
            path = output / name
            if path.is_file():
                path.unlink()
        raise
    return output / 'report.md'
