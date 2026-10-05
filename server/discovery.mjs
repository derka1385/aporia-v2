import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

export const stages = ['literature', 'fulltext', 'selection', 'mapping', 'indexing', 'cognition', 'debate', 'assessment', 'revision', 'contribution_novelty', 'complete'];
export class DiscoveryManager {
  constructor({ engine, store, provider, spawnWorker = spawn, jobRoot = resolve('research/data/jobs') }) { Object.assign(this, { engine, store, provider, spawnWorker, jobRoot }); this.running = new Map(); this.finished = new Map(); }
  ready() { return existsSync(resolve('research/.venv/bin/python')); }
  initialize(s, settings, models) {
    s.workflow = 'discovery'; s.discovery = { version: 1, stage: 'literature', progress: 0, papers: [], targets: [], runs: [], briefs: [], events: [], failures: [], settings, models: null };
    const jobDir = resolve(this.jobRoot, s.id); mkdirSync(jobDir, { recursive: true });
    const topicFile = resolve(jobDir, 'topic.json');
    writeFileSync(topicFile, JSON.stringify({ slug: 'inquiry', name: s.question, area: 'philosophy', queries: {} }));
    const config = { ...settings, question: s.question, model: s.model, models, seed: s.seed, delta: s.delta, jobDir, topicFile, ollamaUrl: this.provider.url, callBudget: 600 };
    writeFileSync(resolve(jobDir, 'request.json'), JSON.stringify(config, null, 2));
    s.protocol.discovery = { sourceRevision: '22299f7f31178cdd357a410cac8d0808f5dcd179', jobId: s.id, settings, modelAssignments: models, sourceDigests: [] };
    this.engine.publish(s); return config;
  }
  async run(s, config) {
    const active = this.engine.active.get(s.id);
    const child = this.spawnWorker(resolve('research/.venv/bin/python'), ['-u', 'worker.py', resolve(config.jobDir, 'request.json')], { cwd: resolve('research'), env: { ...process.env, APORIA_RUN_DIR: config.jobDir, APORIA_TOPIC_FILE: config.topicFile, APORIA_DELTA: String(s.delta), OLLAMA_URL: this.provider.url, APORIA_EMBED_BACKEND: 'ollama', ENABLE_CLI_PROVIDERS: '0', CRUX_LAB_TRACING: '0', PYTHONUNBUFFERED: '1' }, stdio: ['pipe', 'pipe', 'pipe'] });
    this.running.set(s.id, child);
    let resolveFinished;
    this.finished.set(s.id, new Promise(resolve_ => { resolveFinished = resolve_; }));
    const cancel = () => { child.kill('SIGCONT'); child.kill('SIGTERM'); };
    active.controller.signal.addEventListener('abort', cancel, { once: true });
    let stderr = '', gotResult = false, cognitionTask = null;
    child.stderr.on('data', b => { stderr = (stderr + b.toString()).slice(-8000); });
    const lines = createInterface({ input: child.stdout });
    lines.on('line', line => {
      let ev; try { ev = JSON.parse(line); } catch { return; }
      const d = s.discovery;
      if (active.controller.signal.aborted) return;
      if (ev.type === 'cognition_request') {
        d.stage = 'cognition'; d.progress = .45; s.sourceContext = ev.grounding;
        s.protocol.discovery.sourceDigests = d.papers.filter(p => p.sourceDigest).map(p => ({ id: p.id, digest: p.sourceDigest }));
        this.engine.publish(s);
        const source = config.sourceSessionId && this.store.get(config.sourceSessionId);
        cognitionTask = source ? Promise.resolve().then(() => {
          s.profiles = structuredClone(source.profiles); s.cognitiveSourceId = source.id;
          s.cognitiveSource = { id: source.id, protocol: source.protocol, condition: source.condition, delta: source.delta,
            budget: source.budget, seed: source.seed, modelMetadata: source.modelMetadata,
            initialState: source.protocol ? this.store.getInitialState?.(source.protocol.initialStateDigest) : null };
        }) : this.engine.run(s.id, { continuation: true });
        cognitionTask.then(() => { if (!active.controller.signal.aborted && !child.stdin.destroyed) child.stdin.write(JSON.stringify({ profiles: s.profiles }) + '\n'); }).catch(e => { s.error = e.message; cancel(); });
        return;
      }
      if (ev.type === 'stage') { d.stage = ev.stage; d.detail = ev.detail; d.progress = Math.max(d.progress, Math.min(.96, stages.indexOf(ev.stage) / stages.length)); }
      if (ev.type === 'corpus') { d.corpus = ev.corpus; d.papers = ev.papers; }
      if (ev.type === 'models') d.models = ev.assignments;
      if (ev.type === 'targets') d.targets = ev.targets;
      if (ev.type === 'mapping') { d.claims = ev.claims; d.arguments = ev.arguments; }
      if (ev.type === 'index') { d.index = ev.index; d.extraction = ev.extraction; }
      if (ev.type === 'usage') d.usage = ev.usage;
      if (ev.type === 'model_call') d.activeRole = `${ev.role} · ${ev.model}`;
      if (ev.type === 'bridge') d.bridge = ev;
      if (ev.type === 'run') d.runs.push(ev.run);
      if (ev.type === 'brief') { const at = d.briefs.findIndex(b => b.id === ev.brief.id); if (at < 0) d.briefs.push(ev.brief); else d.briefs[at] = ev.brief; }
      if (ev.type === 'failure') d.failures.push(ev);
      if (ev.type === 'fatal') s.error = ev.error;
      if (ev.type === 'result') { Object.assign(d, ev.result); d.stage = 'complete'; d.progress = 1; gotResult = true; }
      d.events.push(ev.type === 'dialectic' ? { ...ev.event, time: ev.time } : { type: ev.type, stage: ev.stage, detail: ev.detail, role: ev.role, time: ev.time });
      s.visual = { ...s.visual, mode: ['debate', 'assessment'].includes(d.stage) ? 'conflict' : d.stage === 'complete' ? 'concentration' : 'exploration' };
      this.engine.publish(s);
    });
    try {
      const code = await new Promise((resolve_, reject) => { child.once('exit', resolve_); child.once('error', reject); });
      if (!active.controller.signal.aborted) {
        s.status = code === 0 && gotResult ? (s.discovery.failures.length || s.profiles.some(p => p.status === 'error') ? 'partial' : 'complete') : 'error';
        if (s.status === 'error' && !s.error) s.error = `Discovery worker stopped before completion (${code}). ${stderr.slice(-500)}`;
      }
    } catch (e) { if (!active.controller.signal.aborted) { s.status = 'error'; s.error = e.message; } }
    finally {
      lines.close(); active.controller.signal.removeEventListener('abort', cancel);
      const finalStatus = s.status;
      if (cognitionTask) {
        if (!gotResult && !active.controller.signal.aborted) active.controller.abort();
        await cognitionTask.catch(() => {});
        s.status = finalStatus;
      }
      this.running.delete(s.id); this.engine.active.delete(s.id); s.discovery.activeRole = null; this.engine.publish(s);
      resolveFinished(); this.finished.delete(s.id);
    }
    return s;
  }
  pause(id, paused) { const child = this.running.get(id); if (child) child.kill(paused ? 'SIGSTOP' : 'SIGCONT'); }
  async stopped(id) {
    const done = this.finished.get(id); if (!done) return;
    const timer = setTimeout(() => this.running.get(id)?.kill('SIGKILL'), 3000);
    try { await done; } finally { clearTimeout(timer); }
  }
}
