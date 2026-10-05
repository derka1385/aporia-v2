import { mkdirSync, writeFileSync } from 'node:fs';
import { Store } from '../server/store.mjs';
import { ResearchEngine } from '../server/engine.mjs';
import { OllamaProvider } from '../server/provider.mjs';
const store = new Store(process.env.APRORIA_VALIDATION_DB || 'data/validation.sqlite'); const provider = new OllamaProvider();
const questions = ['Is personal identity dependent on psychological continuity?', 'Can free will exist in a deterministic universe?', 'Can a person be morally responsible for an action they could not avoid?'];
let last = ''; const engine = new ResearchEngine({ store, provider, onUpdate: s => { const op = `${s.question.slice(0, 18)} / ${s.activeProfile} / ${s.activeOperation}`; if (op !== last) { console.log(op); last = op; } } });
const metadata = await provider.models();
const results = [];
for (const question of questions) {
  const s = engine.create({ question, delta: 0.8, model: process.env.APRORIA_TEST_MODEL || 'qwen2.5:3b', profiles: ['explorer', 'formalist'], budget: 8, seed: 31 });
  s.modelMetadata = metadata.filter(m => m.name === s.model);
  await engine.run(s.id); results.push(s); console.log(`Result: ${s.status} · ${s.profiles.map(p => `${p.id}: ${p.experiments.length} tests, ${p.stance}`).join('; ')}`);
}
mkdirSync('data/experiments', { recursive: true }); writeFileSync('data/experiments/live-validation.json', JSON.stringify(results, null, 2)); store.close();
if (results.some(s => s.status !== 'complete')) process.exitCode = 1;
