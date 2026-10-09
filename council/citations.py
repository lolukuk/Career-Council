"""Selectable frozen excerpts at the model boundary; internal citations stay exact."""
from __future__ import annotations

import copy
import re

from .schemas import Citation, DTO, Id, digest
from .feedback import pack_feedback

PROTOCOL = 'frozen-excerpt-enum-v2'
CITATION_STAGES = frozenset(('initial', 'draft', 'review'))


class Selection(DTO):
    evidence_id: Id


class SelectionError(ValueError):
    def __init__(self, code, path):
        self.code, self.path = code, path
        super().__init__(code)  # Never carry model text into feedback/audit.


def excerpts(chunk):
    """Keep paragraph meaning and exact offsets; never normalize source characters."""
    rows = []
    for block in re.finditer(r'[\s\S]+?(?:\r?\n[ \t]*\r?\n|\Z)', chunk.text):
        start, end = block.span()
        while start < end:
            stop = min(start + 400, end)
            if stop < end:
                boundary = max(chunk.text.rfind(' ', start + 200, stop),
                               chunk.text.rfind('\n', start + 200, stop))
                if boundary >= start + 200:
                    stop = boundary + 1
            quote = chunk.text[start:stop]
            rows.append({'evidence_id': 'q' + digest([chunk.chunk_id, chunk.digest, start, stop])[:12], 'text': quote})
            start = stop
    return rows


def response_schema(schema, selectable_ids=None):
    wire = copy.deepcopy(schema.model_json_schema())
    if 'Citation' in wire.get('$defs', {}):
        wire['$defs']['Citation'] = Selection.model_json_schema()
        if selectable_ids is not None:
            if not selectable_ids:
                from .schemas import Incomplete
                raise Incomplete('no selectable evidence')
            wire['$defs']['Citation']['properties']['evidence_id']['enum'] = list(selectable_ids)
    aliases = {name: f'd{i}' for i, name in enumerate(sorted(wire.get('$defs', {}))) if name != 'Citation'}
    def alias(node):
        if isinstance(node, dict):
            result = {k: alias(v) for k, v in node.items()}
            if '$defs' in result:
                result['$defs'] = {aliases.get(k, k): v for k, v in result['$defs'].items()}
            if '$ref' in result and result['$ref'].startswith('#/$defs/'):
                name = result['$ref'].removeprefix('#/$defs/')
                result['$ref'] = '#/$defs/' + aliases.get(name, name)
            return result
        if isinstance(node, list):
            return [alias(v) for v in node]
        return node
    wire = alias(wire)
    def compact(node):
        if isinstance(node, dict):
            # Annotation-only titles/defaults aren't provider constraints.
            # Required, nullable, bounds and local DTO defaults remain authoritative.
            return {k: compact(v) for k, v in node.items() if k not in ('title', 'default')}
        if isinstance(node, list):
            return [compact(v) for v in node]
        return node
    return compact(wire)


def project_packet(packet, evidence, review_owner=None):
    def compact(item):
        if isinstance(item, dict):
            if set(item) == {'chunk_id', 'quote'}:
                chunk = evidence[item['chunk_id']]
                if digest(chunk.text) != chunk.digest or item['quote'] not in chunk.text:
                    raise SelectionError('citation_selection_invalid', 'retained')
                matches = [e['evidence_id'] for e in excerpts(chunk) if e['text'] == item['quote']]
                if len(matches) == 1:
                    return {'evidence_id': matches[0]}
                start = chunk.text.index(item['quote'])
                # Locate the recorded literal for reading, not a reconstructed
                # original model choice when identical text has multiple offsets.
                return {'source_span': f"{chunk.chunk_id}:{start}:{start + len(item['quote'])}"}
            return {k: compact(v) for k, v in item.items()}
        if isinstance(item, list):
            return [compact(v) for v in item]
        return item
    # Repeated source audit metadata/citations are projected only in model input.
    # Frozen DTOs, decision digest, source text and report remain untouched.
    projected = compact(pack_feedback(packet))
    if review_owner is not None:
        for owner, position in projected.get('positions', {}).items():
            if owner != review_owner:
                position.pop('criteria', None)  # Only its owner can assess these IDs.
    projected['evidence_sources'] = {row['source_id']: {k: row[k] for k in ('origin', 'location') if k in row}
                                     for row in packet['evidence']}
    projected['evidence'] = [dict({k: v for k, v in row.items() if k not in ('text', 'origin', 'location') and
                                  not (k == 'section' and v in evidence[row['chunk_id']].text)},
                                excerpts=excerpts(evidence[row['chunk_id']]))
                             for row in packet['evidence']]
    return projected


def catalog(packet, evidence, seen):
    allowed = {}
    for row in packet.get('evidence', ()):
        id_ = row['chunk_id']
        if id_ not in seen or id_ not in evidence:
            raise SelectionError('citation_not_shown', 'evidence')
        chunk = evidence[id_]
        if row.get('source_id') != chunk.source_id:
            raise SelectionError('citation_selection_invalid', 'evidence')
        if digest(chunk.text) != chunk.digest:
            raise SelectionError('evidence_digest', 'evidence')
        expected = {e['evidence_id']: e['text'] for e in excerpts(chunk)}
        for option in row.get('excerpts', ()):
            selection = option['evidence_id']
            if selection not in expected or option['text'] != expected[selection] or selection in allowed:
                raise SelectionError('citation_selection_invalid', 'evidence')
            allowed[selection] = Citation(chunk_id=id_, quote=expected[selection])
    return allowed


def resolve_output(value, allowed, selected_ids=None):
    # Only fixed DTO field names and numeric indices enter an error path.
    fields = {'arguments', 'claims', 'citations', 'conflicts', 'new_conflicts', 'new_objections'}
    def visit(item, path):
        if isinstance(item, dict):
            if 'evidence_id' in item or set(item) == {'chunk_id', 'quote'}:
                if set(item) != {'evidence_id'} or not isinstance(item.get('evidence_id'), str):
                    raise SelectionError('citation_selection_shape', path)
                selection = item['evidence_id']
                if selection not in allowed:
                    raise SelectionError('citation_selection_not_shown', path)
                if selected_ids is not None:
                    selected_ids.append(selection)
                return allowed[selection].model_dump(mode='json')
            return {k: visit(v, f'{path}.{k}' if k in fields else path) for k, v in item.items()}
        if isinstance(item, list):
            return [visit(v, f'{path}[{i}]') for i, v in enumerate(item)]
        return item
    return visit(value, '$')
