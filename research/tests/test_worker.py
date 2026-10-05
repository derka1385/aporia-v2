import json
import os
import subprocess
import sys
from pathlib import Path
import pytest


@pytest.mark.parametrize('reject_formalizer', [False, True])
def test_complete_worker_pipeline_with_isolated_providers(tmp_path, reject_formalizer):
    topic = tmp_path / 'topic.json'
    topic.write_text(json.dumps({'slug': 'fixture', 'default': True, 'name': 'Synthetic fixture', 'area': 'metaphysics', 'queries': {}}))
    config = tmp_path / 'request.json'
    config.write_text(json.dumps({'question': 'Synthetic integration fixture, not a scientific result', 'targetCount': 1, 'trialBudget': 1, 'corpusLimit': 20, 'fulltextLimit': 3, 'topicFile': str(topic), 'delta': .6}))
    env = {**os.environ, 'APORIA_RUN_DIR': str(tmp_path), 'APORIA_TOPIC_FILE': str(topic), 'APORIA_EMBED_BACKEND': 'lsa'}
    if reject_formalizer:
        env['APORIA_TEST_REJECT_FORMALIZER'] = '1'
    profile = {'id': 'skeptic', 'model': 'fake-fakefam-a', 'graph': {'nodes': [{'type': 'objection', 'text': 'Characterization may not constitute existence.', 'importance': .8}]}}
    process = subprocess.run([sys.executable, str(Path(__file__).with_name('worker_fixture.py')), str(config)], input=json.dumps({'profiles': [profile]}) + '\n', text=True, capture_output=True, env=env, timeout=60)
    assert process.returncode == 0, process.stderr[-4000:]
    events = [json.loads(line) for line in process.stdout.splitlines() if line.startswith('{')]
    assert len([e for e in events if e['type'] == 'corpus']) == 3
    assert next(e for e in events if e['type'] == 'bridge')['mappedObjections'] == 1
    result = next(e for e in events if e['type'] == 'result')['result']
    assert result['corpus']['records'] == 2 and result['corpus']['fulltexts'] == 2
    assert len(result['targets']) == 1
    assert result['papers'][0]['id'] == 'oa:W1'  # raw OpenAlex works must be normalized
    assert result['papers'][0]['sourceDigest']
    assert result['arguments'][0]['valid'] is (None if reject_formalizer else True)
    if reject_formalizer:
        assert len(result['failures']) == 1
        assert result['failures'][0]['stage'] == 'formalization'
    else:
        assert not result['failures'], result['failures']
    assert len(result['runs'][0]['trials']) == 1
    assert len(result['briefs']) == 1
    brief = result['briefs'][0]
    assert brief['revision']['assessment']['overall'] == 4
    assert brief['contribution_novelty']['status'] == 'assessed'
    assert brief['score'] == .64 and brief['rank'] == 1
    assert brief['argument']['premises'][0]['quote']
    assert brief['markdown'] and (tmp_path / 'discovery.json').exists()
