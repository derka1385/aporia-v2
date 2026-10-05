import React, { lazy, Suspense } from 'react';
import { createRoot } from 'react-dom/client';
import './boot.css';

const Landing = lazy(() => import('./landing/Landing.jsx'));
const LaboratoryApp = lazy(() => import('./App.jsx'));
const isLaboratory = /^\/app\/?$/.test(window.location.pathname);
document.title = isLaboratory ? 'APORIA · Cognitive laboratory' : 'APORIA · Reasoning under uncertainty';
document.querySelector('meta[name="theme-color"]').content = isLaboratory ? '#080b10' : '#121416';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Suspense fallback={<div className="route-loading" role="status">Opening APORIA…</div>}>
      {isLaboratory ? <LaboratoryApp /> : <Landing />}
    </Suspense>
  </React.StrictMode>,
);
