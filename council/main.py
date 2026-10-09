from __future__ import annotations

import argparse
import asyncio
import sys
import threading
import time
import uuid
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from council.retrieval import Encoder, Retriever
from council.report import write_report
from council.runtime import Council
from council.schemas import Cancelled, Config, Incomplete
from council.scripted import ScriptedAdapter
from council.sources import Sources, load_personas
from council.settings import EFFORTS, SettingsError, load_settings
from council.providers import make_adapter
from council.model import output_token_ceiling


def main(argv=None) -> int:
    user_prompt = (
        "I'm thinking about switching careers from mechanical engineering "
        "to software development. Help me think through this decision."
    )
    parser = argparse.ArgumentParser(description='Пять персон: bounded consensus prototype')
    parser.add_argument('--mode', choices=('scripted', 'model'), default='scripted')
    parser.add_argument('--scenario', choices=('agree', 'revise', 'disagree'), default='agree')
    parser.add_argument('--max-rounds', type=int, choices=range(1, 4), default=3,
                        help='Число полностью проверяемых версий решения (1–3); разногласия сохраняются в отчёте')
    parser.add_argument('--question', default=user_prompt)
    parser.add_argument('--dossier', type=Path, default=Path(__file__).resolve().parent / 'data')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'output')
    parser.add_argument('--provider', choices=('aitunnel', 'openai'))
    parser.add_argument('--model', help='Название модели, заданное пользователем')
    parser.add_argument('--env-file', type=Path, default=Path(__file__).resolve().parent / '.env')
    parser.add_argument('--reasoning-effort', choices=EFFORTS, help='Необязательная настройка поддерживаемой модели')
    parser.add_argument('--aitunnel-test-mode', action='store_true', help='Условный лимит ответа только для тестового AI Tunnel')
    args = parser.parse_args(argv)
    if args.aitunnel_test_mode and args.mode != 'model':
        parser.error('--aitunnel-test-mode требует --mode model и AI Tunnel.')
    if args.mode == 'model':
        try:
            settings = load_settings(args.env_file, provider=args.provider, model=args.model,
                                     reasoning_effort=args.reasoning_effort, aitunnel_test_mode=args.aitunnel_test_mode)
        except (SettingsError, OSError) as exc:
            print(str(exc) if isinstance(exc, SettingsError) else 'Не удалось прочитать .env.', file=sys.stderr)
            return 2
        adapter = make_adapter(settings)
    else:
        adapter = ScriptedAdapter(args.scenario)
    config, cancel = Config(max_rounds=args.max_rounds), threading.Event()
    started = time.monotonic()
    preparation = {'schema_version': 1, 'run_id': uuid.uuid4().hex, 'status': 'preparing',
                   'mode': args.mode, 'question': args.question, 'reason': '', 'decisions': [],
                   'manifest': [], 'evidence_store': {}, 'initial_positions': {}, 'events': [], 'attempts': 0}
    preparation.update(model=adapter.capabilities.identity, provider=adapter.capabilities.provider,
                       accounting_policy=adapter.capabilities.accounting_policy,
                       output_limit_policy=adapter.capabilities.output_limit_policy,
                       requested_output_tokens=config.output_tokens)
    preparation['accepted_output_token_ceiling'] = output_token_ceiling(adapter.capabilities, config.output_tokens)
    if args.mode == 'model':
        preparation['reasoning_effort'] = settings.reasoning_effort
    encoder = Encoder(config, Path(__file__).resolve().parent / '.cache' / 'models', cancel)
    reader = Sources(config, cancel=cancel)
    async def execute():
        if args.mode == 'model':
            try:
                await asyncio.wait_for(adapter.prepare(config.output_tokens), timeout=config.preparation_timeout)
            except asyncio.TimeoutError:
                raise Incomplete('provider preparation deadline') from None
        personas = load_personas(args.dossier / 'personas.md')
        preparation['persona_config'] = personas.model_dump(mode='json')
        sources = reader.load(args.dossier)
        preparation['manifest'] = [s.model_dump(mode='json') for s in sources]
        remaining = config.preparation_timeout - (time.monotonic() - started)
        if remaining <= 0:
            raise Incomplete('preparation deadline')
        encoder.config = config.model_copy(update={'preparation_timeout': remaining})
        retriever = Retriever.prepare(sources, encoder)
        preparation_elapsed = time.monotonic() - started
        if preparation_elapsed > config.preparation_timeout:
            raise Incomplete('preparation deadline')
        council = Council(args.question, personas, sources, retriever, adapter, config, cancel)
        await council.run()
        result = council.trace()
        result['preparation_elapsed'] = preparation_elapsed
        result['tasker_events'] = reader.events
        result['encoder_events'] = encoder.events
        return result

    async def managed():
        result = None
        try:
            result = await execute()
            return result
        finally:
            if args.mode == 'model':
                try:
                    await adapter.aclose()
                except Exception:
                    (result if result is not None else preparation)['client_cleanup'] = 'incomplete'

    try:
        trace = asyncio.run(managed())
    except KeyboardInterrupt:
        cancel.set()
        preparation.update(status='cancelled', reason='Отменено пользователем.', elapsed=time.monotonic() - started)
        trace = preparation
    except (Incomplete, Cancelled) as exc:
        preparation.update(status='cancelled' if isinstance(exc, Cancelled) else 'incomplete',
                           reason=str(exc), elapsed=time.monotonic() - started)
        trace = preparation
    except Exception as exc:
        preparation.update(status='failed', reason=getattr(exc, 'safe_code', None) or (type(exc).__name__ + ': preparation failure'), elapsed=time.monotonic() - started)
        trace = preparation
    trace.setdefault('tasker_events', reader.events)
    trace.setdefault('encoder_events', encoder.events)
    try:
        output = write_report(trace, args.output / trace['run_id'])
    except (OSError, ValueError):
        print('Не удалось сохранить полный отчёт; usable artifact не создан.', file=sys.stderr)
        return 3
    print(f"{trace['status']}: {output}")
    return 0 if trace['status'] in ('consensus', 'no_consensus') else 1


if __name__ == "__main__":
    raise SystemExit(main())
