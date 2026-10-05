import { useState } from 'react';
const colors = { hypothesis: '#abc5db', premise: '#719bc1', assumption: '#b0a1d7', counterexample: '#d9aa77', objection: '#dc8e6a', evidence: '#82bbb0', question: '#8ba7b5', concept: '#8ba7b5' };
export default function ArgumentGraph({ profile }) {
  const [selected, setSelected] = useState(null);
  const nodes = profile.graph.nodes;
  const active = nodes.find(n => n.id === selected) || nodes.find(n => n.id === profile.root);
  const columns = [['premise', 'assumption', 'concept'], ['hypothesis'], ['counterexample', 'objection', 'evidence', 'question']];
  const positions = {};
  let height = 320;
  columns.forEach((types, col) => { const list = nodes.filter(n => types.includes(n.type)); height = Math.max(height, list.length * 72 + 56); list.forEach((n, i) => { positions[n.id] = { x: 115 + col * 215, y: 50 + i * 72 }; }); });
  return <div className="argument-view">
    <div className="graph-scroll"><svg viewBox={`0 0 660 ${height}`} className="argument-graph" aria-label="Argument dependency graph">
      <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#485969" /></marker></defs>
      {profile.graph.edges.map((e, i) => { const a = positions[e.from], b = positions[e.to]; if (!a || !b) return null; return <g key={i}><path d={`M${a.x} ${a.y} C${(a.x + b.x) / 2} ${a.y}, ${(a.x + b.x) / 2} ${b.y}, ${b.x} ${b.y}`} fill="none" stroke={e.type === 'attacks' ? '#895943' : '#354656'} strokeWidth={e.from === active?.id || e.to === active?.id ? 1.5 : 0.7} strokeDasharray={e.type === 'depends_on' ? '3 4' : undefined} markerEnd="url(#arrow)" /><title>{e.type.replaceAll('_', ' ')}</title></g>; })}
      {nodes.map(n => { const p = positions[n.id]; if (!p) return null; return <g key={n.id} transform={`translate(${p.x},${p.y})`} className={`graph-node ${n.status === 'rejected' ? 'rejected' : ''}`} role="button" tabIndex={0} aria-label={`${n.type}: ${n.text}`} onClick={() => setSelected(n.id)} onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setSelected(n.id); } }}>
        <rect x="-85" y="-23" width="170" height="46" rx="5" fill={n.id === active?.id ? '#19222d' : '#10161e'} stroke={n.id === active?.id ? colors[n.type] : '#26313d'} strokeWidth="1" />
        <circle cx="-72" cy="-9" r="2.5" fill={colors[n.type]} /><text x="-63" y="-6" fill={colors[n.type]} fontSize="9">{n.type.toUpperCase()}</text><text x="-72" y="12" fill="#a9b4c2" fontSize="9">{n.text.length > 26 ? `${n.text.slice(0, 25)}…` : n.text}</text><title>{n.text}</title>
      </g>; })}
    </svg></div>
    {active && <div className="node-inspector"><div className="row"><span className="tag" style={{ color: colors[active.type] }}>{active.type}</span><span>{active.status}</span></div><p>{active.text}</p><div className="node-stats"><span>Confidence <b>{Math.round(active.confidence * 100)}%</b></span><span>Curiosity <b>{(active.curiosity || 0).toFixed(2)}</b></span><span>Source <b>{active.source.replaceAll('-', ' ')}</b></span></div>{active.prediction && <p className="muted">Prediction: {active.prediction}</p>}{active.toolResult && <pre>{JSON.stringify(active.toolResult, null, 2)}</pre>}</div>}
    {!nodes.length && <p className="muted empty">The graph will appear when the first hypothesis is formed.</p>}
  </div>;
}
