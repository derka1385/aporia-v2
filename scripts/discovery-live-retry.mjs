// Targeted real-service validation after a code fix. Reuse the failed job's evidence;
// keep the original session and files intact. No synthetic model responses.
import { readFileSync, writeFileSync, cpSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
const previous = readFileSync('data/verification/live-discovery-id.txt', 'utf8').trim();
const oldRoot = resolve('research/data/jobs', previous);
const request = JSON.parse(readFileSync(resolve(oldRoot, 'request.json'), 'utf8'));
const sessions = await (await fetch('http://127.0.0.1:4317/api/sessions')).json();
if (sessions.some(s => ['running', 'paused'].includes(s.status))) throw new Error('An active local run already exists.');
const prior = await (await fetch(`http://127.0.0.1:4317/api/sessions/${previous}`)).json();
if (prior.status !== 'error') throw new Error('This check only retries the preserved failed validation.');
const health = await (await fetch('http://127.0.0.1:4317/api/health')).json();
for (const model of request.models) {
  const current = health.models.find(m => m.name === model.name);
  if (!current || current.digest !== model.digest) throw new Error('Model identity changed; evidence cache cannot be reused.');
}
const r = await fetch('http://127.0.0.1:4317/api/sessions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...request, models: {}, workflow: 'discovery', profiles: ['skeptic'], condition: 'architecture', budget: 8, memoryMode: 'fresh' }) });
const session = await r.json(); if (!r.ok) throw new Error(session.error);
const newRoot = resolve('research/data/jobs', session.id);
// Copy before source mapping begins; the worker initializes immutable request/topic first.
// Only reusable evidence and content-addressed completions move, never logs or results.
for (const part of ['data/raw', 'data/crux.sqlite', 'data/crux.sqlite-wal', 'data/crux.sqlite-shm', 'cache/llm']) {
  const from = resolve(oldRoot, part); if (existsSync(from)) cpSync(from, resolve(newRoot, part), { recursive: true });
}
const reuse = { retryOf: previous, reused: ['cached source text', '48 verified extracted claims', 'content-addressed local completions'], reason: 'Correct compact JSON schema preserving actual title properties', originalPreserved: true };
writeFileSync(resolve(newRoot, 'verification-reuse.json'), JSON.stringify(reuse, null, 2));
writeFileSync('data/verification/live-discovery-retry-id.txt', session.id);
console.log({ id: session.id, retryOf: previous, status: session.status });
