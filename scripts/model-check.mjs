import { mkdirSync, writeFileSync } from 'node:fs';
import { OllamaProvider } from '../server/provider.mjs';
import { policyFor } from '../server/policies.mjs';
import { similarity } from '../server/tools.mjs';
const provider = new OllamaProvider(); const available = await provider.models();
const models = ['qwen2.5:3b', 'qwen2.5:3b-instruct-q8_0'];
if (models.some(name => !available.some(m => m.name === name))) throw new Error('This check requires the local Qwen 3B Q4 and Q8 checkpoints. Nothing is downloaded automatically.');
const result = { created: new Date().toISOString(), question: 'Is personal identity dependent on psychological continuity?', seed: 31, condition: 'single-pass quantization feasibility check', policy: policyFor('formalist', 0), outputs: [], limitations: ['Only one question and seed.', 'Checkpoint equivalence beyond model family and tags is not independently verified.', 'This tests running variants, not cognitive architecture, pruning, useful diversity or argument quality.'] };
for (const model of models) {
  console.log(`Checking ${model}`);
  try { const response = await provider.generate({ operation: 'hypothesis', question: result.question, context: {}, policy: result.policy, model, seed: result.seed, profile: 'formalist', condition: 'baseline' }); result.outputs.push({ metadata: available.find(m => m.name === model), ...response }); }
  catch (e) { result.outputs.push({ model, error: e.message, usage: e.usage }); }
}
if (result.outputs.every(o => o.data)) result.lexicalHypothesisSimilarity = similarity(result.outputs[0].data.hypothesis, result.outputs[1].data.hypothesis);
mkdirSync('data/experiments', { recursive: true }); writeFileSync('data/experiments/model-level-check.json', JSON.stringify(result, null, 2));
console.log(JSON.stringify(result.outputs.map(o => ({ model: o.metadata?.name || o.model, stance: o.data?.stance, error: o.error, tokens: o.usage?.output }))));
if (result.outputs.some(o => o.error)) process.exitCode = 1;
