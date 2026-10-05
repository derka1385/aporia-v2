import asyncio
import json
import re
from pathlib import Path
from discovery import rank_briefs, finish_briefs
from crux_lab.graph.schema import Brief, Claim
from crux_lab.graph.store import Store
from crux_lab.graph.index import Embedder, HybridIndex
from crux_lab.llm.client import LLMClient


def candidate(**extra):
    return {'id': 'b', 'outcome': 'revision_required', 'novelty': .95,
            'assessment': {'overall': 4, 'grade': 'promising'},
            'contribution_novelty': {'novelty': .05, 'status': 'assessed'}, **extra}


def test_final_thesis_novelty_controls_ranking():
    b = rank_briefs([candidate()])[0]
    assert b['score'] == .032 and b['finalNovelty'] == .05


def test_unassessed_quality_or_contribution_cannot_rank():
    result = rank_briefs([candidate(assessment=None), candidate(id='c', contribution_novelty={'status': 'rerank_failed', 'novelty': None})])
    assert all(b['score'] is None and 'rank' not in b for b in result)


def test_failed_revision_does_not_replace_assessed_original():
    b = rank_briefs([candidate(revision={'assessment': None})])[0]
    assert b['quality'] == .8


def test_assess_revise_reassess_and_recheck_complete(monkeypatch, tmp_path):
    import discovery
    import crux_lab.lab.novelty as novelty
    from crux_lab.corpus import dedup
    dedup._CACHE.clear()
    monkeypatch.setattr(dedup, 'work_of', lambda p: p)
    monkeypatch.setattr(novelty, 'live_openalex', lambda *a: ([], 'test-disabled'))
    monkeypatch.setattr(discovery, 'BRIEFS', tmp_path)
    monkeypatch.setattr(discovery, 'RAW', tmp_path)
    monkeypatch.setattr(discovery, 'persist', lambda b, store: store.put(b))
    text = 'Relations can characterize a subject without constituting its existence.'
    ix = HybridIndex(['Y.c001'], [text], [{'paper_id': 'oa:Y', 'title': 'Synthetic prior-art fixture', 'quote': text}], embedder=Embedder('lsa'))
    monkeypatch.setattr(discovery.HybridIndex, 'load', lambda *a: ix)
    b = Brief(id='b', objection_id='o', research_question='Does composition threaten aseity?',
        argument={'id': 'a', 'title': 'Fixture argument', 'paper_id': 'oa:X', 'paper_title': 'Synthetic test paper',
        'premises': [{'id': 'X.c1', 'text': 'Composition entails dependence.', 'quote': 'Composition entails dependence.'}],
        'conclusion': {'id': 'X.c2', 'text': 'Aseity requires simplicity.'}, 'missing_premise': None, 'valid': True},
        challenged_premise={'id': 'X.c1', 'text': 'Composition entails dependence.'}, objection=text,
        strongest_responses=[], closest_literature=[], novelty=.95, records_searched=2,
        nearest=[], open_questions=['What kind of dependence?'], paper_direction='A paper here would argue for a distinction.', outcome='revision_required')
    def responder(system, messages, model):
        user = messages[-1]['content']
        if 'Restate the objection' in system:
            return json.dumps({'paper_vocabulary': 'composition dependence', 'plain_english': 'composition dependence', 'neighboring_tradition': 'relations existence'})
        if 'PROPOSED' in user or 'Passages:' in user:
            ns = [int(n) for n in re.findall(r'^\[(\d+)\]', user, re.M)]
            return json.dumps({'judgments': [{'n': n, 'verdict': 'same_move', 'similarity': .95, 'quote': text} for n in ns]})
        if 'PhD supervisor' in system:
            return json.dumps({'research_question': 'When does exemplification entail grounding?', 'paper_direction': 'A paper here would argue that characterization alone is insufficient.', 'what_changed': 'Narrowed the dependence claim.', 'narrowed': True, 'reply_to_strongest_objection': ' '.join(['This proposal distinguishes constitutive grounding from characterization and makes the dependence conditional.'] * 3)})
        return json.dumps({'coherence': 4, 'robustness': 4, 'significance': 4, 'specificity': 4,
            'strongest_objection': 'A competent reader would deny that a relation of exemplification establishes constitutive grounding of the subject.',
            'reply_available': True, 'what_it_needs': 'Defend the bridge from characterization to grounding.',
            'reasons': {c: 'The fixture specifies a concrete claim and a substantive test.' for c in ['coherence', 'robustness', 'significance', 'specificity']}, 'summary': 'Synthetic test judgment.'})
    client = LLMClient.fake(responder)
    store = Store(tmp_path / 'store.sqlite'); store.put(b)
    events = []
    results, failures = asyncio.run(finish_briefs(client, store, [{'objections': [], 'briefs': ['b'], 'run_id': 'run-X'}], {}, lambda t, **p: events.append(t)))
    assert not failures
    assert results[0]['revision']['assessment']['overall'] == 4
    assert results[0]['score'] == .032
    assert results[0]['contribution_novelty']['nearest'][0]['quote'] == text
    assert results[0]['markdown'] and events.count('stage') == 3
    store.close()
