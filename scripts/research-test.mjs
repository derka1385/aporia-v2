import { spawnSync } from 'node:child_process';
const r = spawnSync('.venv/bin/python', ['-m', 'pytest', '-q', 'tests'], { cwd: 'research', stdio: 'inherit' });
if (r.error) console.error(r.error.message);
process.exit(r.status ?? 1);
