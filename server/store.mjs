import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { similarity } from './tools.mjs';

export class Store {
  constructor(path = 'data/aproria.sqlite') {
    if (path !== ':memory:') mkdirSync(dirname(path), { recursive: true });
    this.db = new DatabaseSync(path);
    this.db.exec(`PRAGMA journal_mode=WAL;
      CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, created TEXT, question TEXT, status TEXT, snapshot TEXT);
      CREATE TABLE IF NOT EXISTS memories (id TEXT PRIMARY KEY, session_id TEXT, profile TEXT, question TEXT, type TEXT, text TEXT, status TEXT, confidence REAL, utility REAL);
      CREATE TABLE IF NOT EXISTS rewards (session_id TEXT, profile TEXT, operation TEXT, gain REAL);
      CREATE TABLE IF NOT EXISTS initial_states (digest TEXT PRIMARY KEY, snapshot TEXT);`);
    // A process restart cannot leave an apparently running experiment.
    for (const row of this.db.prepare("SELECT id, snapshot FROM sessions WHERE status='running' OR status='paused'").all()) {
      const s = JSON.parse(row.snapshot); s.status = 'interrupted'; s.error = 'Server restarted. This partial record is preserved; start a new run to continue research.'; this.save(s);
    }
  }
  save(s) { this.db.prepare('INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?, ?)').run(s.id, s.created, s.question, s.status, JSON.stringify(s)); }
  saveInitialState(digest, state) { this.db.prepare('INSERT OR IGNORE INTO initial_states VALUES (?, ?)').run(digest, JSON.stringify(state)); }
  getInitialState(digest) { const row = this.db.prepare('SELECT snapshot FROM initial_states WHERE digest=?').get(digest); return row ? JSON.parse(row.snapshot) : null; }
  get(id) { const r = this.db.prepare('SELECT snapshot FROM sessions WHERE id=?').get(id); return r ? JSON.parse(r.snapshot) : null; }
  list() { return this.db.prepare('SELECT id, created, question, status FROM sessions ORDER BY created DESC LIMIT 40').all(); }
  memorySnapshot() { return this.db.prepare('SELECT * FROM memories ORDER BY rowid DESC LIMIT 2000').all(); }
  retrieve(snapshot, query, limit = 4) { return snapshot.map(m => ({ ...m, similarity: similarity(query, `${m.question} ${m.text}`) })).filter(m => m.similarity > 0.16).sort((a, b) => b.similarity * (0.5 + b.utility) - a.similarity * (0.5 + a.utility)).slice(0, limit); }
  remember(s, p) {
    const insert = this.db.prepare('INSERT OR REPLACE INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
    for (const n of p.graph.nodes) if (['hypothesis', 'assumption', 'objection', 'counterexample', 'question'].includes(n.type)) insert.run(`${s.id}:${p.id}:${n.id}`, s.id, p.id, s.question, n.type, n.text, n.status, n.confidence, n.importance);
  }
  reward(sessionId, profile, operation, gain) { this.db.prepare('INSERT INTO rewards VALUES (?, ?, ?, ?)').run(sessionId, profile, operation, gain); }
  rewardSnapshot() { return this.db.prepare('SELECT operation, AVG(gain) AS gain, COUNT(*) AS count FROM rewards GROUP BY operation').all(); }
  stats() { return { sessions: this.db.prepare('SELECT COUNT(*) AS n FROM sessions').get().n, memories: this.db.prepare('SELECT COUNT(*) AS n FROM memories').get().n }; }
  close() { this.db.close(); }
}
