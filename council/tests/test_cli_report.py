import json
from pathlib import Path

import pytest

from council.main import main
from council.report import render, write_report
from council.schemas import canonical
from test_protocol import run


def test_exact_report_and_no_human_vote(retriever, personas, tmp_path):
    c = run(retriever, personas)
    trace = c.trace()
    text = render(trace)
    assert canonical(trace['decisions'][-1]) not in text
    assert 'Рекомендация и план' in text and 'trace.json' in text
    assert all(p.name in text for p in personas.personas)
    assert 'scripted' in text and 'Человек принимает' in text
    report = write_report(trace, tmp_path / 'run')
    assert report.is_file()
    loaded = json.loads((report.parent / 'trace.json').read_text(encoding='utf-8'))
    assert loaded['decisions'][-1]['digest'] == c.decisions[-1].digest
    assert loaded['status'] == 'consensus'


def test_live_unconfigured_and_missing_dossier(tmp_path, monkeypatch):
    # Test runs must never consult personal credentials or paid provider endpoints.
    for key in ('LLM_PROVIDER', 'LLM_MODEL', 'OPENAI_API_KEY', 'AITUNNEL_API_KEY', 'LLM_REASONING_EFFORT'):
        monkeypatch.delenv(key, raising=False)
    assert main(['--mode', 'model', '--env-file', str(tmp_path / 'missing.env'),
                 '--dossier', str(tmp_path)]) == 2
    assert not list(tmp_path.iterdir())
    assert main(['--dossier', str(tmp_path), '--output', str(tmp_path / 'out')]) == 1
    trace = json.loads(next((tmp_path / 'out').glob('*/trace.json')).read_text(encoding='utf-8'))
    assert trace['status'] == 'failed' and not trace['decisions']


def test_output_failure_no_usable_pair(retriever, personas, tmp_path, monkeypatch):
    trace = run(retriever, personas).trace()
    original = Path.write_text
    def failed(self, *args, **kwargs):
        if self.name == 'report.md':
            raise OSError('test')
        return original(self, *args, **kwargs)
    monkeypatch.setattr(Path, 'write_text', failed)
    with pytest.raises(OSError):
        write_report(trace, tmp_path / 'run')
    assert not list((tmp_path / 'run').iterdir())
