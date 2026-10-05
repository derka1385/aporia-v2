import { existsSync, mkdirSync, readFileSync, writeFileSync, renameSync } from 'node:fs';
import { join } from 'node:path';
import { Store } from './store.mjs';
import { ResearchEngine } from './engine.mjs';
import { CODE_DIGEST, digest } from './protocol.mjs';

export const QUESTIONS = [
  'Is personal identity dependent on psychological continuity?',
  'Can free will exist in a deterministic universe?',
  'Can a person be morally responsible for an action they could not avoid?'
];
export function studyPlan({ suite = 'smoke', model = 'qwen2.5:3b', alternateModel, budget = 8 } = {}) {
  const profiles = ['explorer', 'formalist'];
  const conditions = suite === 'smoke' ? [{ condition: 'architecture', delta: 0.8 }] : [
    { condition: 'baseline', delta: 0 }, { condition: 'prompt', delta: 1 },
    { condition: 'architecture', delta: 0 }, { condition: 'architecture', delta: 1 },
    ...(alternateModel ? [{ condition: 'model', delta: 1, models: { explorer: model, formalist: alternateModel } }] : [])
  ];
  return (suite === 'smoke' ? QUESTIONS : [QUESTIONS[0]]).flatMap(question =>
    (suite === 'smoke' ? [31] : [31, 73]).flatMap(seed => conditions.map(config => ({ question, model, profiles, budget, seed, memoryMode: 'fresh', ...config }))));
}
const atomic = (path, data) => { writeFileSync(`${path}.tmp`, JSON.stringify(data, null, 2)); renameSync(`${path}.tmp`, path); };
export function studyReport(manifest, records) {
  const rows = records.map(s => ({ id: s.id, question: s.question, condition: s.condition, delta: s.delta, seed: s.seed, status: s.status,
    completed: s.profiles.filter(p => p.status === 'complete').length, total: s.profiles.length,
    metrics: s.metrics, usage: s.usage,
    profiles: s.profiles.map(p => ({ id: p.id, status: p.status, error: p.error, position: p.position, stance: p.stance, path: p.history.map(h => h.operation), quality: p.quality })) }));
  return { protocol: manifest, recordedCases: rows.length, plannedCases: manifest.cases.length, rows,
    limitations: ['Descriptive feasibility study; no blinded argument-quality assessment.', 'Two profiles and few questions/seeds cannot establish general superiority.', 'Equal operation caps are not equal compute; compare recorded tokens and inference duration.', 'Fresh memory controls prior-session carryover. Model-generated adjudications are not independent evidence.', 'A shared inference cache makes the Δ=0 control exactly reproducible within a run; it is not an independent sampling estimate.', 'No significance tests are reported for this small, dependent sample.'] };
}
export async function runStudy({ cases, provider, directory, maxCases = Infinity, onProgress = () => {} }) {
  mkdirSync(directory, { recursive: true });
  const models = await provider.models();
  const requested = new Set(cases.flatMap(c => [c.model, ...Object.values(c.models || {})]));
  for (const name of requested) if (!models.some(m => m.name === name)) throw new Error(`Model is not installed: ${name}`);
  const identity = { cases, codeDigest: CODE_DIGEST, models: models.filter(m => requested.has(m.name)).sort((a, b) => a.name.localeCompare(b.name)) };
  const fingerprint = digest(identity), path = join(directory, 'manifest.json');
  if (existsSync(path) && JSON.parse(readFileSync(path)).fingerprint !== fingerprint) throw new Error('Study inputs, code or model identity changed. Use a new output directory to preserve the previous study.');
  const manifest = existsSync(path) ? JSON.parse(readFileSync(path)) : { created: new Date().toISOString(), fingerprint, ...identity };
  atomic(path, manifest);
  const records = []; let executed = 0;
  for (let index = 0; index < cases.length; index++) {
    const file = join(directory, `case-${String(index + 1).padStart(3, '0')}.json`);
    let previous = existsSync(file) ? JSON.parse(readFileSync(file)) : null;
    if (previous && !['running', 'paused', 'interrupted', 'cancelled'].includes(previous.status)) { records.push(previous); continue; }
    if (executed >= maxCases) { if (previous) records.push(previous); continue; }
    if (previous) atomic(join(directory, `case-${index + 1}-interrupted-${Date.now()}.json`), previous);
    const store = new Store(':memory:');
    const engine = new ResearchEngine({ store, provider, onUpdate: s => { atomic(file, s); onProgress(s, index + 1, cases.length); } });
    const session = engine.create({ ...cases[index], memoryMode: 'fresh' });
    session.study = { fingerprint, case: index + 1 }; session.modelMetadata = identity.models;
    try { await engine.run(session.id); records.push(session); executed++; }
    finally { store.close(); }
    atomic(join(directory, 'report.json'), studyReport(manifest, records));
  }
  const report = studyReport(manifest, records); atomic(join(directory, 'report.json'), report); return report;
}
