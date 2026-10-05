import { lazy, Suspense, useEffect, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, ArrowDown, Pause, Play, Plus, Minus, Menu, X } from 'lucide-react';
import { SIMULATION } from '../visualStates.js';
import particleFallback from '../../brand/aporia/assets/visuals/particle-exploration.svg';
import './landing.css';

const Intelligence = lazy(() => import('../Intelligence.jsx'));
const inquiry = 'Is personal identity dependent on psychological continuity?';
const inquiryURL = '/app?question=' + encodeURIComponent(inquiry);
const profiles = [
  { id:'explorer', name:'Explorer', description:'Open more possibilities. Follow unfamiliar connections before narrowing the inquiry.', steps:['Map possible continuities','Explore memory, body and narrative','Find a question worth pursuing'] },
  { id:'formalist', name:'Formalist', description:'Make the structure explicit. Define the terms, separate the premises and test what follows.', steps:['Define a criterion for identity','Separate premise from assumption','Test the logical consequences'] },
  { id:'skeptic', name:'Skeptic', description:'Look for the point of failure. Challenge assumptions and examine the strongest counterexample.', steps:['Expose a hidden assumption','Construct a counterexample','Reconsider the original claim'] },
  { id:'synthesizer', name:'Synthesizer', description:'Bring competing accounts into relation. Look for a constraint they can share.', steps:['Compare competing accounts','Identify a shared constraint','Propose a provisional synthesis'] },
  { id:'minimalist', name:'Minimalist', description:'Keep only what the inquiry needs. Reduce the claim until its commitments become clear.', steps:['Reduce the claim to its core','Remove unnecessary assumptions','Retain a precise open question'] },
];
const states = [
  { id:'reasoning', name:'Reasoning', mode:'concentration', description:'Attention gathers around a line of reasoning. Iris holds the active thread.' },
  { id:'exploration', name:'Exploration', mode:'exploration', description:'The field opens toward other possibilities. Cyan traces a path being explored.' },
  { id:'conflict', name:'Conflict', mode:'conflict', description:'A competing claim puts the current path under pressure. Amber marks the tension.' },
];
const questions = [
  ['What is APORIA?', 'A local, experimental laboratory for philosophical inquiry. Five cognitive policies work from the same starting question, maintaining independent reasoning records that you can inspect and compare.'],
  ['What makes the five policies different?', 'Their control settings change how they explore, retrieve, branch, test objections and decide when to stop. The differentiation parameter Δ adjusts how far each policy moves from a shared baseline. Disagreement itself is never rewarded.'],
  ['Where does the research run?', 'On your own machine, using local Ollama models and a local research server. Sessions and memory are stored locally. Open the laboratory to choose an installed model and begin an inquiry.'],
  ['How should I read a conclusion?', 'As provisional. The record exposes assumptions, objections, tests and limitations. Confidence is a controller heuristic; a completed run does not establish philosophical truth.'],
];

function Mark() {
  return <svg viewBox="0 0 128 128" fill="none" aria-hidden="true"><g stroke="currentColor" strokeWidth="7" strokeLinecap="butt" strokeLinejoin="round"><path d="M108.184 45.245 A48 48 0 1 1 64.838 16.007"/><path d="M93.875 75.468 A32 32 0 1 1 86.627 41.373"/><path d="M70.762 78.501 A16 16 0 1 1 79.998 63.721"/></g></svg>;
}
function Signature() { return <><Mark/><span>APORIA</span></>; }
function LabLink({ className='', children='Open the laboratory', example=false }) {
  return <a className={'ap-action ' + className} href={example ? inquiryURL : '/app'}>{children}<ArrowUpRight size={19} strokeWidth={1.5} aria-hidden="true"/></a>;
}

