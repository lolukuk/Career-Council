from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping


class SettingsError(ValueError):
    pass


MODEL_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:/-]{0,159}\Z')
EFFORTS = ('none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max')
KEYS = ('LLM_PROVIDER', 'LLM_MODEL', 'AITUNNEL_API_KEY', 'OPENAI_API_KEY', 'LLM_REASONING_EFFORT')


@dataclass(frozen=True)
class Settings:
    provider: str
    model: str
    api_key: str = field(repr=False)
    reasoning_effort: str | None = None
    aitunnel_test_mode: bool = False

    def __post_init__(self):
        if type(self.aitunnel_test_mode) is not bool or (self.aitunnel_test_mode and self.provider != 'aitunnel'):
            raise SettingsError('Условный тестовый режим доступен только для AI Tunnel.')


def load_settings(path: Path, *, provider=None, model=None, reasoning_effort=None, aitunnel_test_mode=False,
                  environ: Mapping[str, str] | None = None) -> Settings:
    """Read only the small, local settings file; never interpolate or execute values."""
    values = {}
    if path.exists():
        if path.stat().st_size > 65536:
            raise SettingsError('Файл настроек слишком большой.')
        try:
            contents = path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError):
            raise SettingsError('Не удалось прочитать локальный .env.') from None
        for line in contents.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, separator, value = line.partition('=')
            if name.strip() not in KEYS:
                continue  # Includes the legacy LLM_API_KEY: never a provider fallback.
            value = value.strip()
            if not separator or name.strip() in values:
                raise SettingsError('Повтор или некорректное поле настроек.')
            if value.startswith(('"', "'")):
                if len(value) < 2 or value[-1] != value[0]:
                    raise SettingsError('Незакрытые кавычки в настройках.')
                value = value[1:-1]
            values[name.strip()] = value
    env = os.environ if environ is None else environ
    values.update({key: env[key] for key in KEYS if key in env})
    selected = provider if provider is not None else values.get('LLM_PROVIDER', '')
    selected_model = model if model is not None else values.get('LLM_MODEL', '')
    if selected not in ('aitunnel', 'openai'):
        raise SettingsError('Укажите LLM_PROVIDER: aitunnel или openai.')
    if type(aitunnel_test_mode) is not bool or (aitunnel_test_mode and selected != 'aitunnel'):
        raise SettingsError('Условный тестовый режим доступен только для AI Tunnel.')
    if not MODEL_ID.fullmatch(selected_model) or selected_model.lower() == 'auto' or 'latest' in selected_model.lower():
        raise SettingsError('Укажите фиксированное название LLM_MODEL; auto/latest не поддерживаются.')
    key_name = 'AITUNNEL_API_KEY' if selected == 'aitunnel' else 'OPENAI_API_KEY'
    key = values.get(key_name, '')
    if not key or len(key) > 4096 or any(c.isspace() or ord(c) < 32 for c in key):
        raise SettingsError(f'Заполните {key_name} в локальном .env или окружении.')
    if key in selected_model:
        raise SettingsError('Название модели не должно содержать ключ.')
    effort = reasoning_effort if reasoning_effort is not None else values.get('LLM_REASONING_EFFORT', '')
    if effort and effort not in EFFORTS:
        raise SettingsError('Недопустимый LLM_REASONING_EFFORT.')
    return Settings(selected, selected_model, key, effort or None, aitunnel_test_mode)
