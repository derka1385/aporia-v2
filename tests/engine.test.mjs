import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Store } from '../server/store.mjs';
import { ResearchEngine, computeMetrics, chooseOperation } from '../server/engine.mjs';
import { policyFor, PROFILES, referencePolicyFor, reflectionFor } from '../server/policies.mjs';
import { checkLogic, similarity, pathSimilarity } from '../server/tools.mjs';
const fixture = {
  doubt: { objections: [{text:'A branching history makes numerical identity ambiguous.',strength:0.7},{text:'False memories undermine continuity.',strength:0.6},{text:'An interrupted history may preserve bodily identity.',strength:0.5},{text:'Shared memories need not imply numerical sameness.',strength:0.4}] },
  reason: {verdict:'unsupported',confidence:0.55,missingPremise:'Psychological histories cannot branch.',assessment:'Uniqueness is not independently established.'},
  introspect: {assumptions:[]},
  intuit: {ratings:[{id:'n2',value:0.9}],hunch:'Investigate whether continuity can branch.'},
  inquire: {question:'Can two successors preserve the same past?',answer:'A hypothetical fission case permits two successors.',effect:'undermines',confidence:0.5,why:'It tests uniqueness.'},
  revise: {hypothesis:'Psychological continuity is informative but identity also requires a non-branching condition.',assumptions:['Continuity remains unique.'],stance:'conditional',change:'minor'},
  hypothesis: { hypothesis: 'Personal identity requires a continuous unique psychological history.', premises: ['Memory links experiences over time.', 'Identity is transitive.'], assumptions: ['Psychological continuity is unique.', 'Memory accurately preserves prior experience.'], stance: 'conditional', confidence: 0.62 },
  counterfactual: { scenario: 'Two successors inherit the same psychological history.', changedAssumption: 'Continuity is no longer unique.', predictedConsequence: 'Both meet the criterion although they are distinct people.' },
  adjudicate: { damage: 0.7, verdict: 'fails', objection: 'A branching history makes numerical identity ambiguous.', reason: 'The uniqueness assumption is defeated by two equally continuous successors.' },
  formalize: { assessment: 'The formalization does not entail identity.', premises: ['P -> Q', 'Q'], conclusion: 'P', bindings: { P: 'The person persists', Q: 'Memory is preserved' } },
  imagine: { items: [{ hypothesis: 'Identity is grounded in continuity of an organism.', assumption: 'The organism remains numerically singular.', stance: 'no' }, { hypothesis: 'Identity depends on narrative coherence.', assumption: 'Narratives remain coherent.', stance: 'conditional' }] },
  conclude: { position: 'Psychological continuity alone is insufficient when continuity branches.', stance: 'conditional', remainingQuestion: 'Is a non-branching condition independently defensible?' }
};
function setup(provider) { const store = new Store(':memory:'); const calls = []; const engine = new ResearchEngine({ store, provider: provider || { generate: async args => { calls.push(args); return { data: structuredClone(fixture[args.operation]), usage: { input: 30, output: 40, durationMs: 2 } }; } } }); return { store, calls, engine }; }

test('paper grounding reaches cognitive calls and continuation keeps the shared run active', async () => {
  const { engine, store, calls } = setup();
  const s = engine.create({ question: 'Does psychological continuity suffice for identity?', budget: 8, profiles: ['skeptic'] });
  s.sourceContext = { paper: { id: 'fixture-paper' }, claims: [{ text: 'Continuity can branch.', quote: 'Continuity can branch.' }] };
  await engine.run(s.id, { continuation: true });
  assert.equal(s.status, 'running'); assert.equal(s.profiles[0].status, 'complete'); assert.ok(engine.active.has(s.id));
  assert.ok(calls.every(c => c.context.publishedArgument.paper.id === 'fixture-paper'));
  engine.stop(s.id); engine.active.delete(s.id); store.close();
});

