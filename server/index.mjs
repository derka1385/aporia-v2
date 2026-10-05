import express from 'express';
import { z } from 'zod';
import { Store } from './store.mjs';
import { OllamaProvider } from './provider.mjs';
import { ResearchEngine } from './engine.mjs';
import { PROFILES } from './policies.mjs';
import { DiscoveryManager } from './discovery.mjs';
import { readFileSync } from 'node:fs';
import { resolve, sep } from 'node:path';
const app = express(); app.use(express.json({ limit: '24kb' }));
// Block cross-site writes even though the service is loopback-only.
app.use((req, res, next) => { const origin = req.headers.origin; if (origin && !/^http:\/\/(localhost|127\.0\.0\.1):(5173|4317)$/.test(origin)) return res.status(403).json({ error: 'Only the localhost application may access this service.' }); next(); });
const store = new Store(); const provider = new OllamaProvider(); const subscribers = new Map();
const engine = new ResearchEngine({ store, provider, onUpdate: s => { for (const res of subscribers.get(s.id) || []) res.write(`data: ${JSON.stringify(s)}\n\n`); } });
const discovery = new DiscoveryManager({ engine, store, provider });
const schema = z.object({ memoryMode: z.enum(['fresh', 'prior']).default('fresh'), question: z.string().trim().min(12).max(1400), delta: z.number().min(0).max(1).default(0.6), budget: z.number().int().min(8).max(24).default(10), seed: z.number().int().min(0).max(999999).default(31), condition: z.enum(['baseline', 'prompt', 'architecture', 'model']).default('architecture'), model: z.string().max(120), models: z.record(z.string(), z.string().max(120)).default({}), profiles: z.array(z.enum(PROFILES)).min(1).max(5).refine(a => new Set(a).size === a.length, 'Profiles must be unique.').default(PROFILES) });
const discoverySchema = schema.extend({ workflow: z.enum(['reflection', 'discovery']).default('discovery'), targetCount: z.number().int().min(1).max(5).default(2), trialBudget: z.number().int().min(1).max(6).default(6), corpusLimit: z.number().int().min(20).max(200).default(60), fulltextLimit: z.number().int().min(3).max(50).default(16), sourceSessionId: z.string().uuid().optional() });
app.get('/api/health', async (_req, res) => { try { res.json({ online: true, discoveryReady: discovery.ready(), models: await provider.models(), memory: store.stats() }); } catch { res.json({ online: false, discoveryReady: discovery.ready(), models: [], memory: store.stats(), error: 'Ollama is unavailable. Run ollama serve, then refresh connection.' }); } });
app.get('/api/sessions', (_req, res) => res.json(store.list()));
app.get('/api/sessions/:id', (req, res) => { const s = store.get(req.params.id); if (!s) return res.status(404).json({ error: 'Research record not found.' }); res.json(s); });
app.post('/api/sessions', async (req, res) => {
  const parsed = discoverySchema.safeParse(req.body); if (!parsed.success) return res.status(400).json({ error: parsed.error.issues.map(i => `${i.path.join('.')}: ${i.message}`).join('; ') });
  if (engine.active.size) {
    const current = engine.active.values().next().value.session;
    return res.status(409).json({ error: `A local experiment is ${current.status === 'paused' ? 'paused' : 'already running'}. Open it to resume or stop before starting another.`, activeSessionId: current.id });
  }
  try {
    const available = await provider.models(); const names = available.map(m => m.name);
    // A second request can enter while model discovery is awaiting Ollama.
    if (engine.active.size) { const current = engine.active.values().next().value.session; return res.status(409).json({ error: 'A local experiment is already running. Open it to resume or stop before starting another.', activeSessionId: current.id }); }
    const requested = [parsed.data.model, ...(parsed.data.condition === 'model' ? Object.values(parsed.data.models) : [])];
    if (requested.some(n => !names.includes(n))) return res.status(400).json({ error: 'A selected model is not installed locally. Choose an available model.' });
    if (parsed.data.workflow === 'discovery' && !discovery.ready()) return res.status(503).json({ error: 'Research dependencies are missing. Run npm run research:setup, then start again.' });
    if (parsed.data.sourceSessionId) { const source = store.get(parsed.data.sourceSessionId); if (!source || source.question !== parsed.data.question || ['running', 'paused'].includes(source.status)) return res.status(400).json({ error: 'Choose a finished record with the same question to develop its objections.' }); }
    const s = engine.create(parsed.data); s.workflow = parsed.data.workflow; s.modelMetadata = available.filter(m => requested.includes(m.name));
    if (s.workflow === 'discovery') { const { targetCount, trialBudget, corpusLimit, fulltextLimit, sourceSessionId } = parsed.data; const config = discovery.initialize(s, { targetCount, trialBudget, corpusLimit, fulltextLimit, sourceSessionId }, available); res.status(201).json(s); discovery.run(s, config).catch(e => { s.status = 'error'; s.error = e.message; engine.active.delete(s.id); engine.publish(s); }); }
    else { store.save(s); res.status(201).json(s); engine.run(s.id).catch(e => console.error('Research failure:', e.message)); }
  } catch (e) { res.status(503).json({ error: `Cannot start local inference: ${e.message}` }); }
});
app.post('/api/sessions/:id/control', async (req, res) => { const { action } = req.body; const ok = action === 'pause' ? engine.pause(req.params.id, true) : action === 'resume' ? engine.pause(req.params.id, false) : action === 'stop' ? engine.stop(req.params.id) : false; if (!ok) return res.status(409).json({ error: 'This session is no longer active or the action is invalid.' }); if (action !== 'stop') discovery.pause(req.params.id, action === 'pause'); else await discovery.stopped(req.params.id); res.json({ ok }); });
app.get('/api/sessions/:id/briefs/:briefId', (req, res) => { const s = store.get(req.params.id), b = s?.discovery?.briefs.find(b => b.id === req.params.briefId); if (!b) return res.status(404).json({ error: 'Brief not found in this research record.' }); res.type('text/markdown').setHeader('Content-Disposition', `attachment; filename="aporia-brief-${b.id.replace(/[^a-zA-Z0-9.-]/g, '')}.md"`); res.send(b.markdown || 'This brief is still being written.'); });
app.get('/api/sessions/:id/paper', (req, res) => { const s = store.get(req.params.id), p = s?.discovery?.papers.find(p => p.id === req.query.id); if (!p?.pdf_path) return res.status(404).json({ error: 'Only an abstract was available for this paper.' }); const root = resolve('research/data/jobs', s.id), path = resolve(root, p.pdf_path); if (!path.startsWith(root + sep)) return res.status(400).json({ error: 'Invalid source path.' }); try { res.type('text/plain').send(readFileSync(path, 'utf8')); } catch { res.status(404).json({ error: 'Cached source text is unavailable.' }); } });
app.get('/api/sessions/:id/events', (req, res) => {
  const s = store.get(req.params.id); if (!s) return res.status(404).json({ error: 'Session not found.' });
  res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' }); res.flushHeaders();
  res.write(`data: ${JSON.stringify(s)}\n\n`); if (!subscribers.has(s.id)) subscribers.set(s.id, new Set()); subscribers.get(s.id).add(res);
  const timer = setInterval(() => res.write(': heartbeat\n\n'), 12000);
  req.on('close', () => { clearInterval(timer); subscribers.get(s.id)?.delete(res); if (!subscribers.get(s.id)?.size) subscribers.delete(s.id); });
});
app.get('/api/sessions/:id/export', (req, res) => { const s = store.get(req.params.id); if (!s) return res.status(404).json({ error: 'Session not found.' }); res.setHeader('Content-Disposition', `attachment; filename="aproria-${s.id.slice(0, 8)}.json"`); res.json({ ...s, initialState: s.protocol ? store.getInitialState(s.protocol.initialStateDigest) : null }); });
app.use((err, _req, res, _next) => res.status(400).json({ error: err.type === 'entity.too.large' ? 'Request is too large.' : 'Invalid request.' }));
const server = app.listen(4317, '127.0.0.1', () => console.log('Cognitive engine: http://127.0.0.1:4317'));
function shutdown() { for (const id of engine.active.keys()) engine.stop(id); server.close(() => { store.close(); process.exit(); }); setTimeout(() => process.exit(), 3000).unref(); }
process.on('SIGINT', shutdown); process.on('SIGTERM', shutdown);