export default function Landing() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeState, setActiveState] = useState('exploration');
  const [paused, setPaused] = useState(false);
  const [fieldVisible, setFieldVisible] = useState(true);
  const [profileId, setProfileId] = useState('explorer');
  const field = useRef(null), tabRefs = useRef([]);
  const currentState = states.find(s => s.id === activeState);
  const profile = profiles.find(p => p.id === profileId);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => setFieldVisible(entry.isIntersecting), { rootMargin:'80px' });
    observer.observe(field.current);
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    const close = e => { if (e.key === 'Escape') setMenuOpen(false); };
    window.addEventListener('keydown', close);
    return () => window.removeEventListener('keydown', close);
  }, []);

  function selectWithKeyboard(event, index) {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % profiles.length;
    else if (event.key === 'ArrowLeft') next = (index + profiles.length - 1) % profiles.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = profiles.length - 1;
    else return;
    event.preventDefault(); setProfileId(profiles[next].id); tabRefs.current[next].focus();
  }
  const still = <img className="ap-field-fallback" src={particleFallback} alt="Folded particle geometry" width="960" height="660"/>;

  return <div className="ap-landing" id="top">
    <a className="ap-skip" href="#main">Skip to content</a>
    <header className="ap-header ap-wrap">
      <a className="ap-signature" href="#top" aria-label="APORIA home"><Signature/></a>
      <nav id="landing-navigation" className={'ap-nav' + (menuOpen ? ' is-open' : '')} aria-label="Main navigation">
        <a href="#approach" onClick={() => setMenuOpen(false)}>The approach</a>
        <a href="#method" onClick={() => setMenuOpen(false)}>The method</a>
        <a href="#questions" onClick={() => setMenuOpen(false)}>Questions</a>
        <LabLink className="ap-nav-action"/>
      </nav>
      <button className="ap-menu-toggle" type="button" aria-label={menuOpen ? 'Close navigation' : 'Open navigation'} aria-expanded={menuOpen} aria-controls="landing-navigation" onClick={() => setMenuOpen(v => !v)}>{menuOpen ? <X size={23}/> : <Menu size={23}/>}</button>
    </header>

    <main id="main">
      <section className="ap-hero ap-wrap" aria-labelledby="hero-title">
        <div className="ap-hero-copy">
          <h1 id="hero-title">Reasoning under<br/><em>uncertainty.</em></h1>
          <p className="ap-hero-lead">One question. Five ways of thinking.</p>
          <p className="ap-hero-description">A local laboratory for philosophical inquiry.<br className="ap-desktop-break"/> Follow independent reasoning paths, inspect their assumptions, and see what remains open.</p>
          <div className="ap-hero-actions"><LabLink className="ap-action-filled"/><a className="ap-text-link" href="#approach">Explore the approach<ArrowDown size={17} aria-hidden="true"/></a></div>
          <p className="ap-local-note">Local inference. Inspectable reasoning.</p>
        </div>
        <div className="ap-hero-specimen" ref={field}>
          <div className="ap-particle-stage">
            <Suspense fallback={still}><Intelligence state={SIMULATION[currentState.mode]} delta={0.6} paused={paused} palette="obsidian" active={fieldVisible} fallback={still}/></Suspense>
          </div>
          <div className="ap-state-controls" aria-label="Visual state simulation">
            <div className="ap-state-choices">{states.map(s => <button key={s.id} type="button" className={'ap-state-button is-' + s.id} aria-pressed={activeState === s.id} onClick={() => setActiveState(s.id)}><span className={'ap-state-shape ' + s.id} aria-hidden="true"/>{s.name}</button>)}</div>
            <button className="ap-motion-button" type="button" aria-label={paused ? 'Resume particle animation' : 'Pause particle animation'} aria-pressed={paused} onClick={() => setPaused(v => !v)}>{paused ? <Play size={16} aria-hidden="true"/> : <Pause size={16} aria-hidden="true"/>}</button>
          </div>
          <div className="ap-specimen-caption"><span>Visual state simulation</span><p aria-live="polite">{currentState.description}</p></div>
        </div>
        <div className="ap-hero-end"><p>A shared starting point. Independent records.</p><a href="#method">From question to inquiry<ArrowRight size={17} aria-hidden="true"/></a></div>
      </section>

      <section className="ap-paper" id="approach" aria-labelledby="approach-title">
        <div className="ap-wrap ap-approach">
          <div className="ap-section-intro"><h2 id="approach-title">A common origin.<br/>Different paths.</h2><p>What changes when the same question meets a different way of reasoning? APORIA explores that difference through five cognitive policies, each with its own evolving record.</p></div>
          <div className="ap-policy-specimen">
            <div className="ap-question-row"><div><span className="ap-small-label">The shared question</span><p>“Is personal identity dependent on<br className="ap-desktop-break"/> psychological continuity?”</p></div><a className="ap-text-link" href={inquiryURL}>Investigate this question<ArrowUpRight size={18} aria-hidden="true"/></a></div>
            <div className="ap-profile-tabs" role="tablist" aria-label="Cognitive policy">{profiles.map((p,i) => <button ref={el => { tabRefs.current[i] = el; }} key={p.id} id={'tab-' + p.id} type="button" role="tab" aria-selected={profileId === p.id} aria-controls="policy-panel" tabIndex={profileId === p.id ? 0 : -1} onClick={() => setProfileId(p.id)} onKeyDown={e => selectWithKeyboard(e,i)}>{p.name}<ArrowUpRight size={15} strokeWidth={1.5} aria-hidden="true"/></button>)}</div>
            <div className="ap-profile-panel" id="policy-panel" role="tabpanel" aria-labelledby={'tab-' + profileId} tabIndex={0}>
              <div className="ap-profile-description"><h3>{profile.name}</h3><p>{profile.description}</p></div>
              <ol className="ap-path">{profile.steps.map((step,i) => <li key={profile.id + i}><span className="ap-path-node" aria-hidden="true"/><span className="ap-path-count">{i+1}</span><p>{step}</p></li>)}</ol>
            </div>
            <p className="ap-illustration-note">Illustrative workflow. Actual trajectories depend on the question, model and controller state.</p>
          </div>
          <div className="ap-approach-close"><p>Difference is a research question.<br/><strong>Disagreement is never the objective.</strong></p><p>Profiles start from the same question and preserve independent records. Compare the assumptions, objections and operations that produced a position.</p></div>
        </div>
      </section>

      <section className="ap-wrap ap-method" id="method" aria-labelledby="method-title">
        <div className="ap-method-heading"><h2 id="method-title">A thought is more<br/>than its conclusion.</h2><p>The path matters. APORIA makes its structure available for inspection, from the first assumption to the next unresolved question.</p><a className="ap-text-link" href="/app">Enter the instrument<ArrowUpRight size={19} aria-hidden="true"/></a></div>
        <ol className="ap-method-steps">
          <li><span className="ap-step-number">1</span><div><h3>Begin with a question</h3><p>Choose a philosophical inquiry, a local model and a degree of cognitive differentiation. Every policy receives the same starting point.</p></div></li>
          <li><span className="ap-step-number">2</span><div><h3>Inspect the reasoning</h3><p>Follow hypotheses, assumptions and objections in the argument graph. Examine the operations and tests that change the record.</p></div></li>
          <li><span className="ap-step-number">3</span><div><h3>Compare what emerges</h3><p>Read the paths together, inspect their differences, and export the experiment. Each conclusion remains provisional.</p></div></li>
        </ol>
      </section>

      <section className="ap-questions ap-wrap" id="questions" aria-labelledby="questions-title"><h2 id="questions-title">Before you begin.</h2><div className="ap-faq-list">{questions.map(([title,answer]) => <details key={title}><summary><span>{title}</span><Plus className="ap-faq-plus" size={21} strokeWidth={1.5} aria-hidden="true"/><Minus className="ap-faq-minus" size={21} strokeWidth={1.5} aria-hidden="true"/></summary><p>{answer}</p></details>)}</div></section>

      <section className="ap-paper ap-closing" aria-labelledby="closing-title"><div className="ap-wrap"><div><h2 id="closing-title">Keep the question open.</h2><p>Give an idea more than one path to follow.</p></div><LabLink className="ap-action-filled"/></div></section>
    </main>
    <footer className="ap-footer ap-wrap"><a className="ap-signature" href="#top" aria-label="APORIA home"><Signature/></a><p>An experimental space for thought.</p><a className="ap-text-link" href="#top">Back to the question<ArrowUpRight size={16} aria-hidden="true"/></a></footer>
  </div>;
}
