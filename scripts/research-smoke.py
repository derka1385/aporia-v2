"""Bounded real-service check. No experiment or research result is fabricated."""
import asyncio
import json
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research'))
os.environ['CRUX_LAB_TRACING'] = '0'
os.environ['ENABLE_CLI_PROVIDERS'] = '0'
import httpx
from pydantic import BaseModel
from local_provider import LocalClient
from crux_lab.corpus.openalex import search, to_paper

class Plan(BaseModel):
    searches: list[str]

async def main():
    models = httpx.get('http://127.0.0.1:4317/api/health').json()['models']
    path = Path('data/verification'); path.mkdir(parents=True, exist_ok=True)
    client = LocalClient({'models': models, 'model': 'qwen2.5:3b', 'ollamaUrl': 'http://127.0.0.1:11434', 'jobDir': str(path), 'seed': 31, 'callBudget': 3}, lambda *a, **k: None)
    out, _ = await client.json('extractor', 'Find two short philosophy search terms for divine simplicity.', Plan, 'Return two short academic search terms. Do not invent papers.', max_tokens=120)
    if not out:
        raise RuntimeError('Local structured completion could not be validated')
    papers = [to_paper(w) for w in search('"divine simplicity"', max_records=3, per_page=3, field='search')]
    result = {'verified': 'local structured completion and real OpenAlex metadata', 'plan': out.model_dump(), 'works': [{'id': p['id'], 'title': p['title'], 'url': p['url']} for p in papers], 'usage': client.local.usage, 'models': client.resolved}
    if not papers:
        raise RuntimeError('OpenAlex returned no works for the probe')
    (path / 'research-smoke.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({'structuredCompletion': True, 'openAlexWorks': result['works'], 'calls': client.local.usage['calls']}))

asyncio.run(main())
