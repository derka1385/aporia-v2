import test from 'node:test';
import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { PassThrough, Writable } from 'node:stream';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DiscoveryManager } from '../server/discovery.mjs';
class Worker extends EventEmitter {
  constructor() { super(); this.stdout = new PassThrough(); this.stderr = new PassThrough(); this.input = []; this.signals = []; this.stdin = new Writable({ write: (chunk, _, done) => { this.input.push(JSON.parse(chunk)); done(); } }); }
  send(ev) { this.stdout.write(JSON.stringify(ev) + '\n'); }
  kill(signal) { this.signals.push(signal); if (['SIGTERM', 'SIGKILL'].includes(signal)) queueMicrotask(() => this.emit('exit', null)); }
}
function setup() {
  const dir = mkdtempSync(join(tmpdir(), 'aporia-discovery-')); const worker = new Worker(); const controller = new AbortController();
  const s = { id: 'fixture', question: 'Test fixture, not a generated result', seed: 31, delta: .6, model: 'local-fixture', protocol: {}, status: 'running', profiles: [] };
  const snapshots = [], calls = [];
  const engine = { active: new Map([[s.id, { controller, session: s }]]), publish: s => snapshots.push(structuredClone(s)), run: async (id, options) => { calls.push({ id, options }); s.profiles = [{ id: 'skeptic', status: 'complete', graph: { nodes: [] } }]; } };
  const manager = new DiscoveryManager({ engine, store: { get: () => null }, provider: { url: 'http://127.0.0.1:11434' }, spawnWorker: () => worker, jobRoot: dir });
  const config = manager.initialize(s, { targetCount: 1, trialBudget: 1 }, [{ name: s.model, family: 'fixture' }]);
  return { manager, engine, s, controller, worker, dir, config, snapshots, calls };
}
test('source/cognitive handoff stays in one active record and final briefs arrive before completion', async () => {
  const t = setup(); const finished = t.manager.run(t.s, t.config);
  t.worker.send({ type: 'corpus', papers: [{ id: 'P', sourceDigest: 'hash' }], corpus: { records: 1 } });
  t.worker.send({ type: 'cognition_request', grounding: { paper: { id: 'P' } } });
  await new Promise(r => setImmediate(r));
  assert.equal(t.s.status, 'running'); assert.equal(t.calls[0].options.continuation, true);
  assert.equal(t.worker.input[0].profiles[0].id, 'skeptic');
  t.worker.send({ type: 'result', result: { briefs: [{ id: 'B', score: .2 }], failures: [] } });
  t.worker.emit('exit', 0); await finished;
  assert.equal(t.s.status, 'complete'); assert.equal(t.s.discovery.briefs[0].id, 'B');
  assert.equal(t.s.protocol.discovery.sourceDigests[0].digest, 'hash'); assert.equal(t.engine.active.size, 0);
  rmSync(t.dir, { recursive: true });
});
test('cancel resumes a paused child before terminating and releases the active slot', async () => {
  const t = setup(); const finished = t.manager.run(t.s, t.config);
  t.manager.pause(t.s.id, true); t.s.status = 'cancelled'; t.controller.abort(); await finished;
  assert.deepEqual(t.worker.signals, ['SIGSTOP', 'SIGCONT', 'SIGTERM']);
  assert.equal(t.s.status, 'cancelled'); assert.equal(t.engine.active.size, 0); assert.equal(t.manager.running.size, 0);
  rmSync(t.dir, { recursive: true });
});
test('worker failure preserves paper retrieval and never becomes a completed discovery', async () => {
  const t = setup(); const finished = t.manager.run(t.s, t.config);
  t.worker.send({ type: 'corpus', papers: [{ id: 'P' }], corpus: { records: 1 } });
  t.worker.send({ type: 'mapping', claims: [{ id: 'P.c1', quote: 'Saved source passage' }], arguments: [{ id: 'P.arg1', valid: null }] });
  t.worker.send({ type: 'fatal', error: 'No readable full text' }); t.worker.emit('exit', 1); await finished;
  assert.equal(t.s.status, 'error'); assert.equal(t.s.discovery.papers[0].id, 'P'); assert.match(t.s.error, /full text/);
  assert.equal(t.s.discovery.claims[0].quote, 'Saved source passage'); assert.equal(t.s.discovery.arguments[0].valid, null);
  rmSync(t.dir, { recursive: true });
});
test('worker exit aborts and settles cognitive inference before releasing the active slot', async () => {
  const t = setup(); let settled = false;
  t.engine.run = async () => new Promise(resolve => t.controller.signal.addEventListener('abort', () => { settled = true; resolve(); }, { once: true }));
  const finished = t.manager.run(t.s, t.config);
  t.worker.send({ type: 'cognition_request', grounding: {} });
  await new Promise(r => setImmediate(r));
  t.worker.send({ type: 'fatal', error: 'Fixture worker failure' }); t.worker.emit('exit', 1); await finished;
  assert.equal(settled, true); assert.equal(t.s.status, 'error'); assert.equal(t.engine.active.size, 0);
  assert.equal(t.worker.input.length, 0);
  rmSync(t.dir, { recursive: true });
});
test('stop completion waits for cognitive cancellation and the inference slot to be released', async () => {
  const t = setup(); let settle;
  t.engine.run = async () => new Promise(resolve => { settle = resolve; });
  const finished = t.manager.run(t.s, t.config);
  t.worker.send({ type: 'cognition_request', grounding: {} }); await new Promise(r => setImmediate(r));
  t.s.status = 'cancelled'; t.controller.abort(); let stopped = false;
  const stopping = t.manager.stopped(t.s.id).then(() => { stopped = true; });
  await new Promise(r => setImmediate(r)); assert.equal(stopped, false); assert.equal(t.engine.active.size, 1);
  settle(); await stopping; await finished;
  assert.equal(t.engine.active.size, 0); assert.equal(t.s.status, 'cancelled');
  rmSync(t.dir, { recursive: true });
});
test('developing a saved record retains the original cognitive protocol and snapshot', async () => {
  const t = setup(); const source = { id: 'original', question: t.s.question, profiles: [{ id: 'skeptic', status: 'complete' }], protocol: { initialStateDigest: 'original-state', codeDigest: 'original-code' }, delta: .8, budget: 14, seed: 73, condition: 'architecture' };
  t.manager.store = { get: () => source, getInitialState: () => ({ memories: ['original memory'], rewards: [] }) }; t.config.sourceSessionId = source.id;
  const finished = t.manager.run(t.s, t.config);
  t.worker.send({ type: 'cognition_request', grounding: {} }); await new Promise(r => setImmediate(r));
  assert.equal(t.calls.length, 0); assert.equal(t.s.cognitiveSource.protocol.codeDigest, 'original-code');
  assert.equal(t.s.cognitiveSource.initialState.memories[0], 'original memory'); assert.equal(t.s.cognitiveSource.seed, 73);
  t.worker.send({ type: 'result', result: { briefs: [], failures: [] } }); t.worker.emit('exit', 0); await finished;
  assert.equal(t.s.cognitiveSourceId, source.id);
  rmSync(t.dir, { recursive: true });
});
