import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve } from 'node:path';
const bundled = resolve(homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3');
const python = process.env.APORIA_PYTHON || (existsSync(bundled) ? bundled : '3.12');
function run(args) { const r = spawnSync('uv', ['--cache-dir', 'research/.uv-cache', ...args], { stdio: 'inherit' }); if (r.error || r.status) { console.error(r.error?.message || 'Research dependency setup failed.'); process.exit(r.status || 1); } }
if (!existsSync('research/.venv/bin/python')) run(['venv', '--python', python, 'research/.venv']);
run(['pip', 'install', '--python', 'research/.venv/bin/python', '-r', 'research/requirements.lock.txt']);
console.log('Paper discovery dependencies are ready.');
