"""Clearly labeled protocol fixtures, never a substitute for independent LLM reasoning."""
import json

from .model import Capabilities, Response
from .schemas import canonical


class ScriptedAdapter:
    mode = 'scripted'
    capabilities = Capabilities(configured=True, identity='scripted-fixtures-v1')

    def __init__(self, scenario='agree'):
        if scenario not in ('agree', 'revise', 'disagree', 'conflict'):
            raise ValueError('unknown scripted scenario')
        self.scenario = scenario
        self.requests = []

    def count_tokens(self, request):
        raise ValueError('scripted mode does not claim provider token accounting')

    async def generate(self, request):
        self.requests.append(request)
        p = request.payload()
        if request.stage == 'notes':
            ids = [e['chunk_id'] for e in p['evidence']
                   if any(term in e['text'].lower() for term in ('coding', 'career', 'software', 'bootcamp'))]
            return Response(canonical({'relevant_chunk_ids': ids}))
        if request.stage == 'tools':
            results = p.get('tool_results', [])
            if not results:
                action = {'name': 'get_tasks', 'task_id': None}
            elif len(results) == 1 and results[0]['records']:
                action = {'name': 'get_task_details', 'task_id': results[0]['records'][0]['task_id']}
            else:
                action = {'name': 'finish', 'task_id': None}
            return Response(canonical(action))
        if request.stage == 'initial':
            chunk = next(e for e in p['evidence'] if e['source_id'] == 'profile' or e['source_id'] == 's0')
            citation = {'evidence_id': chunk['excerpts'][0]['evidence_id']}
            framework = p['persona']['description'][:160]
            conflicts = []
            if self.scenario == 'conflict' and request.persona_id == 'robert_reich':
                other = next(e for e in p['evidence'] if e['chunk_id'] != chunk['chunk_id'])
                conflicts = [{'text': 'Сценарная пара требует раскрытия неопределённости.',
                              'citations': [citation, {'evidence_id': other['excerpts'][0]['evidence_id']}]}]
            result = {'recommendation': 'Проверить переход ограниченным экспериментом.',
                      'arguments': [{'text': 'Профиль пользователя доступен; это основание для проверки ограничений.',
                                     'basis': 'source', 'citations': [citation]}],
                      'criteria': [{'id': 'c1', 'text': 'План явно ограничивает риск и не обещает найм.'}],
                      'strongest_counterargument': 'Проверка может упустить привлекательную возможность.',
                      'missing_data': ['Нужны актуальные расходы, условия найма и ограничения времени.'],
                      'conflicts': conflicts}
            # Different framework concerns without fabricated user facts.
            result['recommendation'] = {
                'peter_thiel': 'Проверить преимущество конкретного проекта перед сертификатами.',
                'warren_buffett': 'Сначала проверить понятность работы и запас безопасности.',
                'robert_reich': 'Проверить распределение трудового риска и условия найма.',
                'nassim_nicholas_taleb': 'Проверить обратимый эксперимент с ограниченным ущербом.',
                'marcus_aurelius': 'Проверить контролируемые действия и обязательства.'}[request.persona_id]
            return Response(canonical(result))
        if request.stage == 'draft':
            first = next(iter(p['positions'].values()))['arguments'][0]
            reference = first['citations'][0]
            chunk = next(e for e in p['evidence'] if
                         (reference.get('source_span', '').split(':')[0] == e['chunk_id'] or
                          any(x['evidence_id'] == reference.get('evidence_id') for x in e['excerpts'])))
            safe = request.version > 1 or self.scenario == 'agree' or self.scenario == 'conflict'
            recommendation = 'Проверить переход без немедленного увольнения; решение принять после сбора данных.' if safe else 'Проверить переход и затем выбрать следующий шаг.'
            result = {'recommendation': {'text': recommendation, 'claim_refs': ['c1']},
                      'steps': [{'text': 'Уточнить расходы, benefits, время и условия найма; проверить реальный проект.',
                                 'claim_refs': ['c1']}],
                      'claims': [{'id': 'c1', 'text': 'Предоставлен профиль пользователя; текущие условия нуждаются в проверке.',
                                  'basis': 'source', 'citations': [{'evidence_id': chunk['excerpts'][0]['evidence_id']}]}],
                      'alternatives': ['Сравнить обучение при сохранении работы и полный переход.'],
                      'missing_data': ['Актуальный бюджет и проверяемые условия найма.'],
                      'caveats': [], 'objection_responses': [], 'conflict_responses': [],
                      'change_summary': 'Добавлены ограничения и ответы на возражения.' if request.version > 1 else ''}
            for o in p['obligations']:
                result['objection_responses'].append({'id': o['id'], 'text': 'Сохранён запрет немедленного увольнения до проверки.', 'claim_refs': ['c1']})
            for i, c in enumerate(p['conflicts']):
                k = f'k{i+1}'
                result['caveats'].append({'id': k, 'text': 'Противоречивые сведения не позволяют предсказать исход; нужна проверка.', 'claim_refs': ['c1']})
                result['conflict_responses'].append({'id': c['id'], 'text': 'Обе стороны сохранены, неопределённость раскрыта.', 'claim_refs': ['c1'], 'caveat_ref': k})
            return Response(canonical(result))
        d = p['decision']
        payload = d['payload']
        oppose = (self.scenario == 'disagree' and request.persona_id == 'warren_buffett') or (
            self.scenario == 'revise' and request.persona_id == 'warren_buffett' and d['version'] == 1)
        result = {'run_id': d['run_id'], 'snapshot_id': d['snapshot_id'], 'target_version': d['version'],
                  'target_digest': d['digest'], 'verdict': 'object' if oppose else 'approve',
                  'rationale': 'Недостаточно ограничения риска.' if oppose else 'Одобряю именно план проверки, без обещаний исхода.',
                  'criterion_checks': [{'id': c['id'], 'status': 'unmet' if oppose else 'satisfied', 'rationale': 'Проверено ограничение риска.'} for c in p['positions'][request.persona_id]['criteria']],
                  'objection_checks': [], 'conflict_checks': [],
                  'claim_assessments': [{'id': c['id'], 'status': 'supported', 'rationale': 'Профиль показан, будущий исход не утверждается.'} for c in payload['claims']],
                  'payload_assessment': {'status': 'supported', 'rationale': 'Весь проект оценён.', 'unregistered_assertions': []},
                  'new_objections': [], 'new_conflicts': [],
                  'change_explanation': 'План соотнесён с исходной позицией и аргументами остальных.', 'evidence_requests': []}
        for o in p['obligations']:
            if o['owner'] == request.persona_id:
                response = next(r for r in payload['objection_responses'] if r['id'] == o['id'])
                result['objection_checks'].append({'id': o['id'], 'status': 'upheld' if oppose else 'resolved',
                                                   'rationale': 'Перепроверено для текущей версии.', 'claim_ref': response['claim_refs'][0]})
        for c in p['conflicts']:
            if c['owner'] == request.persona_id:
                r = next(r for r in payload['conflict_responses'] if r['id'] == c['id'])
                caveat = next(k for k in payload['caveats'] if k['id'] == r['caveat_ref'])
                result['conflict_checks'].append({'id': c['id'], 'status': 'uncertainty_in_decision',
                    'rationale': 'Обе стороны проверены.', 'claim_ref': r['claim_refs'][0],
                    'caveat_ref': caveat['id'], 'condition_text': caveat['text']})
        if oppose and not any(o['owner'] == request.persona_id for o in p['obligations']):
            result['new_objections'] = [{'text': 'Нельзя переходить без явно проверенного запаса безопасности.', 'blocking': True}]
        return Response(canonical(result))
