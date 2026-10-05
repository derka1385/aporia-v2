import { Component, useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
export { SIMULATION } from './visualStates.js';

const vertex = `
uniform float uTime, uDelta, uCuriosity, uUncertainty, uConflict, uAttention, uConfidence, uInsight, uCollapse;
uniform vec3 uBlue, uCyan, uIris, uWarm, uPaper;
uniform float uBrand;
attribute vec3 aSeed;
varying vec3 vColor;
varying float vAlpha;
vec3 center(float u) {
  float r = 1.17 + .36 * cos(3.0*u);
  return vec3(r*cos(2.0*u), r*sin(2.0*u), .61*sin(3.0*u));
}
void main() {
  float u = aSeed.x * 6.2831853;
  float v = aSeed.y * 6.2831853;
  float t = uTime;
  vec3 c = center(u);
  vec3 tangent = normalize(center(u+.005)-center(u-.005));
  vec3 normal = normalize(vec3(cos(2.0*u),sin(2.0*u),0.0));
  vec3 binormal = normalize(cross(tangent,normal));
  normal = normalize(cross(binormal,tangent));
  float fold = .05 * sin(v*3.0 + u*5.0 + t*.21) + .025 * cos(u*9.0-v*2.0);
  float breath = .025 * sin(t*.6 + u*3.0);
  float width = (.32 + .09*sin(u*3.0+1.4) + fold + breath) * (1.0 - uAttention*.23);
  float flowV = v + t*.07 + .07*sin(u*5.0+t*.3);
  vec3 p = c + width * (normal*cos(flowV)+binormal*sin(flowV)) * (.88 + .2*aSeed.z);
  p *= 1.0 + uCuriosity*.22 - uAttention*.14;
  float branch = pow(max(0.0,sin(u*3.0+t*.22)), 9.0);
  p += normal * branch * uCuriosity * (.12 + uDelta*.42) * sin(v*1.5);
  float pole = sin(u*3.0);
  p.x += pole * uConflict * (.15+uDelta*.4);
  p.z += cos(u*3.0) * uConflict * .34;
  vec3 turbulence = vec3(sin(u*31.0+t*.55), cos(v*23.0-t*.7), sin(u*17.0+v*19.0+t*.6));
  p += turbulence * (.012 + uUncertainty*.062) * aSeed.z * (1.0-uConfidence*.45-uInsight*.45);
  float region = pow(max(0.0,cos(u-1.0)), 12.0);
  p += normal * region * uCollapse * (.3 + aSeed.z*.7);
  p += binormal * region * uCollapse * sin(v*11.0+t*.8)*.28;
  p *= 1.0 + uDelta*.04*sin(u*7.0+v*3.0+t*.13);
  float insightRegion = pow(max(0.0,cos(u+1.0)), 5.0) * uInsight;
  vec3 cool = mix(uBlue,uCyan, .5+.5*cos(v+u*.8));
  cool = mix(cool,uIris, .25*max(0.0,sin(u*2.0)));
  if (uBrand > .5) cool = mix(uIris,uCyan,clamp(uCuriosity*.85+.14*cos(v+u*.8),0.0,1.0));
  vColor = mix(cool,uWarm,uConflict*max(0.0,pole)*.85);
  vColor = mix(vColor,uPaper,insightRegion*.8);
  float facing = .38 + .62*pow(abs(sin(v)),.6);
  vAlpha = facing * (.46 + .4*aSeed.z) * (1.0-region*uCollapse*.64);
  vec4 mv = modelViewMatrix * vec4(p,1.0);
  gl_PointSize = clamp((1.35 + aSeed.z*.85 + insightRegion*.6) * (5.3 / -mv.z), .6, 3.5);
  gl_Position = projectionMatrix*mv;
}`;
const fragment = `varying vec3 vColor; varying float vAlpha;
void main(){float d=length(gl_PointCoord-.5); if(d>.5) discard; float a=(1.0-smoothstep(.14,.5,d))*vAlpha; gl_FragColor=vec4(vColor,a);}`;
function Sculpture({ state, delta, reduced, paused, pointer, palette, active }) {
  const { camera, size, invalidate } = useThree();
  useEffect(() => { invalidate(); }, [state, delta, reduced, paused, active, invalidate]);
  useEffect(() => { camera.fov = size.width < 600 ? 52 : 43; camera.updateProjectionMatrix(); }, [camera, size.width]);
  const material = useRef(), group = useRef();
  const count = window.innerWidth < 600 ? 25000 : 54000;
  const seeds = useMemo(() => {
    const data = new Float32Array(count * 3); let s = 9719;
    const random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
    for (let i = 0; i < count; i++) { data[i * 3] = random(); data[i * 3 + 1] = random(); data[i * 3 + 2] = random(); }
    return data;
  }, [count]);
  const uniforms = useMemo(() => ({
    ...Object.fromEntries(['Time', 'Delta', 'Curiosity', 'Uncertainty', 'Conflict', 'Attention', 'Confidence', 'Insight', 'Collapse'].map(k => [`u${k}`, { value: k === 'Delta' ? delta : 0 }])),
    uBlue: { value: new THREE.Vector3(.19,.33,.63) }, uCyan: { value: new THREE.Vector3(.46,.78,.89) },
    uIris: { value: new THREE.Vector3(.58,.49,.84) }, uWarm: { value: new THREE.Vector3(.95,.53,.30) },
    uPaper: { value: new THREE.Vector3(.9,.97,1) }, uBrand: { value: 0 },
  }), []);
  useEffect(() => {
    const brand = palette === 'obsidian';
    const values = brand ? {
      Blue:[183/255,162/255,232/255], Cyan:[121/255,197/255,207/255], Iris:[183/255,162/255,232/255],
      Warm:[221/255,177/255,107/255], Paper:[244/255,241/255,233/255],
    } : { Blue:[.19,.33,.63], Cyan:[.46,.78,.89], Iris:[.58,.49,.84], Warm:[.95,.53,.30], Paper:[.9,.97,1] };
    for (const [name, rgb] of Object.entries(values)) uniforms['u' + name].value.set(...rgb);
    uniforms.uBrand.value = brand ? 1 : 0;
  }, [palette, uniforms]);
  useFrame((_s, dt) => {
    if (!material.current) return;
    const u = material.current.uniforms;
    if (!reduced && !paused) u.uTime.value += Math.min(dt, 0.05);
    const target = { Delta: delta, Curiosity: state.curiosity ?? 0.15, Uncertainty: state.uncertainty ?? 0.15, Conflict: state.contradiction ?? 0, Attention: state.attention ?? 0.15, Confidence: state.confidence ?? 0.5, Insight: state.mode === 'insight' ? 1 : 0, Collapse: state.mode === 'collapse' ? 1 : 0 };
    const blend = 1 - Math.exp(-Math.min(dt, 0.1) * 2.6);
    let settling = false;
    for (const [k, v] of Object.entries(target)) { const gap = v - u[`u${k}`].value; if (Math.abs(gap) > .001) settling = true; u[`u${k}`].value += gap * blend; }
    const t = u.uTime.value;
    group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, .72 + (reduced ? 0 : pointer.current.y * .08), blend);
    group.current.rotation.y = THREE.MathUtils.lerp(group.current.rotation.y, -.28 + (reduced ? 0 : pointer.current.x * .16) + Math.sin(t * .045) * .14, blend);
    group.current.rotation.z = -.22 + Math.sin(t * .065) * .045;
    if (active && (reduced || paused) && settling) invalidate();
  });
  return <group ref={group} rotation={[0.72, -0.28, -0.22]}><points frustumCulled={false}>
    <bufferGeometry><bufferAttribute attach="attributes-position" args={[new Float32Array(count * 3), 3]} /><bufferAttribute attach="attributes-aSeed" args={[seeds, 3]} /></bufferGeometry>
    <shaderMaterial ref={material} vertexShader={vertex} fragmentShader={fragment} uniforms={uniforms} transparent depthWrite={false} blending={THREE.AdditiveBlending} />
  </points></group>;
}
class RenderBoundary extends Component {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() { return this.state.failed ? this.props.fallback || <div className="render-fallback">The particle engine needs WebGL.<br /><span>Research and argument inspection remain available.</span></div> : this.props.children; }
}
export default function Intelligence({ state, delta, paused, palette, active = true, fallback }) {
  const pointer = useRef({ x: 0, y: 0 });
  const host = useRef(null);
  const [reduced, setReduced] = useState(false);
  const [visible, setVisible] = useState(true), [pageVisible, setPageVisible] = useState(!document.hidden);
  useEffect(() => { const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting), { rootMargin: '60px' }); observer.observe(host.current); const sync = () => setPageVisible(!document.hidden); document.addEventListener('visibilitychange', sync); return () => { observer.disconnect(); document.removeEventListener('visibilitychange', sync); }; }, []);
  useEffect(() => { const m = matchMedia('(prefers-reduced-motion: reduce)'); const sync = () => setReduced(m.matches); sync(); m.addEventListener('change', sync); return () => m.removeEventListener('change', sync); }, []);
  const renderActive = active && visible && pageVisible;
  return <div ref={host} className="intelligence" role="img" aria-label={`Folded particle topology representing ${state.mode || 'idle'} cognition`} onPointerMove={e => { if (reduced || paused) return; const r = e.currentTarget.getBoundingClientRect(); pointer.current = { x: (e.clientX - r.left) / r.width - 0.5, y: (e.clientY - r.top) / r.height - 0.5 }; }} onPointerLeave={() => { pointer.current = { x: 0, y: 0 }; }}>
    <RenderBoundary fallback={fallback}><Canvas frameloop={!renderActive ? 'never' : paused || reduced ? 'demand' : 'always'} camera={{ position: [0, 0, 5.7], fov: 43 }} dpr={[1, 1.8]} gl={{ antialias: false, alpha: true, powerPreference: 'high-performance' }}><Sculpture state={state} delta={delta} reduced={reduced} paused={paused} pointer={pointer} palette={palette} active={renderActive} /></Canvas></RenderBoundary>
  </div>;
}
