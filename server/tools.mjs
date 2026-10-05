export const clamp = (n, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, n));
const stop = new Set('the a an is are of to in and or that this it be with as for on by if can does would should what how under which from'.split(' '));
export function tokens(text = '') { return String(text).toLowerCase().match(/[\p{L}\p{N}]{2,}/gu)?.filter(w => !stop.has(w)).map(w => w.replace(/(ing|ation|s)$/, '')) || []; }
export function similarity(a, b) {
  const counts = s => tokens(s).reduce((m, t) => (m[t] = (m[t] || 0) + 1, m), {});
  const x = counts(a), y = counts(b);
  const dot = Object.keys(x).reduce((s, k) => s + x[k] * (y[k] || 0), 0);
  const norm = m => Math.sqrt(Object.values(m).reduce((s, v) => s + v * v, 0));
  return dot / (norm(x) * norm(y) || 1);
}
export function pathSimilarity(a, b) {
  const rows = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) rows[i][j] = a[i - 1] === b[j - 1] ? rows[i - 1][j - 1] + 1 : Math.max(rows[i - 1][j], rows[i][j - 1]);
  return 2 * rows[a.length][b.length] / (a.length + b.length || 1);
}
export function uniqueTexts(texts, threshold = 0.86) { return texts.reduce((out, s) => out.some(t => similarity(t, s) >= threshold) ? out : [...out, s], []); }

// A bounded Boolean parser, with no eval or executable model output.
export function parseFormula(source) {
  if (typeof source !== 'string' || source.length > 200) throw new Error('Formula must be a string of at most 200 characters.');
  const lex = source.match(/->|[!&|()]|[A-Z][A-Z0-9_]*/g) || [];
  if (lex.join('') !== source.replace(/\s/g, '')) throw new Error('Use uppercase atoms and !, &, |, ->, parentheses only.');
  let i = 0;
  const atom = () => {
    const t = lex[i++];
    if (t === '!') return { op: '!', a: atom() };
    if (t === '(') { const x = implication(); if (lex[i++] !== ')') throw new Error('Unclosed parentheses.'); return x; }
    if (/^[A-Z][A-Z0-9_]*$/.test(t || '')) return { atom: t };
    throw new Error('Expected a proposition.');
  };
  const and = () => { let x = atom(); while (lex[i] === '&') { i++; x = { op: '&', a: x, b: atom() }; } return x; };
  const or = () => { let x = and(); while (lex[i] === '|') { i++; x = { op: '|', a: x, b: and() }; } return x; };
  const implication = () => { const x = or(); if (lex[i] === '->') { i++; return { op: '->', a: x, b: implication() }; } return x; };
  const tree = implication();
  if (i !== lex.length) throw new Error('Unexpected formula tokens.');
  return tree;
}
function evaluate(t, values) { if (t.atom) return values[t.atom]; const a = evaluate(t.a, values); if (t.op === '!') return !a; const b = evaluate(t.b, values); return t.op === '&' ? a && b : t.op === '|' ? a || b : !a || b; }
export function checkLogic({ premises, conclusion, bindings = {} }) {
  if (!Array.isArray(premises) || premises.length < 1 || premises.length > 10) throw new Error('Supply 1–10 premises.');
  const trees = [...premises, conclusion].map(parseFormula);
  const atoms = new Set();
  const visit = t => { if (t.atom) atoms.add(t.atom); else { visit(t.a); if (t.b) visit(t.b); } }; trees.forEach(visit);
  if (atoms.size > 10) throw new Error('Maximum 10 Boolean atoms.');
  const names = [...atoms]; let satisfying = 0;
  for (let mask = 0; mask < 2 ** names.length; mask++) {
    const values = Object.fromEntries(names.map((n, i) => [n, !!(mask & (1 << i))]));
    if (trees.slice(0, -1).every(t => evaluate(t, values))) {
      satisfying++;
      if (!evaluate(trees.at(-1), values)) return { tool: 'propositional-checker', valid: false, consistent: true, countermodel: values, bindings, checkedWorlds: mask + 1, limitation: 'Tests this formalization only; atoms and premises are not verified facts.' };
    }
  }
  return { tool: 'propositional-checker', valid: true, consistent: satisfying > 0, countermodel: null, bindings, checkedWorlds: 2 ** names.length, limitation: satisfying ? 'Validity is conditional on the supplied formalization.' : 'Vacuously valid: premises are jointly inconsistent.' };
}

export const bibliography = [
  { title: 'Personal Identity', keywords: 'personal identity psychological continuity memory persistence fission body person', url: 'https://plato.stanford.edu/entries/identity-personal/', description: 'SEP reference on persistence, psychological continuity, fission and animalism.' },
  { title: 'Free Will', keywords: 'free will determinism freedom choice responsibility agency', url: 'https://plato.stanford.edu/entries/freewill/', description: 'SEP reference on freedom, determinism and accounts of agency.' },
  { title: 'Moral Responsibility', keywords: 'moral responsibility blame praise free will ethics accountability', url: 'https://plato.stanford.edu/entries/moral-responsibility/', description: 'Reading pointer for responsibility and accountability; text is not retrieved by this tool.' },
  { title: 'Consciousness', keywords: 'consciousness conscious subjective experience machine qualia mind', url: 'https://plato.stanford.edu/entries/consciousness/', description: 'Reading pointer for theories of consciousness; text is not retrieved by this tool.' },
  { title: 'Knowledge Analysis', keywords: 'knowledge belief truth justification justified true belief gettier', url: 'https://plato.stanford.edu/entries/knowledge-analysis/', description: 'Reading pointer for the analysis of knowledge; text is not retrieved by this tool.' }
];
export function readingSearch(query, limit = 3, spread = 0) {
  const candidates = bibliography.map(r => ({ ...r, score: similarity(query, r.keywords) }));
  const selected = [], remaining = candidates.filter(r => r.score > 0.07 || spread > 0);
  while (selected.length < limit && remaining.length) {
    const utility = r => (1 - spread) * r.score + spread * (1 - Math.max(0, ...selected.map(s => similarity(r.keywords, s.keywords))));
    remaining.sort((a, b) => utility(b) - utility(a) || b.score - a.score);
    selected.push(remaining.shift());
  }
  return selected;
}
