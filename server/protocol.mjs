import { createHash } from 'node:crypto';
import { readFileSync, readdirSync } from 'node:fs';

export const ENGINE_VERSION = 'aporia-research-v3';
export const digest = value => createHash('sha256').update(typeof value === 'string' ? value : JSON.stringify(value)).digest('hex');
const files = ['engine.mjs', 'provider.mjs', 'policies.mjs', 'aporia-policies.json', 'tools.mjs', 'store.mjs', 'protocol.mjs', 'study.mjs', 'discovery.mjs', '../research/worker.py', '../research/discovery.py', '../research/local_provider.py', '../research/upstream.json', '../research/requirements.txt', '../research/crux_lab/lab/novelty.py', '../research/crux_lab/lab/debate.py', '../research/crux_lab/lab/run.py', '../research/crux_lab/graph/index.py', '../package-lock.json'];
const researchFiles = readdirSync(new URL('../research/crux_lab/', import.meta.url), { recursive: true }).filter(p => /\.(py|md)$/.test(p)).sort().map(p => `../research/crux_lab/${p}`);
export const CODE_DIGEST = digest([...files, '../research/requirements.lock.txt', ...researchFiles].map(file => [file, readFileSync(new URL(file, import.meta.url), 'utf8')]));

export function researchQuality(profile) {
  const nodes = profile.graph.nodes, edges = profile.graph.edges;
  const current = nodes.find(n => n.id === profile.root);
  const dependencies = new Set(edges.filter(e => e.from === profile.root && e.type === 'depends_on').map(e => e.to));
  const assumptions = nodes.filter(n => dependencies.has(n.id) && n.status !== 'pruned');
  const tests = profile.experiments.filter(e => e.hypothesis === profile.root);
  const formal = nodes.filter(n => n.source === 'propositional-checker');
  const checked = formal.filter(n => n.toolResult?.valid === true && n.toolResult?.consistent === true && !n.toolResult?.circular);
  const pending = nodes.filter(n => ['counterexample', 'objection'].includes(n.type) && n.hypothesisId === profile.root && !n.tested && n.status === 'open');
  const unresolved = nodes.filter(n => n.type === 'objection' && n.hypothesisId === profile.root && ['open', 'unresolved', 'surviving'].includes(n.status));
  const warnings = [];
  if (current && !tests.some(e => e.kind === 'counterfactual' || e.assumption)) warnings.push('The current hypothesis has no completed counterfactual test.');
  if (pending.length) warnings.push(`${pending.length} challenge(s) still await assessment.`);
  if (current?.status === 'rejected') warnings.push('The current hypothesis remains rejected.');
  if (formal.some(n => n.toolResult?.error || n.toolResult?.circular || n.toolResult?.consistent === false)) warnings.push('A formalization is invalid, circular or inconsistent; it cannot support a claim.');
  if (profile.status === 'error') warnings.push('This profile failed and is excluded from completed-position comparisons.');
  return {
    currentHypothesis: profile.root, assumptions: assumptions.length,
    testedAssumptions: assumptions.filter(n => tests.some(e => e.assumption === n.id)).length,
    currentHypothesisTests: tests.length, modelJudgments: profile.experiments.length,
    formalChecks: formal.length, validFormalizations: checked.length,
    currentFormalSupport: checked.filter(n => edges.some(e => e.from === n.id && e.to === profile.root && e.type === 'supports')).length,
    pendingChallenges: pending.length, unresolvedObjections: unresolved.length,
    openQuestions: nodes.filter(n => n.type === 'question' && n.status === 'open').map(n => ({ id: n.id, text: n.text })),
    warnings, evidenceBoundary: 'Model judgments are proposals. Formal validity concerns only the supplied formulas. No empirical study or source passage has been verified by this run.'
  };
}

export function computeUsage(profiles) {
  const records = profiles.flatMap(p => p.history);
  return {
    inputTokens: records.reduce((n, h) => n + (h.usage?.input || 0), 0),
    outputTokens: records.reduce((n, h) => n + (h.usage?.output || 0), 0),
    inferenceMs: records.reduce((n, h) => n + (h.usage?.durationMs || 0), 0),
    cachedRequests: records.filter(h => h.usage?.cached).length,
    repairedRequests: records.filter(h => h.usage?.repaired).length,
    failedOperations: records.filter(h => h.error).length,
    byFunction: records.reduce((out, h) => { const row = out[h.operation] ||= { calls: 0, input: 0, output: 0, durationMs: 0 }; row.calls++; row.input += h.usage?.input || 0; row.output += h.usage?.output || 0; row.durationMs += h.usage?.durationMs || 0; return out; }, {})
  };
}