test('Δ=0 yields identical actual policies for every profile; Δ changes numeric and tool policies', () => {
  for (const p of PROFILES) assert.deepEqual(policyFor(p, 0), policyFor('explorer', 0));
  assert.notEqual(policyFor('explorer', 1).weights.imagine, policyFor('formalist', 1).weights.imagine);
  assert.equal(policyFor('explorer', 1).tools.logic, false);
  assert.equal(policyFor('minimalist', 1).tools.readings, false);
  assert.deepEqual(policyFor('explorer', 1, 'prompt'), policyFor('formalist', 1, 'prompt'));
});
test('truth table proves valid implications and supplies countermodels; unsafe formulas and contradictions are visible', () => {
  assert.equal(checkLogic({ premises: ['P -> Q', 'P'], conclusion: 'Q' }).valid, true);
  const result = checkLogic({ premises: ['P -> Q', 'Q'], conclusion: 'P' });
  assert.equal(result.valid, false); assert.deepEqual(result.countermodel, { P: false, Q: true });
  assert.equal(checkLogic({ premises: ['P', '!P'], conclusion: 'Q' }).consistent, false);
  assert.throws(() => checkLogic({ premises: ['process.exit()'], conclusion: 'P' }));
  assert.throws(() => checkLogic({ premises: ['(P'], conclusion: 'P' }));
});
test('complete loop mutates graph, tests counterfactuals, learns utility and persists memory', async () => {
  const { store, engine, calls } = setup();
  const s = engine.create({ question: 'Is personal identity psychological continuity?', profiles: ['formalist'], budget: 10, delta: 0.8 }); await engine.run(s.id);
  const p = s.profiles[0]; assert.equal(s.status, 'complete'); assert.ok(p.graph.nodes.some(n => n.type === 'assumption' && n.inspected));
  assert.ok(p.experiments.length >= 1); assert.ok(p.position); assert.ok(p.history.some(h => h.operation === 'adjudicate'));
  assert.ok(p.history.some(h => h.utilityBefore !== h.utilityAfter)); assert.ok(p.history.at(-1).after.confidence < 0.62);
  assert.ok(store.stats().memories > 0); assert.equal(store.get(s.id).profiles[0].position, p.position);
  assert.ok(calls.every(c => c.question === s.question)); store.close();
});
test('same policies and seed have identical trajectories; no live cross-profile memory contamination', async () => {
  const { store, engine, calls } = setup(); const s = engine.create({ question: 'Is personal identity psychological continuity?', delta: 0, budget: 8 }); await engine.run(s.id);
  for (const p of s.profiles) { assert.deepEqual(p.graph, s.profiles[0].graph); assert.deepEqual(p.history.map(h => h.operation), s.profiles[0].history.map(h => h.operation)); assert.equal(p.memoryHits.length, 0); }
  assert.equal(s.metrics.pathSimilarity, 1); assert.ok(s.metrics.argumentDiversity < 1e-9); assert.equal(s.metrics.disagreementRate, 0);
  assert.ok(calls.length < s.profiles.reduce((n, p) => n + p.history.length, 0)); store.close();
});
test('high Δ changes operation paths even with the same proposals, without optimizing disagreement', async () => {
  const { store, engine } = setup(); const s = engine.create({ question: 'Is personal identity psychological continuity?', delta: 1, budget: 10 }); await engine.run(s.id);
  assert.ok(new Set(s.profiles.map(p => p.history.map(h => h.operation).join(','))).size > 1);
  assert.equal(s.metrics.disagreementRate, 0); assert.ok(s.profiles.every(p => p.experiments.length > 0)); store.close();
});
test('persisted objections influence a subsequent independent run and are retrieved only from prior sessions', async () => {
  const { store, engine } = setup(); const first = engine.create({ question: 'Is personal identity psychological continuity?', profiles: ['skeptic'], budget: 8 }); await engine.run(first.id);
  const second = engine.create({ question: 'Is personal identity psychological continuity?', profiles: ['synthesizer'], delta: 1, budget: 24, memoryMode: 'prior' }); await engine.run(second.id);
  const p = second.profiles[0]; assert.ok(p.memoryHits.length > 0); assert.ok(p.memoryHits.every(m => m.session_id === first.id));
  const memory = p.history.find(h => h.operation === 'memory'); assert.ok(memory.after.confidence < memory.before.confidence); store.close();
});
test('provider failures are logged without fabricated positions or completed success', async () => {
  const { store, engine } = setup({ generate: async () => { throw new Error('Malformed proposal'); } }); const s = engine.create({ question: 'Can free will exist with determinism?', profiles: ['skeptic'] }); await engine.run(s.id);
  assert.equal(s.status, 'error'); assert.equal(s.profiles[0].position, ''); assert.match(s.profiles[0].error, /Malformed/); assert.equal(s.metrics.profilesCompared, 0); store.close();
});
test('single-pass baseline performs one untested inference per profile', async () => {
  const { store, engine } = setup(); const s = engine.create({ question: 'Can free will exist with determinism?', condition: 'baseline', profiles: ['explorer', 'skeptic'] }); await engine.run(s.id);
  assert.ok(s.profiles.every(p => p.history.length === 1 && p.experiments.length === 0 && p.position)); store.close();
});
test('SQLite survives reopening and marks interrupted work honestly', () => {
  const dir = mkdtempSync(join(tmpdir(), 'aproria-test-')); const path = join(dir, 'memory.sqlite'); let store = new Store(path);
  store.save({ id: 'test-session', created: new Date().toISOString(), question: 'A saved question', status: 'running' }); store.close();
  store = new Store(path); assert.equal(store.get('test-session').status, 'interrupted'); assert.match(store.get('test-session').error, /restarted/); store.close(); rmSync(dir, { recursive: true });
});
test('similarity metrics use recorded paths, and missing/undecided comparisons are not counted as disagreement', () => {
  assert.equal(pathSimilarity(['memory', 'doubt'], ['memory', 'doubt']), 1); assert.equal(pathSimilarity(['memory'], ['doubt']), 0);
  assert.ok(similarity('unique continuous memory', 'continuous unique memory') > .99); assert.equal(computeMetrics([]).disagreementRate, null);
});
test('controller never generates a second pending counterfactual for the same assumption', async () => {
  const {store, engine} = setup(); const s=engine.create({question:'Is identity psychological continuity?',profiles:['explorer'],delta:1,budget:14}); const a=engine.active.get(s.id), p=s.profiles[0];
  while (!p.graph.nodes.some(n=>n.type==='counterexample'&&!n.tested) && p.history.length < 13) await engine.step(a,p);
  assert.ok(p.graph.nodes.some(n=>n.type==='counterexample'&&!n.tested));
  const next=chooseOperation(p,14); assert.notEqual(next.operation,'counterfactual'); engine.stop(s.id); store.close();
});
test('local semantic comparisons override lexical estimates only after successful embedding', async () => {
  const {store, engine} = setup({generate:async args=>({data:structuredClone(fixture[args.operation]),usage:{output:2}}),embed:async texts=>texts.map(()=>[1,0])});
  const s=engine.create({question:'Is identity psychological continuity?',profiles:['explorer','formalist'],budget:8}); await engine.run(s.id);
  assert.equal(s.metrics.argumentDiversity,0); assert.match(s.metrics.similarityBasis,/nomic/); assert.equal(s.metrics.conclusionSimilarity,1); store.close();
});

