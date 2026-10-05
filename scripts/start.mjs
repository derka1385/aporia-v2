import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, openSync } from 'node:fs';
const children = []; let closing = false;
function run(command, args, options = {}) { const p = spawn(command, args, { stdio: 'inherit', ...options }); children.push(p); p.on('error', e => { console.error(e.message); close(1); }); p.on('exit', code => { if (!closing && code) close(code); }); return p; }
function close(code = 0) { if (closing) return; closing = true; for (const p of children) p.kill('SIGTERM'); setTimeout(() => process.exit(code), 500); }
process.on('SIGINT', () => close()); process.on('SIGTERM', () => close());
if (!existsSync('node_modules')) { console.error('Install project dependencies with npm install, then run npm start.'); process.exit(1); }
let connected = false;
try { connected = (await fetch('http://127.0.0.1:11434/api/tags', { signal: AbortSignal.timeout(2000) })).ok; } catch {}
if (!connected) {
  mkdirSync('data', { recursive: true });
  const log = openSync('data/ollama.log', 'a');
  const p = spawn('ollama', ['serve'], { env: { ...process.env, OLLAMA_HOST: '127.0.0.1:11434', OLLAMA_NO_CLOUD: '1', OLLAMA_NOPRUNE: '1' }, stdio: ['ignore', log, log] }); children.push(p);
  p.on('error', () => console.warn('Ollama was not found. The visual studies remain available; install Ollama for research.'));
}
run(process.execPath, ['server/index.mjs']);
run(process.execPath, ['node_modules/vite/bin/vite.js']);
console.log('\nAproria · http://localhost:5173\n');
