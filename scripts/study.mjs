import { openSync, closeSync, existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { parseArgs } from 'node:util';
import { OllamaProvider } from '../server/provider.mjs';
import { runStudy, studyPlan } from '../server/study.mjs';
const { values } = parseArgs({ options: { run: { type: 'boolean', default: false }, suite: { type: 'string', default: 'smoke' }, out: { type: 'string' }, limit: { type: 'string', default: '3' }, model: { type: 'string', default: 'qwen2.5:3b' }, alternate: { type: 'string' }, budget: { type: 'string', default: '8' } } });
if (!['smoke', 'compare'].includes(values.suite)) throw new Error('Use --suite smoke or --suite compare.');
const limit = Number(values.limit); if (!Number.isInteger(limit) || limit < 1 || limit > 20) throw new Error('--limit must be 1–20 cases per invocation.');
const budget = Number(values.budget); if (!Number.isInteger(budget) || budget < 8 || budget > 24) throw new Error('--budget must be 8–24 operations per profile.');
const cases = studyPlan({ suite: values.suite, model: values.model, alternateModel: values.alternate, budget });
const directory = resolve(values.out || `data/studies/${values.suite}`);
if (!values.run) {
  console.log(JSON.stringify({ directory, plannedCases: cases.length, cases, next: 'Add --run to execute; completed and failed cases are preserved and skipped. --limit bounds this invocation.' }, null, 2));
} else {
  mkdirSync('data/studies', { recursive: true }); const lock = resolve('data/studies/runner.lock');
  if (existsSync(lock)) {
    const pid = Number(readFileSync(lock, 'utf8')); let alive = true;
    try { process.kill(pid, 0); } catch (e) { if (e.code === 'ESRCH') alive = false; }
    if (alive) throw new Error('Another study runner is active.'); unlinkSync(lock);
  }
  const fd = openSync(lock, 'wx'); writeFileSync(fd, String(process.pid)); closeSync(fd);
  let last = '';
  try {
    const report = await runStudy({ cases, provider: new OllamaProvider(), directory, maxCases: limit, onProgress: (s, i, total) => { const label = `${i}/${total} · ${s.activeProfile || s.status} · ${s.activeOperation || ''}`; if (label !== last) { console.log(label); last = label; } } });
    console.log(`Saved ${report.recordedCases}/${report.plannedCases} cases to ${join(directory, 'report.json')}`);
    if (report.rows.some(r => ['error', 'partial'].includes(r.status))) process.exitCode = 1;
  } finally { unlinkSync(lock); }
}
