"""Deterministic providers around the real worker, executed in a disposable subprocess."""
import asyncio
import contextvars
import json
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from crux_lab.corpus import openalex, pdf, dedup
from crux_lab.llm.client import LLMClient
from crux_lab.lab import novelty
import local_provider
import worker

QUOTES = ['Every constitutive part introduces dependence.',
          'The subject has constitutive parts.',
          'The subject therefore depends on those parts.']
CASE = ('Consider a subject whose properties describe its activities without producing its existence. '
        'A reader treats the descriptions as parts simply because they can be distinguished in thought. '
        'The subject continues to exist if those descriptions change. The proposed dependence follows '
        'only if descriptions are constitutive causes, so the original premise needs a substantive bridge.')
REPLY = 'The premise needs a narrower interpretation.'
current = contextvars.ContextVar('structured_schema')
original_json = LLMClient.json

async def structured(self, role, user, schema, system='', **kwargs):
    token = current.set(schema.__name__)
    try:
        return await original_json(self, role, user, schema, system, **kwargs)
    finally:
        current.reset(token)

LLMClient.json = structured

def responder(system, messages, model):
    # The schema context follows each concurrent task, while real client validation/retries still run.
    kind = current.get(None)
    user = next((m['content'] for m in messages if 'JSON schema:' in m['content']), messages[-1]['content'])
    ids = list(dict.fromkeys(re.findall(r'W\d+\.c\d+', user)))
    target = (re.search(r'Attack (W\d+\.[\w.]+)', user) or re.search(r'(W\d+\.c\d+)', user))
    if kind == 'Plan':
        out = {'name': 'Fixture dependence', 'area': 'metaphysics', 'searches': ['composition dependence', 'constitutive parts'], 'schools': ['Platonism', 'Nominalism']}
    elif kind == 'Screen':
        out = {'in_area': True, 'argues_for_thesis': True, 'thesis': QUOTES[-1], 'topic_relevance': 3, 'argument_clarity': 3, 'english': True}
    elif kind == 'ChunkOut':
        out = {'claims': [{'kind': 'conclusion' if i == 2 else 'premise', 'text': q, 'quote': q} for i, q in enumerate(QUOTES)]}
    elif kind == 'ArgumentsOut':
        out = {'arguments': [{'title': 'Dependence from parts', 'premise_ids': ids[:2], 'conclusion_id': ids[2]}]}
    elif kind == 'FormalOut':
        out = {'atoms': {'A': QUOTES[1], 'B': QUOTES[2]}, 'premise_formulas': {ids[0]: 'A -> B', ids[1]: 'A'}, 'conclusion_formula': 'B'}
        if os.environ.get('APORIA_TEST_REJECT_FORMALIZER'):
            out['premise_formulas'] = {}
    elif kind == 'AbstractBatch':
        out = {'papers': [{'paper_id': p, 'claims': [{'kind': 'objection', 'text': QUOTES[0], 'quote': QUOTES[0]}]} for p in re.findall(r'paper_id: (oa:W\d+)', user)]}
    elif kind in ('GenOut', 'TraditionOut', 'SharpenOut'):
        out = {'target_premise_id': target.group(1), 'objection': CASE, 'premise_fails_because': 'The premise confuses characterization with constitutive dependence.'}
        if kind == 'TraditionOut':
            out['school'] = re.search(r'You have been asked to take: ([^.]+)\.', system).group(1)
        if kind == 'SharpenOut':
            out['usable'] = True
    elif kind == 'Restatements':
        out = {'paper_vocabulary': 'constitutive parts dependence', 'plain_english': 'descriptions and causes', 'neighboring_tradition': 'properties and grounding'}
    elif kind == 'RerankOut':
        out = {'judgments': [{'n': int(n), 'verdict': 'different', 'similarity': .2, 'quote': ''} for n in re.findall(r'^\[(\d+)\]', user, re.M)]}
    elif kind == 'PrescreenOut':
        out = {'misreading': False, 'explanation': 'The challenge concerns a source premise.', 'deciding_quote': CASE.split('. ')[0] + '.'}
    elif kind == 'DefenderOut':
        out = {'misreading_check': 'The objection identifies a genuine qualification.', 'reply': REPLY, 'cited_claim_ids': [], 'concedes': False, 'revised_premise': None}
    elif kind == 'LabelOut':
        out = {'outcome': 'standing', 'deciding_quote': REPLY, 'rationale': 'The replies leave the distinction unresolved.'}
    elif kind == 'BriefOut':
        out = {'research_question': 'When does characterization entail constitutive dependence?', 'strongest_responses': [{'defender': 'Defender A', 'response': REPLY, 'why_it_failed': 'No bridge principle was established.'}], 'open_questions': ['What makes a part constitutive?', 'How can the distinction be tested?'], 'paper_direction': 'A paper here would argue for a conditional bridge principle between parts and grounding.'}
    elif kind == 'AssessOut':
        out = {c: 4 for c in ('coherence', 'robustness', 'significance', 'specificity')}
        out.update(strongest_objection='A competent reader would deny that characterizing a subject establishes constitutive grounding of its existence.', reply_available=True, what_it_needs='A defensible bridge principle and explicit counterexamples.', reasons={c: 'The fixture states a concrete claim and a substantive test.' for c in out}, summary='Synthetic fixture assessment.')
    elif kind == 'ReviseOut':
        out = {'research_question': 'Which constitutive parts ground existence?', 'paper_direction': 'A paper here would argue that characterization implies dependence only under a constitutive bridge principle.', 'what_changed': 'Narrowed the dependence claim.', 'narrowed': True, 'reply_to_strongest_objection': ' '.join(['The proposal distinguishes constitutive grounding from characterization and makes the dependence conditional on a defended bridge principle.'] * 3)}
    else:
        return CASE
    return json.dumps(out)

client = LLMClient.fake(responder)
client.local = SimpleNamespace(usage={'calls': 0, 'inputTokens': 0, 'outputTokens': 0})
client.seed_objections = {}
local_provider.LocalClient = lambda *a: client

def works(*a, **kw):
    abstract = ' '.join(QUOTES)
    inv = {}
    for i, word in enumerate(abstract.split()):
        inv.setdefault(word, []).append(i)
    for i in (1, 2):
        yield {'id': f'https://openalex.org/W{i}', 'display_name': f'Synthetic fixture paper {i}', 'publication_year': 2026, 'publication_date': '2026-09-01', 'language': 'en', 'abstract_inverted_index': inv, 'best_oa_location': {'pdf_url': f'https://example.org/fixture{i}.pdf'}, 'cited_by_count': 3-i, 'type': 'article'}

openalex.search = works

def fulltext(pid, url):
    text = ' '.join(QUOTES) + '\n' + ('The subject and the constitution of its parts is the question that is examined. ' * 125)
    path = pdf.text_path(pid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return text

pdf.get_fulltext = fulltext
novelty.live_openalex = lambda *a: ([], 'fixture-disabled')
dedup.work_of = lambda p: p
config = json.loads(Path(sys.argv[1]).read_text())
asyncio.run(worker.run(config))
