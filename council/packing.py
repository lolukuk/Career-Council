"""Readable, lossless record tables for model INPUT only."""
import copy
from .schemas import canonical

VERSION = 1
MARKER = '~context_tables'
MISSING = {'~missing': True}


def _key(key):
    if not isinstance(key, str):
        raise ValueError('context key type')
    return '~' + key if key.startswith('~') else key


def _bytes(value):
    # Request embeds payload_json as a string: include its escaping.
    return len(canonical(canonical(value)).encode('utf-8'))


def _pack(value):
    if isinstance(value, dict):
        normal = {_key(k): _pack(v) for k, v in value.items()}
        keys, records = list(normal), list(normal.values())
    elif isinstance(value, list):
        normal = [_pack(v) for v in value]
        keys, records = None, normal
    else:
        return value
    if len(records) < 2 or any(not isinstance(r, dict) or '~columns' in r for r in records):
        return normal
    columns = sorted({k for record in records for k in record})
    table = {'~columns': columns,
             '~rows': [[record[k] if k in record else MISSING for k in columns] for record in records]}
    if keys is not None:
        table['~keys'] = keys
    return table if _bytes(table) < _bytes(normal) else normal


def pack_context(packet):
    if not isinstance(packet, dict):
        raise ValueError('context root')
    # Leave root metadata directly readable.
    result = {_key(k): _pack(v) for k, v in packet.items()}
    result[MARKER] = VERSION
    return result


def _unkey(key):
    if not isinstance(key, str) or (key.startswith('~') and not key.startswith('~~')):
        raise ValueError('context reserved key')
    return key[1:] if key.startswith('~~') else key


def _unpack(value):
    if isinstance(value, list):
        return [_unpack(v) for v in value]
    if not isinstance(value, dict):
        return value
    # Recognize generated tables before unescaping source-owned marker keys.
    if '~columns' in value:
        if set(value) not in ({'~columns', '~rows'}, {'~columns', '~rows', '~keys'}):
            raise ValueError('context table shape')
        columns, rows = value['~columns'], value['~rows']
        if not isinstance(columns, list) or any(not isinstance(k, str) for k in columns):
            raise ValueError('context columns')
        names = [_unkey(k) for k in columns]
        if len(set(names)) != len(names) or not isinstance(rows, list):
            raise ValueError('context duplicate columns')
        records = []
        for row in rows:
            if not isinstance(row, list) or len(row) != len(names):
                raise ValueError('context row width')
            record = {}
            for k, cell in zip(names, row):
                if isinstance(cell, dict) and set(cell) == {'~missing'} and cell['~missing'] is True:
                    continue
                record[k] = _unpack(cell)
            records.append(record)
        if '~keys' not in value:
            return records
        keys = value['~keys']
        if not isinstance(keys, list) or len(keys) != len(records):
            raise ValueError('context map keys')
        names = [_unkey(k) for k in keys]
        if len(set(names)) != len(names):
            raise ValueError('context duplicate map keys')
        return dict(zip(names, records))
    return {_unkey(k): _unpack(v) for k, v in value.items()}


def unpack_context(packet):
    if not isinstance(packet, dict):
        raise ValueError('context root')
    if MARKER not in packet:
        return copy.deepcopy(packet)
    if type(packet[MARKER]) is not int or packet[MARKER] != VERSION:
        raise ValueError('context table version')
    return {_unkey(k): _unpack(v) for k, v in packet.items() if k != MARKER}


def context_payload(packet):
    return canonical(pack_context(packet) if packet.get('previous_votes') else packet)
