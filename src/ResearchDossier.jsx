const number = n => (n ?? 0).toLocaleString();
export default function ResearchDossier({ session, profile }) {
  const q = profile.quality, protocol = session.protocol;
  if (!q) return <div className="research-dossier"><h3>Legacy research record</h3><p>This preserved run predates the research protocol. Its graph and history remain inspectable; its initial state and evidence coverage were not recorded.</p></div>;
  return <div className="research-dossier">
    <h3>What has actually been tested?</h3>
    <p className="dossier-intro">Read the evidence boundary before interpreting a conclusion.</p>
    <dl className="evidence-register">
      <div><dt>Current hypothesis</dt><dd>{q.currentHypothesisTests} completed model tests</dd></div>
      <div><dt>Assumptions tested</dt><dd>{q.testedAssumptions} of {q.assumptions}</dd></div>
      <div><dt>Formal support for this hypothesis</dt><dd>{q.currentFormalSupport} valid formalizations</dd></div>
      <div><dt>Challenges awaiting a verdict</dt><dd>{q.pendingChallenges}</dd></div>
      <div><dt>Unresolved objections</dt><dd>{q.unresolvedObjections}</dd></div>
    </dl>
    <p className="evidence-boundary">{q.evidenceBoundary}</p>
    {q.warnings.length > 0 && <ul className="dossier-warnings">{q.warnings.map(text => <li key={text}>{text}</li>)}</ul>}
    <h4>Questions worth carrying forward</h4>
    {q.openQuestions.length ? <ul className="open-questions">{q.openQuestions.map(item => <li key={item.id}>{item.text}</li>)}</ul> : <p>No open question has been recorded yet.</p>}
    <details><summary>Reproduce this experiment</summary><dl className="protocol-register">
      <div><dt>Engine</dt><dd>{session.engineVersion}</dd></div>
      <div><dt>Seed</dt><dd>{session.seed}</dd></div>
      <div><dt>Memory</dt><dd>{protocol.memoryMode === 'fresh' ? 'Fresh state' : 'Prior research'} · {protocol.initialMemoryCount} initial memories</dd></div>
      <div><dt>Code fingerprint</dt><dd><code>{protocol.codeDigest}</code></dd></div>
      <div><dt>Initial-state fingerprint</dt><dd><code>{protocol.initialStateDigest}</code></dd></div>
      {session.modelMetadata?.map(model => <div key={model.name}><dt>{model.name}</dt><dd>{model.quantization} · <code>{model.digest}</code></dd></div>)}
    </dl><p>The JSON export includes the initial memory and learned routing snapshot. A fixed seed does not guarantee identical results across model or runtime versions.</p></details>
    <details><summary>Compute used by this run</summary><dl className="protocol-register">
      <div><dt>Input / generated tokens</dt><dd>{number(session.usage?.inputTokens)} / {number(session.usage?.outputTokens)}</dd></div>
      <div><dt>Inference time</dt><dd>{Math.round((session.usage?.inferenceMs || 0) / 1000)} seconds</dd></div>
      <div><dt>Reused / repaired requests</dt><dd>{number(session.usage?.cachedRequests)} / {number(session.usage?.repairedRequests)}</dd></div>
      <div><dt>Failed operations</dt><dd>{number(session.usage?.failedOperations)}</dd></div>
    </dl><p>{protocol.computeBoundary}</p></details>
  </div>;
}
