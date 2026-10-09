import asyncio
import copy
import json

import pytest

from council.packing import MARKER, context_payload, pack_context, unpack_context
from council.runtime import Council
from council.schemas import canonical
from council.scripted import ScriptedAdapter


def test_record_tables_exact_roundtrip_missing_null_unicode_and_markers():
    rows = [{'long_field_name': 'Квалификация\r\n雪', 'another_long_field': i,
             '~columns': ['source'], '~missing': True, '~context_tables': 99}
            for i in range(8)]
    rows[0]['optional_field_long'] = None
    rows[1]['optional_field_long'] = False
    packet = {'rows': rows, 'owners': {'~owner'+str(i): r for i, r in enumerate(rows)},
              'mixed': [rows[0], None, 'text'], '~context_tables': {'~rows': 'source'},
              'nested': [{'small': 1}], 'previous_votes': {'owner': {'status': 'object'}}}
    before = copy.deepcopy(packet)
    packed = pack_context(packet)
    assert '~columns' in packed['rows']
    assert '~keys' in packed['owners']
    assert isinstance(packed['mixed'], list)
    assert packed['rows']['~rows'][0] != packed['rows']['~rows'][2]
    assert unpack_context(json.loads(canonical(packed))) == before == packet
    assert list(unpack_context(packed)['owners']) == list(packet['owners'])
    assert 'optional_field_long' not in unpack_context(packed)['rows'][2]
    assert unpack_context(packed)['rows'][0]['optional_field_long'] is None
    assert len(canonical(canonical(packed)).encode()) < len(canonical(canonical(packet)).encode())


@pytest.mark.parametrize('table', [
    {'~columns': ['a', 'a'], '~rows': [[1, 2]]},
    {'~columns': ['a'], '~rows': [[1, 2]]},
    {'~columns': ['a'], '~rows': [[1]], '~keys': []},
    {'~columns': ['a'], '~rows': [[1], [2]], '~keys': ['o', 'o']},
    {'~columns': ['a'], '~rows': [[1]], 'extra': 2},
    {'~columns': [1], '~rows': [[1]]},
    {'~columns': ['~bad'], '~rows': [[1]]},
    {'~columns': ['a'], '~rows': [[1]], '~keys': [1]},
    {'~missing': True},
    {'~columns': ['a'], '~rows': [[{'~missing': 1}]]},
    {'~columns': ['a'], '~rows': [[{'~missing': 1.0}]]},
    {'~columns': ['a'], '~rows': [[{'~missing': False}]]},
])
def test_malformed_tables_fail_closed(table):
    with pytest.raises(ValueError):
        unpack_context({MARKER: 1, 'data': table})


@pytest.mark.parametrize('version', [True, 2, None, '1'])
def test_unknown_version_rejected(version):
    with pytest.raises(ValueError):
        unpack_context({MARKER: version})


def test_key_type_and_nonprofitable_structures():
    with pytest.raises(ValueError):
        pack_context({'a': {1: 'not a JSON key'}})
    p = {'a': [{'x': 1}, {'x': 2}], 'b': []}
    assert pack_context(p)['a'] == p['a']
    assert unpack_context(p) == p


def test_all_three_round_requests_tables_measure_and_repair_identity(retriever, personas):
    class RepairOnce(ScriptedAdapter):
        async def generate(self, request):
            result = await super().generate(request)
            if request.stage == 'review' and request.version == 2 and 'repair' not in request.payload():
                output = json.loads(result.payload_json)
                output['target_digest'] = 'wrong'
                from council.model import Response
                return Response(canonical(output))
            return result

    adapter = RepairOnce('disagree')
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
    asyncio.run(c.run())
    assert c.status == 'no_consensus'
    assert len(c.decisions) == 3 and len(c.votes) == 3
    requests = [r for r in adapter.requests if r.version > 1 and r.stage in ('draft', 'review')]
    assert requests and any('repair' in r.payload() for r in requests)
    for r in requests:
        raw, restored = json.loads(r.payload_json), r.payload()
        assert raw[MARKER] == 1
        assert context_payload(restored) == r.payload_json
        assert len(r.serialized().encode('utf-8')) <= c.config.context_bytes
        ids = [e['evidence_id'] for row in restored['evidence'] for e in row['excerpts']]
        schema = json.loads(r.response_schema_json)
        assert schema['$defs']['Citation']['properties']['evidence_id']['enum'] == ids
    repaired = [r for r in requests if 'repair' in r.payload()]
    for r in repaired:
        before = next(p for p in requests if p.request_id == r.payload()['repair']['base_request_id'])
        after = r.payload()
        after.pop('repair')
        assert after == before.payload()
    assert c.trace()['context_table_version'] == 1
