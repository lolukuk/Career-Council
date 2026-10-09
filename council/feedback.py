"""Lossless input-only packing of completed votes; original state is untouched."""
import copy

from .schemas import digest

IDENTITY = ('run_id', 'snapshot_id', 'target_version', 'target_digest')
GROUPS = ('criterion_checks', 'claim_assessments', 'objection_checks', 'conflict_checks')
COLUMNS = ('id', 'status', 'rationale', 'claim_ref', 'caveat_ref', 'condition_text_ref')


def ledger_matches(packet, group, owner, version, item):
    keys = ('text', 'citations', 'blocking') if group == 'obligations' else ('text', 'citations')
    return [entry for entry in packet.get(group, ()) if
            entry['owner'] == owner and entry['origin_version'] == version and
            {k: entry[k] for k in keys} == item]


def pack_feedback(packet):
    result = copy.deepcopy(packet)
    if not result.get('previous_votes'):
        return result
    targets, conditions = {}, {}

    def reference(table, prefix, value):
        key = prefix + digest(value)[:12]
        if key in table and table[key] != value:
            raise ValueError('feedback reference collision')
        table[key] = value
        return key

    for owner, vote in result['previous_votes'].items():
        target = {key: vote.pop(key) for key in IDENTITY}
        vote['target_ref'] = reference(targets, 't', target)
        for group in GROUPS:
            rows = []
            for check in vote[group]:
                if set(check) != set(COLUMNS[:-1]) | {'condition_text'}:
                    raise ValueError('feedback check shape')
                condition = check['condition_text']
                rows.append([check[key] for key in COLUMNS[:-1]] +
                            [reference(conditions, 'c', condition) if condition is not None else None])
            vote[group] = rows
        for field, group, refkey in (('new_objections', 'obligations', 'objection_ref'),
                                     ('new_conflicts', 'conflicts', 'conflict_ref')):
            items = []
            for item in vote[field]:
                matches = ledger_matches(result, group, owner, target['target_version'], item)
                items.append({refkey: matches[0]['id']} if len(matches) == 1 else item)
            vote[field] = items
    result['feedback_layout'] = {'version': 1, 'check_columns': list(COLUMNS), 'check_groups': list(GROUPS)}
    result['vote_targets'], result['vote_conditions'] = targets, conditions
    return result


def unpack_feedback(packet):
    """Restore the original full packet for audit/roundtrip; not model output repair."""
    result = copy.deepcopy(packet)
    if 'feedback_layout' not in result:
        return result
    if result.pop('feedback_layout') != {'version': 1, 'check_columns': list(COLUMNS), 'check_groups': list(GROUPS)}:
        raise ValueError('feedback layout version')
    targets, conditions = result.pop('vote_targets'), result.pop('vote_conditions')
    for owner, vote in result['previous_votes'].items():
        target = targets[vote.pop('target_ref')]
        vote.update(target)
        for group in GROUPS:
            checks = []
            for row in vote[group]:
                if len(row) != len(COLUMNS):
                    raise ValueError('feedback row width')
                check = dict(zip(COLUMNS[:-1], row[:-1]))
                check['condition_text'] = conditions[row[-1]] if row[-1] is not None else None
                checks.append(check)
            vote[group] = checks
        for field, group, refkey in (('new_objections', 'obligations', 'objection_ref'),
                                     ('new_conflicts', 'conflicts', 'conflict_ref')):
            items = []
            for item in vote[field]:
                if set(item) == {refkey}:
                    keys = ('text', 'citations', 'blocking') if group == 'obligations' else ('text', 'citations')
                    matches = [entry for entry in result[group] if entry['id'] == item[refkey] and
                               entry['owner'] == owner and entry['origin_version'] == target['target_version']]
                    if len(matches) != 1:
                        raise ValueError('feedback ledger reference')
                    item = {key: matches[0][key] for key in keys}
                items.append(item)
            vote[field] = items
    return result
