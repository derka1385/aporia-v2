import { randomUUID } from 'node:crypto';
import { policyFor, PROFILES, FUNCTIONS, POLICY_SOURCE, reflectionFor, personaFor } from './policies.mjs';
import { clamp, similarity, pathSimilarity, uniqueTexts, checkLogic, readingSearch } from './tools.mjs';
import { ENGINE_VERSION, CODE_DIGEST, digest, researchQuality, computeUsage } from './protocol.mjs';

function node(p, type, text, extra = {}) {
  const n = { id: `n${p.graph.nodes.length + 1}`, type, text, confidence: 0.45, importance: 0.5, status: 'open', novelty: 1, inspected: false, tested: false, intuition: 0.5, yield: 1, createdStep: p.history.length + 1, source: 'local-model-proposal', ...extra };
  n.novelty = 1 - Math.max(0, ...p.graph.nodes.map(x => similarity(x.text, text)));
  p.graph.nodes.push(n); return n;
}
function edge(p, from, to, type) { p.graph.edges.push({ from: from.id, to: to.id, type }); }
const root = p => p.graph.nodes.find(n => n.id === p.root);
const count = (p, op) => p.history.filter(h => h.operation === op).length;
export function metacognition(p) {
  const h = root(p); const objections = p.graph.nodes.filter(n => n.type === 'objection' && n.hypothesisId === p.root && ['open', 'surviving', 'unresolved'].includes(n.status));
  const dependencies = new Set(p.graph.edges.filter(e => e.from === p.root && e.type === 'depends_on').map(e => e.to));
  const assumptions = p.graph.nodes.filter(n => n.type === 'assumption' && dependencies.has(n.id) && n.status !== 'pruned');
  const conflict = clamp(objections.length / Math.max(2, p.experiments.length + 1));
  const weak = assumptions.filter(n => n.confidence < 0.5).length / Math.max(1, assumptions.length);
  p.state = { confidence: h?.confidence ?? 0.35, uncertainty: clamp((1 - (h?.confidence ?? 0.35)) * 0.6 + weak * 0.2 + conflict * 0.2), contradiction: conflict, novelty: p.graph.nodes.slice(-3).reduce((sum, n) => sum + n.novelty, 0) / Math.min(3, p.graph.nodes.length || 1), surprise: p.experiments.at(-1)?.verdict === 'fails' ? 0.8 : 0.1, curiosity: 0, attention: 0.4, evidenceStrength: p.graph.nodes.some(n => n.source === 'propositional-checker' && n.status === 'surviving' && p.graph.edges.some(e => e.from === n.id && e.to === p.root && e.type === 'supports')) ? 0.4 : 0.15, assumptionDependency: weak, unresolvedObjections: objections.length };
  for (const n of p.graph.nodes) {
    const downstream = p.graph.edges.filter(e => e.to === n.id && e.type === 'depends_on' || e.from === n.id && ['supports', 'refines'].includes(e.type)).length;
    n.curiosity = clamp((1 - n.confidence) * (0.4 + n.importance * 0.6) * (0.35 + n.novelty * 0.65) * (1 + downstream * 0.12 + conflict * 0.2) * (n.tested ? 0.35 : 1) * (n.yield ?? 1) * (0.7 + 0.6 * (n.intuition ?? 0.5)));
  }
  p.state.curiosity = Math.max(0.1, ...p.graph.nodes.filter(n => n.status === 'open').map(n => n.curiosity));
  return p.state;
}
// Stateless seeded draws keep scheduling and profile identity out of the random stream.
function draw(seed, step, salt) {
  let n = (seed ^ Math.imul(step + 1, 0x9e3779b1)) >>> 0;
  for (const c of salt) n = Math.imul(n ^ c.charCodeAt(0), 16777619) >>> 0;
  n ^= n >>> 16; n = Math.imul(n, 0x21f0aaad); n ^= n >>> 15;
  return (n >>> 0) / 4294967296;
}
function distribution(scores, temperature) {
  const entries = Object.entries(scores).filter(([, v]) => v > 0);
  const max = Math.max(0, ...entries.map(([, v]) => v));
  const values = entries.map(([k, v]) => [k, Math.exp((v - max) / Math.max(0.05, temperature))]);
  const sum = values.reduce((n, [, v]) => n + v, 0) || 1;
  return Object.fromEntries(values.map(([k, v]) => [k, v / sum]));
}
function sample(probabilities, value) {
  const entries = Object.entries(probabilities); let cumulative = 0;
  for (const [key, probability] of entries) { cumulative += probability; if (value < cumulative) return key; }
  return entries.at(-1)?.[0];
}
function selectBranch(p, candidates, salt) {
  if (!candidates.length) return root(p);
  const scores = Object.fromEntries(candidates.map(n => [n.id, Math.max(0.01, n.curiosity ?? 0.1)]));
  const max = Math.max(...Object.values(scores));
  const probabilities = distribution(scores, p.policy.exploration * Math.max(max, 0.05));
  return candidates.find(n => n.id === sample(probabilities, draw(p.seed, p.history.length, salt)));
}
const pendingTests = p => p.graph.nodes.filter(n => ['counterexample', 'objection'].includes(n.type) && !n.tested && n.status === 'open');
function availableAssumption(p, n) { return n.status !== 'pruned' && n.inspected && !n.tested && !p.graph.nodes.some(c => c.type === 'counterexample' && c.assumptionId === n.id && !c.tested); }
export function chooseOperation(p, budget) {
  if (!root(p)) return { operation: 'hypothesis', branch: null, scores: {}, probabilities: {}, signals: [], reason: 'No argument model exists. Form a provisional hypothesis from the common question.' };
  const s = metacognition(p), left = budget - p.history.length;
  const currentDependencies = new Set(p.graph.edges.filter(e => e.from === p.root && e.type === 'depends_on').map(e => e.to));
  const assumptions = p.graph.nodes.filter(n => n.type === 'assumption' && currentDependencies.has(n.id) && n.status !== 'pruned');
  const inspected = assumptions.some(n => n.inspected), uninspected = assumptions.some(n => !n.inspected);
  const pending = pendingTests(p), pendingCounterfactual = pending.find(n => n.assumptionId && n.hypothesisId === p.root);
  const coverage = inspected && p.experiments.some(e => e.kind === 'counterfactual' && e.hypothesis === p.root);
  const untested = assumptions.some(n => availableAssumption(p, n));
  const signals = [];
  const signal = (test, operation, text, strength) => { if (test) signals.push({ operation, text, strength }); };
  signal(root(p).confidence > 0.62 && s.evidenceStrength < 0.4, 'doubt', 'Confident but weakly supported', s.confidence - s.evidenceStrength);
  signal(!count(p, 'doubt'), 'doubt', 'No direct objection raised yet', 0.6);
  signal(untested, 'counterfactual', 'An exposed assumption has not been tested', 0.6);
  signal(pending.length, 'adjudicate', 'A challenge awaits a verdict', Math.min(1.3, pending.length * 0.5));
  signal(uninspected, 'introspect', 'Dependencies remain unexamined', 0.7);
  signal(!count(p, 'formalize'), 'formalize', 'The proposed inference has not been formally checked', 0.55);
  signal(root(p).status === 'rejected' || s.surprise > 0.5, 'revise', 'The hypothesis was challenged by a recorded test', 1.2);
  signal(p.graph.nodes.some(n => n.type === 'question' && n.status === 'open'), 'inquire', 'A sub-question is still open', 0.5);
  const scores = {
    memory: !count(p, 'memory') ? 0.4 * s.novelty * (1 - s.confidence) + 0.4 : 0,
    reason: !count(p, 'reason') ? 0.4 * s.uncertainty + 0.3 : 0,
    imagine: !pendingCounterfactual && count(p, 'imagine') < 2 ? 0.3 * (1 - s.novelty) + 0.2 * s.curiosity + 0.15 : 0,
    intuit: !count(p, 'intuit') ? 0.25 * (p.graph.nodes.length > 6) + 0.15 : 0,
    introspect: uninspected ? 0.3 * s.novelty : 0,
    doubt: count(p, 'doubt') < 2 ? 0.3 * s.confidence : 0,
    counterfactual: untested && !pendingCounterfactual ? 0.2 * s.confidence : 0,
    formalize: p.policy.tools.logic && !count(p, 'formalize') ? 0.1 : 0,
    inquire: count(p, 'inquire') < 3 ? 0.2 * s.uncertainty : 0,
    adjudicate: pending.length ? 0.3 * Math.min(2, pending.length) : 0,
    revise: count(p, 'revise') < 2 && (s.contradiction > 0 || root(p).status === 'rejected') ? 0.4 * s.surprise : 0,
    conclude: coverage && p.history.length >= p.policy.minSteps && s.confidence >= p.policy.stopConfidence && !pending.length && root(p).status !== 'rejected' ? 1.6 : 0
  };
  const eligible = Object.fromEntries(Object.entries(scores).map(([op, v]) => [op, v > 0]));
  if (!((p.policy.tools.memory && p.policy.memoryLimit) || (p.policy.tools.readings && p.policy.readingLimit))) eligible.memory = false;
  for (const sig of signals) if (eligible[sig.operation]) scores[sig.operation] += sig.strength;
  const mean = FUNCTIONS.reduce((n, op) => n + (p.learned[op] ?? 0.1), 0) / FUNCTIONS.length;
  for (const op of FUNCTIONS) scores[op] = eligible[op] ? scores[op] * p.policy.weights[op] * clamp(1 + p.policy.learningRate * ((p.learned[op] ?? 0.1) - mean) / (mean + 0.05), 0.4, 2.2) / (1 + count(p, op) * 0.3) : 0;
  const probabilities = distribution(scores, p.policy.controllerTemperature);
  let forced;
  // A fixed user budget reserves a complete test and honest provisional conclusion.
  if (left <= 4 && !coverage) forced = !inspected ? 'introspect' : pendingCounterfactual ? 'adjudicate' : 'counterfactual';
  if (left === 1) forced = 'conclude';
  const operation = forced || sample(probabilities, draw(p.seed, p.history.length, 'controller')) || 'conclude';
  let candidates;
  if (operation === 'introspect') candidates = assumptions.filter(n => !n.inspected);
  else if (operation === 'counterfactual') candidates = assumptions.filter(n => availableAssumption(p, n));
  else if (operation === 'adjudicate') candidates = pendingCounterfactual ? [pendingCounterfactual] : pending;
  else if (operation === 'inquire') candidates = p.graph.nodes.filter(n => n.type === 'question' && n.status === 'open');
  else if (operation === 'imagine') candidates = p.graph.nodes.filter(n => ['question', 'objection', 'assumption'].includes(n.type) && n.status === 'open');
  else candidates = [root(p)];
  const branch = selectBranch(p, candidates, operation);
  const reason = forced ? `Reserve remaining compute for ${operation === 'conclude' ? 'a provisional position' : 'a complete counterfactual test'}.` : `Seeded controller choice: ${operation}, probability ${(100 * (probabilities[operation] || 0)).toFixed(1)}%, weight ${p.policy.weights[operation].toFixed(2)}, exploration ${p.policy.exploration.toFixed(2)}.`;
  return { operation, branch: branch?.id || p.root, scores, probabilities, signals, reason };
}
function pruneAssumptions(p) {
  const assumptions = p.graph.nodes.filter(n => n.type === 'assumption' && n.status !== 'pruned').sort((a, b) => b.importance - a.importance || Number(b.inspected) - Number(a.inspected));
  for (const n of assumptions.slice(p.policy.maxAssumptions)) { n.status = 'pruned'; n.pruneReason = 'Policy assumption cap; retained in the audit graph, excluded from routing.'; }
}
function addAssumption(p, text, hypothesis, extra = {}) {
  const existing = p.graph.nodes.find(n => n.type === 'assumption' && n.status !== 'pruned' && similarity(n.text, text) >= 0.88);
  const n = existing || node(p, 'assumption', text, extra);
  if (!p.graph.edges.some(e => e.from === hypothesis.id && e.to === n.id && e.type === 'depends_on')) edge(p, hypothesis, n, 'depends_on');
  return n;
}
function contextFor(p, decision) {
  const selected = p.graph.nodes.find(n => n.id === decision.branch);
  const compact = n => n ? { id: n.id, type: n.type, text: n.text.slice(0, 600), status: n.status, confidence: n.confidence, assumptionId: n.assumptionId, hypothesisId: n.hypothesisId, prediction: n.prediction?.slice(0, 350), source: n.source, inspected: n.inspected, importance: n.importance } : null;
  const candidates = p.graph.nodes.filter(n => n.status !== 'pruned').sort((a, b) => (a.id === selected?.id ? -1 : b.id === selected?.id ? 1 : b.curiosity - a.curiosity)).slice(0, p.policy.visibleNodes).map(compact);
  const visible = []; let chars = 0; const cap = Math.max(1200, (p.policy.contextTokens - 1800) * 2);
  for (const n of candidates) { const length = JSON.stringify(n).length; if (chars + length > cap) break; visible.push(n); chars += length; }
  return { reflection: reflectionFor(p.policy, decision.operation), initialHypothesis: p.graph.nodes.find(n => n.type === 'hypothesis')?.text, currentHypothesis: root(p)?.text, targetHypothesis: p.graph.nodes.find(n => n.id === selected?.hypothesisId)?.text || root(p)?.text, selectedBranch: compact(selected), nodes: visible, edges: p.graph.edges.filter(e => visible.some(n => n.id === e.from) && visible.some(n => n.id === e.to)), priorExperiments: p.experiments.slice(-2).map(e => ({ scenario: e.scenario.slice(0, 350), verdict: e.verdict, result: e.result.slice(0, 350), source: e.source })), state: p.state, contextLimit: { visibleNodes: visible.length, requestedNodes: p.policy.visibleNodes, nodeCharacterCap: cap } };
}
export function computeMetrics(profiles) {
  const valid = profiles.filter(p => p.graph.nodes.length > 0 && p.status === 'complete' && p.position);
  const pairs = [];
  for (let i = 0; i < valid.length; i++) for (let j = i + 1; j < valid.length; j++) {
    const a = valid[i], b = valid[j];
    const text = p => p.graph.nodes.filter(n => ['hypothesis', 'objection'].includes(n.type)).map(n => n.text).join(' ');
    const branches = p => p.graph.nodes.filter(n => ['assumption', 'counterexample', 'hypothesis'].includes(n.type)).map(n => n.text);
    const ba = branches(a), bb = branches(b);
    const common = (ba.filter(t => bb.some(u => similarity(t, u) >= 0.8)).length + bb.filter(t => ba.some(u => similarity(t, u) >= 0.8)).length) / 2;
    pairs.push({ a: a.id, b: b.id, path: pathSimilarity(a.history.map(h => h.operation), b.history.map(h => h.operation)), argument: similarity(text(a), text(b)), branchDiversity: 1 - common / (Math.max(ba.length, bb.length) || 1), conclusion: a.position && b.position ? similarity(a.position, b.position) : null, disagreement: a.stance === 'undecided' || b.stance === 'undecided' ? null : a.stance !== b.stance ? 1 : 0 });
  }
  const mean = k => { const xs = pairs.map(p => p[k]).filter(n => n !== null); return xs.length ? xs.reduce((s, n) => s + n, 0) / xs.length : null; };
  const all = valid.flatMap(p => p.graph.nodes);
  return { pairs, profilesCompared: valid.length, pathSimilarity: mean('path'), argumentDiversity: pairs.length ? 1 - mean('argument') : null, branchDiversity: mean('branchDiversity'), conclusionSimilarity: mean('conclusion'), disagreementRate: mean('disagreement'), uniqueHypotheses: uniqueTexts(all.filter(n => n.type === 'hypothesis').map(n => n.text)).length, uniqueAssumptions: uniqueTexts(all.filter(n => n.type === 'assumption').map(n => n.text)).length, uniqueObjections: uniqueTexts(all.filter(n => n.type === 'objection').map(n => n.text)).length, survivingHypotheses: all.filter(n => n.type === 'hypothesis' && n.status === 'surviving').length, rejectedHypotheses: all.filter(n => n.type === 'hypothesis' && n.status === 'rejected').length, contradictionResolutionRate: all.some(n => n.type === 'objection') ? all.filter(n => n.type === 'objection' && n.status === 'resolved').length / all.filter(n => n.type === 'objection').length : null, novelty: all.length ? all.reduce((s, n) => s + n.novelty, 0) / all.length : 0, tokens: profiles.reduce((sum, p) => sum + p.history.reduce((s, h) => s + (h.usage?.output || 0), 0), 0), limitation: 'Argument/conclusion scores use token-vector similarity; branching uses lexical deduplication. Stance categories and confidence are provisional, not independent scientific validation.' };
}
export class ResearchEngine {
  constructor({ store, provider, onUpdate = () => {} }) { this.store = store; this.provider = provider; this.onUpdate = onUpdate; this.active = new Map(); }
  create({ question, delta = 0.6, condition = 'architecture', model = 'qwen2.5:3b', models = {}, budget = 10, seed = 31, profiles = PROFILES, memoryMode = 'fresh' }) {
    const memories = memoryMode === 'prior' ? this.store.memorySnapshot() : []; const rewards = memoryMode === 'prior' ? this.store.rewardSnapshot() : [];
    const s = { id: randomUUID(), created: new Date().toISOString(), question, delta, condition, model, budget, seed, engineVersion: 'aporia-reflection-v2', policySource: POLICY_SOURCE, policyAdaptations: ['Equal user-selected hard step budget; no surprise budget expansion.', 'Local curated bibliography pointers only; no corpus retrieval, calculator or first-order theorem prover.', 'Common fixed seed and request reuse for the Δ=0 control.'], status: 'running', error: null, activeProfile: null, activeOperation: null, memoryCount: memories.length, progress: 0, profiles: profiles.map(id => ({ id, seed, model: condition === 'model' && delta >= 0.15 ? models[id] || model : model, policy: policyFor(id, delta, condition), graph: { nodes: [], edges: [] }, root: null, experiments: [], history: [], state: {}, learned: Object.fromEntries(FUNCTIONS.map(op => [op, rewards.find(r => r.operation === op)?.gain || 0.1])), stance: 'undecided', position: '', nextQuestion: '', status: 'running', memoryHits: [], readings: [] })), metrics: computeMetrics([]), visual: { mode: 'idle', curiosity: 0.2, uncertainty: 0.2, contradiction: 0, attention: 0.2, confidence: 0.4, surprise: 0 } };
    s.engineVersion = ENGINE_VERSION;
    const initial = { memories, rewards }; const initialStateDigest = digest(initial);
    this.store.saveInitialState(initialStateDigest, initial);
    s.protocol = { version: 1, memoryMode, initialStateDigest, codeDigest: CODE_DIGEST, runtime: process.version, initialMemoryCount: memories.length, initialRewardCount: rewards.length, comparisonUnit: 'One completed profile position; failed and incomplete profiles remain in the denominator.', computeBoundary: 'Equal operation caps do not imply equal token budgets. Token usage and cache reuse are reported separately.' };
    this.active.set(s.id, { session: s, memories, controller: new AbortController(), paused: false, cache: new Map() }); this.publish(s); return s;
  }
  publish(s) { for (const p of s.profiles) p.quality = researchQuality(p); s.usage = computeUsage(s.profiles); s.metrics = { ...computeMetrics(s.profiles), ...(s.semanticMetrics || {}), totalProfiles: s.profiles.length, failedProfiles: s.profiles.filter(p => p.status === 'error').length, incompleteProfiles: s.profiles.filter(p => p.status !== 'complete' && p.status !== 'error').length }; s.progress = s.profiles.reduce((sum, p) => sum + (p.status === 'running' ? p.history.length / s.budget : 1), 0) / s.profiles.length; this.store.save(s); this.onUpdate(s); }
  pause(id, value) { const a = this.active.get(id); if (!a) return false; a.paused = value; a.session.status = value ? 'paused' : 'running'; this.publish(a.session); return true; }
  stop(id) { const a = this.active.get(id); if (!a) return false; a.session.status = 'cancelled'; a.controller.abort(); for (const p of a.session.profiles) if (p.status === 'running') p.status = 'cancelled'; this.publish(a.session); return true; }
  async generate(a, p, decision) {
    const args = { operation: decision.operation, question: a.session.question, context: { ...contextFor(p, decision), ...(a.session.sourceContext ? { publishedArgument: a.session.sourceContext } : {}) }, policy: p.policy, model: p.model, seed: a.session.seed, profile: p.id, condition: a.session.condition, delta: a.session.delta, signal: a.controller.signal };
    const key = JSON.stringify({ ...args, profile: a.session.condition === 'prompt' && personaFor(p.id, a.session.delta) ? p.id : '', signal: null });
    if (a.cache.has(key)) return { ...structuredClone(a.cache.get(key)), usage: { ...a.cache.get(key).usage, cached: true, output: 0, input: 0, durationMs: 0 } };
    const result = await this.provider.generate(args); a.cache.set(key, structuredClone(result)); return result;
  }
  async step(a, p) {
    const s = a.session, d = chooseOperation(p, s.budget), before = { ...p.state }, nBefore = p.graph.nodes.length;
    s.activeProfile = p.id; s.activeOperation = d.operation;
    p.state.attention = clamp(0.4 + (d.probabilities[d.operation] || 0.6) * 0.4);
    const modes = { hypothesis: 'exploration', memory: 'exploration', introspect: 'concentration', counterfactual: 'exploration', doubt: 'conflict', adjudicate: 'conflict', reason: 'concentration', formalize: 'concentration', imagine: 'exploration', intuit: 'exploration', inquire: 'exploration', revise: 'concentration', conclude: 'insight' };
    s.visual = { ...p.state, mode: modes[d.operation] }; this.publish(s);
    let result, detail = '', tool = null;
    const selected = p.graph.nodes.find(n => n.id === d.branch), h = root(p);
    const reflection = reflectionFor(p.policy, d.operation);
    if (d.operation === 'memory') {
      const snapshot = p.policy.memoryScope === 'shared' ? a.memories : a.memories.filter(m => m.profile === p.id);
      const hits = p.policy.tools.memory ? this.store.retrieve(snapshot, `${s.question} ${selected?.text || ''}`, p.policy.memoryLimit) : [];
      p.memoryHits = hits; p.readings = p.policy.tools.readings ? readingSearch(s.question, p.policy.readingLimit, p.policy.readingSpread) : [];
      for (const m of hits) {
        const openObjection = m.type === 'objection' && !['resolved', 'rejected'].includes(m.status);
        const n = node(p, openObjection ? 'objection' : 'concept', m.text, { source: 'persistent-memory', memorySession: m.session_id, confidence: m.confidence, status: openObjection ? 'open' : 'retrieved', importance: m.utility, hypothesisId: p.root });
        edge(p, n, h, openObjection ? 'attacks' : 'analogous_to');
      }
      const failures = hits.filter(m => m.type === 'objection' && !['resolved', 'rejected'].includes(m.status) || m.type === 'hypothesis' && m.status === 'rejected').length;
      h.confidence = clamp(h.confidence - Math.min(0.12, failures * 0.035));
      detail = `${hits.length} prior memories (${p.policy.memoryScope} scope); ${p.readings.length} bibliography pointers. ${failures ? 'Past counterevidence reduced confidence.' : 'No prior counterevidence applied.'}`;
      tool = { tool: 'local-memory-and-reading-index', retrieved: hits.map(m => ({ text: m.text, sourceSession: m.session_id, score: m.similarity })), readings: p.readings, limitation: 'Token similarity. Bibliography pointers are not evidence or live retrieval.' };
    } else {
      result = await this.generate(a, p, d); const data = result.data;
      if (d.operation === 'hypothesis') {
        const hn = node(p, 'hypothesis', data.hypothesis, { confidence: clamp(data.confidence, 0.2, 0.7), stance: data.stance }); p.root = hn.id; p.stance = data.stance;
        for (const text of data.premises) { const n = node(p, 'premise', text, { confidence: 0.5 }); edge(p, n, hn, 'supports'); }
        for (const text of data.assumptions) addAssumption(p, text, hn);
        detail = data.hypothesis;
        if (s.condition === 'baseline') { p.position = data.hypothesis; p.nextQuestion = 'Which assumptions would survive a counterfactual test?'; p.status = 'complete'; }
      } else if (d.operation === 'introspect') {
        if (selected.type === 'assumption') { selected.inspected = true; selected.importance = clamp(selected.importance + 0.2); selected.confidence = clamp(selected.confidence - 0.06); }
        for (const a of data.assumptions) addAssumption(p, a.text, h, { inspected: true, importance: a.importance, confidence: a.confidence });
        h.confidence = clamp(h.confidence - 0.035);
        detail = `Inspected ${selected.text} Exposed ${data.assumptions.length} proposed dependencies; unsupported confidence decreased.`;
      } else if (d.operation === 'counterfactual') {
        if (selected.type !== 'assumption') throw new Error('No exposed assumption available for a counterfactual.');
        const parent = p.graph.edges.find(e => e.from === p.root && e.to === selected.id && e.type === 'depends_on');
        const n = node(p, 'counterexample', data.scenario, { changedAssumption: data.changedAssumption, prediction: data.predictedConsequence, assumptionId: selected.id, hypothesisId: parent?.from || p.root, importance: selected.importance });
        edge(p, n, selected, 'attacks'); detail = `${data.scenario} Prediction: ${data.predictedConsequence}`;
      } else if (d.operation === 'doubt') {
        for (const o of data.objections.slice(0, p.policy.objectionLimit)) {
          if (p.graph.nodes.some(n => n.type === 'objection' && n.hypothesisId === h.id && similarity(n.text, o.text) >= 0.88)) continue;
          const n = node(p, 'objection', o.text, { confidence: o.strength, hypothesisId: h.id }); edge(p, n, h, 'attacks');
        }
        detail = `Requested up to ${p.policy.objectionLimit} objections; ${p.graph.nodes.length - nBefore} distinct challenges recorded. Their outcomes remain untested.`;
      } else if (d.operation === 'adjudicate') {
        if (!selected || !pendingTests(p).includes(selected)) throw new Error('No pending challenge available for adjudication.');
        selected.tested = true; selected.status = data.verdict === 'fails' ? 'surviving' : data.verdict === 'survives' ? 'resolved' : 'unresolved';
        const assumption = p.graph.nodes.find(n => n.id === selected.assumptionId); if (assumption) assumption.tested = true;
        const tested = p.graph.nodes.find(n => n.id === selected.hypothesisId) || h;
        const pressure = clamp(data.damage * p.policy.adversarialIntensity);
        tested.confidence = clamp(tested.confidence + (data.verdict === 'fails' ? -0.4 * pressure : data.verdict === 'survives' ? 0.05 : -0.04));
        if (data.verdict === 'fails') tested.status = tested.confidence < p.policy.rejectionThreshold ? 'rejected' : 'challenged';
        else if (data.verdict === 'survives' && tested.status !== 'rejected') tested.status = 'surviving';
        const response = node(p, 'premise', data.reason, { source: 'local-model-judgment', confidence: 0.4, status: data.verdict === 'survives' ? 'supported' : 'open' }); edge(p, response, selected, 'responds_to');
        p.experiments.push({ id: `e${p.experiments.length + 1}`, kind: selected.assumptionId ? 'counterfactual' : 'objection', hypothesis: tested.id, counterfactual: selected.id, assumption: selected.assumptionId, scenario: selected.text, prediction: selected.prediction || 'The objection may undermine this hypothesis.', verdict: data.verdict, result: data.reason, damage: pressure, source: 'local-model-judgment', confidenceAfter: tested.confidence, limitation: 'A provisional model judgment, not an empirical or independent verification.' });
        detail = `${data.verdict}: ${data.reason}`;
      } else if (d.operation === 'reason') {
        if (data.verdict === 'valid' && data.confidence >= p.policy.acceptanceThreshold) { selected.confidence = clamp(selected.confidence + Math.max(0, data.confidence - selected.confidence) * 0.5); selected.status = 'model-supported'; }
        else selected.confidence = clamp(selected.confidence - (data.verdict === 'invalid' ? 0.15 : 0.08));
        if (data.missingPremise) addAssumption(p, data.missingPremise, h);
        detail = `${data.verdict} at model confidence ${data.confidence.toFixed(2)} (acceptance threshold ${p.policy.acceptanceThreshold.toFixed(2)}): ${data.assessment}`;
        tool = { tool: 'model-reasoning-assessment', verdict: data.verdict, accepted: data.verdict === 'valid' && data.confidence >= p.policy.acceptanceThreshold, limitation: 'This is a language-model assessment, not a formal proof.' };
      } else if (d.operation === 'formalize') {
        try { tool = checkLogic(data); } catch (e) { tool = { tool: 'propositional-checker', error: e.message, valid: null, limitation: 'Invalid model formalization; no verification credit.' }; }
        tool.circular = data.premises.some(premise => premise.replace(/\s/g, '') === data.conclusion.replace(/\s/g, ''));
        const supported = tool.valid === true && tool.consistent && !tool.circular;
        const evidence = node(p, 'evidence', data.assessment, { source: 'propositional-checker', status: supported ? 'surviving' : tool.valid === false ? 'countermodel' : 'invalid', formalization: { premises: data.premises, conclusion: data.conclusion, bindings: data.bindings }, toolResult: tool, confidence: supported ? 0.6 : 0.3 });
        edge(p, evidence, h, supported ? 'supports' : tool.valid === false || tool.consistent === false ? 'attacks' : 'derived_from');
        if (tool.valid === false || tool.consistent === false) h.confidence = clamp(h.confidence - 0.1); else if (supported) h.confidence = clamp(h.confidence + 0.025);
        detail = tool.error || `${!tool.consistent ? 'Inconsistent premises' : tool.valid ? 'Entailment holds' : 'Countermodel found'} within the proposed Boolean formalization. ${data.assessment}`;
      } else if (d.operation === 'imagine') {
        for (const item of data.items.slice(0, p.policy.branchLimit)) {
          const hn = node(p, 'hypothesis', item.hypothesis, { confidence: 0.4, stance: item.stance }); edge(p, hn, h, 'refines'); addAssumption(p, item.assumption, hn);
        }
        detail = `${Math.min(data.items.length, p.policy.branchLimit)} alternative hypotheses proposed; none is verified.`;
      } else if (d.operation === 'intuit') {
        const visible = new Set(contextFor(p, d).nodes.map(n => n.id));
        for (const rating of data.ratings) if (visible.has(rating.id)) p.graph.nodes.find(n => n.id === rating.id).intuition = rating.value;
        const n = node(p, 'concept', data.hunch, { confidence: 0.3, intuition: 0.9, source: 'local-model-hunch' }); edge(p, n, h, 'refines'); detail = data.hunch;
      } else if (d.operation === 'inquire') {
        if (selected.type === 'question') {
          selected.status = 'investigated'; selected.tested = true;
          const n = node(p, data.effect === 'undermines' ? 'objection' : 'premise', data.answer, { confidence: data.confidence, hypothesisId: h.id, source: 'local-model-subquestion', status: data.effect === 'unknown' ? 'unresolved' : 'open' });
          edge(p, n, h, data.effect === 'undermines' ? 'attacks' : data.effect === 'supports' ? 'supports' : 'refines'); detail = `${data.answer} ${data.why}`;
        } else { const q = node(p, 'question', data.question, { importance: 0.8, intuition: 0.8 }); edge(p, q, h, 'derived_from'); detail = `${data.question} ${data.why}`; }
      } else if (d.operation === 'revise') {
        const rejected = p.graph.nodes.filter(n => n.type === 'hypothesis' && n.status === 'rejected');
        const resemblance = Math.max(0, ...rejected.map(n => similarity(n.text, data.hypothesis)));
        const hn = node(p, 'hypothesis', data.hypothesis, { confidence: clamp(0.5 - Math.max(0, resemblance - 0.7) * 0.6, 0.2, 0.5), stance: data.stance });
        edge(p, hn, h, data.change === 'major' ? 'derived_from' : 'refines');
        if (h.status !== 'rejected') h.status = 'superseded'; p.root = hn.id; p.stance = data.stance;
        for (const text of data.assumptions) addAssumption(p, text, hn);
        detail = `${data.change} revision: ${data.hypothesis} New confidence remains provisional.`;
      } else if (d.operation === 'conclude') {
        p.position = data.position; p.stance = data.stance; p.nextQuestion = data.remainingQuestion;
        const q = node(p, 'question', data.remainingQuestion, { importance: 0.75 }); edge(p, q, h, 'derived_from'); detail = data.position;
      }
    }
    pruneAssumptions(p); metacognition(p);
    const change = Math.abs((before.confidence ?? 0.35) - p.state.confidence), added = p.graph.nodes.slice(nBefore);
    const novelty = added.reduce((sum, n) => sum + n.novelty, 0) / (added.length || 1);
    const gain = clamp(change + Math.abs((before.uncertainty ?? p.state.uncertainty) - p.state.uncertainty) * 0.5 + Math.min(3, added.length) * 0.05 + (d.operation === 'adjudicate' ? 0.1 : 0) + (tool?.countermodel ? 0.1 : 0));
    const old = p.learned[d.operation] ?? 0.1; p.learned[d.operation] = old * 0.7 + gain * 0.3;
    if (selected && gain < 0.03) selected.yield = (selected.yield ?? 1) * 0.6;
    p.history.push({ step: p.history.length + 1, operation: d.operation, branch: d.branch, reason: d.reason, scores: d.scores, probabilities: d.probabilities, signals: d.signals, reflection, detail, tool, before, after: { ...p.state }, informationGain: gain, novelty, utilityBefore: old, utilityAfter: p.learned[d.operation], usage: result?.usage || { input: 0, output: 0, durationMs: 0, cached: false }, time: new Date().toISOString() });
    this.store.reward(s.id, p.id, d.operation, gain);
    if (d.operation === 'conclude' || p.history.length >= s.budget) { p.status = 'complete'; p.stopReason = p.history.length >= s.budget ? 'Hard compute budget reached; conclusion remains provisional.' : 'Confidence threshold reached after a completed test; conclusion remains provisional.'; }
    s.visual = { ...p.state, mode: root(p)?.status === 'rejected' ? 'collapse' : d.operation === 'adjudicate' && p.experiments.at(-1)?.verdict === 'fails' ? 'conflict' : d.operation === 'conclude' ? root(p)?.status === 'surviving' && p.state.confidence >= p.policy.stopConfidence ? 'insight' : 'concentration' : s.visual.mode };
    this.store.remember(s, p); this.publish(s);
  }
  async run(id, { continuation = false } = {}) {
    const a = this.active.get(id); if (!a) throw new Error('Session not active.'); const s = a.session;
    try {
      while (s.profiles.some(p => p.status === 'running') && !a.controller.signal.aborted) {
        if (a.paused) { await new Promise(r => setTimeout(r, 250)); continue; }
        for (const p of s.profiles) {
          if (p.status !== 'running' || a.paused || a.controller.signal.aborted) continue;
          try { await this.step(a, p); }
          catch (e) { if (a.controller.signal.aborted) break; p.status = 'error'; p.error = e.message; p.history.push({ step: p.history.length + 1, operation: s.activeOperation, detail: e.message, error: true, usage: e.usage, after: { ...p.state }, time: new Date().toISOString() }); this.publish(s); }
        }
      }
      if (!a.controller.signal.aborted) {
        const valid = s.profiles.filter(p => p.status === 'complete' && p.position);
        if (valid.length > 1 && this.provider.embed) {
          s.activeProfile = null; s.activeOperation = 'similarity analysis'; this.publish(s);
          try {
            const texts = valid.flatMap(p => [p.graph.nodes.filter(n => ['hypothesis', 'objection'].includes(n.type)).map(n => n.text).join(' '), p.position]);
            const vectors = await this.provider.embed(texts, a.controller.signal);
            const cosine = (x, y) => x.reduce((sum, v, i) => sum + v * y[i], 0) / (Math.sqrt(x.reduce((sum, v) => sum + v * v, 0)) * Math.sqrt(y.reduce((sum, v) => sum + v * v, 0)) || 1);
            const pairs = [];
            for (let i = 0; i < valid.length; i++) for (let j = i + 1; j < valid.length; j++) pairs.push({ a: valid[i].id, b: valid[j].id, argument: cosine(vectors[i * 2], vectors[j * 2]), conclusion: cosine(vectors[i * 2 + 1], vectors[j * 2 + 1]) });
            s.semanticMetrics = { argumentDiversity: clamp(1 - pairs.reduce((sum, p) => sum + p.argument, 0) / pairs.length), conclusionSimilarity: clamp(pairs.reduce((sum, p) => sum + p.conclusion, 0) / pairs.length), semanticPairs: pairs, similarityBasis: 'nomic-embed-text cosine similarity', limitation: 'Argument/conclusion scores use local Nomic embeddings (up to 5,000 characters per text, with tokenizer truncation). Branching uses lexical deduplication. Embedding distance is not a judgment of philosophical merit. Stance and confidence remain provisional.' };
          } catch (e) { if (!a.controller.signal.aborted) s.metricWarning = e.message; }
        }
        s.status = a.controller.signal.aborted ? 'cancelled' : continuation ? 'running' : s.profiles.every(p => p.status === 'error') ? 'error' : s.profiles.some(p => p.status === 'error') ? 'partial' : 'complete';
      }
    } finally { s.activeOperation = null; s.activeProfile = null; this.publish(s); if (!continuation) this.active.delete(id); }
    return s;
  }
}