test('a revised hypothesis cannot inherit coverage from tests of its predecessor', async () => {
  const {store,engine}=setup(); const s=engine.create({question:'Does identity persist across a branching history?',profiles:['formalist'],budget:10}); await engine.run(s.id);
  const p=s.profiles[0]; assert.ok(p.experiments.length); p.root='revised';
  p.graph.nodes.push({id:'revised',type:'hypothesis',text:'A revised criterion requires bodily continuity.',confidence:.5,status:'open',importance:.5,novelty:1},{id:'new-assumption',type:'assumption',text:'The body remains singular.',confidence:.4,status:'open',importance:.7,novelty:1,inspected:true,tested:false});
  p.graph.edges.push({from:'revised',to:'new-assumption',type:'depends_on'}); p.history=p.history.slice(0,4);
  const next=chooseOperation(p,8); assert.equal(next.operation,'counterfactual'); assert.equal(next.branch,'new-assumption'); store.close();
});
test('fresh-memory control excludes both remembered beliefs and learned routing', async () => {
  const {store,engine}=setup(); const a=engine.create({question:'Is personal identity psychological continuity?',profiles:['skeptic'],budget:8}); await engine.run(a.id);
  const fresh=engine.create({question:a.question,profiles:['skeptic'],memoryMode:'fresh'});
  const prior=engine.create({question:a.question,profiles:['skeptic'],memoryMode:'prior'});
  assert.equal(fresh.memoryCount,0); assert.ok(prior.memoryCount>0); assert.notEqual(fresh.protocol.initialStateDigest,prior.protocol.initialStateDigest);
  assert.deepEqual(store.getInitialState(fresh.protocol.initialStateDigest),{memories:[],rewards:[]});
  assert.ok(store.getInitialState(prior.protocol.initialStateDigest).rewards.length); engine.stop(fresh.id); engine.stop(prior.id); store.close();
});
test('invalid and directly circular formalizations never create support or increase confidence', async () => {
  for(const premises of [['process.exit()'],['P']]) {
    const {store,engine}=setup({generate:async a=>({data:structuredClone(a.operation==='formalize'?{assessment:'A formalization requiring inspection.',premises,conclusion:'P',bindings:{P:'Identity persists.'}}:fixture[a.operation]),usage:{output:1}})});
    const s=engine.create({question:'Is personal identity psychological continuity?',profiles:['formalist'],budget:10});const a=engine.active.get(s.id),p=s.profiles[0]; await engine.step(a,p);
    p.policy.weights=Object.fromEntries(Object.keys(p.policy.weights).map(k=>[k,k==='formalize'?1:0])); const before=p.state.confidence; await engine.step(a,p);
    const evidence=p.graph.nodes.find(n=>n.type==='evidence');assert.ok(evidence);assert.equal(evidence.status,'invalid');assert.ok(!p.graph.edges.some(e=>e.from===evidence.id&&e.type==='supports'));assert.equal(p.state.confidence,before);engine.stop(s.id);store.close();
  }
});
test('a resolved remembered objection does not become counterevidence again', async () => {
  const {store,engine}=setup();store.db.prepare('INSERT INTO memories VALUES (?,?,?,?,?,?,?,?,?)').run('m','past','formalist','Is personal identity psychological continuity?','objection','Psychological continuity can branch.','resolved',.4,.8);
  const s=engine.create({question:'Is personal identity psychological continuity?',profiles:['formalist'],memoryMode:'prior',budget:10});const a=engine.active.get(s.id),p=s.profiles[0];await engine.step(a,p);
  p.policy.tools.memory=true;p.policy.memoryLimit=4;p.policy.memoryScope='shared';p.policy.weights=Object.fromEntries(Object.keys(p.policy.weights).map(k=>[k,k==='memory'?1:0])); const before=p.state.confidence;await engine.step(a,p);
  assert.equal(p.memoryHits.length,1);assert.equal(p.state.confidence,before);assert.ok(!p.graph.nodes.some(n=>n.source==='persistent-memory'&&n.type==='objection'));engine.stop(s.id);store.close();
});
test('failed and incomplete profiles do not enter completed-position comparisons', async () => {
  const {store,engine}=setup();const s=engine.create({question:'Is identity psychological continuity?',profiles:['explorer','formalist'],delta:0,budget:8});await engine.run(s.id);
  s.profiles[1].status='error';engine.publish(s);assert.equal(s.metrics.profilesCompared,1);assert.equal(s.metrics.totalProfiles,2);assert.equal(s.metrics.failedProfiles,1);assert.equal(s.metrics.pathSimilarity,null);assert.ok(s.usage.outputTokens>0);store.close();
});
