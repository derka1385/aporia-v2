import test from 'node:test';
import assert from 'node:assert/strict';
import { OllamaProvider, schemas } from '../server/provider.mjs';
import { policyFor } from '../server/policies.mjs';
const good = { hypothesis: 'Identity requires continuity of one psychological history.', premises: ['Memories connect past and present experiences.'], assumptions: ['Continuity remains unique.'], confidence: 0.6, stance: 'conditional' };
const args = { operation: 'hypothesis', question: 'Is identity psychological continuity?', context: {}, policy: policyFor('explorer', 0.8), model: 'test-local', seed: 31, profile: 'explorer', condition: 'architecture' };
test('invalid proposals get one recorded schema repair, without hidden model or sampling changes', async () => {
  const real = globalThis.fetch; const requests = [];
  globalThis.fetch = async (_url, options) => { requests.push(JSON.parse(options.body)); return Response.json({ message: { content: JSON.stringify(requests.length === 1 ? { ...good, confidence: 60 } : good) }, eval_count: 80, prompt_eval_count: 90, total_duration: 1000000 }); };
  try { const r = await new OllamaProvider().generate(args); assert.equal(r.usage.attempts, 2); assert.equal(r.usage.output, 160); assert.equal(r.usage.repaired, true); assert.equal(r.data.confidence, 0.6); assert.deepEqual(requests[0].options, requests[1].options); assert.equal(requests[0].model, requests[1].model); }
  finally { globalThis.fetch = real; }
});
test('two invalid outputs fail visibly, preserving consumed compute', async () => {
  const real = globalThis.fetch; globalThis.fetch = async () => Response.json({ message: { content: '{"invalid":true}' }, eval_count: 40 });
  try { await assert.rejects(new OllamaProvider().generate(args), e => e.usage.output === 80 && /two attempts/.test(e.message)); }
  finally { globalThis.fetch = real; }
});
test('schema accepts single atom formulas and requires substantive final positions', () => {
  assert.ok(schemas.formalize.safeParse({ assessment: 'Conditional on supplied premises.', premises: ['P'], conclusion: 'P', bindings: {P:'The person persists.'} }).success);
  assert.equal(schemas.conclude.safeParse({position:'no',stance:'no',remainingQuestion:'What remains uncertain?'}).success,false);
});
test('counterfactual task echoes are repaired before a graph mutation can use them', async () => {
  const real = globalThis.fetch; let calls = 0;
  globalThis.fetch = async () => Response.json({message:{content:JSON.stringify({scenario:++calls === 1 ? 'A concrete possible-world experiment challenging the selected assumption.' : 'Mira has two successors with identical memories, although the successors occupy separate bodies.',changedAssumption:'Continuity is no longer unique.',predictedConsequence:'Both successors meet the criterion.'})},eval_count:30});
  try { const r=await new OllamaProvider().generate({...args,operation:'counterfactual'}); assert.equal(calls,2); assert.equal(r.usage.output,60); assert.match(r.data.scenario,/Mira/); }
  finally { globalThis.fetch=real; }
});
