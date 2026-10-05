import reference from './aporia-policies.json' with { type: 'json' };

export const FUNCTIONS = reference.OPS;
export const PROFILES = Object.keys(reference.TARGETS);
export const POLICY_SOURCE = reference.source;
export const MOVES = {
  imagine: 'Construct alternative hypotheses or concrete thought experiments.',
  counterfactual: 'Change one background assumption and examine whether the hypothesis still holds.',
  doubt: 'Find specific objections or counterexamples to a claim as literally stated.',
  formalize: 'Expose an inference gap by translating the argument for a bounded truth-table check.',
  memory: 'Bring relevant prior arguments and distant considerations into the inquiry.',
  inquire: 'Ask and investigate the sub-question most likely to change the hypothesis.',
  introspect: 'Expose the contestable assumptions on which the argument depends.',
  intuit: 'Identify promising branches without treating a hunch as evidence.',
  reason: 'Check explicit dependencies and identify missing premises.',
  adjudicate: 'Test a pending objection or counterfactual against the best available reply.',
  revise: 'Revise a challenged hypothesis using the recorded tests and objections.',
  conclude: 'State a provisional answer, its unresolved assumptions and the next useful question.'
};
// Exact reference interpolation, including Python's round-to-even rule for counts.
const roundEven = n => n % 1 === 0.5 ? Math.round(n / 2) * 2 : Math.round(n);
export function referencePolicyFor(id, delta, condition = 'architecture') {
  if (!PROFILES.includes(id)) throw new Error(`Unknown cognitive profile: ${id}`);
  if (!Number.isFinite(delta)) throw new Error('Δ must be finite.');
  const d = condition === 'architecture' ? Math.max(0, Math.min(1, delta)) : 0;
  const lerp = (base, target = base) => Array.isArray(base) ? [...(d >= 0.5 ? target : base)] : typeof base === 'object' ? Object.fromEntries(Object.entries(base).map(([k, v]) => [k, lerp(v, target[k] ?? v)])) : base + d * (target - base);
  const p = lerp(reference.BASE, reference.TARGETS[id]);
  for (const k of reference.INTS) p[k] = roundEven(p[k]);
  return p;
}
export function policyFor(id, delta, condition = 'architecture') {
  const p = referencePolicyFor(id, delta, condition);
  return {
    weights: p.weights, controllerTemperature: p.ctrl_temp, exploration: p.explore,
    learningRate: p.learning_rate, temperature: p.llm_temp, topP: p.top_p,
    contextTokens: 4096, visibleNodes: p.context, readingLimit: p.lit_k,
    readingSpread: p.lit_spread, memoryLimit: p.ltm_k, memoryScope: p.ltm_scope[0],
    branchLimit: p.branch, objectionLimit: p.objections, adversarialIntensity: p.adversarial,
    acceptanceThreshold: p.accept, stopConfidence: p.stop_conf, minSteps: p.min_steps,
    maxAssumptions: p.max_assumptions, rejectionThreshold: p.reject_below,
    tools: { logic: p.tools.includes('logic_check'), readings: p.tools.includes('literature_search'), memory: p.tools.includes('memory_search') }
  };
}
export function personaFor(id, delta) {
  if (delta < 0.15) return '';
  return `Your reasoning style: ${delta < 0.45 ? 'slightly' : delta < 0.8 ? 'clearly' : 'strongly'} ${reference.PERSONAS[id]}.`;
}
export function reflectionFor(policy, operation) {
  return { operation, task: MOVES[operation] || 'Form a provisional initial hypothesis from the common question.',
    limits: { alternatives: policy.branchLimit, objections: policy.objectionLimit, assumptions: policy.maxAssumptions, visibleNodes: policy.visibleNodes },
    criteria: { acceptance: policy.acceptanceThreshold, rejection: policy.rejectionThreshold, adversarialPressure: policy.adversarialIntensity },
    attention: { exploration: policy.exploration, controllerTemperature: policy.controllerTemperature },
    memory: { items: policy.tools.memory ? policy.memoryLimit : 0, scope: policy.memoryScope, readings: policy.tools.readings ? policy.readingLimit : 0, spread: policy.readingSpread }
  };
}
export function policyPreview(id, delta, condition = 'architecture') {
  const policy = policyFor(id, delta, condition);
  const dominant = Object.keys(MOVES).filter(op => !['adjudicate', 'revise', 'conclude'].includes(op)).sort((a, b) => policy.weights[b] - policy.weights[a])[0];
  return { id, policy, dominant, move: MOVES[dominant], persona: condition === 'prompt' ? personaFor(id, delta) : '', reflection: reflectionFor(policy, dominant) };
}
